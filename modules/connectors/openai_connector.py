from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings

class OpenAIConnector:
    def __init__(self, api_base, llm_model, embedding_model, temperature):
        # Handle both OpenAI and LMStudio API endpoints
        self.llm = ChatOpenAI(
            openai_api_base=api_base,
            model=llm_model,
            temperature=temperature,
            # For LMStudio, we don't need a real API key
            # For OpenAI, the API key will be provided in the environment
            openai_api_key="lmstudio" if "lmstudio" in api_base.lower() else None
        )
        self.embeddings = OpenAIEmbeddings(
            model=embedding_model,
            openai_api_base=api_base,
            # For LMStudio, we don't need a real API key
            # For OpenAI, the API key will be provided in the environment
            openai_api_key="lmstudio" if "lmstudio" in api_base.lower() else None
        )

    def ask(self, question):
        return self.llm.invoke(question)