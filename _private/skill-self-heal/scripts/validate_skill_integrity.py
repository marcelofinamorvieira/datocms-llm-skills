#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
CODE_PATH_RE = re.compile(r"`((?:references|scripts|assets|\.\./)[^`\n]+)`")


def find_public_skill_files(repo_root: Path) -> list[Path]:
    skill_files: list[Path] = []
    for child in sorted(repo_root.iterdir()):
        if not child.is_dir() or child.name in {".git", "_private", "evals"}:
            continue
        skill_path = child / "SKILL.md"
        if skill_path.is_file():
            skill_files.append(skill_path)
    return skill_files


def frontmatter_block(text: str) -> str | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    return text[4:end]


def has_required_frontmatter(block: str) -> tuple[bool, bool]:
    has_name = bool(re.search(r"(?m)^name:\s*\S", block))
    has_description = bool(re.search(r"(?m)^description:\s*", block))
    return has_name, has_description


def normalize_link_target(raw: str) -> str:
    target = raw.strip()
    target = target.split("#", 1)[0]
    return target


def is_local_skill_reference(target: str) -> bool:
    if not target:
        return False
    if target.startswith(("http://", "https://", "mailto:", "#", "/")):
        return False
    return target.startswith(("references/", "scripts/", "assets/", "../"))


def extract_references(text: str) -> Iterable[str]:
    for match in LINK_RE.finditer(text):
        normalized = normalize_link_target(match.group(1))
        if is_local_skill_reference(normalized):
            yield normalized

    for match in CODE_PATH_RE.finditer(text):
        normalized = normalize_link_target(match.group(1).strip())
        if is_local_skill_reference(normalized):
            yield normalized


def check_references(skill_file: Path, text: str) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for ref in extract_references(text):
        if ref in seen:
            continue
        seen.add(ref)
        target = (skill_file.parent / ref).resolve()
        if not target.exists():
            errors.append(f"{skill_file}: missing reference target '{ref}'")
    return errors


def check_routing_contract(skill_file: Path, text: str) -> list[str]:
    errors: list[str] = []
    required_tokens = [
        "LLM Failure Observer and Self-Heal Routing",
        "Skill Failure Packet v1",
        "$skill-self-heal",
    ]
    for token in required_tokens:
        if token not in text:
            errors.append(f"{skill_file}: missing routing token '{token}'")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate skill integrity and routing contract.")
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    private_skill = repo_root / "_private" / "skill-self-heal" / "SKILL.md"

    errors: list[str] = []

    if not private_skill.exists():
        errors.append(f"Missing private maintainer skill: {private_skill}")

    public_skills = find_public_skill_files(repo_root)
    if not public_skills:
        errors.append(f"No public skill files found under {repo_root}")

    for skill_file in public_skills:
        text = skill_file.read_text(encoding="utf-8")
        block = frontmatter_block(text)
        if block is None:
            errors.append(f"{skill_file}: missing or malformed frontmatter block")
            continue

        has_name, has_description = has_required_frontmatter(block)
        if not has_name:
            errors.append(f"{skill_file}: frontmatter missing 'name'")
        if not has_description:
            errors.append(f"{skill_file}: frontmatter missing 'description'")

        errors.extend(check_references(skill_file, text))
        errors.extend(check_routing_contract(skill_file, text))

    if errors:
        print("VALIDATION_RESULT: FAIL")
        for err in errors:
            print(f"- {err}")
        return 1

    print("VALIDATION_RESULT: PASS")
    print(f"Validated {len(public_skills)} public skill files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
