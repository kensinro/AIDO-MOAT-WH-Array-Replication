import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_protocol4_headline_recompute_matches_frozen_result(tmp_path):
    out = tmp_path / "p4_recomputed.json"
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "recompute_p4_endpoints.py"),
            "--json-out",
            str(out),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr
    assert "P4_SCORE_RECOMPUTE = PASS" in proc.stdout

    x = json.loads(out.read_text(encoding="utf-8"))
    ep = x["primary_endpoints"]
    assert x["n_cases"] == 90
    assert ep["exact_source_entitlement_n"] == 2
    assert ep["exact_selective_correct_n"] == 2
    assert ep["false_exact_entitlement_events_n"] == 0
    assert ep["UNDERDETERMINED_n"] == 83
    assert ep["ABSTAIN_n"] == 5
    assert ep["HOLD_n"] == 0
    assert x["topology_state_counts"] == {"TOPOLOGY_UNDERDETERMINED": 90}
    assert x["support_criterion"] is True
