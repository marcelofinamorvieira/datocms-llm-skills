#!/usr/bin/env python3
"""Validate repo invariants for DatoCMS skill documentation."""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

BANNED_SKILL_BODY_PATTERNS = (
    "AskUserQuestion",
    "Read tool",
    "Claude Code alias",
    "slash alias",
)

REFERENCE_PATH_RE = re.compile(r"`(((?:\.\./)+|references/)[^`]+\.md)`")
ROUTED_SKILL_RE = re.compile(r"\*\*(datocms-[a-z0-9-]+)\*\*")

SYNC_NAME_RE = re.compile(r"^# synced_from_name: (?P<value>.+)$", re.MULTILINE)
SYNC_DESC_HASH_RE = re.compile(
    r"^# synced_from_description_sha256: (?P<value>[0-9a-f]{64})$",
    re.MULTILINE,
)
DISPLAY_NAME_RE = re.compile(r'^  display_name: "(?P<value>(?:[^"\\]|\\.)*)"$', re.MULTILINE)
SHORT_DESCRIPTION_RE = re.compile(
    r'^  short_description: "(?P<value>(?:[^"\\]|\\.)*)"$',
    re.MULTILINE,
)
DEFAULT_PROMPT_RE = re.compile(r'^  default_prompt: "(?P<value>(?:[^"\\]|\\.)*)"$', re.MULTILINE)
ALLOW_IMPLICIT_RE = re.compile(
    r"^  allow_implicit_invocation: (?P<value>true|false)$",
    re.MULTILINE,
)

SKILL_GLOB_PATTERNS = (
    "skills/*/SKILL.md",
    "setup/*/*/SKILL.md",
)

SCAFFOLD_CAPABLE_SKILLS = {
    "datocms-frontend-integrations",
    "datocms-setup-cache-tags",
    "datocms-setup-responsive-images",
    "datocms-setup-structured-text",
    "datocms-setup-video-player",
    "datocms-setup-site-search",
    "datocms-setup-seo",
    "datocms-setup-robots-sitemaps",
    "datocms-setup-web-previews",
    "datocms-setup-webhooks",
    "datocms-setup-build-triggers",
}

STALE_SCAFFOLD_MARKETING_PATTERNS = (
    "or uses TODO placeholders",
    "or TODO placeholders",
    "placeholder noted for user to fill in",
)

IGNORED_GIT_STATUS_PREFIXES = (
    "?? local/",
    "?? local",
)


@dataclass(frozen=True)
class SkillFrontmatter:
    name: str
    description: str
    disable_model_invocation: bool


@dataclass(frozen=True)
class SkillMetadata:
    synced_name: str
    synced_description_hash: str
    display_name: str
    short_description: str
    default_prompt: str
    allow_implicit_invocation: bool


def _decode_double_quoted_yaml(value: str) -> str:
    return bytes(value, "utf-8").decode("unicode_escape")


def _extract_frontmatter(path: Path) -> SkillFrontmatter:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing frontmatter")

    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError(f"{path}: frontmatter not closed")

    lines = text[4:end].splitlines()

    name: str | None = None
    description: str | None = None
    disable_model_invocation = False

    i = 0
    while i < len(lines):
        stripped = lines[i].strip()

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
                    if not block_line.strip():
                        i += 1
                        continue
                    break
                description = " ".join(chunk for chunk in chunks if chunk)
                continue

            description = raw_value
            i += 1
            continue

        if stripped.startswith("disable-model-invocation:"):
            disable_model_invocation = stripped.split(":", 1)[1].strip().lower() == "true"

        i += 1

    if not name:
        raise ValueError(f"{path}: missing name in frontmatter")
    if not description:
        raise ValueError(f"{path}: missing description in frontmatter")

    return SkillFrontmatter(
        name=name,
        description=description,
        disable_model_invocation=disable_model_invocation,
    )


