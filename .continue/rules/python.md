Python Project Rules and Environment Definition


PROJECT DECLARATION

This is a Python project.

The application entrypoint is:

main.py

Location:
Project root directory.

The application must be executed using module mode:

python3 -m main

Do NOT run:
python main.py

Module execution is mandatory to ensure correct package resolution and import behavior.


CRITICAL RULE — NO LIVE RUNTIME EXECUTION

The agent MUST NOT execute the application interactively.

The agent MUST NOT run:

python3 -m main
python3 .\main.py gui
python3 .\main.py terminal

The application may require user interaction and must NOT be executed automatically.

NO live runtime tests.
NO interactive execution.
NO fire tests.

Validation must be STATIC ONLY.


ALLOWED VALIDATION METHODS

The agent may:

- Perform static code analysis
- Check imports logically
- Review syntax
- Inspect code structure
- Validate argument parsing logic by inspection
- Run non-interactive tooling (if confirmed safe)

The agent must NOT execute any command that launches the application interface.


PYTHON VERSION AND EXECUTION

The agent must assume:

- Python 3 environment
- python3 command is available
- Virtual environments are expected

Before executing Python-related commands (non-interactive only), the agent may verify:

python3 --version

If dependencies are required, use:

python3 -m pip install <package>

Never assume global pip without module invocation.


VIRTUAL ENVIRONMENT RULE

The project should use a virtual environment.

Preferred creation:

python3 -m venv .venv

Activation (PowerShell):

.venv\Scripts\Activate.ps1

If the virtual environment is not activated, the agent should recommend activation before installing dependencies.

The agent must NOT automatically recreate or delete environments.


PROJECT STRUCTURE ASSUMPTIONS

- main.py is the application entrypoint.
- Source files should be modular and organized.
- Avoid placing large logic blocks directly inside main.py.
- Use functions and modules.
- Avoid circular imports.
- Use absolute imports where appropriate.

The agent must not restructure the project without clear intent.


IMPORT BEHAVIOR

Because execution uses:

python3 -m main

- Imports must be compatible with module execution.
- Avoid relying on relative path hacks.
- Do NOT modify sys.path unless explicitly required and justified.
- Do NOT use runtime path manipulation as a default solution.


DEPENDENCY MANAGEMENT

If dependency management is present, prefer:

- requirements.txt
- pyproject.toml

Install dependencies using:

python3 -m pip install -r requirements.txt

Do NOT assume poetry or pipenv unless explicitly detected.

Before using any tool, verify its presence.

The agent must not automatically upgrade all dependencies unless explicitly requested.


CODE STYLE AND BEST PRACTICES

The agent must follow modern Python best practices:

- Use Python 3 syntax only.
- Use type hints where appropriate.
- Follow PEP 8 style guidelines.
- Prefer explicit over implicit.
- Avoid global mutable state.
- Keep functions small and focused.
- Use descriptive variable names.
- Avoid deeply nested logic.
- Handle exceptions explicitly.
- Avoid bare except blocks.

Use:

if __name__ == "__main__":
    main()

Only if main.py internally calls a main() function.
Otherwise rely on module execution entry.


ERROR HANDLING

- Raise specific exceptions.
- Do not suppress errors silently.
- Log meaningful error messages.
- Avoid swallowing stack traces unless intentionally handled.


TESTING POLICY

If automated tests exist (e.g., pytest), they may be executed ONLY if:

- They are non-interactive.
- They do not launch GUI or terminal modes.
- They do not require user input.

Run tests using:

python3 -m pytest

Do NOT create artificial runtime tests.
Do NOT simulate user interaction.


FORMATTING AND LINTING

If formatting tools are present, prefer:

- black
- ruff
- flake8

Verify existence before use:

python3 -m black --version

Do not assume availability.


FILE PATH RULES (WINDOWS ENVIRONMENT)

- Use Windows-compatible paths.
- Prefer pathlib over string-based paths.
- Avoid hardcoding forward slashes.
- Use pathlib.Path for file manipulation.
- Ensure proper escaping of backslashes.


ASYNC AND CONCURRENCY

If async code is used:

- Use asyncio properly.
- Avoid mixing blocking IO inside async functions.
- Do not create new event loops unnecessarily.
- Do not introduce concurrency unless required.


SECURITY PRACTICES

- Never hardcode secrets.
- Use environment variables via:
  os.environ
- Validate external input.
- Avoid eval or exec unless explicitly required.
- Avoid insecure deserialization.


PERFORMANCE PRACTICES

- Avoid premature optimization.
- Avoid unnecessary global caching.
- Avoid excessive object creation inside tight loops.
- Prefer built-in libraries over custom implementations when appropriate.


ABSOLUTE RULE

The agent must treat this as a structured Python application executed via:

python3 -m main

However:

Execution must NOT be triggered automatically.

All validation must be static and non-interactive.

All development decisions must respect:

- Windows environment
- PowerShell shell rules
- Python 3 module execution semantics
- Clean project architecture
- Maintainable and production-safe Python code
- No automatic runtime execution
