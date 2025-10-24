from modules.prompts_manager import PromptsManager
from modules.docs_manager import DocsManager
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

class ConnectorManager:
    def __init__(self, config):
        self.config = config
        self.connector = self.getConnector()
        promptsMgr = PromptsManager(config)
        self.prompts = promptsMgr.get_prompts()
        self.document_chain = create_stuff_documents_chain(self.connector.llm, self.prompts)
        docsMgr = DocsManager(config)
        docs = docsMgr.getDocs()
        splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
        chunks = splitter.split_documents(docs)
        vectorStore = FAISS.from_documents(chunks, self.connector.embeddings)
        self.retriever = vectorStore.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.3, "k": 4})

    def getConnector(self):
        if self.config.LLM_TYPE == "gemini":
            from modules.connectors.gemini_connector import GeminiConnector
            return GeminiConnector(self.config.LLM_AI_API_KEY, self.config.LLM_AI_MODEL, self.config.EMBEDDINGS_AI_MODEL, self.config.LLM_AI_TEMPERATURE)
        else:
            raise ValueError(f"Unsupported LLM type: {self.config.LLM_TYPE}")

    def call(self, question):
        context = self.retriever.invoke(question)
        answer = self.document_chain.invoke({"input": question, "context": context})
        return answer
