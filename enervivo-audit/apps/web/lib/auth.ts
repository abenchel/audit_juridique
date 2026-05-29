import NextAuth, { type DefaultSession } from "next-auth";
import MicrosoftEntraID from "next-auth/providers/microsoft-entra-id";

export const ALLOWED_DOMAIN = process.env.ALLOWED_EMAIL_DOMAIN ?? "enervivo.fr";
const TENANT_ID = process.env.AZURE_AD_TENANT_ID ?? "";

declare module "next-auth" {
  interface Session {
    user: {
      id?: string;
      role?: "user" | "admin";
    } & DefaultSession["user"];
    accessToken?: string;
  }
}

export const { auth, handlers, signIn, signOut } = NextAuth({
  trustHost: true,
  providers: [
    MicrosoftEntraID({
      clientId: process.env.AZURE_AD_CLIENT_ID!,
      clientSecret: process.env.AZURE_AD_CLIENT_SECRET!,
      issuer: `https://login.microsoftonline.com/${TENANT_ID}/v2.0`,
      authorization: {
        params: {
          scope: "openid profile email User.Read",
          domain_hint: ALLOWED_DOMAIN,
        },
      },
    }),
  ],
  session: { strategy: "jwt" },
  callbacks: {
    async signIn({ profile }) {
      const profileAny = profile as Record<string, unknown> | null;
      const rawEmail =
        (profileAny?.email as string | undefined) ??
        (profileAny?.preferred_username as string | undefined) ??
        "";
      const email = rawEmail.toLowerCase();

      if (!email.endsWith(`@${ALLOWED_DOMAIN}`)) {
        console.warn(`[auth] Refused login from non-${ALLOWED_DOMAIN} email: ${email}`);
        return false;
      }

      // Bloquer comptes B2B invités d'un autre tenant
      const tid = profileAny?.tid as string | undefined;
      if (tid && TENANT_ID && tid !== TENANT_ID) {
        console.warn(`[auth] Refused login from foreign tenant: ${tid}`);
        return false;
      }
      return true;
    },
    async jwt({ token, account, profile }) {
      const profileAny = profile as Record<string, unknown> | undefined;
      if (account && profileAny) {
        token.email =
          (profileAny.email as string | undefined) ??
          (profileAny.preferred_username as string | undefined) ??
          token.email;
        token.name = (profileAny.name as string | undefined) ?? token.name;
        token.tid = profileAny.tid as string | undefined;
      }
      return token;
    },
    async session({ session, token }) {
      if (token.email) session.user.email = String(token.email);
      if (token.name) session.user.name = String(token.name);
      session.user.role = "user";
      return session;
    },
  },
  pages: {
    signIn: "/login",
    error: "/login?error=domain",
  },
});
