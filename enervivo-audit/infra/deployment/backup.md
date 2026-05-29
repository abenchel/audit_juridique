# Backup — PostgreSQL

Le seul état critique vit dans **Postgres** :
- `users` — identités SSO
- `projects` — référentiel projets (seed manuel pour l'instant)
- `audits` — historique + rapports JSONB
- `classified_documents` — cache classification cross-audit

(MinIO peut être perdu sans drame, c'est un cache.)

## Backup automatique nocturne

Sur le VPS, crontab (`crontab -e`) :

```cron
# Backup quotidien 02:00 + rotation 7 jours
0 2 * * * cd /opt/enervivo-audit && make backup && find infra/backups -name "dump-*.sql.gz" -mtime +7 -delete
```

Le target `make backup` :
- `pg_dump` → compressé gzip
- Fichier : `infra/backups/dump-YYYYMMDD-HHMMSS.sql.gz`

## Restauration

```bash
# Arrêter l'API pour éviter écriture concurrente
docker compose -f infra/docker-compose.yml stop api worker beat

# Vider la base actuelle
make reset-db

# Restaurer
gunzip < infra/backups/dump-20260513-020001.sql.gz | \
  docker compose -f infra/docker-compose.yml exec -T postgres \
    psql -U $POSTGRES_USER -d $POSTGRES_DB

# Redémarrer
make up
```

## Backup off-site (recommandé)

Le VPS pouvant tomber, recopier les dumps sur un stockage externe (S3, Backblaze B2, OneDrive personnel) :

```bash
# rclone (à configurer une fois) :
rclone copy infra/backups/ enervivo-onedrive:audit-backups/ --max-age 8d
```

Crontab :
```cron
30 2 * * * rclone copy /opt/enervivo-audit/infra/backups/ enervivo-onedrive:audit-backups/ --max-age 8d
```
