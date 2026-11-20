# ExemploFlask2 — Universidade (primeira etapa: MVC + PostgreSQL)

Evolução do projeto da aula anterior, com **mudanças mínimas** em `Aluno`, `Disciplina`, `Matricula` e nas rotas REST originais. A aplicação agora tem páginas MVC, login e Flask-Admin, usando PostgreSQL com Peewee. **Ainda não inclui API de frequência nem simulador**.

## Rodar

Pré-requisito: Docker com Docker Compose.

```bash
cp .env.example .env
```

Edite `.env` e substitua todas as senhas e chaves de exemplo. Para gerar uma chave aleatória:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(48))"
```

Pode usar esse comando separadamente para `SECRET_KEY` e `API_TOKEN`.

```bash
docker compose up --build
```

Abra **http://localhost:5000/login** e entre com `ADMIN_USERNAME` / `ADMIN_PASSWORD` configurados em `.env`. O contêiner cria as tabelas e popula os dados Faker automaticamente na primeira inicialização (semente 42). Ao reiniciar, não duplica os dados.

| Endereço | Para quê? |
| --- | --- |
| `http://localhost:5000/` | Painel MVC com contadores |
| `http://localhost:5000/painel/alunos` | Listagem HTML de alunos |
| `http://localhost:5000/painel/disciplinas` | Listagem HTML de disciplinas |
| `http://localhost:5000/painel/matriculas` | Listagem HTML de matrículas |
| `http://localhost:5000/admin/` | Cadastro, edição e exclusão com Flask-Admin |
| `http://localhost:5000/api` | Endpoint original de identificação da API (exige token) |

### Testar as rotas REST anteriores

As rotas originais `/alunos`, `/disciplinas` e `/matriculas` permanecem disponíveis. Agora exigem um **token Bearer** (separado do login de sessão do MVC):

```bash
# Substitua pelo valor de API_TOKEN definido em .env.
curl -H 'Authorization: Bearer SEU_TOKEN_AQUI' http://localhost:5000/alunos
```

Por exemplo, as mesmas rotas anteriores: `GET /alunos`, `GET /alunos/95633`, `POST /alunos`, `PUT /alunos/95633`, `DELETE /alunos/95633`, `GET /disciplinas`, `GET /matriculas`, `GET /matriculas/1`.

### PostgreSQL

O serviço `postgres` do Compose usa o banco `universidade`, usuário `universidade`, porta interna 5432. A porta do computador é **5433**, apenas em `localhost`, para não conflitar com outro PostgreSQL local. Os dados ficam no volume `pgdata` e persistem entre reinicializações.

O banco é acessado pelas classes do Peewee em `mvc/model/orm.py` e pelos DAOs em `mvc/model/dao.py`. Os modelos de domínio da aula anterior foram preservados em `mvc/model/modelos.py`.

### Desenvolvimento e manutenção

```bash
docker compose ps
docker compose logs -f mvc
./testar.sh   # verifica login, proteção e token da API
docker compose down
```

Atenção: `docker compose down -v` **apaga o volume PostgreSQL e todos os registros**. Use apenas quando quiser reinicializar do zero.

O usuário admin é criado somente se não existir. Alterar `ADMIN_PASSWORD` depois que ele já foi criado **não muda a senha existente**; para trocar a senha de um usuário persistido será necessário realizar uma atualização segura ou reinicializar o volume (perdendo os dados).

## Organização

```text
ExemploFlask2/
├── docker-compose.yml
├── .env.example
├── README.md
└── mvc/
    ├── Dockerfile
    ├── requirements.txt
    ├── main.py                 # Criação do app Flask
    ├── auth.py                 # Autenticação de sessão
    ├── web.py                  # Controllers MVC (HTML/Jinja)
    ├── admin_views.py          # Flask-Admin protegido
    ├── rotas.py                # Rotas REST da aula anterior
    ├── forms.py                # Login e logout (CSRF)
    ├── core/banco.py           # Conexão PostgreSQL
    ├── model/modelos.py        # Classes de domínio preservadas
    ├── model/orm.py            # Modelos do Peewee
    ├── model/dao.py            # DAO com Peewee
    ├── data/criar_banco.py
    ├── data/popular_banco.py   # Faker preservado
    ├── data/inicializar.py
    ├── templates/
    └── static/
```

## Observações didáticas

- **Model**: classes de domínio e DAOs do pacote `model/`.
- **View**: templates HTML em `templates/`, renderizados com Jinja.
- **Controller**: funções de rota em `web.py`; formulários CRUD no Flask-Admin.
- **Autenticação**: sessão para usuários humanos via Flask-Login, senha armazenada com hash; rotas antigas REST com token Bearer.
- Os dados iniciais refletem o exemplo anterior: matrículas ainda são ligadas diretamente a disciplinas. `Oferecimento` e serviço de frequência serão adicionados numa etapa posterior.
- Não use as senhas de exemplo em um servidor exposto à internet. Este é um projeto didático, não um sistema acadêmico de produção.
