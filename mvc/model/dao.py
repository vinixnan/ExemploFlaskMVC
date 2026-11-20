import sqlite3
from peewee import IntegrityError as PeeweeIntegrityError, fn

from model.modelos import (
    Aluno,
    Disciplina,
    Matricula,
    AlunoORM,
    DisciplinaORM,
    MatriculaORM,
    banco_peewee,
)


def _executar(consulta):
    try:
        return consulta.execute()
    except PeeweeIntegrityError as erro:
        # Mantém compatibilidade com o tratamento sqlite3.IntegrityError das rotas.
        raise sqlite3.IntegrityError(str(erro)) from erro


def _sql(consulta, parametros=()):
    # Peewee usa '?' no SQLite e '%s' no PostgreSQL.
    return banco_peewee.execute_sql(
        consulta.replace("%s", banco_peewee.param), parametros
    )


def _dicionarios(cursor):
    colunas = [coluna[0] for coluna in cursor.description]
    return [dict(zip(colunas, linha)) for linha in cursor.fetchall()]


class AlunoDAO:
    @staticmethod
    def _converter(registro):
        return Aluno(
            registro.nusp,
            registro.nome,
            registro.email,
            registro.curso,
            registro.ano_ingresso,
        )

    @banco_peewee.connection_context()
    def listar(self, curso=None):
        consulta = AlunoORM.select()
        if curso:
            consulta = consulta.where(AlunoORM.curso == curso).order_by(AlunoORM.nome)
        else:
            consulta = consulta.order_by(AlunoORM.nusp)
        return [self._converter(a) for a in consulta]

    @banco_peewee.connection_context()
    def buscar(self, nusp):
        aluno = AlunoORM.get_or_none(AlunoORM.nusp == nusp)
        return None if aluno is None else self._converter(aluno)

    @banco_peewee.connection_context()
    def inserir(self, aluno):
        _executar(
            AlunoORM.insert(
                nusp=aluno.nusp,
                nome=aluno.nome,
                email=aluno.email,
                curso=aluno.curso,
                ano_ingresso=aluno.ano_ingresso,
            )
        )

    @banco_peewee.connection_context()
    def atualizar(self, aluno):
        return _executar(
            AlunoORM.update(
                nome=aluno.nome,
                email=aluno.email,
                curso=aluno.curso,
                ano_ingresso=aluno.ano_ingresso,
            ).where(AlunoORM.nusp == aluno.nusp)
        )

    @banco_peewee.connection_context()
    def excluir(self, nusp):
        return _executar(AlunoORM.delete().where(AlunoORM.nusp == nusp))

    def listar_por_curso(self, curso):
        return self.listar(curso)

    @banco_peewee.connection_context()
    def contar(self):
        return AlunoORM.select().count()

    @banco_peewee.connection_context()
    def buscar_por_nome(self, nome):
        return [a.nusp for a in AlunoORM.select().where(AlunoORM.nome == nome)]

    @banco_peewee.connection_context()
    def listar_ingressantes(self, ano):
        consulta = (
            AlunoORM.select()
            .where(AlunoORM.ano_ingresso == ano)
            .order_by(AlunoORM.nome)
        )
        return [
            {"nusp": a.nusp, "nome": a.nome, "ano_ingresso": a.ano_ingresso}
            for a in consulta
        ]

    @banco_peewee.connection_context()
    def consultar_por_curso(self, curso):
        consulta = (
            AlunoORM.select().where(AlunoORM.curso == curso).order_by(AlunoORM.nome)
        )
        return [{"nusp": a.nusp, "nome": a.nome, "curso": a.curso} for a in consulta]

    @banco_peewee.connection_context()
    def consultar_por_curso_nomeado(self, curso):
        consulta = (
            AlunoORM.select().where(AlunoORM.curso == curso).order_by(AlunoORM.nome)
        )
        return [{"nusp": a.nusp, "nome": a.nome} for a in consulta]

    @banco_peewee.connection_context()
    def contar_por_curso(self):
        consulta = (
            AlunoORM.select(AlunoORM.curso, fn.COUNT(AlunoORM.nusp).alias("quantidade"))
            .group_by(AlunoORM.curso)
            .order_by(fn.COUNT(AlunoORM.nusp).desc(), AlunoORM.curso)
        )
        return [{"curso": a.curso, "quantidade": a.quantidade} for a in consulta]


