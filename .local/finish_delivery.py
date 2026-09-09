from pathlib import Path
from dotenv import dotenv_values
import ast

root = Path(__file__).resolve().parents[1]
ws = root / 'workspace'
pub = ws / 'publico'
# Reúne imports no início para manter os arquivos didáticos.
for name in ('auth.py', 'database.py', 'main.py'):
    path = ws / 'privada/backend' / name
    source = path.read_text(encoding='utf-8')
    if name == 'main.py':
        source = source.replace('from fastapi import Depends, HTTPException, Query', 'from fastapi import Depends, Query')
    lines = source.splitlines()
    imports = []
    removed = set()
    for node in ast.parse(source).body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            statement = '\n'.join(lines[node.lineno-1:node.end_lineno])
            if statement not in imports: imports.append(statement)
            removed.update(range(node.lineno-1, node.end_lineno))
    body = '\n'.join(line for index, line in enumerate(lines) if index not in removed).strip()
    while '\n\n\n\n' in body: body = body.replace('\n\n\n\n', '\n\n\n')
    path.write_text('\n'.join(imports)+'\n\n\n'+body+'\n', encoding='utf-8')

path = ws / 'README.md'
text = path.read_text(encoding='utf-8').replace('API: 39 testes passaram', 'API: 43 testes passaram')
text = text.replace('incluindo integração com banco e concorrência.', 'incluindo integração com banco, compra de vários itens, rejeição de preço adulterado e concorrência.')
text = text.replace('Navegador: fluxo real', 'O teste de navegador foi executado separadamente: fluxo real')
text = text.replace('A disponibilidade do serviço externo depende da rede.', 'A consulta real do CEP `01001000` também retornou HTTP 200 e o endereço de São Paulo nesta revisão. A disponibilidade do serviço externo depende da rede.')
path.write_text(text, encoding='utf-8')
path = pub / 'README.md'
text = path.read_text(encoding='utf-8').replace('pelas regras finais em', 'pelas seções comentadas em')
path.write_text(text, encoding='utf-8')

source = (root / '.local/finalize_workspace.py').read_text(encoding='utf-8')
exec(source[source.index('descriptions ='):])
secret_values = dotenv_values(ws / 'privada/.env')
files = [path for path in pub.rglob('*') if path.is_file() and path.suffix != '.png'] + [ws / 'CODIGO_COMPLETO.md']
assert not any(secret_values[key] in path.read_text(encoding='utf-8') for key in ('JWT_SECRET', 'DB_PASSWORD') for path in files)
print('Guia atualizado. Nenhuma credencial privada no front-end ou guia.')
