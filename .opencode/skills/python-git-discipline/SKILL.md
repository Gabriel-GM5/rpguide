# Git Discipline Policy

## Protected Branches

The following branches are protected:

- main
- master
- production

The agent MUST NEVER:

- commit directly to them
- modify files while checked out on them
- force push
- reset
- rebase
- delete them

Exception:

Only if the user explicitly writes:

"Commit directly to main"

## Allowed Branch Naming

feature/<name>
fix/<name>
refactor/<name>
chore/<name>

Rules:

- lowercase
- hyphen-separated
- concise

## Commit Format

[AI Generated] <type>: <clear description>