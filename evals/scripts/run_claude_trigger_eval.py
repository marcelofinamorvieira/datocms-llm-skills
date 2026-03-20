#!/usr/bin/env python3
"""Run trigger evals using Claude Code as a classifier."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from trigger_eval_common import (
    VALID_SOURCES,
    SOURCE_FRONTMATTER,
    discover_eval_configs,
    evaluate_skill,
    filter_eval_configs,
)

DEFAULT_TIMEOUT_SECONDS = 180
JSON_OBJECT_RE = re.compile(r"\{.*\}", re.DOTALL)


def _ensure_claude_cli_available() -> None:
    claude_path = shutil.which("claude")
    if claude_path is None:
        raise RuntimeError(
            "claude CLI not found on PATH. Install it, authenticate it, and verify "
            "`claude --help` works before running the Claude Code eval track."
        )


def _extract_predictions(payload: Any) -> list[bool] | None:
    if isinstance(payload, dict):
        predictions = payload.get("predictions")
        if isinstance(predictions, list):
            return predictions

        for key in ("result", "output", "response", "message", "content", "messages", "text"):
            if key not in payload:
                continue
            extracted = _extract_predictions(payload[key])
            if extracted is not None:
                return extracted
        return None

    if isinstance(payload, list):
        for item in payload:
            extracted = _extract_predictions(item)
            if extracted is not None:
                return extracted
        return None

    if isinstance(payload, str):
        try:
            nested = json.loads(payload)
        except json.JSONDecodeError:
            match = JSON_OBJECT_RE.search(payload)
            if match is None:
                return None
            try:
                nested = json.loads(match.group(0))
            except json.JSONDecodeError:
                return None
        return _extract_predictions(nested)

    return None


def _parse_predictions(raw: str, expected_len: int) -> list[bool]:
    if not raw.strip():
        raise ValueError("invalid claude output: empty stdout")

    payload_candidates: list[Any] = []
    try:
        payload_candidates.append(json.loads(raw))
    except json.JSONDecodeError:
        match = JSON_OBJECT_RE.search(raw)
        if match is not None:
            payload_candidates.append(json.loads(match.group(0)))

    if not payload_candidates:
        raise ValueError(f"invalid claude output, expected JSON object: {raw[-1000:]}")

    for payload in payload_candidates:
        predictions = _extract_predictions(payload)
        if not isinstance(predictions, list):
            continue

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

    raise ValueError(f"invalid claude output, missing predictions list: {raw[-1000:]}")


def _run_claude_predictions(repo_root: Path, prompt: str, expected_len: int, model: str | None) -> list[bool]:
    del repo_root

    cmd = [
        "claude",
        "-p",
        "--no-session-persistence",
        "--dangerously-skip-permissions",
        "--setting-sources",
        "user",
        "--tools",
        "",
        "--system-prompt",
        "You are a JSON-only classifier. Never use tools. Reply with only the requested JSON object.",
    ]

    if model:
        cmd.extend(["--model", model])

    cmd.append(prompt)

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            completed = subprocess.run(
                cmd,
                check=False,
                capture_output=True,
                text=True,
                timeout=DEFAULT_TIMEOUT_SECONDS,
                cwd=temp_dir,
            )
    except subprocess.TimeoutExpired as exc:
        stdout_preview = (exc.stdout or "")[-1000:]
        stderr_preview = (exc.stderr or "")[-1000:]
        raise RuntimeError(
            "claude command timed out\n"
            f"timeout_seconds={DEFAULT_TIMEOUT_SECONDS}\n"
            f"stdout_tail={stdout_preview}\n"
            f"stderr_tail={stderr_preview}"
        ) from exc

    if completed.returncode != 0:
        stderr_preview = completed.stderr[-1000:]
        stdout_preview = completed.stdout[-1000:]
        raise RuntimeError(
            "claude command failed\n"
            f"returncode={completed.returncode}\n"
            f"stdout_tail={stdout_preview}\n"
            f"stderr_tail={stderr_preview}"
        )

    return _parse_predictions(completed.stdout, expected_len)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Claude Code trigger eval for skill routing")
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
        help="Optional Claude Code model override",
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
    _ensure_claude_cli_available()
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
            _run_claude_predictions,
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
