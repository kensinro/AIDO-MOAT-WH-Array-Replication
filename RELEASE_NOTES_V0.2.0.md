# V0.2.0-ARRAY public replication release

This release provides the public reviewer-facing replication surface for:

**Evidence-Bounded Supervisory Diagnosis of Compositional Failures in Modular Software Systems**

## Included

- frozen Protocols 1–3 and R³ evidence/reproduction code;
- Protocol 4 RCAEval RE2-TT governed artifacts and endpoint recomputation;
- specification-reconstructibility packets;
- exact historical V0.1 compiled adjudicator used for the clean 64/64 historical re-score;
- public CI for baseline, Protocol 4, and reconstruction checks;
- SHA-256 governed-artifact manifest.

## Headline Protocol 4 recomputation

- N = 90
- exact-source entitlement = 2/90
- selective correctness = 2/2
- false exact-source entitlement = 0/90
- UNDERDETERMINED = 83/90
- ABSTAIN = 5/90
- topology = 90/90 TOPOLOGY_UNDERDETERMINED

## Reconstructibility

- 20/20 canonical cases
- 9,216/9,216 property checks
- 18/18 normalization checks
- exact 64-case blind-prediction regeneration
- 64/64 historical re-score across 14 load-bearing fields

## Boundary

The original historical V0.1 source .py file was not recovered. The exact surviving compiled V0.1 executable bytecode is included and clean-executed.

This package supports reproducibility and auditability; it does not establish production effectiveness, broad RCA coverage, autonomous-repair safety, or complete historical implementation ↔ revised-specification equivalence.

Public availability does not grant reuse rights beyond those stated in LICENSE.
