# MinIO — Cache PDF, rétention, quota

## Configuration auto

Au démarrage de l'API, [`services/storage/lifecycle.py`](../../apps/api/services/storage/lifecycle.py:1) :

1. Crée le bucket `pdf-cache` s'il n'existe pas
2. Pose une **lifecycle policy** : tous les objets sont supprimés **30 jours** après leur création (variable `MINIO_RETENTION_DAYS`)

C'est **idempotent** : on peut redémarrer l'API sans risque.

## Quota disque

Le quota se définit au niveau du serveur MinIO via la console (`localhost:9001` en dev) :

1. Se connecter avec `MINIO_ACCESS_KEY` / `MINIO_SECRET_KEY`
2. **Buckets** → `pdf-cache` → **Manage** → **Quota**
3. Définir `Hard quota: 5 GiB`

Alternative ligne de commande (`mc` client) :
```bash
mc alias set local http://localhost:9000 enervivo changeme-min-8-chars
mc admin bucket quota local/pdf-cache --size 5GB
```

## Pourquoi pas Postgres ?

Le rapprochement « 1 audit = 30+ PDF × ~2 Mo = 60 Mo en DB » se fait vite à 100 audits/mois → 6 Go en JSONB. Postgres n'est pas fait pour ça.

MinIO offre :
- **Sharding par hash** : chaque objet va dans `{hash[:2]}/{hash}` → 256 préfixes, pas de hotspot
- **Lifecycle natif** : pas de cron à maintenir, MinIO purge tout seul
- **Quota dur** : impossible de saturer le disque du VPS

## Cache cross-audit

Si deux audits téléchargent le même fichier (même hash SHA-256) :

1. Premier audit : `find_by_hash(session, hash)` → MISS → MinIO put + LLM call + INSERT
2. Second audit : `find_by_hash(session, hash)` → HIT → réutilise `classified_type` + `confidence` → **0 appel LLM**

Le hash Postgres reste valable même après expiration MinIO (lifecycle = bytes seulement, métadonnées en DB infinies). Si on doit re-classifier, il faudra purger le cache Postgres (endpoint admin à venir).

## Surveillance

```bash
# Espace utilisé
mc du local/pdf-cache

# Nombre d'objets
mc ls --recursive local/pdf-cache | wc -l

# Lifecycle policy active ?
mc ilm ls local/pdf-cache
```
