"""Ambiente local de revisão. Credenciais ficam somente em arquivos ignorados."""
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import time
import mysql.connector

root = Path(__file__).resolve().parents[1]
private = root / 'workspace/privada'
local = root / '.local'
credentials = json.loads((local / 'test-env.json').read_text())
options = dict(host='127.0.0.1', port=33316, user='root', password=credentials['DB_PASSWORD'], ssl_disabled=True)
try:
    conn = mysql.connector.connect(**options)
except mysql.connector.Error:
    log = (local / 'workspace-db.log').open('a')
    server = subprocess.Popen([str(local / 'mariadb-11.4.11-winx64/bin/mariadbd.exe'),
        f'--defaults-file={local / "mysql-test-data/my.ini"}', '--bind-address=127.0.0.1', '--port=33316', '--console'],
        stdout=log, stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW)
    for _ in range(40):
        try:
            conn = mysql.connector.connect(**options)
            break
        except mysql.connector.Error:
            time.sleep(.25)
    else:
        raise RuntimeError('Banco local não iniciou.')

cursor = conn.cursor()
for name in ('dessik_workspace', 'dessik_workspace_test'):
    cursor.execute(f'CREATE DATABASE IF NOT EXISTS {name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
    cursor.execute(f'USE {name}')
    for file in ('schema.sql', 'dados.sql'):
        sql = '\n'.join(line for line in (private / 'database' / file).read_text(encoding='utf-8').splitlines() if not line.lstrip().startswith('--'))
        for statement in sql.split(';'):
            if statement.strip(): cursor.execute(statement)
conn.commit()
cursor.close()
conn.close()

env_path = private / '.env'
if not env_path.exists():
    # Usuário local separado de root, limitado ao banco desta entrega.
    password = secrets.token_urlsafe(32)
    conn = mysql.connector.connect(**options)
    cursor = conn.cursor()
    cursor.execute('CREATE USER IF NOT EXISTS %s@%s IDENTIFIED BY %s', ('dessik_workspace', '127.0.0.1', password))
    cursor.execute('GRANT SELECT, INSERT, UPDATE, DELETE ON dessik_workspace.* TO %s@%s', ('dessik_workspace', '127.0.0.1'))
    conn.commit(); cursor.close(); conn.close()
    values = {'DB_HOST':'127.0.0.1', 'DB_PORT':'33316', 'DB_USER':'dessik_workspace', 'DB_PASSWORD':password,
        'DB_NAME':'dessik_workspace', 'DB_SSL':'false', 'JWT_SECRET':secrets.token_urlsafe(48),
        'JWT_ALGORITHM':'HS256', 'ACCESS_TOKEN_EXPIRE_MINUTES':'60', 'APP_ENV':'development',
        'CORS_ORIGINS':'http://127.0.0.1:5500,http://localhost:5500,http://localhost:8000'}
    env_path.write_text('\n'.join(f'{k}={v}' for k,v in values.items())+'\n', encoding='utf-8')

test_env = os.environ | credentials | {'DB_NAME':'dessik_workspace_test', 'RUN_MYSQL_TESTS':'1'}
result = subprocess.run([sys.executable, '-m', 'pytest', '-q'], cwd=private, env=test_env)
if result.returncode: sys.exit(result.returncode)
log = (local / 'workspace-api.log').open('a')
api = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'backend.main:app', '--host', '127.0.0.1', '--port', '8000'],
    cwd=private, stdout=log, stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW)
print('API local: http://127.0.0.1:8000 | PID', api.pid)
