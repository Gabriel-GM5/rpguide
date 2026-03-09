# Safe Development Workflow

The agent must follow this exact workflow.

## Step 1 — Understand Task

Identify:

- goal
- constraints
- impact areas

Impact areas may include:

- GUI
- terminal
- shared logic
- startup
- configuration
- IO
- dependencies

If ambiguity exists: STOP.

---

## Step 2 — Impact Analysis

Before coding:

- inspect project structure
- identify integration boundaries
- identify dependencies
- evaluate regression risk
- verify startup integrity
- confirm module execution compatibility

No code may be written before impact clarity.

---

## Step 3 — Implementation

Requirements:

- minimal change
- no unrelated refactors
- preserve architecture
- preserve startup behavior
- preserve Windows compatibility
- preserve module execution

Avoid:

- duplication
- unnecessary complexity
- debug artifacts