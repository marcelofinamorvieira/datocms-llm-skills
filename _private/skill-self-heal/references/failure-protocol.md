# Failure Protocol

This document defines how runtime LLMs escalate failures to `skill-self-heal`.

## Runtime Observer

The runtime LLM using a skill is the failure observer. Skill files do not self-detect failures.

## Hard Failure Types

1. `knowledge_gap`: Required knowledge is missing or stale enough to block reliable output.
2. `inaccuracy_or_conflict`: Instructions or facts conflict, causing unreliable behavior.
3. `context_bloat_or_ambiguity`: Excessive or noisy instructions prevent stable execution.
4. `missing_dependency_or_file`: Required file/path/dependency is unavailable.
5. `invalid_output_contract`: Output shape or required interface cannot be satisfied.

## Trigger Rule

On first hard failure:
1. Stop normal execution.
2. Emit `Skill Failure Packet v1`.
3. Invoke `$skill-self-heal`.
4. Resume original task only after `Skill Repair Report v1`.

## Skill Failure Packet v1

```json
{
  "packet_version": "v1",
  "source_skill": "string",
  "timestamp": "ISO-8601 string",
  "hard_failure_type": "knowledge_gap|inaccuracy_or_conflict|context_bloat_or_ambiguity|missing_dependency_or_file|invalid_output_contract",
  "failing_step": "string",
  "user_request": "string",
  "attempted_actions": ["string"],
  "evidence": ["string"],
  "candidate_files": ["/absolute/path"],
  "confidence": 0.0,
  "stop_reason": "string"
}
```

## Emission Quality Rules

1. Include concrete evidence strings (error text, missing path, conflicting line references).
2. Keep `candidate_files` constrained to relevant absolute paths.
3. Set confidence from 0.0 to 1.0 based on evidence quality.
4. Avoid speculation in `stop_reason`; state objective blocker only.
