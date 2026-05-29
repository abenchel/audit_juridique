# TASKS.md — Problèmes prioritaires à fixer

> **But** : liste opérationnelle des gros problèmes constatés (lenteur, RAM, fragilité) avec **fichier + ligne** et **cause racine**. À lire avant d'attaquer l'optimisation. Complète [SESSION.md](SESSION.md).
>
> **Date** : 2026-05-18 (mise à jour 2026-05-19 — 3 nouvelles demandes produit)
> **Contexte** : audits réels DMUZZOLINI (167 fichiers) / DDESCUNS (331 fichiers) — temps observé 35-40 min, OOM worker régulier, UI figée au refresh.

---

## 🔴 P0 — Bloquants (perf + stabilité)

### 1. ~~pdfplumber bloque l'event loop~~ + **lazy extraction** ✅ FAIT (2026-05-19)

**Implémenté** :
- [engine.py:168](apps/api/services/audit/engine.py#L168) : `sample = await asyncio.to_thread(extract_text, content, file.mime_type)` → l'event loop n'est plus bloqué pendant l'extraction → CONCURRENCY=5 redevient effective.
- [pdf.py](apps/api/services/extraction/pdf.py) **réécrit en lazy** : lit les pages depuis le début jusqu'à `HEAD_CHARS * 2` de texte (~10 pages typiquement), puis saute aux **3 dernières pages** pour la tail. Sur un PDF de 200 p, on lit ~10 pages au lieu de 200 → **~20× moins de RAM décompressée**, ~5-10× plus rapide.
- Risque connu : 1-2 % des docs avec titre/signataire en plein milieu peuvent rater leur tail context. Acceptable vu que `truncate_sample` ne garde de toute façon que head 2000 + tail 800 chars.

### 2. Le worker mange la RAM — 5 PDFs simultanément en mémoire (80 MB chacun max)

- **Fichier** : [engine.py:151](apps/api/services/audit/engine.py#L151) `content = await sp_client.download_file(file)` — charge tout le PDF en RAM avant le hash.
- **Symptôme** : 5 × 80 MB = **400 MB de pic théorique** rien que pour les bytes bruts, + 2-3× ça pour pdfplumber qui décompresse les pages. SIGKILL OOM observé (cf. [SESSION.md §9-Fix OOM worker](SESSION.md)).
- **Fix** :
  1. Baisser `MAX_FILE_SIZE_BYTES` (80 → 40 MB) **OU** streamer le hash (SHA-256 chunk par chunk pendant le download — supprime le besoin de tout garder en RAM avant le hash).
  2. Forcer un `gc.collect()` après chaque fichier dans `_wrapped` (les bytes des gros PDFs ne sont pas toujours libérés tout de suite par CPython à cause des cycles dans pdfplumber).
- **Note** : `content = None` (engine.py:175) ne suffit pas — `pdfplumber.open()` garde encore des références internes. À vérifier avec `tracemalloc`.

### 3. `_periodic_partial` rebuild un AuditReport complet **toutes les 30 s** depuis la DB

- **Fichier** : [engine.py:489-495](apps/api/services/audit/engine.py#L489-L495) (boucle), [engine.py:191-344](apps/api/services/audit/engine.py#L191-L344) (corps).
- **Symptôme** : pour un audit de 331 fichiers, à 80 % d'avancement, chaque cycle re-lit ~265 lignes, refait le `match_classified_to_expected` complet, sérialise un JSONB de plusieurs centaines de KB, et UPDATE `audits.result`. Toutes les 30 s. Le worker dépense ~5-10 % de son temps là-dedans **sans avancer**, et la connexion DB est monopolisée.
- **Fix** :
  - Allonger l'intervalle à 60-90 s OU déclencher seulement à des paliers (25/50/75 %).
  - Faire la requête `SELECT` sans charger tout l'ORM (utiliser `select(ClassifiedDocument.file_hash, .file_name, …)` colonnes plates).

### 4. Connexions Redis ouvertes/fermées **par fichier** (pas de pool)

- **Fichier** : 4 endroits dans [engine.py](apps/api/services/audit/engine.py) :
  - L114-117 (`_publish_progress` — chaque event)
  - L425-435 (`_is_cancelled` — **avant chaque fichier**, donc N fois)
  - L477-483 (snapshot done/current_file — après chaque fichier)
  - L412-417 (snapshot total — une fois OK)
- **Symptôme** : pour 331 fichiers on ouvre **~1000 connexions TCP Redis**, chacune ~5-20 ms de handshake. Soit **5-20 s perdus** + sockets en TIME_WAIT.
- **Fix** : créer **un seul** client Redis au début de `run_audit`, le passer en paramètre aux helpers, le `close()` dans le `finally`. Idéalement un singleton process-wide avec `Redis.from_url(..., decode_responses=True)` mis en cache via `@lru_cache`.

---

## 🟠 P1 — Importants (UX + coût)

### 5. L'UI ne se rafraîchit pas auto pendant l'audit (F5 manuel)

- **Fichier** : [apps/web/app/(app)/projects/[code]/audits/[auditId]/page.tsx](apps/web/app/(app)/projects/[code]/audits/[auditId]/page.tsx) — Server Component, pas de live refresh du `audit.result` partiel.
- **Symptôme** : on rebuild un rapport partiel toutes les 30 s (cf. P0 #3) mais le user doit faire F5 pour le voir.
- **Fix** : soit (a) ajouter un event SSE `partial_ready` que le client écoute → `router.refresh()`, soit (b) un client poll léger sur `GET /api/audits/{id}` toutes les 30 s tant que `status === 'running'`.

### 6. Pas de heartbeat Celery → audits zombies en `running`

- **Fichier** : [engine.py:362-363](apps/api/services/audit/engine.py#L362-L363) (set `status='running'` au début, jamais revérifié).
- **Symptôme** : worker SIGKILL = DB garde `status='running'` → l'UI affiche "audit en cours" éternellement. Cleanup manuel obligatoire : `UPDATE audits SET status='failed' WHERE status='running' AND started_at < NOW() - INTERVAL '10 minutes'` (déjà fait à la main 2 fois cette semaine, cf. SESSION.md).
- **Fix** : tâche Celery beat périodique (toutes les 2 min) qui marque `failed` les audits dont `started_at < now() - 15min` ET dont aucun event Redis `audit:{id}:done` n'a bougé depuis 5 min.

### 7. CONCURRENCY=5 dans le code + `--concurrency=2` Celery = effet multiplicatif sur 2 audits parallèles

- **Fichiers** : [engine.py:57](apps/api/services/audit/engine.py#L57) (CONCURRENCY=5) + [infra/docker-compose.yml](infra/docker-compose.yml) (`worker` cmd `--concurrency=2`).
- **Symptôme** : si deux audits tournent en même temps, on a **2 × 5 = 10 PDF en RAM** → re-OOM garanti malgré `mem_limit=4G`.
- **Fix** : baisser Celery `--concurrency=1` (un seul audit à la fois sur ce worker) OU passer CONCURRENCY de 5 à 3 si on garde 2 workers Celery. Documenter le calcul (`workers × CONCURRENCY × MAX_FILE_SIZE × 3` doit rester sous `mem_limit`).

### 8. Cache LLM Postgres ne peut pas être purgé sans accès SQL

- **Fichier** : aucun endpoint admin n'existe (cf. [SESSION.md §11](SESSION.md)).
- **Symptôme** : si un PDF est mal classifié (confidence 90, mauvais type), tous les futurs audits qui rencontrent ce hash réutilisent l'erreur → le user n'a aucun moyen de corriger sans `make shell-db`.
- **Fix** : `POST /api/admin/reclassify/{hash}` qui `DELETE FROM classified_documents WHERE file_hash = ?` (protégé par `require_admin`).

---

## 🟡 P2 — Polish (moins critique)

### 9. Frontend Next.js — `output: 'standalone'` abandonné, image runtime ~+300 MB

- **Fichier** : [apps/web/next.config.mjs](apps/web/next.config.mjs) (commenté), [apps/web/Dockerfile](apps/web/Dockerfile).
- **Symptôme** : image `web` ~500 MB au lieu de ~200 MB → push/pull plus lent en CI, plus de RAM à l'idle.
- **Fix** : re-tenter standalone avec `pnpm deploy --filter=web` (commande dédiée monorepo de pnpm 9) qui copie les bons `node_modules` sans symlinks. Plus propre que `node-linker=hoisted`.

### 10. Le sample d'extraction (2000 head + 800 tail) rate parfois le bon classement

- **Fichier** : [apps/api/services/extraction/base.py](apps/api/services/extraction/base.py) `HEAD_CHARS=2000, TAIL_CHARS=800`.
- **Symptôme** : sur des conventions de servitude longues, le titre est en p.1 (OK) mais les signatures (qui aident à dater + identifier les parties) sont en p.15 → ratent la tail.
- **Fix** : si pdfplumber détecte > 20 pages, prendre 2000 head + 800 milieu + 800 tail au lieu de juste head+tail. Test sur 5 PDFs ambigus avant de généraliser.

### 11. Liste `ALL_JALONS` dupliquée côté front

- **Fichier** : [apps/web/app/(app)/projects/[code]/page.tsx](apps/web/app/(app)/projects/[code]/page.tsx) — const en dur.
- **Fix** : endpoint `GET /api/reference/jalons` qui lit `documents_v11.json` côté API et expose la liste. Évite la divergence quand V12 arrive (cf. [SESSION.md §9.bis Sélecteur de jalon](SESSION.md)).

---

---

## 🆕 Demandes produit (2026-05-19) — état d'avancement

**Statut au 2026-05-20** : ✅ A faite · ✅ B faite · ✅ C faite · ✅ **bonus** : (1) fallback vision LLM pour PDF scannés, (2) **support multi-format** — images (.jpg/.png/.heic) classées en vision directement (CNI/RIB en image natif désormais classés), PPTX via python-pptx, XLSX via openpyxl. Le filtre `_classify_ignored_reason` n'ignore plus QUE vidéo/audio/archive/CAD/email. Reste pour plus tard : top-N par case dans le matcher si nécessaire (voir §10 ci-dessous).

### A. Exclure le dossier `Visuels/` du listing SharePoint ✅ FAIT (2026-05-19)

**Implémenté** :
- [settings.py](apps/api/config/settings.py) : ajout `sharepoint_excluded_folders: str = "Visuels"` + property `sharepoint_excluded_folders_set` (CSV → set lowercase).
- [sharepoint/real.py](apps/api/services/sharepoint/real.py) : `_walk()` skippe les dossiers dont le nom match `excluded` (case-insensitive) **avant** de descendre dedans → 0 appel Graph + 0 download pour le sous-arbre exclu. Log `Dossier exclu : path (N items) — skip`.
- ~~[sharepoint/mock.py]~~ : client mock **supprimé** le 2026-05-19 (data réelle SharePoint uniquement).
- [.env](.env) : `SHAREPOINT_EXCLUDED_FOLDERS=Visuels` (override-able CSV, ex : `Visuels,0-OLD`).

**Détails de spec d'origine ci-dessous (gardés pour traçabilité)** :

- **Pourquoi** : sur DIBOS / DMONFLANQUIN et autres projets, le dossier `Visuels/` contient des renders 3D, photomontages, PDF de présentation commerciale — **aucun intérêt juridique**, gros poids (souvent 50-200 MB par fichier). Aujourd'hui le listing récursif les attrape, ils sont téléchargés, hashés, puis (au mieux) jetés par le filtre `_classify_ignored_reason` (engine.py) → bande passante + RAM gaspillées.
- **Fichiers à modifier** :
  - [apps/api/services/sharepoint/real.py](apps/api/services/sharepoint/real.py) — fonction qui itère récursivement les dossiers Graph : ajouter une liste `_EXCLUDED_FOLDER_NAMES = {"visuels", "visuel", "renders", "photomontages"}` (lowercase) et **skip** tout dossier dont le nom matche **avant** de lister son contenu (économie d'1 appel Graph par dossier exclu + 0 fichier descendu).
  - [apps/api/services/sharepoint/mock.py](apps/api/services/sharepoint/mock.py) — par cohérence, retirer ou tagger comme exclus les éventuels fichiers fictifs sous un chemin contenant "Visuels".
  - [apps/api/config/settings.py](apps/api/config/settings.py) — exposer `SHAREPOINT_EXCLUDED_FOLDERS: list[str]` (default `["Visuels"]`) **configurable via .env** plutôt qu'en dur, pour ajouter d'autres dossiers à exclure sans redéploiement.
- **Test** : relancer un audit sur DIBOS_H → vérifier dans les logs `Listing : N fichiers à classifier` que N a baissé, et qu'aucun fichier du dossier `Visuels` n'apparaît dans `ignored_files` non plus (il faut qu'ils soient **ignorés au listing**, pas listés-puis-rejetés).
- **Bonus** : logger `Dossier exclu : Visuels (12 fichiers, 340 MB)` au listing pour visibilité.

### B. Intégrer V2 comme référentiel d'enrichissement ✅ FAIT (2026-05-20)

**Implémenté** :
- [scripts/convert_liste_projet_to_json.py](apps/api/scripts/convert_liste_projet_to_json.py) — convertit `EnerVivo_Liste_Documents_Projet_V2.xlsx` → [config/documents_projet_v2.json](apps/api/config/documents_projet_v2.json) (227 docs avec `folder_path`, `extensions[]`, `comment`).
- [services/audit/types/juridique.py](apps/api/services/audit/types/juridique.py) — `_load_reference()` charge V11 + V2 et fait une jointure floue **2 passes** :
  1. **Match par nom** (token containment+jaccard, seuil 0.45) → 37/107 docs.
  2. **Fallback folder-based** (1 token V11 dans un folder V2) → +42 docs.
  3. **Total : 79/107 docs V11 enrichis** avec hint folder/ext/note. Les 28 restants n'ont pas d'équivalent V2 (ex. "Lettre de motivation", "Feuille d'émargement") → pas de hint, pas de problème, le LLM classe sur le contenu seul.
- [services/llm/prompts/juridique.py](apps/api/services/llm/prompts/juridique.py) — `build_system_prompt` ajoute `  (dossier : X ; ext : Y ; note : Z)` à chaque ligne du catalogue. Nouveau paragraphe explique au LLM d'utiliser le dossier comme signal fort. `build_user_prompt` accepte `file_path=` optionnel et l'inclut comme `Chemin SharePoint : /...`.
- [services/llm/classifier.py](apps/api/services/llm/classifier.py) — `classify()` et `classify_vision()` propagent `file_path` jusqu'au user prompt.
- [services/audit/engine.py](apps/api/services/audit/engine.py) — les 2 appels classifier passent désormais `file_path=file.path`.

**Impact attendu** : élimine les faux positifs du type "Devis signé EPA contient 8 devis dont 6 ne sont pas EPA" — le hint folder `7-Achat-Fournisseurs/1-Consultations/EPA` permet au LLM de rejeter un devis ENEDIS trouvé dans `/10-Raccordement/`.

**Limites connues** (acceptables pour v1) :
- Le fallback folder picke parfois la mauvaise sous-branche pour les cas conditionnels (ex. "personne morale" mappe vers la branche "personne physique"). Le LLM voit la fois le hint **et** le path réel du fichier → arbitre.
- Prompt système grossit à ~3300 tokens (vs ~700 avant). Cached via `cache_control: ephemeral` → coût marginal négligeable pour les audits batch.

---

#### Spec d'origine (gardée pour contexte) :

#### B. Intégrer V2 comme **référentiel d'enrichissement** de V11 (dossier + extension + contexte)

- **Source** : [../EnerVivo_Liste_Documents_Projet_V2.xlsx](../EnerVivo_Liste_Documents_Projet_V2.xlsx) à la racine de `audit_juridique/`.
- **Rôle de V2** (clarifié 2026-05-19) : pour chaque document, V2 dit :
  - **où** il se trouve (dossier N1/N2/N3 — ex. `4-Documents Administratifs > 6-Bail > PDB`)
  - **quelle extension** est attendue (ex. `.pdf, .docx`)
  - **le contexte conditionnel** dans le commentaire (ex. `"jalon J1"`, `"Si projet AgriPV"`, `"Si candidature AMI"`)
  - **228 types de docs** au total, organisés en 11 dossiers N1.
- **Comparaison des xlsx** (vérifié 2026-05-19) :
  - **V11** : 9 jalons stables (`Avant J1`, `J1`, `J2a`, `J2b`, `J3`, `J4`, `Construction`, `MES`, `Cloture`). Source de vérité unique pour le référentiel par jalon (V10 obsolète, V11 le surensemble).
  - **V2** : vue orthogonale à V11 — pas de jalon en clé primaire, mais le commentaire référence souvent un jalon.
- **Stratégie d'intégration** : **enrichir** V11 avec V2 par jointure sur le nom/type de document. V11 reste la **source de vérité** pour « qu'est-ce qui est attendu à quel jalon », V2 apporte les indices :
  - **Folder hint** → si le LLM voit un fichier dans `…/6-Bail/PDB/…`, c'est probablement la "Promesse de Bail signée" attendue en J2a, pas une LOI.
  - **Extension hint** → un `.dotx` est un *template*, à ignorer ou classer en `not_applicable`. Un `.pdf` dans `2-LOI/` est une LOI signée, un `.docx` dans `2-LOI/` est un draft.
  - **Conditional hint** → "Si projet AgriPV" pour Attestation MSA, "Si projet S21" pour qualification toiture, etc. → permet d'affiner les conditionnels déjà partiellement gérés ([SESSION.md §3.6](SESSION.md)).
- **Fichiers à créer / modifier** :
  - **Nouveau script** : `apps/api/scripts/convert_liste_projet_to_json.py` (clone adapté de [convert_excel_to_json.py](apps/api/scripts/convert_excel_to_json.py)). Produit `apps/api/config/documents_projet_v2.json` avec la structure :
    ```json
    {
      "documents": [
        {
          "type": "Promesse de Bail signée",
          "folder_n1": "4-Documents Administratifs",
          "folder_path": "4-Documents Administratifs/6-Bail/PDB",
          "extensions": [".pdf"],
          "comment": "PDB notariée ou sous seing privé",
          "jalon_hint": null,
          "conditional": null
        }
      ]
    }
    ```
  - [apps/api/services/audit/types/juridique.py](apps/api/services/audit/types/juridique.py) — au `load_reference()`, charger V11 **et** V2, puis matcher chaque doc V11 avec son équivalent V2 (jointure floue sur le nom — `rapidfuzz` ou simple normalisation). Stocker l'enrichissement dans `reference["jalons"][i]["documents"][j]["v2_metadata"]`.
  - [apps/api/services/llm/prompts/juridique.py](apps/api/services/llm/prompts/juridique.py) — le prompt généré inclut désormais, pour chaque doc attendu : `(attendu dans le dossier "X/Y", extensions: .pdf/.docx)`. Le LLM utilise ces indices pour mieux disambiguer.
  - [apps/api/services/audit/matcher.py](apps/api/services/audit/matcher.py) — bonus : utiliser `folder_path` comme **signal supplémentaire** dans le matching (si le fichier classifié est trouvé dans le bon dossier SharePoint, on monte la confidence ; si le fichier est dans `0-OLD/`, on baisse).
- **Validation** : sur DIBOS_H, comparer 5 classifications avant/après l'enrichissement V2 (cf. tâche C). Mesurer si la confidence moyenne monte et si les "ambiguous" diminuent.
- **Non-objectif** : on ne change **pas** la liste des 107 docs attendus de V11. V2 sert d'**indices**, pas de nouvelle source de vérité.

### C. Réduire les projets de test à `DIBOS_H` et `DMONFLANQUIN` ✅ FAIT (2026-05-19)

**Implémenté** : [projects_seed.json](apps/api/config/projects_seed.json) remplacé. `DIBOS_H` (type `Toiture`, jalon `J2a`) + `DMONFLANQUIN` (type `AgriPV`, jalon `J2a`). ⚠️ **À valider** : le `type` et le `current_jalon` ont été choisis par défaut — ajuster si tu connais la vraie valeur. **Reste à faire côté toi** : `make seed` pour que la DB prenne le nouveau JSON, et purger les anciens projets si besoin (`DELETE FROM projects WHERE code IN ('DMUZZOLINI','DDESCUNS')`).

**Détails de spec d'origine ci-dessous** :

- **Fichier principal** : [apps/api/config/projects_seed.json](apps/api/config/projects_seed.json) — remplacer les 2 entrées DMUZZOLINI/DDESCUNS par :

  ```json
  [
    {
      "code": "DIBOS_H",
      "name": "DIBOS Hangar",
      "type": "Toiture",
      "sharepoint_url": "https://enervivo.sharepoint.com/Documents%20partages/09-Projets/DIBOS/Hangar",
      "current_jalon": "J2a",
      "power_mwc": null,
      "department": null,
      "project_metadata": { "client": "DIBOS", "seeded_at": "2026-05-19" }
    },
    {
      "code": "DMONFLANQUIN",
      "name": "DMONFLANQUIN",
      "type": "AgriPV",
      "sharepoint_url": "https://enervivo.sharepoint.com/Documents%20partages/09-Projets/DMONFLANQUIN",
      "current_jalon": "J2a",
      "power_mwc": null,
      "department": null,
      "project_metadata": { "client": "Monflanquin", "seeded_at": "2026-05-19" }
    }
  ]
  ```

  - ⚠️ **À valider** : `type` (`AgriPV` vs `Toiture` vs autre) — impacte les conditionnels (ex. attestation MSA n'apparaît que pour AgriPV, cf. [SESSION.md §3.6](SESSION.md)). DIBOS Hangar suggère **Toiture**, à confirmer.
  - ⚠️ **À valider** : `current_jalon` — DMUZZOLINI était J2a, DDESCUNS J2b. Les nouveaux projets ont besoin de leur vrai jalon courant pour que la vue par défaut soit correcte.
- **Vérifier le path SharePoint réel** : lancer [apps/api/scripts/find_projects.py](apps/api/scripts/find_projects.py) avec les noms `DIBOS` et `DMONFLANQUIN` pour confirmer que le path existe et choper le bon `webUrl` (espacement, accents, encodage `%20` vs `+`, etc.).
- **Cleanup DB** : après modif du seed, **idempotent** par design, donc `make seed` suffit. Pour purger les anciens projets :
  ```sql
  DELETE FROM audits WHERE project_code IN ('DMUZZOLINI', 'DDESCUNS');
  DELETE FROM projects WHERE code IN ('DMUZZOLINI', 'DDESCUNS');
  ```
  (à faire **après** s'être assuré qu'on n'a pas besoin de l'historique des audits passés).
- **Documentation** : mettre à jour [SESSION.md §3.5](SESSION.md) qui mentionne encore DMUZZOLINI/DDESCUNS, et [README.md](README.md) si applicable.

---

## Récap par axe

| Axe | Tickets concernés | Gain attendu |
|---|---|---|
| **Lenteur** | #1 (asyncio.to_thread pdfplumber), #3 (partial moins fréquent), #4 (pool Redis) | **-30 à -50 %** sur temps total |
| **RAM / OOM** | #2 (streaming hash + gc), #7 (concurrence cumulative) | Fin des SIGKILL sur DDESCUNS |
| **UX** | #5 (auto-refresh partiel), #6 (heartbeat audits zombies), #8 (reclassify) | Plus de "audit figé" perçu |
| **Coût LLM** | Déjà bien optimisé (prompt caching 76 % cheaper, cf. [LLM_CACHE_OPTIMIZATIONS.md](LLM_CACHE_OPTIMIZATIONS.md)) | — |

**Ordre suggéré d'attaque** : #1 → #4 → #2 → #3 → #6 → #5 → reste. Les 4 premiers se font en une journée et changent radicalement le ressenti.

**Demandes produit du 2026-05-19** (A/B/C) : indépendantes des perf, faisables en parallèle. **C** d'abord (5 min, débloque les tests sur les vrais projets cibles), puis **A** (1-2 h, gain bande passante immédiat), puis **B** (à scoper après avoir ouvert le xlsx).
