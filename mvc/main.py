import os

from flask import Flask

from view.admin_views import configurar_admin
from auth import configurar_autenticacao
from core.definitions import DEBUG
from model.modelos import banco_peewee
from rotas import api
from view.web import web


def criar_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
    app.register_blueprint(api)  # Rotas REST da aula anterior.
    app.register_blueprint(web)  # Páginas HTML/Jinja.
    configurar_autenticacao(app)
    configurar_admin(app)

    @app.teardown_appcontext
    def fechar_banco(erro=None):
        if not banco_peewee.is_closed():
            banco_peewee.close()

    return app


app = criar_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=DEBUG, threaded=True, use_reloader=False)
