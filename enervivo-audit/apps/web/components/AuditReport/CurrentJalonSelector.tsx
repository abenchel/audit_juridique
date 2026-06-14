"use client";

import type { AuditReport } from "@enervivo/shared-types";
import { jalonRank } from "./completion";

// Sélecteur "Jalon actuel" : choisit le jalon où en est le projet. La complétude
// globale, les documents critiques et la progression sont alors calculés en
// CUMUL sur tous les jalons ≤ celui choisi (à J3, tout l'antérieur doit être là).
// "Tous les jalons" = pas de filtre (vue d'ensemble, défaut).
export function CurrentJalonSelector({
  report,
  currentJalon,
  onChange,
}: {
  report: AuditReport;
  currentJalon: string | null;
  onChange: (jalon: string | null) => void;
}) {
  // Jalons présents dans le rapport, dans l'ordre chronologique.
  const jalons = [...report.jalons.map((j) => j.jalon)].sort(
    (a, b) => jalonRank(a) - jalonRank(b),
  );

  return (
    <div className="max-w-[1280px] mx-auto px-8 pb-6">
      <div className="bg-bg-card border border-line rounded-lg p-4 flex flex-wrap items-center gap-3">
        <label
          htmlFor="current-jalon"
          className="text-xs uppercase tracking-wider text-ink-soft font-bold"
        >
          Jalon actuel du projet
        </label>
        <select
          id="current-jalon"
          value={currentJalon ?? ""}
          onChange={(e) => onChange(e.target.value || null)}
          className="border border-line rounded-md bg-bg px-3 py-1.5 text-sm font-semibold text-ink focus:outline-none focus:border-ink-soft"
        >
          <option value="">Tous les jalons (vue d&apos;ensemble)</option>
          {jalons.map((j) => (
            <option key={j} value={j}>
              {j}
            </option>
          ))}
        </select>
        <span className="text-xs text-ink-soft">
          {currentJalon
            ? `Complétude et documents critiques cumulés jusqu'à « ${currentJalon} » inclus.`
            : "Sélectionne un jalon pour ne mesurer que les documents attendus jusqu'à ce stade."}
        </span>
      </div>
    </div>
  );
}
