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
