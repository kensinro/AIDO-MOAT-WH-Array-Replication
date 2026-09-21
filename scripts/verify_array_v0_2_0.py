#!/usr/bin/env python3
"""Fail-closed verifier for the Array V0.2.0 reproducibility package.

Stdlib only. It verifies exact recovered artifact bytes, Protocol 4 lineage
invariants, and specification-reconstructibility evidence that can be checked
without re-running scientific inference.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_SHA256 = {
    "data/p4/GATE3C_RE2TT_PREDICTION_FREEZE_RECEIPT.json": "d014fd060d9c65dfdb2721c767d6b2e5bf5e43c6e8cf5c2e19c91e304f4a1022",
    "data/p4/GATE3D_GOLD_PATH_PARSE_HOLD.json": "988122883b9b558356d1399365eadd3304392397e4239cb500540a48466e5dec",
    "data/p4/GATE3D1_RE2TT_GOLD_MAPPING_REPAIRED.json": "7a2431b7163809bc6abb9a38daf54fef1e4b7cccf37f35a50d30a9d7b3d281cc",
    "data/p4/GATE3D1_GOLD_PATH_SEMANTICS_AUDIT.json": "f952f5942d8621eee1c1764fadba0a2e3e53237c4984d19786241fa69bacb4e9",
    "data/p4/GATE3D2_RE2TT_CONFIRMATORY_RESULTS.json": "ffb6f9a1d9d82782b4afc9ed6eaf935cdb1e8ef85b814ce06a66fb294dd703db",
    "data/p4/GATE3D2_RESULT_FREEZE_RECEIPT.json": "7bb7d75f748e409e0352ddf39e0f882ae2ed08730dd5325a28cf68fccd040fa4",
    "data/p4/GATE3D2_RE2TT_CASE_LEVEL_SCORE.csv": "8af4f019135e6197bee54dab3d6471e99a8676884beb9eefedf9e3a9debcadd3",
    "data/p4/WH1X_GATE3D1_INDEPENDENT_MAPPING_AUDIT_PASS_2026-08-29.md": "c95fae2c4ee043ec33c6a929eda8ccf9c4d1cef2c423378f38b3952ff34cbd41",
    "data/p4/GATE3C_RETURN_PACKET_PRE_GOLD.zip": "3b46dc057e9d50335f957621f7a9639092e9b6426a27232bb6441a3c281957a8",
    "data/p4/GATE3D1_RETURN_PACKET_GOLD_MAPPING_REPAIRED.zip": "e9899bb7b39e16c656fff32aaf08e32422e5cda2bb0f1bff3646a19bd47fa69e",
    "data/p4/GATE3D2_RETURN_PACKET_CONFIRMATORY_RESULTS.zip": "f31b2314d5e603288a421a919fc707d6da03fef7584165df47cb29296118fcda",
    "reconstruction/WH_JSS_DECISION_INPUT_CONTRACT_V0.1.json": "82065a9b5af20dfeeb6e4931580bc1e1568a29fbeb1c0c6204b0fa2eb6faa699",
    "reconstruction/WH_JSS_INDEPENDENT_RECONSTRUCTION_AUDIT_V0.1.md": "1a6d05ad7d8c24fc98d424ab13c422a4049763058dae13839b429533bc44f276",
    "reconstruction/WH_JSS_INDEPENDENT_RECONSTRUCTION_PACKET_V0.1.zip": "7581b4fc7744fa5c872622edd9b6c2b9a047a69ee97bfc8ace843d14e45eae1d",
    "reconstruction/WH_JSS_EXECUTABLE_RECONSTRUCTION_V0.2.zip": "879dd0f86454ea67e63e81592c5914ff1ed7aa4d1d82e5a8ecf2dd8abada52ec",
}

PRED_SHA = "5d0cc805eefb353935b5b277f62610850f0f23e1e4a11bd64014b231d43e09f5"
GOLD_SHA = "7a2431b7163809bc6abb9a38daf54fef1e4b7cccf37f35a50d30a9d7b3d281cc"
RESULT_SHA = "ffb6f9a1d9d82782b4afc9ed6eaf935cdb1e8ef85b814ce06a66fb294dd703db"
CASE_SCORE_SHA = "8af4f019135e6197bee54dab3d6471e99a8676884beb9eefedf9e3a9debcadd3"
V01_PYC_MEMBER = "WH_JSS_EXECUTABLE_RECONSTRUCTION_V0.2/__pycache__/wh_jss_reference_adjudicator_v0_1.cpython-313.pyc"
V01_PYC_SHA = "d70a283e6fa949566a28fa7cabb65544229489d9365df7a4ae993e6f4d7862e5"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def fail(msg: str, problems: list[str]):
    problems.append(msg)


def main() -> int:
    problems: list[str] = []

    # A. Exact byte identity.
    for rel, expected in EXPECTED_SHA256.items():
        path = ROOT / rel
        if not path.is_file():
            fail(f"MISSING {rel}", problems)
            continue
        got = sha256(path)
        if got != expected:
            fail(f"HASH {rel}: expected {expected}, got {got}", problems)

    # A2. Recover exact historical V0.1 executable bytecode embedded in V0.2 packet.
    exec_zip = ROOT / "reconstruction/WH_JSS_EXECUTABLE_RECONSTRUCTION_V0.2.zip"
    try:
        with zipfile.ZipFile(exec_zip, "r") as zf:
            pyc_bytes = zf.read(V01_PYC_MEMBER)
        got_pyc = hashlib.sha256(pyc_bytes).hexdigest()
        if got_pyc != V01_PYC_SHA:
            fail(f"V0.1 bytecode hash mismatch: expected {V01_PYC_SHA}, got {got_pyc}", problems)
    except Exception as e:
        fail(f"V0.1 bytecode recovery failed: {e}", problems)

    # B. Protocol 4 pre-Gold freeze invariants.
    freeze = load_json("data/p4/GATE3C_RE2TT_PREDICTION_FREEZE_RECEIPT.json")
    if freeze.get("status") != "GATE3C_RE2TT_PREDICTIONS_FROZEN_PRE_GOLD":
        fail("P4 freeze status mismatch", problems)
    if freeze.get("gold_read") is not False:
        fail("P4 freeze must record gold_read=false", problems)
    if freeze.get("n_cases") != 90:
        fail("P4 freeze denominator must be 90", problems)
    if freeze.get("prediction_bundle_sha256") != PRED_SHA:
        fail("P4 prediction bundle hash mismatch", problems)
    if freeze.get("state_counts") != {"UNDERDETERMINED": 83, "EXACT_SOURCE_ENTITLED": 2, "ABSTAIN": 5}:
        fail("P4 state counts mismatch", problems)
    if freeze.get("post_prediction_tuning_permitted") is not False:
        fail("P4 post-prediction tuning must be false", problems)

    # C. Preserve the historical parser HOLD rather than silently deleting it.
    hold = load_json("data/p4/GATE3D_GOLD_PATH_PARSE_HOLD.json")
    if hold.get("status") != "GOLD_OPENED_BUT_MAPPING_PARSE_HOLD":
        fail("P4 parser HOLD status mismatch", problems)
    if hold.get("gold_opened") is not True or hold.get("n_parse_fail") != 90:
        fail("P4 parser HOLD must preserve 90/90 failure", problems)
    failures = hold.get("parse_failures", [])
    if len(failures) != 90 or any(x.get("error") != "GOLD_PATH_PATTERN_NOT_UNIQUE" for x in failures):
        fail("P4 parser HOLD failure ledger mismatch", problems)

    # D. Deterministic path-semantics repair.
    mapping = load_json("data/p4/GATE3D1_RE2TT_GOLD_MAPPING_REPAIRED.json")
    audit = load_json("data/p4/GATE3D1_GOLD_PATH_SEMANTICS_AUDIT.json")
    if mapping.get("n_cases") != 90 or mapping.get("prediction_bundle_sha256") != PRED_SHA:
        fail("P4 repaired mapping denominator/prediction hash mismatch", problems)
    if mapping.get("prediction_content_read_for_parser_choice") is not False:
        fail("P4 parser repair must not read prediction content", problems)
    if mapping.get("parser_repair_scope") != "PATH_SEMANTICS_ONLY":
        fail("P4 parser repair scope mismatch", problems)
    if mapping.get("grid_integrity_pass") is not True:
        fail("P4 repaired mapping grid integrity failed", problems)
    if len(mapping.get("mapping", [])) != 90:
        fail("P4 repaired mapping must contain 90 cases", problems)
    if audit.get("parse_pass_cases") != 90 or audit.get("parse_fail_cases") != 0:
        fail("P4 repaired parser audit must be 90/90 PASS", problems)
    if audit.get("prediction_bundle_sha256") != PRED_SHA:
        fail("P4 repaired parser audit prediction hash mismatch", problems)

    # E. Confirmatory score-only result and freeze.
    result = load_json("data/p4/GATE3D2_RE2TT_CONFIRMATORY_RESULTS.json")
    receipt = load_json("data/p4/GATE3D2_RESULT_FREEZE_RECEIPT.json")
    if result.get("status") != "CONFIRMATORY_SCORE_ONLY_COMPLETE" or result.get("n_cases") != 90:
        fail("P4 confirmatory result status/denominator mismatch", problems)
    if result.get("prediction_bundle_sha256") != PRED_SHA or result.get("gold_mapping_sha256") != GOLD_SHA:
        fail("P4 confirmatory lineage hash mismatch", problems)
    ep = result.get("primary_endpoints", {})
    expected_ep = {
        "exact_source_entitlement_n": 2,
        "exact_selective_correct_n": 2,
        "exact_selective_accuracy": 1.0,
        "false_exact_entitlement_events_n": 0,
        "UNDERDETERMINED_n": 83,
        "ABSTAIN_n": 5,
        "HOLD_n": 0,
        "K2_status": "DISABLED_NA",
    }
    for k, v in expected_ep.items():
        if ep.get(k) != v:
            fail(f"P4 endpoint {k} mismatch: {ep.get(k)!r} != {v!r}", problems)
    if result.get("post_gold_tuning_permitted") is not False:
        fail("P4 post-Gold tuning must be false", problems)
    if receipt.get("prediction_bundle_sha256") != PRED_SHA or receipt.get("gold_mapping_sha256") != GOLD_SHA:
        fail("P4 result receipt lineage mismatch", problems)
    if receipt.get("result_json_sha256") != RESULT_SHA or receipt.get("case_score_csv_sha256") != CASE_SCORE_SHA:
        fail("P4 result receipt output hashes mismatch", problems)
    if receipt.get("post_gold_tuning_permitted") is not False:
        fail("P4 result receipt post-Gold tuning must be false", problems)

    # F. Case score denominator.
    with (ROOT / "data/p4/GATE3D2_RE2TT_CASE_LEVEL_SCORE.csv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 90:
        fail(f"P4 case-level score must contain 90 rows, got {len(rows)}", problems)

    # G. Specification reconstructibility evidence and boundary.
    recon = (ROOT / "reconstruction/WH_JSS_INDEPENDENT_RECONSTRUCTION_AUDIT_V0.1.md").read_text(encoding="utf-8")
    for required in (
        "Primitive input-normalization contract tests: **18/18 PASS**.",
        "**64 / 64 cases matched; 0 output mismatches.**",
        "Exact historical archived implementation ↔ JSS specification equivalence: **HOLD**",
        "External human/institutional third-party replication: **NOT CLAIMED**",
    ):
        if required not in recon:
            fail(f"Reconstruction audit missing required statement: {required}", problems)

    dic = load_json("reconstruction/WH_JSS_DECISION_INPUT_CONTRACT_V0.1.json")
    if dic.get("tri_state") != ["TRUE", "FALSE", "UNKNOWN"]:
        fail("Decision Input Contract tri-state mismatch", problems)
    if len(dic.get("primitive_predicates", [])) != 12:
        fail("Decision Input Contract must contain 12 primitive predicates", problems)
    required_fields = {
        "predicate_id", "input_evidence_fields", "data_type",
        "operator_or_categorical_rule", "threshold_or_allowed_set_if_applicable",
        "direction_or_polarity", "missingness_behavior", "integrity_precondition",
        "provenance_source", "effective_version",
        "calibration_or_reference_source_if_applicable",
    }
    if set(dic.get("pipeline_specific_predicate_contract_required_fields", [])) != required_fields:
        fail("Decision Input Contract required-field set mismatch", problems)

    if problems:
        print("ARRAY_V0.2.0_VERIFY = FAIL")
        for p in problems:
            print(" -", p)
        return 1

    print("ARRAY_V0.2.0_VERIFY = PASS")
    print("ARTIFACT_HASH_IDENTITY = PASS")
    print("P4_PRE_GOLD_FREEZE = PASS")
    print("P4_HISTORICAL_PARSER_HOLD_PRESERVED = PASS")
    print("P4_MAPPING_REPAIR_LINEAGE = PASS")
    print("P4_CONFIRMATORY_SCORE_ONLY = PASS")
    print("RECONSTRUCTIBILITY_EVIDENCE_IDENTITY = PASS")
    print("HISTORICAL_V0.1_EXECUTABLE_BYTECODE_IDENTITY = PASS")
    print("NOTE: this verifier does not claim clean-environment execution of the archived ZIP-internal scripts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
