import { signIn } from "@/lib/auth";

interface LoginPageProps {
  searchParams: Promise<{ error?: string; from?: string }>;
}

export default async function LoginPage({ searchParams }: LoginPageProps) {
  const { error, from } = await searchParams;
  const errorMsg =
    error === "domain"
      ? "Accès réservé aux collaborateurs @enervivo.fr."
      : error
        ? "Erreur d'authentification. Réessaie."
        : null;

  return (
    <main className="min-h-screen flex items-center justify-center bg-bg px-4">
      <div className="bg-bg-card p-10 rounded-lg shadow-md max-w-md w-full border border-line">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-8 h-8 rounded-full bg-solar relative">
            <div className="absolute inset-[6px] bg-ink rounded-full" />
          </div>
          <span className="font-display text-2xl font-bold text-ink">EnerVivo</span>
          <span className="text-xs uppercase tracking-wider text-ink-soft font-medium">Audit</span>
        </div>

        <h1 className="text-2xl font-display font-bold text-ink mb-2">Connexion</h1>
        <p className="text-ink-mid text-sm mb-8">
          Outil d&apos;audit r&eacute;serv&eacute; aux collaborateurs <strong>@enervivo.fr</strong>.
        </p>

        {errorMsg && (
          <div className="bg-red-soft border-l-4 border-red text-red px-4 py-3 mb-6 rounded text-sm">
            {errorMsg}
          </div>
        )}

        <form
          action={async () => {
            "use server";
            await signIn("microsoft-entra-id", { redirectTo: from || "/projects" });
          }}
        >
          <button
            type="submit"
            className="w-full bg-ink text-white py-3 px-4 rounded font-semibold hover:bg-[#155A4A] transition-colors"
          >
            Se connecter avec Outlook EnerVivo
          </button>
        </form>

        <p className="text-xs text-ink-soft mt-6 text-center">
          Authentification SSO Microsoft Entra ID
        </p>
      </div>
    </main>
  );
}
