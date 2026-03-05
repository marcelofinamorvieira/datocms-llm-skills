#!/usr/bin/env python3
"""Run trigger evals using codex exec as a classifier.

This evaluates each skill's current frontmatter description against the prompt sets
in evals/*.json and emits result files compatible with analyze_trigger_results.py.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class SkillEvalConfig:
    eval_file: str
    skill_file: str


SKILL_EVAL_CONFIGS: list[SkillEvalConfig] = [
    SkillEvalConfig("evals/datocms-cda-skill-eval.json", "datocms-cda-skill/SKILL.md"),
    SkillEvalConfig("evals/datocms-cli-skill-eval.json", "datocms-cli-skill/SKILL.md"),
    SkillEvalConfig("evals/datocms-cma-skill-eval.json", "datocms-cma-skill/SKILL.md"),
    SkillEvalConfig(
        "evals/datocms-frontend-integrations-skill-eval.json",
        "datocms-frontend-integrations-skill/SKILL.md",
    ),
    SkillEvalConfig("evals/datocms-pluginsdk-skill-eval.json", "datocms-pluginsdk-skill/SKILL.md"),
]


def _extract_frontmatter(skill_path: Path) -> tuple[str, str]:
    text = skill_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{skill_path}: missing frontmatter")

    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError(f"{skill_path}: frontmatter not closed")

    frontmatter = text[4:end]
    lines = frontmatter.splitlines()

    name: str | None = None
    description: str | None = None

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("name:"):
            name = stripped.split(":", 1)[1].strip()
            i += 1
            continue

        if stripped.startswith("description:"):
            raw_value = stripped.split(":", 1)[1].strip()
            if raw_value in {">", ">-", "|", "|-"}:
                i += 1
                chunks: list[str] = []
                while i < len(lines):
                    block_line = lines[i]
                    if block_line.startswith("  "):
                        chunks.append(block_line.strip())
                        i += 1
                        continue
                    break
                description = " ".join(chunk for chunk in chunks if chunk)
                continue

            description = raw_value
            i += 1
            continue

        i += 1

    if not name:
        raise ValueError(f"{skill_path}: missing name in frontmatter")
    if not description:
        raise ValueError(f"{skill_path}: missing description in frontmatter")

    return name, description


def _build_prompt(skill_name: str, description: str, queries: list[str]) -> str:
    query_lines = "\n".join(f"{idx + 1}. {query}" for idx, query in enumerate(queries))

    return f"""You are a strict skill-trigger classifier.

Target skill name: {skill_name}
Target skill description:
{description}

Task:
For each user query below, decide if this TARGET skill should trigger.

Rules:
- Return true only when the query directly falls within this target skill scope.
- Return false when the query is better handled by a different DatoCMS skill domain.
- If uncertain, prefer false.

Output:
Return exactly one JSON object with this shape:
{{"predictions":[boolean,...]}}
The predictions array must contain exactly {len(queries)} booleans, in the same order as the queries.
No explanation.

Queries:
{query_lines}
"""


def _run_codex_predictions(repo_root: Path, prompt: str, expected_len: int, model: str | None) -> list[bool]:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as schema_file:
        schema_path = Path(schema_file.name)
        schema = {
            "type": "object",
            "properties": {
                "predictions": {"type": "array", "items": {"type": "boolean"}},
            },
            "required": ["predictions"],
            "additionalProperties": False,
        }
        schema_file.write(json.dumps(schema))

    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as output_file:
        output_path = Path(output_file.name)

    cmd = [
        "codex",
        "exec",
        "--ephemeral",
        "--sandbox",
        "read-only",
        "--skip-git-repo-check",
        "--cd",
        str(repo_root),
        "--output-schema",
        str(schema_path),
        "--output-last-message",
        str(output_path),
    ]

    if model:
        cmd.extend(["--model", model])

    cmd.append(prompt)

    try:
        completed = subprocess.run(
            cmd,
            check=False,
            capture_output=True,
            text=True,
        )

        if completed.returncode != 0:
            stderr_preview = completed.stderr[-1000:]
            stdout_preview = completed.stdout[-1000:]
            raise RuntimeError(
                "codex exec failed\n"
                f"returncode={completed.returncode}\n"
                f"stdout_tail={stdout_preview}\n"
                f"stderr_tail={stderr_preview}"
            )

        raw = output_path.read_text(encoding="utf-8").strip()
        payload = json.loads(raw)
        predictions = payload.get("predictions")

        if not isinstance(predictions, list):
            raise ValueError(f"invalid codex output, expected predictions list: {raw}")

        if len(predictions) != expected_len:
            raise ValueError(
                f"invalid predictions length: expected {expected_len}, got {len(predictions)}"
            )

        normalized: list[bool] = []
        for idx, value in enumerate(predictions):
            if not isinstance(value, bool):
                raise ValueError(f"prediction index {idx} is not bool: {value!r}")
            normalized.append(value)

        return normalized
    finally:
        schema_path.unlink(missing_ok=True)
        output_path.unlink(missing_ok=True)


def _evaluate_skill(
    repo_root: Path,
    config: SkillEvalConfig,
    output_dir: Path,
    model: str | None,
) -> dict[str, Any]:
    eval_path = repo_root / config.eval_file
    skill_path = repo_root / config.skill_file

    skill_name, description = _extract_frontmatter(skill_path)
    eval_queries = json.loads(eval_path.read_text(encoding="utf-8"))

    if not isinstance(eval_queries, list):
        raise ValueError(f"{eval_path}: expected array of eval cases")

    queries: list[str] = [str(row["query"]) for row in eval_queries]
    predictions = _run_codex_predictions(repo_root, _build_prompt(skill_name, description, queries), len(queries), model)

    results: list[dict[str, Any]] = []
    passed = 0

    for row, prediction in zip(eval_queries, predictions, strict=True):
        should_trigger = bool(row["should_trigger"])
        triggers = 1 if prediction else 0
        trigger_rate = float(triggers)
        case_pass = prediction == should_trigger
        if case_pass:
            passed += 1

        results.append(
            {
                "query": str(row["query"]),
                "should_trigger": should_trigger,
                "trigger_rate": trigger_rate,
                "triggers": triggers,
                "runs": 1,
                "pass": case_pass,
            }
        )

    payload = {
        "skill_name": skill_name,
        "description": description,
        "results": results,
        "summary": {
            "total": len(results),
            "passed": passed,
            "failed": len(results) - passed,
        },
    }

    output_name = f"{skill_name}-eval-results.json"
    output_path = output_dir / output_name
    output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    return {
        "skill_name": skill_name,
        "output_path": str(output_path),
        "passed": passed,
        "total": len(results),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run codex-based trigger eval for skill descriptions")
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root containing skills and evals (default: .)",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory where result JSON files will be written",
    )
    parser.add_argument(
        "--model",
        help="Optional codex model override",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    summaries: list[dict[str, Any]] = []
    for config in SKILL_EVAL_CONFIGS:
        summary = _evaluate_skill(repo_root, config, output_dir, args.model)
        summaries.append(summary)
        print(
            f"[done] {summary['skill_name']}: {summary['passed']}/{summary['total']} "
            f"-> {summary['output_path']}"
        )

    total = sum(item["total"] for item in summaries)
    passed = sum(item["passed"] for item in summaries)
    print(f"[summary] overall {passed}/{total} ({(passed / total):.1%})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
