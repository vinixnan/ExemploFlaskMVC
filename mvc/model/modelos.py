import os

from peewee import (
    Model,
    PostgresqlDatabase,
    IntegerField,
    TextField,
    FloatField,
    ForeignKeyField,
)
from model.dominio import Pessoa, Aluno, Disciplina, Matricula

banco_peewee = PostgresqlDatabase(
    os.getenv("POSTGRES_DB", "universidade"),
    user=os.getenv("POSTGRES_USER", "universidade"),
    password=os.environ.get("POSTGRES_PASSWORD", ""),
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=int(os.getenv("POSTGRES_PORT", "5432")),
)


class ModeloBase(Model):
    class Meta:
        database = banco_peewee


class AlunoORM(ModeloBase):
    nusp = IntegerField(primary_key=True)
    nome = TextField()
    email = TextField()
    curso = TextField()
    ano_ingresso = IntegerField()

    class Meta:
        table_name = "alunos"


class DisciplinaORM(ModeloBase):
    codigo = TextField(primary_key=True, column_name="codigo_disciplina")
    nome = TextField(column_name="nome_disciplina")

    class Meta:
        table_name = "disciplinas"


class MatriculaORM(ModeloBase):
    id_matricula = IntegerField(primary_key=True)
    aluno = ForeignKeyField(AlunoORM, field=AlunoORM.nusp, column_name="nusp")
    disciplina = ForeignKeyField(
        DisciplinaORM, field=DisciplinaORM.codigo, column_name="codigo_disciplina"
    )
    periodo = TextField()
    nota = FloatField()
    frequencia = FloatField()

    class Meta:
        table_name = "matriculas"
