import os
from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv
from contextlib import contextmanager
import mysql.connector


load_dotenv(Path(__file__).resolve().parents[1] / ".env")


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


"""Conexões curtas: cada operação libera cursor e conexão, inclusive com erro."""


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
