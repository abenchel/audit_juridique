"use client";

import { useEffect, useState } from "react";

interface ProgressEvent {
  event: "started" | "listed" | "progress" | "completed" | "failed";
  total?: number;
  done?: number;
  file?: string;
  error?: string;
}

export function AuditProgress({
  auditId,
  sseToken,
  initialTotal = null,
  initialDone = 0,
  initialCurrentFile = null,
  cancelAction,
}: {
  auditId: string;
  sseToken: string;
  initialTotal?: number | null;
  initialDone?: number;
  initialCurrentFile?: string | null;
  cancelAction?: () => Promise<void>;
}) {
  const [events, setEvents] = useState<ProgressEvent[]>([]);
  const [total, setTotal] = useState<number | null>(initialTotal);
  const [done, setDone] = useState(initialDone);
  const [currentFile, setCurrentFile] = useState<string | null>(initialCurrentFile);
  const [finished, setFinished] = useState<"completed" | "failed" | null>(null);

  useEffect(() => {
    const es = new EventSource(`/api/audits/${auditId}/stream?token=${encodeURIComponent(sseToken)}`);
    es.addEventListener("audit", (e) => {
      try {
        const data = JSON.parse((e as MessageEvent).data) as ProgressEvent;
        setEvents((p) => [...p.slice(-50), data]);
        if (data.event === "listed" && data.total != null) setTotal(data.total);
        if (data.event === "progress") {
          setDone(data.done ?? 0);
          setCurrentFile(data.file ?? null);
        }
        if (data.event === "completed") {
          setFinished("completed");
          es.close();
          setTimeout(() => location.reload(), 800);
        }
        if (data.event === "failed") {
          setFinished("failed");
          es.close();
        }
      } catch {
        // ignore
      }
    });
    es.onerror = () => {
      es.close();
    };
    return () => es.close();
  }, [auditId, sseToken]);

  const pct = total ? Math.round((100 * done) / total) : 0;

  return (
    <div className="max-w-3xl mx-auto px-8 py-16">
      <div className="text-center mb-10">
        <div className="text-xs uppercase tracking-wider text-ink-soft font-bold mb-3">
          Audit en cours
        </div>
        <h1 className="font-display font-bold text-4xl text-ink mb-3">
          {finished === "failed" ? "Audit échoué" : finished === "completed" ? "Audit terminé" : "Analyse des documents…"}
        </h1>
        <p className="text-ink-mid text-sm">
          {total ? `${done} / ${total} fichiers traités` : "Listing SharePoint…"}
        </p>
        {/* Bouton d'annulation — visible tant que l'audit tourne */}
        {!finished && cancelAction && (
          <form
            action={cancelAction}
            className="mt-6"
            onSubmit={(e) => {
              if (!confirm("Arrêter cet audit ? Les fichiers déjà traités seront conservés.")) {
                e.preventDefault();
              }
            }}
          >
            <button
              type="submit"
              className="text-red border border-red px-4 py-2 rounded text-sm font-semibold hover:bg-red-soft transition-colors"
            >
              ✕ Arrêter l&apos;audit
            </button>
          </form>
        )}
      </div>

      <div className="bg-bg-card border border-line rounded-lg p-8 mb-6">
        <div className="h-3 bg-bg-soft rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-ink to-green transition-all duration-300"
            style={{ width: `${pct}%` }}
          />
        </div>
        <div className="flex justify-between items-center mt-3 text-sm">
          <span className="text-ink-soft font-mono">{pct}%</span>
          {currentFile && (
            <span className="text-ink-mid font-mono text-xs truncate max-w-md" title={currentFile}>
              {currentFile}
            </span>
          )}
        </div>
      </div>

      <div className="bg-bg-card border border-line rounded-lg p-4 max-h-72 overflow-y-auto font-mono text-xs space-y-1">
        {events.map((e, i) => (
          <div key={i} className="text-ink-mid">
            <span className="text-ink-soft">[{e.event}]</span>{" "}
            {e.file ?? e.error ?? `${e.done ?? ""}/${e.total ?? ""}`}
          </div>
        ))}
        {events.length === 0 && <div className="text-ink-soft italic">En attente d&apos;événements…</div>}
      </div>
    </div>
  );
}
