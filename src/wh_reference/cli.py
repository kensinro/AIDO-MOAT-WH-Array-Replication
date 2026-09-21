from __future__ import annotations
import argparse
from pathlib import Path
from .reproduce import reproduce, write_report
from .validate import verify_manifest


def main(argv=None):
    p=argparse.ArgumentParser(prog='wh-reference',description='Reproduce and validate WH1.0 frozen qualification results.')
    sp=p.add_subparsers(dest='cmd',required=True)
    r=sp.add_parser('reproduce'); r.add_argument('--data-root',default='data'); r.add_argument('--output',default='artifacts')
    v=sp.add_parser('validate'); v.add_argument('--repo-root',default='.')
    a=p.parse_args(argv)
    if a.cmd=='reproduce':
        result=reproduce(Path(a.data_root)); write_report(result,Path(a.output)); print(Path(a.output)/'REPRODUCED_RESULTS.md')
    else:
        ok,problems=verify_manifest(Path(a.repo_root));
        if ok: print('MANIFEST PASS')
        else:
            print('MANIFEST FAIL'); [print(' -',x) for x in problems]; raise SystemExit(1)

if __name__=='__main__': main()
