Terminal & Environment Rules


ENVIRONMENT

- OS: Windows
- Default shell: PowerShell
- All commands must follow:
  - PowerShell syntax
  - Windows filesystem conventions
  - Windows command behavior


PRIMARY RULE

Always use:

- Native PowerShell
- Native Windows tools
- Git for Windows
- CMD-compatible commands (if appropriate)

Do NOT default to Linux tools.


GIT BASH / WSL (LAST RESORT)

Git Bash and WSL:

- Are emergency tools only
- Must be used ONLY if impossible in PowerShell/CMD
- Require explicit user permission before use

Before requesting permission, explain:

- Why PowerShell cannot solve the task
- Why Bash/WSL is required
- What will be executed

Without approval, NEVER use:
- bash
- wsl
- Linux commands
- Unix-only tooling


FORBIDDEN ASSUMPTIONS

Do NOT assume:

- Linux filesystem (/)
- Bash syntax
- GNU coreutils
- Unix piping semantics
- WSL is running
- Git Bash is default shell

Do NOT default to:
ls, grep, sed, awk, chmod, sudo, export, rm, mv, cp, touch

Unless explicitly inside approved Bash/WSL.


POWERSHELL EQUIVALENTS

Directory:
  Get-ChildItem

Read file:
  Get-Content

Search:
  Select-String

Temp env var:
  $env:NAME = "value"

Persistent env var:
  setx NAME "value"

Remove file:
  Remove-Item

Move file:
  Move-Item

Copy file:
  Copy-Item

Create file:
  New-Item

Remove directory:
  Remove-Item -Recurse -Force

Check command:
  Get-Command <name>

Current directory:
  Get-Location

Join path:
  Join-Path


PATH RULES

- Use Windows paths (C:\...)
- Do not assume forward-slash root
- Prefer Join-Path for dynamic paths


COMMAND CHAINING

- Use ; to separate commands
- Use proper PowerShell if syntax
- Do NOT rely on bash && or ||

Example:
if (Test-Path "file.txt") { Remove-Item "file.txt" }


SCRIPTING

- Use .ps1 format
- Use $variable syntax
- Respect execution policy
- No bash syntax


GIT CONTEXT

- Git commands must be PowerShell-compatible
- Ensure Windows-safe paths
- Do not assume Unix quoting behavior


TOOL VERIFICATION

Before using non-native tools:

  Get-Command <tool>

If unavailable:
STOP and inform user.


ABSOLUTE RULE

PowerShell is mandatory.
Windows-native solutions first.

Git Bash and WSL are emergency-only and require explicit approval.
