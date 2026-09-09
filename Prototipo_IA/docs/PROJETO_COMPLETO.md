# Dessik — projeto completo em 14 etapas

Entrega com tutorial e arquivos integrais. Os mesmos arquivos estão no repositório. Gerado por `python -m scripts.export_guide`. Nenhum segredo real é incluído.

## ETAPA 1 — Visão geral

```text
Navegador (HTML + CSS + JavaScript)
             | fetch, JSON e Authorization: Bearer JWT
             v
Vercel: arquivos públicos + FastAPI em /api/*
             | consultas parametrizadas e transações
             v
MySQL remoto (usuários, produtos, pedidos e itens)

GET /api/cep/{cep} -> FastAPI -> ViaCEP -> endereço em JSON
```

Localmente, o Uvicorn serve a API e os mesmos arquivos públicos em uma única origem. Senhas recebem hash bcrypt com salt; tokens expiram; a permissão administrativa é lida no banco a cada operação protegida.


## ETAPA 2 — Estrutura de pastas

```text
Dessik/
├── api/
│   ├── __init__.py
│   └── index.py
├── backend/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── auth.py
│   ├── schemas.py
│   ├── security.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── usuarios.py
│   │   ├── produtos.py
│   │   ├── pedidos.py
│   │   └── cep.py
│   └── services/
│       ├── __init__.py
│       └── password_generator.py
├── public/
│   ├── index.html
│   ├── loja.html
│   ├── cadastro.html
│   ├── login.html
│   ├── admin.html
│   ├── css/style.css
│   ├── css/storefront.css
│   ├── data/produtos-demo.json
│   ├── js/
│   │   ├── api.js
│   │   ├── cadastro.js
│   │   ├── login.js
│   │   ├── loja.js
│   │   └── admin.js
│   ├── images/placeholder.svg
│   └── images/catalogo-dessik.png
├── database/
│   ├── schema.sql
│   └── dados.sql
├── scripts/
│   ├── __init__.py
│   ├── init_db.py
│   ├── admin.py
│   └── export_guide.py
├── tests/
│   ├── conftest.py
│   ├── test_security.py
│   ├── test_cep.py
│   ├── test_frontend.py
│   └── test_mysql.py
├── docs/
│   ├── PROJETO_COMPLETO.md
│   └── VALIDACAO.md
├── .env.example
├── .gitignore
├── .vercelignore
├── requirements.txt
├── requirements-dev.txt
├── requirements-lock.txt
├── pyproject.toml
├── vercel.json
└── README.md
```

`public/` substitui a pasta `frontend/` sugerida no enunciado para que a Vercel sirva os arquivos estáticos diretamente. Não existe duplicação de builds nem etapa JavaScript. `schemas.py` representa e valida a entrada; usamos SQL parametrizado, então não precisamos de modelos ORM. Cadastro e login ficam juntos em `usuarios.py`.


## ETAPA 3 — Banco de dados

O DDL completo está em [database/schema.sql](../database/schema.sql). As oito amostras fictícias estão em [database/dados.sql](../database/dados.sql): notebook, mouse, teclado, monitor, headset, webcam, SSD e RAM. A webcam começa sem estoque para demonstrar o botão indisponível.

Use MySQL 8.0.16+ com InnoDB ou serviço compatível com transações, bloqueio `FOR UPDATE` e chaves estrangeiras. Os valores monetários são `DECIMAL`, não `FLOAT`. O pedido armazena o preço unitário vigente, preservando o valor histórico mesmo que o administrador altere o preço depois.

Crie o banco no painel do provedor ou, em um servidor próprio, no Workbench:

```sql
CREATE DATABASE loja_ficticia CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE loja_ficticia;
```

Depois abra e execute `schema.sql`, seguido de `dados.sql`, com o banco selecionado. Alternativamente, configure `.env` e execute `python -m scripts.init_db`: ele executa ambos no banco informado em `DB_NAME`. Não precisa conceder `CREATE DATABASE` à aplicação na nuvem.

O script não apaga tabelas e a carga de demonstração não redefine produtos já existentes com os mesmos IDs. Execute a massa em banco novo; não é uma ferramenta de migração para schemas anteriores. DDL MySQL pode provocar commit implícito. Não há criação de tabela automática em cada requisição ou deploy.

Não há senha padrão ou usuário administrador embutido. Um usuário com pedidos não pode ser excluído por causa da FK. Produtos com pedidos retornam HTTP 409 na exclusão: zere o estoque se quiser interromper as vendas sem perder o histórico.

Os oito produtos fictícios usam ilustrações locais criadas com IA, organizadas em um atlas visual `public/images/catalogo-dessik.png`. O CSS recorta cada item visualmente. A correspondência usa o nome do produto; imagens próprias cadastradas no administrador continuam sendo exibidas normalmente. Para usar fotos próprias, coloque os arquivos em `public/images/` e altere `imagem_url` para `/images/nome.webp` no administrador. Também é aceita URL HTTPS. Use imagens com autorização de uso.



### Arquivo: database/schema.sql

```sql
-- MySQL 8.0.16+ (InnoDB). Execute no banco escolhido na conexão.
-- Em provedores sem CREATE DATABASE, crie/selecione o banco pelo painel.
-- Opcional, em servidor próprio:
-- CREATE DATABASE loja_ficticia CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- USE loja_ficticia;

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(254) NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    cep VARCHAR(8) NOT NULL DEFAULT '',
    logradouro VARCHAR(150) NOT NULL DEFAULT '',
    bairro VARCHAR(100) NOT NULL DEFAULT '',
    cidade VARCHAR(100) NOT NULL DEFAULT '',
    estado VARCHAR(2) NOT NULL DEFAULT '',
    data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_usuarios_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS produtos (
    id_produto INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    descricao TEXT NOT NULL,
    categoria VARCHAR(60) NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    quantidade_estoque INT NOT NULL DEFAULT 0,
    imagem_url VARCHAR(1000) NOT NULL,
    data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    KEY idx_produtos_categoria (categoria),
    CONSTRAINT ck_produtos_preco CHECK (preco > 0),
    CONSTRAINT ck_produtos_estoque CHECK (quantidade_estoque >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS pedidos (
    id_pedido INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    data_pedido TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    valor_total DECIMAL(16,2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'simulado',
    KEY idx_pedidos_usuario_data (id_usuario, data_pedido),
    CONSTRAINT fk_pedidos_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    CONSTRAINT ck_pedidos_total CHECK (valor_total > 0),
    CONSTRAINT ck_pedidos_status CHECK (status = 'simulado')
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS itens_pedido (
    id_item INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL,
    UNIQUE KEY uq_item_produto (id_pedido, id_produto),
    KEY idx_itens_produto (id_produto),
    CONSTRAINT fk_itens_pedido FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido) ON DELETE RESTRICT,
    CONSTRAINT fk_itens_produto FOREIGN KEY (id_produto) REFERENCES produtos(id_produto) ON DELETE RESTRICT,
    CONSTRAINT ck_itens_quantidade CHECK (quantidade > 0),
    CONSTRAINT ck_itens_preco CHECK (preco_unitario > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- A massa de demonstração fica em dados.sql; scripts.init_db executa ambos.
```


### Arquivo: database/dados.sql

```sql
-- Execute uma vez, após schema.sql, em um banco vazio.
-- As condições por ID permitem repetir a inicialização sem resetar o estoque.
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 1,'Notebook Horizon 14','Leve para estudar, criar e levar sua rotina a qualquer lugar. Tela de 14 polegadas e SSD de 512 GB.','Computadores',3299.90,8,'/images/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=1);
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 2,'Mouse Pulse','Precisão e conforto para trabalhar e jogar. Sensor de 6.400 DPI e seis botões.','Periféricos',129.90,24,'/images/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=2);
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 3,'Teclado mecânico Type','Formato compacto, conexão USB e teclas mecânicas para o seu setup.','Periféricos',249.90,15,'/images/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=3);
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 4,'Monitor View 24','Mais espaço para suas ideias. Painel de 24 polegadas Full HD com conexão HDMI.','Monitores',899.90,6,'/images/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=4);
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 5,'Headset Wave','Áudio estéreo, microfone ajustável e almofadas macias para longas sessões.','Áudio',189.90,18,'/images/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=5);
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 6,'Webcam Focus','Videochamadas em Full HD com microfone integrado e suporte para monitor.','Periféricos',219.90,0,'/images/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=6);
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 7,'SSD Sprint 1 TB','Espaço e velocidade para arquivos, jogos e projetos. Interface SATA.','Componentes',399.90,20,'/images/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=7);
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 8,'Memória RAM Flux 16 GB','Mais fôlego para várias tarefas. Módulo DDR4 de 3.200 MHz.','Componentes',229.90,12,'/images/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=8);
```

## ETAPA 4 — Back-End

- `config.py`: lê `.env`, exige segredo JWT forte e exige banco remoto com TLS em produção.
- `database.py`: única fábrica de conexões e contexto de transação. Commita ao concluir, desfaz em caso de erro e sempre fecha os recursos.
- `schemas.py`: valida e-mail, nomes, senhas coincidentes, CEP, UF, preço, estoque e quantidades. Campos extras são rejeitados, inclusive `is_admin` no cadastro.
- `security.py`: bcrypt com salt e JWT HS256 com expiração, emissor e audiência.
- `auth.py`: valida Bearer, assinatura e prazo do token; consulta a conta e suas permissões.
- `services/password_generator.py`: gera senha de 16 caracteres com `secrets`, contendo minúsculas, maiúsculas, números e símbolos.

O bcrypt tem limite de 72 **bytes**; a API rejeita senhas acima disso em vez de truncá-las. O mínimo no cadastro é de 8 caracteres. Não se registra senha ou token nos logs. Erros de validação omitem a entrada enviada.

As consultas usam parâmetros `%s` e tuplas separadas. O driver transmite o dado como valor, impedindo que um e-mail ou nome seja interpretado como comando SQL. Consultas nunca concatenam a entrada do usuário.



### Arquivo: backend/__init__.py

```python
"""Regras e serviços da loja Dessik."""
```


### Arquivo: backend/config.py

```python
import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


@lru_cache
def settings():
    """Falha explicitamente se faltam segredos; não existe chave padrão."""
    secret = os.getenv("JWT_SECRET", "")
    if len(secret.encode()) < 32:
        raise RuntimeError("Configure JWT_SECRET com pelo menos 32 bytes aleatórios.")
    if os.getenv("JWT_ALGORITHM", "HS256") != "HS256":
        raise RuntimeError("Este projeto utiliza somente JWT_ALGORITHM=HS256.")
    minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    if not 1 <= minutes <= 1440:
        raise RuntimeError("ACCESS_TOKEN_EXPIRE_MINUTES deve estar entre 1 e 1440.")
    production = os.getenv("APP_ENV") == "production" or os.getenv("VERCEL") == "1"
    host = os.getenv("DB_HOST", "")
    tls = os.getenv("DB_SSL", "true").lower() == "true"
    if not host or not os.getenv("DB_USER") or not os.getenv("DB_NAME"):
        raise RuntimeError("Configure DB_HOST, DB_USER e DB_NAME.")
    if production and (not tls or host.lower() in {"localhost", "127.0.0.1", "::1"}):
        raise RuntimeError("Produção exige MySQL remoto com TLS.")
    origins = [x.strip() for x in os.getenv("CORS_ORIGINS", "").split(",") if x.strip()]
    if "*" in origins:
        raise RuntimeError("CORS_ORIGINS deve conter origens explícitas, sem *.")
    return {"secret": secret, "minutes": minutes, "production": production,
            "host": host, "tls": tls, "origins": origins}
```


### Arquivo: backend/database.py

```python
"""Conexões curtas: cada operação libera cursor e conexão, inclusive com erro."""
import os
from contextlib import contextmanager

import mysql.connector

from backend.config import settings


def connect():
    config = settings()
    options = {
        "host": config["host"], "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.environ["DB_USER"], "password": os.getenv("DB_PASSWORD", ""),
        "database": os.environ["DB_NAME"], "charset": "utf8mb4",
        "autocommit": False, "connection_timeout": 10,
        "read_timeout": 15, "write_timeout": 15, "use_pure": True,
        "ssl_disabled": not config["tls"],
    }
    if config["tls"]:
        options.update(ssl_verify_cert=True, ssl_verify_identity=True)
        if os.getenv("DB_SSL_CA"):
            options["ssl_ca"] = os.environ["DB_SSL_CA"]
    return mysql.connector.connect(**options)


@contextmanager
def transaction():
    connection = connect()
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        yield cursor
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()
```


### Arquivo: backend/schemas.py

```python
from decimal import Decimal
import re

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator


class Input(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Login(Input):
    email: EmailStr = Field(max_length=254)
    senha: str = Field(min_length=1, max_length=72)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value):
        return value.lower()

    @field_validator("senha")
    @classmethod
    def password_bytes(cls, value):
        if len(value.encode("utf-8")) > 72:
            raise ValueError("A senha deve ter no máximo 72 bytes UTF-8.")
        return value


class Cadastro(Login):
    nome: str = Field(min_length=2, max_length=100)
    senha: str = Field(min_length=8, max_length=72)
    confirmar_senha: str = Field(min_length=8, max_length=72)
    cep: str = ""
    logradouro: str = Field(default="", max_length=150)
    bairro: str = Field(default="", max_length=100)
    cidade: str = Field(default="", max_length=100)
    estado: str = Field(default="", max_length=2)

    @field_validator("nome")
    @classmethod
    def valid_name(cls, value):
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Informe um nome com pelo menos 2 caracteres.")
        return value

    @field_validator("cep")
    @classmethod
    def valid_cep(cls, value):
        value = value.replace("-", "").strip()
        if value and not re.fullmatch(r"[0-9]{8}", value):
            raise ValueError("CEP deve conter 8 números.")
        return value

    @field_validator("estado")
    @classmethod
    def valid_state(cls, value):
        value = value.upper()
        if value and value not in "AC AL AP AM BA CE DF ES GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO".split():
            raise ValueError("UF inválida.")
        return value

    @model_validator(mode="after")
    def matching_passwords(self):
        if self.senha != self.confirmar_senha:
            raise ValueError("As senhas não coincidem.")
        return self


class Produto(Input):
    nome: str = Field(min_length=2, max_length=120)
    descricao: str = Field(min_length=1, max_length=2000)
    categoria: str = Field(min_length=1, max_length=60)
    preco: Decimal = Field(gt=0, le=99999999.99, max_digits=10, decimal_places=2)
    quantidade_estoque: int = Field(ge=0, le=1000000, strict=True)
    imagem_url: str = Field(max_length=1000)

    @field_validator("nome", "descricao", "categoria")
    @classmethod
    def non_blank(cls, value):
        if not value.strip():
            raise ValueError("O campo não pode ficar vazio.")
        return value.strip()

    @field_validator("imagem_url")
    @classmethod
    def safe_image(cls, value):
        from urllib.parse import urlsplit
        parsed = urlsplit(value)
        if (parsed.scheme == "https" and parsed.netloc and not parsed.username
                and not parsed.password):
            return value
        if re.fullmatch(r"/images/[a-zA-Z0-9_/-]+\.(png|jpg|jpeg|webp|svg)", value) and ".." not in value:
            return value
        raise ValueError("Use uma URL HTTPS ou imagem local em /images/.")


class ItemPedido(Input):
    id_produto: int = Field(gt=0, strict=True)
    quantidade: int = Field(gt=0, le=1000, strict=True)


class Pedido(Input):
    itens: list[ItemPedido] = Field(min_length=1, max_length=50)

    @model_validator(mode="after")
    def unique_items(self):
        if len({i.id_produto for i in self.itens}) != len(self.itens):
            raise ValueError("Agrupe as quantidades de cada produto em um único item.")
        return self
```


### Arquivo: backend/security.py

