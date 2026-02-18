Strict Pre-Commit Review and Risk Assessment Policy


PURPOSE

Before creating any commit, the agent must perform a structured internal production-grade review.

No commit is allowed without passing this review.


MANDATORY APPLICATION EXECUTION AWARENESS

The application must remain runnable in both modes:

GUI mode:
python3 .\main.py gui

Terminal mode:
python3 .\main.py terminal

If the change impacts:

- Startup logic
- Imports
- Argument parsing
- Mode selection
- Configuration loading
- File IO
- Initialization flow
- Global state
- Dependency loading

The agent must assume startup could break and review accordingly.

If runtime integrity cannot be reasonably guaranteed:
STOP.
Do not commit.
Inform the user.


MANDATORY RISK ASSESSMENT (INTERNAL CHECK)

Before committing, the agent must internally evaluate:

CHANGE SCOPE

- What files were modified?
- Why were they modified?
- Is every modification directly related to the task?

STRUCTURAL RISK

- Could this introduce circular imports?
- Could this break module resolution?
- Could this break python3 -m main execution?
- Could indentation be broken?
- Could multiline blocks be malformed?

ESCAPING AND STRING SAFETY

- Are Windows paths correctly escaped?
- Are raw strings used when appropriate?
- Are f-strings properly formatted?
- Are backslashes valid?
- Are quotes balanced?
- Are triple-quoted strings intact?
- Are there stray markdown artifacts?
- Are there partial or duplicated paste fragments?

LOGICAL CONSISTENCY

- Was existing behavior unintentionally changed?
- Was any unrelated logic modified?
- Were conditionals altered safely?
- Were default values changed?
- Was state mutation introduced?

REGRESSION RISK

- Could GUI mode fail to initialize?
- Could terminal mode fail to initialize?
- Could argument parsing break?
- Could missing imports occur?
- Could dependency loading fail?
- Could Windows-specific behavior break?


MANDATORY DIFF AUDIT

Before commit, the agent must:

- Review staged files.
- Review full staged diff.
- Confirm only intended changes exist.
- Confirm no debug prints remain.
- Confirm no commented legacy code remains.
- Confirm no temporary experimentation code remains.
- Confirm no sensitive data appears.


SECURITY REVIEW

The agent must verify:

- No hardcoded credentials.
- No embedded secrets.
- No unsafe eval or exec.
- No unsafe deserialization.
- No logging of sensitive data.
- No accidental exposure of environment variables.


CODE QUALITY REVIEW

The agent must verify:

- PEP 8 alignment.
- Reasonable function size.
- Clear naming.
- No duplicated logic.
- No dead code.
- No unreachable blocks.
- No global mutable state added unnecessarily.
- No overly complex nesting introduced.


STARTUP INTEGRITY ASSERTION

The agent must confirm internally that:

The project still supports:

python3 .\main.py gui
python3 .\main.py terminal

The entrypoint main.py remains valid.

Argument handling still functions.

Imports resolve correctly.

Module structure remains coherent.


COMMIT JUSTIFICATION GATE

Before committing, the agent must internally answer:

- Why is this change safe?
- What risk does this change introduce?
- Why is that risk acceptable?
- Is the commit message accurate and precise?
- Does the commit message reflect actual diff content?

If any answer is uncertain:
STOP.
Ask the user.


ABSOLUTE BLOCK CONDITIONS

The agent must refuse to commit if:

- Startup integrity is uncertain.
- Escaping correctness is uncertain.
- Diff contains unrelated changes.
- Protected branches are targeted.
- Commit message is vague.
- The change introduces architectural instability.
- The change cannot be clearly justified.


FINAL AUTHORIZATION RULE

A commit may only be created if:

- The application is structurally intact.
- Both execution modes remain callable.
- Escaping and formatting are correct.
- The change is minimal and intentional.
- The commit message is precise.
- Risk has been consciously evaluated and accepted.

If not fully confident:
Do not commit.
Request clarification.
