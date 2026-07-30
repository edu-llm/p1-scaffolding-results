# Full-Holdout Evaluation Summary

## Evaluation Contract

The primary evaluation used `39,155` bare math prompts from `eval/holdout_bare.jsonl`.

The prompts span `1,393` family clusters.

Each arm generated eight completions per prompt using temperature `0.7`, top-p `0.95`, and at most `512` new tokens.

The evaluation supplied only the bare problem and no worked solution or scaffold.

## Arm Metrics

| Arm | Pass@8 | PassRatio@8 | Prediction rows |
| --- | ---: | ---: | ---: |
| `bare` | 13.49% | 5.11% | 39,155 |
| `complete` | 17.30% | 4.33% | 39,155 |
| `fade_ordered` | 17.59% | 4.52% | 39,155 |
| `fade_shuffled` | 18.21% | 4.59% | 39,155 |

## Family-Cluster Comparisons

| Comparison | Metric | Difference | 95% cluster bootstrap CI | Two-sided p |
| --- | --- | ---: | ---: | ---: |
| `complete - bare` | Pass@8 | +3.81 pp | [+2.62, +5.04] pp | 0.0002 |
| `complete - bare` | PassRatio@8 | -0.78 pp | [-1.41, -0.16] pp | 0.0122 |
| `fade_ordered - bare` | Pass@8 | +4.10 pp | [+2.96, +5.23] pp | 0.0002 |
| `fade_ordered - bare` | PassRatio@8 | -0.59 pp | [-1.21, -0.00] pp | 0.0538 |
| `fade_ordered - complete` | Pass@8 | +0.29 pp | [-0.65, +1.23] pp | 0.5483 |
| `fade_ordered - fade_shuffled` | Pass@8 | -0.62 pp | [-1.13, -0.11] pp | 0.0202 |
| `fade_shuffled - bare` | Pass@8 | +4.72 pp | [+3.57, +5.88] pp | 0.0002 |

## Interpretation

All worked-example or scaffolded arms beat `bare` on the final Pass@8 metric.

The highest Pass@8 arm was `fade_shuffled` at `18.21%`.

The complete and scaffolded formats did not improve average single-sample correctness over `bare` in this run.

The evidence does not support a causal benefit for ordered fading because the source roster was not independently audited to establish the required same-underlying-instance condition.
