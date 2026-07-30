#!/usr/bin/env python3
"""Analyze worked-example Pass@N evals with paired family-cluster statistics."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import random
import sys
from typing import Any


MetricRows = dict[str, list[float]]


def _add_holdout_passn_to_path(olmo_repo: Path | None) -> None:
    candidates: list[Path] = []
    if olmo_repo is not None:
        candidates.append(olmo_repo / "src/scripts/hypothesis/worked_examples")
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


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--holdout", type=Path, required=True)
    parser.add_argument("--arm", action="append", default=[], help="ARM=predictions.jsonl")
    parser.add_argument("--pass-n", type=int, default=8)
    parser.add_argument("--max-items", type=int, default=0)
    parser.add_argument("--olmo-repo", type=Path, default=None)
    parser.add_argument("--bootstrap-samples", type=int, default=5000)
    parser.add_argument("--permutation-samples", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=20260728)
    parser.add_argument("--examples-per-comparison", type=int, default=5)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    return parser


def _load_jsonl(path: Path, *, max_items: int = 0) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            rows.append(json.loads(line))
            if max_items and len(rows) >= max_items:
                break
    return rows


def _load_generations(path: Path, pass_n: int) -> list[list[str]]:
    rows: list[list[str]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            gens = [str(item) for item in row["gens"][:pass_n]]
            if len(gens) != pass_n:
                raise ValueError(f"{path}: expected {pass_n} gens, got {len(gens)}")
            rows.append(gens)
    return rows


def _mean(values: list[float]) -> float:
    return sum(values) / max(len(values), 1)


def _quantile(sorted_values: list[float], q: float) -> float:
    if not sorted_values:
        return 0.0
    pos = q * (len(sorted_values) - 1)
    lo = int(pos)
    hi = min(lo + 1, len(sorted_values) - 1)
    frac = pos - lo
    return sorted_values[lo] * (1.0 - frac) + sorted_values[hi] * frac


def _first_correct(gens: list[str], flags: list[bool]) -> str | None:
    for gen, flag in zip(gens, flags):
        if flag:
            return gen
    return None


def _short(text: str, limit: int = 300) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."


def _cluster_indices(holdout_rows: list[dict[str, Any]]) -> dict[str, list[int]]:
    clusters: dict[str, list[int]] = {}
    for index, row in enumerate(holdout_rows):
        family = row.get("family_id") or row.get("original_question") or f"row_{index}"
        clusters.setdefault(str(family), []).append(index)
    return clusters


def _bootstrap_diff(
    rng: random.Random,
    clusters: dict[str, list[int]],
    left: list[float],
    right: list[float],
    samples: int,
) -> dict[str, float]:
    cluster_rows: list[tuple[float, int]] = []
    for indices in clusters.values():
        cluster_rows.append(
            (
                sum(left[index] - right[index] for index in indices),
                len(indices),
            )
        )
    observed = _mean([a - b for a, b in zip(left, right)])
    draws: list[float] = []
    for _ in range(samples):
        total = 0.0
        count = 0
        for _ in cluster_rows:
            cluster_sum, cluster_count = rng.choice(cluster_rows)
            total += cluster_sum
            count += cluster_count
        draws.append(total / max(count, 1))
    draws.sort()
    return {
        "diff": observed,
        "ci95_low": _quantile(draws, 0.025),
        "ci95_high": _quantile(draws, 0.975),
    }


def _cluster_signflip_p_value(
    rng: random.Random,
    clusters: dict[str, list[int]],
    left: list[float],
    right: list[float],
    samples: int,
) -> dict[str, float]:
    cluster_sums: list[float] = []
    total_count = 0
    for indices in clusters.values():
        cluster_sums.append(sum(left[index] - right[index] for index in indices))
        total_count += len(indices)
    observed_sum = sum(cluster_sums)
    observed = observed_sum / max(total_count, 1)
    abs_observed = abs(observed_sum)
    greater_equal = 0
    two_sided = 0
    for _ in range(samples):
        sampled_sum = 0.0
        for cluster_sum in cluster_sums:
            sampled_sum += cluster_sum if rng.random() < 0.5 else -cluster_sum
        if sampled_sum >= observed_sum:
            greater_equal += 1
        if abs(sampled_sum) >= abs_observed:
            two_sided += 1
    return {
        "one_sided_p_left_greater": (greater_equal + 1) / (samples + 1),
        "two_sided_p": (two_sided + 1) / (samples + 1),
    }


def _comparison_examples(
    holdout_rows: list[dict[str, Any]],
    generations: dict[str, list[list[str]]],
    flags: dict[str, list[list[bool]]],
    left: str,
    right: str,
    limit: int,
) -> dict[str, list[dict[str, Any]]]:
    def collect(want_left: bool, want_right: bool) -> list[dict[str, Any]]:
        output: list[dict[str, Any]] = []
        for index, row in enumerate(holdout_rows):
            left_pass = any(flags[left][index])
            right_pass = any(flags[right][index])
            if left_pass != want_left or right_pass != want_right:
                continue
            output.append(
                {
                    "index": index,
                    "family_id": row.get("family_id"),
                    "type": row.get("type"),
                    "gold": row.get("final_answer"),
                    "prompt": _short(str(row.get("prompt") or row.get("question") or "")),
                    f"{left}_first_correct": _short(_first_correct(generations[left][index], flags[left][index]) or ""),
                    f"{right}_first_correct": _short(_first_correct(generations[right][index], flags[right][index]) or ""),
                    f"{left}_first_generation": _short(generations[left][index][0]),
                    f"{right}_first_generation": _short(generations[right][index][0]),
                }
            )
            if len(output) >= limit:
                break
        return output

    return {
        f"{left}_passes_{right}_fails": collect(True, False),
        f"{right}_passes_{left}_fails": collect(False, True),
    }


def _write_markdown(report: dict[str, Any], output: Path) -> None:
    lines: list[str] = []
    lines.append("# Worked Examples Eval Analysis")
    lines.append("")
    lines.append(f"Items: {report['n_items']}")
    lines.append(f"Families: {report['n_families']}")
    lines.append(f"Pass@N: {report['pass_n']}")
    lines.append("")
    lines.append("## Arm Metrics")
    lines.append("")
    lines.append("| Arm | Pass@8 | PassRatio@8 |")
    lines.append("|---|---:|---:|")
    for arm, metrics in report["arms"].items():
        lines.append(
            f"| `{arm}` | {metrics['pass_at_n']:.4f} | {metrics['pass_ratio_at_n']:.5f} |"
        )
    lines.append("")
    lines.append("## Paired Comparisons")
    lines.append("")
    lines.append("| Comparison | Metric | Diff | 95% cluster bootstrap CI | one-sided p | two-sided p |")
    lines.append("|---|---|---:|---:|---:|---:|")
    for key, metrics in report["comparisons"].items():
        for metric_name, stats in metrics.items():
            lines.append(
                "| "
                f"`{key}` | `{metric_name}` | {stats['diff']:.5f} | "
                f"[{stats['ci95_low']:.5f}, {stats['ci95_high']:.5f}] | "
                f"{stats['one_sided_p_left_greater']:.4f} | {stats['two_sided_p']:.4f} |"
            )
    lines.append("")
    lines.append("## Example Audits")
    lines.append("")
    for key, examples in report["examples"].items():
        lines.append(f"### {key}")
        lines.append("")
        for direction, rows in examples.items():
            lines.append(f"#### {direction}")
            lines.append("")
            if not rows:
                lines.append("No examples found.")
                lines.append("")
                continue
            for row in rows:
                lines.append(f"- index `{row['index']}`, family `{row.get('family_id')}`, gold `{row.get('gold')}`")
                lines.append(f"  Prompt: {row['prompt']}")
                for subkey, value in row.items():
                    if subkey.endswith("_first_correct") and value:
                        lines.append(f"  {subkey}: {value}")
                lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    args = _build_parser().parse_args()
    if not args.arm:
        raise ValueError("Provide at least one --arm ARM=predictions.jsonl")
    _add_holdout_passn_to_path(args.olmo_repo)
    from holdout_passn import is_correct, load_holdout

    holdout_rows = _load_jsonl(args.holdout, max_items=args.max_items)
    items = load_holdout(args.holdout, max_items=args.max_items)
    if len(holdout_rows) != len(items):
        raise ValueError("raw holdout row count does not match parsed holdout item count")

    generations: dict[str, list[list[str]]] = {}
    flags: dict[str, list[list[bool]]] = {}
    per_metric: dict[str, MetricRows] = {}
    for arm_spec in args.arm:
        arm, path_text = arm_spec.split("=", 1)
        generations[arm] = _load_generations(Path(path_text), args.pass_n)
        if len(generations[arm]) != len(items):
            raise ValueError(f"{arm}: prediction rows {len(generations[arm])} != items {len(items)}")
        flags[arm] = [
            [is_correct(gen, item.final_answer) for gen in gens]
            for item, gens in zip(items, generations[arm])
        ]
        per_metric[arm] = {
            "pass_at_n": [1.0 if any(row) else 0.0 for row in flags[arm]],
            "pass_ratio_at_n": [sum(1.0 for value in row if value) / len(row) for row in flags[arm]],
        }

    clusters = _cluster_indices(holdout_rows)
    report: dict[str, Any] = {
        "holdout": str(args.holdout),
        "n_items": len(items),
        "n_families": len(clusters),
        "pass_n": args.pass_n,
        "bootstrap_samples": args.bootstrap_samples,
        "permutation_samples": args.permutation_samples,
        "arms": {},
        "comparisons": {},
        "examples": {},
    }
    for arm in generations:
        report["arms"][arm] = {
            "pass_at_n": _mean(per_metric[arm]["pass_at_n"]),
            "pass_ratio_at_n": _mean(per_metric[arm]["pass_ratio_at_n"]),
            "prediction_rows": len(generations[arm]),
        }

    comparison_pairs = [
        ("complete", "bare"),
        ("fade_ordered", "bare"),
        ("fade_shuffled", "bare"),
        ("fade_ordered", "complete"),
        ("fade_ordered", "fade_shuffled"),
        ("complete", "fade_shuffled"),
    ]
    rng = random.Random(args.seed)
    for left, right in comparison_pairs:
        if left not in generations or right not in generations:
            continue
        key = f"{left}_minus_{right}"
        report["comparisons"][key] = {}
        for metric_name in ("pass_at_n", "pass_ratio_at_n"):
            bootstrap = _bootstrap_diff(
                rng,
                clusters,
                per_metric[left][metric_name],
                per_metric[right][metric_name],
                args.bootstrap_samples,
            )
            p_values = _cluster_signflip_p_value(
                rng,
                clusters,
                per_metric[left][metric_name],
                per_metric[right][metric_name],
                args.permutation_samples,
            )
            report["comparisons"][key][metric_name] = {**bootstrap, **p_values}
        report["examples"][key] = _comparison_examples(
            holdout_rows,
            generations,
            flags,
            left,
            right,
            args.examples_per_comparison,
        )

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_markdown(report, args.output_md)
    print(json.dumps(report["arms"], indent=2, sort_keys=True))
    print(f"Wrote {args.output_json}")
    print(f"Wrote {args.output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
