"""Cria tabelas e insere a massa inicial em um banco previamente criado."""
from pathlib import Path

from backend.database import transaction


def execute_file(cursor, path):
    # Estes arquivos controlados pelo projeto não contêm procedures nem ';' em strings.
    sql = "\n".join(line for line in path.read_text(encoding="utf-8").splitlines()
                    if not line.lstrip().startswith("--"))
    for statement in sql.split(";"):
        if statement.strip():
            cursor.execute(statement)


def main():
    folder = Path(__file__).resolve().parents[1] / "database"
    with transaction() as cursor:
        execute_file(cursor, folder / "schema.sql")
        execute_file(cursor, folder / "dados.sql")
    print("Tabelas e produtos iniciais preparados. Nenhuma conta padrão foi criada.")


if __name__ == "__main__":
    main()
