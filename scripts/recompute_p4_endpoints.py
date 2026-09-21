#!/usr/bin/env python3
"""Recompute Protocol 4 confirmatory headline endpoints from the frozen case-level score table.

This is a score-summary recomputation layer. It does not regenerate predictions,
open Gold, alter mappings, or perform any post-Gold tuning.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


DEFAULT_CSV = Path("data/p4/GATE3D2_RE2TT_CASE_LEVEL_SCORE.csv")
DEFAULT_FROZEN = Path("data/p4/GATE3D2_RE2TT_CONFIRMATORY_RESULTS.json")


def compute(rows: list[dict[str, str]]) -> dict:
    n = len(rows)
    states = Counter(r["decision_state"] for r in rows)
    topology = Counter(r["topology_state"] for r in rows)

    entitled = [r for r in rows if r["decision_state"] == "EXACT_SOURCE_ENTITLED"]
    correct = [
        r for r in entitled
        if r.get("exact_correct", "").strip().lower() == "true"
        and r.get("predicted_exact_source", "") == r.get("gold_root_cause_service", "")
    ]
    false_entitlements = [
        r for r in entitled
        if not (
            r.get("exact_correct", "").strip().lower() == "true"
            and r.get("predicted_exact_source", "") == r.get("gold_root_cause_service", "")
        )
    ]

    cross = Counter((r["decision_state"], r["topology_state"]) for r in rows)

    return {
        "n_cases": n,
        "primary_endpoints": {
            "exact_source_entitlement_n": len(entitled),
            "exact_source_entitlement_coverage": (len(entitled) / n) if n else None,
            "exact_selective_correct_n": len(correct),
            "exact_selective_accuracy": (len(correct) / len(entitled)) if entitled else None,
            "false_exact_entitlement_events_n": len(false_entitlements),
            "false_exact_entitlement_events_per_90": (len(false_entitlements) / n) if n else None,
            "UNDERDETERMINED_n": states.get("UNDERDETERMINED", 0),
            "ABSTAIN_n": states.get("ABSTAIN", 0),
            "HOLD_n": states.get("HOLD", 0),
            "K2_status": "DISABLED_NA",
            "source_topology_separability_cross_tab": [
                {"source_state": s, "topology_state": t, "n": c}
                for (s, t), c in sorted(cross.items())
            ],
        },
        "topology_state_counts": dict(sorted(topology.items())),
        "support_criterion": (
            len(entitled) > 0 and len(correct) == len(entitled) and len(false_entitlements) == 0
        ),
    }


def compare(computed: dict, frozen: dict) -> list[str]:
    problems: list[str] = []
    if computed["n_cases"] != frozen.get("n_cases"):
        problems.append(f"n_cases: {computed['n_cases']} != {frozen.get('n_cases')}")
    cp = computed["primary_endpoints"]
    fp = frozen.get("primary_endpoints", {})

    keys = [
        "exact_source_entitlement_n",
        "exact_source_entitlement_coverage",
        "exact_selective_correct_n",
        "exact_selective_accuracy",
        "false_exact_entitlement_events_n",
        "false_exact_entitlement_events_per_90",
        "UNDERDETERMINED_n",
        "ABSTAIN_n",
        "HOLD_n",
        "K2_status",
        "source_topology_separability_cross_tab",
    ]
    for k in keys:
        a, b = cp.get(k), fp.get(k)
        if isinstance(a, float) and isinstance(b, (float, int)):
            if abs(a - float(b)) > 1e-15:
                problems.append(f"{k}: {a!r} != {b!r}")
        elif a != b:
            problems.append(f"{k}: {a!r} != {b!r}")

    frozen_support = frozen.get("confirmatory_support_criterion", {}).get("support")
    if computed["support_criterion"] != frozen_support:
        problems.append(
            f"support_criterion: {computed['support_criterion']} != {frozen_support}"
        )
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--case-score", type=Path, default=DEFAULT_CSV)
    ap.add_argument("--frozen-result", type=Path, default=DEFAULT_FROZEN)
    ap.add_argument("--json-out", type=Path)
    ap.add_argument("--no-compare", action="store_true")
    args = ap.parse_args()

    with args.case_score.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    computed = compute(rows)
    print(json.dumps(computed, indent=2, sort_keys=True))

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(computed, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if not args.no_compare:
        frozen = json.loads(args.frozen_result.read_text(encoding="utf-8"))
        problems = compare(computed, frozen)
        if problems:
            print("P4_SCORE_RECOMPUTE = FAIL")
            for p in problems:
                print(" -", p)
            return 1

    ep = computed["primary_endpoints"]
    print("P4_SCORE_RECOMPUTE = PASS")
    print(f"N = {computed['n_cases']}")
    print(f"EXACT_SOURCE_ENTITLEMENT = {ep['exact_source_entitlement_n']}/{computed['n_cases']}")
    print(f"SELECTIVE_CORRECT = {ep['exact_selective_correct_n']}/{ep['exact_source_entitlement_n']}")
    print(f"FALSE_EXACT_ENTITLEMENT = {ep['false_exact_entitlement_events_n']}/{computed['n_cases']}")
    print(f"UNDERDETERMINED = {ep['UNDERDETERMINED_n']}/{computed['n_cases']}")
    print(f"ABSTAIN = {ep['ABSTAIN_n']}/{computed['n_cases']}")
    print(f"HOLD = {ep['HOLD_n']}/{computed['n_cases']}")
    print("TOPOLOGY_UNDERDETERMINED = "
          f"{computed['topology_state_counts'].get('TOPOLOGY_UNDERDETERMINED', 0)}/{computed['n_cases']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
