from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError

from backend.database import transaction
from backend.security import decode_token

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
        cursor.execute("SELECT id_usuario, nome, email, is_admin FROM usuarios WHERE id_usuario = %s", (user_id,))
        user = cursor.fetchone()
    if not user:
        raise unauthorized
    user["is_admin"] = bool(user["is_admin"])
    return user


def admin_user(user=Depends(current_user)):
    # A permissão vem do banco em cada requisição, nunca de um botão ou do cliente.
    if not user["is_admin"]:
        raise HTTPException(403, "Esta operação exige um administrador.")
    return user
