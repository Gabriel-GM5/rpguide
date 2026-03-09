---
name: python-safe-development
description: Defines the mandatory step-by-step workflow the AI agent must follow when analyzing, implementing, and validating code changes.
compatibility: opencode
---

# Safe Development Workflow

This skill defines the **mandatory development workflow** that the AI agent must follow when performing any code-related task.

The goal is to ensure that every change is **fully understood, carefully analyzed, and safely implemented** within the constraints of the existing architecture.

The workflow must be followed **exactly in the order defined below**.

---

# Step 1 — Understand the Task

Before performing any analysis or code generation, the agent must clearly identify:

- The **goal** of the task
- All **explicit constraints**
- The potential **impact areas** within the project

Possible impact areas include:

- GUI components
- Terminal or CLI interfaces
- Shared application logic
- Application startup and entrypoints
- Configuration systems
- File or network I/O
- Project dependencies

The agent must ensure that the task requirements are **fully understood**.

If any ambiguity or missing information exists:

**Stop execution and request clarification from the user.**

No further steps may be taken until the task is clear.

---

# Step 2 — Impact Analysis

Before writing any code, the agent must perform a structured impact analysis.

The agent must:

- Inspect the project structure
- Identify integration boundaries
- Identify dependent modules and services
- Evaluate potential regression risks
- Verify that application startup will remain intact
- Confirm that module execution compatibility will not be broken

The agent must ensure that the **full scope of the change is understood**.

Code generation must **not begin** until the impact of the change is clear.

---

# Step 3 — Implementation

Once the task and its impact are fully understood, the agent may proceed with implementation.

All code changes must follow these principles:

- Changes must be **minimal and targeted**
- No unrelated refactors may be introduced
- Existing architecture must be preserved
- Application startup behavior must remain unchanged
- Windows compatibility must be preserved
- Module execution compatibility must be preserved

---

# Implementation Constraints

During implementation, the agent must avoid introducing unnecessary complexity.

The agent must avoid:

- Code duplication
- Unnecessary abstractions
- Overly complex logic
- Temporary debug artifacts
- Experimental or speculative changes

All generated code must be **clean, maintainable, and production-safe**.

---

# When This Skill Applies

This workflow applies to **all development tasks**, including:

- Code generation
- Code modification
- Bug fixes
- Refactoring
- Integration changes

The workflow ensures that all changes are performed in a **safe, structured, and architecture-aware manner**.