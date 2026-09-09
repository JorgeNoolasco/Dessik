import secrets
import string


def generate_password(length=16):
    groups = (string.ascii_lowercase, string.ascii_uppercase, string.digits, "!@#$%&*+-=?")
    alphabet = "".join(groups)
    # Rejeição garante que todos os grupos apareçam, usando somente secrets.
    while True:
        password = "".join(secrets.choice(alphabet) for _ in range(length))
        if all(any(char in group for char in password) for group in groups):
            return password
