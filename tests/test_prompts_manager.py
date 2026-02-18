import os
import sys
from unittest.mock import patch, MagicMock

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

from modules.prompts_manager import PromptsManager


def test_prompts_manager_init():
    """Test PromptsManager initialization"""
    # Mock config with required attributes
    mock_config = MagicMock()
    mock_config.AI_PERSONA = "Test Persona"
    mock_config.texts = {'exit.term': 'quit'}
    
    # Mock file reading to avoid actual file I/O
    mock_system_prompt = "System prompt content"
    mock_human_prompt = "Human prompt content"
    mock_analyzer_prompt = "Analyzer prompt content"
    
    with patch('modules.prompts_manager.open') as mock_open:
        # Setup mock file reads
        mock_file_context = MagicMock()
        mock_file_context.read.return_value = mock_system_prompt
        mock_open.return_value.__enter__.return_value = mock_file_context
        
        # First call for system prompt
        mock_open.reset_mock()
        mock_file_context.read.return_value = mock_system_prompt
        mock_open.return_value.__enter__.return_value = mock_file_context
        
        # Second call for human prompt  
        mock_open.reset_mock()
        mock_file_context.read.return_value = mock_human_prompt
        mock_open.return_value.__enter__.return_value = mock_file_context
        
        # Third call for analyzer prompt
        mock_open.reset_mock()
        mock_file_context.read.return_value = mock_analyzer_prompt
        mock_open.return_value.__enter__.return_value = mock_file_context
        
        # Mock os.path.exists to return True for all files
        with patch('os.path.exists', return_value=True):
            prompts_mgr = PromptsManager(mock_config)
            
            assert prompts_mgr.system_prompt is not None
            assert prompts_mgr.human_prompt is not None
            assert prompts_mgr.analyzer_prompt is not None


def test_prompts_manager_get_prompts():
    """Test PromptsManager get_prompts method"""
    # Mock config with required attributes
    mock_config = MagicMock()
    mock_config.AI_PERSONA = "Test Persona"
    mock_config.texts = {'exit.term': 'quit'}
    
    # Mock file reading
    mock_system_prompt = "System prompt content with {PERSONA_DESCRIPTION} and {EXIT_COMMAND}"
    mock_human_prompt = "Human prompt content with {input} and {context}"
    
    with patch('modules.prompts_manager.open') as mock_open:
        mock_file_context = MagicMock()
        
        # Setup for system prompt
        mock_file_context.read.return_value = mock_system_prompt
        mock_open.return_value.__enter__.return_value = mock_file_context
        
        # Reset for human prompt
        mock_open.reset_mock()
        mock_file_context.read.return_value = mock_human_prompt
        mock_open.return_value.__enter__.return_value = mock_file_context
        
        with patch('os.path.exists', return_value=True):
            prompts_mgr = PromptsManager(mock_config)
            
            # Test get_prompts method
            prompt_template = prompts_mgr.get_prompts()
            assert prompt_template is not None


def test_prompts_manager_get_analyzer_prompt():
    """Test PromptsManager get_analyzer_prompt method"""
    # Mock config with required attributes
    mock_config = MagicMock()
    mock_config.AI_PERSONA = "Test Persona"
    mock_config.texts = {'exit.term': 'quit'}
    
    # Mock file reading for analyzer prompt
    mock_analyzer_prompt = "Analyzer prompt content"
    
    with patch('modules.prompts_manager.open') as mock_open:
        mock_file_context = MagicMock()
        mock_file_context.read.return_value = mock_analyzer_prompt
        mock_open.return_value.__enter__.return_value = mock_file_context
        
        with patch('os.path.exists', return_value=True):
            prompts_mgr = PromptsManager(mock_config)
            
            # Test get_analyzer_prompt method
            analyzer_prompt = prompts_mgr.get_analyzer_prompt()
            assert analyzer_prompt == mock_analyzer_prompt


def test_prompts_manager_missing_files():
    """Test PromptsManager behavior when prompt files are missing"""
    # Mock config with required attributes
    mock_config = MagicMock()
    mock_config.AI_PERSONA = "Test Persona"
    mock_config.texts = {'exit.term': 'quit'}
    
    with patch('os.path.exists', return_value=False):
        try:
            prompts_mgr = PromptsManager(mock_config)
            # This should raise FileNotFoundError
            assert False, "Should have raised FileNotFoundError"
        except FileNotFoundError:
            pass  # Expected behavior