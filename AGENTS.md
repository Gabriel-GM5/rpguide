# Project AGENT Guidelines

## Build, Lint, and Test Commands

### Running Tests
- Run all tests: `python run_tests.py`
- Run a single test file: `python -m pytest tests/test_filename.py -v`
- Run a specific test function: `python -m pytest tests/test_filename.py::test_function_name -v`
- Run tests with coverage: `python -m pytest tests/ --cov=modules/ --cov-report=html`

### Linting
- Check code style: `pylint modules/`
- Format code: `black modules/`
- Check for issues: `flake8 modules/`

### Development Commands
- Install dependencies: `pip install -r requirements.txt`
- Run in GUI mode: `python main.py`
- Run in terminal mode: `python main.py terminal`

## Code Style Guidelines

### Imports
- Group imports in order: standard library, third-party, local modules
- Use explicit relative imports for local modules (`from .module import function`)
- Import full module names for third-party libraries
- Avoid wildcard imports (`from module import *`)

### Naming Conventions
- Variables and functions: snake_case
- Classes: PascalCase
- Constants: UPPER_CASE
- Private methods: _private_method (leading underscore)
- Protected attributes: _protected_attribute

### Type Hints
- Use type hints for all function parameters and return values
- Use typing modules (List, Dict, Optional, etc.) for complex types
- Prefer `str` over `Union[str, None]` for optional strings

### Error Handling
- Catch specific exceptions rather than using bare `except:`
- Log errors appropriately with meaningful messages
- Use try/except blocks around potentially failing operations
- Raise custom exceptions when appropriate

### Documentation
- Add docstrings to all functions and classes (Google style)
- Document parameters, return values, and exceptions
- Include examples where helpful

### Code Structure
- Keep functions short and focused on single responsibilities
- Use meaningful variable names that describe their purpose
- Break complex logic into smaller, testable functions
- Maintain consistent indentation (4 spaces)
- Follow PEP 8 style guide for Python code

## Environment Configuration

The project uses environment variables for configuration. Key variables include:
- `LLM_TYPE`: e.g., 'gemini'
- `LLM_AI_API_KEY`: Your provider API key
- `LLM_AI_MODEL`: The model ID to use
- `EMBEDDINGS_AI_MODEL`: The embedding model ID
- `LANGUAGE`: 'en_us' or 'pt_br'
- `DEBUG`: 'true' or 'false' for debug output
- `MODE`: 'gui' or 'terminal'

## Testing Approach

Tests are organized in the `tests/` directory with test files named `test_<module>.py`. Each test file should contain:
- Test functions prefixed with `test_`
- Use of pytest fixtures where appropriate
- Clear, descriptive test names
- Comprehensive coverage of edge cases and error conditions

## Code Quality Standards

- All code must pass linting checks before merging
- Tests must pass for all changes
- Maintain backward compatibility in API changes
- Follow the existing code patterns and conventions
- Write tests for new features and bug fixes