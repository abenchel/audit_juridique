// Types manuels — gardent le frontend compilable même si generated.ts n'a pas
// encore tourné. À aligner sur apps/api/models/*.py.

export type AuditStatus = "pending" | "running" | "completed" | "failed";
export type DocumentStatus = "present" | "ambiguous" | "missing" | "other" | "error" | "not_applicable";
export type AuditType = "juridique" | "technique" | "financier";
export type Propriete = "Obligatoire" | "Facultatif" | "Cas par cas" | "Annexes 3 PDB" | "Informatif";

export interface ProjectSummary {
  code: string;
  name: string;
  type: string;
  current_jalon: string | null;
}

export interface ProjectOut extends ProjectSummary {
  sharepoint_url: string;
  power_mwc: number | null;
  department: string | null;
  created_at: string;
  updated_at: string;
}

export interface FoundFile {
  file_name: string;
  sharepoint_url: string;
  sharepoint_path: string;
  confidence: number;
  reason: string;
  file_hash: string | null;
}

export interface ExpectedDocument {
  code: string;
  name: string;
  propriete: Propriete;
  status: DocumentStatus;
  found_files: FoundFile[];
  note: string | null;
}

export interface JalonReport {
  jalon: string;
  total_expected: number;
  total_present: number;
  total_ambiguous: number;
  total_missing: number;
  completion_pct: number;
  documents: ExpectedDocument[];
}

export interface UnclassifiedFile {
  file_name: string;
  sharepoint_url: string;
  sharepoint_path: string;
  classified_type: string | null;
  confidence: number | null;
  reason: string | null;
}

export interface ErrorFile {
  file_name: string;
  sharepoint_url: string;
  sharepoint_path: string;
  error: string;
}

export interface IgnoredFile {
  file_name: string;
  sharepoint_url: string;
  sharepoint_path: string;
  mime_type: string;
  size: number;
  /** "video" | "image" | "presentation" | "spreadsheet" | "archive" | "cad" | "email" | "audio" | "other" */
  reason: string;
}

export interface AuditReport {
  audit_id: string;
  project_code: string;
  project_name: string;
  project_type: string;
  audit_type: AuditType;
  jalons_audited: string[];
  started_at: string;
  completed_at: string | null;
  model_used: string | null;
  total_files_scanned: number;
  total_expected: number;
  total_present: number;
  total_ambiguous: number;
  total_missing: number;
  overall_completion_pct: number;
  top_critical_missing: string[];
  jalons: JalonReport[];
  unclassified: UnclassifiedFile[];
  errors: ErrorFile[];
  /** Fichiers ignorés au listing (vidéos, images, pptx, etc.). Optionnel pour rétro-compat. */
  ignored?: IgnoredFile[];
}

export interface AuditSummary {
  id: string;
  project_code: string;
  audit_type: AuditType;
  status: AuditStatus;
  started_at: string;
  completed_at: string | null;
  total_expected: number | null;
  total_found: number | null;
  total_ambiguous: number | null;
  total_missing: number | null;
  // Versioning : version de l'outil au lancement + version du cache (la plus
  // ancienne tool_version des classifications réutilisées). Optionnels pour
  // rétro-compat avec les audits d'avant le versioning (→ null).
  tool_version?: string | null;
  cache_version?: string | null;
}

export interface AuditDetail extends AuditSummary {
  jalons: string[];
  result: AuditReport | null;
  error_message: string | null;
  // Snapshot de progression (renvoyé par l'API pour les audits running/pending)
  progress_total?: number | null;
  progress_done?: number | null;
  progress_current_file?: string | null;
}

export interface AuditCreateRequest {
  project_code: string;
  audit_type?: AuditType;
  jalons?: string[];
  // Relance « + nettoyer le cache » : purge les classifs du projet + re-classe tout.
  purge_cache?: boolean;
}

/** Une entrée du changelog de l'outil (config/tool_version.json). */
export interface ToolVersionEntry {
  version: string;
  date: string;
  description: string;
}

export interface AuditCreateResponse {
  id: string;
  status: AuditStatus;
}
