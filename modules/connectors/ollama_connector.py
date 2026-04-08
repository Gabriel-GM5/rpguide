from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings

_DEFAULT_BASE_URL = "http://localhost:11434"


class OllamaConnector:
    def __init__(self, base_url: str, llm_model: str, embedding_model: str, temperature: float):
        effective_base_url = base_url or _DEFAULT_BASE_URL
        self.llm = ChatOllama(
            base_url=effective_base_url,
            model=llm_model,
            temperature=temperature,
        )
        self.embeddings = OllamaEmbeddings(
            base_url=effective_base_url,
            model=embedding_model,
        )

    def ask(self, question: str):
        return self.llm.invoke(question)
