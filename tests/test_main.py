import os
import sys
from unittest.mock import patch, MagicMock

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

def test_main_module_import():
    """Test that main module can be imported without errors"""
    try:
        # This should not raise any exceptions
        from main import main
        assert callable(main)
    except Exception as e:
        assert False, f"Failed to import main: {e}"


def test_main_mode_selection():
    """Test main function mode selection logic"""
    # Save original environment
    original_env = dict(os.environ)
    try:
        # Test with no arguments (should default to gui)
        with patch('sys.argv', ['main.py']):
        with patch('modules.configs.Config') as mock_config_class:
            mock_config = MagicMock()
            mock_config.MODE = "gui"  # Default from .env
            mock_config_class.return_value = mock_config
            
            # Mock the run functions to avoid actual execution
            with patch('modules.terminal_app.run_terminal') as mock_terminal, \
                 patch('modules.gui_app.run_gui') as mock_gui:
                
                # Import and call main function
                from main import main
                
                # This should not raise exceptions
                try:
                    main()
                except SystemExit:
                    pass  # Expected on error

                    # Verify that appropriate function was called based on mode
                    # Since default is gui, run_gui should be called
                mock_gui.assert_called_once()
    finally:
        # Restore original environment
        os.environ.clear()
        os.environ.update(original_env)


def test_main_invalid_mode():
    """Test main function with invalid mode argument"""
    # Save original environment
    original_env = dict(os.environ)

    try:
        with patch('sys.argv', ['main.py', 'invalid_mode']):
            with patch('modules.configs.Config') as mock_config_class:
                mock_config = MagicMock()
                mock_config.MODE = "gui"  # Default from .env
                mock_config_class.return_value = mock_config

                # Mock the run functions to avoid actual execution
                with patch('modules.terminal_app.run_terminal') as mock_terminal, \
                     patch('modules.gui_app.run_gui') as mock_gui:

                    # Import and call main function
                    from main import main

                    # This should not raise exceptions
                    try:
                        main()
                    except SystemExit:
                        pass  # Expected on error
    finally:
        # Restore original environment
        os.environ.clear()
        os.environ.update(original_env)


def test_main_valid_mode_argument():
    """Test main function with valid mode argument"""
    # Save original environment
    original_env = dict(os.environ)

    try:
        # Test with terminal argument
        with patch('sys.argv', ['main.py', 'terminal']):
            with patch('modules.configs.Config') as mock_config_class:
                mock_config = MagicMock()
                mock_config.MODE = "gui"  # Default from .env
                mock_config_class.return_value = mock_config

                # Mock the run functions to avoid actual execution
                with patch('modules.terminal_app.run_terminal') as mock_terminal, \
                     patch('modules.gui_app.run_gui') as mock_gui:

                    # Import and call main function
                    from main import main

                    # This should not raise exceptions
                    try:
                        main()
                    except SystemExit:
                        pass  # Expected on error

                    # Verify that appropriate function was called based on argument
                    mock_terminal.assert_called_once()
    finally:
        # Restore original environment
        os.environ.clear()
        os.environ.update(original_env)


def test_main_with_gui_mode():
    """Test main function with gui mode argument"""
    # Save original environment
    original_env = dict(os.environ)

    try:
        # Test with gui argument
        with patch('sys.argv', ['main.py', 'gui']):
            with patch('modules.configs.Config') as mock_config_class:
                mock_config = MagicMock()
                mock_config.MODE = "terminal"  # Default from .env
                mock_config_class.return_value = mock_config

                # Mock the run functions to avoid actual execution
                with patch('modules.terminal_app.run_terminal') as mock_terminal, \
                     patch('modules.gui_app.run_gui') as mock_gui:

                    # Import and call main function
                    from main import main

                    # This should not raise exceptions
                    try:
                        main()
                    except SystemExit:
                        pass  # Expected on error

                    # Verify that appropriate function was called based on argument
                    mock_gui.assert_called_once()
    finally:
        # Restore original environment
        os.environ.clear()
        os.environ.update(original_env)
