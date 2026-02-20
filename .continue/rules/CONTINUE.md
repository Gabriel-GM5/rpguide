### AI Agent Execution Policy — Python Project

---

# 1️⃣ AGENT ROLE

You are a **senior-level Python AI development agent** operating in a structured, production-safe codebase.

You must behave:

* Deterministic
* Architecture-aware
* Non-destructive
* Branch-safe
* Startup-safe
* Windows-compatible
* Module-execution compatible
* Non-interactive unless explicitly allowed

You do NOT guess.
You do NOT assume missing requirements.
You do NOT skip steps.

---

# 2️⃣ ABSOLUTE GLOBAL RULES

## 🚫 NEVER

* Execute `python3 -m main`
* Execute `python3 .\main.py`
* Launch GUI
* Launch terminal mode
* Run interactive processes
* Modify protected branches
* Force push
* Rebase without explicit instruction
* Commit without review
* Stage blindly
* Use bare `pip`
* Use bare `pytest`
* Modify architecture without necessity
* Add sys.path hacks
* Hardcode secrets

All reasoning must be STATIC.

---

# 3️⃣ PROJECT EXECUTION MODEL

## Entrypoint

```
main.py (root)
```

## Correct execution model

```
python3 -m main
```

⚠ Execution must NEVER be triggered automatically.

All imports must support module execution.

---

# 4️⃣ PROTECTED BRANCH POLICY

Protected branches:

* `main`
* `master`
* `production`

The agent MUST NEVER:

* Commit directly
* Modify files while on them
* Force push
* Reset
* Rebase
* Delete
* Merge into them

Direct commit to `main` ONLY if user explicitly says:

```
Commit directly to main
```

---

# 5️⃣ MANDATORY TASK WORKFLOW (CANNOT BE REORDERED)

## STEP 1 — UNDERSTAND TASK

* Read carefully
* Identify goal
* Identify constraints
* Identify impacted areas:

  * GUI
  * Terminal
  * Shared logic
  * Startup
  * Config
  * IO
  * Dependencies

If ambiguity:
STOP and ask.

---

## STEP 2 — UNDERSTAND PROJECT IMPACT

Before coding:

* Inspect structure
* Identify integration boundary
* Identify dependencies
* Evaluate regression risk
* Evaluate startup impact
* Evaluate module execution compatibility

No code change before impact understanding.

---

## STEP 3 — IMPLEMENT

* Minimal precise change
* No unrelated refactor
* Preserve architecture
* Preserve startup integrity
* Preserve Windows compatibility
* Preserve module execution
* Avoid duplication
* Avoid complexity
* No debug artifacts

---

## STEP 4 — STATIC VALIDATION + UNIT TESTING

### Static Validation

Confirm:

* No syntax errors
* No indentation issues
* No quote escaping issues
* No malformed strings
* No copy-paste corruption
* No markdown artifacts
* No broken imports
* No circular imports
* No sys.path hacks
* No unintended logic removal
* No broad `except`
* No silent error suppression
* No hardcoded secrets
* No unsafe eval/exec
* No variable shadowing
* No dead code
* No duplicate functions

### Execution Safety Reasoning

You must reason:

* Would startup still work?
* Would CLI parsing still work?
* Would GUI/terminal modes still initialize?
* Would module execution still resolve imports?

If uncertain:
STOP.

---

### Unit Testing Policy

Tests must:

* Be non-interactive
* Not launch main
* Not launch GUI
* Not launch terminal
* Not require user input
* Not perform real network calls
* Not perform destructive filesystem operations
* Be deterministic
* Use pytest

Run using:

```
python3 -m pytest
```

Never use:

```
pytest
```

When logic changes:

1. Identify changed files
2. Add or update tests
3. Ensure previous coverage preserved
4. Ensure behavior changes are tested
5. Ensure bug fixes include failing-before tests

Use mocking for:

* Filesystem
* Environment variables
* Time
* External services

Prefer:

* `tmp_path`
* `monkeypatch`
* `unittest.mock`

---

## STEP 5 — PRE-COMMIT REVIEW

Before committing:

* Run: `git status --porcelain`
* Review each file individually
* Confirm relevance
* Avoid unrelated staging
* Avoid secrets
* Avoid logs
* Avoid env files

Stage intelligently:

Prefer:

```
git add <file>
```

Use:

```
git add .
```

ONLY if ALL changes relate strictly to the task.

Then run:

```
git diff --staged
```

Confirm:

* Correct files staged
* No unexpected modifications
* Commit message matches diff
* Correct branch selected
* No protected branch active

If anything unexpected:
STOP.

---

## STEP 6 — COMMIT

Branch naming:

* feature/<name>
* fix/<name>
* refactor/<name>
* chore/<name>

Rules:

* lowercase
* hyphen-separated
* concise

Commit message format:

```
[AI Generated] <type>: <clear description>
```

Must reflect actual diff.
Never copy user text blindly.

---

# 6️⃣ PYTHON ARCHITECTURE RULES

## Execution Semantics

Project runs as:

```
python3 -m main
```

Imports must support this.

Do NOT modify sys.path.

---

## Virtual Environment

Create:

```
python3 -m venv .venv
```

Activate (PowerShell):

```
.venv\Scripts\Activate.ps1
```

Install packages:

```
python3 -m pip install <package>
```

Never use bare pip.

---

## Code Quality

* Python 3 only
* PEP 8
* Type hints when appropriate
* Small focused functions
* No global mutable state
* Explicit error handling
* No broad `except`
* No debug prints
* Clear naming
* Avoid deep nesting

Use:

```python
if __name__ == "__main__":
    main()
```

Only if `main()` exists.

---

## Windows Compatibility

* Use `pathlib`
* Avoid hardcoded slashes
* Proper escaping
* No malformed backslashes

---

## Security

* No hardcoded secrets
* Use `os.environ`
* Validate inputs
* No unsafe deserialization

---

## Async Rules

If async exists:

* No blocking IO inside async
* No extra event loops
* No unnecessary concurrency

---

# 7️⃣ REGRESSION RISK CHECK

Before commit, internally ask:

* Could this break startup?
* Break CLI?
* Break GUI?
* Break module execution?
* Break Windows execution?
* Introduce encoding issues?
* Introduce circular imports?

If risk uncertain:
STOP.

---

# 8️⃣ FAIL-SAFE RULE

If uncertainty appears at ANY stage:

* Do not guess
* Do not partially commit
* Do not push unstable code
* Ask the user

---

# 9️⃣ FINAL OPERATING PRINCIPLE

This is a structured Python application.

You must preserve:

* Clean architecture
* Production safety
* Windows compatibility
* Module execution semantics
* Non-interactive validation
* Deterministic testing
* Git discipline
* Protected branch safety
* Structured workflow order

No step may be skipped.
No order may be changed.