Git Usage Rules for AI Agent

BRANCH PROTECTION (MANDATORY)

The agent must NEVER commit directly to:
main
master
production

When the user requests any change:

- Check the current branch.
- If on main, master, or production:
  - Create a new branch.
  - Switch to that branch.
- Perform all work on that branch.

Only commit directly to main if the user explicitly says:
Commit directly to main


BRANCH NAMING

Use one of the following formats:

feature/<short-description>
fix/<short-description>
refactor/<short-description>
chore/<short-description>

Branch names must be lowercase and use hyphens.


COMMIT MESSAGE POLICY (MANDATORY)

Every commit MUST:

- Be written by the agent.
- Start with: [AI Generated]

Format:

[AI Generated] <type>: <clear description>

The agent must NEVER reuse user text as the commit message.


PRE-COMMIT VERIFICATION (STRICT)

Before staging or committing, the agent MUST:

1. Run:
   git status --porcelain

2. Identify:
   - Modified files
   - Deleted files
   - Renamed files
   - Staged files
   - Untracked files (lines starting with ??)

3. Evaluate every file individually.

UNTRACKED FILE POLICY

- The agent must inspect all untracked files.
- The agent must determine whether each untracked file is required for the task.
- If an untracked file is unrelated, it must NOT be staged.
- If unsure about any untracked file:
  STOP and ask the user.

STAGING RULES

Default behavior:
- Stage files individually:
  git add <specific-file>

If important untracked files are required for the task AND all files in the working directory are verified as intentional:

- The agent MAY use:
  git add .

Conditions for using git add .:
- All untracked files have been reviewed.
- No unrelated files exist.
- No secrets, logs, environment files, or temporary files are present.
- The agent explicitly confirms internally that all changes are task-related.

After staging, the agent MUST run:

git diff --staged

The agent must confirm:

- Only intended files are staged.
- The changes match the requested task.
- The commit message accurately reflects the staged changes.

If anything is unexpected:
STOP.
Do NOT commit.
Inform the user.


FORBIDDEN ACTIONS

The agent must NOT:

- Commit directly to main unless explicitly authorized.
- Use git add . without verifying all files first.
- Stage unreviewed untracked files.
- Create vague commit messages.
- Force push.
- Rebase without instruction.
- Auto-merge branches.
- Push without explicit instruction.
