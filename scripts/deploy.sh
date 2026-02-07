#!/usr/bin/env bash
set -euo pipefail

# Deploy local com Docker Compose.
# Pré-requisitos: docker e docker compose plugin instalados.

if [ ! -f .env ]; then
  echo "Copiando .env.example para .env"
  cp .env.example .env
  echo "Edite o arquivo .env antes de continuar." >&2
  exit 1
fi

docker compose pull --ignore-pull-failures

docker compose build

docker compose up -d

printf "\nDeploy concluído.\n"
