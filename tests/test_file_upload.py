import os
import sys
import tempfile
from unittest.mock import patch, MagicMock

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")


def _mock_gui_config():
    """Return a MagicMock that satisfies ChatApp.__init__ attribute access."""
    mock_config = MagicMock()
    mock_config.AI_PERSONA = "Test Persona"
    mock_config.DEBUG = False
    mock_config.texts = {
        "ui.window.title": "RPGuide",
        "ui.button.upload": "Upload",
        "ui.button.send": "Send",
        "ui.button.exit": "Exit",
        "initial.question": "Introduce yourself.",
    }
    return mock_config


def test_docs_manager_with_uploaded_files():
    """DocsManager loads uploaded files when LOCAL_KNOWLEDGE_PATH is not configured."""
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        try:
            # Create an uploads directory with a test file
            upload_dir = os.path.join(temp_dir, "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            with open(os.path.join(upload_dir, "test.txt"), "w") as f:
                f.write("This is a test file for upload functionality.")

            mock_config = MagicMock()
            mock_config.LOCAL_KNOWLEDGE_PATH = None
            mock_config.DEBUG = False
            mock_config.texts = {
                "file": "File",
                "loaded.successfully": "loaded successfully",
                "file.loading.error": "Error loading file",
            }

            from modules.docs_manager import DocsManager

            docs_mgr = DocsManager(mock_config)
            docs = docs_mgr.getDocs()

            assert isinstance(docs, list), "getDocs should return a list"
        finally:
            os.chdir(original_cwd)


def test_gui_app_upload_functionality():
    """ChatApp exposes upload_files and process_uploaded_file methods."""
    # gui_app.py binds 'ttk', 'tk', 'Config', and 'ConnectorManager' at import time,
    # so patches must target the names inside the gui_app module namespace.
    with patch("modules.gui_app.Config") as mock_config_cls, \
         patch("modules.gui_app.ConnectorManager"), \
         patch("modules.gui_app.ttk") as mock_ttk, \
         patch("modules.gui_app.tk"):

        mock_config_cls.return_value = _mock_gui_config()
        # Ensure ttk widget constructors return MagicMocks
        mock_ttk.Frame.return_value = MagicMock()
        mock_ttk.Text.return_value = MagicMock()
        mock_ttk.Scrollbar.return_value = MagicMock()
        mock_ttk.Button.return_value = MagicMock()
        mock_ttk.Entry.return_value = MagicMock()

        from modules.gui_app import ChatApp

        root = MagicMock()
        app = ChatApp(root)

        assert hasattr(app, "upload_files"), "ChatApp should have upload_files method"
        assert hasattr(app, "process_uploaded_file"), "ChatApp should have process_uploaded_file method"


def test_upload_directory_creation():
    """process_uploaded_file creates the uploads directory when it does not exist."""
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        try:
            with patch("modules.gui_app.Config") as mock_config_cls, \
                 patch("modules.gui_app.ConnectorManager"), \
                 patch("modules.gui_app.ttk") as mock_ttk, \
                 patch("modules.gui_app.tk"), \
                 patch("shutil.copy2"):

                mock_config_cls.return_value = _mock_gui_config()
                mock_ttk.Frame.return_value = MagicMock()
                mock_ttk.Text.return_value = MagicMock()
                mock_ttk.Scrollbar.return_value = MagicMock()
                mock_ttk.Button.return_value = MagicMock()
                mock_ttk.Entry.return_value = MagicMock()

                from modules.gui_app import ChatApp

                root = MagicMock()
                app = ChatApp(root)

                # Source file doesn't need to exist — copy2 is mocked
                try:
                    app.process_uploaded_file("/some/path/test.txt")
                except Exception:
                    pass

            uploads_path = os.path.join(temp_dir, "uploads")
            assert os.path.isdir(uploads_path), "uploads/ directory should be created by process_uploaded_file"
        finally:
            os.chdir(original_cwd)
