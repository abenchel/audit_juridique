// Client API typé — appelle FastAPI côté serveur (Next.js Server Components/Actions).
// Signe un JWT HS256 avec NEXTAUTH_SECRET qu'on partage avec le backend (cf.
// apps/api/services/auth/jwt_verify.py).

import "server-only";
import { SignJWT } from "jose";
import { auth } from "@/lib/auth";
import type {
  AuditCreateRequest,
  AuditCreateResponse,
  AuditDetail,
  AuditSummary,
  ProjectOut,
  ProjectSummary,
  ToolVersionEntry,
} from "@enervivo/shared-types";

export interface MeInfo {
  email: string;
  name: string;
  role: "user" | "admin";
}

const API_INTERNAL_URL =
  process.env.API_INTERNAL_URL ?? // Docker compose : http://api:8000
  process.env.NEXT_PUBLIC_API_URL ?? // Dev hors Docker
  "http://localhost:11118";

const NEXTAUTH_SECRET = process.env.NEXTAUTH_SECRET ?? "";

async function signJwt(email: string, name: string): Promise<string> {
  const secret = new TextEncoder().encode(NEXTAUTH_SECRET);
  return await new SignJWT({ email, name, role: "user" })
    .setProtectedHeader({ alg: "HS256" })
    .setIssuedAt()
    .setExpirationTime("10m")
    .sign(secret);
}

async function getAuthHeader(): Promise<HeadersInit> {
  const session = await auth();
  if (!session?.user?.email) {
    throw new Error("Non authentifié");
  }
  const token = await signJwt(session.user.email, session.user.name ?? session.user.email);
  return { Authorization: `Bearer ${token}`, "Content-Type": "application/json" };
}

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const headers = await getAuthHeader();
  const res = await fetch(`${API_INTERNAL_URL}/api${path}`, {
    ...init,
    headers: { ...headers, ...(init?.headers ?? {}) },
    cache: "no-store",
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API ${res.status} ${path}: ${text.slice(0, 200)}`);
  }
  return (await res.json()) as T;
}

// ---------- Endpoints ----------

export async function fetchProjects(): Promise<ProjectSummary[]> {
  return apiFetch<ProjectSummary[]>("/projects");
}

export async function fetchProject(code: string): Promise<ProjectOut> {
  return apiFetch<ProjectOut>(`/projects/${encodeURIComponent(code)}`);
}

export async function createAudit(req: AuditCreateRequest): Promise<AuditCreateResponse> {
  return apiFetch<AuditCreateResponse>("/audits", {
    method: "POST",
    body: JSON.stringify(req),
  });
}

export async function fetchAudit(id: string): Promise<AuditDetail> {
  return apiFetch<AuditDetail>(`/audits/${id}`);
}

export async function cancelAudit(id: string): Promise<{ id: string; status: string; cancelled: boolean }> {
  return apiFetch(`/audits/${id}/cancel`, { method: "POST" });
}

export async function fetchAuditsForProject(code: string): Promise<AuditSummary[]> {
  return apiFetch<AuditSummary[]>(`/audits/project/${encodeURIComponent(code)}`);
}

/** Profil de l'utilisateur courant (dont le rôle réel, calculé côté backend). */
export async function fetchMe(): Promise<MeInfo> {
  return apiFetch<MeInfo>("/auth/me");
}

/** Changelog de l'outil (admin only — l'API renvoie 403 sinon). */
export async function fetchChangelog(): Promise<ToolVersionEntry[]> {
  return apiFetch<ToolVersionEntry[]>("/admin/changelog");
}

// Pour SSE (client-side) — on issue un token côté serveur et on le passe via query
export async function issueClientToken(): Promise<string> {
  const session = await auth();
  if (!session?.user?.email) throw new Error("Non authentifié");
  return signJwt(session.user.email, session.user.name ?? session.user.email);
}
