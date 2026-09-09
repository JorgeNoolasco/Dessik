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
