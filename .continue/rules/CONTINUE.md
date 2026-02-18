# rpguide Project Guide

## Project Overview

rpguide is a Personal Persona-Based AI Assistant that provides intelligent question answering through a multi-agent architecture. The system routes questions between two specialized agents:
- **RAG Agent**: Answers questions using loaded knowledge documents (Retrieval-Augmented Generation)
- **Simple LLM Agent**: Handles general questions without document context

The application features both GUI and terminal interfaces with multi-language support (English/Portuguese) and debug mode for development.

## Getting Started

### Prerequisites
- Python 3.7+
- pip package manager
- Required dependencies listed in `requirements.txt`

### Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create environment configuration:
   ```bash
   cp .env.example .env
   ```
4. Configure environment variables in `.env` file

### Basic Usage
```bash
# Run in GUI mode (default)
python3 main.py

# Run in terminal mode
python3 main.py terminal
```

### Running Tests
The project includes comprehensive unit tests:
```bash
# Run all tests
python3 run_tests.py

# Or directly with pytest
python3 -m pytest tests/
```

## Project Structure

```
.
├── .env.example          # Example environment file
├── .git/                 # Git repository
├── main.py               # Main entry point
├── modules/              # Core application modules
│   ├── configs.py        # Configuration management
│   ├── connectors/       # LLM connector implementations  
│   │   └── gemini_connector.py
│   ├── connectors_manager.py  # Agent manager and routing logic
│   ├── docs_manager.py   # Document loading and processing
│   ├── prompts/          # Prompt templates
│   │   ├── analyzer_en_us.txt
│   │   ├── human_en_us.txt  
│   │   └── system_en_us.txt
│   └── prompts_manager.py
├── texts/                # Localization files (language support)
│   ├── en_us.properties
│   └── pt_br.properties
├── terminal/             # Terminal interface modules
│   └── app.py
├── gui/                  # GUI interface modules  
│   └── app.py
├── run_tests.py          # Test runner script
└── tests/                # Unit test files
```

## Development Workflow

### Coding Standards
- Follow Python 3 syntax and PEP 8 style guidelines
- Modular design with clear separation of concerns
- Type hints where appropriate
- Proper error handling and logging
- Use of absolute imports for clarity

### Testing Approach
The project includes a comprehensive unit testing framework:
- Tests organized by module (`tests/test_*.py`)
- Mocking used to isolate dependencies
- Coverage for all major components including agents, managers, and configuration
- Non-interactive tests that don't launch GUI or terminal interfaces
- Test runner script (`run_tests.py`) for easy execution

### Build and Deployment
No complex build process required:
1. Install dependencies via `pip install -r requirements.txt`
2. Configure environment variables in `.env` file
3. Run with `python3 main.py`

### Contribution Guidelines
1. Follow existing code patterns and conventions
2. Write unit tests for new functionality
3. Maintain clear, descriptive commit messages
4. Keep changes focused and well-documented

## Key Concepts

### Multi-Agent Architecture
The system uses a multi-agent approach:
- **PromptAnalyzerAgent**: Determines whether to use RAG or simple LLM based on question content
- **RAGAgent**: Processes questions using document embeddings and context retrieval  
- **SimpleLLMAgent**: Handles general questions without document context

### Decision Logic
Questions are routed based on:
- Keywords like "find", "search", "reference" (RAG indicators)
- Question length (>200 characters) 
- Specific phrases like "summarize", "detailed"
- LLM classification when available
- Fallback heuristics for edge cases

### Configuration System
- Environment variables via python-dotenv
- Language localization through `.properties` files
- Flexible configuration management in `configs.py`
- Default values for all settings

## Common Tasks

### Adding New Prompt Templates
1. Create new prompt files in `modules/prompts/`
2. Update `PromptsManager` to load the new template
3. Reference in relevant agent logic

### Adding New LLM Support
1. Create new connector class in `modules/connectors/`
2. Implement required methods (LLM, embeddings)
3. Update `ConnectorManager.getConnector()` method to handle new type

### Extending Document Support
1. Add document types to `LOCAL_KNOWLEDGE_DOC_TYPES` in `.env`
2. Ensure appropriate file loaders exist for new formats
3. Test with sample documents

### Adding New Languages
1. Create new `.properties` file in `texts/` (e.g., `fr_fr.properties`)
2. Update language detection logic if needed
3. Add localization support to all user-facing strings

## Troubleshooting

### Common Issues

**Environment Variables Not Loading**
- Ensure `.env` file exists and is properly formatted
- Check that environment variables are set correctly
- Verify `.env.example` for required variables

**LLM Connection Errors**
- Verify `LLM_AI_API_KEY` is valid
- Check `LLM_TYPE` matches your provider (gemini, etc.)
- Ensure correct model IDs are specified

**Document Loading Failures**
- Confirm `LOCAL_KNOWLEDGE_PATH` exists and is accessible
- Validate document file types in `LOCAL_KNOWLEDGE_DOC_TYPES`
- Check file permissions for knowledge documents

### Debugging Tips

1. **Enable debug mode**: Set `DEBUG=true` in `.env` to see agent routing information
2. **Test individual components**: Run specific tests with `python3 -m pytest tests/test_<component>.py`
3. **Check configuration**: Print config values to verify environment loading
4. **Use test runner**: Execute `run_tests.py` for comprehensive test execution

## References

### Key Technologies
- [LangChain](https://www.langchain.com/) - LLM application framework
- [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap) - GUI toolkit
- [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/) - PDF processing
- [FAISS](https://github.com/facebookresearch/faiss) - Vector similarity search

### Documentation
- [LangChain Documentation](https://python.langchain.com/docs/)
- [Python dotenv documentation](https://github.com/theskumar/python-dotenv)
- [Python configparser documentation](https://docs.python.org/3/library/configparser.html)

### Related Resources
- LLM Provider API documentation (e.g., Google Gemini, OpenAI)
- Vector database documentation for FAISS usage
- Prompt engineering best practices