```python
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from backend.config import settings


def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode()


def verify_password(password, hashed):
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode())
    except (ValueError, TypeError):
        return False


def create_token(user_id):
    now = datetime.now(timezone.utc)
    return jwt.encode({"sub": str(user_id), "iat": now,
                       "exp": now + timedelta(minutes=settings()["minutes"]),
                       "iss": "dessik", "aud": "dessik-web"},
                      settings()["secret"], algorithm="HS256")


def decode_token(token):
    return jwt.decode(token, settings()["secret"], algorithms=["HS256"],
                      issuer="dessik", audience="dessik-web",
                      options={"require": ["sub", "exp", "iat", "iss", "aud"]})
```


### Arquivo: backend/auth.py

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError

from backend.database import transaction
from backend.security import decode_token

bearer = HTTPBearer(auto_error=False)


def current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)):
    unauthorized = HTTPException(401, "Sessão inválida ou expirada. Entre novamente.",
                                 headers={"WWW-Authenticate": "Bearer"})
    if credentials is None:
        raise unauthorized
    try:
        user_id = int(decode_token(credentials.credentials)["sub"])
        if user_id <= 0:
            raise ValueError()
    except (InvalidTokenError, ValueError, TypeError, KeyError):
        raise unauthorized
    with transaction() as cursor:
        cursor.execute("SELECT id_usuario, nome, email, is_admin FROM usuarios WHERE id_usuario = %s", (user_id,))
        user = cursor.fetchone()
    if not user:
        raise unauthorized
    user["is_admin"] = bool(user["is_admin"])
    return user


def admin_user(user=Depends(current_user)):
    # A permissão vem do banco em cada requisição, nunca de um botão ou do cliente.
    if not user["is_admin"]:
        raise HTTPException(403, "Esta operação exige um administrador.")
    return user
```


### Arquivo: backend/services/__init__.py

```python
"""Serviços independentes das rotas."""
```


### Arquivo: backend/services/password_generator.py

```python
import secrets
import string


def generate_password(length=16):
    groups = (string.ascii_lowercase, string.ascii_uppercase, string.digits, "!@#$%&*+-=?")
    alphabet = "".join(groups)
    # Rejeição garante que todos os grupos apareçam, usando somente secrets.
    while True:
        password = "".join(secrets.choice(alphabet) for _ in range(length))
        if all(any(char in group for char in password) for group in groups):
            return password
```

## ETAPA 5 — API REST

| Método | Endpoint | Função | Acesso |
|---|---|---|---|
| GET | `/api/health` | Verificar API (não consulta o banco) | Público |
| POST | `/api/cadastro` | Cadastrar cliente | Público |
| POST | `/api/login` | Emitir JWT | Público |
| GET | `/api/me` | Consultar conta autenticada | Cliente/Admin |
| GET | `/api/gerar-senha` | Sugerir senha forte | Público |
| GET | `/api/produtos` | Listar catálogo | Público |
| GET | `/api/produtos/{id}` | Consultar um produto | Público |
| POST | `/api/produtos` | Criar produto | Admin |
| PUT | `/api/produtos/{id}` | Substituir dados do produto | Admin |
| DELETE | `/api/produtos/{id}` | Excluir produto sem pedidos | Admin |
| POST | `/api/pedidos` | Simular compra | Cliente/Admin |
| GET | `/api/pedidos` | Últimos 100 pedidos da própria conta | Cliente/Admin |
| GET | `/api/cep/{cep}` | Consultar ViaCEP | Público |
| GET | `/api/docs` | Swagger interativo | Público |
| GET | `/api/openapi.json` | Contrato OpenAPI | Público |

Produtos aceitam `?limite=12&offset=0` (limite de 1 a 100). O front-end pagina o catálogo e a tabela administrativa. O preço na resposta é uma string decimal como `"129.90"`. O JavaScript a formata como moeda; o cálculo oficial sempre é feito no servidor.

Pedidos aceitam até 50 produtos diferentes e quantidades inteiras de 1 a 1.000 por item. Produtos duplicados devem ser agrupados. A interface simula um produto por vez; a API também suporta vários produtos. O cliente não envia o valor a pagar nem o ID do usuário. Esses dados vêm do banco e do JWT.

O servidor bloqueia os produtos por ordem de ID com `SELECT ... FOR UPDATE`, valida todas as disponibilidades, grava pedido e itens e reduz o estoque na mesma transação. Se qualquer etapa falhar, ocorre rollback. Há também atualização condicional e restrição de estoque não negativo. Deadlock ou timeout de bloqueio retorna 409 para uma nova tentativa consciente do usuário.

Respostas usam 200/201 no sucesso, 401 para autenticação inválida, 403 para permissão insuficiente, 404 para recursos inexistentes, 409 para conflitos, 422 para dados inválidos, 502 para erro no ViaCEP, 503 para falha de banco e 500 para falha inesperada. Mensagens não expõem credenciais nem SQL.



### Arquivo: backend/routes/__init__.py

```python
"""Rotas REST organizadas por responsabilidade."""
```


### Arquivo: backend/routes/usuarios.py

```python
from fastapi import APIRouter, Depends, HTTPException
from mysql.connector import IntegrityError

from backend.auth import current_user
from backend.database import transaction
from backend.schemas import Cadastro, Login
from backend.security import create_token, hash_password, verify_password
from backend.services.password_generator import generate_password

router = APIRouter(tags=["Usuários"])
# Hash válido apenas para equalizar o custo do login de um e-mail inexistente.
DUMMY_HASH = hash_password(generate_password())


