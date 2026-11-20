import os
from pathlib import Path

DATABASEKIND = os.getenv("DATABASEKIND", "Postgres").strip()
if DATABASEKIND not in ("SQLite", "Postgres"):
    raise ValueError("DATABASEKIND deve ser SQLite ou Postgres")

NOME_BANCO = "universidade.db"
ARQUIVO_BANCO = Path(
    os.getenv("SQLITE_PATH", str(Path(__file__).resolve().parents[1] / NOME_BANCO))
)
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
