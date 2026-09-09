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
from backend.database import settings


@pytest.fixture
def client():
    settings.cache_clear()
    with TestClient(app) as client:
        yield client
    settings.cache_clear()
