# ExemploFlaskMVC — PostgreSQL, Flask MVC e Flask-Admin

Esta versão foi adaptada **do `atual.zip` fornecido na aula**, mantendo a organização `mvc/` e o código existente em `model/`. **Não foi criado `model2/`**. A API de catracas e o simulador ainda não fazem parte desta etapa.

## Executar

Requisitos: Docker e Docker Compose.

```sh
cp .env.example .env
```

Altere as senhas no `.env` e defina uma `SECRET_KEY` longa e aleatória (por exemplo, gerada com `python3 -c "import secrets; print(secrets.token_urlsafe(48))"`). Então:

```sh
docker compose up --build
```

Na primeira inicialização, o contêiner MVC cria as tabelas PostgreSQL, popula os mesmos dados gerados pelo Faker (`SEED = 42`) e cria o usuário administrativo definido no `.env`. Em reinicializações, os registros existentes são preservados.

| URL | Descrição |
| --- | --- |
| http://localhost:5000/ | API REST da aula anterior (mesmo endpoint) |
| http://localhost:5000/alunos | API REST de alunos (mesmas rotas) |
| http://localhost:5000/login | Login de usuário humano |
| http://localhost:5000/painel/ | Painel HTML/Jinja protegido |
| http://localhost:5000/painel/alunos | Página HTML de alunos |
| http://localhost:5000/painel/disciplinas | Página HTML de disciplinas |
| http://localhost:5000/painel/matriculas | Página HTML de matrículas |
| http://localhost:5000/admin/ | CRUD no Flask-Admin, protegido por login |

O **usuário e a senha** de login são `ADMIN_USERNAME` e `ADMIN_PASSWORD` do arquivo `.env`.

Para conferir as rotas originais e os redirecionamentos de autenticação:

```sh
./testar.sh
```

Para inspecionar os logs e encerrar os serviços:

```sh
docker compose logs -f mvc
docker compose down
```

`docker compose down -v` **apaga também o volume de dados** do PostgreSQL.

## Organização

```text
ExemploFlaskMVC/
├── docker-compose.yml         # PostgreSQL + MVC
├── .env.example
├── testar.sh
└── mvc/
    ├── Dockerfile
    ├── requirements.txt
    ├── main.py                # Criação do app Flask
    ├── rotas.py               # Rotas REST originais (com ajustes de import)
    ├── model/
    │   ├── modelos.py         # 3 modelos Peewee (mesmas tabelas e campos)
    │   ├── dominio.py         # Classes Aluno, Disciplina, Matrícula e Pessoa
    │   └── dao.py             # Mesmo DAO Peewee + consultas SQL prontas
    ├── data/
    │   ├── criar_banco2.py    # Criação das tabelas acadêmicas
    │   ├── popular_banco2.py  # População com os dados originais
    │   ├── popular_banco.py   # Função gerar_dados/Faker original
    │   └── inicializar.py     # Inicialização e usuário administrativo
    ├── auth.py                # Flask-Login + formulário de login
    ├── view/
    │   ├── __init__.py
    │   ├── web.py             # Controllers MVC, retornam HTML
    │   └── admin_views.py     # CRUD Flask-Admin + verificação de login
    └── templates/             # Views HTML/Jinja
```

As telas de cadastro de alunos no Flask-Admin oferecem seletores de **curso** e **ano de ingresso**, usando as opções de `data/popular_banco.py`, sem mudanças no banco.

## Mudanças no código antigo (mínimas)

1. **`model/modelos.py`:** apenas a conexão `SqliteDatabase` foi substituída por `PostgresqlDatabase`. Os campos de `AlunoORM`, `DisciplinaORM` e `MatriculaORM` são os mesmos.
2. **`model/dao.py`:** `model2.modelos` virou `model.modelos`; placeholders SQL `?` viraram `%s`; a média usa `ROUND(AVG(m.nota)::numeric, 2)` no PostgreSQL. Os métodos e as consultas SQL foram preservados. A conversão de erros de integridade para `sqlite3.IntegrityError` continua existindo para compatibilidade com as rotas antigas.
3. **`rotas.py`:** referências a `model2` viraram `model`; removidas as chamadas de rollback do banco SQLite, que não é mais utilizado pelas rotas.
4. **`data/criar_banco2.py` e `data/popular_banco2.py`:** somente imports ajustados para `model/` e mensagem de saída do banco.
5. **`model/dominio.py`:** foi necessário declarar as classes de domínio em um módulo pequeno, porque o `model/modelos.py` incluído no ZIP tinha um `from model.modelos import ...` apontando para o **próprio arquivo**, impedindo qualquer import. Os modelos ORM não foram reestruturados; as classes continuam acessíveis via `from model.modelos import Aluno`.
6. `core/banco.py`, `data/criar_banco.py` e a função antiga `data/popular_banco.py::popular_banco` foram mantidos como **legado SQLite**; não participam da execução PostgreSQL. O script `criar_e_popular.sh` passa a chamar as variantes `2`.

## Autenticação e banco

- **MVC e Flask-Admin:** usam sessão com Flask-Login. Senhas são guardadas com hash Werkzeug. Os formulários de login e Flask-Admin usam proteção CSRF.
- **API REST antiga:** continua acessível sem login, para preservar os comandos da aula anterior. A autenticação da API de frequência será um assunto separado, em etapa posterior.
- **PostgreSQL:** um contêiner oficial `postgres:17-alpine` com volume `pgdata`; conexão de dentro do MVC via `POSTGRES_HOST=postgres`, porta interna 5432; porta 5433 local opcional para ferramentas SQL.
- O esquema acadêmico continua tendo apenas `alunos`, `disciplinas` e `matriculas`. A única tabela nova é `usuarios`, exclusiva da autenticação. `Oferecimento`, `Sala` e `Presenca` não foram adicionados.

O projeto é **didático**: para uso fora de localhost seriam necessárias configurações adicionais de segurança, servidor WSGI apropriado e revisão do acesso à API REST antiga.
