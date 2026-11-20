import os
from pathlib import Path

NOME_BANCO = "universidade.db"
ARQUIVO_BANCO = Path(__file__).resolve().parents[1] / NOME_BANCO
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
