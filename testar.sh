#!/bin/sh
# Executar depois de: docker compose up --build
set -eu

if [ ! -f .env ]; then
  echo 'Crie .env a partir de .env.example.' >&2
  exit 1
fi
set -a
# .env.example contém apenas valores simples compatíveis com o shell.
. ./.env
set +a

BASE_URL="${BASE_URL:-http://localhost:5000}"
status() {
  curl -sS -o /dev/null -w '%{http_code}' "$@"
}

[ "$(status "$BASE_URL/login")" = '200' ] || { echo 'Login não respondeu 200'; exit 1; }
[ "$(status "$BASE_URL/")" = '302' ] || { echo 'Painel sem login não redirecionou'; exit 1; }
[ "$(status "$BASE_URL/admin/")" = '302' ] || { echo 'Admin sem login não redirecionou'; exit 1; }
[ "$(status "$BASE_URL/alunos")" = '401' ] || { echo 'API sem token não retornou 401'; exit 1; }
[ "$(status -H "Authorization: Bearer $API_TOKEN" "$BASE_URL/alunos")" = '200' ] || { echo 'API com token não retornou 200'; exit 1; }

echo 'OK: login, proteção MVC/Admin e autenticação da API.'
echo "Abra $BASE_URL/login para testar o usuário admin no navegador."
