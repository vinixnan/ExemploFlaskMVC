#!/bin/sh
# Inicialização EXPLÍCITA: não é executada a cada subida do contêiner.
set -eu
docker compose build mvc
docker compose run --rm mvc python -m data.inicializar
docker compose up -d mvc
