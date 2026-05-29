import { handlers } from "@/lib/auth";

export const { GET, POST } = handlers;

// IMPORTANT : ce handler doit être placé sur /api/auth/* — nginx redirige
// explicitement /api/auth/ vers le service web (Next.js) et /api/* vers FastAPI.
// Voir infra/nginx/conf.d/default.conf.

export const dynamic = "force-dynamic";
