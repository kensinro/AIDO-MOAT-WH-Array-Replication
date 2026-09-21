# Protocol 4 — RCAEval RE2-TT Replication Layer

Status: EXACT ARTIFACTS RECOVERED / HASH-VERIFIED / INTEGRATED VERIFIER ADDED

This directory contains exact, already-existing Protocol 4 artifacts recovered from the governed source lineage. No predictions, thresholds, or scientific conclusions were regenerated during this repair.

## Reviewer command

From repository root:

```bash
python scripts/verify_array_v0_2_0.py
```

The verifier checks exact SHA-256 identity, pre-Gold freeze state, preservation of the historical 90/90 parser HOLD, deterministic path-semantics repair, confirmatory score-only lineage, and the 90-row case-level score table.

## Frozen confirmatory result

- denominator: 90
- exact-source entitlement: 2/90
- selective correctness: 2/2
- false exact-source entitlement: 0/90
- UNDERDETERMINED: 83/90
- ABSTAIN: 5/90
- topology: 90/90 TOPOLOGY_UNDERDETERMINED
- multi-candidate exact-source escalation K2: DISABLED

## Required lineage

The all-90 prediction bundle was frozen before Gold opening. The first Gold-opening attempt produced a systematic path-pattern parser HOLD and predictions remained immutable. A deterministic path-semantics-only mapping repair was then applied before score-only comparison.

Key immutable identifiers:

- pre-Gold prediction bundle SHA-256:
  `5d0cc805eefb353935b5b277f62610850f0f23e1e4a11bd64014b231d43e09f5`
- repaired Gold mapping SHA-256:
  `7a2431b7163809bc6abb9a38daf54fef1e4b7cccf37f35a50d30a9d7b3d281cc`
- confirmatory result SHA-256:
  `ffb6f9a1d9d82782b4afc9ed6eaf935cdb1e8ef85b814ce06a66fb294dd703db`
- case-level score SHA-256:
  `8af4f019135e6197bee54dab3d6471e99a8676884beb9eefedf9e3a9debcadd3`

## Historical HOLD preservation

`GATE3D_GOLD_PATH_PARSE_HOLD.json` is intentionally retained. The repair must not erase the first 90/90 `GOLD_PATH_PATTERN_NOT_UNIQUE` failure.

## Claim boundary

This is a selective exact-source entitlement witness on a controlled injected-failure third-party benchmark. It is not broad RCA coverage, production validation, or a leaderboard claim.

## Still not claimed

- post-Gold tuning
- production-incident validation
- broad RCA accuracy
- future untouched status for RE2-TT