@router.post("/cadastro", status_code=201)
def cadastro(data: Cadastro):
    hashed = hash_password(data.senha)
    try:
        with transaction() as cursor:
            cursor.execute(
                """INSERT INTO usuarios
                (nome, email, senha_hash, cep, logradouro, bairro, cidade, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (data.nome, str(data.email), hashed, data.cep, data.logradouro,
                 data.bairro, data.cidade, data.estado))
            user_id = cursor.lastrowid
    except IntegrityError as error:
        if error.errno == 1062:
            raise HTTPException(409, "Este e-mail já está cadastrado.")
        raise
    return {"mensagem": "Conta criada. Você já pode entrar.", "id_usuario": user_id}


@router.post("/login")
def login(data: Login):
    with transaction() as cursor:
        cursor.execute("SELECT id_usuario, senha_hash FROM usuarios WHERE email = %s", (str(data.email),))
        user = cursor.fetchone()
    valid = verify_password(data.senha, user["senha_hash"] if user else DUMMY_HASH)
    if not user or not valid:
        raise HTTPException(401, "E-mail ou senha incorretos.", headers={"WWW-Authenticate": "Bearer"})
    return {"access_token": create_token(user["id_usuario"]), "token_type": "bearer"}


@router.get("/me")
def me(user=Depends(current_user)):
    return user


@router.get("/gerar-senha")
def password():
    return {"senha": generate_password()}
```


### Arquivo: backend/routes/produtos.py

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from mysql.connector import IntegrityError

from backend.auth import admin_user
from backend.database import transaction
from backend.schemas import Produto

router = APIRouter(prefix="/produtos", tags=["Produtos"])


def serialize_product(product):
    # Decimal vira string para preservar centavos na transmissão JSON.
    product["preco"] = str(product["preco"])
    return product


@router.get("")
def list_products(limite: int = Query(100, ge=1, le=100), offset: int = Query(0, ge=0)):
    with transaction() as cursor:
        cursor.execute("SELECT * FROM produtos ORDER BY id_produto LIMIT %s OFFSET %s", (limite, offset))
        return [serialize_product(p) for p in cursor.fetchall()]


@router.get("/{product_id}")
def get_product(product_id: int):
    with transaction() as cursor:
        cursor.execute("SELECT * FROM produtos WHERE id_produto = %s", (product_id,))
        product = cursor.fetchone()
    if not product:
        raise HTTPException(404, "Produto não encontrado.")
    return serialize_product(product)


@router.post("", status_code=201)
def create_product(data: Produto, user=Depends(admin_user)):
    with transaction() as cursor:
        cursor.execute("""INSERT INTO produtos
            (nome, descricao, categoria, preco, quantidade_estoque, imagem_url)
            VALUES (%s, %s, %s, %s, %s, %s)""", tuple(data.model_dump().values()))
        product_id = cursor.lastrowid
    return {"mensagem": "Produto cadastrado.", "id_produto": product_id}


@router.put("/{product_id}")
def update_product(product_id: int, data: Produto, user=Depends(admin_user)):
    with transaction() as cursor:
        cursor.execute("SELECT id_produto FROM produtos WHERE id_produto = %s FOR UPDATE", (product_id,))
        if not cursor.fetchone():
            raise HTTPException(404, "Produto não encontrado.")
        cursor.execute("""UPDATE produtos SET nome=%s, descricao=%s, categoria=%s,
            preco=%s, quantidade_estoque=%s, imagem_url=%s WHERE id_produto=%s""",
                       (*data.model_dump().values(), product_id))
    return {"mensagem": "Produto atualizado."}


@router.delete("/{product_id}")
def delete_product(product_id: int, user=Depends(admin_user)):
    try:
        with transaction() as cursor:
            cursor.execute("DELETE FROM produtos WHERE id_produto = %s", (product_id,))
            if cursor.rowcount == 0:
                raise HTTPException(404, "Produto não encontrado.")
    except IntegrityError as error:
        if error.errno == 1451:
            raise HTTPException(409, "Produto possui pedidos. Mantenha o histórico e ajuste o estoque para zero.")
        raise
    return {"mensagem": "Produto excluído."}
```


### Arquivo: backend/routes/pedidos.py

```python
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException

from backend.auth import current_user
from backend.database import transaction
from backend.schemas import Pedido

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post("", status_code=201)
def create_order(data: Pedido, user=Depends(current_user)):
    with transaction() as cursor:
        products = {}
        total = Decimal("0.00")
        # Ordem fixa de bloqueios reduz deadlocks entre pedidos de vários produtos.
        for item in sorted(data.itens, key=lambda item: item.id_produto):
            cursor.execute("SELECT * FROM produtos WHERE id_produto = %s FOR UPDATE", (item.id_produto,))
            product = cursor.fetchone()
            if not product:
                raise HTTPException(404, "Um dos produtos não existe mais.")
            if product["quantidade_estoque"] < item.quantidade:
                raise HTTPException(409, f"Estoque insuficiente para {product['nome']}.")
            products[item.id_produto] = product
            total += product["preco"] * item.quantidade
        cursor.execute("INSERT INTO pedidos (id_usuario, valor_total, status) VALUES (%s, %s, %s)",
                       (user["id_usuario"], total, "simulado"))
        order_id = cursor.lastrowid
        for item in data.itens:
            cursor.execute("""INSERT INTO itens_pedido
                (id_pedido, id_produto, quantidade, preco_unitario)
                VALUES (%s, %s, %s, %s)""",
                           (order_id, item.id_produto, item.quantidade, products[item.id_produto]["preco"]))
            cursor.execute("""UPDATE produtos SET quantidade_estoque = quantidade_estoque - %s
                WHERE id_produto = %s AND quantidade_estoque >= %s""",
                           (item.quantidade, item.id_produto, item.quantidade))
            if cursor.rowcount != 1:
                raise HTTPException(409, "Estoque alterado. Atualize a loja e tente novamente.")
        # O context manager confirma tudo junto ou desfaz tudo se uma etapa falhar.
    return {"mensagem": "Pedido simulado com sucesso. Nenhuma cobrança foi realizada.",
            "id_pedido": order_id, "valor_total": str(total)}


@router.get("")
def list_orders(user=Depends(current_user)):
    with transaction() as cursor:
        cursor.execute("""SELECT id_pedido, data_pedido, valor_total, status FROM pedidos
            WHERE id_usuario = %s ORDER BY id_pedido DESC LIMIT 100""", (user["id_usuario"],))
        orders = cursor.fetchall()
    for order in orders:
        order["valor_total"] = str(order["valor_total"])
    return orders
```


### Arquivo: backend/routes/cep.py

```python
import re

import httpx
from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["Endereço"])


@router.get("/cep/{cep}")
def lookup_cep(cep: str):
    cep = cep.replace("-", "")
    if not re.fullmatch(r"[0-9]{8}", cep):
        raise HTTPException(422, "Informe um CEP com 8 números.")
    try:
        # Host fixo e CEP numérico impedem que a entrada vire uma URL arbitrária.
        with httpx.Client(timeout=5.0) as client:
            response = client.get(f"https://viacep.com.br/ws/{cep}/json/")
            response.raise_for_status()
            address = response.json()
        if not isinstance(address, dict):
            raise ValueError("Resposta inválida")
    except (httpx.HTTPError, ValueError):
        raise HTTPException(502, "ViaCEP indisponível. Preencha o endereço manualmente.")
    if address.get("erro"):
        raise HTTPException(404, "CEP não encontrado.")
    fields = {"cep": "cep", "logradouro": "logradouro", "bairro": "bairro",
              "cidade": "localidade", "estado": "uf"}
    if any(not isinstance(address.get(key, ""), str) for key in fields.values()):
        raise HTTPException(502, "Resposta inválida do ViaCEP.")
    return {key: address.get(source, "") for key, source in fields.items()}
```

## ETAPA 6 — Front-End

Abra `http://127.0.0.1:8000/` com o servidor iniciado; não dê duplo clique no HTML. Os scripts são módulos JavaScript separados e usam caminhos da mesma origem. O catálogo é montado a partir de `GET /api/produtos`, sem produtos fixos no HTML.

O navegador mantém o JWT em `sessionStorage` durante a sessão da aba. `api.js` inclui `Authorization: Bearer ...` nas operações protegidas. Sair remove o token local. Se ele vencer, a API retorna 401 e a sessão é removida; entre novamente. Fechar a aba normalmente encerra esse armazenamento, sujeito ao recurso de restauração de sessão do navegador.

Esse armazenamento pode ser acessado por JavaScript: uma falha XSS pode expor o token. Aqui os textos são inseridos por `textContent`, as imagens são validadas e há CSP. Em um sistema profissional, cookies `HttpOnly`, `Secure`, `SameSite` com proteção CSRF e revogação/renovação de sessão merecem consideração. Logout local não revoga um JWT já copiado, que permanece válido até expirar. O projeto não implementa rate limiting distribuído; para publicação aberta, configure regras de limitação no provedor para login e cadastro.

Na loja, escolha uma quantidade, clique em Comprar e confirme a simulação. O total devolvido pelo servidor é o definitivo. Após a compra, os cards são recarregados. Em indisponibilidade da API/banco, a página informa o erro e abre um catálogo demonstrativo identificado, com oito itens de `public/data/produtos-demo.json`. Nesse modo não são criados pedidos nem apresentados estoques como reais. É possível abri-lo diretamente em `/loja.html?demo=1`. O botão Atualizar catálogo tenta reconectar à API. O catálogo conectado continua vindo exclusivamente do MySQL. Botões desativados evitam cliques repetidos durante uma requisição, mas a API não oferece idempotência: se houver perda da resposta, consulte `GET /api/pedidos` antes de repetir a compra.

Os campos de endereço são opcionais. O botão Consultar CEP chama nossa API, que consulta ViaCEP com timeout de 5 segundos. Erros permitem preenchimento manual. Conforme o [contrato do ViaCEP](https://viacep.com.br/), CEP inexistente é identificado por `erro` na resposta. Evite consultas em massa.



### Arquivo: public/admin.html

```html
<!doctype html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Dessik: loja fictícia de tecnologia para um projeto acadêmico."><title>Administração | Dessik</title><link rel="icon" href="/images/placeholder.svg" type="image/svg+xml"><link rel="stylesheet" href="/css/style.css"><link rel="stylesheet" href="/css/storefront.css"><script type="module" src="/js/admin.js"></script></head>
<body class="account-page"><a class="skip" href="#main">Pular para o conteúdo</a>
<div class="topnote">Loja fictícia · Compras simuladas, sem cobrança</div>
<header class="navbar"><div class="nav-inner"><a class="brand" href="/loja.html" aria-label="Dessik início">dessik<span>.</span></a>
<nav aria-label="Navegação principal"><a href="/loja.html">Produtos</a><a href="/admin.html" data-admin hidden>Administração</a>
<a href="/login.html" data-guest>Entrar</a><a class="button secondary" href="/cadastro.html" data-guest>Criar conta</a>
<span class="nav-session" data-session hidden><span data-user></span><button class="secondary" data-logout>Sair</button></span></nav></div></header><main id="main"><section class="intro"><div><p class="eyebrow">Administração</p><h1>Seu catálogo, em dia.</h1><p>Cadastre produtos, ajuste preços e acompanhe o estoque.</p></div></section><div id="message" class="message" role="status" aria-live="polite" hidden></div><div id="admin-content" class="admin-layout" hidden><section class="form-panel"><h2 id="form-title">Novo produto</h2><form id="product-form"><div class="fields"><label>Nome<input name="nome" minlength="2" maxlength="120" required></label><label>Descrição<textarea name="descricao" maxlength="2000" required></textarea></label><label>Categoria<input name="categoria" maxlength="60" required></label><div class="two-cols"><label>Preço (R$)<input name="preco" type="number" min="0.01" max="99999999.99" step="0.01" required></label><label>Estoque<input name="quantidade_estoque" type="number" min="0" max="1000000" step="1" required></label></div><label>Imagem<input name="imagem_url" value="/images/placeholder.svg" maxlength="1000" required><span class="hint">URL HTTPS ou caminho em /images/.</span></label></div><div class="actions"><button id="save-product" type="submit">Cadastrar produto</button><button id="cancel-edit" type="button" class="secondary">Limpar</button></div></form></section><section aria-label="Produtos cadastrados"><div class="table-wrap"><table><thead><tr><th scope="col">Produto</th><th scope="col">Preço</th><th scope="col">Estoque</th><th scope="col">Ações</th></tr></thead><tbody id="product-rows"></tbody></table></div><div class="pagination"><button id="previous" class="secondary" disabled>Anterior</button><span id="page-number">Página 1</span><button id="next" class="secondary" disabled>Próxima</button></div></section></div></main><dialog id="confirm-dialog" aria-labelledby="dialog-title"><h2 id="dialog-title"></h2><p></p><form method="dialog" class="actions"><button class="secondary" value="cancel" autofocus>Cancelar</button><button value="confirm">Confirmar</button></form></dialog><footer><span><strong>dessik.</strong> Tecnologia para sua rotina.</span><span>Projeto acadêmico · Produtos e especificações fictícios</span></footer></body></html>
```


### Arquivo: public/cadastro.html

```html
<!doctype html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Dessik: loja fictícia de tecnologia para um projeto acadêmico."><title>Criar conta | Dessik</title><link rel="icon" href="/images/placeholder.svg" type="image/svg+xml"><link rel="stylesheet" href="/css/style.css"><link rel="stylesheet" href="/css/storefront.css"><script type="module" src="/js/cadastro.js"></script></head>
<body class="account-page"><a class="skip" href="#main">Pular para o conteúdo</a>
<div class="topnote">Loja fictícia · Compras simuladas, sem cobrança</div>
<header class="navbar"><div class="nav-inner"><a class="brand" href="/loja.html" aria-label="Dessik início">dessik<span>.</span></a>
<nav aria-label="Navegação principal"><a href="/loja.html">Produtos</a><a href="/admin.html" data-admin hidden>Administração</a>
<a href="/login.html" data-guest>Entrar</a><a class="button secondary" href="/cadastro.html" data-guest>Criar conta</a>
<span class="nav-session" data-session hidden><span data-user></span><button class="secondary" data-logout>Sair</button></span></nav></div></header><main id="main"><div class="form-layout"><section class="form-intro"><p class="eyebrow">Vamos começar</p><h1>Suas ideias.<br>Seu próximo setup.</h1><p>Crie sua conta para experimentar a loja. Todas as compras são simulações, sem pagamento.</p><a href="/loja.html">← Conhecer os produtos</a></section><section class="form-panel"><h2>Crie sua conta</h2><div id="message" class="message" role="status" aria-live="polite" hidden></div><form id="register-form"><div class="fields"><label>Nome<input name="nome" autocomplete="name" minlength="2" maxlength="100" required></label><label>E-mail<input type="email" name="email" autocomplete="email" maxlength="254" required></label><label>Senha<input type="password" name="senha" autocomplete="new-password" minlength="8" maxlength="72" aria-describedby="password-hint" required><span class="hint" id="password-hint">Pelo menos 8 caracteres. Use uma senha exclusiva.</span></label><button class="secondary" type="button" id="generate-password">Sugerir senha segura</button><label>Confirmar senha<input type="password" name="confirmar_senha" autocomplete="new-password" minlength="8" maxlength="72" required></label></div><div class="form-section"><h3>Endereço</h3><p class="hint">Opcional. Consulte o CEP ou preencha manualmente.</p></div><div class="fields"><label>CEP<input name="cep" autocomplete="postal-code" inputmode="numeric" pattern="[0-9]{5}-?[0-9]{3}" maxlength="9" placeholder="00000-000"></label><button type="button" class="secondary" id="lookup-cep">Consultar CEP</button><div class="message" id="cep-message" role="status" hidden></div><label>Logradouro<input name="logradouro" autocomplete="address-line1" maxlength="150"></label><label>Bairro<input name="bairro" maxlength="100"></label><div class="two-cols"><label>Cidade<input name="cidade" autocomplete="address-level2" maxlength="100"></label><label>Estado (UF)<input name="estado" autocomplete="address-level1" maxlength="2" pattern="[A-Za-z]{2}" placeholder="SP"></label></div></div><div class="actions"><button class="full" type="submit">Cadastrar</button></div></form><p class="form-foot">Já tem uma conta? <a href="/login.html">Entrar</a></p></section></div></main><dialog id="confirm-dialog" aria-labelledby="dialog-title"><h2 id="dialog-title"></h2><p></p><form method="dialog" class="actions"><button class="secondary" value="cancel" autofocus>Cancelar</button><button value="confirm">Confirmar</button></form></dialog><footer><span><strong>dessik.</strong> Tecnologia para sua rotina.</span><span>Projeto acadêmico · Produtos e especificações fictícios</span></footer></body></html>
```


### Arquivo: public/css/storefront.css

```css
/* Identidade Dessik. Compartilhada pela loja e pelos formulários. */
:root {
  --ink: #161a26;
  --muted: #697181;
  --green: #2855e8;
  --lime: #dce6ff;
  --line: #e5e8ef;
  --bg: #fafbfe;
  font-family: "Segoe UI", Arial, sans-serif;
}
html { scroll-behavior: smooth; scroll-padding-top: 30px; }
body { -webkit-font-smoothing: antialiased; }
button, .button, a, input { transition: background .18s, color .18s, box-shadow .18s, transform .18s; }
button, .button { border-radius: 10px; font-size: .9375rem; font-weight: 600; }
button:focus-visible, a:focus-visible, input:focus-visible, textarea:focus-visible { outline-color: #426cf1; }
.secondary { background: #edf1fb; color: #2748a9; }
.topnote { background: #1c253d; padding: 9px 20px; color: #e5eaff; font-size: .8125rem; letter-spacing: .4px; }
.navbar { background: #fff; }
.nav-inner { max-width: 1320px; padding: 22px 36px; min-height: 92px; }
.brand { font-size: 2.6rem; letter-spacing: -2.4px; line-height: 1; }
.brand span { color: #3763f3; }
nav { gap: 30px; }
nav a { color: #555d70; }
nav a:hover { color: var(--green); }
nav a.button { background: var(--ink); color: white; padding: 11px 22px; }
main { max-width: 1320px; padding: 28px 36px 70px; }
.eyebrow { letter-spacing: 2px; font-size: .75rem; color: var(--green); margin-bottom: 12px; }
.hero { display: grid; grid-template-columns: 1.1fr 1fr; min-height: 492px; overflow: hidden; border-radius: 22px; background: #121d39; }
.hero-copy { padding: 48px 46px 34px; color: #fff; display: flex; flex-direction: column; align-items: flex-start; }
.collection-label { display: flex; align-items: center; gap: 10px; color: #c6d1ed; font-size: .7rem; font-weight: 600; letter-spacing: 2px; }
.collection-label > span { width: 7px; height: 7px; border-radius: 50%; background: #83a4ff; box-shadow: 0 0 0 4px #83a4ff1a; }
.hero h1 { font-size: clamp(2.4rem,4.1vw,3.6rem); font-weight: 650; line-height: 1.08; letter-spacing: -2.4px; margin: 30px 0 20px; }
.hero h1 em { font-style: normal; color: #9eb8ff; }
.hero-copy > p { max-width: 355px; font-size: 1rem; color: #bbc6de; line-height: 1.65; margin-bottom: 25px; }
.hero-button { background: #fff; color: #182646; padding: 14px 22px; gap: 28px; }
.hero-button > span { font-size: 1.3rem; }
.hero-button:hover { transform: translateY(-2px); background: #e7edff; }
.hero-caption { border-top: 1px solid #ffffff20; display: flex; gap: 18px; width: 100%; color: #b5c2dc; font-size: .75rem; padding-top: 20px; margin-top: 35px; }
.hero-caption > span { color: #fff; font-weight: 600; white-space: nowrap; }
.hero-showcase { position: relative; display: flex; flex-direction: column; justify-content: space-between; background: #edf1f8; padding: 30px; overflow: hidden; }
.showcase-kicker { position: relative; z-index: 1; font-size: .66rem; font-weight: 700; letter-spacing: 3px; color: #586680; }
.hero-product { position: absolute; width: 100%; aspect-ratio: 1; top: 50%; left: 50%; transform: translate(-50%,-51%); }
.showcase-bottom { position: relative; z-index: 1; display: flex; justify-content: space-between; align-items: end; margin-top: auto; }
.showcase-bottom > div { display: flex; flex-direction: column; gap: 4px; }
.showcase-bottom span { font-size: .65rem; color: #59687e; letter-spacing: 2px; font-weight: 700; }
.showcase-bottom strong { font-size: 1.6rem; font-weight: 600; letter-spacing: -.7px; }
.showcase-bottom > a { background: white; color: #263b76; width: 48px; height: 48px; border-radius: 50%; display: grid; place-items: center; text-decoration: none; font-size: 1.5rem; box-shadow: 0 3px 14px #24395310; }
.store-values { display: grid; grid-template-columns: repeat(3,1fr); gap: 28px; padding: 28px 8px; border-bottom: 1px solid var(--line); margin-bottom: 38px; }
.store-values > div { display: flex; align-items: center; gap: 15px; }
.store-values > div > span { font-size: 1.8rem; color: #4164c1; width: 36px; text-align: center; }
.store-values p { display: flex; flex-direction: column; margin: 0; gap: 3px; }
.store-values strong { font-size: .875rem; font-weight: 600; }
.store-values p span { font-size: .8rem; color: var(--muted); }
.catalog-bar { border-top: 0; padding: 0; margin-bottom: 28px; align-items: end; gap: 20px; }
.catalog-bar h2 { font-size: clamp(1.9rem,3vw,2.45rem); font-weight: 600; line-height: 1.2; letter-spacing: -1.3px; margin-bottom: 12px; }
#product-count { font-size: .875rem; }
#reload { background: transparent; border: 1px solid #d7dfef; color: #4e5c7a; white-space: nowrap; }
.grid { gap: 22px; }
.card { border-radius: 15px; border-color: #e9ecf2; box-shadow: 0 4px 15px #243a6704; transition: transform .2s, box-shadow .2s, border-color .2s; }
.card:hover { transform: translateY(-5px); border-color: #ced9f2; box-shadow: 0 15px 30px #243a6710; }
.product-visual { position: relative; aspect-ratio: 1; background: #f0f3f8; overflow: hidden; }
.product-visual img { width: 100%; height: 100%; object-fit: contain; background: #f0f3f8; }
.product-art { background-image: url('/images/catalogo-dessik.png'); background-size: 400% 200%; background-repeat: no-repeat; }
.product-visual .product-art { width: 100%; height: 100%; transition: transform .35s; }
.card:hover .product-art { transform: scale(1.04); }
.art-notebook { background-position: 0% 0%; }
.art-mouse { background-position: 33.333333% 0%; }
.art-teclado { background-position: 66.666667% 0%; }
.art-monitor { background-position: 100% 0%; }
.art-headset { background-position: 0% 100%; }
.art-webcam { background-position: 33.333333% 100%; }
.art-ssd { background-position: 66.666667% 100%; }
.art-ram { background-position: 100% 100%; }
.product-tag { position: absolute; top: 13px; left: 13px; color: #43516c; background: #ffffffed; padding: 5px 9px; border-radius: 5px; font-size: .65rem; font-weight: 600; letter-spacing: .3px; }
.card-body { padding: 20px; gap: 8px; }
.card .category { font-size: .66rem; font-weight: 700; letter-spacing: 1.7px; color: #73809a; }
.card h3 { font-size: 1.12rem; font-weight: 650; line-height: 1.4; letter-spacing: -.3px; }
.description { font-size: .8125rem; line-height: 1.6; color: #7a8291; margin-bottom: 9px; }
.price { font-size: 1.55rem; font-weight: 650; letter-spacing: -.8px; }
.stock { color: #527265; font-size: .75rem; display: flex; align-items: center; gap: 6px; margin-bottom: 10px; }
.stock::before { content: ''; width: 5px; height: 5px; background: #4d9676; border-radius: 50%; flex: 0 0 auto; }
.stock.out { color: #876c70; }.stock.out::before { background: #ae9396; }
.buy-row { gap: 8px; }.buy-row button { font-size: .8125rem; border-radius: 8px; }.buy-row input { border-color: #e0e5ef; width: 58px; }
.buy-row button:disabled { background: #edf0f5; color: #8991a2; opacity: 1; }
.pagination { border-top: 1px solid var(--line); margin-top: 32px; padding-top: 22px; font-size: .8125rem; }
.pagination button { background: white; border: 1px solid var(--line); font-size: .8125rem; }
.demo-notice { background: #edf2ff; border: 1px solid #d7e2ff; padding: 13px 17px; border-radius: 10px; font-size: .8125rem; color: #496087; margin-bottom: 22px; display: flex; justify-content: space-between; gap: 16px; align-items: center; }
.demo-notice a { flex-shrink: 0; font-weight: 600; }
.message { font-size: .875rem; }
footer { max-width: 1248px; padding: 32px 0; margin: 0 auto; align-items: center; font-size: .8125rem; }
footer strong { color: #1b2440; font-size: 1.6rem; letter-spacing: -1px; margin-right: 10px; }
.account-page main { padding-top: 60px; padding-bottom: 90px; }
.form-layout { max-width: 1080px; gap: 70px; align-items: center; }
.form-intro h1 { font-size: clamp(2.8rem,4.3vw,4.3rem); font-weight: 600; letter-spacing: -2.7px; color: #192746; }
.form-intro p { line-height: 1.8; }
.form-intro a { display: inline-flex; margin-top: 18px; font-size: .9rem; }
.form-panel { padding: 34px; border-radius: 18px; border-color: #e1e7f3; box-shadow: 0 16px 55px #233a6410; }
.form-panel h2 { color: #1d2c4f; font-weight: 600; }
input, textarea { border-color: #dce2ee; background: #fcfdff; }
input:focus, textarea:focus { border-color: #416be8; box-shadow: 0 0 0 3px #416be812; }
label { color: #414c63; font-size: .875rem; }
.hint { color: #7b8597; font-size: .8125rem; }
.admin-layout .form-panel { padding: 26px; }.table-wrap { border-color: #e1e7f3; border-radius: 14px; }th { background: #f0f3fa; color: #53617c; }
dialog { border-radius: 18px; border-color: #dbe2f1; box-shadow: 0 25px 90px #0b163c33; }dialog::backdrop { background: #0d173c99; backdrop-filter: blur(4px); }
@media (min-width: 1440px) { .hero { min-height: 540px; }.hero h1 { font-size: 3.85rem; } }
@media (max-width: 1100px) {
  .hero-copy { padding: 38px 30px 28px; }.hero h1 { font-size: 3rem; }
  .hero { min-height: 480px; }.grid { grid-template-columns: repeat(3,minmax(0,1fr)); }
  .store-values { gap: 15px; }.store-values strong { font-size: .8rem; }.store-values p span { font-size: .75rem; }
  footer { margin: 0 36px; }.demo-notice { align-items: flex-start; flex-direction: column; gap: 8px; }
}
@media (max-width: 760px) {
  .nav-inner { padding: 21px 22px; min-height: 82px; }.brand { font-size: 2.3rem; }nav { gap: 17px; }nav a { font-size: .8rem; }nav a.button { padding: 9px 14px; }
  main { padding: 20px 22px 40px; }.hero { grid-template-columns: 1fr 0.85fr; min-height: 430px; border-radius: 17px; }
  .hero-copy { padding: 30px 24px; }.hero h1 { font-size: 2.45rem; letter-spacing: -1.7px; }.hero-copy > p { font-size: .875rem; }
  .collection-label { font-size: .58rem; letter-spacing: 1.1px; }.hero-button { font-size: .8rem; gap: 12px; padding: 12px 15px; }
  .hero-caption { font-size: .65rem; gap: 8px; margin-top: 26px; }.hero-showcase { padding: 22px 17px; }
  .showcase-kicker { font-size: .56rem; letter-spacing: 1.3px; }.showcase-bottom strong { font-size: 1.15rem; }.showcase-bottom span { font-size: .5rem; }
  .showcase-bottom > a { width: 36px; height: 36px; }.store-values { grid-template-columns: 1fr; padding: 22px 4px; gap: 16px; margin-bottom: 27px; }
  .store-values strong { font-size: .875rem; }.store-values p span { font-size: .8rem; }.grid { grid-template-columns: repeat(2,minmax(0,1fr)); gap: 15px; }
  .card-body { padding: 16px; }.catalog-bar h2 { font-size: 1.9rem; }#reload { font-size: .75rem; padding: 9px 12px; }
  .form-layout { gap: 30px; }.account-page main { padding-top: 30px; }.form-intro h1 { font-size: 3rem; }.form-panel { padding: 25px; }
  footer { margin: 0 22px; align-items: flex-start; }.hero-product { width: 120%; }
}
@media (max-width: 520px) {
  .nav-inner { flex-direction: row; align-items: center; gap: 15px; }nav { gap: 12px; justify-content: flex-end; }nav > a:first-child { display: none; }
  .brand { font-size: 2.05rem; }.hero { grid-template-columns: 1fr; }.hero-copy { padding: 30px 27px; }.hero h1 { font-size: 2.9rem; }
  .hero-showcase { min-height: 320px; }.hero-product { width: 330px; }.hero-caption { margin-top: 26px; }.hero-copy > p { max-width: 100%; }
  .showcase-bottom strong { font-size: 1.35rem; }.showcase-bottom span { font-size: .6rem; }.showcase-kicker { font-size: .6rem; }
  .grid { grid-template-columns: 1fr; gap: 22px; }.product-visual { aspect-ratio: 1.2; }.product-visual .product-art { width: 100%; height: auto; aspect-ratio: 1; position: absolute; top: 50%; transform: translateY(-50%); }.card:hover .product-art { transform: translateY(-50%); }
  .card-body { padding: 22px; }.card h3 { font-size: 1.25rem; }.description { font-size: .9rem; }.price { font-size: 1.7rem; }.stock { font-size: .8125rem; }.product-tag { font-size: .7rem; }
  .catalog-bar { align-items: flex-start; flex-direction: column; gap: 16px; }.catalog-bar h2 { font-size: 2rem; }.card .category { font-size: .72rem; }.buy-row button { font-size: .9rem; }
  .form-intro h1 { font-size: 2.7rem; }.account-page main { padding-bottom: 50px; }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }*, *::before, *::after { transition: none !important; }.card:hover, .hero-button:hover { transform: none; }
}
```


### Arquivo: public/css/style.css

```css
:root{color-scheme:light;--ink:#182622;--muted:#56665f;--green:#156c48;--lime:#d9f46b;--line:#dce3de;--bg:#f5f7f5;--white:#fff;--red:#aa2533;font-family:Arial,Helvetica,sans-serif;font-size:16px}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);line-height:1.5}a{color:var(--green);text-underline-offset:4px}button,input,textarea,select{font:inherit}button,.button{cursor:pointer;border:0;border-radius:8px;background:var(--green);color:white;padding:12px 18px;font-weight:700;text-decoration:none;display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:46px}button:hover,.button:hover{filter:brightness(.92)}button:disabled{cursor:not-allowed;opacity:.55}.secondary{background:#eaf0eb;color:var(--ink)}.danger{background:#fff0f0;color:var(--red)}button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible{outline:3px solid #88700c;outline-offset:3px}[hidden]{display:none!important}.skip{position:absolute;top:-80px;left:10px;background:white;padding:15px;z-index:10}.skip:focus{top:5px}
.topnote{background:var(--ink);color:#eef5ef;text-align:center;padding:8px;font-size:.875rem}.navbar{background:white;border-bottom:1px solid var(--line)}.nav-inner{max-width:1200px;margin:auto;min-height:88px;display:flex;align-items:center;justify-content:space-between;gap:24px;padding:16px 28px}.brand{color:var(--ink);font-weight:900;font-size:2rem;letter-spacing:-1.8px;text-decoration:none}.brand span{color:var(--green)}nav{display:flex;align-items:center;gap:24px;flex-wrap:wrap}nav a{color:var(--ink);text-decoration:none;font-size:.9375rem}nav a[aria-current=page]{color:var(--green);font-weight:bold}.nav-session{display:flex;align-items:center;gap:12px}.nav-session button{padding:8px 14px;min-height:40px}main{max-width:1200px;margin:0 auto;padding:38px 28px 64px}.eyebrow{color:var(--green);font-size:.875rem;letter-spacing:1.4px;text-transform:uppercase;font-weight:700}h1,h2,h3,p{margin-top:0}h1{font-size:clamp(2rem,4vw,3.3rem);line-height:1.12;letter-spacing:-1.5px;margin-bottom:18px}h2{font-size:1.6rem;letter-spacing:-.6px}h3{font-size:1.125rem}.intro{display:flex;align-items:center;justify-content:space-between;gap:24px;margin-bottom:30px}.intro p{color:var(--muted);margin-bottom:0}.pill{background:var(--lime);padding:8px 14px;border-radius:50px;font-size:.875rem;white-space:nowrap}.catalog-bar{display:flex;align-items:center;justify-content:space-between;margin-bottom:18px;padding-top:20px;border-top:1px solid var(--line)}.catalog-bar h2{margin:0}.muted{color:var(--muted)}.grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px}.card{background:white;border:1px solid var(--line);border-radius:12px;overflow:hidden;display:flex;flex-direction:column}.card img{width:100%;height:185px;object-fit:contain;background:#e9eeea}.card-body{padding:20px;display:flex;flex-direction:column;flex:1;gap:8px}.card .category{color:var(--green);font-size:.8125rem;text-transform:uppercase;letter-spacing:.8px;margin:0}.card h3{margin:0}.description{color:var(--muted);font-size:.9375rem;flex:1;margin:0 0 4px}.price{font-size:1.5rem;font-weight:700;margin:0}.stock{font-size:.875rem;color:var(--green);margin:0 0 10px}.stock.out{color:var(--red)}.buy-row{display:flex;gap:8px}.buy-row input{width:65px;padding:10px}.buy-row button{flex:1;padding:10px}.message{padding:14px 18px;border-radius:8px;background:#edf2ef;border:1px solid var(--line);margin-bottom:20px;overflow-wrap:anywhere}.message.error{background:#fff0f0;border-color:#e8bac0;color:#86212d}.message.success{background:#e5f2e9;border-color:#9dceb1;color:#15552e}.empty{padding:48px;text-align:center;background:white;border:1px dashed var(--line);border-radius:12px;grid-column:1/-1}.form-layout{display:grid;grid-template-columns:.85fr 1.15fr;gap:70px;align-items:start;max-width:1000px}.form-intro{padding-top:32px}.form-intro p{color:var(--muted);max-width:330px}.form-panel{background:white;border:1px solid var(--line);border-radius:14px;padding:30px}.form-panel h2{margin-bottom:22px}label{display:flex;flex-direction:column;gap:6px;font-size:.9375rem;font-weight:600}input,textarea,select{width:100%;border:1px solid #b8c7bd;border-radius:7px;padding:11px 12px;background:white;color:var(--ink);min-height:46px}textarea{resize:vertical;min-height:100px}.fields{display:grid;gap:18px}.two-cols{display:grid;grid-template-columns:1fr 1fr;gap:16px}.actions{display:flex;flex-wrap:wrap;gap:12px;margin-top:20px}.full{width:100%}.form-foot{font-size:.9375rem;color:var(--muted);margin:22px 0 0}.hint{font-size:.875rem;color:var(--muted);font-weight:400}.form-section{margin:24px 0 16px;border-top:1px solid var(--line);padding-top:22px}.form-section h3{margin-bottom:4px}.admin-layout{display:grid;grid-template-columns:360px 1fr;gap:28px;align-items:start}.table-wrap{overflow:auto;background:white;border:1px solid var(--line);border-radius:12px}table{width:100%;border-collapse:collapse;text-align:left;font-size:.9375rem}th,td{padding:16px;border-bottom:1px solid var(--line)}th{background:#ecf1ed;font-size:.875rem}td button{font-size:.875rem;min-height:36px;padding:6px 10px;margin:3px}.pagination{display:flex;justify-content:flex-end;align-items:center;gap:14px;margin-top:24px}footer{max-width:1200px;margin:auto;padding:24px 28px;border-top:1px solid var(--line);display:flex;justify-content:space-between;gap:15px;font-size:.875rem;color:var(--muted)}dialog{border:1px solid var(--line);border-radius:14px;padding:28px;max-width:460px;width:calc(100% - 32px)}dialog::backdrop{background:#10251eb3}dialog h2{font-size:1.5rem}dialog .actions{justify-content:flex-end}
@media(max-width:1000px){.grid{grid-template-columns:repeat(3,minmax(0,1fr))}.admin-layout{grid-template-columns:300px 1fr}.form-layout{gap:32px}}@media(max-width:760px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}.form-layout,.admin-layout{grid-template-columns:1fr}.form-intro{padding-top:0}.form-intro p{max-width:none}.nav-inner{align-items:flex-start;gap:16px;padding:16px 20px}nav{gap:14px;justify-content:flex-end}.intro{align-items:flex-start}.pill{white-space:normal}main{padding:28px 20px 44px}.form-panel{padding:24px}.nav-session{flex-wrap:wrap;justify-content:flex-end}}@media(max-width:460px){.grid,.two-cols{grid-template-columns:1fr}.card img{height:210px}.intro{display:block}.intro .pill{display:inline-block;margin-top:18px}.nav-inner{flex-direction:column}nav{justify-content:flex-start;gap:18px}.brand{font-size:1.8rem}.catalog-bar{gap:12px;align-items:flex-start}footer{flex-direction:column}.form-panel{padding:20px}}
```


### Arquivo: public/data/produtos-demo.json

```json
[
  {
    "id_produto": 1,
    "nome": "Notebook Horizon 14",
    "descricao": "Leve para estudar, criar e levar sua rotina a qualquer lugar. Tela de 14 polegadas e SSD de 512 GB.",
    "categoria": "Computadores",
    "preco": "3299.90",
    "quantidade_estoque": 8,
    "imagem_url": "/images/catalogo-dessik.png"
  },
  {
    "id_produto": 2,
    "nome": "Mouse Pulse",
    "descricao": "Precisão e conforto para trabalhar e jogar. Sensor de 6.400 DPI e seis botões.",
    "categoria": "Periféricos",
    "preco": "129.90",
    "quantidade_estoque": 24,
    "imagem_url": "/images/catalogo-dessik.png"
  },
  {
    "id_produto": 3,
    "nome": "Teclado mecânico Type",
    "descricao": "Formato compacto, conexão USB e teclas mecânicas para o seu setup.",
    "categoria": "Periféricos",
    "preco": "249.90",
    "quantidade_estoque": 15,
    "imagem_url": "/images/catalogo-dessik.png"
  },
  {
    "id_produto": 4,
    "nome": "Monitor View 24",
    "descricao": "Mais espaço para suas ideias. Painel de 24 polegadas Full HD com conexão HDMI.",
    "categoria": "Monitores",
    "preco": "899.90",
    "quantidade_estoque": 6,
    "imagem_url": "/images/catalogo-dessik.png"
  },
  {
    "id_produto": 5,
    "nome": "Headset Wave",
    "descricao": "Áudio estéreo, microfone ajustável e almofadas macias para longas sessões.",
    "categoria": "Áudio",
    "preco": "189.90",
    "quantidade_estoque": 18,
    "imagem_url": "/images/catalogo-dessik.png"
  },
  {
    "id_produto": 6,
    "nome": "Webcam Focus",
    "descricao": "Videochamadas em Full HD com microfone integrado e suporte para monitor.",
    "categoria": "Periféricos",
    "preco": "219.90",
    "quantidade_estoque": 0,
    "imagem_url": "/images/catalogo-dessik.png"
  },
  {
    "id_produto": 7,
    "nome": "SSD Sprint 1 TB",
    "descricao": "Espaço e velocidade para arquivos, jogos e projetos. Interface SATA.",
    "categoria": "Componentes",
    "preco": "399.90",
    "quantidade_estoque": 20,
    "imagem_url": "/images/catalogo-dessik.png"
  },
  {
    "id_produto": 8,
    "nome": "Memória RAM Flux 16 GB",
    "descricao": "Mais fôlego para várias tarefas. Módulo DDR4 de 3.200 MHz.",
    "categoria": "Componentes",
    "preco": "229.90",
    "quantidade_estoque": 12,
    "imagem_url": "/images/catalogo-dessik.png"
  }
]
```


### Arquivo: public/images/catalogo-dessik.png

Asset de imagem: [catalogo-dessik.png](../public/images/catalogo-dessik.png). Copie o arquivo binário junto com o projeto.


### Arquivo: public/images/placeholder.svg

```xml
<svg xmlns="http://www.w3.org/2000/svg" width="640" height="420" viewBox="0 0 640 420"><rect width="640" height="420" fill="#e9eeea"/><text x="320" y="205" text-anchor="middle" font-family="Arial,sans-serif" font-size="60" font-weight="bold" letter-spacing="-3" fill="#156c48">dessik.</text><text x="320" y="250" text-anchor="middle" font-family="Arial,sans-serif" font-size="18" letter-spacing="3" fill="#56665f">IMAGEM ILUSTRATIVA</text></svg>
```


### Arquivo: public/index.html

```html
<!doctype html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Dessik: loja fictícia de tecnologia para um projeto acadêmico."><title>Loja | Dessik</title><link rel="icon" href="/images/placeholder.svg" type="image/svg+xml"><link rel="stylesheet" href="/css/style.css"><link rel="stylesheet" href="/css/storefront.css"><script type="module" src="/js/loja.js"></script></head>
<body class="store-page"><a class="skip" href="#main">Pular para o conteúdo</a>
<div class="topnote">Loja fictícia · Compras simuladas, sem cobrança</div>
<header class="navbar"><div class="nav-inner"><a class="brand" href="/loja.html" aria-label="Dessik início">dessik<span>.</span></a>
<nav aria-label="Navegação principal"><a href="/loja.html" aria-current="page">Explorar produtos</a><a href="/admin.html" data-admin hidden>Administração</a>
<a href="/login.html" data-guest>Entrar</a><a class="button secondary" href="/cadastro.html" data-guest>Criar conta</a>
<span class="nav-session" data-session hidden><span data-user></span><button class="secondary" data-logout>Sair</button></span></nav></div></header><main id="main"><section class="hero" aria-labelledby="hero-title">
<div class="hero-copy"><span class="collection-label"><span></span> DESSIK ESSENTIALS / VOL. 01</span>
<h1 id="hero-title">Seu espaço.<br>Seu estilo.<br><em>Seu próximo nível.</em></h1>
<p>O essencial para transformar suas ideias em realidade. Tecnologia que combina com você.</p>
<a class="button hero-button" href="#catalogo">Encontre seu upgrade <span aria-hidden="true">↗</span></a>
<div class="hero-caption"><span>01 — 08</span> Uma seleção para criar, jogar e ir além.</div></div>
<div class="hero-showcase"><span class="showcase-kicker">DESIGN QUE VOCÊ SENTE.</span>
<div class="hero-product product-art art-headset" role="img" aria-label="Headset fictício preto com detalhes azuis"></div>
<div class="showcase-bottom"><div><span>ÁUDIO / ESSENTIALS</span><strong>Headset Wave</strong></div><a href="#catalogo" aria-label="Explorar o catálogo">↙</a></div>
</div></section>
<div class="store-values" aria-label="Sobre a loja"><div><span aria-hidden="true">✳</span><p><strong>Escolhas com personalidade</strong><span>Do primeiro setup ao próximo upgrade</span></p></div><div><span aria-hidden="true">◇</span><p><strong>Estoque transparente</strong><span>Disponibilidade em cada produto</span></p></div><div><span aria-hidden="true">↗</span><p><strong>Explore sem compromisso</strong><span>Uma experiência de compra fictícia</span></p></div></div>
<div id="demo-notice" class="demo-notice" hidden><span><strong>Catálogo demonstrativo</strong> · Produtos e preços fictícios. Compras disponíveis somente com a API e o banco conectados.</span><a href="/loja.html">Tentar loja conectada ↗</a></div>
<div id="message" class="message" role="status" aria-live="polite" hidden></div>
<section id="catalogo" aria-labelledby="catalog-title"><div class="catalog-bar"><div><p class="eyebrow">CURADORIA DESSIK</p><h2 id="catalog-title">Pequenos detalhes.<br>Grandes possibilidades.</h2><span id="product-count" class="muted">Carregando catálogo…</span></div><button id="reload" class="secondary">Atualizar catálogo ↻</button></div><div id="products" class="grid" aria-busy="true"></div><div class="pagination"><button id="previous" class="secondary" disabled>Anterior</button><span id="page-number">Página 1</span><button id="next" class="secondary" disabled>Próxima</button></div></section></main><dialog id="confirm-dialog" aria-labelledby="dialog-title"><h2 id="dialog-title"></h2><p></p><form method="dialog" class="actions"><button class="secondary" value="cancel" autofocus>Cancelar</button><button value="confirm">Confirmar</button></form></dialog><footer><span><strong>dessik.</strong> Tecnologia para sua rotina.</span><span>Projeto acadêmico · Produtos e especificações fictícios</span></footer></body></html>
```


### Arquivo: public/js/admin.js

```javascript
import {apiRequest, message, money, element, setupSession, confirmAction} from './api.js';
const form = document.querySelector('#product-form');
const table = document.querySelector('#product-rows');
let editing = null;
let offset = 0;
const limit = 20;
function resetForm() {
  form.reset(); editing = null;
  document.querySelector('#form-title').textContent = 'Novo produto';
  document.querySelector('#save-product').textContent = 'Cadastrar produto';
}
async function loadProducts() {
  const products = await apiRequest(`/produtos?limite=${limit}&offset=${offset}`);
  table.replaceChildren();
  for (const product of products) {
    const row = element('tr');
    row.append(element('td', `#${product.id_produto} ${product.nome}`), element('td', money(product.preco)),
      element('td', String(product.quantidade_estoque)));
    const actions = element('td');
    const edit = element('button', 'Editar', 'secondary');
    edit.setAttribute('aria-label', `Editar ${product.nome}`);
    edit.onclick = () => {
      editing = product.id_produto;
      for (const key of ['nome', 'descricao', 'categoria', 'preco', 'quantidade_estoque', 'imagem_url']) form.elements[key].value = product[key];
      document.querySelector('#form-title').textContent = `Editar produto #${editing}`;
      document.querySelector('#save-product').textContent = 'Salvar alterações';
      form.elements.nome.focus();
    };
    const remove = element('button', 'Excluir', 'danger');
    remove.setAttribute('aria-label', `Excluir ${product.nome}`);
    remove.onclick = async () => {
      if (!await confirmAction('Excluir produto?', `O produto ${product.nome} será removido do catálogo.`, 'Excluir')) return;
      remove.disabled = true;
      try {
        await apiRequest(`/produtos/${product.id_produto}`, {method: 'DELETE', auth: true});
        if (editing === product.id_produto) resetForm();
        message('Produto excluído.', 'success');
        await loadProducts();
      } catch (error) { message(error.message); }
      finally { remove.disabled = false; }
    };
    actions.append(edit, remove); row.append(actions); table.append(row);
  }
  if (!products.length) {
    const row = element('tr'); const cell = element('td', 'Nenhum produto nesta página.');
    cell.colSpan = 4; row.append(cell); table.append(row);
  }
  document.querySelector('#previous').disabled = offset === 0;
  document.querySelector('#next').disabled = products.length < limit;
  document.querySelector('#page-number').textContent = `Página ${offset / limit + 1}`;
}
async function refresh() { try { await loadProducts(); } catch (error) { message(error.message); } }
form.addEventListener('submit', async event => {
  event.preventDefault();
  const button = document.querySelector('#save-product'); button.disabled = true;
  try {
    const body = Object.fromEntries(new FormData(form));
    body.quantidade_estoque = Number(body.quantidade_estoque);
    const data = await apiRequest(editing ? `/produtos/${editing}` : '/produtos',
      {method: editing ? 'PUT' : 'POST', auth: true, body});
    resetForm(); message(data.mensagem, 'success'); await refresh();
  } catch (error) { message(error.message); }
  finally { button.disabled = false; }
});
document.querySelector('#cancel-edit').onclick = resetForm;
document.querySelector('#previous').onclick = () => { offset = Math.max(0, offset - limit); refresh(); };
document.querySelector('#next').onclick = () => { offset += limit; refresh(); };
const user = await setupSession(true, true);
if (user) { document.querySelector('#admin-content').hidden = false; await refresh(); }
```


### Arquivo: public/js/api.js

```javascript
export const money = value => Number(value).toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'});

export async function apiRequest(path, {method = 'GET', body, auth = false} = {}) {
  const headers = {};
  if (body !== undefined) headers['Content-Type'] = 'application/json';
  if (auth) {
    const token = sessionStorage.getItem('dessik_token');
    if (!token) throw new Error('Entre na sua conta para continuar.');
    headers.Authorization = `Bearer ${token}`;
  }
  let response;
  try {
    response = await fetch(`/api${path}`, {method, headers, cache: 'no-store',
      body: body === undefined ? undefined : JSON.stringify(body)});
  } catch {
    throw new Error('Sem conexão com a loja. Verifique sua internet e tente novamente.');
  }
  let data;
  try { data = await response.json(); }
  catch { throw new Error('O servidor não respondeu corretamente. Tente novamente.'); }
  if (!response.ok) {
    if (response.status === 401 && auth) sessionStorage.removeItem('dessik_token');
    const detail = data.erros?.map(item => `${item.campo || 'Dados'}: ${item.mensagem}`).join(' ');
    const error = new Error(detail || data.mensagem || 'Não foi possível concluir a operação.');
    error.status = response.status;
    throw error;
  }
  return data;
}

export function message(text = '', kind = 'error', target = document.querySelector('#message')) {
  target.textContent = text;
  target.className = `message ${kind}`;
  target.hidden = !text;
}

export function element(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text; // Dados do banco nunca viram HTML executável.
  if (className) node.className = className;
  return node;
}

export async function setupSession(required = false, admin = false) {
  const token = sessionStorage.getItem('dessik_token');
  if (!token) {
    if (required) location.replace('/login.html');
    return null;
  }
  try {
    const user = await apiRequest('/me', {auth: true});
    document.querySelectorAll('[data-guest]').forEach(el => el.hidden = true);
    document.querySelectorAll('[data-session]').forEach(el => el.hidden = false);
    document.querySelectorAll('[data-admin]').forEach(el => el.hidden = !user.is_admin);
    document.querySelectorAll('[data-user]').forEach(el => el.textContent = user.nome.split(' ')[0]);
    document.querySelectorAll('[data-logout]').forEach(el => el.onclick = () => {
      sessionStorage.removeItem('dessik_token');
      location.assign('/login.html');
    });
    if (admin && !user.is_admin) throw new Error('Esta área está disponível apenas para administradores.');
    return user;
  } catch (error) {
    if (error.status === 401) {
      sessionStorage.removeItem('dessik_token');
      if (required) location.replace('/login.html');
    }
    if (required) message(error.message);
    return null;
  }
}

export function confirmAction(title, description, action = 'Confirmar') {
  return new Promise(resolve => {
    const dialog = document.querySelector('#confirm-dialog');
    dialog.querySelector('h2').textContent = title;
    dialog.querySelector('p').textContent = description;
    dialog.querySelector('[value="confirm"]').textContent = action;
    dialog.returnValue = 'cancel';
    dialog.addEventListener('close', () => resolve(dialog.returnValue === 'confirm'), {once: true});
    dialog.showModal();
  });
}
```


### Arquivo: public/js/cadastro.js

```javascript
import {apiRequest, message, setupSession} from './api.js';
setupSession();
const form = document.querySelector('#register-form');
const cepMessage = document.querySelector('#cep-message');
const senha = form.elements.senha;
const confirmation = form.elements.confirmar_senha;
function validatePasswords() {
  confirmation.setCustomValidity(confirmation.value && confirmation.value !== senha.value ? 'As senhas não coincidem.' : '');
  senha.setCustomValidity(new TextEncoder().encode(senha.value).length > 72 ? 'Use no máximo 72 bytes na senha.' : '');
}
senha.addEventListener('input', validatePasswords);
confirmation.addEventListener('input', validatePasswords);
document.querySelector('#generate-password').addEventListener('click', async event => {
  const button = event.currentTarget;
  button.disabled = true;
  try {
    const data = await apiRequest('/gerar-senha');
    senha.value = confirmation.value = data.senha;
    senha.type = 'text';
    validatePasswords();
    message('Senha sugerida preenchida. Guarde-a antes de cadastrar.', 'success');
  } catch (error) { message(error.message); }
  finally { button.disabled = false; }
});
document.querySelector('#lookup-cep').addEventListener('click', async event => {
  const value = form.elements.cep.value.replace(/\D/g, '');
  if (value.length !== 8) return message('Informe os 8 números do CEP.', 'error', cepMessage);
  const button = event.currentTarget;
  button.disabled = true;
  message('Consultando CEP…', '', cepMessage);
  try {
    const address = await apiRequest(`/cep/${value}`);
    // Não substitui um endereço caso o usuário tenha alterado o CEP durante a consulta.
    if (form.elements.cep.value.replace(/\D/g, '') !== value) return;
    for (const key of ['logradouro', 'bairro', 'cidade', 'estado']) form.elements[key].value = address[key];
    message('Endereço encontrado. Confira os dados abaixo.', 'success', cepMessage);
  } catch (error) { message(error.message, 'error', cepMessage); }
  finally { button.disabled = false; }
});
form.addEventListener('submit', async event => {
  event.preventDefault();
  validatePasswords();
  if (!form.reportValidity()) return;
  const button = form.querySelector('[type="submit"]');
  button.disabled = true;
  message();
  try {
    const body = Object.fromEntries(new FormData(form));
    body.cep = body.cep.replace(/\D/g, '');
    await apiRequest('/cadastro', {method: 'POST', body});
    location.assign('/login.html?cadastro=ok');
  } catch (error) { message(error.message); }
  finally { button.disabled = false; }
});
```


### Arquivo: public/js/login.js

```javascript
import {apiRequest, message, setupSession} from './api.js';
setupSession();
if (new URLSearchParams(location.search).get('cadastro') === 'ok') {
  message('Conta criada com sucesso. Entre para começar.', 'success');
}
document.querySelector('#login-form').addEventListener('submit', async event => {
  event.preventDefault();
  const form = event.currentTarget;
  const button = form.querySelector('[type="submit"]');
  button.disabled = true;
  message();
  try {
    const data = await apiRequest('/login', {method: 'POST', body: Object.fromEntries(new FormData(form))});
    sessionStorage.setItem('dessik_token', data.access_token);
    location.assign('/loja.html');
  } catch (error) { message(error.message); }
  finally { button.disabled = false; }
});
```


### Arquivo: public/js/loja.js

```javascript
import {apiRequest, message, money, element, setupSession, confirmAction} from './api.js';
setupSession();
const grid = document.querySelector('#products');
let offset = 0;
const limit = 12;
let demo = new URLSearchParams(location.search).get('demo') === '1';
const productArt = new Map([
  ['Notebook Horizon 14', 'notebook'], ['Mouse Pulse', 'mouse'],
  ['Teclado mecânico Type', 'teclado'], ['Monitor View 24', 'monitor'],
  ['Headset Wave', 'headset'], ['Webcam Focus', 'webcam'],
  ['SSD Sprint 1 TB', 'ssd'], ['Memória RAM Flux 16 GB', 'ram'],
]);
function card(product) {
  const article = element('article', undefined, 'card');
  const visual = element('div', undefined, 'product-visual');
  const image = element('img');
  image.src = product.imagem_url;
  image.alt = product.nome;
  image.loading = 'lazy';
  image.addEventListener('error', () => image.src = '/images/placeholder.svg', {once: true});
  const art = productArt.get(product.nome);
  if (art && ['/images/placeholder.svg', '/images/catalogo-dessik.png'].includes(product.imagem_url)) {
    const sprite = element('div', undefined, `product-art art-${art}`);
    sprite.setAttribute('role', 'img');
    sprite.setAttribute('aria-label', `Ilustração de ${product.nome}`);
    visual.append(sprite);
  } else visual.append(image);
  visual.append(element('span', product.quantidade_estoque ? 'Coleção Essentials' : 'Esgotado', 'product-tag'));
  const body = element('div', undefined, 'card-body');
  body.append(element('p', product.categoria, 'category'),
    element('h3', product.nome), element('p', product.descricao, 'description'),
    element('p', money(product.preco), 'price'),
    element('p', product.quantidade_estoque ? `${product.quantidade_estoque} unidades ${demo ? 'ilustrativas' : 'disponíveis'}` : 'Produto indisponível',
      product.quantidade_estoque ? 'stock' : 'stock out'));
  const row = element('div', undefined, 'buy-row');
  const quantity = element('input');
  quantity.type = 'number'; quantity.min = '1'; quantity.max = String(Math.min(product.quantidade_estoque, 1000)); quantity.value = '1';
  quantity.setAttribute('aria-label', `Quantidade de ${product.nome}`);
  quantity.disabled = product.quantidade_estoque === 0;
  const button = element('button', demo ? 'Conhecer produto ↗' : product.quantidade_estoque ? 'Comprar ↗' : 'Indisponível');
  if (demo) quantity.hidden = true;
  button.disabled = product.quantidade_estoque === 0;
  button.addEventListener('click', async () => {
    if (demo) {
      await confirmAction(product.nome, `${product.descricao} Preço fictício: ${money(product.preco)}. Para simular uma compra com estoque, configure o banco e abra a loja conectada.`, 'Entendi');
      return;
    }
    if (!sessionStorage.getItem('dessik_token')) { location.assign('/login.html'); return; }
    const amount = Number(quantity.value);
    if (!Number.isInteger(amount) || amount < 1 || !quantity.reportValidity()) {
      message('Informe uma quantidade válida.'); return;
    }
    button.disabled = true;
    try {
      const confirmed = await confirmAction('Simular compra', `${amount} × ${product.nome} — ${money(Number(product.preco) * amount)}. Nenhuma cobrança será realizada.`, 'Confirmar compra');
      if (!confirmed) return;
      const order = await apiRequest('/pedidos', {method: 'POST', auth: true,
        body: {itens: [{id_produto: product.id_produto, quantidade: amount}]}});
      message(`Pedido #${order.id_pedido} confirmado · ${money(order.valor_total)}. ${order.mensagem}`, 'success');
      await loadProducts(false);
    } catch (error) {
      message(error.message);
      if (error.status === 409) await loadProducts(false);
    } finally { button.disabled = product.quantidade_estoque === 0; }
  });
  row.append(quantity, button); body.append(row); article.append(visual, body);
  return article;
}
async function loadProducts(clear = true) {
  if (clear) message();
  grid.setAttribute('aria-busy', 'true');
  try {
    let products;
    if (demo) {
      const response = await fetch('/data/produtos-demo.json');
      if (!response.ok) throw new Error('Não foi possível abrir o catálogo demonstrativo.');
      products = (await response.json()).slice(offset, offset + limit);
    } else {
      try {
        products = await apiRequest(`/produtos?limite=${limit}&offset=${offset}`);
      } catch (error) {
        // Demonstração identificada; não representa estoque ou pedidos de um banco ativo.
        demo = true;
        message('A loja conectada está indisponível. Você está vendo apenas o catálogo demonstrativo.', '');
        await loadProducts(false);
        return;
      }
    }
    document.querySelector('#demo-notice').hidden = !demo;
    grid.replaceChildren(...products.map(card));
    if (!products.length) grid.append(element('p', 'Nenhum produto nesta página.', 'empty'));
    document.querySelector('#product-count').textContent = `${products.length} produtos para o seu próximo upgrade`;
    document.querySelector('#previous').disabled = offset === 0;
    document.querySelector('#next').disabled = products.length < limit;
    document.querySelector('#page-number').textContent = `Página ${offset / limit + 1}`;
  } catch (error) {
    grid.replaceChildren(element('p', 'Não foi possível carregar o catálogo.', 'empty'));
    message(error.message);
  } finally { grid.setAttribute('aria-busy', 'false'); }
}
document.querySelector('#previous').onclick = () => { offset = Math.max(0, offset - limit); loadProducts(); };
document.querySelector('#next').onclick = () => { offset += limit; loadProducts(); };
document.querySelector('#reload').onclick = () => { demo = false; offset = 0; loadProducts(); };
loadProducts();
```


### Arquivo: public/login.html

```html
<!doctype html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Dessik: loja fictícia de tecnologia para um projeto acadêmico."><title>Entrar | Dessik</title><link rel="icon" href="/images/placeholder.svg" type="image/svg+xml"><link rel="stylesheet" href="/css/style.css"><link rel="stylesheet" href="/css/storefront.css"><script type="module" src="/js/login.js"></script></head>
<body class="account-page"><a class="skip" href="#main">Pular para o conteúdo</a>
<div class="topnote">Loja fictícia · Compras simuladas, sem cobrança</div>
<header class="navbar"><div class="nav-inner"><a class="brand" href="/loja.html" aria-label="Dessik início">dessik<span>.</span></a>
<nav aria-label="Navegação principal"><a href="/loja.html">Produtos</a><a href="/admin.html" data-admin hidden>Administração</a>
<a href="/login.html" data-guest>Entrar</a><a class="button secondary" href="/cadastro.html" data-guest>Criar conta</a>
<span class="nav-session" data-session hidden><span data-user></span><button class="secondary" data-logout>Sair</button></span></nav></div></header><main id="main"><div class="form-layout"><section class="form-intro"><p class="eyebrow">Bom ter você de volta</p><h1>Seu setup começa<br>por aqui.</h1><p>Entre na sua conta para explorar os produtos e simular sua próxima compra.</p><a href="/loja.html">← Continuar explorando</a></section><section class="form-panel"><h2>Entrar na conta</h2><div id="message" class="message" role="status" aria-live="polite" hidden></div><form id="login-form"><div class="fields"><label>E-mail<input type="email" name="email" autocomplete="email" maxlength="254" required></label><label>Senha<input type="password" name="senha" autocomplete="current-password" maxlength="72" required></label></div><div class="actions"><button class="full" type="submit">Entrar</button></div></form><p class="form-foot">Ainda não tem conta? <a href="/cadastro.html">Cadastre-se</a></p></section></div></main><dialog id="confirm-dialog" aria-labelledby="dialog-title"><h2 id="dialog-title"></h2><p></p><form method="dialog" class="actions"><button class="secondary" value="cancel" autofocus>Cancelar</button><button value="confirm">Confirmar</button></form></dialog><footer><span><strong>dessik.</strong> Tecnologia para sua rotina.</span><span>Projeto acadêmico · Produtos e especificações fictícios</span></footer></body></html>
```


### Arquivo: public/loja.html

```html
<!doctype html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Dessik: loja fictícia de tecnologia para um projeto acadêmico."><title>Loja | Dessik</title><link rel="icon" href="/images/placeholder.svg" type="image/svg+xml"><link rel="stylesheet" href="/css/style.css"><link rel="stylesheet" href="/css/storefront.css"><script type="module" src="/js/loja.js"></script></head>
<body class="store-page"><a class="skip" href="#main">Pular para o conteúdo</a>
<div class="topnote">Loja fictícia · Compras simuladas, sem cobrança</div>
<header class="navbar"><div class="nav-inner"><a class="brand" href="/loja.html" aria-label="Dessik início">dessik<span>.</span></a>
<nav aria-label="Navegação principal"><a href="/loja.html" aria-current="page">Explorar produtos</a><a href="/admin.html" data-admin hidden>Administração</a>
<a href="/login.html" data-guest>Entrar</a><a class="button secondary" href="/cadastro.html" data-guest>Criar conta</a>
<span class="nav-session" data-session hidden><span data-user></span><button class="secondary" data-logout>Sair</button></span></nav></div></header><main id="main"><section class="hero" aria-labelledby="hero-title">
<div class="hero-copy"><span class="collection-label"><span></span> DESSIK ESSENTIALS / VOL. 01</span>
<h1 id="hero-title">Seu espaço.<br>Seu estilo.<br><em>Seu próximo nível.</em></h1>
<p>O essencial para transformar suas ideias em realidade. Tecnologia que combina com você.</p>
<a class="button hero-button" href="#catalogo">Encontre seu upgrade <span aria-hidden="true">↗</span></a>
<div class="hero-caption"><span>01 — 08</span> Uma seleção para criar, jogar e ir além.</div></div>
<div class="hero-showcase"><span class="showcase-kicker">DESIGN QUE VOCÊ SENTE.</span>
<div class="hero-product product-art art-headset" role="img" aria-label="Headset fictício preto com detalhes azuis"></div>
<div class="showcase-bottom"><div><span>ÁUDIO / ESSENTIALS</span><strong>Headset Wave</strong></div><a href="#catalogo" aria-label="Explorar o catálogo">↙</a></div>
</div></section>
<div class="store-values" aria-label="Sobre a loja"><div><span aria-hidden="true">✳</span><p><strong>Escolhas com personalidade</strong><span>Do primeiro setup ao próximo upgrade</span></p></div><div><span aria-hidden="true">◇</span><p><strong>Estoque transparente</strong><span>Disponibilidade em cada produto</span></p></div><div><span aria-hidden="true">↗</span><p><strong>Explore sem compromisso</strong><span>Uma experiência de compra fictícia</span></p></div></div>
<div id="demo-notice" class="demo-notice" hidden><span><strong>Catálogo demonstrativo</strong> · Produtos e preços fictícios. Compras disponíveis somente com a API e o banco conectados.</span><a href="/loja.html">Tentar loja conectada ↗</a></div>
<div id="message" class="message" role="status" aria-live="polite" hidden></div>
<section id="catalogo" aria-labelledby="catalog-title"><div class="catalog-bar"><div><p class="eyebrow">CURADORIA DESSIK</p><h2 id="catalog-title">Pequenos detalhes.<br>Grandes possibilidades.</h2><span id="product-count" class="muted">Carregando catálogo…</span></div><button id="reload" class="secondary">Atualizar catálogo ↻</button></div><div id="products" class="grid" aria-busy="true"></div><div class="pagination"><button id="previous" class="secondary" disabled>Anterior</button><span id="page-number">Página 1</span><button id="next" class="secondary" disabled>Próxima</button></div></section></main><dialog id="confirm-dialog" aria-labelledby="dialog-title"><h2 id="dialog-title"></h2><p></p><form method="dialog" class="actions"><button class="secondary" value="cancel" autofocus>Cancelar</button><button value="confirm">Confirmar</button></form></dialog><footer><span><strong>dessik.</strong> Tecnologia para sua rotina.</span><span>Projeto acadêmico · Produtos e especificações fictícios</span></footer></body></html>
```

## ETAPA 7 — Variáveis de ambiente

Copie `.env.example` para `.env`. Nunca publique o arquivo real.

| Variável | Conteúdo |
|---|---|
| `APP_ENV` | `development` local, `production` na Vercel |
| `DB_HOST` | Host fornecido pelo provedor |
| `DB_PORT` | Porta do provedor, normalmente 3306 ou 4000 |
| `DB_USER` | Usuário do banco |
| `DB_PASSWORD` | Senha do banco |
| `DB_NAME` | Nome do banco previamente criado |
| `DB_SSL` | `true` remoto; `false` somente em desenvolvimento local |
| `DB_SSL_CA` | Caminho opcional do certificado CA PEM |
| `JWT_SECRET` | Chave aleatória, no mínimo 32 bytes |
| `JWT_ALGORITHM` | `HS256`, único algoritmo aceito |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 60 por padrão; de 1 a 1.440 |
| `CORS_ORIGINS` | Vazio para mesma origem; origens extras separadas por vírgula |

Gere a chave, copie a saída para `JWT_SECRET` e guarde-a somente no `.env` e na Vercel:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Coloque entre aspas valores que contenham caracteres especiais para o formato `.env`, por exemplo `DB_PASSWORD="valor fornecido pelo provedor"`. A aplicação passa os campos separadamente ao driver, sem montar uma URL que exija escapar a senha.

Na mesma origem, deixe `CORS_ORIGINS` vazio. Se usar um servidor estático separado, informe a origem exata, como `http://127.0.0.1:5500`, e adapte o endereço base de `api.js` e o `connect-src` da CSP desse servidor. `localhost` e `127.0.0.1` são origens diferentes. CORS não substitui autenticação. `*` é rejeitado pela configuração.



### Arquivo: .env.example

```text
APP_ENV=development
DB_HOST=seu-host-mysql-remoto
DB_PORT=3306
DB_USER=seu_usuario
DB_PASSWORD=
DB_NAME=loja_ficticia
# Em produção TLS é obrigatório. Para MySQL local, use false.
DB_SSL=true
# Opcional: caminho para CA PEM do provedor. Sem caminho, usa CAs do sistema.
DB_SSL_CA=
JWT_SECRET=
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
# Vazio = frontend e API na mesma origem. Separe origens extras por vírgula.
CORS_ORIGINS=
```


### Arquivo: .gitignore

```text
.env
.env.*
!.env.example
__pycache__/
*.py[cod]
.venv/
venv/
.pytest_cache/
.vercel/
.local/
*.log
certs/*
!certs/.gitkeep
```


### Arquivo: .vercelignore

```text
.env
.env.*
.venv
.local
.git
tests
docs
certs
```

## ETAPA 8 — Dependências

`requirements.txt` fixa as bibliotecas diretas usadas na aplicação. `requirements-dev.txt` acrescenta pytest. `requirements-lock.txt` registra todas as versões do ambiente validado, inclusive transitivas; pode ser usado para reproduzir esse ambiente com `pip install -r requirements-lock.txt`. Python 3.13 foi usado na validação.

```bash
python -m pip install -r requirements.txt
```

Não é necessário instalar Node, framework de CSS ou compilador front-end.



### Arquivo: requirements.txt

```text
fastapi==0.135.1
uvicorn==0.41.0
mysql-connector-python==9.6.0
python-dotenv==1.2.2
PyJWT==2.12.1
bcrypt==5.0.0
httpx==0.28.1
email-validator==2.3.0
```


### Arquivo: requirements-dev.txt

```text
-r requirements.txt
pytest==9.0.2
```


### Arquivo: requirements-lock.txt

```text
annotated-doc==0.0.5
annotated-types==0.8.0
anyio==4.15.1
bcrypt==5.0.0
certifi==2026.7.22
click==8.5.0
colorama==0.4.6
dnspython==2.8.0
email-validator==2.3.0
fastapi==0.135.1
h11==0.16.0
httpcore==1.0.9
httpx==0.28.1
idna==3.19
iniconfig==2.3.0
mysql-connector-python==9.6.0
packaging==26.3
pluggy==1.6.0
pydantic==2.13.5
pydantic_core==2.46.5
Pygments==2.21.0
PyJWT==2.12.1
pytest==9.0.2
python-dotenv==1.2.2
starlette==1.6.0
typing-inspection==0.4.4
typing_extensions==4.16.0
uvicorn==0.41.0
```

## ETAPA 9 — Configuração Vercel

`api/index.py` exporta `app`. `pyproject.toml` declara explicitamente `entrypoint = "api.index:app"`. `vercel.json` seleciona FastAPI, define duração de 30 segundos e cabeçalhos. `public/` é servido como arquivos estáticos. Localmente esse diretório é montado apenas quando `VERCEL` não é `1`.

A configuração segue o [suporte atual de FastAPI da Vercel](https://vercel.com/docs/frameworks/backend/fastapi), consultado em 08/09/2026. Não usa builders legados `@vercel/python`, runtimes inventados ou reescrita geral que converta endpoints em HTML. A raiz do projeto na Vercel deve ser a pasta que contém `pyproject.toml` e `vercel.json`.



### Arquivo: api/__init__.py

```python
"""Entrada ASGI da aplicação."""
```


### Arquivo: api/index.py

```python
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from mysql.connector import Error as DatabaseError
from starlette.exceptions import HTTPException

from backend.config import settings
from backend.routes import cep, pedidos, produtos, usuarios


@asynccontextmanager
async def lifespan(app):
    settings()  # Valida configuração no início, sem abrir conexão permanente.
    yield


app = FastAPI(title="Dessik • API da loja", version="1.0.0", lifespan=lifespan,
              docs_url="/api/docs", redoc_url=None, openapi_url="/api/openapi.json")
origins = [value.strip() for value in os.getenv("CORS_ORIGINS", "").split(",") if value.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False,
                   allow_methods=["GET", "POST", "PUT", "DELETE"],
                   allow_headers=["Authorization", "Content-Type"])


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    if request.url.path.startswith("/api/"):
        response.headers["Cache-Control"] = "no-store"
    if not request.url.path.startswith("/api/docs"):
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; style-src 'self'; "
            "img-src 'self' https:; connect-src 'self'; object-src 'none'; "
            "base-uri 'self'; frame-ancestors 'none'; form-action 'self'")
    return response


@app.exception_handler(HTTPException)
async def http_error(request, error):
    return JSONResponse({"mensagem": error.detail}, status_code=error.status_code, headers=error.headers)


@app.exception_handler(RequestValidationError)
async def validation_error(request, error):
    # Nunca devolva error.input: pode conter senhas enviadas pelo usuário.
    fields = [{"campo": ".".join(str(part) for part in item["loc"][1:]),
               "mensagem": item["msg"]} for item in error.errors()]
    return JSONResponse({"mensagem": "Confira os campos informados.", "erros": fields}, status_code=422)


@app.exception_handler(DatabaseError)
async def database_error(request, error):
    logging.getLogger("dessik").error("Falha MySQL: código %s", error.errno)
    if error.errno in (1205, 1213):
        return JSONResponse({"mensagem": "Operação concorrente. Atualize os dados e tente novamente."}, status_code=409)
    return JSONResponse({"mensagem": "Banco indisponível. Tente novamente mais tarde."}, status_code=503)


@app.exception_handler(Exception)
async def unexpected_error(request, error):
    logging.getLogger("dessik").error("Falha inesperada: %s", type(error).__name__)
    return JSONResponse({"mensagem": "Não foi possível concluir a operação."}, status_code=500)


@app.get("/api/health", tags=["Sistema"])
def health():
    return {"status": "ok"}


for router in (usuarios.router, produtos.router, pedidos.router, cep.router):
    app.include_router(router, prefix="/api")


@app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"], include_in_schema=False)
def unknown_api(path: str):
    raise HTTPException(404, "Endpoint não encontrado.")


# Na Vercel, public/ é servido pela CDN. Localmente, Uvicorn serve a mesma pasta.
if os.getenv("VERCEL") != "1":
    app.mount("/", StaticFiles(directory=Path(__file__).resolve().parents[1] / "public", html=True), name="frontend")
```


### Arquivo: pyproject.toml

```toml
[project]
name = "dessik"
version = "1.0.0"
requires-python = ">=3.12,<3.15"

[tool.vercel]
entrypoint = "api.index:app"

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
markers = ["integration: requer MySQL de teste isolado"]
```


### Arquivo: vercel.json

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": "fastapi",
  "functions": {
    "api/index.py": {
      "maxDuration": 30,
      "excludeFiles": "{tests/**,docs/**,.local/**,.venv/**}"
    }
  },
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "Referrer-Policy",
          "value": "strict-origin-when-cross-origin"
        }
      ]
    },
    {
      "source": "/:page*.html",
      "headers": [
        {
          "key": "Content-Security-Policy",
          "value": "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' https:; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'self'"
        }
      ]
    },
    {
      "source": "/",
      "headers": [
        {
          "key": "Content-Security-Policy",
          "value": "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' https:; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'self'"
        }
      ]
    },
    {
      "source": "/api/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "no-store"
        }
      ]
    }
  ]
}
```

## ETAPA 10 — Testes

Inicie o servidor e acesse `/api/docs`. Execute o login, copie `access_token`, clique em **Authorize** e cole somente o token. O Swagger envia o cabeçalho Bearer automaticamente.

### Cadastro — POST /api/cadastro

```json
{
  "nome": "João Silva",
  "email": "joao@example.com",
  "senha": "Senha123!",
  "confirmar_senha": "Senha123!",
  "cep": "01001000",
  "logradouro": "Praça da Sé",
  "bairro": "Sé",
  "cidade": "São Paulo",
  "estado": "SP"
}
```

As senhas acima são exemplos de teste. Em uma conta de uso real, use o gerador. Repetir o e-mail deve retornar 409; senha divergente, campo faltando ou tentativa de enviar `is_admin` deve retornar 422.

### Login — POST /api/login

```json
{"email": "joao@example.com", "senha": "Senha123!"}
```

Espera-se `access_token` e `token_type: "bearer"`. Senha incorreta deve retornar 401. `GET /api/me` com o token deve mostrar `is_admin: false` inicialmente.

### Criar produto — POST /api/produtos

Após promover a conta pelo comando da etapa 11:

```json
{
  "nome": "Mouse de teste",
  "descricao": "Mouse para testar o CRUD.",
  "categoria": "Periféricos",
  "preco": "99.90",
  "quantidade_estoque": 10,
  "imagem_url": "/images/placeholder.svg"
}
```

Anote o `id_produto` retornado. Use `GET /api/produtos/{id}` para consultar. Use `PUT /api/produtos/{id}` com o mesmo JSON e preço `"89.90"` para alterar. PUT exige todos os campos. Para excluir, use DELETE no ID antes de fazer pedidos. Um cliente comum recebe 403 em todas as mutações.

### Fazer pedido — POST /api/pedidos

```json
{"itens": [{"id_produto": 2, "quantidade": 3}]}
```

Troque `2` pelo ID desejado. A resposta 201 traz `id_pedido`, `valor_total` e mensagem de simulação. Se havia 10 unidades, ficam 7. Verifique em `GET /api/produtos/{id}`. Quantidade 0, negativa, fracionária ou item duplicado gera 422. Acima do estoque gera 409. Sem token gera 401. `GET /api/pedidos` lista somente os pedidos da conta autenticada.

### Testes automatizados

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Testes unitários e HTTP não precisam de banco. Os testes de integração são pulados se não houver autorização explícita pela variável abaixo. Para executá-los, crie **outro banco**, chamado `dessik_test`, configure as variáveis DB para ele e inicialize suas tabelas:

```powershell
$env:DB_NAME = "dessik_test"
# Configure também DB_HOST, DB_PORT, DB_USER, DB_PASSWORD e DB_SSL para o banco de teste.
python -m scripts.init_db
$env:RUN_MYSQL_TESTS = "1"
python -m pytest -q
Remove-Item Env:RUN_MYSQL_TESTS
Remove-Item Env:DB_NAME
```

O banco de teste deve terminar em `_test`. Os testes criam contas e produtos exclusivos e preservam os dados para inspeção; não use o banco real da loja. A integração verifica cadastro, duplicidade, login, hash, CRUD, FK, SQL injection como dado, rollback de pedido inválido e disputa de duas compras pela última unidade.



### Arquivo: tests/conftest.py

```python
import os
import secrets

import pytest
from fastapi.testclient import TestClient

# Os testes não carregam credenciais reais nem sobrescrevem o .env do usuário.
os.environ.setdefault("JWT_SECRET", secrets.token_urlsafe(48))
os.environ.setdefault("DB_HOST", "127.0.0.1")
os.environ.setdefault("DB_USER", "dessik_test")
os.environ.setdefault("DB_NAME", "dessik_test")
os.environ.setdefault("DB_SSL", "false")

from api.index import app
from backend.config import settings


@pytest.fixture
def client():
    settings.cache_clear()
    with TestClient(app) as client:
        yield client
    settings.cache_clear()
```


### Arquivo: tests/test_cep.py

```python
import httpx
import pytest


def test_invalid_cep(client):
    assert client.get('/api/cep/123').status_code == 422


@pytest.mark.parametrize('payload,status,expected', [
    ({'cep': '01001-000', 'logradouro': 'Praça da Sé', 'bairro': 'Sé', 'localidade': 'São Paulo', 'uf': 'SP'}, 200, 200),
    ({'erro': True}, 200, 404),
    ({}, 500, 502),
    ([], 200, 502),
])
def test_viacep_responses(client, monkeypatch, payload, status, expected):
    def get(self, url):
        assert url == 'https://viacep.com.br/ws/01001000/json/'
        return httpx.Response(status, json=payload, request=httpx.Request('GET', url))
    monkeypatch.setattr(httpx.Client, 'get', get)
    # TestClient também herda httpx.Client; chamamos request para não interceptar o teste.
    response = client.request('GET', '/api/cep/01001000')
    assert response.status_code == expected
    if expected == 200:
        assert response.json()['cidade'] == 'São Paulo'


def test_viacep_timeout(client, monkeypatch):
    def get(self, url):
        raise httpx.ReadTimeout('timeout')
    monkeypatch.setattr(httpx.Client, 'get', get)
    assert client.request('GET', '/api/cep/01001000').status_code == 502
```


### Arquivo: tests/test_frontend.py

```python
from html.parser import HTMLParser
from pathlib import Path

PUBLIC = Path(__file__).resolve().parents[1] / 'public'


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = []
    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if 'id' in attributes:
            self.ids.append(attributes['id'])
        for key in ('src', 'href'):
            if attributes.get(key, '').startswith('/'):
                self.links.append(attributes[key].split('?')[0])


def test_pages_have_resolvable_assets_and_unique_ids():
    for path in PUBLIC.glob('*.html'):
        page = Page()
        source = path.read_text(encoding='utf-8')
        page.feed(source)
        assert 'lang="pt-BR"' in source
        assert len(page.ids) == len(set(page.ids)), path
        for link in page.links:
            assert (PUBLIC / link.lstrip('/')).is_file(), (path, link)


def test_catalog_is_not_hardcoded():
    for name in ('index.html', 'loja.html'):
        source = (PUBLIC / name).read_text(encoding='utf-8')
        assert 'Notebook Horizon' not in source
        assert 'id="products"' in source
    script = (PUBLIC / 'js' / 'loja.js').read_text(encoding='utf-8')
    assert 'apiRequest(`/produtos' in script
```


### Arquivo: tests/test_mysql.py

```python
"""Integração real, sem SQLite. Cria dados novos e não remove tabelas existentes."""
import os
import uuid
from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi.testclient import TestClient

from api.index import app
from backend.database import transaction
from backend.security import verify_password

pytestmark = [pytest.mark.integration,
              pytest.mark.skipif(os.getenv('RUN_MYSQL_TESTS') != '1', reason='Configure um MySQL isolado e RUN_MYSQL_TESTS=1.')]


@pytest.fixture
def account(client):
    assert os.environ['DB_NAME'].endswith('_test'), 'Por segurança, use um banco terminado em _test.'
    email = f'{uuid.uuid4().hex}@example.com'
    body = {'nome': 'Cliente teste', 'email': email, 'senha': 'Teste123!', 'confirmar_senha': 'Teste123!'}
    registered = client.post('/api/cadastro', json=body)
    assert registered.status_code == 201
    assert client.post('/api/cadastro', json=body).status_code == 409
    assert client.post('/api/login', json={'email': email, 'senha': 'wrong'}).status_code == 401
    login = client.post('/api/login', json={'email': email, 'senha': body['senha']})
    assert login.status_code == 200
    headers = {'Authorization': f"Bearer {login.json()['access_token']}"}
    user_id = registered.json()['id_usuario']
    with transaction() as cursor:
        cursor.execute('SELECT senha_hash, is_admin FROM usuarios WHERE id_usuario=%s', (user_id,))
        stored = cursor.fetchone()
    assert verify_password(body['senha'], stored['senha_hash'])
    assert stored['is_admin'] == 0
    return user_id, headers


def create_product(client, account, stock=3):
    user_id, headers = account
    with transaction() as cursor:
        cursor.execute('UPDATE usuarios SET is_admin=TRUE WHERE id_usuario=%s', (user_id,))
    body = {'nome': 'Produto teste', 'descricao': 'Produto de teste isolado', 'categoria': 'Teste',
            'preco': '12.90', 'quantidade_estoque': stock, 'imagem_url': '/images/placeholder.svg'}
    response = client.post('/api/produtos', json=body, headers=headers)
    assert response.status_code == 201, response.text
    return response.json()['id_produto'], body


def test_full_crud(client, account):
    _, headers = account
    assert client.delete('/api/produtos/1', headers=headers).status_code == 403
    product_id, body = create_product(client, account)
    assert client.get(f'/api/produtos/{product_id}').json()['preco'] == '12.90'
    assert client.put(f'/api/produtos/{product_id}', json=body | {'preco': '19.90'}, headers=headers).status_code == 200
    assert client.delete(f'/api/produtos/{product_id}', headers=headers).status_code == 200
    assert client.get(f'/api/produtos/{product_id}').status_code == 404


def test_order_and_rollback(client, account):
    _, headers = account
    product_id, _ = create_product(client, account, stock=3)
    other_id, _ = create_product(client, account, stock=0)
    failed = client.post('/api/pedidos', headers=headers, json={'itens': [
        {'id_produto': product_id, 'quantidade': 1}, {'id_produto': other_id, 'quantidade': 1}]})
    assert failed.status_code == 409
    assert client.get(f'/api/produtos/{product_id}').json()['quantidade_estoque'] == 3
    assert client.get('/api/pedidos', headers=headers).json() == []
    success = client.post('/api/pedidos', headers=headers, json={'itens': [{'id_produto': product_id, 'quantidade': 2}]})
    assert success.status_code == 201
    assert success.json()['valor_total'] == '25.80'
    assert client.get(f'/api/produtos/{product_id}').json()['quantidade_estoque'] == 1
    assert client.delete(f'/api/produtos/{product_id}', headers=headers).status_code == 409
    assert len(client.get('/api/pedidos', headers=headers).json()) == 1


def test_concurrent_purchase_never_oversells(client, account):
    _, headers = account
    product_id, _ = create_product(client, account, stock=1)
    def buy():
        with TestClient(app) as buyer:
            return buyer.post('/api/pedidos', headers=headers,
                              json={'itens': [{'id_produto': product_id, 'quantidade': 1}]}).status_code
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda _: buy(), range(2)))
    assert sorted(results) == [201, 409]
    assert client.get(f'/api/produtos/{product_id}').json()['quantidade_estoque'] == 0


def test_sql_injection_is_data(client, account):
    product_id, body = create_product(client, account)
    _, headers = account
    name = "Mouse'); DROP TABLE produtos; --"
    assert client.put(f'/api/produtos/{product_id}', json=body | {'nome': name}, headers=headers).status_code == 200
    assert client.get(f'/api/produtos/{product_id}').json()['nome'] == name
    assert client.get('/api/produtos').status_code == 200
```


### Arquivo: tests/test_security.py

```python
from datetime import datetime, timedelta, timezone
import string

import jwt
import pytest
from mysql.connector import DatabaseError
from pydantic import ValidationError

from backend.config import settings
from backend.schemas import Cadastro, Pedido, Produto
from backend.security import create_token, decode_token, hash_password, verify_password
from backend.services.password_generator import generate_password


def test_hash_salt_and_verification():
    password = generate_password()
    first, second = hash_password(password), hash_password(password)
    assert first != second and first != password
    assert verify_password(password, first)
    assert not verify_password(password + '!', first)


def test_password_generator():
    passwords = {generate_password() for _ in range(100)}
    assert len(passwords) == 100
    for password in passwords:
        assert len(password) == 16
        for group in (string.ascii_lowercase, string.ascii_uppercase, string.digits, '!@#$%&*+-=?'):
            assert any(char in group for char in password)


def test_jwt_signature_expiration():
    token = create_token(1)
    assert decode_token(token)['sub'] == '1'
    with pytest.raises(jwt.InvalidTokenError):
        decode_token(token + 'corrupted')
    now = datetime.now(timezone.utc)
    expired = jwt.encode({'sub': '1', 'iat': now - timedelta(hours=2),
                          'exp': now - timedelta(hours=1), 'iss': 'dessik', 'aud': 'dessik-web'},
                         settings()['secret'], algorithm='HS256')
    with pytest.raises(jwt.ExpiredSignatureError):
        decode_token(expired)


@pytest.mark.parametrize('changes', [
    {'nome': '  '}, {'email': 'invalid'}, {'senha': 'short'},
    {'confirmar_senha': 'Different123!'}, {'senha': 'á' * 40, 'confirmar_senha': 'á' * 40},
    {'is_admin': True}, {'cep': '123'}, {'estado': 'ZZ'},
])
def test_invalid_registration(changes):
    data = {'nome': 'João Silva', 'email': 'joao@example.com', 'senha': 'Senha123!', 'confirmar_senha': 'Senha123!'}
    with pytest.raises(ValidationError):
        Cadastro(**(data | changes))


@pytest.mark.parametrize('quantity', [0, -1, 1.5, True, 1001])
def test_invalid_order_quantities(quantity):
    with pytest.raises(ValidationError):
        Pedido(itens=[{'id_produto': 1, 'quantidade': quantity}])


def test_duplicate_order_items():
    with pytest.raises(ValidationError):
        Pedido(itens=[{'id_produto': 1, 'quantidade': 1}] * 2)


@pytest.mark.parametrize('url', ['javascript:alert(1)', '//evil.com/image.png', '/images/../../.env', 'http://example.com/image.png'])
def test_unsafe_image_url(url):
    with pytest.raises(ValidationError):
        Produto(nome='Mouse', descricao='Mouse gamer', categoria='Mouse', preco='12.90', quantidade_estoque=1, imagem_url=url)


def test_api_validation_does_not_leak_password(client):
    response = client.post('/api/cadastro', json={'nome': '', 'email': 'x', 'senha': 'SUPER-SECRET'})
    assert response.status_code == 422
    assert 'SUPER-SECRET' not in response.text


def test_auth_guards(client):
    assert client.post('/api/pedidos', json={'itens': [{'id_produto': 1, 'quantidade': 1}]}).status_code == 401
    assert client.get('/api/me', headers={'Authorization': 'Bearer invalid'}).status_code == 401


def test_admin_guard(client):
    from api.index import app
    from backend.auth import current_user
    app.dependency_overrides[current_user] = lambda: {'id_usuario': 1, 'is_admin': False}
    try:
        assert client.delete('/api/produtos/1').status_code == 403
    finally:
        app.dependency_overrides.clear()


def test_database_unavailable(client, monkeypatch):
    def unavailable():
        raise DatabaseError('private database details', errno=2003)
    monkeypatch.setattr('backend.database.connect', unavailable)
    response = client.get('/api/produtos')
    assert response.status_code == 503
    assert 'private' not in response.text


def test_static_and_api_routes(client):
    for path in ['/', '/loja.html', '/login.html', '/cadastro.html', '/admin.html', '/css/style.css', '/js/api.js', '/images/placeholder.svg']:
        assert client.get(path).status_code == 200
    assert client.get('/api/health').json() == {'status': 'ok'}
    assert client.get('/api/unknown').status_code == 404
    assert client.get('/api/gerar-senha').headers['cache-control'] == 'no-store'
    assert client.get('/.env').status_code == 404


def test_production_requires_tls(monkeypatch):
    monkeypatch.setenv('APP_ENV', 'production')
    monkeypatch.setenv('DB_SSL', 'false')
    settings.cache_clear()
    with pytest.raises(RuntimeError):
        settings()
    settings.cache_clear()
```

## ETAPA 11 — Executar localmente, do início

1. Instale Python 3.13 em [python.org](https://www.python.org/downloads/) e habilite o acesso pelo terminal. Verifique `python --version`.
2. Instale MySQL Server 8.0.16+ ou use banco remoto compatível. **Workbench é um cliente e não substitui o servidor.** Crie o banco conforme a etapa 3. Reserve um usuário da aplicação, evitando usar root na produção.
3. Baixe/clône este repositório ou abra esta pasta no VS Code. Abra o terminal **na raiz do projeto**, onde está `requirements.txt`.
4. Crie e ative o ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Se a política do PowerShell impedir ativar, não precisa alterá-la: substitua `python` por `.\.venv\Scripts\python.exe` nos comandos seguintes. No Prompt de Comando, use `.venv\Scripts\activate.bat`. No Linux/macOS, use `source .venv/bin/activate`.

5. Instale as dependências e crie `.env`:

```powershell
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

No Linux/macOS: `cp .env.example .env`. Se `.env` já existe, edite-o; não sobrescreva suas credenciais.

6. Preencha `.env` com o banco. Localmente, `DB_HOST=127.0.0.1`, porta configurada e `DB_SSL=false` são permitidos com `APP_ENV=development`. No banco remoto use o host real, a porta do provedor e `DB_SSL=true`. Gere `JWT_SECRET` com o comando da etapa 7.
7. Execute o SQL no Workbench, com o banco selecionado, ou use:

```bash
python -m scripts.init_db
```

8. Inicie a aplicação:

```bash
python -m uvicorn api.index:app --reload
```

9. Abra [a loja local](http://127.0.0.1:8000/loja.html). A documentação interativa está em [Swagger](http://127.0.0.1:8000/api/docs).
10. Clique em Criar conta. Teste Sugerir senha e Consultar CEP. Guarde a senha e conclua o cadastro.
11. Faça login. Consulte produtos, escolha quantidade e confirme uma compra. Confira a redução do estoque.
12. Para administrar, abra outro terminal com o mesmo ambiente, na raiz, e promova **a conta que você acabou de cadastrar**:

```bash
python -m scripts.admin joao@example.com
```

13. Atualize a loja e abra Administração no menu. Cadastre, edite e exclua um produto de teste. Não há endpoint público de promoção: o comando depende de acesso autorizado ao banco.
14. Confira os testes da etapa 10. Para encerrar o servidor, use `Ctrl+C`.



### Arquivo: scripts/__init__.py

```python
"""Utilitários executados explicitamente pelo responsável pelo banco."""
```


### Arquivo: scripts/init_db.py

```python
"""Cria tabelas e insere a massa inicial em um banco previamente criado."""
from pathlib import Path

from backend.database import transaction


def execute_file(cursor, path):
    # Estes arquivos controlados pelo projeto não contêm procedures nem ';' em strings.
    sql = "\n".join(line for line in path.read_text(encoding="utf-8").splitlines()
                    if not line.lstrip().startswith("--"))
    for statement in sql.split(";"):
        if statement.strip():
            cursor.execute(statement)


def main():
    folder = Path(__file__).resolve().parents[1] / "database"
    with transaction() as cursor:
        execute_file(cursor, folder / "schema.sql")
        execute_file(cursor, folder / "dados.sql")
    print("Tabelas e produtos iniciais preparados. Nenhuma conta padrão foi criada.")


if __name__ == "__main__":
    main()
```


### Arquivo: scripts/admin.py

```python
"""Promove uma conta existente: python -m scripts.admin email@exemplo.com"""
import argparse

from backend.database import transaction


def main():
    parser = argparse.ArgumentParser(description="Conceder acesso administrativo a uma conta existente.")
    parser.add_argument("email")
    args = parser.parse_args()
    with transaction() as cursor:
        cursor.execute("SELECT id_usuario FROM usuarios WHERE email = %s", (args.email.lower(),))
        user = cursor.fetchone()
        if not user:
            raise SystemExit("Conta não encontrada. Cadastre-se primeiro na loja.")
        cursor.execute("UPDATE usuarios SET is_admin = TRUE WHERE id_usuario = %s", (user["id_usuario"],))
    print("Conta promovida a administrador.")


if __name__ == "__main__":
    main()
```


### Arquivo: scripts/export_guide.py

```python
"""Gera a entrega em 14 etapas com o conteúdo integral dos arquivos do projeto."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def files_for_stage(stage):
    mapping = {
        3: ["database/schema.sql", "database/dados.sql"],
        4: ["backend/__init__.py", "backend/config.py", "backend/database.py", "backend/schemas.py",
            "backend/security.py", "backend/auth.py", "backend/services/__init__.py",
            "backend/services/password_generator.py"],
        5: ["backend/routes/__init__.py", "backend/routes/usuarios.py", "backend/routes/produtos.py",
            "backend/routes/pedidos.py", "backend/routes/cep.py"],
        6: [str(path.relative_to(ROOT)).replace("\\", "/") for path in sorted((ROOT / "public").rglob("*")) if path.is_file()],
        7: [".env.example", ".gitignore", ".vercelignore"],
        8: ["requirements.txt", "requirements-dev.txt", "requirements-lock.txt"],
        9: ["api/__init__.py", "api/index.py", "pyproject.toml", "vercel.json"],
        10: [str(path.relative_to(ROOT)).replace("\\", "/") for path in sorted((ROOT / "tests").glob("*.py"))],
        11: ["scripts/__init__.py", "scripts/init_db.py", "scripts/admin.py", "scripts/export_guide.py"],
    }
    return mapping.get(stage, [])


def main():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    sections = re.split(r"(?=^## ETAPA \d+)", readme, flags=re.MULTILINE)
    output = ["# Dessik — projeto completo em 14 etapas\n\n"
              "Entrega com tutorial e arquivos integrais. Os mesmos arquivos estão no repositório. "
              "Gerado por `python -m scripts.export_guide`. Nenhum segredo real é incluído.\n"]
    languages = {".py": "python", ".js": "javascript", ".html": "html", ".css": "css",
                 ".sql": "sql", ".json": "json", ".toml": "toml", ".svg": "xml"}
    for section in sections[1:]:
        number = int(re.match(r"## ETAPA (\d+)", section).group(1))
        # Corrige links relativos do README porque este documento fica em docs/.
        section = re.sub(r"\]\((?!https?://)([^)]+)\)", r"](../\1)", section)
        output.append(section)
        for filename in files_for_stage(number):
            path = ROOT / filename
            language = languages.get(path.suffix, "text")
            if path.suffix in {".png", ".jpg", ".jpeg", ".webp"}:
                output.append(f"\n### Arquivo: {filename}\n\nAsset de imagem: [{path.name}](../{filename}). Copie o arquivo binário junto com o projeto.\n")
                continue
            output.append(f"\n### Arquivo: {filename}\n\n```{language}\n{path.read_text(encoding='utf-8').rstrip()}\n```\n")
    destination = ROOT / "docs" / "PROJETO_COMPLETO.md"
    destination.parent.mkdir(exist_ok=True)
    destination.write_text("\n".join(output), encoding="utf-8")
    print(f"Documento completo gerado: {destination.name}")


if __name__ == "__main__":
    main()
```

## ETAPA 12 — Banco na nuvem e serverless

Escolha um serviço **MySQL compatível**, por exemplo TiDB Cloud Starter. A [página oficial de preços](https://www.pingcap.com/pricing/) e a [página do Starter](https://www.pingcap.com/tidb-cloud-starter/) apresentavam uma opção gratuita em 08/09/2026. Verifique os limites, regiões e exigências de conta no momento da contratação; não se promete gratuidade permanente. Não foram presumidos planos atuais de Clever Cloud, FreeDB ou db4free.

No painel do serviço, crie uma instância e copie host, porta, usuário, senha e nome do banco para o `.env` e, depois, para a Vercel. Utilize o endereço público ou a conectividade suportada pelo provedor e autorize somente o acesso necessário. A Vercel não consegue acessar o MySQL do seu computador por `localhost`.

No TiDB, use as instruções de conexão geradas pelo próprio painel e mantenha TLS ativo. Veja a [documentação de TLS do TiDB Cloud](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters/). A aplicação verifica tanto a cadeia de certificados quanto o hostname. Se a CA estiver na confiança do sistema, `DB_SSL_CA` pode ficar vazio; se o provedor exigir uma CA própria, configure seu arquivo PEM. Não desative a verificação para contornar erros.

Se precisar de CA própria na Vercel, inclua **somente o certificado público CA** em uma pasta versionada, como `database/ca.pem`, e configure `DB_SSL_CA=database/ca.pem`. Nunca inclua chaves privadas. A pasta `certs/` é ignorada por padrão e serve apenas para uso local.

O DDL foi direcionado a InnoDB/MySQL. Serviços compatíveis podem ter diferenças de versão no suporte/enforcement de CHECK e FKs; habilite o suporte quando necessário, confira a documentação da versão e execute os testes de integração antes de usar o serviço. A validação e a atualização condicional no servidor protegem o estoque além das restrições do schema.

Serverless significa que várias execuções podem começar simultaneamente. Cada transação abre uma conexão curta e a fecha ao terminar; não existe conexão global permanente. Ainda assim, muitas requisições simultâneas podem atingir o limite de conexões do plano. Ajuste concorrência e limites no provedor, monitore os erros e considere proxy/pool gerenciado se o projeto crescer.

O cold start pode aumentar a latência da primeira chamada. As funções têm limites de duração, memória e tamanho; não mantenha tarefas longas, estado importante ou arquivos mutáveis no disco da função. O MySQL remoto é a fonte persistente dos dados.


## ETAPA 13 — Deploy na Vercel

1. Crie um repositório no GitHub e envie estes arquivos. Use GitHub Desktop ou Git. `.env`, `.venv` e `.local` devem ficar fora do commit. Se já publicou um segredo, removê-lo do arquivo não basta: troque a credencial.
2. Crie/configure o banco remoto e execute `schema.sql` e `dados.sql` nele. Não execute seed automático em todo deploy.
3. Na Vercel, escolha **Add New → Project** e importe o repositório. Selecione a raiz do projeto e o preset FastAPI, se não for detectado.
4. Deixe instalação/build/output nos padrões do preset, respeitando os arquivos deste repositório. Não selecione `public` como raiz do projeto, pois isso excluiria o backend.
5. Em **Settings → Environment Variables**, adicione **individualmente** `APP_ENV=production`, `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_SSL=true`, `JWT_SECRET`, `JWT_ALGORITHM=HS256`, `ACCESS_TOKEN_EXPIRE_MINUTES=60`. Adicione `DB_SSL_CA` apenas se necessário. Deixe `CORS_ORIGINS` vazio para a mesma origem.
6. Selecione os ambientes desejados (Production e, se for testar previews, Preview). Prefira bancos separados para produção e preview. Não copie o `.env` para `public/`.
7. Clique em **Deploy**. Se mudar variáveis depois, faça um novo deploy para aplicá-las.
8. Abra `/api/health`, `/api/produtos`, `/loja.html`, `/cadastro.html` e `/login.html`. O health valida que a função respondeu; produtos confirma a conexão real com o banco.
9. Cadastre uma conta de teste e faça uma compra. Promova a conta necessária via `python -m scripts.admin seu@email.com` em um ambiente autorizado conectado ao banco remoto. Teste CRUD e restrições com outra conta comum.
10. Em falhas, consulte Build Logs e Runtime Logs no painel. Não cole senhas ou tokens em capturas públicas.

| Sintoma | Verificação |
|---|---|
| Configuração JWT inválida | Chave preenchida, algoritmo HS256 e novo deploy |
| HTTP 503 em produtos | Host, porta, usuário, senha, DB_NAME, rede e TLS |
| Tabela inexistente | Execute os dois scripts SQL no banco correto |
| Erro de certificado | CA correta e hostname do certificado; não desative TLS |
| HTTP 401 | Faça login novamente e envie Bearer válido |
| HTTP 403 | Confira `is_admin` pelo comando de promoção |
| HTTP 409 ao excluir | Produto já aparece em pedido; mantenha o histórico |
| 404 na raiz | Confira preset FastAPI, raiz do repositório e pasta public |
| CEP não preenche | Verifique formato e conectividade com ViaCEP; preencha manualmente |

O projeto entrega a configuração e o tutorial de deploy. A publicação real exige a sua conta Vercel e credenciais de um banco remoto; esses recursos não são criados nem inventados pelo código.


## ETAPA 14 — Explicação para apresentação

“Este projeto é uma loja fictícia de tecnologia. A interface é feita com HTML e CSS, e o JavaScript usa `fetch` para enviar requisições à API em Python.

API REST é um conjunto de endereços que permite trabalhar com recursos. GET consulta, POST cria, PUT atualiza e DELETE exclui. JSON é o formato usado para transportar os campos, como nome e quantidade.

O FastAPI recebe esses dados e valida o conteúdo antes de executar a regra. Depois, o conector MySQL executa consultas parametrizadas. Assim, a entrada do usuário é tratada como dado e não como comando SQL.

No cadastro, a senha passa pelo bcrypt, que gera um hash com salt. O banco guarda esse hash, não a senha. No login, o bcrypt verifica se a senha digitada corresponde ao hash. Se corresponder, a API emite um JWT assinado e com prazo de validade.

O navegador guarda esse token temporariamente e o envia no cabeçalho Authorization. A API valida o token e consulta a conta. Para cadastrar, editar ou excluir produtos, ela também verifica se a conta é administradora.

O catálogo vem do banco. Na compra simulada, o servidor verifica e bloqueia os produtos, registra o pedido e seus itens e reduz o estoque numa transação. Se uma parte falhar, tudo é desfeito. Isso impede pedido pela metade e evita vender a mesma última unidade duas vezes.

O CEP demonstra a integração entre sistemas: o navegador chama nossa API, nossa API consulta o ViaCEP e o endereço volta em JSON para preencher o formulário.

Na publicação, a Vercel entrega as páginas e executa o Python. O banco fica em outro serviço acessível com TLS. Assim, a aplicação pode reiniciar sem perder os dados. Não há cobrança real: o objetivo é demonstrar a comunicação completa entre interface, API e banco.”
