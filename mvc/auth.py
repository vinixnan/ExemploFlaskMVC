"""Login de usuários humanos para as páginas MVC e o Flask-Admin."""

import os

from flask import redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_wtf import FlaskForm
from peewee import AutoField, TextField
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired

from model.modelos import ModeloBase, banco_peewee


class UsuarioORM(ModeloBase, UserMixin):
    id = AutoField()
    usuario = TextField(unique=True)
    senha_hash = TextField()

    class Meta:
        table_name = "usuarios"

    def get_id(self):
        return str(self.id)


class LoginForm(FlaskForm):
    usuario = StringField("Usuário", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    entrar = SubmitField("Entrar")


class LogoutForm(FlaskForm):
    pass


@banco_peewee.connection_context()
def criar_admin_inicial():
    usuario = os.environ["ADMIN_USERNAME"]
    senha = os.environ["ADMIN_PASSWORD"]
    if UsuarioORM.get_or_none(UsuarioORM.usuario == usuario) is None:
        UsuarioORM.create(usuario=usuario, senha_hash=generate_password_hash(senha))
        print(f"Usuário administrativo criado: {usuario}")


def configurar_autenticacao(app):
    gerenciador = LoginManager()
    gerenciador.login_view = "login"
    gerenciador.init_app(app)

    @app.context_processor
    def incluir_logout():
        return {"logout_form": LogoutForm()}

    @gerenciador.user_loader
    def carregar_usuario(user_id):
        try:
            id_usuario = int(user_id)
        except (ValueError, TypeError):
            return None
        with banco_peewee.connection_context():
            return UsuarioORM.get_or_none(UsuarioORM.id == id_usuario)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("web.painel"))
        form = LoginForm()
        erro = None
        if form.validate_on_submit():
            with banco_peewee.connection_context():
                usuario = UsuarioORM.get_or_none(
                    UsuarioORM.usuario == form.usuario.data
                )
                valido = usuario is not None and check_password_hash(
                    usuario.senha_hash, form.senha.data
                )
            if valido:
                login_user(usuario)
                destino = request.args.get("next", "")
                if not destino.startswith("/") or destino.startswith("//"):
                    destino = url_for("web.painel")
                return redirect(destino)
            erro = "Usuário ou senha inválidos"
        return render_template("login.html", form=form, erro=erro)

    @app.post("/logout")
    @login_required
    def logout():
        if not LogoutForm().validate_on_submit():
            return {"erro": "Token CSRF inválido"}, 400
        logout_user()
        return redirect(url_for("login"))
