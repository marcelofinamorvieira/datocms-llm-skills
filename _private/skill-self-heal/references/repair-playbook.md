# Repair Playbook

Use this mapping from failure type to repair strategy.

## `knowledge_gap`

1. Identify missing knowledge location.
2. Add concise procedural guidance to `SKILL.md`.
3. Move heavy detail to `references/` if needed.
4. Add or fix reference links.

## `inaccuracy_or_conflict`

1. Locate contradictory instructions.
2. Keep one authoritative path and remove the conflicting path.
3. Ensure ordering and stop conditions are explicit.

## `context_bloat_or_ambiguity`

1. Remove duplicated or non-essential text.
2. Keep critical workflow in `SKILL.md`.
3. Move details to `references/` and link from `SKILL.md`.

## `missing_dependency_or_file`

1. Verify referenced path exists.
2. Fix wrong relative paths.
3. Create missing local reference file only when necessary.

## `invalid_output_contract`

1. Compare expected output schema to current instructions.
2. Add explicit field requirements and examples.
3. Validate the contract appears exactly once in canonical form.

## Completion Rules

1. Run validation after edits.
2. Roll back on validation failure.
3. Return `Skill Repair Report v1` with changed files and validation evidence.
