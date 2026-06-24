import Link from "next/link";
import { auth, signOut } from "@/lib/auth";
import { fetchMe } from "@/lib/api-client";

export async function Sidebar() {
  const session = await auth();
  const email = session?.user?.email ?? "";
  const initials = email.slice(0, 2).toUpperCase();

  // Rôle réel calculé côté backend (ADMIN_EMAILS). Fallback "user" si l'appel
  // échoue (réseau/non connecté) — le lien admin reste alors masqué.
  let isAdmin = false;
  try {
    const me = await fetchMe();
    isAdmin = me.role === "admin";
  } catch {
    isAdmin = false;
  }

  return (
    <aside className="w-64 border-r border-line bg-bg-card flex flex-col">
      <div className="p-6 border-b border-line">
        <Link href="/projects" className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-solar relative">
            <div className="absolute inset-[6px] bg-ink rounded-full" />
          </div>
          <div>
            <div className="font-display text-lg font-bold text-ink leading-none">EnerVivo</div>
            <div className="text-[10px] uppercase tracking-wider text-ink-soft font-medium mt-1">
              Audit
            </div>
          </div>
        </Link>
      </div>

      <nav className="flex-1 p-4 space-y-1">
        <Link
          href="/projects"
          className="block px-3 py-2 rounded text-sm font-semibold text-ink hover:bg-bg-soft"
        >
          Projets
        </Link>
        {isAdmin && (
          <Link
            href="/changelog"
            className="block px-3 py-2 rounded text-sm font-semibold text-ink hover:bg-bg-soft"
          >
            Changelog
          </Link>
        )}
      </nav>

      <div className="p-4 border-t border-line">
        <div className="flex items-center gap-3 mb-3">
          <div className="w-8 h-8 rounded-full bg-bg-soft flex items-center justify-center font-semibold text-ink text-xs">
            {initials}
          </div>
          <div className="text-xs">
            <div className="font-semibold text-ink truncate max-w-[160px]">{email}</div>
            <div className="text-ink-soft">{isAdmin ? "Administrateur" : "Collaborateur"}</div>
          </div>
        </div>
        <form
          action={async () => {
            "use server";
            await signOut({ redirectTo: "/login" });
          }}
        >
          <button
            type="submit"
            className="w-full text-left text-xs text-ink-soft hover:text-ink py-1"
          >
            Se déconnecter
          </button>
        </form>
      </div>
    </aside>
  );
}
