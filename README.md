# AIDO-MOAT-WH — Array Replication Package V0.2.1

Public replication package for the manuscript:

**Evidence-Bounded Supervisory Diagnosis of Compositional Failures in Modular Software Systems**

This repository is a clean reviewer-facing release surface derived from the governed AIDO-MOAT-WH reproducibility lineage. It intentionally excludes internal project history, working notes, submission-management records, and unrelated implementation material.

## Quick start

Install the frozen baseline package and run the original Protocol 1–3 / R³ checks:

```bash
python -m pip install -e ".[test]"
python -m wh_reference reproduce --data-root data --output artifacts
pytest -q
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
- `MANIFEST_SHA256_ARRAY_V0.2.1.json`
- `CODE_AVAILABILITY.md`
- `REPRODUCIBILITY.md`

## License

See `LICENSE`. Public availability does not by itself grant reuse rights beyond those stated in the license file.


## V0.2.1 release-identity repair

V0.2.1 binds the public replication release to the exact current Array submission artifacts without changing the scientific payload:

- Main V1.5 SHA-256: `9a59c6d735e70d759a9ec5997b1dd5124ecbf7054b48bc411472fe7d67551357`
- SI V1.5 SHA-256: `466d7f24aa1af36955e29f678e26b51c2e0a1fcefbcace139cdb548a75717724`
- Highlights V1.2 SHA-256: `48b43b9db9b17d0e502b34af5adfd5bffb56cb9e53b06220cd15e04a967f4e1b`

The previous Zenodo V0.2.0 DOI is `10.5281/zenodo.22879998`. A new Zenodo version DOI will be bound after the V0.2.1 GitHub release is published and ingested.
