from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings


class OpenAIConnector:
    def __init__(self, api_key: str, base_url: str, llm_model: str, embedding_model: str, temperature: float):
        self.llm = ChatOpenAI(
            openai_api_key=api_key,
            openai_api_base=base_url or None,
            model=llm_model,
            temperature=temperature,
        )
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=api_key,
            openai_api_base=base_url or None,
            model=embedding_model,
        )

    def ask(self, question: str):
        return self.llm.invoke(question)
