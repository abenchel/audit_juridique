// Types partagés Backend ↔ Frontend
// Le fichier ./generated.ts est généré depuis Pydantic via :
//   cd apps/api && python -m scripts.generate_ts_types
//
// Re-export tout depuis generated quand disponible ; sinon fallback minimal.

export * from "./manual";

// Quand le script aura tourné, décommenter :
// export * from "./generated";
