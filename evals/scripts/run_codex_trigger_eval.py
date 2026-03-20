#!/usr/bin/env python3
"""Run trigger evals using codex exec as a classifier."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from trigger_eval_common import (
    VALID_SOURCES,
    SOURCE_FRONTMATTER,
    discover_eval_configs,
    evaluate_skill,
    filter_eval_configs,
)


def _ensure_codex_cli_available() -> None:
    codex_path = shutil.which("codex")
    if codex_path is None:
        raise RuntimeError(
            "codex CLI not found on PATH. Install it, authenticate it, and verify "
            "`codex exec --help` works before running the Codex eval track."
        )


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run codex-based trigger eval for skill routing")
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
    parser.add_argument(
        "--source",
        default=SOURCE_FRONTMATTER,
        choices=VALID_SOURCES,
        help="Routing source to evaluate: frontmatter, metadata, or combined (default: frontmatter)",
    )
    parser.add_argument(
        "--skill",
        help="Optional single skill name to evaluate",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    _ensure_codex_cli_available()
    repo_root = Path(args.repo_root).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    configs = filter_eval_configs(discover_eval_configs(repo_root), args.skill)

    summaries: list[dict[str, object]] = []
    for config in configs:
        summary = evaluate_skill(
            repo_root,
            config,
            output_dir,
            args.model,
            args.source,
            _run_codex_predictions,
        )
        summaries.append(summary)
        print(
            f"[done] {summary['skill_name']}: {summary['passed']}/{summary['total']} "
            f"-> {summary['output_path']}"
        )

    total = sum(int(item["total"]) for item in summaries)
    passed = sum(int(item["passed"]) for item in summaries)
    print(f"[summary] overall {passed}/{total} ({(passed / total):.1%})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
