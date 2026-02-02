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

- `LLM_TYPE` - e.g. `gemini`
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

## Running the Application

Start the application:

```bash
python3 main.py
```

The application will run in the mode specified by the `MODE` environment variable:

- **GUI Mode** (`MODE=gui`): Opens a modern chat window with conversation history.
- **Terminal Mode** (`MODE=terminal`): Runs a command-line chat interface in the terminal.

Type your questions and press Enter. Type the exit command (configured in your language settings) to exit the application.
