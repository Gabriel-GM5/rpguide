Pre-Commit Code Review Rules


PURPOSE

Before any commit, perform structured internal review.

Goals:

- Application integrity preserved
- No syntax or escaping errors
- No copy-paste corruption
- Change matches task
- Startup remains structurally valid


EXECUTION AWARENESS

Application supports:

- python3 .\main.py gui
- python3 .\main.py terminal

If change affects:

- Argument parsing
- Mode selection
- Startup logic
- Imports
- UI/CLI flow
- Initialization
- Core logic
- File IO
- Config handling

Ensure startup paths remain structurally valid.

If execution integrity is uncertain:
STOP and inform user.


SYNTAX & ESCAPING CHECK (CRITICAL)

Verify:

- Quotes balanced
- Backslashes valid (Windows paths)
- Raw strings used when appropriate
- f-strings correct
- No broken multiline strings
- Indentation correct (no tab/space mix)
- No truncated copy-paste
- No duplicate blocks
- No partial fragments
- No malformed docstrings
- No markdown artifacts
- No stray backticks
- No invisible characters

Prefer pathlib over manual Windows paths.


LOGIC CONSISTENCY

Confirm:

- Change matches request
- No unrelated logic modified
- No behavior unintentionally removed
- No circular imports
- No dead or unreachable code
- No duplicate functions
- No variable shadowing
- No name collisions


IMPORT & STRUCTURE

Ensure:

- Imports resolve logically
- No unused or duplicate imports
- No incorrect relative imports
- No sys.path hacks (unless justified)
- python3 -m main compatibility preserved


ERROR HANDLING

- No broad except:
- Exceptions are specific
- No silent suppression
- Logging meaningful
- Stack traces not suppressed without reason


SECURITY

- No hardcoded secrets
- No embedded API keys
- No sensitive logs
- No unsafe eval/exec
- No insecure deserialization


CODE QUALITY

Confirm:

- PEP 8 alignment
- Clear naming
- Reasonable function size
- No excessive nesting
- No unnecessary complexity
- No new global mutable state
- No debug prints
- No commented legacy blocks


REGRESSION RISK CHECK

Internally ask:

- Could this break startup?
- Break imports?
- Break CLI arguments?
- Break Windows execution?
- Break module execution?
- Introduce encoding issues?

If risk cannot be reasoned as safe:
STOP and ask.


FINAL PRE-COMMIT CHECK

Before committing:

- Review changed files
- Review staged diff
- Validate logic
- Validate escaping
- Validate structure
- Confirm entrypoint intact
- Confirm gui/terminal paths preserved
- Confirm commit message matches diff
- Confirm no unintended files staged


ABSOLUTE RULE

Do NOT commit unless confident that:

- Startup paths remain structurally valid
- Logic is correct
- No escaping corruption exists
- Architecture remains clean
- Codebase remains maintainable
