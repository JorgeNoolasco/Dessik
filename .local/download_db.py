from pathlib import Path
import hashlib
import zipfile
import httpx

root = Path(__file__).resolve().parent
base = 'https://buildbot.mariadb.net/archive/pack/bb-11.4-release/build-67747/winx64-packages/'
name = 'mariadb-11.4.11-winx64.zip'
with httpx.Client(follow_redirects=True, timeout=45) as client:
    checksum = client.get(base + 'sha256sums.txt')
    checksum.raise_for_status()
    expected = next(line.split()[0].lower() for line in checksum.content.decode('utf-16').splitlines() if line.rstrip().endswith(name))
    with client.stream('GET', base + name) as response:
        response.raise_for_status()
        with (root / name).open('wb') as out:
            for chunk in response.iter_bytes():
                out.write(chunk)
assert hashlib.sha256((root / name).read_bytes()).hexdigest() == expected
with zipfile.ZipFile(root / name) as archive:
    archive.extractall(root)
print('MariaDB portátil extraído e SHA256 verificado.')
