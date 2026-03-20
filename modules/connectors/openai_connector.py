from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings

class OpenAIConnector:
    def __init__(self, api_base, llm_model, embedding_model, temperature):
        self.llm = ChatOpenAI(
            openai_api_base=api_base,
            model=llm_model,
            temperature=temperature,
            openai_api_key="lmstudio"  # LMStudio doesn't require a real API key
        )
        self.embeddings = OpenAIEmbeddings(
            model=embedding_model,
            openai_api_base=api_base,
            openai_api_key="lmstudio"  # LMStudio doesn't require a real API key
        )

    def ask(self, question):
        return self.llm.invoke(question)