def _parse_metadata_file(path: Path) -> SkillMetadata:
    text = path.read_text(encoding="utf-8")

    synced_name_match = SYNC_NAME_RE.search(text)
    synced_hash_match = SYNC_DESC_HASH_RE.search(text)
    display_name_match = DISPLAY_NAME_RE.search(text)
    short_description_match = SHORT_DESCRIPTION_RE.search(text)
    default_prompt_match = DEFAULT_PROMPT_RE.search(text)
    allow_implicit_match = ALLOW_IMPLICIT_RE.search(text)

    missing_fields = []
    if synced_name_match is None:
        missing_fields.append("synced_from_name")
    if synced_hash_match is None:
        missing_fields.append("synced_from_description_sha256")
    if display_name_match is None:
        missing_fields.append("interface.display_name")
    if short_description_match is None:
        missing_fields.append("interface.short_description")
    if default_prompt_match is None:
        missing_fields.append("interface.default_prompt")
    if allow_implicit_match is None:
        missing_fields.append("policy.allow_implicit_invocation")

    if missing_fields:
        missing = ", ".join(missing_fields)
        raise ValueError(f"{path}: missing metadata fields: {missing}")

    return SkillMetadata(
        synced_name=synced_name_match.group("value"),
        synced_description_hash=synced_hash_match.group("value"),
        display_name=_decode_double_quoted_yaml(display_name_match.group("value")),
        short_description=_decode_double_quoted_yaml(short_description_match.group("value")),
        default_prompt=_decode_double_quoted_yaml(default_prompt_match.group("value")),
        allow_implicit_invocation=allow_implicit_match.group("value") == "true",
    )


def _iter_skill_files(repo_root: Path) -> list[Path]:
    skill_files: list[Path] = []
    for pattern in SKILL_GLOB_PATTERNS:
        skill_files.extend(sorted(repo_root.glob(pattern)))
    return skill_files


def _validate_reference_paths(skill_file: Path, errors: list[str]) -> None:
    text = skill_file.read_text(encoding="utf-8")
    for rel_path, _prefix in REFERENCE_PATH_RE.findall(text):
        resolved = (skill_file.parent / rel_path).resolve()
        if not resolved.exists():
            errors.append(f"{skill_file}: missing referenced file {rel_path}")


def _validate_banned_skill_body_patterns(skill_file: Path, errors: list[str]) -> None:
    text = skill_file.read_text(encoding="utf-8")
    for pattern in BANNED_SKILL_BODY_PATTERNS:
        if pattern in text:
            errors.append(f"{skill_file}: banned host-specific wording `{pattern}`")


def _validate_routed_skill_names(
    skill_file: Path,
    canonical_skill_names: set[str],
    errors: list[str],
) -> None:
    text = skill_file.read_text(encoding="utf-8")
    for routed_name in ROUTED_SKILL_RE.findall(text):
        if routed_name not in canonical_skill_names:
            errors.append(
                f"{skill_file}: routed skill name `{routed_name}` does not match any frontmatter name"
            )


def _validate_metadata(skill_file: Path, frontmatter: SkillFrontmatter, errors: list[str]) -> None:
    metadata_path = skill_file.parent / "agents" / "openai.yaml"
    if not metadata_path.exists():
        errors.append(f"{skill_file}: missing agents/openai.yaml metadata")
        return

    try:
        metadata = _parse_metadata_file(metadata_path)
    except ValueError as exc:
        errors.append(str(exc))
        return

    expected_hash = hashlib.sha256(frontmatter.description.encode("utf-8")).hexdigest()
    expected_allow_implicit = not frontmatter.disable_model_invocation

    if metadata.synced_name != frontmatter.name:
        errors.append(
            f"{metadata_path}: synced skill name `{metadata.synced_name}` does not match `{frontmatter.name}`"
        )

    if metadata.synced_description_hash != expected_hash:
        errors.append(f"{metadata_path}: synced description hash is stale relative to SKILL.md")

    if not metadata.display_name.strip():
        errors.append(f"{metadata_path}: interface.display_name must not be empty")

    short_len = len(metadata.short_description)
    if not (25 <= short_len <= 64):
        errors.append(
            f"{metadata_path}: interface.short_description must be 25-64 characters (got {short_len})"
        )

    if f"${frontmatter.name}" not in metadata.default_prompt:
        errors.append(f"{metadata_path}: interface.default_prompt must reference ${frontmatter.name}")

    if metadata.allow_implicit_invocation != expected_allow_implicit:
        expected_value = "true" if expected_allow_implicit else "false"
        errors.append(
            f"{metadata_path}: policy.allow_implicit_invocation must be {expected_value}"
        )


