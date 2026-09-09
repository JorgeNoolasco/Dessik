import os
import secrets
import sys
from pathlib import Path
import uvicorn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

os.environ.update(APP_ENV='development', DB_HOST='127.0.0.1', DB_PORT='33316',
                  DB_USER='dessik_preview', DB_NAME='dessik_preview', DB_SSL='false',
                  JWT_SECRET=secrets.token_urlsafe(48))
# Prévia da interface: não cria nem conecta dados de produção.
uvicorn.run('api.index:app', host='127.0.0.1', port=8765)
