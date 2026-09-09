from pathlib import Path
import shutil
import re

root = Path(__file__).resolve().parents[1]
ws = root / 'workspace'
pub = ws / 'publico'
private = ws / 'privada'

def read(path):
    return (root / path).read_text(encoding='utf-8')

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')

# A versão anterior permanece intacta; a entrega acadêmica é autocontida.
for source in (root / 'public').rglob('*'):
    if source.is_file() and 'data' not in source.parts:
        target = pub / source.relative_to(root / 'public')
        target = Path(str(target).replace('images', 'imagens'))
        if source.suffix in ('.html', '.js', '.css', '.svg'):
            text = source.read_text(encoding='utf-8').replace('/images/', '/imagens/')
            if source.suffix == '.html':
                text = text.replace('<nav aria-label="Navegação principal">', '<nav aria-label="Navegação principal"><a href="/index.html">Início</a><a href="/carrinho.html">Carrinho</a>')
                text = text.replace('class="brand" href="/loja.html"', 'class="brand" href="/index.html"')
            write(target, text)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)

config = read('backend/config.py').replace('from dotenv import load_dotenv', 'from pathlib import Path\nfrom dotenv import load_dotenv')
config = config.replace('load_dotenv()', 'load_dotenv(Path(__file__).resolve().parents[1] / ".env")')
database = read('backend/database.py').replace('from backend.config import settings', '')
write(private / 'backend/database.py', config + '\n\n' + database)
security = read('backend/security.py').replace('from backend.config import settings', 'from backend.database import settings')
auth = read('backend/auth.py').replace('from backend.security import decode_token', '')
auth = auth.replace('is_admin FROM', 'tipo_usuario FROM').replace('user["is_admin"] = bool(user["is_admin"])', 'user["is_admin"] = user["tipo_usuario"] == "admin"')
auth = auth.replace('if not user["is_admin"]:', 'if user["tipo_usuario"] != "admin":')
write(private / 'backend/auth.py', security + '\n\n' + read('backend/services/password_generator.py') + '\n\n' + auth)
write(private / 'backend/schemas.py', read('backend/schemas.py').replace('/images/', '/imagens/'))
write(private / 'backend/models.py', '''"""Sem ORM: as tabelas estão em database/schema.sql e usamos dicionários."""

def serialize_product(product):
    # Decimal vira texto no JSON para preservar os centavos.
    product["preco"] = str(product["preco"])
    return product
''')
main = read('api/index.py')
main = main.replace('from backend.config import settings', 'from backend.database import settings, transaction')
main = main.replace('from backend.routes import cep, pedidos, produtos, usuarios', '''import re
import httpx
from decimal import Decimal
from typing import Literal
from fastapi import Depends, HTTPException, Query
from mysql.connector import IntegrityError
from backend.auth import current_user, admin_user, create_token, hash_password, verify_password, generate_password
from backend.schemas import Cadastro, Login, Produto, Pedido
from backend.models import serialize_product''')
start = main.index('for router in ')
main = main[:start]
for name, prefix in [('usuarios', ''), ('produtos', '/produtos'), ('pedidos', '/pedidos'), ('cep', '')]:
    route = read(f'backend/routes/{name}.py')
    route = route[route.index('router = '):].split('\n', 1)[1]
    if name == 'produtos':
        route = route[route.index('@router.get'):]
    route = re.sub(r'@router\.(get|post|put|delete)\("([^\"]*)"', lambda m: f'@app.{m[1]}("/api{prefix}{m[2]}"', route)
    main += '\n\n# ' + name.upper() + '\n' + route
main += '''

@app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"], include_in_schema=False)
def unknown_api(path: str):
    raise HTTPException(404, "Endpoint não encontrado.")


# Somente publico/ é servido. Nunca monte workspace/ ou privada/ como arquivos estáticos.
if os.getenv("VERCEL") != "1":
    app.mount("/", StaticFiles(directory=Path(__file__).resolve().parents[2] / "publico", html=True), name="frontend")
'''
main = main.replace('cursor.execute(', '# Query parametrizada: valores separados do SQL evitam SQL Injection.\n        cursor.execute(', 1)
main = main.replace('total += product["preco"] * item.quantidade', '# O navegador envia apenas IDs e quantidades: preço e estoque vêm do banco.\n            total += product["preco"] * item.quantidade')
write(private / 'backend/main.py', main)
write(private / 'api/index.py', '"""Ponto de entrada reconhecido pela Vercel."""\nfrom backend.main import app\n')
for file in ['schema.sql', 'dados.sql']:
    sql = read('database/' + file).replace('/images/', '/imagens/').replace('is_admin BOOLEAN NOT NULL DEFAULT FALSE', "tipo_usuario ENUM('cliente', 'admin') NOT NULL DEFAULT 'cliente'")
    write(private / 'database' / file, sql)
