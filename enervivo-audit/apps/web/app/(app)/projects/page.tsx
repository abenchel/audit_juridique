import Link from "next/link";
import { fetchProjects } from "@/lib/api-client";

export default async function ProjectsPage() {
  let projects: Awaited<ReturnType<typeof fetchProjects>> = [];
  let error: string | null = null;
  try {
    projects = await fetchProjects();
  } catch (e) {
    error = (e as Error).message;
  }

  return (
    <div className="max-w-6xl mx-auto px-8 py-12">
      <div className="mb-10">
        <div className="text-xs uppercase tracking-wider text-ink-soft font-bold mb-3">
          Tableau de bord
        </div>
        <h1 className="font-display font-bold text-5xl text-ink leading-none mb-2">
          Projets <em className="not-italic text-[#00B685] font-medium">à auditer</em>
        </h1>
        <p className="text-ink-mid text-sm mt-4">
          Sélectionne un projet pour lancer un audit juridique sur ses jalons.
        </p>
      </div>

      {error && (
        <div className="bg-red-soft border-l-4 border-red text-red px-4 py-3 mb-6 rounded text-sm">
          ⚠ Impossible de charger les projets : {error}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {projects.map((p) => (
          <Link
            key={p.code}
            href={`/projects/${p.code}`}
            className="bg-bg-card border border-line rounded-lg p-6 hover:border-ink hover:shadow-md transition-all"
          >
            <div className="flex items-start justify-between mb-4">
              <div>
                <div className="text-[10px] uppercase tracking-wider text-ink-soft font-bold mb-1">
                  {p.type}
                </div>
                <div className="font-display text-2xl font-bold text-ink leading-tight">
                  {p.code}
                </div>
              </div>
              {p.current_jalon && (
                <span className="bg-solar-soft text-amber px-3 py-1 rounded text-xs font-bold uppercase">
                  {p.current_jalon}
                </span>
              )}
            </div>
            <div className="text-sm text-ink-mid">{p.name}</div>
          </Link>
        ))}
        {projects.length === 0 && !error && (
          <div className="col-span-full text-center py-12 text-ink-soft">
            Aucun projet — lance <code className="font-mono text-xs">make seed</code>.
          </div>
        )}
      </div>
    </div>
  );
}
