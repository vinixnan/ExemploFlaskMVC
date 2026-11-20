#!/bin/sh
# Execute depois de iniciar: docker compose up --build
set -eu
URL="${BASE_URL:-http://localhost:5000}"
status() { curl -sS -o /dev/null -w '%{http_code}' "$@"; }
[ "$(status "$URL/")" = '200' ] || { echo 'Rota REST original não respondeu 200'; exit 1; }
[ "$(status "$URL/alunos")" = '200' ] || { echo 'Listagem REST não respondeu 200'; exit 1; }
[ "$(status "$URL/login")" = '200' ] || { echo 'Login não respondeu 200'; exit 1; }
case "$(status "$URL/painel/")" in 302|303) ;; *) echo 'Painel desprotegido'; exit 1;; esac
case "$(status "$URL/admin/")" in 302|303) ;; *) echo 'Admin desprotegido'; exit 1;; esac
echo 'OK: rotas originais e proteção de painel/Admin.'
