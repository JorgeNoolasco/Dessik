"""Gera a entrega em 14 etapas com o conteúdo integral dos arquivos do projeto."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def files_for_stage(stage):
    mapping = {
        3: ["database/schema.sql", "database/dados.sql"],
        4: ["backend/__init__.py", "backend/config.py", "backend/database.py", "backend/schemas.py",
            "backend/security.py", "backend/auth.py", "backend/services/__init__.py",
            "backend/services/password_generator.py"],
        5: ["backend/routes/__init__.py", "backend/routes/usuarios.py", "backend/routes/produtos.py",
            "backend/routes/pedidos.py", "backend/routes/cep.py"],
        6: [str(path.relative_to(ROOT)).replace("\\", "/") for path in sorted((ROOT / "public").rglob("*")) if path.is_file()],
        7: [".env.example", ".gitignore", ".vercelignore"],
        8: ["requirements.txt", "requirements-dev.txt", "requirements-lock.txt"],
        9: ["api/__init__.py", "api/index.py", "pyproject.toml", "vercel.json"],
        10: [str(path.relative_to(ROOT)).replace("\\", "/") for path in sorted((ROOT / "tests").glob("*.py"))],
        11: ["scripts/__init__.py", "scripts/init_db.py", "scripts/admin.py", "scripts/export_guide.py"],
    }
    return mapping.get(stage, [])


def main():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    sections = re.split(r"(?=^## ETAPA \d+)", readme, flags=re.MULTILINE)
    output = ["# Dessik — projeto completo em 14 etapas\n\n"
              "Entrega com tutorial e arquivos integrais. Os mesmos arquivos estão no repositório. "
              "Gerado por `python -m scripts.export_guide`. Nenhum segredo real é incluído.\n"]
    languages = {".py": "python", ".js": "javascript", ".html": "html", ".css": "css",
                 ".sql": "sql", ".json": "json", ".toml": "toml", ".svg": "xml"}
    for section in sections[1:]:
        number = int(re.match(r"## ETAPA (\d+)", section).group(1))
        # Corrige links relativos do README porque este documento fica em docs/.
        section = re.sub(r"\]\((?!https?://)([^)]+)\)", r"](../\1)", section)
        output.append(section)
        for filename in files_for_stage(number):
            path = ROOT / filename
            language = languages.get(path.suffix, "text")
            if path.suffix in {".png", ".jpg", ".jpeg", ".webp"}:
                output.append(f"\n### Arquivo: {filename}\n\nAsset de imagem: [{path.name}](../{filename}). Copie o arquivo binário junto com o projeto.\n")
                continue
            output.append(f"\n### Arquivo: {filename}\n\n```{language}\n{path.read_text(encoding='utf-8').rstrip()}\n```\n")
    destination = ROOT / "docs" / "PROJETO_COMPLETO.md"
    destination.parent.mkdir(exist_ok=True)
    destination.write_text("\n".join(output), encoding="utf-8")
    print(f"Documento completo gerado: {destination.name}")


if __name__ == "__main__":
    main()
