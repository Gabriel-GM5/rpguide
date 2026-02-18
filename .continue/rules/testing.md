Python Unit Testing Policy and Implementation Guide


PURPOSE

This document defines how unit tests must be implemented, structured, and executed
within this Python project.

Testing must respect:

- Project architecture
- Module execution semantics (python3 -m main)
- Windows environment
- Non-interactive policy
- Separation of concerns
- Production-safe design


CORE PRINCIPLE

Unit tests must validate isolated logic.

They must NOT:

- Launch GUI mode
- Launch terminal mode
- Require user input
- Perform real external network calls
- Perform destructive filesystem operations
- Depend on global runtime state


TESTING FRAMEWORK

Assume pytest unless another framework is explicitly detected.

Run tests using:

python3 -m pytest

Do NOT use:
pytest (without module invocation)

Always use module invocation form.


TEST DIRECTORY STRUCTURE

Tests must be placed in:

tests/

Naming convention:

test_<module>.py

Example:

tests/
    test_utils.py
    test_parser.py
    test_services.py


TEST DISCOVERY RULE

Tests must:

- Not modify sys.path
- Not rely on relative execution hacks
- Respect module import behavior

Imports inside tests must reflect actual project structure.

Example (if module is in root):

from utils import parse_config

If project uses packages:

from mypackage.utils import parse_config


ARCHITECTURE-AWARE TESTING

Before creating tests, the agent must:

1. Identify which files were modified.
2. Understand how those files integrate into project architecture.
3. Determine whether logic is:
   - Pure logic
   - IO-related
   - State-driven
   - Startup-related
4. Determine correct isolation boundaries.


WHAT TO TEST

Unit tests must focus on:

- Pure functions
- Business logic
- Data transformations
- Validation logic
- Argument parsing logic (without executing full app)
- Utility modules
- Error handling behavior


WHAT NOT TO TEST

Unit tests must NOT:

- Execute main.py
- Execute python3 -m main
- Execute GUI startup
- Execute terminal startup
- Depend on interactive flows
- Rely on real environment variables unless mocked


MOCKING POLICY

When testing code that depends on:

- Filesystem
- Environment variables
- Time
- External services
- OS-specific behavior

Use mocking.

Recommended tools:

- unittest.mock
- pytest fixtures
- monkeypatch (pytest)

Example:

Mock environment variables:
monkeypatch.setenv("API_KEY", "test_key")

Mock filesystem calls:
patch("module.open")


TESTING CHANGED FILES

When code changes occur:

The agent must:

1. Identify modified files.
2. Determine if logic changed.
3. Determine if behavior changed.
4. Add or update unit tests accordingly.
5. Ensure previous test coverage is not broken.

If a change modifies public behavior,
a corresponding test must validate the new behavior.

If a change fixes a bug,
a test must be created that would have failed before the fix.


TEST DESIGN PRINCIPLES

Each test must:

- Test one logical behavior
- Have a clear name
- Have deterministic results
- Not depend on execution order
- Not rely on shared mutable state

Example naming:

test_parse_config_returns_dict_when_valid()
test_parse_config_raises_error_on_missing_file()


ASSERTION RULES

Assertions must be explicit.

Avoid vague assertions like:
assert result

Prefer:
assert result == expected_value

For exceptions:
with pytest.raises(ValueError):
    function_call()


ERROR HANDLING TESTING

If a function raises exceptions:

- Test expected exception
- Test incorrect input behavior
- Test edge cases
- Test boundary conditions


FILE SYSTEM TESTING RULE

If filesystem interaction is necessary:

- Use temporary directories (tmp_path fixture)
- Do not write to project root
- Do not modify real configuration files
- Do not modify main.py


PROJECT ENTRYPOINT RULE

Tests must NOT depend on:

if __name__ == "__main__":

Tests must import functions directly and test them in isolation.


NO SIDE EFFECT RULE

Unit tests must:

- Not change global application state
- Not modify configuration files
- Not leave residual files
- Not alter environment permanently


TESTING BEFORE COMMIT

If code was modified:

The agent must ensure:

- Related unit tests still pass
- New behavior is covered
- No unrelated tests fail
- No architectural assumptions were broken


COVERAGE POLICY (OPTIONAL)

If coverage tools exist:

python3 -m pytest --cov

The agent may inspect coverage,
but must not enforce arbitrary coverage thresholds unless defined.


STRICT BOUNDARY

Unit testing is for logic verification.

Integration testing (GUI/Terminal execution) is NOT automatic
and must not be triggered by the agent.


ABSOLUTE RULE

The agent must treat testing as:

- Structured
- Isolated
- Architecture-aware
- Non-interactive
- Deterministic
- Safe for Windows PowerShell environment

Unit tests must strengthen confidence
without launching or interacting with the application runtime.
