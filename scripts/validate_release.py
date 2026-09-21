from pathlib import Path
from wh_reference.validate import verify_manifest
root=Path(__file__).resolve().parents[1]
ok,problems=verify_manifest(root)
print('PASS' if ok else 'FAIL')
for p in problems: print(p)
raise SystemExit(0 if ok else 1)
