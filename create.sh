docker compose up -d postgres
docker compose build mvc
docker compose run --rm mvc python -m data.inicializar
docker compose up -d mvc