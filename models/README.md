# Model Card

## Scope

This repository is a results package and does not distribute checkpoint binaries.

It records a publication-safe model identity and an integrity anchor for the base checkpoint used in the experiment.

## Architecture

Model factory: `olmo2_370M`.

The training runs started from a 370M-parameter OLMo2-compatible continued-pretraining checkpoint.

The final checkpoint for every arm was `step382`.

## Distribution Boundary

The base checkpoint location and final checkpoint binaries are intentionally omitted from this release.

They were not published through a durable public model registry at release time.

The model hash in [model_summary.json](model_summary.json) permits verification by an authorized holder without disclosing a storage location.

## Use Limitation

These checkpoints were research artifacts for a controlled math experiment.

They are not presented as general-purpose mathematical reasoning models or deployment-ready systems.
