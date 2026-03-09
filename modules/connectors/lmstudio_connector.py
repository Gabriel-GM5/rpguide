from langchain_community.chat_models import ChatLMStudio
from langchain_community.embeddings import LMStudioEmbeddings

class LMStudioConnector:
    def __init__(self, api_base, llm_model, embedding_model, temperature):
        self.llm = ChatLMStudio(base_url=api_base, model=llm_model, temperature=temperature)
        self.embeddings = LMStudioEmbeddings(model=embedding_model, base_url=api_base)

    def ask(self, question):
        return self.llm.invoke(question)