import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import time

import mysql.connector

root = Path(__file__).resolve().parents[1]
folder = root / '.local'
bin_dir = folder / 'mariadb-11.4.11-winx64' / 'bin'
data = folder / 'mysql-test-data'
credentials = folder / 'test-env.json'
if credentials.exists():
    env_values = json.loads(credentials.read_text())
else:
    env_values = {'DB_HOST': '127.0.0.1', 'DB_PORT': '33316', 'DB_USER': 'root',
                  'DB_PASSWORD': secrets.token_urlsafe(32), 'DB_NAME': 'dessik_test',
                  'DB_SSL': 'false', 'JWT_SECRET': secrets.token_urlsafe(48),
                  'APP_ENV': 'development', 'RUN_MYSQL_TESTS': '1'}
    credentials.write_text(json.dumps(env_values))
environment = os.environ | env_values
hidden = subprocess.CREATE_NO_WINDOW
if not data.exists():
    result = subprocess.run([str(bin_dir / 'mariadb-install-db.exe'), f'--datadir={data}',
                             f"--password={env_values['DB_PASSWORD']}", '--port=33316', '--silent'],
                            capture_output=True, creationflags=hidden)
    if result.returncode:
        print('Falha ao inicializar banco de teste.'); sys.exit(1)
server = subprocess.Popen([str(bin_dir / 'mariadbd.exe'), f'--defaults-file={data / "my.ini"}',
                           '--bind-address=127.0.0.1', '--port=33316', '--console'],
                          stdout=(folder / 'mysql-test.log').open('w'), stderr=subprocess.STDOUT,
                          creationflags=hidden)
try:
    for _ in range(60):
        try:
            connection = mysql.connector.connect(host='127.0.0.1', port=33316,
                user='root', password=env_values['DB_PASSWORD'], ssl_disabled=True)
            break
        except mysql.connector.Error:
            if server.poll() is not None: raise RuntimeError('Servidor de teste encerrou antes de iniciar.')
            time.sleep(.5)
    else:
        raise RuntimeError('Banco de teste não iniciou.')
    cursor = connection.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS dessik_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
    cursor.close(); connection.close()
    result = subprocess.run([sys.executable, '-m', 'scripts.init_db'], env=environment, cwd=root)
    if result.returncode: sys.exit(result.returncode)
    result = subprocess.run([sys.executable, '-m', 'pytest', '-q'], env=environment, cwd=root)
    sys.exit(result.returncode)
finally:
    try:
        connection = mysql.connector.connect(host='127.0.0.1', port=33316, user='root',
            password=env_values['DB_PASSWORD'], ssl_disabled=True)
        cursor = connection.cursor(); cursor.execute('SHUTDOWN'); cursor.close(); connection.close()
    except mysql.connector.Error:
        server.terminate()
    server.wait(timeout=15)
