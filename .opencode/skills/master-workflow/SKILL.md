---
name: master-workflow
description: Unified workflow policy that combines all individual skill requirements for Python development in a production-safe environment.
compatibility: opencode
---

# Master Workflow Policy

This skill defines the comprehensive **development workflow and safety rules** that the AI agent must follow when performing any code-related task in the Python project.

The master workflow integrates all individual skill requirements to ensure **safe, deterministic, and production-ready code generation and modification**.

---
## Core Principles

The agent must operate with the following characteristics:
- Deterministic
- Architecture-aware
- Non-destructive
- Branch-safe
- Startup-safe
- Windows-compatible
- Module-execution compatible
- Security-conscious
- Test-aware

All operations must prioritize **production stability and code quality**.

---
## Workflow Structure

### Step 1 — Understand the Task
Before performing any analysis or code generation, the agent must clearly identify:
- The goal of the task
- All explicit constraints
- The potential impact areas within the project

Impact areas include:
- GUI components
- Terminal or CLI interfaces
- Shared application logic
- Application startup and entrypoints
- Configuration systems
- File or network I/O
- Project dependencies

If any ambiguity or missing information exists, **stop execution and request clarification from the user.**

### Step 2 — Impact Analysis
Before writing any code, the agent must perform a structured impact analysis:
- Inspect the project structure
- Identify integration boundaries
- Identify dependent modules and services
- Evaluate potential regression risks
- Verify that application startup will remain intact
- Confirm that module execution compatibility will not be broken

Code generation must not begin until the impact of the change is clear.

### Step 3 — Implementation
Once the task and its impact are fully understood, the agent may proceed with implementation:
- Changes must be minimal and targeted
- No unrelated refactors may be introduced
- Existing architecture must be preserved
- Application startup behavior must remain unchanged
- Windows compatibility must be preserved
- Module execution compatibility must be preserved

Implementation constraints:
- Avoid code duplication
- Avoid unnecessary abstractions
- Avoid overly complex logic
- Avoid temporary debug artifacts
- Avoid experimental or speculative changes

---
## Safety Requirements

### Security Policy
The agent must enforce mandatory security practices:
- Never embed secrets directly in source code
- All sensitive information must be obtained from environment variables
- Inputs must be treated as untrusted data and validated before use
- Avoid Python features that allow unsafe runtime execution (`eval()`, `exec()`)
- Avoid insecure deserialization mechanisms

### Validation Requirements
The agent must apply mandatory static validation checks:
- Verify no syntax errors, indentation errors, or malformed string literals
- Ensure no broken imports or circular imports
- Prevent overly broad or silent exception handlers
- Avoid unsafe runtime execution patterns (`eval()`, `exec()`)
- Check for shadowed variables, unreachable code, and duplicated functions

### Execution Model Compliance
The agent must respect the project's execution model:
- The application must remain compatible with `python3 -m main` execution
- Imports must not trigger application startup (no implicit execution on import)
- If a main() function exists, use proper `if __name__ == "__main__"` guard

### Windows Compatibility
The agent must ensure all code remains fully compatible with Windows environments:
- All filesystem paths must be handled using `pathlib` or other platform-aware utilities
- Avoid hardcoded path separators (forward slashes, backslashes)
- Ensure correct escaping of path strings and system-related strings
- Avoid Unix-only shell commands (`ls`, `grep`, `chmod`, `bash` scripts)

---
## Git Discipline

The agent must enforce safe Git workflow rules:
- Protected branches (`main`, `master`, `production`) must not be modified directly
- Forbidden actions on protected branches: direct commits, file modifications, force pushes, resets, rebases, deletions
- Explicit user override required for commits to protected branches (only with "Commit directly to main" instruction)
- Allowed branch naming prefixes: `feature/<name>`, `fix/<name>`, `refactor/<name>`, `chore/<name>`
- Commit messages must follow format: `[AI Generated] <type>: <clear description>`

---
## Regression Safety

Before finalizing any implementation, the agent must verify:
- Application startup flow remains intact
- CLI commands behave exactly as before (if applicable)
- GUI startup and initialization paths remain unchanged (if applicable)
- Module execution compatibility is preserved
- Windows compatibility is maintained
- File encoding remains unchanged
- No circular imports are introduced

---
## Testing Policy

The agent must follow testing standards:
- All tests must be deterministic, non-interactive, isolated, and side-effect safe
- Tests must not launch main application entrypoint, GUI, or terminal interfaces
- Tests must use module-based execution (`python3 -m pytest`)
- Tests must use temporary directories and mock external dependencies for isolation

---
## Fail-Safe Behavior

When requirements, system state, or architecture details are unclear:
- Stop the current execution path
- Avoid making assumptions
- Avoid generating partial implementations
- Request clarification from the user

Production safety always takes priority over speed or task completion.

---
## When This Skill Applies

This master workflow applies to all development tasks including:
- Code generation
- Code modification
- Bug fixes
- Refactoring
- Integration changes
- Test creation and modification
- Security reviews
- System integration tasks

The unified workflow ensures that all changes are performed in a **safe, structured, and architecture-aware manner** while maintaining production stability.