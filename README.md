# AIDO-MOAT-WH — Array Replication Package V0.2.0

Public replication package for the manuscript:

**Evidence-Bounded Supervisory Diagnosis of Compositional Failures in Modular Software Systems**

This repository is a clean reviewer-facing release surface derived from the governed AIDO-MOAT-WH reproducibility lineage. It intentionally excludes internal project history, working notes, submission-management records, and unrelated implementation material.

## Quick start

Install the frozen baseline package and run the original Protocol 1–3 / R³ checks:

```bash
python -m pip install -e ".[test]"
python -m wh_reference reproduce --data-root data --output artifacts
pytest -q
python -m wh_reference validate --repo-root .
```

Run the Array-specific governed checks:

```bash
python scripts/verify_array_v0_2_0.py
python scripts/recompute_p4_endpoints.py
```

## Protocol 4 expected recomputation

The second command recomputes the headline endpoints from the frozen case-level score table and checks them against the frozen confirmatory result:

- N = 90
- exact-source entitlement = 2/90
- selective correctness = 2/2, conditional on entitlement
- false exact-source entitlement = 0/90
- UNDERDETERMINED = 83/90
- ABSTAIN = 5/90
- case-level HOLD = 0/90
- topology = 90/90 TOPOLOGY_UNDERDETERMINED

## Specification reconstructibility

The governed reconstruction materials support:

- 20/20 canonical decision-edge cases
- 9,216/9,216 generated property checks
- 18/18 input-normalization checks
- exact regeneration of the frozen 64-case blind-prediction JSON
- 64/64 historical re-score across 14 load-bearing fields using the exact surviving V0.1 CPython-3.13 compiled adjudicator

The original historical V0.1 source `.py` file has not been recovered. The surviving compiled V0.1 executable bytecode is hash-bound and clean-executed. Complete historical implementation ↔ revised published-specification equivalence is not claimed.

## Claim boundary

This package supports result reproducibility and auditability. It does **not** establish:

- production effectiveness
- autonomous repair safety
- broad RCA coverage
- external personnel/institutional replication
- unrestricted reproducibility of the complete WH product implementation

## Release integrity

The public repository is an append-only clean release surface. The historical/private development repository is intentionally not exposed.

See:

- `MANIFEST_SHA256.json`
- `MANIFEST_SHA256_ARRAY_V0.2.0.json`
- `CODE_AVAILABILITY.md`
- `REPRODUCIBILITY.md`

## License

See `LICENSE`. Public availability does not by itself grant reuse rights beyond those stated in the license file.
