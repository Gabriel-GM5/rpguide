---
name: python-regression-check
description: Defines mandatory regression checks that the AI agent must perform before finalizing any code change.
compatibility: opencode
---

# Regression Safety Checklist

This skill defines the **mandatory regression validation process** the AI agent must follow before finalizing any code modification.

The objective is to ensure that changes **do not introduce unintended side effects** or break existing application behavior.

All generated changes must be verified against this checklist.

---

# Core Principle

Every modification must preserve **existing application functionality, execution paths, and runtime compatibility**.

The agent must assume that **regressions are unacceptable in production-oriented repositories**.

Before completing a task, the agent must confirm that the change does not introduce instability.

---

# Mandatory Verification Checks

Before finalizing any implementation, the agent must verify the following conditions.

## Application Startup

- The application startup flow remains intact
- No changes break the main entrypoint
- Initialization logic remains consistent

---

## CLI Behavior

If the project exposes command-line interfaces:

- CLI commands must behave exactly as before
- CLI argument parsing must remain unchanged
- No new side effects should occur during CLI execution

---

## GUI Behavior

If the application includes a graphical interface:

- GUI startup must remain unchanged
- UI initialization paths must remain intact
- No UI-related imports or startup triggers should break

---

## Module Execution Compatibility

The project must remain compatible with module execution.

The agent must verify that:

- `python3 -m main` execution remains valid
- Import paths remain consistent
- Modules do not introduce unintended side effects

---

## Windows Compatibility

The project must remain fully compatible with Windows environments.

The agent must ensure:

- No OS-specific code breaks Windows execution
- File paths remain platform-safe
- No shell commands assume Unix-only behavior

---

## Encoding Stability

The agent must ensure that:

- File encoding remains unchanged
- No unintended encoding transformations occur
- Text processing logic continues to behave correctly

---

## Circular Import Prevention

The agent must verify that changes do not introduce circular imports.

New dependencies between modules must be evaluated to ensure that:

- Import chains remain valid
- Modules can still initialize without dependency loops

---

# When This Skill Applies

This skill applies whenever the agent performs:

- Code generation
- Code modification
- Refactoring
- Dependency changes
- Import restructuring

The regression checklist must be completed **before considering any task finished**.