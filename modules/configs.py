from dotenv import load_dotenv
import os
import configparser

load_dotenv()

def load_texts(filepath: str) -> dict:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Localization file not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        # Filter comments and empty lines for safety
        lines = [
            line for line in f
            if line.strip() and not line.strip().startswith(("#", "!"))
        ]
        content = "[DEFAULT]\n" + "".join(lines)

    parser = configparser.ConfigParser(strict=False, interpolation=None)
    parser.read_string(content)
    return dict(parser["DEFAULT"])

class Config:
    LLM_TYPE = os.getenv("LLM_TYPE")
    LLM_AI_API_KEY = os.getenv("LLM_AI_API_KEY")
    LLM_AI_MODEL = os.getenv("LLM_AI_MODEL")
    LLM_AI_TEMPERATURE = float(os.getenv("LLM_AI_TEMPERATURE"))
    LANGUAGE = os.getenv("LANGUAGE")
    AI_PERSONA = os.getenv("AI_PERSONA")
    LOCAL_KNOWLEDGE_PATH = os.getenv("LOCAL_KNOWLEDGE_PATH")
    LOCAL_KNOWLEDGE_DOC_TYPES = os.getenv("LOCAL_KNOWLEDGE_DOC_TYPES").split(",")
    EMBEDDINGS_AI_MODEL = os.getenv("EMBEDDINGS_AI_MODEL")
    texts = load_texts(f"texts/{LANGUAGE}.properties")

config = Config()