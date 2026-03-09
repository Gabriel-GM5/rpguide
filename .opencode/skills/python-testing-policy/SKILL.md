# Python Testing Policy

Tests must be:

- deterministic
- non-interactive
- isolated
- side-effect safe

Tests must NOT:

- launch main
- launch GUI
- launch terminal interfaces
- require user input
- make real network calls
- perform destructive filesystem operations

Allowed tools:

- pytest
- tmp_path
- monkeypatch
- unittest.mock

Tests must be executed using:

python3 -m pytest

Never use:

pytest