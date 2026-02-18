Python Unit Testing Policy


PURPOSE

Defines how unit tests must be written and executed.

Testing must respect:

- Project architecture
- Module execution semantics (python3 -m main)
- Windows environment
- Non-interactive execution
- Separation of concerns
- Production-safe design


CORE PRINCIPLE

Unit tests validate isolated logic.

They must NOT:

- Launch GUI
- Launch terminal mode
- Execute main.py
- Run python3 -m main
- Require user input
- Perform real network calls
- Perform destructive filesystem operations
- Depend on global runtime state


FRAMEWORK

Assume pytest unless explicitly detected otherwise.

Run tests using:

  python3 -m pytest

Do NOT use:

  pytest

Always use module invocation.


TEST STRUCTURE

Location:
  tests/

Naming:
  test_<module>.py

Example:
  tests/
    test_utils.py
    test_parser.py


DISCOVERY RULES

Tests must:

- Not modify sys.path
- Not rely on execution hacks
- Respect real project imports

If module is in root:
  from utils import parse_config

If package-based:
  from mypackage.utils import parse_config


ARCHITECTURE-AWARE REQUIREMENT

Before writing tests:

1. Identify modified files.
2. Understand how they integrate into the project.
3. Classify logic:
   - Pure logic
   - IO-related
   - State-driven
   - Startup-related
4. Define proper isolation boundary.


WHAT TO TEST

Focus on:

- Pure functions
- Business logic
- Data transformations
- Validation logic
- Argument parsing (without app execution)
- Utility modules
- Error handling


WHAT NOT TO TEST

Do NOT:

- Execute main entrypoint
- Trigger GUI/terminal startup
- Depend on interactive flows
- Use real environment unless mocked


MOCKING POLICY

When code depends on:

- Filesystem
- Environment variables
- Time
- External services
- OS behavior

Use mocking:

- unittest.mock
- pytest fixtures
- monkeypatch

Examples:

  monkeypatch.setenv("API_KEY", "test_key")
  patch("module.open")


CHANGED FILE RULE

When code changes:

1. Identify modified files.
2. Determine logic/behavior impact.
3. Update or add tests.
4. Preserve previous coverage.

If behavior changes → test new behavior.
If bug fixed → add test that would previously fail.


TEST DESIGN PRINCIPLES

Each test must:

- Cover one logical behavior
- Have a clear name
- Be deterministic
- Not depend on execution order
- Avoid shared mutable state

Naming examples:

  test_parse_config_returns_dict_when_valid()
  test_parse_config_raises_error_on_missing_file()


ASSERTIONS

Avoid vague assertions:

  assert result

Prefer explicit:

  assert result == expected

Exception testing:

  with pytest.raises(ValueError):
      function_call()


ERROR & EDGE CASES

Always test:

- Expected exceptions
- Invalid input
- Edge cases
- Boundary conditions


FILESYSTEM RULE

If filesystem interaction required:

- Use tmp_path fixture
- Do not write to project root
- Do not modify real configs
- Do not modify main.py


ENTRYPOINT RULE

Tests must NOT rely on:

  if __name__ == "__main__":

Import functions directly and test in isolation.


NO SIDE EFFECT RULE

Tests must:

- Not alter global state
- Not persist environment changes
- Not leave residual files
- Not modify configuration permanently


PRE-COMMIT VALIDATION

After modifications:

- All related tests pass
- New behavior is covered
- No unrelated tests fail
- Architecture assumptions remain valid


COVERAGE (OPTIONAL)

If coverage exists:

  python3 -m pytest --cov

Do not enforce arbitrary thresholds unless defined.


STRICT BOUNDARY

Unit testing = logic verification only.

Integration (GUI/terminal execution) must NOT be triggered automatically.


ABSOLUTE RULE

Testing must be:

- Structured
- Isolated
- Architecture-aware
- Deterministic
- Non-interactive
- Safe for Windows PowerShell environment

Unit tests must increase confidence
without executing the application runtime.