write(private / 'requirements.txt', read('requirements.txt'))
write(private / 'vercel.json', '{\n  "$schema": "https://openapi.vercel.sh/vercel.json",\n  "framework": "fastapi"\n}\n')
write(private / '.env.example', '''DB_HOST=
DB_PORT=3306
DB_USER=
DB_PASSWORD=
DB_NAME=loja_ficticia
DB_SSL=true
DB_SSL_CA=

JWT_SECRET=
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
APP_ENV=development
CORS_ORIGINS=http://127.0.0.1:5500,http://localhost:5500
''')
for folder in (private, pub):
    write(folder / '.gitignore', '.env\n.env.*\n!.env.example\nvenv/\n.venv/\n__pycache__/\n*.pyc\n.pytest_cache/\n.vercel/\n')
api = (pub / 'js/api.js').read_text(encoding='utf-8')
api = 'export const API_URL = "http://127.0.0.1:8000/api"; // Altere aqui para a URL HTTPS da API publicada.\n' + api.replace('fetch(`/api${path}`', 'fetch(`${API_URL}${path}`')
write(pub / 'js/api.js', api)

# Imagens adicionais são SVGs simples e locais, fáceis de editar.
arts = {
 'hub': '<rect x="90" y="110" width="220" height="90" rx="20" fill="#414854"/><path d="M310 150h30v-60" fill="none" stroke="#414854" stroke-width="12"/><g fill="#ff855a"><rect x="115" y="145" width="35" height="20"/><rect x="180" y="145" width="35" height="20"/><rect x="245" y="145" width="35" height="20"/></g>',
 'mousepad': '<path d="M80 100h220l40 120H40z" fill="#343b47" stroke="#ff855a" stroke-width="5"/><path d="M115 135h90m-65 25h90m-60 25h90" stroke="#596576" stroke-width="4"/>',
 'suporte': '<path d="M130 95l-40 120h210L260 95" fill="none" stroke="#687789" stroke-width="15"/><path d="M100 155h190" stroke="#ff855a" stroke-width="14"/>',
 'controle': '<path d="M135 105h130c35 0 65 115 35 125-25 8-50-45-65-45h-60c-15 0-40 53-65 45-30-10 0-125 25-125z" fill="#343b47"/><path d="M140 130v42m-21-21h42" stroke="#94a0b1" stroke-width="10"/><circle cx="258" cy="142" r="10" fill="#ff855a"/><circle cx="280" cy="163" r="10" fill="#ff855a"/>'
}
for name, art in arts.items():
    write(pub / 'imagens' / f'{name}.svg', f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#e9edf2"/>{art}</svg>')
extras = [(9, 'Hub USB Connect', 'Quatro portas USB para organizar seus acessórios.', 'Acessórios', '89.90', 3, 'hub'),
          (10, 'Mousepad Glide', 'Base antiderrapante com espaço para movimentos livres.', 'Acessórios', '49.90', 30, 'mousepad'),
          (11, 'Suporte Rise', 'Suporte de mesa para elevar seu notebook.', 'Acessórios', '119.90', 2, 'suporte'),
          (12, 'Controle Play', 'Controle USB para seus jogos no computador.', 'Periféricos', '159.90', 10, 'controle')]
sql = (private / 'database/dados.sql').read_text(encoding='utf-8')
for id, name, desc, category, price, stock, art in extras:
    sql += f"\nINSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)\nSELECT {id},'{name}','{desc}','{category}',{price},{stock},'/imagens/{art}.svg'\nWHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto={id});\n"
write(private / 'database/dados.sql', sql)
print('Workspace criado.')
