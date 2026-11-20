
#!/bin/sh
set -eu
cd "$(dirname "$0")"

MODO="${1:-dev}"
case "$MODO" in
    dev|prod) ;;
    *) echo "Uso: ./run.sh [dev|prod]"; exit 1 ;;
esac

# Aceita .env dentro de mvc/ ou na raiz do repositório
ENV_FILE="$PWD/.env"
[ -f "$ENV_FILE" ] || ENV_FILE="$PWD/../.env"
[ -f "$ENV_FILE" ] || { echo "Arquivo .env não encontrado"; exit 1; }

docker build -t exemplo-flask-mvc .
docker volume create universidade_sqlite >/dev/null

# Inicializa o banco apenas se ainda não existir
if ! docker run --rm \
    -v universidade_sqlite:/dados \
    --entrypoint sh exemplo-flask-mvc \
    -c 'test -s /dados/universidade.db'; then

    docker run --rm --env-file "$ENV_FILE" \
        -e DATABASEKIND=SQLite \
        -v universidade_sqlite:/dados \
        exemplo-flask-mvc python -m data.inicializar
fi

docker rm -f exemplo-flask-mvc >/dev/null 2>&1 || true

if [ "$MODO" = dev ]; then
    docker run --rm --name exemplo-flask-mvc \
        --env-file "$ENV_FILE" \
        -e DATABASEKIND=SQLite -e DEBUG=true \
        -v universidade_sqlite:/dados \
        -v "$PWD:/app" \
        -p 127.0.0.1:5000:5000 \
        exemplo-flask-mvc \
        flask --app main:app run --debug --host=0.0.0.0
else
    docker run --rm --name exemplo-flask-mvc \
        --env-file "$ENV_FILE" \
        -e DATABASEKIND=SQLite -e DEBUG=false \
        -v universidade_sqlite:/dados \
        -p 127.0.0.1:5000:5000 \
        exemplo-flask-mvc
fi
