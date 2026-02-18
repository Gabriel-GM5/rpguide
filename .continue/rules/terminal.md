Terminal and Environment Rules for AI Agent


ENVIRONMENT DECLARATION (MANDATORY)

The agent is operating in a Windows environment.

The default and required shell is:
PowerShell

All commands must follow:

- PowerShell syntax
- PowerShell semantics
- Windows command behavior
- Windows filesystem conventions


PRIMARY EXECUTION RULE

PowerShell is the first and mandatory choice.

The agent must always attempt to solve the problem using:

- Native PowerShell
- Native Windows tools
- Native Git for Windows
- CMD-compatible commands when appropriate

Linux-based environments must NOT be used by default.


LIMITED USE OF GIT BASH AND WSL

Git Bash and WSL are available, but:

- They are LAST RESORT tools.
- They must ONLY be used when the task is impossible or unsafe in PowerShell or CMD.
- The agent MUST ask for explicit user permission before using them.

The agent must clearly explain:

- Why PowerShell cannot accomplish the task.
- Why Git Bash or WSL is required.
- What will be executed inside that environment.

Without explicit approval, the agent must NOT use:

- bash
- wsl
- Linux shell commands
- Unix-only tooling


FORBIDDEN ASSUMPTIONS

The agent must NOT assume:

- Linux filesystem structure
- Root path "/"
- Bash syntax
- GNU coreutils availability
- Unix-style piping behavior
- That WSL is running or configured
- That Git Bash is the default shell

Do NOT default to:

- ls
- grep
- sed
- awk
- chmod
- sudo
- export
- rm
- mv
- cp
- touch

Unless explicitly running inside approved Git Bash or WSL.


POWERSHELL COMMAND REQUIREMENT

Use PowerShell equivalents:

Directory listing:
Get-ChildItem

File content:
Get-Content

Search in files:
Select-String

Temporary environment variable:
$env:VARIABLE_NAME = "value"

Persistent environment variable:
setx VARIABLE_NAME "value"

Remove file:
Remove-Item

Move file:
Move-Item

Copy file:
Copy-Item

Create file:
New-Item

Delete directory:
Remove-Item -Recurse -Force

Check command existence:
Get-Command <name>

Current directory:
Get-Location

Path join:
Join-Path


PATH RULES

- Use Windows path format.
- Example: C:\Users\gabri\Project
- Do NOT assume forward-slash root paths.
- Prefer Join-Path for dynamic paths.


COMMAND CHAINING RULES

In PowerShell:

- Use semicolon ; to separate commands.
- Use proper if statements for conditional logic.
- Do NOT rely on bash-style && or || semantics.

Example:

if (Test-Path "file.txt") { Remove-Item "file.txt" }


SCRIPTING RULES

When writing scripts:

- Use .ps1 format.
- Use PowerShell variable syntax with $.
- Respect execution policies.
- Avoid bash syntax.


GIT EXECUTION CONTEXT

Git commands must be written in PowerShell-compatible syntax.

Do not assume Unix quoting behavior.
Ensure paths are Windows-compatible.


TOOL VERIFICATION RULE

Before using any non-native tool, the agent must verify its existence:

Get-Command <tool-name>

If unavailable:
STOP.
Inform the user.


ABSOLUTE RULE

The agent must prioritize native Windows and PowerShell solutions.

Git Bash and WSL are emergency tools only.

Explicit permission is required before using them.
