---
name: python-security-policy
description: Defines mandatory security practices the AI agent must enforce when generating or modifying Python code.
compatibility: opencode
---

# Python Security Policy

This skill defines the **security rules** that the AI agent must enforce when generating, modifying, or reviewing Python code.

The objective is to ensure that the codebase follows **secure coding practices** and prevents the introduction of vulnerabilities, credential leaks, or unsafe execution patterns.

Security must always take priority over convenience or speed of implementation.

---

# Secret Management

The agent must ensure that **sensitive information is never hardcoded** into the codebase.

Sensitive values must always be obtained from environment variables.

Acceptable pattern:

```python
import os

API_KEY = os.environ.get("API_KEY")
```

The agent must **never embed secrets directly in source code**.

---

# Forbidden Secret Exposure

The agent must never expose or include the following in generated code:

* API keys
* Credentials
* Access tokens
* Private keys
* Environment variable values
* Authentication secrets

If the agent encounters such values in prompts, logs, or examples, they must **not be reproduced or propagated into the codebase**.

---

# Input Validation

All external inputs must be treated as **untrusted data**.

The agent must ensure that:

* Inputs are validated before use
* Data types are verified
* Unexpected values are handled safely
* Parsing logic does not assume well-formed input

This applies to inputs from:

* User interfaces
* CLI arguments
* Configuration files
* Network requests
* File I/O

---

# Unsafe Execution Prevention

The agent must avoid Python features that allow unsafe runtime execution.

The following constructs must **not be introduced into the codebase**:

* `eval()`
* `exec()`
* Dynamic code execution from untrusted sources

These patterns create significant security risks and must be avoided.

---

# Unsafe Deserialization

The agent must avoid insecure deserialization mechanisms.

The agent must not introduce code that deserializes untrusted data using unsafe libraries or patterns that could allow code execution.

Safe serialization formats (such as JSON) should be preferred when exchanging structured data.

---

# When This Skill Applies

This skill applies whenever the agent performs:

* Code generation
* Code modification
* Security reviews
* Integration with external systems
* Handling of configuration or credentials

All generated code must comply with **secure coding standards and secret management best practices**.