# P1 Worked Examples and Faded Scaffolds

This repository is the public results and reproducibility package for a matched-token continued-pretraining experiment on worked examples and faded scaffolds.

It tests whether training on complete worked solutions or partial solution scaffolds improves bare-prompt mathematical problem solving relative to problem plus final-answer training at the same token budget.

## One-Minute Summary

All worked-example and scaffolded arms improved Pass@8 over the bare control on the final 39,155-item holdout.

The best arm was `fade_shuffled`, with Pass@8 of `18.21%`, compared with `13.49%` for `bare`.

The completed run does not support ordered fading as a beneficial mechanism.

All scaffolded arms had lower PassRatio@8 point estimates than `bare`, so the result supports a multi-sample capability gain rather than improved single-sample reliability.

## Research Question

Does training on complete worked examples or faded scaffolds improve unscaffolded mathematical problem solving more than final-answer-only training at the same continued-pretraining token budget?

The broad comparison is worked-example depth versus final-answer-only breadth.

The stricter schedule comparison is `fade_ordered` versus `fade_shuffled`.

## Hypotheses

### H1: Worked examples improve Pass@8 over bare problem-answer pairs.

Supported in this run.

All three worked-example or scaffolded arms beat `bare` on the main full-holdout Pass@8 metric.

### H2: Ordered fading improves on complete worked examples.

Not supported in this run.

The `fade_ordered - complete` Pass@8 difference was `+0.29` percentage points with a 95% family-cluster bootstrap interval of `[-0.65, +1.23]` percentage points.

### H3: Ordered fading improves on shuffled fading.

Not supported in this run.

`fade_shuffled` exceeded `fade_ordered` by `0.62` percentage points on Pass@8.

The source-pack roster audit does not independently establish the same-underlying-instance condition required for a clean causal schedule comparison.

## Final Results

| Arm | Training format | Pass@8 | PassRatio@8 |
| --- | --- | ---: | ---: |
| `bare` | Problem plus final answer only. | 13.49% | 5.11% |
| `complete` | Problem plus complete worked solution plus final answer. | 17.30% | 4.33% |
| `fade_ordered` | Faded solution scaffolds in decreasing-support order. | 17.59% | 4.52% |
| `fade_shuffled` | Faded solution scaffolds with schedule order shuffled within family. | 18.21% | 4.59% |

| Comparison | Pass@8 difference | 95% family-cluster bootstrap CI | Two-sided sign-flip p |
| --- | ---: | ---: | ---: |
| `complete - bare` | +3.81 pp | [+2.62, +5.04] pp | 0.0002 |
| `fade_ordered - bare` | +4.10 pp | [+2.96, +5.23] pp | 0.0002 |
| `fade_shuffled - bare` | +4.72 pp | [+3.57, +5.88] pp | 0.0002 |
| `fade_ordered - complete` | +0.29 pp | [-0.65, +1.23] pp | 0.5483 |
| `fade_ordered - fade_shuffled` | -0.62 pp | [-1.13, -0.11] pp | 0.0202 |

Pass@8 counts an item as solved when at least one of eight sampled completions is correct.

PassRatio@8 is the average fraction of the eight completions that are correct.

## Experimental Setup

| Setting | Value |
| --- | --- |
| Model factory | `olmo2_370M` |
| Base model | 370M-parameter OLMo2-compatible continued-pretraining checkpoint |
| Dataset | `hiyasvyas/worked-examples-metamath-v0` |
| Dataset revision | `3d16357860e33f4906d7d1440d133052d4115b01` |
| Planned budget | 200,000,000 tokens per arm |
| Scheduled budget | 200,278,016 tokens per arm |
| Total scheduled tokens | 801,112,064 across four arms |
| Training steps | 382 per arm |
| Global batch | 524,288 tokens |
| Sequence length | 2,048 |
| Optimizer | AdamW with learning rate `5e-5` and weight decay `0.01` |
| Learning-rate schedule | Cosine with 200 warmup steps and final ratio `0.1` |
| Precision and parallelism | bf16 parameters, fp32 reduction, FSDP |
| Compute | 2 H100 GPUs per active arm |
| Evaluation | 39,155 bare prompts across 1,393 family clusters |
| Sampling | 8 completions, temperature `0.7`, top-p `0.95`, max 512 new tokens |

## What This Shows

At this token budget and evaluation protocol, worked-solution and scaffolded training made it more likely that at least one of eight answers was correct on a bare held-out problem.

The result does not establish that a scheduled fading order adds value beyond using worked examples.

The result also does not establish improved single-sample answer reliability or generalization outside this math benchmark.

## Repository Contents

```text
.
|-- README.md
|-- SHA256SUMS
|-- data/
|   |-- README.md
|   `-- dataset_manifest.json
|-- docs/
|   |-- hypothesis_context.md
|   `-- reproducibility.md
|-- models/
|   |-- README.md
|   `-- model_summary.json
|-- results/
|   |-- artifact_index.md
|   |-- fullholdout_summary.md
|   `-- metrics_summary.json
`-- scripts/
    |-- README.md
    |-- analyze_passn_eval.py
    `-- score_holdout_passn.py
```

`data/` identifies the canonical public data pack and records its integrity anchors.

`models/` records the model identity without distributing access-controlled checkpoint files or locations.

`results/` contains the primary aggregate metrics and statistical comparisons.

`scripts/` contains portable scoring and paired family-cluster analysis helpers.

## Scope of This Release

This release intentionally excludes raw prediction JSONL files, model binaries, local paths, cluster launch scripts, internal run tracking links, and storage locations.

The underlying data pack is already publicly distributed by its maintainers.

The base and final checkpoints are not redistributed here.

## Reproduce the Analysis

Retrieve the canonical data pack at the pinned revision in [data/README.md](data/README.md).

Use a compatible OLMo-core checkout to regenerate predictions from independently obtained checkpoints.

Then use the documented commands in [scripts/README.md](scripts/README.md) to score predictions and run paired family-cluster analysis.

See [docs/reproducibility.md](docs/reproducibility.md) for the complete public reproduction boundary.

## Limitations and Next Steps

This is one base checkpoint and one training seed.

It does not measure error-type changes or performance outside the evaluated problem distribution. 51 of the 1,393 holdout families also appear in the training build.

The next experiment should use a roster-verified ordered and shuffled pair, add at least one training seed, and re-run the analysis without the 51 holdout families that also appear in training.
