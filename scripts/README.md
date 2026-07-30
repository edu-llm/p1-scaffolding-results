# Analysis Scripts

The scripts in this directory are portable analysis helpers.

They do not submit jobs, access remote storage, read local credentials, or report to an experiment-tracking service by default.

## Prerequisite

Both helpers use the `holdout_passn.py` module from a compatible OLMo-core checkout.

Set `OLMO_REPO_ROOT` to that checkout or run the commands from its repository root.

## Score One Arm

```bash
python scripts/score_holdout_passn.py \
  --holdout /path/to/eval/holdout_bare.jsonl \
  --predictions /path/to/bare_predictions.jsonl \
  --pass-n 8 \
  --output /path/to/bare_metrics.json
```

Each prediction row must contain a `gens` array with eight generated strings.

The prediction rows must match the holdout order exactly.

## Analyze Four Arms

```bash
python scripts/analyze_passn_eval.py \
  --holdout /path/to/eval/holdout_bare.jsonl \
  --arm bare=/path/to/bare_predictions.jsonl \
  --arm complete=/path/to/complete_predictions.jsonl \
  --arm fade_ordered=/path/to/fade_ordered_predictions.jsonl \
  --arm fade_shuffled=/path/to/fade_shuffled_predictions.jsonl \
  --pass-n 8 \
  --bootstrap-samples 5000 \
  --permutation-samples 5000 \
  --output-json /path/to/analysis.json \
  --output-md /path/to/analysis.md
```

The analysis uses family IDs from the holdout records when present.
