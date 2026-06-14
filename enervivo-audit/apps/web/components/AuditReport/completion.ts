// Logique de complétude recalculée côté client, partagée par KpiCards / Alerts /
// JalonProgress. Tout est dérivé du rapport (jalons[].documents : status +
// propriete), donc aucun appel backend ni re-audit n'est nécessaire.
import type { AuditReport, ExpectedDocument, JalonReport } from "@enervivo/shared-types";

// Périmètre des pièces comptées dans la complétude.
//  - "all"      : toutes les pièces (= calcul backend d'origine)
//  - "required" : uniquement Obligatoire + Annexes 3 PDB (vrai taux de conformité)
export type CompletionScope = "all" | "required";

const REQUIRED_PROPRIETES = new Set(["Obligatoire", "Annexes 3 PDB"]);

// Ordre chronologique canonique des jalons (doit suivre le référentiel).
// Sert à interpréter "jalon actuel = J3" comme "tout jalon ≤ J3".
export const JALON_ORDER = [
  "Avant J1",
  "J1",
  "J2a",
  "J2b",
  "J3",
  "J4",
  "J5_Construction",
  "J6_MES",
  "J7_Cloture",
];

/** Rang d'un jalon dans l'ordre chronologique (−1 si inconnu → trié en fin). */
export function jalonRank(jalon: string): number {
  const i = JALON_ORDER.indexOf(jalon);
  return i === -1 ? JALON_ORDER.length : i;
}

export interface CompletionStats {
  present: number;
  ambiguous: number;
  missing: number;
  expected: number;
  pct: number;
}

/** Compteurs d'un ensemble de documents selon le périmètre choisi. Formule :
 *  (présents + 0.5·ambigus) / attendus.
 *  ⚠️ Décision produit : les "not_applicable" sont IGNORÉS — comme s'ils
 *  n'existaient pas (ni dans attendus, ni manquants, ni le %). Plus de N/A. */
export function statsForDocuments(
  documents: ExpectedDocument[],
  scope: CompletionScope,
): CompletionStats {
  // On écarte d'emblée les not_applicable, puis on applique le périmètre.
  const applicable = documents.filter((d) => d.status !== "not_applicable");
  const docs =
    scope === "required"
      ? applicable.filter((d) => REQUIRED_PROPRIETES.has(d.propriete))
      : applicable;
  const present = docs.filter((d) => d.status === "present").length;
  const ambiguous = docs.filter((d) => d.status === "ambiguous").length;
  const missing = docs.filter((d) => d.status === "missing").length;
  const expected = docs.length;
  const pct = expected ? Math.round((100 * (present + 0.5 * ambiguous)) / expected) : 0;
  return { present, ambiguous, missing, expected, pct };
}

/** Jalons retenus selon le "jalon actuel" : tous ceux de rang ≤ celui choisi.
 *  `currentJalon = null` → tous les jalons (pas de filtre). */
export function jalonsUpTo(jalons: JalonReport[], currentJalon: string | null): JalonReport[] {
  if (!currentJalon) return jalons;
  const max = jalonRank(currentJalon);
  return jalons.filter((j) => jalonRank(j.jalon) <= max);
}

/** Tous les documents des jalons retenus, aplatis. */
export function documentsUpTo(
  jalons: JalonReport[],
  currentJalon: string | null,
): ExpectedDocument[] {
  return jalonsUpTo(jalons, currentJalon).flatMap((j) => j.documents);
}

/** Stats globales (KPI) selon le jalon actuel + le périmètre. */
export function overallStats(
  report: AuditReport,
  currentJalon: string | null,
  scope: CompletionScope,
): CompletionStats {
  return statsForDocuments(documentsUpTo(report.jalons, currentJalon), scope);
}

/** Documents obligatoires manquants (≤ jalon actuel), pour la section Alerts.
 *  Recalculé côté client pour respecter le filtre jalon (le `top_critical_missing`
 *  du backend ne porte pas l'info de jalon). */
export function criticalMissing(
  report: AuditReport,
  currentJalon: string | null,
  limit = 8,
): string[] {
  return documentsUpTo(report.jalons, currentJalon)
    .filter((d) => REQUIRED_PROPRIETES.has(d.propriete) && d.status === "missing")
    .map((d) => d.name)
    .slice(0, limit);
}