class DisciplinaDAO:
    @staticmethod
    def _converter(registro):
        return Disciplina(registro.codigo, registro.nome)

    @banco_peewee.connection_context()
    def listar(self):
        consulta = DisciplinaORM.select().order_by(DisciplinaORM.codigo)
        return [self._converter(d) for d in consulta]

    @banco_peewee.connection_context()
    def buscar(self, codigo):
        disciplina = DisciplinaORM.get_or_none(DisciplinaORM.codigo == codigo)
        return None if disciplina is None else self._converter(disciplina)

    @banco_peewee.connection_context()
    def inserir(self, disciplina):
        _executar(DisciplinaORM.insert(codigo=disciplina.codigo, nome=disciplina.nome))

    @banco_peewee.connection_context()
    def atualizar(self, disciplina):
        return _executar(
            DisciplinaORM.update(nome=disciplina.nome).where(
                DisciplinaORM.codigo == disciplina.codigo
            )
        )

    @banco_peewee.connection_context()
    def excluir(self, codigo):
        return _executar(DisciplinaORM.delete().where(DisciplinaORM.codigo == codigo))

    @banco_peewee.connection_context()
    def buscar_por_nusp(self, nusp):
        sql = """
            SELECT DISTINCT d.codigo_disciplina, d.nome_disciplina
            FROM disciplinas AS d
            INNER JOIN matriculas AS m
              ON d.codigo_disciplina = m.codigo_disciplina
            WHERE m.nusp = %s
            ORDER BY d.nome_disciplina
        """
        return [
            Disciplina(codigo, nome) for codigo, nome in _sql(sql, (nusp,)).fetchall()
        ]

    @banco_peewee.connection_context()
    def listar_alunos_matriculados(self, codigo):
        sql = """
            SELECT a.nome AS aluno, d.nome_disciplina AS disciplina, m.nota
            FROM matriculas AS m
            INNER JOIN alunos AS a ON a.nusp = m.nusp
            INNER JOIN disciplinas AS d ON d.codigo_disciplina = m.codigo_disciplina
            WHERE d.codigo_disciplina = %s
            ORDER BY m.nota DESC
        """
        return _dicionarios(_sql(sql, (codigo,)))

    @banco_peewee.connection_context()
    def medias_notas(self):
        sql = """
            SELECT d.nome_disciplina, ROUND(CAST(AVG(m.nota) AS NUMERIC), 2) AS media_notas
            FROM disciplinas AS d
            INNER JOIN matriculas AS m
              ON m.codigo_disciplina = d.codigo_disciplina
            GROUP BY d.codigo_disciplina, d.nome_disciplina
            ORDER BY media_notas DESC
        """
        return _dicionarios(_sql(sql))


class MatriculaDAO:
    @staticmethod
    def _converter(registro):
        aluno = registro.aluno
        disciplina = registro.disciplina
        return Matricula(
            registro.id_matricula,
            Aluno(aluno.nusp, aluno.nome, aluno.email, aluno.curso, aluno.ano_ingresso),
            Disciplina(disciplina.codigo, disciplina.nome),
            registro.periodo,
            registro.nota,
            registro.frequencia,
        )

    @banco_peewee.connection_context()
    def listar(self):
        consulta = MatriculaORM.select().order_by(MatriculaORM.id_matricula)
        return [self._converter(m) for m in consulta]

    @banco_peewee.connection_context()
    def buscar(self, id_matricula):
        matricula = MatriculaORM.get_or_none(MatriculaORM.id_matricula == id_matricula)
        return None if matricula is None else self._converter(matricula)

    @banco_peewee.connection_context()
    def inserir(self, matricula):
        _executar(
            MatriculaORM.insert(
                id_matricula=matricula.id_matricula,
                aluno=matricula.aluno.nusp,
                disciplina=matricula.disciplina.codigo,
                periodo=matricula.periodo,
                nota=matricula.nota,
                frequencia=matricula.frequencia,
            )
        )

    @banco_peewee.connection_context()
    def atualizar(self, matricula):
        return _executar(
            MatriculaORM.update(
                periodo=matricula.periodo,
                nota=matricula.nota,
                frequencia=matricula.frequencia,
            ).where(MatriculaORM.id_matricula == matricula.id_matricula)
        )

    @banco_peewee.connection_context()
    def excluir(self, id_matricula):
        return _executar(
            MatriculaORM.delete().where(MatriculaORM.id_matricula == id_matricula)
        )

    @banco_peewee.connection_context()
    def listar_por_nusp(self, nusp):
        consulta = (
            MatriculaORM.select()
            .where(MatriculaORM.aluno == nusp)
            .order_by(MatriculaORM.disciplina)
        )
        return [
            {
                "id_matricula": m.id_matricula,
                "nusp": m.aluno_id,
                "codigo_disciplina": m.disciplina_id,
                "nota": m.nota,
            }
            for m in consulta
        ]

    @banco_peewee.connection_context()
    def listar_aprovados(self, nota_minima=5.0, frequencia_minima=70.0):
        consulta = (
            MatriculaORM.select()
            .where(
                (MatriculaORM.nota >= nota_minima)
                & (MatriculaORM.frequencia >= frequencia_minima)
            )
            .order_by(MatriculaORM.nota.desc(), MatriculaORM.id_matricula)
        )
        return [
            {
                "id_matricula": m.id_matricula,
                "nusp": m.aluno_id,
                "codigo_disciplina": m.disciplina_id,
                "nota": m.nota,
                "frequencia": m.frequencia,
            }
            for m in consulta
        ]

    @banco_peewee.connection_context()
    def listar_aprovados_por_disciplina(
        self, codigo, nota_minima=5.0, frequencia_minima=70.0
    ):
        sql = """
            SELECT a.nusp, a.nome, a.curso,
                   d.nome_disciplina, m.nota, m.frequencia
            FROM matriculas AS m
            INNER JOIN alunos AS a ON m.nusp = a.nusp
            INNER JOIN disciplinas AS d ON m.codigo_disciplina = d.codigo_disciplina
            WHERE d.codigo_disciplina = %s
              AND m.nota >= %s AND m.frequencia >= %s
            ORDER BY m.nota DESC, a.nome ASC, m.id_matricula ASC
        """
        return _dicionarios(_sql(sql, (codigo, nota_minima, frequencia_minima)))
