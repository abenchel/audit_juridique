import type { AuditReport } from "@enervivo/shared-types";
import { ExportHtmlButton } from "./ExportHtmlButton";

export function ReportHeader({ report }: { report: AuditReport }) {
  return (
    <div className="max-w-[1280px] mx-auto px-8 pt-12 pb-8">
      <div className="flex items-start justify-between gap-4 mb-4">
        <div className="text-xs uppercase tracking-wider text-ink-soft">
          Audit {report.audit_type} <span className="text-ink font-bold">/ {report.project_type}</span>
        </div>
        <ExportHtmlButton projectCode={report.project_code} auditId={report.audit_id} />
      </div>
      <h1 className="font-display font-bold text-5xl md:text-6xl text-ink leading-none tracking-tight mb-3">
        {report.project_code}{" "}
        <em className="not-italic text-[#00B685] font-medium">— {report.project_name}</em>
      </h1>

      <dl className="flex flex-wrap gap-8 mt-6 pt-6 border-t border-line text-sm">
        <div>
          <dt className="text-[10px] uppercase tracking-wider text-ink-soft font-bold mb-1">
            Date audit
          </dt>
          <dd className="font-bold text-ink">
            {report.completed_at
              ? new Date(report.completed_at).toLocaleString("fr-FR")
              : "En cours"}
          </dd>
        </div>
        <div>
          <dt className="text-[10px] uppercase tracking-wider text-ink-soft font-bold mb-1">
            Jalons audités
          </dt>
          <dd className="font-bold text-ink">{report.jalons_audited.join(", ")}</dd>
        </div>
        <div>
          <dt className="text-[10px] uppercase tracking-wider text-ink-soft font-bold mb-1">
            Fichiers scannés
          </dt>
          <dd className="font-bold text-ink">{report.total_files_scanned}</dd>
        </div>
        {report.model_used && (
          <div>
            <dt className="text-[10px] uppercase tracking-wider text-ink-soft font-bold mb-1">
              Modèle LLM
            </dt>
            <dd className="font-mono text-xs text-ink">{report.model_used}</dd>
          </div>
        )}
      </dl>
    </div>
  );
}
