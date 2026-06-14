"use client";

import { useState } from "react";
import type { AuditReport as AuditReportType } from "@enervivo/shared-types";
import { ReportHeader } from "./Header";
import { KpiCards } from "./KpiCards";
import { Alerts } from "./Alerts";
import { JalonProgress } from "./JalonProgress";
import { JalonFilter } from "./JalonFilter";
import { UnclassifiedSection } from "./UnclassifiedSection";
import { CurrentJalonSelector } from "./CurrentJalonSelector";
import type { CompletionScope } from "./completion";

export function AuditReport({ report }: { report: AuditReportType }) {
  // État partagé piloté par les sélecteurs en tête de rapport :
  //  - currentJalon : null = tous les jalons ; sinon cumul ≤ ce jalon.
  //  - scope        : périmètre des pièces comptées (toutes / requises).
  // KpiCards, Alerts et JalonProgress recalculent leur affichage en conséquence.
  const [currentJalon, setCurrentJalon] = useState<string | null>(null);
  const [scope, setScope] = useState<CompletionScope>("all");

  return (
    <article className="bg-bg pb-16">
      <ReportHeader report={report} />
      <CurrentJalonSelector
        report={report}
        currentJalon={currentJalon}
        onChange={setCurrentJalon}
      />
      <KpiCards report={report} currentJalon={currentJalon} scope={scope} />
      <Alerts report={report} currentJalon={currentJalon} />
      <JalonProgress
        report={report}
        currentJalon={currentJalon}
        scope={scope}
        onScopeChange={setScope}
      />
      {/* Sélecteur + tableaux filtrés par jalon (cf maquette v6) */}
      <JalonFilter report={report} />
      <UnclassifiedSection report={report} />
    </article>
  );
}
