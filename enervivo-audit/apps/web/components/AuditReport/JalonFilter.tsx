"use client";

import type { AuditReport as AuditReportType, JalonReport } from "@enervivo/shared-types";
import { useState } from "react";
import { DocumentsTable } from "./DocumentsTable";

/**
 * Sélecteur de jalon de vue (cf maquette rapport_audit_DDENIS_v6.html).
 * L'audit contient déjà tous les jalons dans `report.jalons` — on filtre juste
 * l'affichage, on ne relance rien. "Tous" affiche tous les tableaux.
 */
export function JalonFilter({ report }: { report: AuditReportType }) {
  const [selected, setSelected] = useState<string>("all");

  const visible: JalonReport[] =
    selected === "all" ? report.jalons : report.jalons.filter((j) => j.jalon === selected);

  return (
    <div className="max-w-[1280px] mx-auto px-8">
      <div className="flex items-center gap-3 mb-4 bg-bg-card border border-line rounded-lg px-6 py-4">
        <label className="text-xs uppercase tracking-wider text-ink-soft font-bold" htmlFor="jalon-view">
          Voir
        </label>
        <select
          id="jalon-view"
          value={selected}
          onChange={(e) => setSelected(e.target.value)}
          className="border border-line rounded px-3 py-2 text-sm font-semibold bg-white text-ink"
        >
          <option value="all">Tous les jalons ({report.jalons.length})</option>
          {report.jalons.map((j) => (
            <option key={j.jalon} value={j.jalon}>
              {j.jalon} — {j.total_expected} attendus · {j.completion_pct}%
            </option>
          ))}
        </select>
        {selected !== "all" && (
          <button
            type="button"
            onClick={() => setSelected("all")}
            className="text-xs text-ink-soft hover:text-ink underline ml-auto"
          >
            Réinitialiser
          </button>
        )}
      </div>

      {visible.map((j) => (
        <DocumentsTable key={j.jalon} jalon={j} />
      ))}
    </div>
  );
}
