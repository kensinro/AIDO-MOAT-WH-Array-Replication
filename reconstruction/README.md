# Specification Reconstructibility Replication Layer

Status: EXACT ARTIFACTS RECOVERED / HASH-VERIFIED / INTEGRATED VERIFIER ADDED

This directory contains exact supporting artifacts for the manuscript's specification-level reconstructibility claims.

## Reviewer command

From repository root:

```bash
python scripts/verify_array_v0_2_0.py
```

The integrated verifier checks byte identity of the recovered governed packets and verifies the published audit/contract invariants that can be tested without regenerating scientific inference.

## Recovered governed checks

- 20/20 canonical decision-edge cases — contained in executable reconstruction packet
- 9,216/9,216 abstract state-space/property checks — contained in executable reconstruction packet
- 18/18 decision-input normalization checks
- 64/64 specification-separated second-path cases
- agreement across 14 load-bearing output fields
- prediction SHA-256 frozen before reference comparison

Exact package identities:

- `WH_JSS_EXECUTABLE_RECONSTRUCTION_V0.2.zip`
  SHA-256 `879dd0f86454ea67e63e81592c5914ff1ed7aa4d1d82e5a8ecf2dd8abada52ec`
- `WH_JSS_INDEPENDENT_RECONSTRUCTION_PACKET_V0.1.zip`
  SHA-256 `7581b4fc7744fa5c872622edd9b6c2b9a047a69ee97bfc8ace843d14e45eae1d`
- `WH_JSS_DECISION_INPUT_CONTRACT_V0.1.json`
  SHA-256 `82065a9b5af20dfeeb6e4931580bc1e1568a29fbeb1c0c6204b0fa2eb6faa699`

## Required boundary

These checks support executability and reconstructibility of the published decision contract. They do not prove:

- field performance;
- external personnel/institutional replication;
- historical source-code identity;
- production safety/effectiveness.

Historical implementation-to-published-specification exact equivalence remains HOLD.

## Remaining execution work

The exact packet bytes are present and hash-bound, but a fresh clean-environment execution of the ZIP-internal scripts is not yet claimed by this README. That gate remains explicit until independently run and recorded.
