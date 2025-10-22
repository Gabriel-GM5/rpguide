from langchain_google_genai import ChatGoogleGenerativeAI

class GeminiConnector:
    def __init__(self, api_key, model, temperature):
        self.llm = ChatGoogleGenerativeAI(api_key=api_key, model=model, temperature=temperature)

    def ask(self, question):
        return self.llm.invoke(question)