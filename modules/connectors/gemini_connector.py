from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings

class GeminiConnector:
    def __init__(self, api_key, llm_model, embedding_model, temperature):
        self.llm = ChatGoogleGenerativeAI(api_key=api_key, model=llm_model, temperature=temperature)
        self.embeddings = GoogleGenerativeAIEmbeddings(model=embedding_model, google_api_key=api_key)

    def ask(self, question):
        return self.llm.invoke(question)