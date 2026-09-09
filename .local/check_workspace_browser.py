import json
import os
from pathlib import Path
import subprocess
import sys
import time
import httpx

root = Path(__file__).resolve().parents[1]
private = root / 'workspace/privada'
env = os.environ | json.loads((root / '.local/test-env.json').read_text())
env.update(DB_NAME='dessik_workspace_test', RUN_BROWSER_TESTS='1', BROWSER_URL='http://127.0.0.1:8001',
           QA_SCREENSHOT=str(root / '.local/workspace-desktop.png'))
log = (root / '.local/workspace-browser-api.log').open('w')
server = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'backend.main:app', '--port', '8001'],
    cwd=private, env=env, stdout=log, stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW)
try:
    for _ in range(40):
        try:
            if httpx.get('http://127.0.0.1:8001/api/health').status_code == 200: break
        except httpx.HTTPError: pass
        time.sleep(.2)
    result = subprocess.run([sys.executable, '-m', 'pytest', 'tests/test_browser.py', '-q'], cwd=private, env=env)
    sys.exit(result.returncode)
finally:
    server.terminate(); server.wait(timeout=10)
