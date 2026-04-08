from dotenv import load_dotenv
import os
import configparser

load_dotenv()

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
        # Use defaults for all values to ensure consistency in tests
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
        self.texts = load_texts(f"texts/{self.LANGUAGE}.properties")

config = Config()