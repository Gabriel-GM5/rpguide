# Static Validation Requirements

Before completing a task the agent must verify:

- no syntax errors
- no indentation errors
- no malformed strings
- no broken imports
- no circular imports
- no sys.path hacks
- no broad silent except clauses
- no unsafe eval or exec
- no shadowed variables
- no dead code
- no duplicated functions