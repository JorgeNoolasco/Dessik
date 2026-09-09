from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from backend.database import settings
import secrets
import string
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from backend.database import transaction


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


def generate_password(length=16):
    groups = (string.ascii_lowercase, string.ascii_uppercase, string.digits, "!@#$%&*+-=?")
    alphabet = "".join(groups)
    # Rejeição garante que todos os grupos apareçam, usando somente secrets.
    while True:
        password = "".join(secrets.choice(alphabet) for _ in range(length))
        if all(any(char in group for char in password) for group in groups):
            return password


bearer = HTTPBearer(auto_error=False)


def current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)):
    unauthorized = HTTPException(401, "Sessão inválida ou expirada. Entre novamente.",
                                 headers={"WWW-Authenticate": "Bearer"})
    if credentials is None:
        raise unauthorized
    try:
        user_id = int(decode_token(credentials.credentials)["sub"])
        if user_id <= 0:
            raise ValueError()
    except (InvalidTokenError, ValueError, TypeError, KeyError):
        raise unauthorized
    with transaction() as cursor:
        cursor.execute("SELECT id_usuario, nome, email, tipo_usuario FROM usuarios WHERE id_usuario = %s", (user_id,))
        user = cursor.fetchone()
    if not user:
        raise unauthorized
    user["is_admin"] = user["tipo_usuario"] == "admin"
    return user


def admin_user(user=Depends(current_user)):
    # A permissão vem do banco em cada requisição, nunca de um botão ou do cliente.
    if user["tipo_usuario"] != "admin":
        raise HTTPException(403, "Esta operação exige um administrador.")
    return user
