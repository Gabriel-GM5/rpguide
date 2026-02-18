Pre-Commit Code Review Rules for AI Agent


PURPOSE

Before committing any change, the agent must perform a structured internal code review.

The goal is to ensure:

- The application still works.
- The code follows best practices.
- No syntax or escaping errors were introduced.
- No accidental copy-paste corruption occurred.
- The change aligns with the task objective.
- The application can still start successfully.


MANDATORY APPLICATION RUNTIME CHECK

This project can be executed in two modes:

GUI mode:
python3 .\main.py gui

Terminal mode:
python3 .\main.py terminal

Before committing significant changes that affect execution flow, CLI behavior, or UI behavior, the agent must:

- Ensure the application still launches.
- Ensure no import errors were introduced.
- Ensure no syntax errors exist.
- Ensure argument handling still works.

If execution could be impacted and verification is not possible:
STOP.
Inform the user.


SYNTAX AND ESCAPING VALIDATION (CRUCIAL)

AI-generated code is prone to escaping and formatting errors.

The agent must carefully verify:

- Correct string quoting.
- Proper escaping of backslashes in Windows paths.
- No broken multiline strings.
- No incorrect indentation.
- No mixed tabs and spaces.
- No broken f-strings.
- No truncated copy-paste blocks.
- No duplicated blocks of code.
- No partially inserted code fragments.
- No malformed docstrings.
- No accidental markdown artifacts inside code.
- No stray backticks.
- No invisible characters.

Backslash handling is critical in Windows:

- Ensure paths like C:\Users\Name are correctly represented.
- Prefer raw strings when appropriate.
- Prefer pathlib over manual path strings.


LOGIC CONSISTENCY CHECK

Before committing, verify:

- The change matches the user’s request.
- No unrelated logic was modified.
- No existing behavior was unintentionally removed.
- No circular imports were introduced.
- No unreachable code was added.
- No dead code remains.
- No duplicate functions were created.
- No variable shadowing issues were introduced.
- No name collisions were introduced.


IMPORT AND STRUCTURE CHECK

- All imports must resolve correctly.
- No unused imports.
- No duplicate imports.
- No incorrect relative imports.
- No sys.path hacks unless explicitly required.
- Module execution via python3 -m main must remain valid.


ERROR HANDLING REVIEW

- No broad "except:" blocks.
- Exceptions must be specific.
- Errors must not be silently swallowed.
- Logging must remain meaningful.
- Do not suppress stack traces without reason.


SECURITY CHECK

- No hardcoded secrets.
- No API keys embedded in code.
- No sensitive data accidentally logged.
- No unsafe eval or exec usage.
- No unsafe deserialization patterns.


FUNCTIONALITY VERIFICATION

If the change affects:

- Argument parsing
- Mode selection (gui or terminal)
- Initialization logic
- Core business logic
- File IO
- Configuration handling

The agent must ensure:

- Both gui and terminal modes still initialize correctly.
- No runtime crash occurs during startup.
- Default behavior remains intact unless intentionally modified.


CODE QUALITY CHECK

Before committing, confirm:

- Code follows PEP 8.
- Functions are reasonably sized.
- Variables are clearly named.
- No unnecessary complexity was added.
- No excessive nesting.
- No global mutable state introduced.
- No debug prints left behind.
- No commented-out legacy blocks left unintentionally.


REGRESSION RISK CHECK

The agent must ask internally:

- Could this break startup?
- Could this break imports?
- Could this break CLI arguments?
- Could this break Windows execution?
- Could this break module execution?
- Could this introduce encoding issues?

If risk is detected and cannot be verified:
STOP.
Ask the user.


FINAL PRE-COMMIT CHECKLIST

Before committing:

- Review changed files.
- Review staged diff.
- Verify logic correctness.
- Verify escaping correctness.
- Verify structural integrity.
- Verify application entrypoint remains valid.
- Verify gui and terminal modes are still callable.
- Confirm commit message accurately reflects changes.
- Confirm no unintended files are staged.


ABSOLUTE RULE

No commit may be created unless the agent is confident that:

- The application can still start using:
  python3 .\main.py gui
  python3 .\main.py terminal

- The change is logically correct.
- No structural or escaping corruption was introduced.
- The codebase remains clean and maintainable.
