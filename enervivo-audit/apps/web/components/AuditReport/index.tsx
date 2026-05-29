import type { AuditReport as AuditReportType } from "@enervivo/shared-types";
import { ReportHeader } from "./Header";
import { KpiCards } from "./KpiCards";
import { Alerts } from "./Alerts";
import { JalonProgress } from "./JalonProgress";
import { JalonFilter } from "./JalonFilter";
import { UnclassifiedSection } from "./UnclassifiedSection";

export function AuditReport({ report }: { report: AuditReportType }) {
  return (
    <article className="bg-bg pb-16">
      <ReportHeader report={report} />
      <KpiCards report={report} />
      <Alerts report={report} />
      <JalonProgress report={report} />
      {/* Sélecteur + tableaux filtrés par jalon (cf maquette v6) */}
      <JalonFilter report={report} />
      <UnclassifiedSection report={report} />
    </article>
  );
}
