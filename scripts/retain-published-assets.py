#!/usr/bin/env python3
"""Retain immutable CSS/JS referenced by cached HTML; leave old pages behind."""
import hashlib
from pathlib import Path
import re
import subprocess
import sys

output = Path(sys.argv[1] if len(sys.argv) > 1 else 'public')
ref = sys.argv[2] if len(sys.argv) > 2 else 'origin/gh-pages'
pattern = re.compile(r'assets/(?:css|js)/[^/]+\.([0-9a-f]{64})\.(?:css|js)$')


def git(*args):
    return subprocess.check_output(['git', *args])


# The latest tree carries retained assets forward. Recent history also recovers
# hashes deleted before this policy was introduced.
revisions = git('rev-list', '--max-count=6', ref).decode().splitlines()
retained = 0
for revision in revisions:
    for record in git('ls-tree', '-rz', revision, 'assets/css', 'assets/js').split(b'\0'):
        if not record:
            continue
        metadata, name = record.split(b'\t', 1)
        name = name.decode()
        match = pattern.fullmatch(name)
        if not match or metadata.split()[1] != b'blob':
            continue
        target = output / name
        if target.exists():
            continue
        content = git('cat-file', 'blob', metadata.split()[2].decode())
        if hashlib.sha256(content).hexdigest() != match.group(1):
            raise SystemExit(f'Asset fingerprint mismatch: {name}')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        retained += 1
print(f'Retained {retained} previously published fingerprinted CSS/JS assets')
