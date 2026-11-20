from peewee import (
    Model,
    SqliteDatabase,
    IntegerField,
    TextField,
    FloatField,
    ForeignKeyField,
)
from core.definitions import ARQUIVO_BANCO
from model.modelos import Pessoa, Aluno, Disciplina, Matricula

banco_peewee = SqliteDatabase(
    str(ARQUIVO_BANCO), pragmas={"foreign_keys": 1}, timeout=30
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
