"""Cria tabelas e popula a base sem duplicar registros a cada reinício."""

from auth import UsuarioORM, criar_admin_inicial
from data.criar_banco import criar_tabelas
from data.popular_banco import popular_banco
from model.modelos import banco_peewee


def inicializar():
    criar_tabelas()
    with banco_peewee:
        banco_peewee.create_tables([UsuarioORM], safe=True)
    popular_banco()
    criar_admin_inicial()


if __name__ == "__main__":
    inicializar()
