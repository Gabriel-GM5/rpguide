# rpguide

Personal Persona-Based AI Assistant for General Purposes Usage

A multi-agent AI assistant with a modern GUI chat interface. The system intelligently routes questions between a Retrieval-Augmented Generation (RAG) agent for document-based answers and a simple LLM agent for general queries.

## Features

- **Multi-Agent Architecture**:
  - Prompt Analyzer Agent: Classifies questions as RAG or simple LLM
  - RAG Agent: Answers questions using loaded knowledge documents
  - Simple LLM Agent: Answers general questions without document context
- **GUI & Terminal Modes**: Modern ttkbootstrap-based GUI or lightweight terminal chat
- **Multi-language Support**: English (`en_us`) and Portuguese (`pt_br`)
- **Debug Mode**: Optional debug output showing which agent handles each request
- **Rich Document Loading**: PDF, Word, Excel, CSV, HTML, RTF, PPTX, Markdown, plain text
- **File Upload**: Upload files directly through the GUI for on-the-fly RAG ingestion
- **Multiple LLM Providers**: Gemini, OpenAI, LM Studio, Ollama, Anthropic/Claude
- **Standalone Executable**: Distributable `.exe` built with PyInstaller (no Python install required)

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (replaces pip/venv)

Install `uv` once:

```bash
pip install uv
```

## Installation

```bash
# Clone the repo
git clone https://github.com/Gabriel-GM5/rpguide.git
cd rpguide

# Install all dependencies (creates .venv automatically)
uv sync --dev
```

## Configuration

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

| Variable | Description |
|----------|-------------|
| `LLM_TYPE` | `gemini`, `openai`, `lmstudio`, `ollama`, `anthropic` |
| `LLM_AI_API_KEY` | Provider API key (not required for `lmstudio` / `ollama`) |
| `LLM_AI_BASE_URL` | Custom API base URL — required for `lmstudio` and `ollama`; optional override for `openai` |
| `LLM_AI_MODEL` | Model ID string |
| `EMBEDDINGS_AI_MODEL` | Embeddings model ID (unused when `LLM_TYPE=anthropic`) |
| `LLM_AI_TEMPERATURE` | Temperature value (0.0–1.0) |
| `LANGUAGE` | `en_us` or `pt_br` |
| `AI_PERSONA` | Description of the AI assistant's personality |
| `LOCAL_KNOWLEDGE_PATH` | Path to your local knowledge documents |
| `LOCAL_KNOWLEDGE_DOC_TYPES` | Comma-separated file types, e.g. `pdf,txt,md` |
| `DEBUG` | `true` / `false` — shows agent routing decisions in the UI |
| `MODE` | `gui` (default) or `terminal` |

### Provider-specific notes

**LM Studio:**
```
LLM_TYPE=lmstudio
LLM_AI_BASE_URL=http://localhost:1234/v1
LLM_AI_MODEL=<model-name>
EMBEDDINGS_AI_MODEL=<model-name>
```

**Ollama:**
```
LLM_TYPE=ollama
LLM_AI_BASE_URL=http://localhost:11434
LLM_AI_MODEL=<model-name>
EMBEDDINGS_AI_MODEL=<model-name>
```

**Anthropic/Claude** — RAG is disabled (no embeddings API); only `SimpleLLMAgent` is used.

## Running

```bash
# GUI mode (default)
uv run python main.py

# Terminal mode
uv run python main.py terminal
```

The `MODE` env var also controls the default; the CLI argument takes precedence.

### File Upload

Use the **Upload Files** button in the GUI to add documents at runtime. Files are saved to `uploads/` and automatically ingested into the RAG pipeline. Supported formats: `.pdf`, `.txt`, `.doc`, `.docx`, `.xls`, `.xlsx`, `.md`, `.html`, `.htm`, `.rtf`, `.csv`, `.pptx`.

## Building a Standalone Executable

The project ships with a PyInstaller spec (`rpguide.spec`) that produces a one-directory Windows executable with a d20 icon.

**1. Generate the icon** (only needed once, or after modifying `create_icon.py`):

```bash
uv run python create_icon.py
```

This writes `icon.ico` to the project root.

**2. Build the executable:**

```bash
uv run pyinstaller rpguide.spec
```

Output is placed in `dist/rpguide/`. Run `dist/rpguide/rpguide.exe` — no Python installation required on the target machine.

> Build artifacts (`build/`, `dist/`) are git-ignored. Do not commit them.

## Development

```bash
# Run tests
uv run pytest tests/ -v

# Run tests with coverage
uv run pytest tests/ --cov=modules/ --cov-report=html

# Lint / format
uv run pylint modules/
uv run black modules/
uv run flake8 modules/

# Add a dependency
uv add <package>          # production
uv add --dev <package>    # dev only
```

## Project Structure

```
.
├── .env.example              # Environment variable template
├── .gitignore
├── create_icon.py            # Generates icon.ico for the exe build
├── icon.ico                  # d20-themed application icon
├── main.py                   # Entry point — dispatches to GUI or terminal
├── modules/
│   ├── configs.py            # Config + .env loading; PyInstaller path resolution
│   ├── connectors/           # One file per LLM provider
│   │   ├── anthropic_connector.py
│   │   ├── gemini_connector.py
│   │   ├── lmstudio_connector.py
│   │   ├── ollama_connector.py
│   │   └── openai_connector.py
│   ├── connectors_manager.py # Agent orchestration (RAG / SimpleLLM / Analyzer)
│   ├── docs_manager.py       # Document loading, chunking, FAISS indexing
│   └── prompts/
│       └── prompts_manager.py
├── gui_app.py                # ttkbootstrap GUI chat interface
├── terminal_app.py           # Terminal chat interface
├── rpguide.spec              # PyInstaller build spec
├── pyproject.toml            # Project metadata and dependencies (uv)
├── texts/                    # Localization files (*.properties)
├── uploads/                  # Runtime file upload directory
└── tests/                    # Pytest test suite
```

## License

This project is licensed under the MIT License — see [LICENSE.md](LICENSE.md) for details.
