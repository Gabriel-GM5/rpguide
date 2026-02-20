Task Execution Workflow Policy


PURPOSE

Defines the mandatory workflow for ANY task.

No step may be skipped.
Order may not be changed.


STEP 1 — UNDERSTAND THE TASK

Before modifying code:

- Read the task carefully.
- Identify goal and expected behavior.
- Identify constraints.
- Identify affected areas:
  - GUI mode
  - Terminal mode
  - Shared logic
  - Startup behavior
  - Filesystem
  - Configuration
  - Dependencies

If ambiguity exists:
STOP.
Ask for clarification.

Never assume missing requirements.


STEP 2 — UNDERSTAND THE PROJECT

Before changes:

- Inspect project structure.
- Identify entrypoint (main.py at root).
- Understand execution flow:
    python3 .\main.py gui
    python3 .\main.py terminal
- Identify impacted modules.
- Identify dependencies between files.
- Evaluate side effects.
- Determine correct integration boundary.

The agent must know:

- Where change belongs.
- What existing behavior could be affected.
- Architectural constraints.

No modification before integration impact is understood.


STEP 3 — IMPLEMENT

Only after Steps 1–2:

- Apply minimal, precise changes.
- Avoid unrelated refactoring.
- Avoid structural changes unless required.
- Maintain Windows compatibility.
- Preserve startup integrity.
- Preserve GUI/Terminal compatibility.
- Avoid duplicated logic.
- Avoid unnecessary complexity.
- Preserve existing behavior unless instructed otherwise.

Code must be clean and production-safe.


STEP 4 — TEST (MANDATORY)

After implementation, validate:

Technical validation:
- Imports resolve
- No syntax errors
- Correct indentation
- Proper escaping
- No debug artifacts
- No partial edits

Execution validation:
    python3 .\main.py gui
    python3 .\main.py terminal

Application integrity must remain intact.

Unit testing validation:

- Identify changed files.
- Determine if logic/behavior changed.
- Add or update unit tests accordingly.
- Ensure new behavior is covered.
- Ensure bug fixes include failing-before tests.
- Ensure no existing tests break.

Run tests using:

    python3 -m pytest

If available, optional coverage:

    python3 -m pytest --cov

Unit tests must be:
- Isolated
- Deterministic
- Non-interactive
- Architecture-aware

If execution or tests are uncertain:
STOP.
Do not proceed.


STEP 5 — REVIEW

Before commit:

- Review full diff.
- Confirm only relevant files changed.
- Confirm no unintended edits.
- Confirm no formatting corruption.
- Confirm no residual artifacts.
- Validate logical correctness.
- Evaluate regression risk.
- Evaluate startup risk.
- Ensure tests properly reflect changes and there are no test errors.

If risk or uncertainty exists:
STOP.
Ask for clarification.


STEP 6 — COMMIT

Only after:

1. Task understood
2. Project impact understood
3. Implementation complete
4. Testing (including unit tests) passed
5. Review complete

Commit rules:

- Use proper branch (never protected branches).
- Include tag: [AI Generated]
- Message must accurately describe change.
- Must reflect actual diff.


MANDATORY ORDER

Strict sequence:

1. Understand task
2. Understand project
3. Implement
4. Test (includes unit testing)
5. Review
6. Commit

Reordering is forbidden.
Skipping is forbidden.


FAIL-SAFE RULE

If uncertainty appears at any stage:

- Do not guess.
- Do not partially commit.
- Do not push unstable code.

Instead:
Ask the user.
