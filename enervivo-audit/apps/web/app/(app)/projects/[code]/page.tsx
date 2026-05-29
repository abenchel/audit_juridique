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

  async function launchAudit() {
    "use server";
    // Toujours audit complet sur les 9 jalons (référentiel V11).
    // Le filtre par jalon se fait côté UI dans le rapport.
    const res = await createAudit({
      project_code: code,
      audit_type: "juridique",
      jalons: [],
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
              Audit complet sur les <strong>9 jalons</strong> (107 documents attendus).
              Tu pourras filtrer la vue par jalon dans le rapport, et cliquer sur un jalon
              dans la barre de progression pour aller directement à sa section.
            </p>
          </div>
          <form action={launchAudit}>
            <button
              type="submit"
              className="bg-ink text-white px-6 py-3 rounded font-semibold hover:bg-[#155A4A] whitespace-nowrap"
            >
              Lancer audit complet →
            </button>
          </form>
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
