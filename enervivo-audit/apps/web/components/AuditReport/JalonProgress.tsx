import type { AuditReport, JalonReport } from "@enervivo/shared-types";
import { jalonAnchorId } from "./DocumentsTable";

export function JalonProgress({ report }: { report: AuditReport }) {
  return (
    <div className="max-w-[1280px] mx-auto px-8 pb-8">
      <div className="border-b border-line pb-4 mb-6">
        <h2 className="font-display text-3xl font-bold text-ink">Progression par jalon</h2>
        <p className="text-sm text-ink-soft mt-1">
          Complétude des documents attendus par jalon — clique sur un jalon pour aller à sa section.
        </p>
      </div>
      <div className="flex flex-col gap-3">
        {report.jalons.map((j) => (
          <JalonRow key={j.jalon} jalon={j} />
        ))}
      </div>
    </div>
  );
}

function JalonRow({ jalon }: { jalon: JalonReport }) {
  const pct = jalon.completion_pct;
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
          <div className="text-xs text-ink-soft mt-0.5">{jalon.total_expected} attendus</div>
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
              {jalon.total_present} ✓ · {jalon.total_ambiguous} ⚠ · {jalon.total_missing} ✗
            </span>
          </div>
        </div>

        <div className="flex gap-2 text-xs items-center">
          <span className="bg-green-soft text-green px-3 py-1 rounded font-bold">
            {jalon.total_present} trouvés
          </span>
          <span className="bg-amber-soft text-amber px-3 py-1 rounded font-bold">
            {jalon.total_ambiguous} ambigus
          </span>
          <span className="bg-red-soft text-red px-3 py-1 rounded font-bold">
            {jalon.total_missing} manquants
          </span>
          <span className="text-ink-soft ml-1" aria-hidden>→</span>
        </div>
      </div>
    </a>
  );
}
