from pathlib import Path
root = Path(__file__).resolve().parents[1]
private = root / 'workspace/privada'
tests = private / 'tests'
tests.mkdir(exist_ok=True)
for file in (root / 'tests').glob('*.py'):
    text = file.read_text(encoding='utf-8')
    text = text.replace('from backend.config import settings', 'from backend.database import settings')
    text = text.replace('from backend.security import ', 'from backend.auth import ')
    text = text.replace('from backend.services.password_generator import ', 'from backend.auth import ')
    text = text.replace('/images/', '/imagens/')
    text = text.replace("parents[1] / 'public'", "parents[2] / 'publico'")
    text = text.replace("{'id_usuario': 1, 'is_admin': False}", "{'id_usuario': 1, 'tipo_usuario': 'cliente'}")
    text = text.replace('SELECT senha_hash, is_admin FROM', 'SELECT senha_hash, tipo_usuario FROM')
    text = text.replace("stored['is_admin'] == 0", "stored['tipo_usuario'] == 'cliente'")
    text = text.replace("'UPDATE usuarios SET is_admin=TRUE WHERE id_usuario=%s'", '"UPDATE usuarios SET tipo_usuario=\'admin\' WHERE id_usuario=%s"')
    if file.name == 'conftest.py':
        text = text.replace('os.environ.setdefault(', 'os.environ.setdefault(')
    (tests / file.name).write_text(text, encoding='utf-8')
(private / 'pytest.ini').write_text('[pytest]\ntestpaths = tests\npythonpath = .\nmarkers =\n    integration: requer banco isolado terminado em _test\n', encoding='utf-8')
(private / 'requirements-dev.txt').write_text('-r requirements.txt\npytest==9.0.2\n', encoding='utf-8')
print('Testes adaptados à estrutura acadêmica.')
