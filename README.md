# ExemploFlaskMVC — SQLite ou PostgreSQL

O projeto mantém `model/`, `data/`, os DAOs, as consultas SQL e as rotas existentes. A escolha do banco é feita por **uma variável** no `.env`:

```dotenv
DATABASEKIND=SQLite
```

ou:

```dotenv
DATABASEKIND=Postgres
```

As demais configurações do projeto são as mesmas. `COMPOSE_PROFILES=${DATABASEKIND}` é uma configuração **fixa** do `.env` que ativa o PostgreSQL somente quando selecionado; não precisa ser alterada. É necessário Docker Compose atualizado (suporte a `depends_on.required: false`).

## Primeira execução

```sh
cp .env.example .env
```

Troque `SECRET_KEY`, `ADMIN_PASSWORD` e `POSTGRES_PASSWORD` pelos valores desejados. Escolha `DATABASEKIND` no `.env` e rode:

```sh
./create.sh
```

Esse script cria as tabelas, popula a base de teste e cadastra o administrador no banco **selecionado**. O script é explícito, não faz parte do `CMD` do Dockerfile e não roda a cada `up`.

## Execuções seguintes

```sh
docker compose up -d --build
```

Acesse `http://127.0.0.1:5000/login` e `http://127.0.0.1:5000/admin/`.

Em **SQLite**, o arquivo `/dados/universidade.db` fica no volume Docker `sqlite_data` (persistente). O PostgreSQL nem é iniciado. Em **Postgres**, usa-se o volume `pgdata`; o serviço `postgres` é iniciado e o MVC espera seu healthcheck.

Para desligar, use `docker compose down` **sem** `-v` para preservar os dois volumes.

### Atenção ao alternar o banco

Trocar `DATABASEKIND` **não migra dados**. SQLite e Postgres são bases independentes. Ao escolher um banco ainda não inicializado, execute novamente `./create.sh` para criar/popular somente essa base. Após trocar de banco, recrie o contêiner MVC (`docker compose up -d --force-recreate mvc`); ao voltar para um banco já criado, os registros anteriores permanecem.

O projeto mantém as tabelas acadêmicas `alunos`, `disciplinas` e `matriculas`, além de `usuarios` para autenticação. Os formulários de cursos e anos consultam o banco ativo, não o Faker.

## Mudanças pontuais

- `mvc/core/definitions.py`: lê e valida `DATABASEKIND` e o caminho SQLite.
- `mvc/model/modelos.py`: seleciona `SqliteDatabase` ou `PostgresqlDatabase`; modelos ORM e campos inalterados.
- `mvc/model/dao.py`: usa `banco_peewee.param` nos JOINs SQL (`?` / `%s`) e um `CAST` portátil no `ROUND`.
- `mvc/view/admin_views.py`: dropdowns consultam `AlunoORM` no banco atual.
- `docker-compose.yml`: volume SQLite + perfil PostgreSQL opcional.
- `create.sh`: criação/população sob demanda.

A aplicação MVC, o login, Flask-Admin, os modelos e os demais DAOs não foram redesenhados.
