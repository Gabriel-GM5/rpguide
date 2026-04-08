from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings

_DEFAULT_BASE_URL = "http://localhost:1234/v1"
_DUMMY_API_KEY = "lmstudio"


class LMStudioConnector:
    def __init__(self, base_url: str, llm_model: str, embedding_model: str, temperature: float):
        effective_base_url = base_url or _DEFAULT_BASE_URL
        self.llm = ChatOpenAI(
            openai_api_key=_DUMMY_API_KEY,
            openai_api_base=effective_base_url,
            model=llm_model,
            temperature=temperature,
        )
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=_DUMMY_API_KEY,
            openai_api_base=effective_base_url,
            model=embedding_model,
        )

    def ask(self, question: str):
        return self.llm.invoke(question)
