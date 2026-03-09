---
name: python-windows-compatibility
description: Ensures that all generated or modified code remains fully compatible with Windows environments.
compatibility: opencode
---

# Windows Compatibility Policy

This skill defines the **platform compatibility requirements** the AI agent must follow to ensure that the project remains fully functional on Windows systems.

All code generated or modified by the agent must preserve **cross-platform behavior with guaranteed Windows compatibility**.

---

# Core Principle

The codebase must remain **fully operational on Windows environments**.

The agent must avoid introducing patterns, dependencies, or commands that assume a Unix-like operating system.

All filesystem interactions and system behaviors must remain **platform-safe**.

---

# Filesystem Path Handling

All filesystem paths must be handled using **`pathlib`** or other platform-aware utilities.

Preferred pattern:

```
from pathlib import Path

data_path = Path("data") / "file.txt"
```

The agent must avoid manual string concatenation when building filesystem paths.

---

# Path Separator Safety

The agent must avoid **hardcoded path separators**, including:

* Forward slashes (`/`)
* Backslashes (`\`)

Filesystem paths must always be constructed using platform-aware tools such as:

* `pathlib.Path`
* `os.path`

This ensures paths resolve correctly across operating systems.

---

# String Escaping

The agent must ensure that all path strings and system-related strings use **correct escaping**.

Improper escaping can break execution on Windows systems, especially when backslashes appear in file paths.

Where possible, **raw strings or pathlib paths should be preferred**.

---

# Shell Command Restrictions

The agent must avoid introducing **Unix-only shell commands**.

Examples of commands that must not be assumed to exist:

* `ls`
* `grep`
* `chmod`
* `bash` scripts

If system commands are required, they must be implemented using **cross-platform Python libraries** instead of shell-specific tools.

---

# When This Skill Applies

This skill applies whenever the agent performs:

* File system operations
* Path construction
* Script generation
* Automation tasks
* Integration with system commands

All modifications must preserve **Windows compatibility and cross-platform stability**.
