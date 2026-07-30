# Reproducibility Boundary

## What This Release Supports

This release supports independent inspection of the result, verification of public data hashes, re-scoring of prediction files, and re-running the paired family-cluster analysis.

It also records the training budget, optimizer, scheduler, sequence length, evaluation sampling settings, and the base checkpoint hash used by the experiment.

## What Is Required for an Exact Rerun

An exact training rerun requires the pinned public data pack, a compatible OLMo-core checkout, and an authorized copy of the base checkpoint matching the recorded SHA-256 hash.

The public package intentionally does not provide storage locations, credentials, or cluster-specific launch instructions.

## Analysis Reproduction

1. Retrieve the data pack at the revision in [../data/README.md](../data/README.md).
2. Verify `eval/holdout_bare.jsonl` against the recorded SHA-256.
3. Produce aligned prediction JSONL files with eight `gens` strings per holdout item.
4. Run [../scripts/score_holdout_passn.py](../scripts/score_holdout_passn.py) once for each arm.
5. Run [../scripts/analyze_passn_eval.py](../scripts/analyze_passn_eval.py) with the four aligned prediction files.

The released result used a family-cluster bootstrap and family-cluster sign-flip permutation test with `5,000` draws each.

## Scope Limitations

The release records one seed and one base checkpoint.

It does not provide a checkpoint distribution, a trained-model license, or an audit of the ordered-versus-shuffled source roster beyond the limitations stated in the results.
