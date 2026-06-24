import Link from "next/link";
import { fetchChangelog } from "@/lib/api-client";
import type { ToolVersionEntry } from "@enervivo/shared-types";

// Changelog de l'outil — réservé aux admins (ADMIN_EMAILS). L'endpoint renvoie
// 403 pour un non-admin → on affiche un message d'accès refusé plutôt que de
// planter. Le lien vers cette page n'apparaît dans la Sidebar que pour les admins.
export default async function ChangelogPage() {
  let entries: ToolVersionEntry[] | null = null;
  let denied = false;
  try {
    entries = await fetchChangelog();
  } catch {
    denied = true;
  }

  return (
    <div className="max-w-3xl mx-auto px-8 py-12">
      <Link
        href="/projects"
        className="text-xs uppercase tracking-wider text-ink-soft font-bold mb-3 inline-block hover:text-ink"
      >
        ← Projets
      </Link>

      <h1 className="font-display font-bold text-4xl text-ink mb-2">Changelog de l&apos;outil</h1>
      <p className="text-sm text-ink-mid mb-8">
        Historique des versions de l&apos;outil d&apos;audit. La version courante est enregistrée
        sur chaque audit lancé.
      </p>

      {denied ? (
        <div className="bg-red-soft border-l-4 border-red rounded p-6 text-sm text-ink-mid">
          Accès réservé aux administrateurs.
        </div>
      ) : !entries || entries.length === 0 ? (
        <div className="bg-bg-card border border-line rounded-lg p-8 text-center text-ink-soft text-sm">
          Aucune version enregistrée.
        </div>
      ) : (
        <ol className="space-y-4">
          {[...entries].reverse().map((e, i) => {
            const isCurrent = i === 0; // après reverse, la 1ʳᵉ = dernière entrée = courante
            return (
              <li
                key={e.version}
                className={`bg-bg-card border rounded-lg p-5 ${
                  isCurrent ? "border-l-4 border-l-green border-line" : "border-line"
                }`}
              >
                <div className="flex items-center gap-3 mb-1">
                  <span className="font-display text-xl font-bold text-ink">{e.version}</span>
                  {isCurrent && (
                    <span className="bg-green-soft text-green px-2 py-0.5 rounded text-[10px] font-bold uppercase">
                      Version courante
                    </span>
                  )}
                  <span className="text-xs text-ink-soft ml-auto font-mono">{e.date}</span>
                </div>
                <p className="text-sm text-ink-mid">{e.description}</p>
              </li>
            );
          })}
        </ol>
      )}
    </div>
  );
}
