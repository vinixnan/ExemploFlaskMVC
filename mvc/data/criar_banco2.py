from core.definitions import ARQUIVO_BANCO
from model2.modelos import (
    banco_peewee,
    AlunoORM,
    DisciplinaORM,
    MatriculaORM,
)


def criar_tabelas():
    with banco_peewee:
        banco_peewee.create_tables([AlunoORM, DisciplinaORM, MatriculaORM], safe=True)
    print(f"Tabelas criadas em: {ARQUIVO_BANCO}")


if __name__ == "__main__":
    criar_tabelas()
