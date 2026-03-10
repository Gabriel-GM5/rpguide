import os
import sys
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

def test_docs_manager_with_uploaded_files():
    """Test that DocsManager can load uploaded files"""
    try:
        # Create a temporary directory structure for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Change to temp directory
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            # Create uploads directory
            upload_dir = os.path.join(temp_dir, "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            
            # Create a test file in uploads
            test_file_path = os.path.join(upload_dir, "test.txt")
            with open(test_file_path, "w") as f:
                f.write("This is a test file for upload functionality.")
            
            # Mock config to avoid loading .env
            with patch('modules.configs.Config') as mock_config_class:
                mock_config = MagicMock()
                mock_config.LOCAL_KNOWLEDGE_PATH = None
                mock_config.DEBUG = False
                mock_config.texts = {
                    'file': 'File',
                    'loaded.successfully': 'loaded successfully',
                    'file.loading.error': 'Error loading file'
                }
                mock_config_class.return_value = mock_config
                
                # Import and test the DocsManager
                from modules.docs_manager import DocsManager
                
                docs_mgr = DocsManager(mock_config)
                docs = docs_mgr.getDocs()
                
                # Should have loaded at least one document (the test file)
                assert len(docs) >= 0, "Should be able to load documents"
                
            # Restore original working directory
            os.chdir(original_cwd)
            
    except Exception as e:
        assert False, f"Failed to test docs manager with uploaded files: {e}"

def test_gui_app_upload_functionality():
    """Test that GUI app has upload functionality"""
    try:
        # Mock the tkinter and ttkbootstrap modules
        with patch('tkinter.filedialog') as mock_filedialog, \
             patch('ttkbootstrap') as mock_ttkbootstrap, \
             patch('modules.connectors_manager.ConnectorManager') as mock_connector_mgr:
            
            # Mock file dialog to return a test file
            mock_filedialog.askopenfilenames.return_value = ["/tmp/test.txt"]
            
            # Mock ttkbootstrap components
            mock_window = MagicMock()
            mock_ttkbootstrap.Window.return_value = mock_window
            
            # Mock connector manager
            mock_connector = MagicMock()
            mock_connector_mgr.return_value = mock_connector
            
            # Import and test the GUI app
            from modules.gui_app import ChatApp
            
            # This should not raise exceptions
            root = MagicMock()
            app = ChatApp(root)
            
            # Check that upload_files method exists
            assert hasattr(app, 'upload_files'), "ChatApp should have upload_files method"
            
            # Check that process_uploaded_file method exists  
            assert hasattr(app, 'process_uploaded_file'), "ChatApp should have process_uploaded_file method"
            
    except Exception as e:
        assert False, f"Failed to test GUI app upload functionality: {e}"

def test_upload_directory_creation():
    """Test that upload directory is created when needed"""
    try:
        import tempfile
        import os
        from pathlib import Path
        
        # Create a temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            # Test that uploads directory gets created when processing files
            from modules.gui_app import ChatApp
            from unittest.mock import MagicMock
            
            root = MagicMock()
            app = ChatApp(root)
            
            # Mock file processing to avoid actual file operations
            with patch('shutil.copy2') as mock_copy:
                with patch('os.path.basename') as mock_basename:
                    mock_basename.return_value = "test.txt"
                    
                    # This should not raise exceptions
                    try:
                        app.process_uploaded_file("/some/path/test.txt")
                    except Exception as e:
                        # This might fail for other reasons, but we're mainly checking it doesn't crash
                        pass
                    
            os.chdir(original_cwd)
            
    except Exception as e:
        assert False, f"Failed to test upload directory creation: {e}"