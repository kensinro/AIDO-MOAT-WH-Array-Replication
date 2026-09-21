# WH JSS Independent Reconstruction / Evaluability Audit V0.1

**Date:** 2026-08-24  
**Basis:** JSS Main V0.5.3 + SI V1.2 only for decision semantics; historical archived WH implementation was not consulted by the blind reconstruction path.  
**Purpose:** test whether the published decision contract can be reconstructed without author-intent rescue and identify any remaining cross-surface ambiguity before JSS adaptation.

## Final disposition

**EVALUABILITY PASS — SPECIFICATION-SEPARATED RECONSTRUCTION**

- Primitive input-normalization contract tests: **18/18 PASS**.
- Fresh blinded normalized decision cases: **64/64 matched** across 14 scientific/governance output fields against the pre-existing clean-room reference adjudicator after prediction hash freeze.
- Worked state ordering: **PASS** — no topology/source-set construction is entitled before abnormality is established.
- Main ↔ SI ↔ reference-package vocabulary synchronization: **PASS AFTER REPAIR**.
- Frozen P1–P3 empirical results changed: **NO**.
- Exact historical archived implementation ↔ JSS specification equivalence: **HOLD** — authoritative archived package not recovered.
- External human/institutional third-party replication: **NOT CLAIMED**. This audit establishes implementation-separated reconstructibility, not personnel independence.

## Reconstruction protocol

1. Treat Main V0.5.3 and SI V1.2 as the scientific specification.
2. Identify the published decision order: integrity/admissibility → detection → structural descriptor/minimal source sets → target-specific sufficiency → topology compatibility/known-primitive decomposition → diagnostic/resolution state → localization → repair entitlement → Human authorization → re-audit closure → registry promotion → append-only trace.
3. Implement a second adjudicator without importing or calling the pre-existing JSS reference adjudicator.
4. Generate 64 fresh normalized cases under fixed seed 24082026; remove expected verdicts from the evaluator input.
5. Execute the second adjudicator and freeze its prediction file by SHA-256 before comparison.
6. Only after freeze, score the predictions against the pre-existing clean-room reference adjudicator over 14 load-bearing output fields.
7. Separately test primitive evidence normalization functions for contract aggregation, direct-source status, graph reachability, threshold/categorical evaluation, primitive decomposition, and structural residual generation.

## Blind reconstruction result

**64 / 64 cases matched; 0 output mismatches.**

Fields compared:

- diagnostic_disposition
- topology_label
- known_space_compatible
- resolution_state
- compatible_topologies
- unresolved_topologies
- exact_localization
- candidate_source_sets
- inspection_state
- repair_recommendation_entitled
- repair_target
- repair_execution_authorized
- closure_state
- registry_promotion_state

The blinded prediction file was frozen before scoring. See `PREDICTION_FREEZE_SHA256.txt`.

## Defects exposed before final freeze

### IR-01 — raw evidence → primitive-predicate boundary was under-specified
Main/SI were sufficient to reconstruct verdicts once primitive predicates had already been evaluated, but did not fully enumerate the contract that converts raw pipeline evidence into those three-valued predicates.

**Repair:** add a formal Decision Input Contract. Every pipeline-specific predicate must declare evidence fields, operator/categorical rule, threshold/allowed set where applicable, direction/polarity, missingness behavior, integrity precondition, provenance/version, and calibration/reference source. WH core does not invent universal thresholds; it consumes the auditable output of these frozen external contracts.

### IR-02 — Human-Gate authorization token drift
Main used `AUTHORIZE_SCOPE`; reference package V0.1 used `AUTHORIZE`.

**Repair:** canonical repair Human-Gate input is `AUTHORIZE_SCOPE` (with REFUSE, NARROW_SCOPE, REQUEST_MORE_EVIDENCE). Reference package upgraded to V0.2.

### IR-03 — registry-promotion state-label drift
SI used `PROMOTED_BY_HUMAN_GATE`; reference package V0.1 serialized `AUTHORIZED_PROSPECTIVE_VERSION` and grammatical variants `REFUSE_PROMOTION` / `DEFER_PROMOTION`.

**Repair:** canonical outputs are `PROMOTED_BY_HUMAN_GATE`, `REFUSED_PROMOTION`, and `DEFERRED_PROMOTION`.

### IR-04 — closure spelling drift
Narrative prose used `REOPENED/NOT_RESOLVED` while executable/SI state used `REOPENED_NOT_RESOLVED`.

**Repair:** use `REOPENED_NOT_RESOLVED` whenever the formal state token is intended; ordinary prose may say “reopened/not resolved” only when not representing the machine state.

### IR-05 — evaluator attempted premature source-set serialization
The first blind evaluator draft initialized candidate source sets before the detection gate. Algorithm 1 specifies structural-descriptor construction only after abnormality is established.

**Repair:** evaluator corrected before prediction freeze. CLEAN and detection-insufficient early exits do not claim constructed source sets.

## Input-normalization result

The new normalization contract was exercised on 18 canonical predicate-level tests:

- hard-contract PASS/FAIL/UNKNOWN aggregation;
- direct-source TRUE/FALSE/UNKNOWN conversion;
- directed dependency reachability TRUE/FALSE/UNKNOWN;
- numerical threshold PASS/FAIL/UNKNOWN;
- categorical acceptance PASS/FAIL;
- known-primitive decomposition complete/incomplete;
- structural residual absent/present.

Result: **18/18 PASS**.

## Interpretation

The audit closes the evaluator question at the **published specification layer**: a separate implementation path can reproduce the same governed outputs from the same normalized inputs without guessing hidden precedence or author intent. The audit also makes explicit the boundary between pipeline-specific evidence normalization and WH core adjudication.

It does **not** prove that the archived historical software that generated P1–P3 is exactly equivalent to the JSS specification. That stronger provenance claim remains HOLD until authoritative archive recovery, hash verification, rule-to-function mapping, and frozen-case regression.
