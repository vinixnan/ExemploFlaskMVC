"""Flask-Admin sobre os mesmos modelos Peewee já utilizados pelo DAO."""

from flask import flash, redirect, request, url_for
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.peewee import ModelView
from flask_admin.form import SecureForm
from flask_login import current_user
from wtforms import SelectField

from data.popular_banco import CURSOS, ANOS

from model.modelos import AlunoORM, DisciplinaORM, MatriculaORM


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

    # Mesmo catálogo usado na população dos dados; sem alterar o modelo Peewee.
    form_overrides = {"curso": SelectField, "ano_ingresso": SelectField}
    form_args = {
        "curso": {"choices": [(curso, curso) for curso in CURSOS]},
        "ano_ingresso": {
            "choices": [(ano, str(ano)) for ano in ANOS],
            "coerce": int,
        },
    }


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
