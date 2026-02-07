#!/usr/bin/env bash
set -euo pipefail

# Backup simples de banco e volumes Docker.
# Ajuste BACKUP_DIR conforme sua política.

BACKUP_DIR=${BACKUP_DIR:-/var/backups/voxy}
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

mkdir -p "$BACKUP_DIR"

# Dump do Postgres
CONTAINER_ID=$(docker compose ps -q postgres)
if [ -z "$CONTAINER_ID" ]; then
  echo "Container do Postgres não encontrado." >&2
  exit 1
fi

docker exec "$CONTAINER_ID" pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" > "$BACKUP_DIR/postgres_${TIMESTAMP}.sql"

# Backup volumes
VOL_DIR="$BACKUP_DIR/volumes_${TIMESTAMP}"
mkdir -p "$VOL_DIR"

docker run --rm -v postgres_data:/data -v "$VOL_DIR":/backup alpine \
  tar -czf /backup/postgres_data_${TIMESTAMP}.tar.gz -C /data .

docker run --rm -v redis_data:/data -v "$VOL_DIR":/backup alpine \
  tar -czf /backup/redis_data_${TIMESTAMP}.tar.gz -C /data .

printf "\nBackup salvo em %s\n" "$BACKUP_DIR"
