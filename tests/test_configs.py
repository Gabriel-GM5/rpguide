import os
import sys
from unittest.mock import patch, MagicMock

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

from modules.configs import Config, load_texts


def test_load_texts_valid_file():
    """Test loading texts from a valid properties file"""
    # Since we're working with actual files, let's just verify the function can read them properly
    # We'll check that it doesn't throw an error when reading a real file
    
    # Mock os.path.exists to return True for our test path
    with patch('os.path.exists', return_value=True):
        # Test that it handles the configparser correctly by mocking the file read
        mock_content = """
# This is a comment
key1=value1
key2=value2
# Another comment
key3=value3
"""
        
        # Mock the actual file reading
        with patch('builtins.open', return_value=MagicMock(__enter__=lambda _: MagicMock(read=lambda: mock_content))):
            # Mock configparser to return our test data
            with patch('modules.configs.configparser.ConfigParser') as mock_parser_class:
                mock_parser = MagicMock()
                mock_parser_class.return_value = mock_parser
                mock_parser.read_string.return_value = None
                
                # Create a mock dict that returns our values
                mock_dict = {'DEFAULT': {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}}
                mock_parser.__getitem__.side_effect = lambda x: mock_dict[x]
                
                result = load_texts("dummy_path")
                # We're mainly testing that it doesn't crash and can handle the parsing
                assert isinstance(result, dict)


def test_load_texts_file_not_found():
    """Test that load_texts raises FileNotFoundError when file doesn't exist"""
    with patch('os.path.exists', return_value=False):
        try:
            load_texts("nonexistent_path")
            assert False, "Should have raised FileNotFoundError"
        except FileNotFoundError:
            pass  # Expected


def test_config_initialization():
    """Test Config class initialization with mocked environment variables"""
    # Clear any existing env vars and set our own
    original_env = dict(os.environ)
    
    try:
        # Mock environment variables
        mock_env_vars = {
            'LLM_TYPE': 'gemini',
            'LLM_AI_API_KEY': 'test_api_key',
            'LLM_AI_MODEL': 'test_model',
            'LLM_AI_TEMPERATURE': '0.5',
            'LANGUAGE': 'en_us',
            'AI_PERSONA': 'Test Persona',
            'LOCAL_KNOWLEDGE_PATH': '/test/path',
            'LOCAL_KNOWLEDGE_DOC_TYPES': 'pdf,txt',
            'EMBEDDINGS_AI_MODEL': 'test_embeddings_model',
            'DEBUG': 'true',
            'MODE': 'terminal'
        }
        
        # Clear environment and set our test variables
        os.environ.clear()
        os.environ.update(mock_env_vars)
        
        # Mock the load_texts function to avoid file reading
        with patch('modules.configs.load_texts', return_value={'initial.question': 'Hello', 'exit.term': 'quit'}):
            config = Config()
            
            assert config.LLM_TYPE == 'gemini'
            assert config.LLM_AI_API_KEY == 'test_api_key'
            assert config.LLM_AI_MODEL == 'test_model'
            assert config.LLM_AI_TEMPERATURE == 0.5
            assert config.LANGUAGE == 'en_us'
            assert config.AI_PERSONA == 'Test Persona'
            assert config.LOCAL_KNOWLEDGE_PATH == '/test/path'
            assert config.LOCAL_KNOWLEDGE_DOC_TYPES == ['pdf', 'txt']
            assert config.EMBEDDINGS_AI_MODEL == 'test_embeddings_model'
            assert config.DEBUG is True
            assert config.MODE == 'terminal'
            assert 'initial.question' in config.texts
            assert 'exit.term' in config.texts
            
    finally:
        # Restore original environment
        os.environ.clear()
        os.environ.update(original_env)


def test_config_default_values():
    """Test Config class with default values when environment variables are not set"""
    # Clear any existing env vars and set our own
    original_env = dict(os.environ)
    
    try:
        # Mock environment variables with minimal set
        mock_env_vars = {
            'LANGUAGE': 'en_us',
            'DEBUG': 'false',
            'MODE': 'gui'
        }
        
        # Clear environment and set our test variables
        os.environ.clear()
        os.environ.update(mock_env_vars)
        
        # Mock the load_texts function to avoid file reading
        with patch('modules.configs.load_texts', return_value={'initial.question': 'Hello'}):
            config = Config()
            
            # Test defaults
            assert config.LLM_TYPE is None
            assert config.LLM_AI_API_KEY is None
            assert config.LLM_AI_MODEL is None
            assert config.LLM_AI_TEMPERATURE == 0.0  # Default from float conversion
            assert config.AI_PERSONA is None
            assert config.LOCAL_KNOWLEDGE_PATH is None
            assert config.LOCAL_KNOWLEDGE_DOC_TYPES == []  # Default from split()
            assert config.EMBEDDINGS_AI_MODEL is None
            assert config.DEBUG is False
            assert config.MODE == 'gui'
            
    finally:
        # Restore original environment
        os.environ.clear()
        os.environ.update(original_env)
