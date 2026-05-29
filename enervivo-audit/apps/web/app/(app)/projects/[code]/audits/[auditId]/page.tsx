import Link from "next/link";
import { revalidatePath } from "next/cache";
import { cancelAudit, fetchAudit, issueClientToken } from "@/lib/api-client";
import { AuditProgress } from "@/components/AuditProgress";
import { AuditReport } from "@/components/AuditReport";
import type { AuditReport as AuditReportType } from "@enervivo/shared-types";

interface PageProps {
  params: Promise<{ code: string; auditId: string }>;
}

export default async function AuditPage({ params }: PageProps) {
  const { code, auditId } = await params;
  const audit = await fetchAudit(auditId);

  if (audit.status === "failed") {
    return (
      <div className="max-w-3xl mx-auto px-8 py-16">
        <Link
          href={`/projects/${code}`}
          className="text-xs uppercase tracking-wider text-ink-soft font-bold mb-3 inline-block hover:text-ink"
        >
          ← Retour projet
        </Link>
        <h1 className="font-display text-4xl font-bold text-red mb-4">Audit échoué</h1>
        <div className="bg-red-soft border-l-4 border-red p-6 rounded">
          <p className="text-ink-mid text-sm">{audit.error_message ?? "Erreur inconnue"}</p>
        </div>
      </div>
    );
  }

  if (audit.status === "pending" || audit.status === "running") {
    const token = await issueClientToken();
    // Si un rapport partiel a déjà été reconstruit (engine.py le fait toutes
    // les 30s), on l'affiche AVEC la barre de progression et un bandeau "en cours".
    const hasPartial = audit.status === "running" && audit.result != null;

    async function cancelAction() {
      "use server";
      try {
        await cancelAudit(auditId);
      } catch {
        // Si l'audit est déjà terminé entre temps, ignore — la page va se re-render.
      }
      revalidatePath(`/projects/${code}/audits/${auditId}`);
    }

    return (
      <>
        <div className="max-w-[1280px] mx-auto px-8 pt-8">
          <Link
            href={`/projects/${code}`}
            className="text-xs uppercase tracking-wider text-ink-soft font-bold inline-block hover:text-ink"
          >
            ← Retour projet
          </Link>
        </div>
        <AuditProgress
          auditId={auditId}
          sseToken={token}
          initialTotal={audit.progress_total ?? null}
          initialDone={audit.progress_done ?? 0}
          initialCurrentFile={audit.progress_current_file ?? null}
          cancelAction={cancelAction}
        />
        {hasPartial && (
          <>
            <div className="max-w-[1280px] mx-auto px-8 mb-4">
              <div className="bg-solar-soft border-l-4 border-solar rounded p-4 text-sm">
                <strong className="font-bold text-ink">Rapport partiel</strong>{" "}
                <span className="text-ink-mid">
                  — l&apos;audit continue ({audit.progress_done ?? 0}/
                  {audit.progress_total ?? "?"} fichiers traités). Cette vue se met à
                  jour automatiquement toutes les 30 s.
                </span>
              </div>
            </div>
            <AuditReport report={audit.result as AuditReportType} />
          </>
        )}
      </>
    );
  }

  // Completed
  if (!audit.result) {
    return (
      <div className="max-w-3xl mx-auto px-8 py-16">
        <p className="text-ink-soft">Audit complété mais rapport vide.</p>
      </div>
    );
  }

  return (
    <>
      <div className="max-w-[1280px] mx-auto px-8 pt-8">
        <Link
          href={`/projects/${code}`}
          className="text-xs uppercase tracking-wider text-ink-soft font-bold inline-block hover:text-ink"
        >
          ← Retour projet
        </Link>
      </div>
      <AuditReport report={audit.result as AuditReportType} />
    </>
  );
}
