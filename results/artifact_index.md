# Artifact Index

## Included

- [metrics_summary.json](metrics_summary.json) contains the primary arm metrics and paired family-cluster comparisons.
- [fullholdout_summary.md](fullholdout_summary.md) provides a human-readable account of the primary evaluation.
- [../data/dataset_manifest.json](../data/dataset_manifest.json) records the public data-pack files and hashes used by the run.
- [../models/model_summary.json](../models/model_summary.json) records the model factory and a base-checkpoint integrity anchor.
- [../docs/hypothesis_context.md](../docs/hypothesis_context.md) describes the hypothesis and its evidence boundary.

## Intentionally Excluded

- Raw completion files.
- Checkpoint binaries.
- Local filesystem paths.
- Cluster-specific launch and recovery scripts.
- Execution identifiers and run-tracking links.
- Access-controlled storage references.

The exclusions preserve the public evidence needed to interpret and reproduce the analysis while avoiding publication of private operational metadata.
