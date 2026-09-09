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
