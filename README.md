# rpguide
Personal Persona-Based AI Assistant for General Purposes Usage

A multi-agent AI assistant with a modern GUI chat interface. The system intelligently routes questions between a Retrieval-Augmented Generation (RAG) agent for document-based answers and a simple LLM agent for general queries.

## Features

- **Multi-Agent Architecture**: 
  - Prompt Analyzer Agent: Classifies questions as RAG or simple LLM
  - RAG Agent: Answers questions using loaded knowledge documents
  - Simple LLM Agent: Answers general questions without document context
- **GUI Chat Interface**: Modern ttkbootstrap-based interface with conversation history
- **Multi-language Support**: English (en_us) and Portuguese (pt_br)
- **Debug Mode**: Optional debug output showing which agent handles each request
- **Document Loading**: Supports PDF, text, and markdown documents
- **File Upload Feature**: Users can upload files directly through the GUI interface for RAG processing
- **Multiple LLM Support**: Google Gemini and LM Studio

## Installation

Install required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Configure the application using environment variables. Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Key variables:

- `LLM_TYPE` - e.g. `gemini` or `lmstudio`
- `LLM_AI_API_KEY` - your provider API key
- `LLM_AI_MODEL` - the model id to use
- `EMBEDDINGS_AI_MODEL` - the embedding model id
- `LLM_AI_TEMPERATURE` - temperature value (0.0-1.0)
- `LANGUAGE` - `en_us` or `pt_br`
- `AI_PERSONA` - description of the AI assistant's personality
- `LOCAL_KNOWLEDGE_PATH` - path to your knowledge documents
- `LOCAL_KNOWLEDGE_DOC_TYPES` - comma-separated file types (e.g., pdfs,txt,md)
- `DEBUG` - `true` or `false` (when `true`, prints which agent is used)
- `MODE` - `gui` for graphical interface or `terminal` for command-line chat (defaults to `gui`)

See `.env.example` for a complete template.

For LM Studio, use:
```
LLM_TYPE=lmstudio
LLM_AI_API_KEY=http://localhost:1234/v1
LLM_AI_MODEL=<model-name>
EMBEDDINGS_AI_MODEL=<model-name>
```

## Running the Application

Start the application in GUI mode (default):

```bash
python3 main.py
```

Or start the application in terminal mode explicitly:

```bash
python3 main.py terminal
```

The application will run in the mode specified by the `MODE` environment variable or command-line argument. When running with no arguments, it defaults to GUI mode. When using the `terminal` argument, it runs in command-line mode instead of GUI mode.

### File Upload Feature

Users can upload files directly through the GUI interface using the "Upload Files" button. Uploaded files will be stored in the `uploads/` directory and automatically included in the RAG processing context.

The system supports uploading various document formats including:
- PDF documents (.pdf)
- Text files (.txt)
- Word documents (.doc, .docx)
- Excel spreadsheets (.xls, .xlsx)
- Markdown files (.md)
- HTML files (.html, .htm)
- Rich Text Format files (.rtf)
- CSV files (.csv)

Uploaded files are automatically processed and made available to the AI assistant for context-aware responses.

### Application Structure

The application is now structured into separate modules for better organization:
- `gui/app.py`: Contains all GUI-related logic and the ChatApp class
- `terminal/app.py`: Contains all terminal-based chat logic
- `main.py`: Main entry point that determines which interface to launch based on configuration or command-line arguments

## Project Structure

```
.
├── .env.example          # Example environment file
├── .git/                 # Git repository
├── .gitattributes
├── .gitignore
├── docs/                 # Documentation files
├── gui/                  # GUI application modules
│   ├── __init__.py
│   └── app.py            # GUI logic and ChatApp class
├── LICENSE.md            # MIT License
├── main.py               # Main entry point
├── modules/              # Core modules
│   ├── configs.py        # Configuration management
│   ├── connectors/
│   ├── connectors_manager.py
│   ├── docs_manager.py
│   └── prompts/
│       └── prompts_manager.py
├── README.md             # This file
├── requirements.txt      # Python dependencies
└── terminal/             # Terminal application modules
    ├── __init__.py
    └── app.py            # Terminal logic
```

## Dependencies

The project requires the following Python packages (as listed in `requirements.txt`):

- langchain_classic==1.0.1
- langchain_community==0.4.1
- langchain_core==1.2.8
- langchain_google_genai==4.2.0
- langchain_unstructured==1.0.1
- python-dotenv==1.2.1
- ttkbootstrap==1.20.1
- PyMuPDF==1.26.7
- faiss-cpu==1.13.2
- langchain-lmstudio==0.1.0

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.