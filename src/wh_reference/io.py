from __future__ import annotations
from pathlib import Path
import json, hashlib


def load_json(path: str | Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha256_file(path: str | Path) -> str:
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ratio(n: int, d: int) -> dict:
    return {"n": int(n), "d": int(d), "rate": None if d == 0 else n / d}


def as_set(x):
    return set(x or [])
