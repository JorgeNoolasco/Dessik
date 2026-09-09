import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
env = os.environ | json.loads((root / '.local/test-env.json').read_text())
env.update(DB_NAME='dessik_workspace_test', RUN_MYSQL_TESTS='1')
result = subprocess.run([sys.executable, '-m', 'pytest', '-q'], cwd=root / 'workspace/privada', env=env)
sys.exit(result.returncode)
