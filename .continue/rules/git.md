Git Usage Rules for AI Agent


PROTECTED BRANCHES (ABSOLUTE)

Protected:
- main
- master
- production

The agent MUST NEVER:
- Commit to them
- Modify files while on them
- Delete them
- Force push
- Reset / rebase / rewrite history
- Merge into them

Only a human may modify protected branches.

Direct commit to main is allowed ONLY if user explicitly says:
"Commit directly to main"


WORKING BRANCH RULE (MANDATORY)

On any requested change:

1. Run:
   git branch --show-current

2. If on a protected branch:
   - Create new branch
   - Switch to it
   - Work only there

Refuse if user does not allow branch creation.


BRANCH NAMING

Use:
- feature/<name>
- fix/<name>
- refactor/<name>
- chore/<name>

Rules:
- lowercase
- hyphen-separated
- concise


COMMIT MESSAGE (MANDATORY)

Every commit must:

- Be written by the agent
- Start with: [AI Generated]

Format:
[AI Generated] <type>: <clear description>

Message must reflect actual staged diff.
Never reuse raw user text blindly.


PRE-STAGING CHECK (STRICT)

Before staging:

Run:
  git status --porcelain

Review ALL:
- Modified
- Deleted
- Renamed
- Staged
- Untracked (??)

Evaluate each file individually.


UNTRACKED FILES

- Review all untracked files.
- Stage only if directly related to task.
- If unsure: STOP and ask.


STAGING STRATEGY (INTELLIGENT)

Prefer:
  git add <file>

Use:
  git add .

ONLY IF ALL are true:
- All changes relate to task
- No unrelated files
- No secrets / env / logs
- Working directory is clean
- Bulk staging is safer

Blind bulk staging is forbidden.


POST-STAGING CHECK (MANDATORY)

Run:
  git diff --staged

Confirm:
- Only intended files staged
- Diff matches task
- No unrelated changes
- Commit message matches diff

If anything unexpected:
STOP.
Do not commit.


FORBIDDEN ACTIONS

- Modify protected branches
- Skip branch creation
- Force push
- Rebase without explicit instruction
- Auto-merge
- Push without explicit instruction
- Use vague commit messages
