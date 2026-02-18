Python Project Rules


PROJECT DECLARATION

- This is a Python 3 project.
- Entrypoint: main.py (project root)
- Execution mode:
    python3 -m main
- Never use:
    python main.py
- Module execution is mandatory (correct import resolution).


ABSOLUTE RULE — NO RUNTIME EXECUTION

The agent MUST NOT run:

- python3 -m main
- python3 .\main.py gui
- python3 .\main.py terminal

No interactive execution.
No GUI launch.
No terminal launch.
No fire tests.

All validation must be STATIC only.


ALLOWED VALIDATION

The agent may:

- Perform static analysis
- Review syntax and imports
- Inspect architecture
- Validate logic by reasoning
- Run non-interactive tools (if safe)

The agent must NOT execute anything that launches the application.


PYTHON ENVIRONMENT

Assume:

- Python 3
- python3 command available
- Virtual environments expected

Verify version (if needed):
    python3 --version

Install packages using:
    python3 -m pip install <package>

Never use bare pip.


VIRTUAL ENVIRONMENT

Preferred creation:
    python3 -m venv .venv

PowerShell activation:
    .venv\Scripts\Activate.ps1

Do not auto-delete or recreate environments.
Recommend activation if missing.


PROJECT STRUCTURE RULES

- main.py is entrypoint.
- Keep logic modular.
- Avoid large logic blocks in main.py.
- Avoid circular imports.
- Prefer absolute imports.
- Do not restructure architecture without explicit intent.


IMPORT RULES

Because execution is:
    python3 -m main

- Imports must support module execution.
- Do NOT modify sys.path unless explicitly justified.
- Do NOT rely on path hacks.


DEPENDENCIES

Prefer:
- requirements.txt
- pyproject.toml

Install via:
    python3 -m pip install -r requirements.txt

Do not assume poetry/pipenv.
Do not auto-upgrade dependencies.


CODE QUALITY

Follow modern Python best practices:

- Python 3 syntax only
- Type hints when appropriate
- PEP 8
- Small focused functions
- Explicit error handling
- No bare except
- Avoid global mutable state
- Clear naming
- Avoid deep nesting

Use:

if __name__ == "__main__":
    main()

Only if main() exists.


TESTING RULE

Tests (e.g., pytest) may run ONLY if:

- Non-interactive
- Do not launch GUI
- Do not launch terminal
- Do not require user input

Run using:
    python3 -m pytest

Never create artificial runtime tests.


FORMATTING / LINTING

If available:
- black
- ruff
- flake8

Verify before use:
    python3 -m black --version

Do not assume tools exist.


WINDOWS PATH RULES

- Windows-compatible paths only
- Prefer pathlib
- Avoid hardcoded slashes
- Ensure proper escaping


ASYNC RULES

If async exists:

- Use asyncio correctly
- Avoid blocking IO inside async
- Do not create extra event loops
- Do not introduce concurrency unless required


SECURITY

- No hardcoded secrets
- Use os.environ for config
- Validate input
- Avoid eval/exec unless explicitly required
- Avoid insecure deserialization


PERFORMANCE

- No premature optimization
- Avoid unnecessary global caching
- Avoid excessive object creation
- Prefer standard library


FINAL RULE

Treat this as a structured Python application executed via:

    python3 -m main

BUT:

Execution must NEVER be triggered automatically.

All reasoning must be static.
All changes must preserve architecture.
All decisions must respect:

- Windows + PowerShell environment
- Python 3 module semantics
- Clean architecture
- Maintainability
- Production safety
- Non-interactive validation only
