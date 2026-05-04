from dotenv import load_dotenv
import json
import os
import sys
import configparser

_FROZEN: bool = getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")

if not _FROZEN:
    load_dotenv()


def _resource_base() -> str:
    """Return the directory that contains bundled resources at runtime.

    When running as a PyInstaller bundle (frozen), data files land in
    sys._MEIPASS; otherwise fall back to the current working directory so that
    the original relative-path behaviour is preserved for dev/test runs.
    """
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.getcwd()

def _user_config_dir() -> str:
    appdata = os.environ.get("APPDATA") or os.path.expanduser("~")
    return os.path.join(appdata, "rpguide")


def _user_config_path() -> str:
    return os.path.join(_user_config_dir(), "config.json")


def load_user_config() -> dict:
    """Load persisted user config from the OS user-data directory."""
    path = _user_config_path()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_user_config(data: dict) -> None:
    """Persist user config to the OS user-data directory."""
    os.makedirs(_user_config_dir(), exist_ok=True)
    with open(_user_config_path(), "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


def load_texts(filepath: str) -> dict:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Localization file not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        lines = [
            line for line in f
            if line.strip() and not line.strip().startswith(("#", "!"))
        ]
        content = "[DEFAULT]\n" + "".join(lines)

    parser = configparser.ConfigParser(strict=False, interpolation=None)
    parser.read_string(content)
    return dict(parser["DEFAULT"])

class Config:
    def __init__(self):
        if _FROZEN:
            for key, val in load_user_config().items():
                if isinstance(val, str):
                    os.environ[key] = val

        self.needs_setup: bool = _FROZEN and not os.path.exists(_user_config_path())

        self.LLM_TYPE = os.getenv("LLM_TYPE", None)
        self.LLM_AI_API_KEY = os.getenv("LLM_AI_API_KEY", None)
        self.LLM_AI_BASE_URL = os.getenv("LLM_AI_BASE_URL", None)
        self.LLM_AI_MODEL = os.getenv("LLM_AI_MODEL", None)
        self.LLM_AI_TEMPERATURE = float(os.getenv("LLM_AI_TEMPERATURE", "0.0"))
        self.LANGUAGE = os.getenv("LANGUAGE", "en_us")
        self.AI_PERSONA = os.getenv("AI_PERSONA", None)
        self.LOCAL_KNOWLEDGE_PATH = os.getenv("LOCAL_KNOWLEDGE_PATH", None)
        self.LOCAL_KNOWLEDGE_DOC_TYPES = os.getenv("LOCAL_KNOWLEDGE_DOC_TYPES", "").split(",") if os.getenv("LOCAL_KNOWLEDGE_DOC_TYPES") else []
        self.EMBEDDINGS_AI_MODEL = os.getenv("EMBEDDINGS_AI_MODEL", None)
        self.DEBUG = os.getenv("DEBUG", "False").lower() in ("1", "true", "yes", "y")
        self.MODE = os.getenv("MODE", "gui").lower()
        self.texts = load_texts(
            os.path.join(_resource_base(), "texts", f"{self.LANGUAGE}.properties")
        )

config = Config()