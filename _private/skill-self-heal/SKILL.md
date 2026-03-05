---
name: skill-self-heal
description: >-
  Diagnose and repair broken or degraded skills using structured failure packets
  from the runtime LLM. Use when a skill run hits knowledge gaps,
  inaccuracies/conflicts, context bloat, missing dependencies/files, or output
  contract failures and needs validated auto-repair with rollback on failure.
---

# Skill Self-Heal

You repair skill definitions after a runtime LLM detects a hard failure. Follow these steps in order. Do not skip steps.

---

## Step 1: Intake Failure Packet

Require a complete `Skill Failure Packet v1` before editing files.

If required fields are missing, stop and request a corrected packet.

Required fields:
1. `packet_version` (must be `v1`)
2. `source_skill`
3. `timestamp`
4. `hard_failure_type`
5. `failing_step`
6. `user_request`
7. `attempted_actions`
8. `evidence`
9. `candidate_files`
10. `confidence`
11. `stop_reason`

Allowed `hard_failure_type` values:
1. `knowledge_gap`
2. `inaccuracy_or_conflict`
3. `context_bloat_or_ambiguity`
4. `missing_dependency_or_file`
5. `invalid_output_contract`

---

## Step 2: Reproduce Minimally

1. Reproduce only the failing step, not the full user workflow.
2. Confirm at least one concrete evidence item from the packet.
3. Narrow repair scope to the smallest set of files in `candidate_files`.
4. If packet evidence is weak, open only the minimum extra file context required.

---

## Step 3: Plan the Minimal Repair

Select one primary repair path:
1. Frontmatter/trigger mismatch
2. Missing or wrong resource path
3. Contradictory instructions
4. Context bloat reduction (move details to `references/`)
5. Output contract corrections

Rules:
1. Edit tracked skill files directly in this repository.
2. Keep changes minimal and deterministic.
3. Preserve valid existing behavior outside the failing path.

---

## Step 4: Apply Repair with Rollback Guard

Use `scripts/apply_with_rollback.sh` to protect edits:

```bash
bash _private/skill-self-heal/scripts/apply_with_rollback.sh \
  --repo-root /absolute/repo/path \
  --files /absolute/path/to/file1,/absolute/path/to/file2 \
  --change-cmd "<mutating command>" \
  --validate-cmd "python3 _private/skill-self-heal/scripts/validate_skill_integrity.py --repo-root /absolute/repo/path"
```

If validation fails, the script must restore all touched files.

---

## Step 5: Validate

Run:

```bash
python3 _private/skill-self-heal/scripts/validate_skill_integrity.py --repo-root /absolute/repo/path
```

Validation must confirm:
1. Public skill frontmatter has `name` and `description`.
2. Skill-local references to `references/`, `scripts/`, `assets/`, and `../` targets resolve.
3. Routing references to `$skill-self-heal` and `Skill Failure Packet v1` exist in public `SKILL.md` files.

If any check fails, repair is invalid.

---

## Step 6: Return Skill Repair Report v1

Return this exact contract:

```json
{
  "report_version": "v1",
  "source_packet_id": "string",
  "files_changed": ["/absolute/path"],
  "validation_results": [
    { "name": "string", "pass": true, "evidence": "string" }
  ],
  "rolled_back": false,
  "root_cause": "string",
  "fix_summary": "string",
  "followups": ["string"]
}
```

Set `rolled_back` to `true` when rollback was triggered.

---

## Operational Rules

1. Do not continue normal task execution after a hard failure until repair is complete.
2. Do not widen scope beyond packet-driven root cause.
3. Do not modify `_private/skill-self-heal` itself unless explicitly requested.
4. Prefer shorter `SKILL.md` bodies and move detailed content into `references/`.
