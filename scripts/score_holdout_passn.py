#!/usr/bin/env python3
"""Score worked-example predictions with an explicit --pass-n argument."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--holdout", type=Path, required=True)
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--pass-n", type=int, default=8)
    parser.add_argument("--max-items", type=int, default=0)
    parser.add_argument("--output", type=Path, required=True)
    return parser


def _add_holdout_passn_to_path() -> None:
    candidates: list[Path] = []
    olmo_root = os.environ.get("OLMO_REPO_ROOT")
    if olmo_root:
        candidates.append(Path(olmo_root) / "src/scripts/hypothesis/worked_examples")
    candidates.append(Path.cwd() / "src/scripts/hypothesis/worked_examples")
    for entry in os.environ.get("PYTHONPATH", "").split(os.pathsep):
        if entry:
            candidates.append(Path(entry) / "scripts/hypothesis/worked_examples")

    for candidate in candidates:
        if (candidate / "holdout_passn.py").is_file():
            sys.path.insert(0, str(candidate))
            return


def main() -> int:
    args = _build_parser().parse_args()
    if args.pass_n < 1:
        raise ValueError("--pass-n must be positive")

    _add_holdout_passn_to_path()
    from holdout_passn import load_holdout, score_generations

    items = load_holdout(args.holdout, max_items=args.max_items)
    generations: list[list[str]] = []
    with args.predictions.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            gens = [str(item) for item in row["gens"][: args.pass_n]]
            if len(gens) != args.pass_n:
                raise ValueError(
                    f"prediction row {len(generations) + 1} has {len(gens)} generations, "
                    f"expected {args.pass_n}"
                )
            generations.append(gens)
    if len(generations) != len(items):
        raise ValueError(f"prediction rows {len(generations)} != holdout items {len(items)}")

    metrics = score_generations(items, generations)
    payload = {
        "eval/pass_at_n": metrics["eval/pass_at_n"],
        "eval/pass_ratio_at_n": metrics["eval/pass_ratio_at_n"],
        "eval/n_items": metrics["eval/n_items"],
        "eval/pass_n": float(args.pass_n),
        "holdout": str(args.holdout),
        "predictions": str(args.predictions),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
