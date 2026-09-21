from __future__ import annotations
from pathlib import Path
import json
from .io import sha256_file


def verify_manifest(repo_root: str | Path):
    root=Path(repo_root); manifest=json.loads((root/'MANIFEST_SHA256.json').read_text(encoding='utf-8'))
    problems=[]
    for rel,meta in manifest['files'].items():
        p=root/rel
        if not p.exists(): problems.append(f'missing:{rel}'); continue
        got=sha256_file(p)
        if got != meta['sha256']: problems.append(f'hash:{rel}')
    return not problems, problems
