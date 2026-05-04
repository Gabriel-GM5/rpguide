# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

> **Requires [uv](https://docs.astral.sh/uv/getting-started/installation/).**
> Install it once with `pip install uv` (or via the standalone installer), then use the
> commands below. `uv` manages the virtual environment and lockfile automatically.

```bash
# Install / sync dependencies (creates .venv on first run)
uv sync --dev                    # install all deps including dev group
uv sync                          # install only production deps

# Run (GUI mode default)
uv run python main.py
uv run python main.py terminal

# Tests
uv run pytest tests/ -v                                          # all tests
uv run pytest tests/test_filename.py -v                         # single file
uv run pytest tests/test_filename.py::test_function_name -v     # single test
uv run pytest tests/ --cov=modules/ --cov-report=html           # with coverage

# Lint / format
uv run pylint modules/
uv run black modules/
uv run flake8 modules/

# Dependency management
uv add <package>                 # add a production dependency
uv add --dev <package>           # add a dev dependency
uv lock                          # regenerate uv.lock after manual edits to pyproject.toml
```

> **Note:** `uv` is invocable as `python3 -m uv` if the `uv` binary is not on PATH.

## Architecture

This is a RAG-based AI assistant with multi-agent routing. Entry point is `main.py`, which dispatches to `gui_app.py` (ttkbootstrap) or `terminal_app.py` based on the `MODE` env var or CLI arg.

### Agent routing (modules/connectors_manager.py)

`ConnectorManager` orchestrates three agents:

1. **`PromptAnalyzerAgent`** — classifies the user prompt via LLM call; falls back to heuristics (keyword list, message length >200 chars) to decide between RAG and direct LLM.
2. **`RAGAgent`** — retrieves docs from FAISS vector store (similarity_score_threshold=0.3, top-4) and answers using a document chain.
3. **`SimpleLLMAgent`** — direct LLM call, no retrieval context.

### Document pipeline (modules/docs_manager.py)

Loads from `LOCAL_KNOWLEDGE_PATH` (env) and `uploads/` directory. Specialized loaders per format (PDF via PyMuPDF, docx, csv, html, rtf, pptx), with `UnstructuredLoader` as fallback. Chunks via `RecursiveCharacterTextSplitter` (chunk_size=300, overlap=30), then indexes into FAISS.

### LLM connectors (modules/connectors/)

Swap LLM provider via `LLM_TYPE` env var:
- `gemini` → `gemini_connector.py` (Google Generative AI)
- `openai` → `openai_connector.py` (OpenAI; optional `LLM_AI_BASE_URL` for custom endpoints)
- `lmstudio` → `lmstudio_connector.py` (LM Studio via OpenAI-compatible API; defaults to `http://localhost:1234/v1`)
- `ollama` → `ollama_connector.py` (Ollama; defaults to `http://localhost:11434`)
- `anthropic` → `anthropic_connector.py` (Anthropic/Claude; RAG disabled — no embeddings API)

Each connector exposes both an LLM instance and an embeddings model instance consumed by `ConnectorManager`.

### Prompt templates (modules/prompts/)

Templates are plain `.txt` files loaded by `prompts_manager.py`. Naming: `{system|human|analyzer}_{language}.txt`. `AI_PERSONA` env var is injected into the system prompt at load time.

### Configuration (modules/configs.py)

Single `Config` class wrapping `python-dotenv`. All `.env` keys have defaults. Localization strings come from `texts/{LANGUAGE}.properties` key=value files; accessed as `config.texts["key"]`.

## Build-mode setup

When the app runs as a PyInstaller executable (`sys.frozen`), it does **not** read `.env`. Instead:

1. On first launch, `Config.needs_setup` is `True` and `main.py` opens the **setup wizard** (`modules/setup_app.py`) — a ttkbootstrap GUI that collects all LLM provider settings.
2. Settings are saved to `%APPDATA%\rpguide\config.json` (Windows) or `~/rpguide/config.json` (other platforms).
3. On subsequent launches, `Config` loads from that JSON file, injecting values into `os.environ` before reading them — the rest of the startup path is unchanged.
4. In dev mode (`sys.frozen` is False), the existing `.env` flow is preserved.

The setup wizard (`run_setup()`) can be re-invoked at any time to reconfigure the app.

## Key env vars

| Var | Values |
|-----|--------|
| `LLM_TYPE` | `gemini`, `openai`, `lmstudio`, `ollama`, `anthropic` |
| `LLM_AI_API_KEY` | provider API key (not required for `lmstudio` / `ollama`) |
| `LLM_AI_BASE_URL` | custom API base URL — required for `lmstudio` and `ollama`; optional override for `openai` |
| `LLM_AI_MODEL` | model ID string |
| `EMBEDDINGS_AI_MODEL` | embeddings model ID (unused for `anthropic` — RAG is disabled) |
| `LANGUAGE` | `en_us`, `pt_br` |
| `DEBUG` | `true` / `false` — shows agent routing decisions in UI |
| `LOCAL_KNOWLEDGE_PATH` | path to docs for RAG |
| `MODE` | `gui` / `terminal` |

## Code conventions

- snake_case functions/vars, PascalCase classes, UPPER_CASE constants, `_prefix` for private.
- Type hints on all function signatures; use `typing` module for complex types.
- Google-style docstrings.
- Group imports: stdlib → third-party → local (explicit relative: `from .module import ...`).

---

## Agent Workflow Rules

These rules govern how the AI agent must behave throughout every task in this project. They are non-negotiable and apply to every change, no matter how small.

### 1. Understand the Task First

- Read and analyze the full request before writing any code or running any command.
- If requirements, constraints, or expected outcomes are unclear or ambiguous, ask for clarification before proceeding. Never assume.
- Identify which modules, files, and env vars are affected based on the architecture described above.

### 2. Analyze the Execution Environment

- This project runs on **Windows 11** with **bash** as the primary shell (Git Bash / WSL context). Use Unix-style paths (`/`) and Unix shell syntax unless the user explicitly requests otherwise.
- The correct Python binary on this system is `python` (not `python3`). Always verify with `python --version` before running scripts if there is any doubt.
- Never hard-code OS-specific paths or shell syntax. Prefer env vars and cross-platform constructs.
- If a command fails due to environment mismatch (wrong binary, wrong shell, wrong path separator), diagnose and fix the root cause — do not bypass with workarounds.

### 3. Plan Before Implementing

- Break every task into small, logical, and reversible steps before touching any file.
- Identify risks: which changes could break existing agents (RAG, SimpleLLM, PromptAnalyzer), the FAISS index, the connector swap mechanism, or the GUI/terminal dispatch.
- State the plan clearly when the task is non-trivial. Only proceed after the plan is understood.
- Prefer adding over replacing; prefer reversible over destructive.

### 4. Coding Standards (Enforced)

- Follow all conventions in the **Code conventions** section above — no exceptions.
- Do not modify code unrelated to the task. Scope changes tightly.
- Do not add speculative features, extra configurability, or "future-proof" abstractions not asked for.
- Do not add docstrings, comments, or type hints to code you did not change.
- Do not introduce new env vars without adding them to the **Key env vars** table in this file.
- Security: never log API keys, never expose credentials, never introduce injection vectors in prompt construction or file loading paths.

### 5. Test Every Change

- After any implementation, run the full test suite:
  ```bash
  uv run pytest tests/ -v
  ```
- For targeted changes, run the relevant test file:
  ```bash
  uv run pytest tests/test_<module>.py -v
  ```
- If the change affects agent routing, RAG retrieval, or connector behavior, write or update tests to cover it before committing.
- Never commit code that causes test failures. Fix the root cause — do not disable or delete tests to make the suite pass.

### 6. Self-Review Before Committing

Before creating any commit, verify:
- [ ] The change does exactly what was requested — nothing more, nothing less.
- [ ] No unrelated files were modified (`git diff --stat`).
- [ ] All tests pass.
- [ ] No secrets, API keys, or `.env` contents are staged.
- [ ] New or changed env vars are documented in the **Key env vars** table.
- [ ] The commit message is clear, descriptive, and starts with `[AI Generated]`.

### 7. Commit Message Format

Every commit created by the agent **must** follow this format:

```
[AI Generated] <type>: <short description>

<optional body explaining what changed and why>
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`.

Example:
```
[AI Generated] feat: add RTF support to docs_manager loader pipeline
```

### 8. Version Control Discipline

- **Never commit directly to `main`.** Every task must be developed on a dedicated branch.
- Branch naming: `feature/<slug>`, `fix/<slug>`, or `chore/<slug>`.
- Only merge to `main` via a pull request, and only when the user explicitly requests it.
- Never force-push, never reset published commits, never use `--no-verify` to skip hooks.
- If a pre-commit hook fails, fix the underlying issue — do not bypass it.

### 9. Pull Request Standards

Every pull request created by the agent **must** follow these rules:

**Title format:**
```
<type>: <short description>
```
Same types as commit messages: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`.

**Body must include:**

```markdown
## Summary

- <bullet describing what changed and why>

## Test plan

- [ ] <manual or automated step to verify the change>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

**Rules:**
- The `🤖 Generated with [Claude Code](https://claude.com/claude-code)` footer is **mandatory** — it makes AI authorship explicit and traceable.
- The summary must describe *what* changed and *why*, not just list files.
- The test plan must include at least one concrete, actionable verification step.
- Do not open a PR unless all tests pass and the self-review checklist (Rule 6) is complete.
- Target branch is always `main` unless the user specifies otherwise.
- Before creating the PR, verify the branch is pushed to remote (`git push -u origin <branch>`).