def _validate_scaffold_contract(skill_file: Path, frontmatter: SkillFrontmatter, errors: list[str]) -> None:
    if frontmatter.name not in SCAFFOLD_CAPABLE_SKILLS:
        return

    text = skill_file.read_text(encoding="utf-8")
    if "scaffolded" not in text or "production-ready" not in text:
        errors.append(
            f"{skill_file}: scaffold-capable skill must declare both `scaffolded` and `production-ready` states"
        )


def _validate_scaffold_marketing(repo_root: Path, errors: list[str]) -> None:
    readme = (repo_root / "README.md").read_text(encoding="utf-8")

    if "scaffolded" not in readme or "production-ready" not in readme:
        errors.append("README.md: missing scaffolded vs production-ready wording")

    for pattern in STALE_SCAFFOLD_MARKETING_PATTERNS:
        if pattern in readme:
            errors.append(f"README.md: stale scaffold wording `{pattern}`")


def _validate_astro_imports(repo_root: Path, errors: list[str]) -> None:
    astro_refs = sorted(
        (repo_root / "skills" / "datocms-frontend-integrations" / "references").glob("astro*.md")
    )
    for astro_ref in astro_refs:
        text = astro_ref.read_text(encoding="utf-8")
        if "from '@datocms/astro'" in text:
            errors.append(
                f"{astro_ref}: Astro references must use subpath imports, not `from '@datocms/astro'`"
            )


def _validate_clean_git(repo_root: Path, errors: list[str]) -> None:
    completed = subprocess.run(
        ["git", "-C", str(repo_root), "status", "--short"],
        capture_output=True,
        text=True,
        check=False,
    )

    if completed.returncode != 0:
        errors.append("git status --short failed during clean-tree validation")
        return

    remaining = []
    for line in completed.stdout.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if any(stripped.startswith(prefix) for prefix in IGNORED_GIT_STATUS_PREFIXES):
            continue
        remaining.append(stripped)

    if remaining:
        preview = ", ".join(remaining[:8])
        if len(remaining) > 8:
            preview += ", ..."
        errors.append(f"git status is not clean: {preview}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate DatoCMS skill repo invariants")
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root containing the skill folders (default: .)",
    )
    parser.add_argument(
        "--require-clean-git",
        action="store_true",
        help="Fail if `git status --short` is not clean, ignoring known local-only paths.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()

    skill_files = _iter_skill_files(repo_root)
    if not skill_files:
        raise ValueError(f"{repo_root}: no SKILL.md files found in expected repo layout")

    frontmatter_by_path = {path: _extract_frontmatter(path) for path in skill_files}
    canonical_skill_names = {frontmatter.name for frontmatter in frontmatter_by_path.values()}

    errors: list[str] = []

    for skill_file, frontmatter in frontmatter_by_path.items():
        _validate_reference_paths(skill_file, errors)
        _validate_banned_skill_body_patterns(skill_file, errors)
        _validate_routed_skill_names(skill_file, canonical_skill_names, errors)
        _validate_metadata(skill_file, frontmatter, errors)
        _validate_scaffold_contract(skill_file, frontmatter, errors)

    _validate_scaffold_marketing(repo_root, errors)
    _validate_astro_imports(repo_root, errors)

    if args.require_clean_git:
        _validate_clean_git(repo_root, errors)

    if errors:
        print("[fail] skill repo validation failed")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"[ok] validated {len(skill_files)} skills")
    print("[ok] reference paths resolve")
    print("[ok] metadata files are present and synced")
    print("[ok] routed skill names match frontmatter names")
    print("[ok] scaffold-capable skills declare scaffolded vs production-ready states")
    print("[ok] banned host-specific labels are absent from skill bodies")
    print("[ok] Astro references use subpath imports")
    if args.require_clean_git:
        print("[ok] git status is clean (ignoring local-only excluded paths)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
