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
