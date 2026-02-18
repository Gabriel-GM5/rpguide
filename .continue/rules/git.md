Git Usage Rules for AI Agent


PROTECTED BRANCH POLICY (ABSOLUTE RULE)

The following branches are PROTECTED:

main
master
production

The agent must NEVER:

- Commit directly to a protected branch.
- Modify files while currently on a protected branch.
- Delete a protected branch.
- Force push to a protected branch.
- Reset, rebase, or rewrite history of a protected branch.
- Merge into a protected branch.

Protected branches must only be modified by explicit human action.


WORKING BRANCH REQUIREMENT (MANDATORY)

When the user requests any change:

- Run:
  git branch --show-current

- If currently on main, master, or production:
  - Create a new branch.
  - Switch to that branch.
  - Perform all work there.

The agent may only commit directly to main if the user explicitly says:
Commit directly to main

Without explicit authorization, the agent must refuse.


BRANCH NAMING

Use one of the following formats:

feature/<short-description>
fix/<short-description>
refactor/<short-description>
chore/<short-description>

Branch names must:
- Be lowercase
- Use hyphens
- Be concise and descriptive


COMMIT MESSAGE POLICY (MANDATORY)

Every commit MUST:

- Be written by the agent.
- Start with: [AI Generated]

Format:

[AI Generated] <type>: <clear description>

The commit message must accurately describe the staged changes.
The agent must NEVER blindly reuse user text as the commit message.


PRE-COMMIT VERIFICATION (STRICT)

Before staging any files, the agent MUST:

1. Run:
   git status --porcelain

2. Identify:
   - Modified files
   - Deleted files
   - Renamed files
   - Staged files
   - Untracked files (lines starting with ??)

3. Evaluate every file individually.

4. Determine which files are directly related to the task.


UNTRACKED FILE POLICY

- All untracked files must be reviewed.
- The agent must determine whether each untracked file is required for the task.
- If an untracked file is unrelated, it must NOT be staged.
- If unsure about any file:
  STOP and ask the user.


STAGING DECISION RULE (INTELLIGENT STAGING)

After analysis, the agent must choose the safest and most appropriate staging strategy.

Use:
  git add <specific-file>

WHEN:
- Only a subset of files are related to the task.
- Some files in the working directory are unrelated.
- There are temporary, log, or unrelated files present.
- Selective staging reduces risk.

Use:
  git add .

ONLY WHEN ALL of the following are true:

- All modified and untracked files are directly related to the task.
- No unrelated files exist.
- No secrets, environment files, logs, or temporary files are present.
- The working directory is fully intentional and clean.
- Using git add . is logically safer and simpler than staging individually.

Blind bulk staging is forbidden.


POST-STAGING VERIFICATION

After staging, the agent MUST run:

git diff --staged

The agent must confirm:

- Only intended files are staged.
- Changes match the requested task.
- No unrelated content is included.
- The commit message accurately reflects the staged changes.

If anything unexpected appears:
STOP.
Do NOT commit.
Inform the user.


FORBIDDEN ACTIONS

The agent must NOT:

- Delete protected branches.
- Modify protected branches directly.
- Bypass branch creation.
- Use vague commit messages.
- Force push.
- Rebase without explicit instruction.
- Auto-merge branches.
- Push without explicit instruction.
