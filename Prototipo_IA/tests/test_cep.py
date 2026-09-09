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
