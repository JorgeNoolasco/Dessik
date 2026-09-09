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
from backend.database import settings, transaction
import re
import httpx
from decimal import Decimal
from typing import Literal
from fastapi import Depends, Query
from mysql.connector import IntegrityError
from backend.auth import current_user, admin_user, create_token, hash_password, verify_password, generate_password
from backend.schemas import Cadastro, Login, Produto, Pedido
from backend.models import serialize_product


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


# USUARIOS
# Hash válido apenas para equalizar o custo do login de um e-mail inexistente.
DUMMY_HASH = hash_password(generate_password())


@app.post("/api/cadastro", status_code=201)
def cadastro(data: Cadastro):
    hashed = hash_password(data.senha)
    try:
        with transaction() as cursor:
            # Query parametrizada: valores separados do SQL evitam SQL Injection.
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


@app.post("/api/login")
def login(data: Login):
    with transaction() as cursor:
        cursor.execute("SELECT id_usuario, senha_hash FROM usuarios WHERE email = %s", (str(data.email),))
        user = cursor.fetchone()
    valid = verify_password(data.senha, user["senha_hash"] if user else DUMMY_HASH)
    if not user or not valid:
        raise HTTPException(401, "E-mail ou senha incorretos.", headers={"WWW-Authenticate": "Bearer"})
    return {"access_token": create_token(user["id_usuario"]), "token_type": "bearer"}


@app.get("/api/me")
def me(user=Depends(current_user)):
    return user


@app.get("/api/gerar-senha")
def password():
    return {"senha": generate_password()}


# PRODUTOS
@app.get("/api/produtos")
def list_products(limite: int = Query(100, ge=1, le=100), offset: int = Query(0, ge=0),
                  busca: str = Query('', max_length=100), categoria: str = Query('', max_length=60),
                  ordem: Literal['recentes', 'menor-preco', 'maior-preco'] = 'recentes'):
    # Apenas expressões constantes entram no ORDER BY. Texto do usuário é parametrizado.
    sorting = {'recentes': 'id_produto ASC', 'menor-preco': 'preco ASC, id_produto ASC',
               'maior-preco': 'preco DESC, id_produto ASC'}[ordem]
    with transaction() as cursor:
        cursor.execute("""SELECT * FROM produtos
            WHERE (%s = '' OR LOCATE(%s, CONCAT(nome, ' ', descricao)) > 0)
              AND (%s = '' OR categoria = %s)
            ORDER BY """ + sorting + " LIMIT %s OFFSET %s",
                       (busca.strip(), busca.strip(), categoria, categoria, limite, offset))
        return [serialize_product(p) for p in cursor.fetchall()]


@app.get("/api/produtos/{product_id}")
def get_product(product_id: int):
    with transaction() as cursor:
        cursor.execute("SELECT * FROM produtos WHERE id_produto = %s", (product_id,))
        product = cursor.fetchone()
    if not product:
        raise HTTPException(404, "Produto não encontrado.")
    return serialize_product(product)


@app.post("/api/produtos", status_code=201)
def create_product(data: Produto, user=Depends(admin_user)):
    with transaction() as cursor:
        cursor.execute("""INSERT INTO produtos
            (nome, descricao, categoria, preco, quantidade_estoque, imagem_url)
            VALUES (%s, %s, %s, %s, %s, %s)""", tuple(data.model_dump().values()))
        product_id = cursor.lastrowid
    return {"mensagem": "Produto cadastrado.", "id_produto": product_id}


@app.put("/api/produtos/{product_id}")
def update_product(product_id: int, data: Produto, user=Depends(admin_user)):
    with transaction() as cursor:
        cursor.execute("SELECT id_produto FROM produtos WHERE id_produto = %s FOR UPDATE", (product_id,))
        if not cursor.fetchone():
            raise HTTPException(404, "Produto não encontrado.")
        cursor.execute("""UPDATE produtos SET nome=%s, descricao=%s, categoria=%s,
            preco=%s, quantidade_estoque=%s, imagem_url=%s WHERE id_produto=%s""",
                       (*data.model_dump().values(), product_id))
    return {"mensagem": "Produto atualizado."}


@app.delete("/api/produtos/{product_id}")
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


# PEDIDOS


@app.post("/api/pedidos", status_code=201)
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
            # O navegador envia apenas IDs e quantidades: preço e estoque vêm do banco.
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


@app.get("/api/pedidos")
def list_orders(user=Depends(current_user)):
    with transaction() as cursor:
        cursor.execute("""SELECT id_pedido, data_pedido, valor_total, status FROM pedidos
            WHERE id_usuario = %s ORDER BY id_pedido DESC LIMIT 100""", (user["id_usuario"],))
        orders = cursor.fetchall()
    for order in orders:
        order["valor_total"] = str(order["valor_total"])
    return orders


# CEP


@app.get("/api/cep/{cep}")
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


@app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"], include_in_schema=False)
def unknown_api(path: str):
    raise HTTPException(404, "Endpoint não encontrado.")


# Somente publico/ é servido. Nunca monte workspace/ ou privada/ como arquivos estáticos.
if os.getenv("VERCEL") != "1":
    app.mount("/", StaticFiles(directory=Path(__file__).resolve().parents[2] / "publico", html=True), name="frontend")
