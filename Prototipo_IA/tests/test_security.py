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
