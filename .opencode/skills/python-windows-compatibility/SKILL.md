# Windows Compatibility Policy

The codebase must remain Windows compatible.

Rules:

- use pathlib for filesystem paths
- avoid hardcoded forward/back slashes
- ensure correct escaping
- avoid Unix-only shell commands