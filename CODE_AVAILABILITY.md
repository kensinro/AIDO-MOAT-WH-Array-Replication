# Code and replication-package availability — Array V0.2.1

This public repository is the reviewer-facing reference and replication package for the Array manuscript candidate **Evidence-Bounded Supervisory Diagnosis of Compositional Failures in Modular Software Systems**.

It supports the governed checks reported in the manuscript, including Protocol 4 endpoint recomputation and specification reconstructibility.

Reviewer-facing commands:

```bash
python scripts/verify_array_v0_2_0.py
python scripts/recompute_p4_endpoints.py
```

The package includes the exact surviving compiled historical V0.1 reference adjudicator bytecode embedded in the recovered executable reconstruction packet. That bytecode is hash-bound and has been clean-executed for the historical 64/64 score. The original historical V0.1 source `.py` file remains unrecovered, and complete historical implementation ↔ revised specification equivalence is not claimed.

Public availability is now active for reproducibility review. Public availability does not grant reuse rights beyond those stated in `LICENSE`.

The public package is archived at Zenodo: DOI 10.5281/zenodo.22879998 (https://doi.org/10.5281/zenodo.22879998). Array portal binding remains a separate submission step.


## V0.2.1 manuscript binding

This release-identity repair binds the unchanged replication payload to the exact current submission artifacts:

- Main V1.5: `9a59c6d735e70d759a9ec5997b1dd5124ecbf7054b48bc411472fe7d67551357`
- SI V1.5: `466d7f24aa1af36955e29f678e26b51c2e0a1fcefbcace139cdb548a75717724`
- Highlights V1.2: `48b43b9db9b17d0e502b34af5adfd5bffb56cb9e53b06220cd15e04a967f4e1b`

The V0.2.1 Zenodo version DOI is pending publication of the corresponding GitHub release. The previous V0.2.0 DOI remains `10.5281/zenodo.22879998`.
