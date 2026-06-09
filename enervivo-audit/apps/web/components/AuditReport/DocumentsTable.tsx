import type { JalonReport, ExpectedDocument } from "@enervivo/shared-types";

/** Slug stable utilisé comme ancre URL (#jalon-XXX). */
export function jalonAnchorId(jalon: string): string {
  return `jalon-${jalon.replace(/\s+/g, "-")}`;
}

export function DocumentsTable({ jalon }: { jalon: JalonReport }) {
  return (
    <div
      id={jalonAnchorId(jalon.jalon)}
      className="max-w-[1280px] mx-auto px-8 pb-12 scroll-mt-24"
    >
      <div className="border-b border-line pb-4 mb-6">
        <h3 className="font-display text-2xl font-bold text-ink">{jalon.jalon}</h3>
        <p className="text-sm text-ink-soft mt-1">
          {jalon.total_expected} documents attendus — {jalon.completion_pct}% complétés
        </p>
      </div>

      <div className="bg-bg-card border border-line rounded-lg overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-bg-soft text-ink-soft text-[10px] uppercase tracking-wider font-bold">
            <tr>
              <th className="text-left px-4 py-3">Document attendu</th>
              <th className="text-left px-4 py-3">Propriété</th>
              <th className="text-left px-4 py-3">Statut</th>
              <th className="text-left px-4 py-3">Fichiers trouvés</th>
              <th className="text-right px-4 py-3">Confiance max</th>
            </tr>
          </thead>
          <tbody>
            {jalon.documents.map((d) => (
              <DocumentRow key={d.code} doc={d} />
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function DocumentRow({ doc }: { doc: ExpectedDocument }) {
  const status = doc.status;
  const map = {
    present: { bg: "bg-green-soft", fg: "text-green", label: "Trouvé" },
    ambiguous: { bg: "bg-amber-soft", fg: "text-amber", label: "Ambigu" },
    missing: { bg: "bg-red-soft", fg: "text-red", label: "Manquant" },
    not_applicable: { bg: "bg-bg-soft", fg: "text-ink-soft", label: "N/A" },
    other: { bg: "bg-violet-soft", fg: "text-violet", label: "Autre" },
    error: { bg: "bg-bg-soft", fg: "text-ink-soft", label: "Erreur" },
  } as const;
  const s = map[status] ?? map.missing;

  const maxConf = doc.found_files.reduce((m, f) => Math.max(m, f.confidence), 0);

  const proprieteAccent =
    doc.propriete === "Obligatoire"
      ? "bg-red-soft text-red"
      : doc.propriete === "Annexes 3 PDB"
        ? "bg-violet-soft text-violet"
        : "bg-bg-soft text-ink-mid";

  return (
    <tr className="border-t border-line hover:bg-bg-soft/50 align-top">
      <td className="px-4 py-3 font-semibold text-ink">
        {doc.name}
        {doc.note && <div className="text-xs text-ink-soft font-normal mt-1">{doc.note}</div>}
      </td>
      <td className="px-4 py-3">
        <span
          className={`${proprieteAccent} px-2 py-1 rounded text-[10px] font-bold uppercase whitespace-nowrap inline-block`}
        >
          {doc.propriete}
        </span>
      </td>
      <td className="px-4 py-3">
        <span className={`${s.bg} ${s.fg} px-2 py-1 rounded text-xs font-bold uppercase`}>
          {s.label}
        </span>
      </td>
      <td className="px-4 py-3">
        {doc.found_files.length === 0 ? (
          <span className="text-ink-soft text-xs italic">—</span>
        ) : (
          <ul className="space-y-1">
            {doc.found_files.map((f) => {
              const confClass =
                f.confidence >= 70
                  ? "bg-green-soft text-green"
                  : f.confidence >= 40
                    ? "bg-amber-soft text-amber"
                    : "bg-red-soft text-red";
              return (
                <li key={f.sharepoint_path}>
                  <span className="flex items-baseline gap-2">
                    <a
                      href={f.sharepoint_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-ink hover:underline font-mono text-xs"
                      title={f.reason}
                    >
                      {f.file_name}
                    </a>
                    <span
                      className={`${confClass} px-1.5 py-0.5 rounded font-mono text-[10px] font-bold shrink-0`}
                    >
                      {f.confidence}%
                    </span>
                  </span>
                  {f.reason && (
                    <div className="text-[11px] text-ink-soft italic mt-0.5">{f.reason}</div>
                  )}
                </li>
              );
            })}
          </ul>
        )}
      </td>
      <td className="px-4 py-3 text-right font-mono font-bold text-sm">
        {doc.found_files.length === 0 ? (
          <span className="text-ink-soft">—</span>
        ) : (
          <span className={s.fg}>{maxConf}%</span>
        )}
      </td>
    </tr>
  );
}
