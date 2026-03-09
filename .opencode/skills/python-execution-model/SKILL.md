---
name: python-execution-model
description: Defines the execution model and entrypoint constraints for the Python project, ensuring module-safe startup and preventing unintended runtime execution.
compatibility: opencode
---

# Python Execution Model Policy

This skill defines the **runtime execution model** for the Python project and ensures that the AI agent preserves a **safe, predictable startup structure**.

The agent must respect the defined project entrypoint and avoid introducing code that alters or bypasses the expected execution flow.

---

# Project Entrypoint

The project entrypoint is:

`main.py` (repository root)

The execution model must support module execution using:

```python3 -m main
```


The agent must ensure that all modifications remain compatible with this execution pattern.

---

# Execution Requirements

All generated or modified code must comply with the following rules.

## Module Execution Compatibility

The codebase must remain compatible with Python module execution.

The agent must ensure:

- The application can run with `python3 -m main`
- Imports remain module-safe
- The project structure does not rely on direct script execution

---

## Import Safety

The agent must ensure that imports do not trigger application startup.

The codebase must follow this rule:

- **No implicit execution on import**

Application startup logic must only occur inside a controlled entrypoint.

---

## Entrypoint Guard

If a `main()` function exists in `main.py`, the following pattern must be used:

```python
if __name__ == "__main__":
    main()
```

The agent must not introduce this guard unless a main() function already exists.