import type { AuditReport } from "@enervivo/shared-types";
import { overallStats, type CompletionScope } from "./completion";

export function KpiCards({
  report,
  currentJalon,
  scope,
}: {
  report: AuditReport;
  currentJalon: string | null;
  scope: CompletionScope;
}) {
  // Recalcul côté client selon le jalon actuel (cumul ≤ jalon) et le périmètre
  // (toutes les pièces / Obligatoire + Annexes 3). Sans filtre actif, on retombe
  // sur les chiffres du backend.
  const stats = overallStats(report, currentJalon, scope);
  const scopeLabel = scope === "required" ? "obligatoires + annexes 3" : "documents";

  return (
    <div className="max-w-[1280px] mx-auto px-8 pb-8">
      <div className="grid grid-cols-1 md:grid-cols-[1.4fr_1fr_1fr_1fr] gap-px bg-line border border-line rounded-lg overflow-hidden">
        {/* Feature cell */}
        <div className="bg-gradient-to-br from-ink to-[#155A4A] text-white p-7 relative overflow-hidden">
          <div className="absolute -top-10 -right-10 w-32 h-32 rounded-full bg-solar opacity-[0.18]" />
          <div className="text-[10px] uppercase tracking-wider opacity-70 font-bold mb-2">
            Complétude {currentJalon ? `jusqu'à ${currentJalon}` : "globale"}
          </div>
          <div className="font-display text-6xl font-bold leading-none">
            {stats.pct}
            <sup className="text-2xl font-semibold opacity-60 -top-5 ml-1">%</sup>
          </div>
          <div className="text-sm opacity-80 mt-2">
            {stats.present + stats.ambiguous} / {stats.expected} {scopeLabel} identifiés
          </div>
        </div>

        <KpiCell label="Trouvés" value={stats.present} accent="green" subtitle="conf. ≥ 70 %" />
        <KpiCell
          label="Ambigus"
          value={stats.ambiguous}
          accent="amber"
          subtitle="40 – 70 % — revue"
        />
        <KpiCell label="Manquants" value={stats.missing} accent="red" subtitle="à fournir" />
      </div>
    </div>
  );
}

function KpiCell({
  label,
  value,
  accent,
  subtitle,
}: {
  label: string;
  value: number;
  accent: "green" | "amber" | "red";
  subtitle: string;
}) {
  const dotClass = { green: "bg-green", amber: "bg-amber", red: "bg-red" }[accent];
  return (
    <div className="bg-bg-card p-7">
      <div className="text-[10px] uppercase tracking-wider text-ink-soft font-bold mb-2">
        {label}
      </div>
      <div className="font-display text-6xl font-bold leading-none text-ink">{value}</div>
      <div className="text-sm text-ink-mid mt-2 flex items-center gap-2">
        <span className={`w-2 h-2 rounded-full ${dotClass} inline-block`} />
        {subtitle}
      </div>
    </div>
  );
}
