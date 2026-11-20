"""Controllers MVC: acessam os DAOs e renderizam páginas com Jinja."""

from flask import Blueprint, render_template
from flask_login import login_required

from model.dao import AlunoDAO, DisciplinaDAO, MatriculaDAO

web = Blueprint("web", __name__, url_prefix="/painel")


@web.get("/")
@login_required
def painel():
    return render_template(
        "painel.html",
        alunos=AlunoDAO().contar(),
        disciplinas=len(DisciplinaDAO().listar()),
        matriculas=len(MatriculaDAO().listar()),
    )


@web.get("/alunos")
@login_required
def alunos():
    return render_template("alunos.html", alunos=AlunoDAO().listar())


@web.get("/disciplinas")
@login_required
def disciplinas():
    return render_template("disciplinas.html", disciplinas=DisciplinaDAO().listar())


@web.get("/matriculas")
@login_required
def matriculas():
    return render_template("matriculas.html", matriculas=MatriculaDAO().listar())
