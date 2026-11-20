from model.modelos import (
    banco_peewee,
    AlunoORM,
    DisciplinaORM,
    MatriculaORM,
)


def criar_tabelas():
    with banco_peewee:
        banco_peewee.create_tables([AlunoORM, DisciplinaORM, MatriculaORM], safe=True)
    print("Tabelas criadas")


if __name__ == "__main__":
    criar_tabelas()
