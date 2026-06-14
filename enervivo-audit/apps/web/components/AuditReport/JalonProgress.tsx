"use client";

import { useMemo } from "react";
import type { AuditReport, JalonReport } from "@enervivo/shared-types";
import { jalonAnchorId } from "./DocumentsTable";
import { jalonsUpTo, statsForDocuments, type CompletionScope } from "./completion";

export function JalonProgress({
  report,
  currentJalon,
  scope,
  onScopeChange,
}: {
  report: AuditReport;
  currentJalon: string | null;
  scope: CompletionScope;
  onScopeChange: (s: CompletionScope) => void;
}) {
  // Quand un "jalon actuel" est choisi, on ne montre que les jalons ≤ celui-ci
  // (cumul) — cohérent avec la complétude globale et les documents critiques.
  const visibleJalons = jalonsUpTo(report.jalons, currentJalon);

  return (
    <div className="max-w-[1280px] mx-auto px-8 pb-8">
      <div className="border-b border-line pb-4 mb-6 flex flex-wrap items-end justify-between gap-4">
        <div>
          <h2 className="font-display text-3xl font-bold text-ink">Progression par jalon</h2>
          <p className="text-sm text-ink-soft mt-1">
            Complétude des documents attendus par jalon — clique sur un jalon pour aller à sa
            section.
          </p>
        </div>
        <CompletionToggle scope={scope} onChange={onScopeChange} />
      </div>
      <div className="flex flex-col gap-3">
        {visibleJalons.map((j) => (
          <JalonRow key={j.jalon} jalon={j} scope={scope} />
        ))}
      </div>
    </div>
  );
}

function CompletionToggle({
  scope,
  onChange,
}: {
  scope: CompletionScope;
  onChange: (s: CompletionScope) => void;
}) {
  const options: { value: CompletionScope; label: string }[] = [
    { value: "all", label: "Toutes les pièces" },
    { value: "required", label: "Obligatoire + Annexes 3" },
  ];
  return (
    <div className="inline-flex rounded-lg border border-line bg-bg-card p-1 text-xs font-bold">
      {options.map((o) => (
        <button
          key={o.value}
          type="button"
          onClick={() => onChange(o.value)}
          aria-pressed={scope === o.value}
          className={`px-3 py-1.5 rounded-md transition-colors ${
            scope === o.value ? "bg-ink text-white" : "text-ink-soft hover:text-ink"
          }`}
        >
          {o.label}
        </button>
      ))}
    </div>
  );
}

function JalonRow({ jalon, scope }: { jalon: JalonReport; scope: CompletionScope }) {
  const stats = useMemo(() => statsForDocuments(jalon.documents, scope), [jalon.documents, scope]);
  const pct = stats.pct;
  const status = pct >= 90 ? "done" : pct >= 50 ? "active" : "pending";
  // Les jalons "longs" (ex. "J5_Construction", "J7_Cloture") débordaient de la
  // colonne label et chevauchaient la barre de progression. On découpe le code
  // court (J5) du suffixe (Construction) UNIQUEMENT pour les codes de forme "Jx_…".
  // Les libellés sans ce motif (ex. "Avant J1") restent affichés entiers.
  const jalonMatch = jalon.jalon.match(/^(J\d+[a-z]?)[_ ](.+)$/);
  const jalonCode = jalonMatch ? jalonMatch[1] : jalon.jalon;
  const jalonLabel = jalonMatch ? jalonMatch[2] : "";
  const borderClass =
    status === "done"
      ? "border-l-4 border-l-green"
      : status === "active"
        ? "border-l-4 border-l-solar bg-gradient-to-r from-solar-soft to-transparent"
        : "border-l-4 border-l-line";

  return (
    <a
      href={`#${jalonAnchorId(jalon.jalon)}`}
      className={`block bg-bg-card border border-line rounded-lg p-5 ${borderClass} hover:border-ink-soft hover:shadow-sm transition-all cursor-pointer no-underline`}
    >
      <div className="grid grid-cols-1 md:grid-cols-[140px_1fr_360px] gap-8 items-center">
        <div className="min-w-0">
          <div className="font-display text-2xl font-bold text-ink leading-tight">
            {jalonCode}
          </div>
          {jalonLabel && (
            <div className="text-sm font-semibold text-ink-mid leading-tight truncate">
              {jalonLabel}
            </div>
          )}
          <div className="text-xs text-ink-soft mt-0.5">{stats.expected} attendus</div>
        </div>

        <div>
          <div className="h-2 bg-bg-soft rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-ink to-green"
              style={{ width: `${pct}%` }}
            />
          </div>
          <div className="text-xs text-ink-mid mt-2 flex justify-between">
            <span>{pct}% complet</span>
            <span>
              {stats.present} ✓ · {stats.ambiguous} ⚠ · {stats.missing} ✗
            </span>
          </div>
        </div>

        <div className="flex gap-2 text-xs items-center">
          <span className="bg-green-soft text-green px-3 py-1 rounded font-bold">
            {stats.present} trouvés
          </span>
          <span className="bg-amber-soft text-amber px-3 py-1 rounded font-bold">
            {stats.ambiguous} ambigus
          </span>
          <span className="bg-red-soft text-red px-3 py-1 rounded font-bold">
            {stats.missing} manquants
          </span>
          <span className="text-ink-soft ml-1" aria-hidden>
            →
          </span>
        </div>
      </div>
    </a>
  );
}
