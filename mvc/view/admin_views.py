"""Flask-Admin sobre os mesmos modelos Peewee já utilizados pelo DAO."""

from flask import flash, redirect, request, url_for
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.peewee import ModelView
from flask_admin.form import SecureForm
from flask_login import current_user
from wtforms import SelectField

from model.modelos import AlunoORM, DisciplinaORM, MatriculaORM, banco_peewee


class Protegida:
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login", next=request.path))


class InicioAdmin(Protegida, AdminIndexView):
    pass


class TabelaAdmin(Protegida, ModelView):
    form_base_class = SecureForm
    can_view_details = True
    column_display_pk = True
    page_size = 25

    def delete_model(self, model):
        # Não excluir matrículas automaticamente ao remover um aluno ou disciplina.
        try:
            model.delete_instance(recursive=False)
            return True
        except Exception as erro:
            flash(f"Não foi possível excluir o registro: {erro}", "error")
            return False


class AlunosAdmin(TabelaAdmin):
    form_columns = ("nusp", "nome", "email", "curso", "ano_ingresso")

    form_overrides = {"curso": SelectField, "ano_ingresso": SelectField}
    form_args = {"ano_ingresso": {"coerce": int}}

    @staticmethod
    def _configurar_opcoes(formulario):
        # Lê as opções do PostgreSQL a cada abertura do formulário.
        with banco_peewee.connection_context():
            cursos = [
                a.curso
                for a in AlunoORM.select(AlunoORM.curso)
                .distinct()
                .order_by(AlunoORM.curso)
            ]
            anos = [
                a.ano_ingresso
                for a in AlunoORM.select(AlunoORM.ano_ingresso)
                .distinct()
                .order_by(AlunoORM.ano_ingresso.desc())
            ]

        formulario.curso.choices = [(curso, curso) for curso in cursos]
        formulario.ano_ingresso.choices = [(ano, str(ano)) for ano in anos]
        return formulario

    def create_form(self, obj=None):
        return self._configurar_opcoes(super().create_form(obj))

    def edit_form(self, obj=None):
        return self._configurar_opcoes(super().edit_form(obj))


class DisciplinasAdmin(TabelaAdmin):
    form_columns = ("codigo", "nome")


class MatriculasAdmin(TabelaAdmin):
    form_columns = (
        "id_matricula",
        "aluno",
        "disciplina",
        "periodo",
        "nota",
        "frequencia",
    )


def configurar_admin(app):
    admin = Admin(app, name="Universidade", index_view=InicioAdmin())
    admin.add_view(AlunosAdmin(AlunoORM, name="Alunos"))
    admin.add_view(DisciplinasAdmin(DisciplinaORM, name="Disciplinas"))
    admin.add_view(MatriculasAdmin(MatriculaORM, name="Matrículas"))
    return admin
