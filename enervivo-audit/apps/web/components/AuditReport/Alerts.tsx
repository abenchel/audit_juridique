import type { AuditReport } from "@enervivo/shared-types";
import { criticalMissing } from "./completion";

export function Alerts({
  report,
  currentJalon,
}: {
  report: AuditReport;
  currentJalon: string | null;
}) {
  // Documents obligatoires manquants recalculés selon le jalon actuel (cumul ≤
  // jalon). Recalcul nécessaire : top_critical_missing du backend ne porte pas
  // l'info de jalon, donc on ne pourrait pas le filtrer.
  const missing = criticalMissing(report, currentJalon);
  if (missing.length === 0) return null;
  return (
    <div className="max-w-[1280px] mx-auto px-8 pb-8">
      <div className="bg-red-soft border-l-4 border-red rounded-lg p-6">
        <div className="flex items-start gap-4">
          <div className="text-2xl">⚠</div>
          <div className="flex-1">
            <div className="text-[10px] uppercase tracking-wider text-red font-bold mb-2">
              Documents critiques manquants
            </div>
            <div className="font-display text-xl font-bold text-ink mb-3">
              {missing.length} document{missing.length > 1 ? "s" : ""} obligatoire
              {missing.length > 1 ? "s" : ""} à fournir
              {currentJalon ? ` (jusqu'à ${currentJalon})` : ""}
            </div>
            <ul className="space-y-1.5">
              {missing.map((name) => (
                <li key={name} className="flex items-start gap-2 text-sm text-ink-mid">
                  <span className="text-red font-bold">·</span>
                  <span>{name}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
