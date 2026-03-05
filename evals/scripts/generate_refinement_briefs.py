#!/usr/bin/env python3
"""Generate refinement briefs from trigger-eval analysis reports."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

STOPWORDS = {
    "a",
    "about",
    "all",
    "am",
    "an",
    "and",
    "any",
    "are",
    "as",
    "at",
    "be",
    "because",
    "been",
    "before",
    "but",
    "by",
    "can",
    "change",
    "changes",
    "client",
    "code",
    "component",
    "components",
    "could",
    "display",
    "do",
    "does",
    "done",
    "field",
    "fields",
    "for",
    "from",
    "get",
    "got",
    "has",
    "have",
    "help",
    "how",
    "im",
    "i",
    "if",
    "into",
    "in",
    "is",
    "it",
    "its",
    "just",
    "like",
    "make",
    "need",
    "me",
    "my",
    "next",
    "page",
    "pages",
    "part",
    "project",
    "projects",
    "query",
    "queries",
    "record",
    "records",
    "right",
    "run",
    "runs",
    "same",
    "set",
    "setup",
    "show",
    "site",
    "something",
    "of",
    "on",
    "or",
    "our",
    "please",
    "really",
    "so",
    "that",
    "the",
    "their",
    "they",
    "them",
    "this",
    "to",
    "too",
    "title",
    "up",
    "use",
    "using",
    "way",
    "ways",
    "want",
    "we",
    "what",
    "when",
    "with",
    "work",
    "working",
    "you",
    "your",
}

TOKEN_RE = re.compile(r"[a-z0-9@._-]+")


def _load_report(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if "skills" not in payload or not isinstance(payload["skills"], list):
        raise ValueError(f"{path}: invalid analysis report")
    return payload


def _extract_name_from_skill_md(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None

    # Read only frontmatter block
    end = text.find("\n---\n", 4)
    if end == -1:
        return None

    frontmatter = text[4:end].splitlines()
    for line in frontmatter:
        stripped = line.strip()
        if stripped.startswith("name:"):
            return stripped.split(":", 1)[1].strip()

    return None


def _discover_skill_files(skills_root: Path) -> dict[str, Path]:
    mapping: dict[str, Path] = {}
    for path in sorted(skills_root.glob("*/SKILL.md")):
        name = _extract_name_from_skill_md(path)
        if name:
            mapping[name] = path
    return mapping


def _tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    for raw_token in TOKEN_RE.findall(text.lower()):
        token = raw_token.strip("._-")
        if len(token) < 3:
            continue
        if not any(char.isalnum() for char in token):
            continue
        tokens.append(token)
    return tokens


def _top_terms(
    queries: list[dict[str, Any]], description_text: str, *, limit: int = 12
) -> list[str]:
    description_terms = set(_tokenize(description_text))
    counter: Counter[str] = Counter()

    for row in queries:
        for token in _tokenize(str(row.get("query", ""))):
            if token in STOPWORDS:
                continue
            if token in description_terms:
                continue
            counter[token] += 1

    return [term for term, _count in counter.most_common(limit)]


def _preview(text: str, limit: int = 180) -> str:
    normalized = text.replace("\n", " ").strip()
    if len(normalized) <= limit:
        return normalized
    return f"{normalized[: limit - 3]}..."


def _render_brief(skill: dict[str, Any], skill_file: Path | None, threshold: float) -> str:
    false_negatives = [
        query
        for query in skill.get("queries", [])
        if query.get("should_trigger") and not query.get("threshold_predicted_trigger")
    ]
    false_positives = [
        query
        for query in skill.get("queries", [])
        if (not query.get("should_trigger")) and query.get("threshold_predicted_trigger")
    ]

    false_negatives.sort(key=lambda row: float(row.get("trigger_rate", 0.0)))
    false_positives.sort(key=lambda row: float(row.get("trigger_rate", 0.0)), reverse=True)

    positive_terms = _top_terms(false_negatives, str(skill.get("description", "")))
    negative_terms = _top_terms(false_positives, str(skill.get("description", "")))

    lines: list[str] = []
    lines.append(f"# Refinement Brief: {skill['skill_name']}")
    lines.append("")

    if skill_file is not None:
        lines.append(f"Target skill file: `{skill_file}`")
    else:
        lines.append("Target skill file: not found automatically")
    lines.append("")

    lines.append(
        "Current metrics: "
        f"reported pass {skill['reported_passed']}/{skill['total']} ({float(skill['reported_accuracy']):.1%}), "
        f"precision {float(skill['precision']):.1%}, "
        f"recall {float(skill['recall']):.1%}, "
        f"F1 {float(skill['f1']):.1%}, "
        f"FN {skill['fn']}, FP {skill['fp']}, "
        f"unstable {skill['unstable_count']}."
    )
    lines.append("")

    lines.append(f"Classification threshold used: `{threshold}`")

    if false_negatives:
        lines.append("")
        lines.append("## False Negatives (expected trigger, missed)")
        lines.append("")
        for item in false_negatives[:12]:
            lines.append(
                f"- rate={float(item['trigger_rate']):.3f}: {_preview(str(item['query']))}"
            )

    if false_positives:
        lines.append("")
        lines.append("## False Positives (should not trigger)")
        lines.append("")
        for item in false_positives[:12]:
            lines.append(
                f"- rate={float(item['trigger_rate']):.3f}: {_preview(str(item['query']))}"
            )

    lines.append("")
    lines.append("## Description Refinement Suggestions")
    lines.append("")

    if positive_terms:
        lines.append(
            "- Add explicit positive trigger language for these high-signal terms: "
            + ", ".join(f"`{term}`" for term in positive_terms)
            + "."
        )
    else:
        lines.append("- Positive trigger coverage looks broad; focus on reducing ambiguity in boundaries.")

    if negative_terms:
        lines.append(
            "- Add explicit exclusion language to avoid overlap with: "
            + ", ".join(f"`{term}`" for term in negative_terms)
            + "."
        )
    else:
        lines.append("- False-positive pressure is low; prioritize recall-oriented refinements first.")

    lines.append(
        "- Change only the frontmatter `description` first, re-run evals, then compare before editing the body."
    )

    lines.append("")
    lines.append("## Next Iteration Checklist")
    lines.append("")
    lines.append("1. Apply small description changes (one scope at a time).")
    lines.append("2. Re-run trigger eval on the same query set.")
    lines.append("3. Compare baseline vs candidate with compare_trigger_runs.py.")
    lines.append("4. Keep the change only if recall improves without unacceptable precision drop.")

    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate skill refinement briefs from analysis JSON")
    parser.add_argument(
        "--analysis",
        required=True,
        help="Analysis report JSON produced by analyze_trigger_results.py",
    )
    parser.add_argument(
        "--skills-root",
        default=".",
        help="Repository root containing */SKILL.md folders (default: .)",
    )
    parser.add_argument(
        "--output-dir",
        default="evals/refinement-briefs",
        help="Directory where per-skill briefs are written",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    analysis_path = Path(args.analysis)
    report = _load_report(analysis_path)

    skills_root = Path(args.skills_root)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    skill_files = _discover_skill_files(skills_root)
    threshold = float(report.get("threshold", 0.5))

    generated_files: list[Path] = []
    for skill in sorted(report["skills"], key=lambda row: str(row["skill_name"])):
        skill_name = str(skill["skill_name"])
        target_file = skill_files.get(skill_name)

        brief_text = _render_brief(skill, target_file, threshold)
        output_path = output_dir / f"{skill_name}-refinement.md"
        output_path.write_text(brief_text, encoding="utf-8")
        generated_files.append(output_path)

    print("Generated refinement briefs:")
    for path in generated_files:
        print(f"- {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
