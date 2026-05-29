import type { AuditReport } from "@enervivo/shared-types";

const REASON_LABELS: Record<string, string> = {
  video: "Vidéo",
  audio: "Audio",
  archive: "Archive (zip)",
  cad: "Plan CAO (.dwg)",
  gis: "Fichier SIG (QGIS / shapefile)",
  technique_binary: "Outil technique (PVsyst, D5Render, MS Project, script .py)",
  point_cloud: "Nuage de points / photogrammétrie",
  web: "Page web (.html)",
  // Anciens labels conservés pour compat rétro (audits déjà en BDD)
  image: "Image",
  presentation: "Présentation",
  spreadsheet: "Tableur",
  email: "Email",
  other: "Autre",
};

function formatBytes(n: number): string {
  if (n < 1024) return `${n} B`;
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`;
  if (n < 1024 * 1024 * 1024) return `${(n / (1024 * 1024)).toFixed(1)} MB`;
  return `${(n / (1024 * 1024 * 1024)).toFixed(1)} GB`;
}

export function UnclassifiedSection({ report }: { report: AuditReport }) {
  const ignored = report.ignored ?? [];
  if (
    report.unclassified.length === 0 &&
    report.errors.length === 0 &&
    ignored.length === 0
  )
    return null;

  return (
    <div className="max-w-[1280px] mx-auto px-8 pb-12 space-y-8">
      {report.unclassified.length > 0 && (
        <section>
          <div className="border-b border-line pb-4 mb-6">
            <h3 className="font-display text-2xl font-bold text-ink">Documents non identifiés</h3>
            <p className="text-sm text-ink-soft mt-1">
              {report.unclassified.length} fichier(s) sans correspondance dans le référentiel V11.
            </p>
          </div>
          <div className="bg-bg-card border border-line rounded-lg overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-bg-soft text-ink-soft text-[10px] uppercase tracking-wider font-bold">
                <tr>
                  <th className="text-left px-4 py-3">Fichier</th>
                  <th className="text-left px-4 py-3">Type LLM</th>
                  <th className="text-right px-4 py-3">Confiance</th>
                </tr>
              </thead>
              <tbody>
                {report.unclassified.map((u) => (
                  <tr key={u.sharepoint_path} className="border-t border-line">
                    <td className="px-4 py-3 font-mono text-xs">
                      <a
                        href={u.sharepoint_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-ink hover:underline"
                      >
                        {u.file_name}
                      </a>
                      {u.reason && (
                        <div className="text-[11px] text-ink-soft italic mt-0.5 font-sans">{u.reason}</div>
                      )}
                    </td>
                    <td className="px-4 py-3 text-ink-mid">{u.classified_type ?? "—"}</td>
                    <td className="px-4 py-3 text-right font-mono">{u.confidence ?? "—"}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      )}

      {report.errors.length > 0 && (
        <section>
          <div className="border-b border-line pb-4 mb-6">
            <h3 className="font-display text-2xl font-bold text-ink">Erreurs techniques</h3>
            <p className="text-sm text-ink-soft mt-1">
              {report.errors.length} fichier(s) illisibles (protégés, corrompus, scan sans OCR).
            </p>
          </div>
          <div className="bg-bg-card border border-line rounded-lg overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-bg-soft text-ink-soft text-[10px] uppercase tracking-wider font-bold">
                <tr>
                  <th className="text-left px-4 py-3">Fichier</th>
                  <th className="text-left px-4 py-3">Erreur</th>
                </tr>
              </thead>
              <tbody>
                {report.errors.map((e) => (
                  <tr key={e.sharepoint_path} className="border-t border-line">
                    <td className="px-4 py-3 font-mono text-xs">
                      <a
                        href={e.sharepoint_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-ink hover:underline"
                      >
                        {e.file_name}
                      </a>
                    </td>
                    <td className="px-4 py-3 text-red text-xs">{e.error}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      )}

      {ignored.length > 0 && (
        <section>
          <div className="border-b border-line pb-4 mb-6">
            <h3 className="font-display text-2xl font-bold text-ink">Fichiers ignorés</h3>
            <p className="text-sm text-ink-soft mt-1">
              {ignored.length} fichier(s) écartés au listing (vidéos, images,
              présentations, tableurs, etc. — non classifiables par le pipeline juridique).
            </p>
          </div>
          <div className="bg-bg-card border border-line rounded-lg overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-bg-soft text-ink-soft text-[10px] uppercase tracking-wider font-bold">
                <tr>
                  <th className="text-left px-4 py-3">Fichier</th>
                  <th className="text-left px-4 py-3">Type</th>
                  <th className="text-right px-4 py-3">Taille</th>
                </tr>
              </thead>
              <tbody>
                {ignored.map((i) => (
                  <tr key={i.sharepoint_path} className="border-t border-line">
                    <td className="px-4 py-3 font-mono text-xs">
                      <a
                        href={i.sharepoint_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-ink hover:underline"
                      >
                        {i.file_name}
                      </a>
                    </td>
                    <td className="px-4 py-3 text-ink-mid">
                      {REASON_LABELS[i.reason] ?? i.reason}
                    </td>
                    <td className="px-4 py-3 text-right font-mono text-xs text-ink-soft">
                      {formatBytes(i.size)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      )}
    </div>
  );
}
