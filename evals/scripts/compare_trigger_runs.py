#!/usr/bin/env python3
"""Compare two trigger-eval analysis reports.

Both input files must be JSON outputs produced by analyze_trigger_results.py.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_QUERY_MODE = "implicit"
KNOWN_QUERY_MODES = ("implicit", "explicit", "overlap")


@dataclass
class SkillDelta:
    skill_name: str
    baseline_reported_accuracy: float
    candidate_reported_accuracy: float
    delta_reported_accuracy: float
    baseline_recall: float
    candidate_recall: float
    delta_recall: float
    baseline_precision: float
    candidate_precision: float
    delta_precision: float
    baseline_f1: float
    candidate_f1: float
    delta_f1: float
    baseline_fn: int
    candidate_fn: int
    delta_fn: int
    baseline_fp: int
    candidate_fp: int
    delta_fp: int


@dataclass
class QueryModeDelta:
    query_mode: str
    baseline_total: int
    candidate_total: int
    delta_total: int
    baseline_reported_accuracy: float
    candidate_reported_accuracy: float
    delta_reported_accuracy: float
    baseline_recall: float
    candidate_recall: float
    delta_recall: float
    baseline_precision: float
    candidate_precision: float
    delta_precision: float
    baseline_f1: float
    candidate_f1: float
    delta_f1: float


def _load_report(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected object JSON")
    if "skills" not in payload or not isinstance(payload["skills"], list):
        raise ValueError(f"{path}: missing skills[]")
    return payload


def _mode_sort_key(query_mode: str) -> tuple[int, str]:
    try:
        return (KNOWN_QUERY_MODES.index(query_mode), query_mode)
    except ValueError:
        return (len(KNOWN_QUERY_MODES), query_mode)


def _index_skills(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(skill["skill_name"]): skill for skill in report["skills"]}


def _index_query_modes(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    aggregate = report.get("aggregate", {})
    query_modes = aggregate.get("query_modes", [])
    if not isinstance(query_modes, list):
        return {}
    return {str(mode["query_mode"]): mode for mode in query_modes}


def _collect_deltas(baseline: dict[str, Any], candidate: dict[str, Any]) -> list[SkillDelta]:
    baseline_map = _index_skills(baseline)
    candidate_map = _index_skills(candidate)

    shared_names = sorted(set(baseline_map) & set(candidate_map))
    deltas: list[SkillDelta] = []

    for name in shared_names:
        b = baseline_map[name]
        c = candidate_map[name]
        deltas.append(
            SkillDelta(
                skill_name=name,
                baseline_reported_accuracy=float(b["reported_accuracy"]),
                candidate_reported_accuracy=float(c["reported_accuracy"]),
                delta_reported_accuracy=float(c["reported_accuracy"]) - float(b["reported_accuracy"]),
                baseline_recall=float(b["recall"]),
                candidate_recall=float(c["recall"]),
                delta_recall=float(c["recall"]) - float(b["recall"]),
                baseline_precision=float(b["precision"]),
                candidate_precision=float(c["precision"]),
                delta_precision=float(c["precision"]) - float(b["precision"]),
                baseline_f1=float(b["f1"]),
                candidate_f1=float(c["f1"]),
                delta_f1=float(c["f1"]) - float(b["f1"]),
                baseline_fn=int(b["fn"]),
                candidate_fn=int(c["fn"]),
                delta_fn=int(c["fn"]) - int(b["fn"]),
                baseline_fp=int(b["fp"]),
                candidate_fp=int(c["fp"]),
                delta_fp=int(c["fp"]) - int(b["fp"]),
            )
        )

    return deltas


def _collect_query_mode_deltas(
    baseline: dict[str, Any], candidate: dict[str, Any]
) -> list[QueryModeDelta]:
    baseline_modes = _index_query_modes(baseline)
    candidate_modes = _index_query_modes(candidate)

    shared_modes = sorted(set(baseline_modes) & set(candidate_modes), key=_mode_sort_key)
    deltas: list[QueryModeDelta] = []

    for query_mode in shared_modes:
        b = baseline_modes[query_mode]
        c = candidate_modes[query_mode]
        deltas.append(
            QueryModeDelta(
                query_mode=query_mode,
                baseline_total=int(b["total"]),
                candidate_total=int(c["total"]),
                delta_total=int(c["total"]) - int(b["total"]),
                baseline_reported_accuracy=float(b["reported_accuracy"]),
                candidate_reported_accuracy=float(c["reported_accuracy"]),
                delta_reported_accuracy=float(c["reported_accuracy"]) - float(b["reported_accuracy"]),
                baseline_recall=float(b["recall"]),
                candidate_recall=float(c["recall"]),
                delta_recall=float(c["recall"]) - float(b["recall"]),
                baseline_precision=float(b["precision"]),
                candidate_precision=float(c["precision"]),
                delta_precision=float(c["precision"]) - float(b["precision"]),
                baseline_f1=float(b["f1"]),
                candidate_f1=float(c["f1"]),
                delta_f1=float(c["f1"]) - float(b["f1"]),
            )
        )

    return deltas


def _query_changes(
    baseline: dict[str, Any], candidate: dict[str, Any]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    baseline_map = _index_skills(baseline)
    candidate_map = _index_skills(candidate)

    improvements: list[dict[str, Any]] = []
    regressions: list[dict[str, Any]] = []

    for skill_name in sorted(set(baseline_map) & set(candidate_map)):
        b_queries = {
            str(query["query"]): query
            for query in baseline_map[skill_name].get("queries", [])
        }
        c_queries = {
            str(query["query"]): query
            for query in candidate_map[skill_name].get("queries", [])
        }

        for query_text in sorted(set(b_queries) & set(c_queries)):
            bq = b_queries[query_text]
            cq = c_queries[query_text]

            b_pass = bool(bq.get("reported_pass", False))
            c_pass = bool(cq.get("reported_pass", False))

            b_rate = float(bq.get("trigger_rate", 0.0))
            c_rate = float(cq.get("trigger_rate", 0.0))

            row = {
                "skill_name": skill_name,
                "query": query_text,
                "query_mode": str(cq.get("query_mode", bq.get("query_mode", DEFAULT_QUERY_MODE))),
                "baseline_trigger_rate": b_rate,
                "candidate_trigger_rate": c_rate,
                "delta_trigger_rate": c_rate - b_rate,
                "baseline_pass": b_pass,
                "candidate_pass": c_pass,
                "should_trigger": bool(cq.get("should_trigger", bq.get("should_trigger", False))),
            }

            if not b_pass and c_pass:
                improvements.append(row)
            elif b_pass and not c_pass:
                regressions.append(row)

    improvements.sort(key=lambda row: (-row["delta_trigger_rate"], row["skill_name"]))
    regressions.sort(key=lambda row: (row["delta_trigger_rate"], row["skill_name"]))

    return improvements, regressions


def _fmt_delta(value: float) -> str:
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.1%}"


def _preview(text: str, limit: int = 160) -> str:
    normalized = text.replace("\n", " ").strip()
    if len(normalized) <= limit:
        return normalized
    return f"{normalized[: limit - 3]}..."


def _render_query_change_lines(items: list[dict[str, Any]]) -> list[str]:
    lines: list[str] = []
    for item in items[:15]:
        mode_prefix = ""
        if item["query_mode"] != DEFAULT_QUERY_MODE:
            mode_prefix = f"[{item['query_mode']}] "
        lines.append(
            "- "
            f"`{item['skill_name']}` {mode_prefix}rate "
            f"{item['baseline_trigger_rate']:.3f} -> {item['candidate_trigger_rate']:.3f}: "
            f"{_preview(item['query'])}"
        )
    return lines


def _render_markdown(
    baseline_path: Path,
    candidate_path: Path,
    baseline: dict[str, Any],
    candidate: dict[str, Any],
    deltas: list[SkillDelta],
    query_mode_deltas: list[QueryModeDelta],
    improvements: list[dict[str, Any]],
    regressions: list[dict[str, Any]],
) -> str:
    lines: list[str] = []

    lines.append("# Trigger Eval Comparison")
    lines.append("")
    lines.append(f"Baseline: `{baseline_path}`")
    lines.append(f"Candidate: `{candidate_path}`")
    lines.append("")

    b_agg = baseline["aggregate"]
    c_agg = candidate["aggregate"]

    lines.append(
        "Overall reported pass: "
        f"{b_agg['reported_passed']}/{b_agg['total']} ({float(b_agg['reported_accuracy']):.1%}) -> "
        f"{c_agg['reported_passed']}/{c_agg['total']} ({float(c_agg['reported_accuracy']):.1%}) "
        f"({_fmt_delta(float(c_agg['reported_accuracy']) - float(b_agg['reported_accuracy']))})"
    )
    lines.append(
        "Overall recall / precision / F1: "
        f"{float(b_agg['recall']):.1%}/{float(b_agg['precision']):.1%}/{float(b_agg['f1']):.1%} -> "
        f"{float(c_agg['recall']):.1%}/{float(c_agg['precision']):.1%}/{float(c_agg['f1']):.1%}"
    )
    lines.append("")

    if query_mode_deltas:
        lines.append("## Overall By Query Mode")
        lines.append("")
        lines.append("| Query Mode | Total Δ | Pass Δ | Recall Δ | Precision Δ | F1 Δ |")
        lines.append("|---|---:|---:|---:|---:|---:|")
        for delta in query_mode_deltas:
            lines.append(
                "| "
                f"{delta.query_mode} | "
                f"{delta.delta_total:+d} | "
                f"{_fmt_delta(delta.delta_reported_accuracy)} | "
                f"{_fmt_delta(delta.delta_recall)} | "
                f"{_fmt_delta(delta.delta_precision)} | "
                f"{_fmt_delta(delta.delta_f1)} |"
            )
        lines.append("")

    lines.append("| Skill | Pass Δ | Recall Δ | Precision Δ | F1 Δ | FN Δ | FP Δ |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")

    for delta in deltas:
        lines.append(
            "| "
            f"{delta.skill_name} | "
            f"{_fmt_delta(delta.delta_reported_accuracy)} | "
            f"{_fmt_delta(delta.delta_recall)} | "
            f"{_fmt_delta(delta.delta_precision)} | "
            f"{_fmt_delta(delta.delta_f1)} | "
            f"{delta.delta_fn:+d} | "
            f"{delta.delta_fp:+d} |"
        )

    if improvements:
        lines.append("")
        lines.append("## Query-Level Improvements")
        lines.append("")
        lines.extend(_render_query_change_lines(improvements))

    if regressions:
        lines.append("")
        lines.append("## Query-Level Regressions")
        lines.append("")
        lines.extend(_render_query_change_lines(regressions))

    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare two trigger-eval analysis reports")
    parser.add_argument("--baseline", required=True, help="Baseline analysis report JSON")
    parser.add_argument("--candidate", required=True, help="Candidate analysis report JSON")
    parser.add_argument("--output-markdown", help="Optional path for markdown comparison")
    parser.add_argument("--output-json", help="Optional path for machine-readable comparison")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    baseline_path = Path(args.baseline)
    candidate_path = Path(args.candidate)

    baseline = _load_report(baseline_path)
    candidate = _load_report(candidate_path)

    deltas = _collect_deltas(baseline, candidate)
    query_mode_deltas = _collect_query_mode_deltas(baseline, candidate)
    improvements, regressions = _query_changes(baseline, candidate)

    payload = {
        "baseline": str(baseline_path),
        "candidate": str(candidate_path),
        "skill_deltas": [delta.__dict__ for delta in deltas],
        "query_mode_deltas": [delta.__dict__ for delta in query_mode_deltas],
        "query_improvements": improvements,
        "query_regressions": regressions,
    }

    markdown = _render_markdown(
        baseline_path,
        candidate_path,
        baseline,
        candidate,
        deltas,
        query_mode_deltas,
        improvements,
        regressions,
    )

    print(markdown, end="")

    if args.output_json:
        output_json = Path(args.output_json)
        output_json.parent.mkdir(parents=True, exist_ok=True)
        output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    if args.output_markdown:
        output_markdown = Path(args.output_markdown)
        output_markdown.parent.mkdir(parents=True, exist_ok=True)
        output_markdown.write_text(markdown, encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
