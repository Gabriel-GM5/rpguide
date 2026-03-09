---
name: python-validation
description: Defines mandatory static validation checks that must be satisfied before the AI agent completes a task.
compatibility: opencode
---

# Python Static Validation Requirements

This skill defines the **static validation rules** the AI agent must apply before considering any task complete.

Static validation ensures that generated or modified code is **structurally correct, safe, and free of obvious defects** before runtime execution.

All code must pass these checks **prior to finalization**.

---

# Core Principle

The agent must verify that the codebase remains **syntactically valid, structurally consistent, and free of common programming errors**.

Static validation must occur **before delivering or committing any implementation**.

---

# Mandatory Validation Checks

The agent must verify the following conditions.

## Syntax Integrity

The code must contain:

- No syntax errors
- No indentation errors
- No malformed string literals

All Python files must remain **valid Python source code**.

---

## Import Safety

The agent must verify that imports remain correct and stable.

The codebase must contain:

- No broken imports
- No circular imports
- No runtime path manipulation such as `sys.path` modifications

Imports must remain **module-safe and architecture-consistent**.

---

## Exception Safety

Exception handling must be explicit and controlled.

The agent must ensure that the code does **not introduce overly broad or silent exception handlers**, such as:
```
  except:
    pass

```

Exception blocks must not hide errors silently.

---

## Unsafe Execution Prevention

The agent must verify that the code does **not introduce unsafe runtime execution patterns**.

The following constructs must not appear in the codebase:

- `eval()`
- `exec()`

These functions allow dynamic code execution and introduce security risks.

---

## Code Quality Checks

The agent must verify that the implementation does not introduce structural code issues.

The code must contain:

- No shadowed variables
- No unreachable or dead code
- No duplicated functions or redundant implementations

The agent must ensure that code remains **clean, readable, and maintainable**.

---

# When This Skill Applies

This skill applies whenever the agent performs:

- Code generation
- Code modification
- Refactoring
- Integration changes

Static validation must be performed **before the agent considers the task complete**.

The objective is to ensure that all generated code is **structurally correct and production-safe** before further validation or runtime testing occurs.