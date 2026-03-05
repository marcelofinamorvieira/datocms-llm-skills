#!/usr/bin/env python3
"""Analyze skill trigger-eval result files.

This script accepts result files with either pure JSON or a human-readable preamble
followed by JSON (the format currently used in this repository).
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class QueryEvaluation:
    query: str
    should_trigger: bool
    trigger_rate: float
    triggers: int
    runs: int
    reported_pass: bool
    threshold_predicted_trigger: bool
    threshold_pass: bool
    unstable: bool


@dataclass
class SkillSummary:
    skill_name: str
    description: str
    source_file: str
    total: int
    reported_passed: int
    reported_accuracy: float
    threshold_accuracy: float
    tp: int
    tn: int
    fp: int
    fn: int
    precision: float
    recall: float
    f1: float
    unstable_count: int
    avg_trigger_rate_true: float
    avg_trigger_rate_false: float
    queries: list[QueryEvaluation]


def _safe_div(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def _extract_json_payload(raw: str, source: Path) -> dict[str, Any]:
    first_brace = raw.find("{")
    if first_brace < 0:
        raise ValueError(f"{source}: no JSON object found")

    decoder = json.JSONDecoder()
    last_error: ValueError | None = None

    cursor = first_brace
    while cursor >= 0:
        try:
            parsed, _end = decoder.raw_decode(raw[cursor:])
            if isinstance(parsed, dict):
                return parsed
            raise ValueError(f"{source}: JSON root is not an object")
        except ValueError as exc:
            last_error = exc
            cursor = raw.find("{", cursor + 1)

    if last_error is not None:
        raise ValueError(f"{source}: could not parse JSON payload") from last_error
    raise ValueError(f"{source}: could not parse JSON payload")


def _load_result_file(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    payload = _extract_json_payload(raw, path)

    required = ("skill_name", "description", "results")
    missing = [key for key in required if key not in payload]
    if missing:
        missing_text = ", ".join(missing)
        raise ValueError(f"{path}: missing required keys: {missing_text}")

    if not isinstance(payload["results"], list):
        raise ValueError(f"{path}: 'results' must be a list")

    return payload


def _build_skill_summary(payload: dict[str, Any], source_file: Path, threshold: float) -> SkillSummary:
    query_items: list[QueryEvaluation] = []

    tp = tn = fp = fn = 0
    reported_passed = 0

    true_rates: list[float] = []
    false_rates: list[float] = []

    for entry in payload["results"]:
        query = str(entry.get("query", "")).strip()
        should_trigger = bool(entry.get("should_trigger", False))
        trigger_rate = float(entry.get("trigger_rate", 0.0))
        triggers = int(entry.get("triggers", round(trigger_rate * int(entry.get("runs", 0) or 0))))
        runs = int(entry.get("runs", 0))

        threshold_predicted_trigger = trigger_rate >= threshold
        threshold_pass = threshold_predicted_trigger == should_trigger

        reported_pass = bool(entry["pass"]) if "pass" in entry else threshold_pass

        unstable = 0.0 < trigger_rate < 1.0

        if reported_pass:
            reported_passed += 1

        if should_trigger:
            true_rates.append(trigger_rate)
            if threshold_predicted_trigger:
                tp += 1
            else:
                fn += 1
        else:
            false_rates.append(trigger_rate)
            if threshold_predicted_trigger:
                fp += 1
            else:
                tn += 1

        query_items.append(
            QueryEvaluation(
                query=query,
                should_trigger=should_trigger,
                trigger_rate=trigger_rate,
                triggers=triggers,
                runs=runs,
                reported_pass=reported_pass,
                threshold_predicted_trigger=threshold_predicted_trigger,
                threshold_pass=threshold_pass,
                unstable=unstable,
            )
        )

    total = len(query_items)
    reported_accuracy = _safe_div(reported_passed, total)
    threshold_accuracy = _safe_div(tp + tn, total)

    precision = _safe_div(tp, tp + fp)
    recall = _safe_div(tp, tp + fn)
    f1 = _safe_div(2 * precision * recall, precision + recall)

    unstable_count = sum(1 for item in query_items if item.unstable)

    avg_trigger_rate_true = _safe_div(sum(true_rates), len(true_rates))
    avg_trigger_rate_false = _safe_div(sum(false_rates), len(false_rates))

    return SkillSummary(
        skill_name=str(payload["skill_name"]),
        description=str(payload["description"]),
        source_file=str(source_file),
        total=total,
        reported_passed=reported_passed,
        reported_accuracy=reported_accuracy,
        threshold_accuracy=threshold_accuracy,
        tp=tp,
        tn=tn,
        fp=fp,
        fn=fn,
        precision=precision,
        recall=recall,
        f1=f1,
        unstable_count=unstable_count,
        avg_trigger_rate_true=avg_trigger_rate_true,
        avg_trigger_rate_false=avg_trigger_rate_false,
        queries=query_items,
    )


def _aggregate(skills: list[SkillSummary]) -> dict[str, Any]:
    total = sum(skill.total for skill in skills)
    reported_passed = sum(skill.reported_passed for skill in skills)

    tp = sum(skill.tp for skill in skills)
    tn = sum(skill.tn for skill in skills)
    fp = sum(skill.fp for skill in skills)
    fn = sum(skill.fn for skill in skills)

    precision = _safe_div(tp, tp + fp)
    recall = _safe_div(tp, tp + fn)
    f1 = _safe_div(2 * precision * recall, precision + recall)

    return {
        "total": total,
        "reported_passed": reported_passed,
        "reported_accuracy": _safe_div(reported_passed, total),
        "threshold_accuracy": _safe_div(tp + tn, total),
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "unstable_count": sum(skill.unstable_count for skill in skills),
    }


def _render_markdown(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Trigger Eval Analysis")
    lines.append("")
    lines.append(f"Generated at: {report['generated_at_utc']}")
    lines.append(f"Threshold: `{report['threshold']}`")
    lines.append("")

    aggregate = report["aggregate"]
    lines.append(
        "Overall: "
        f"{aggregate['reported_passed']}/{aggregate['total']} reported-pass "
        f"({aggregate['reported_accuracy']:.1%}), "
        f"precision {aggregate['precision']:.1%}, "
        f"recall {aggregate['recall']:.1%}, "
        f"F1 {aggregate['f1']:.1%}."
    )
    lines.append("")

    lines.append("| Skill | Reported Pass | Precision | Recall | F1 | FN | FP | Unstable |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for skill in report["skills"]:
        lines.append(
            "| "
            f"{skill['skill_name']} | "
            f"{skill['reported_passed']}/{skill['total']} ({skill['reported_accuracy']:.1%}) | "
            f"{skill['precision']:.1%} | "
            f"{skill['recall']:.1%} | "
            f"{skill['f1']:.1%} | "
            f"{skill['fn']} | "
            f"{skill['fp']} | "
            f"{skill['unstable_count']} |"
        )

    highest_impact: list[dict[str, Any]] = []
    for skill in report["skills"]:
        for query in skill["queries"]:
            if query["should_trigger"] and not query["threshold_predicted_trigger"]:
                highest_impact.append(
                    {
                        "skill_name": skill["skill_name"],
                        "query": query["query"],
                        "trigger_rate": query["trigger_rate"],
                    }
                )

    highest_impact.sort(key=lambda item: item["trigger_rate"])

    if highest_impact:
        lines.append("")
        lines.append("## Highest-Impact False Negatives")
        lines.append("")
        for item in highest_impact[:10]:
            query_preview = item["query"].replace("\n", " ").strip()
            if len(query_preview) > 180:
                query_preview = f"{query_preview[:177]}..."
            lines.append(
                f"- `{item['skill_name']}` rate={item['trigger_rate']:.3f}: {query_preview}"
            )

    return "\n".join(lines) + "\n"


def _build_report(result_files: list[Path], threshold: float) -> dict[str, Any]:
    skill_summaries = [
        _build_skill_summary(_load_result_file(path), path, threshold)
        for path in result_files
    ]

    skill_summaries.sort(key=lambda summary: summary.skill_name)

    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "threshold": threshold,
        "skills": [
            {
                **{key: value for key, value in asdict(skill).items() if key != "queries"},
                "queries": [asdict(query) for query in skill.queries],
            }
            for skill in skill_summaries
        ],
        "aggregate": _aggregate(skill_summaries),
    }

    return report


def _discover_files(results_dir: Path, pattern: str) -> list[Path]:
    files = sorted(results_dir.glob(pattern))
    if not files:
        raise ValueError(f"no files found in {results_dir} matching pattern '{pattern}'")
    return files


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze skill trigger-eval result files")
    parser.add_argument(
        "--results-dir",
        default="evals/results",
        help="Directory containing result files (default: evals/results)",
    )
    parser.add_argument(
        "--pattern",
        default="*-eval-results.json",
        help="Glob pattern inside results dir (default: *-eval-results.json)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="Trigger threshold used to classify query-level predictions (default: 0.5)",
    )
    parser.add_argument(
        "--output-json",
        help="Optional path for machine-readable report JSON",
    )
    parser.add_argument(
        "--output-markdown",
        help="Optional path for human-readable markdown summary",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    results_dir = Path(args.results_dir)

    result_files = _discover_files(results_dir, args.pattern)
    report = _build_report(result_files, args.threshold)

    markdown = _render_markdown(report)
    print(markdown, end="")

    if args.output_json:
        output_json = Path(args.output_json)
        output_json.parent.mkdir(parents=True, exist_ok=True)
        output_json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if args.output_markdown:
        output_markdown = Path(args.output_markdown)
        output_markdown.parent.mkdir(parents=True, exist_ok=True)
        output_markdown.write_text(markdown, encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
