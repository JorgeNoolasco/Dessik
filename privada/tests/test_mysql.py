"""Integração real, sem SQLite. Cria dados novos e não remove tabelas existentes."""
import os
import uuid
from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi.testclient import TestClient

from api.index import app
from backend.database import transaction
from backend.auth import verify_password

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
        cursor.execute('SELECT senha_hash, tipo_usuario FROM usuarios WHERE id_usuario=%s', (user_id,))
        stored = cursor.fetchone()
    assert verify_password(body['senha'], stored['senha_hash'])
    assert stored['tipo_usuario'] == 'cliente'
    return user_id, headers


def create_product(client, account, stock=3):
    user_id, headers = account
    with transaction() as cursor:
        cursor.execute("UPDATE usuarios SET tipo_usuario='admin' WHERE id_usuario=%s", (user_id,))
    body = {'nome': 'Produto teste', 'descricao': 'Produto de teste isolado', 'categoria': 'Teste',
            'preco': '12.90', 'quantidade_estoque': stock, 'imagem_url': '/imagens/placeholder.svg'}
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


def test_cart_multiple_products_and_price_tampering(client, account):
    _, headers = account
    first, _ = create_product(client, account, stock=4)
    second, _ = create_product(client, account, stock=3)
    forged = client.post('/api/pedidos', headers=headers, json={'itens': [
        {'id_produto': first, 'quantidade': 2, 'preco': '0.01'}]})
    assert forged.status_code == 422
    assert client.get(f'/api/produtos/{first}').json()['quantidade_estoque'] == 4
    order = client.post('/api/pedidos', headers=headers, json={'itens': [
        {'id_produto': first, 'quantidade': 2}, {'id_produto': second, 'quantidade': 1}]})
    assert order.status_code == 201
    assert order.json()['valor_total'] == '38.70'
    assert client.get(f'/api/produtos/{first}').json()['quantidade_estoque'] == 2
    assert client.get(f'/api/produtos/{second}').json()['quantidade_estoque'] == 2


def test_sql_injection_is_data(client, account):
    product_id, body = create_product(client, account)
    _, headers = account
    name = "Mouse'); DROP TABLE produtos; --"
    assert client.put(f'/api/produtos/{product_id}', json=body | {'nome': name}, headers=headers).status_code == 200
    assert client.get(f'/api/produtos/{product_id}').json()['nome'] == name
    assert client.get('/api/produtos').status_code == 200
