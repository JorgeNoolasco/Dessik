from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from backend.config import settings


def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode()


def verify_password(password, hashed):
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode())
    except (ValueError, TypeError):
        return False


def create_token(user_id):
    now = datetime.now(timezone.utc)
    return jwt.encode({"sub": str(user_id), "iat": now,
                       "exp": now + timedelta(minutes=settings()["minutes"]),
                       "iss": "dessik", "aud": "dessik-web"},
                      settings()["secret"], algorithm="HS256")


def decode_token(token):
    return jwt.decode(token, settings()["secret"], algorithms=["HS256"],
                      issuer="dessik", audience="dessik-web",
                      options={"require": ["sub", "exp", "iat", "iss", "aud"]})
