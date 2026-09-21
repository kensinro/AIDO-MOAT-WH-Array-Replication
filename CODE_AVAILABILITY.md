# Code and replication-package availability — Array V0.2.0

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
