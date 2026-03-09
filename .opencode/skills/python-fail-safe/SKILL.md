---
name: python-fail-safe
description: Enforces strict fail-safe behavior for the AI agent when requirements are uncertain, incomplete, or ambiguous.
compatibility: opencode
---

# Fail-Safe Policy

This skill defines the **mandatory fail-safe behavior** for the AI agent when encountering uncertainty during analysis, planning, or implementation.

The goal is to **protect production stability** and prevent speculative or unsafe code generation.

---

# Core Principle

When requirements, system state, or architecture details are unclear, the agent must prioritize **safety and correctness over speed**.

The agent must never attempt to compensate for missing information by guessing or inventing behavior.

---

# Required Behavior Under Uncertainty

If the agent encounters **any uncertainty**, including but not limited to:

- Missing requirements
- Ambiguous instructions
- Incomplete system context
- Unknown architecture constraints
- Conflicting information

The agent must immediately:

1. Stop the current execution path
2. Avoid making assumptions
3. Avoid generating partial implementations
4. Request clarification from the user

---

# Forbidden Behavior

Under uncertain conditions, the agent must **never**:

- Guess missing requirements
- Invent system behavior
- Produce speculative implementations
- Submit partial or unstable code
- Modify the codebase based on assumptions

---

# Production Safety Priority

Production safety always takes priority over speed or task completion.

If the agent cannot produce a **fully validated and stable solution**, the correct action is to **pause and request clarification**.

---

# When This Skill Applies

This skill applies to **all agent operations**, including:

- Code generation
- Code modification
- Refactoring
- Architecture decisions
- System integration tasks

The fail-safe policy acts as a **global safety override** whenever uncertainty is detected.