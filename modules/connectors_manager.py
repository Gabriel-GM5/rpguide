class ConnectorManager:
    def __init__(self, config):
        self.config = config
        self.connector = self.getConnector()

    def getConnector(self):
        if self.config.LLM_TYPE == "gemini":
            from modules.connectors.gemini_connector import GeminiConnector
            return GeminiConnector(self.config.LLM_AI_API_KEY, self.config.LLM_AI_MODEL, self.config.LLM_AI_TEMPERATURE)
        else:
            raise ValueError(f"Unsupported LLM type: {self.config.LLM_TYPE}")

    def call(self, question):
        response = self.connector.ask(question).content
        return response
