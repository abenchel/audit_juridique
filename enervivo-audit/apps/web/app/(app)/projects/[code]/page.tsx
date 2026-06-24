import Link from "next/link";
import { redirect } from "next/navigation";
import { createAudit, fetchAuditsForProject, fetchProject } from "@/lib/api-client";

interface PageProps {
  params: Promise<{ code: string }>;
}

export default async function ProjectDetailPage({ params }: PageProps) {
  const { code } = await params;
  const project = await fetchProject(code);
  const audits = await fetchAuditsForProject(code);

  // Deux modes de relance (toujours audit complet sur les 9 jalons) :
  //  - sans purge : on réutilise le cache (économie LLM).
  //  - avec purge : on nettoie le cache du projet → re-classification complète.
  async function launchAudit() {
    "use server";
    const res = await createAudit({
      project_code: code,
      audit_type: "juridique",
      jalons: [],
      purge_cache: false,
    });
    redirect(`/projects/${code}/audits/${res.id}`);
  }

  async function launchAuditPurge() {
    "use server";
    const res = await createAudit({
      project_code: code,
      audit_type: "juridique",
      jalons: [],
      purge_cache: true,
    });
    redirect(`/projects/${code}/audits/${res.id}`);
  }

  return (
    <div className="max-w-5xl mx-auto px-8 py-12">
      <Link href="/projects" className="text-xs uppercase tracking-wider text-ink-soft font-bold mb-3 inline-block hover:text-ink">
        ← Projets
      </Link>

      <div className="mb-10">
        <div className="text-xs uppercase tracking-wider text-ink-soft font-bold mb-3">{project.type}</div>
        <h1 className="font-display font-bold text-5xl text-ink leading-none mb-2">
          {project.code}
        </h1>
        <div className="text-ink-mid mt-3">{project.name}</div>

        <dl className="flex flex-wrap gap-8 mt-6 pt-6 border-t border-line text-sm">
          {project.current_jalon && (
            <div>
              <dt className="text-[10px] uppercase tracking-wider text-ink-soft font-bold mb-1">
                Jalon courant
              </dt>
              <dd className="font-bold text-ink">{project.current_jalon}</dd>
            </div>
          )}
          {project.power_mwc && (
            <div>
              <dt className="text-[10px] uppercase tracking-wider text-ink-soft font-bold mb-1">
                Puissance
              </dt>
              <dd className="font-bold text-ink">{project.power_mwc} MWc</dd>
            </div>
          )}
          <div>
            <dt className="text-[10px] uppercase tracking-wider text-ink-soft font-bold mb-1">
              SharePoint
            </dt>
            <dd>
              <a href={project.sharepoint_url} target="_blank" rel="noopener noreferrer" className="text-ink underline font-mono text-xs">
                {project.sharepoint_url}
              </a>
            </dd>
          </div>
        </dl>
      </div>

      <section className="bg-bg-card border border-line rounded-lg p-8 mb-8">
        <div className="flex items-start justify-between gap-6 flex-wrap">
          <div className="flex-1 min-w-[300px]">
            <h2 className="font-display text-2xl font-bold text-ink mb-1">Lancer un audit juridique</h2>
            <p className="text-sm text-ink-mid">
              Audit complet sur les <strong>9 jalons</strong>. Tu pourras filtrer la vue par
              jalon dans le rapport.
            </p>
            <ul className="text-xs text-ink-soft mt-3 space-y-1">
              <li>
                <strong className="text-ink-mid">Mise à jour de l&apos;audit</strong> — réutilise
                le cache de classification (rapide, économe).
              </li>
              <li>
                <strong className="text-ink-mid">+ nettoyer le cache</strong> — re-classifie tous
                les fichiers du projet avec la version courante de l&apos;outil (plus long).
              </li>
            </ul>
          </div>
          <div className="flex flex-col gap-2 min-w-[240px]">
            <form action={launchAudit}>
              <button
                type="submit"
                className="w-full bg-ink text-white px-6 py-3 rounded font-semibold hover:bg-[#155A4A] whitespace-nowrap"
              >
                Mise à jour de l&apos;audit →
              </button>
            </form>
            <form action={launchAuditPurge}>
              <button
                type="submit"
                className="w-full bg-white text-ink border border-ink px-6 py-3 rounded font-semibold hover:bg-bg whitespace-nowrap"
              >
                + nettoyer le cache
              </button>
            </form>
          </div>
        </div>
      </section>

      <section>
        <h2 className="font-display text-2xl font-bold text-ink mb-4">Historique des audits</h2>
        <div className="bg-bg-card border border-line rounded-lg overflow-hidden">
          {audits.length === 0 ? (
            <div className="p-8 text-center text-ink-soft text-sm">
              Aucun audit encore. Lance le premier ci-dessus.
            </div>
          ) : (
            <table className="w-full text-sm">
              <thead className="bg-bg-soft text-ink-soft text-xs uppercase tracking-wider">
                <tr>
                  <th className="text-left px-4 py-3">Date</th>
                  <th className="text-left px-4 py-3">Type</th>
                  <th className="text-left px-4 py-3">Statut</th>
                  <th className="text-left px-4 py-3">Présent</th>
                  <th className="text-left px-4 py-3">Ambigu</th>
                  <th className="text-left px-4 py-3">Manquant</th>
                  <th className="text-left px-4 py-3">Version outil</th>
                  <th className="text-left px-4 py-3">Version cache</th>
                  <th className="text-right px-4 py-3"></th>
                </tr>
              </thead>
              <tbody>
                {audits.map((a) => (
                  <tr key={a.id} className="border-t border-line hover:bg-bg-soft">
                    <td className="px-4 py-3 text-ink-mid font-mono text-xs">
                      {new Date(a.started_at).toLocaleString("fr-FR")}
                    </td>
                    <td className="px-4 py-3 font-semibold text-ink capitalize">{a.audit_type}</td>
                    <td className="px-4 py-3">
                      <StatusBadge status={a.status} />
                    </td>
                    <td className="px-4 py-3 text-green font-bold">{a.total_found ?? "—"}</td>
                    <td className="px-4 py-3 text-amber font-bold">{a.total_ambiguous ?? "—"}</td>
                    <td className="px-4 py-3 text-red font-bold">{a.total_missing ?? "—"}</td>
                    <td className="px-4 py-3 text-ink-mid font-mono text-xs">{a.tool_version ?? "—"}</td>
                    <td className="px-4 py-3 text-ink-mid font-mono text-xs">{a.cache_version ?? "—"}</td>
                    <td className="px-4 py-3 text-right">
                      <Link
                        href={`/projects/${code}/audits/${a.id}`}
                        className="text-ink font-semibold hover:underline"
                      >
                        Voir →
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </section>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const map = {
    pending: { bg: "bg-bg-soft", fg: "text-ink-soft", label: "En attente" },
    running: { bg: "bg-solar-soft", fg: "text-amber", label: "En cours" },
    completed: { bg: "bg-green-soft", fg: "text-green", label: "Terminé" },
    failed: { bg: "bg-red-soft", fg: "text-red", label: "Échec" },
  } as const;
  const c = map[status as keyof typeof map] ?? map.pending;
  return (
    <span className={`${c.bg} ${c.fg} px-2 py-1 rounded text-xs font-bold uppercase`}>
      {c.label}
    </span>
  );
}
