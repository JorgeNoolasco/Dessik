from fastapi import APIRouter, Depends, HTTPException
from mysql.connector import IntegrityError

from backend.auth import current_user
from backend.database import transaction
from backend.schemas import Cadastro, Login
from backend.security import create_token, hash_password, verify_password
from backend.services.password_generator import generate_password

router = APIRouter(tags=["Usuários"])
# Hash válido apenas para equalizar o custo do login de um e-mail inexistente.
DUMMY_HASH = hash_password(generate_password())


@router.post("/cadastro", status_code=201)
def cadastro(data: Cadastro):
    hashed = hash_password(data.senha)
    try:
        with transaction() as cursor:
            cursor.execute(
                """INSERT INTO usuarios
                (nome, email, senha_hash, cep, logradouro, bairro, cidade, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (data.nome, str(data.email), hashed, data.cep, data.logradouro,
                 data.bairro, data.cidade, data.estado))
            user_id = cursor.lastrowid
    except IntegrityError as error:
        if error.errno == 1062:
            raise HTTPException(409, "Este e-mail já está cadastrado.")
        raise
    return {"mensagem": "Conta criada. Você já pode entrar.", "id_usuario": user_id}


@router.post("/login")
def login(data: Login):
    with transaction() as cursor:
        cursor.execute("SELECT id_usuario, senha_hash FROM usuarios WHERE email = %s", (str(data.email),))
        user = cursor.fetchone()
    valid = verify_password(data.senha, user["senha_hash"] if user else DUMMY_HASH)
    if not user or not valid:
        raise HTTPException(401, "E-mail ou senha incorretos.", headers={"WWW-Authenticate": "Bearer"})
    return {"access_token": create_token(user["id_usuario"]), "token_type": "bearer"}


@router.get("/me")
def me(user=Depends(current_user)):
    return user


@router.get("/gerar-senha")
def password():
    return {"senha": generate_password()}
