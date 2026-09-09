"""Promove uma conta existente: python -m scripts.admin email@exemplo.com"""
import argparse

from backend.database import transaction


def main():
    parser = argparse.ArgumentParser(description="Conceder acesso administrativo a uma conta existente.")
    parser.add_argument("email")
    args = parser.parse_args()
    with transaction() as cursor:
        cursor.execute("SELECT id_usuario FROM usuarios WHERE email = %s", (args.email.lower(),))
        user = cursor.fetchone()
        if not user:
            raise SystemExit("Conta não encontrada. Cadastre-se primeiro na loja.")
        cursor.execute("UPDATE usuarios SET is_admin = TRUE WHERE id_usuario = %s", (user["id_usuario"],))
    print("Conta promovida a administrador.")


if __name__ == "__main__":
    main()
