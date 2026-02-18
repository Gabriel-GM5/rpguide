Task Execution Workflow Policy


PURPOSE

This file defines the mandatory workflow the agent must follow for ANY task, regardless of size or complexity.

No step may be skipped.


STEP 1 — UNDERSTAND THE TASK

Before writing or modifying any code, the agent must:

- Carefully read the task.
- Identify the goal.
- Identify constraints.
- Identify expected output or behavior.
- Identify whether the task affects:
  - GUI mode
  - Terminal mode
  - Shared logic
  - Startup behavior
  - File system operations
  - Configuration
  - Dependencies

If any part of the task is ambiguous:
STOP.
Ask for clarification before proceeding.

The agent must never assume missing requirements.


STEP 2 — UNDERSTAND THE PROJECT

Before making changes, the agent must:

- Inspect the project structure.
- Identify entrypoint (main.py at project root).
- Understand how execution flows for:
  python3 .\main.py gui
  python3 .\main.py terminal
- Identify modules impacted by the task.
- Identify dependencies between files.
- Evaluate potential side effects.

The agent must determine:

- Where the change belongs.
- Whether existing functionality could be affected.
- Whether architecture constraints exist.

No code modification is allowed before understanding integration impact.


STEP 3 — IMPLEMENT THE CHANGE

Only after Steps 1 and 2 are complete:

- Implement minimal, precise changes.
- Avoid unrelated refactoring.
- Avoid structural modifications unless required.
- Follow Python best practices.
- Maintain Windows compatibility.
- Maintain correct escaping.
- Maintain startup integrity.
- Maintain GUI and Terminal mode compatibility.

The agent must:

- Write clean code.
- Avoid duplicated logic.
- Avoid introducing unnecessary complexity.
- Preserve existing behavior unless explicitly instructed otherwise.


STEP 4 — TEST

After implementation, the agent must validate:

- Imports resolve correctly.
- No syntax errors exist.
- Indentation is correct.
- Strings are properly escaped.
- No partial copy-paste artifacts remain.
- No debug code remains.

The agent must ensure the application can still be executed in both modes:

python3 .\main.py gui
python3 .\main.py terminal

If execution integrity is uncertain:
STOP.
Do not proceed to commit.


STEP 5 — REVIEW

Before committing:

- Review full diff.
- Confirm only relevant files changed.
- Confirm no unintended edits occurred.
- Confirm no formatting corruption.
- Confirm no trailing artifacts.
- Confirm commit message reflects actual change.
- Evaluate regression risk.
- Evaluate startup risk.
- Evaluate logical correctness.

If any risk is unclear:
STOP.
Ask for clarification.


STEP 6 — COMMIT

Only after successful:

- Task understanding
- Project understanding
- Implementation
- Testing
- Review

The agent may commit.

Commit must:

- Be created on a proper branch (never protected branches).
- Include [AI Generated] tag.
- Accurately describe the change.
- Reflect actual diff content.


MANDATORY EXECUTION ORDER

The workflow order is strictly:

1. Understand the task
2. Understand the project and integration impact
3. Implement
4. Test
5. Review
6. Commit

Reordering is not allowed.

Skipping steps is not allowed.


FAIL-SAFE RULE

If at any stage uncertainty appears:

- Do not guess.
- Do not partially commit.
- Do not push unstable changes.

Instead:
Ask the user.
