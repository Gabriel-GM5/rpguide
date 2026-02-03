from modules.prompts_manager import PromptsManager
from modules.docs_manager import DocsManager
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

class PromptAnalyzerAgent:
    RAG_KEYWORDS = {
        "find",
        "search",
        "where",
        "which",
        "reference",
        "cite",
        "document",
        "docs",
        "source",
        "file",
        "pdf",
    }

    def __init__(self, llm, prompt_template: str = None, persona: str = None, debug: bool = False):
        self.llm = llm
        self.debug = debug
        self.prompt_template = prompt_template
        self.persona = persona or "General purpose assistant"

    def decide(self, question: str) -> str:
        if not question:
            return "simple"

        prompt = self.prompt_template.replace("{QUESTION}", question).replace("{PERSONA}", self.persona)

        try:
            resp = self.llm.invoke(prompt)
            if resp is None:
                raise ValueError("empty response")
            r = str(resp).lower()
            if "rag" in r:
                if self.debug:
                    print("[DEBUG] Analyzer chose: rag")
                return "rag"
            if "simple" in r or "direct" in r or "llm" in r:
                if self.debug:
                    print("[DEBUG] Analyzer chose: simple")
                return "simple"
        except Exception:
            pass

        q = question.lower()
        for kw in self.RAG_KEYWORDS:
            if kw in q:
                if self.debug:
                    print("[DEBUG] Analyzer heuristic chose: rag")
                return "rag"
        if len(q) > 200 or "summarize" in q or "detailed" in q:
            if self.debug:
                print("[DEBUG] Analyzer heuristic chose: rag")
            return "rag"
        if self.debug:
            print("[DEBUG] Analyzer heuristic chose: simple")
        return "simple"


class RAGAgent:
    def __init__(self, document_chain, retriever, debug: bool = False, config=None):
        self.document_chain = document_chain
        self.retriever = retriever
        self.debug = debug
        self.config = config

    def answer(self, question: str):
        if self.debug:
            print("[DEBUG] Using agent: RAGAgent")
        
        if self.retriever is None:
            if self.debug:
                print("[DEBUG] Warning: No documents loaded, RAG cannot proceed")
            
            if self.config and hasattr(self.config, 'texts'):
                return self.config.texts.get('rag.no.knowledge.base', "ERROR")
            return "ERROR"
        
        context = self.retriever.invoke(question)
        return self.document_chain.invoke({"input": question, "context": context})


class SimpleLLMAgent:
    def __init__(self, document_chain, debug: bool = False):
        self.document_chain = document_chain
        self.debug = debug

    def answer(self, question: str):
        if self.debug:
            print("[DEBUG] Using agent: SimpleLLMAgent")
        return self.document_chain.invoke({"input": question, "context": ""})

class ConnectorManager:
    def __init__(self, config):
        self.config = config
        self.connector = self.getConnector()
        promptsMgr = PromptsManager(config)
        self.prompts = promptsMgr.get_prompts()
        self.document_chain = create_stuff_documents_chain(self.connector.llm, self.prompts)
        docsMgr = DocsManager(config)
        docs = docsMgr.getDocs()
        
        self.retriever = None
        if docs:
            splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
            chunks = splitter.split_documents(docs)
            vectorStore = FAISS.from_documents(chunks, self.connector.embeddings)
            self.retriever = vectorStore.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.3, "k": 4})
        
        analyzer_prompt = promptsMgr.get_analyzer_prompt()

        self.prompt_analyzer = PromptAnalyzerAgent(self.connector.llm, analyzer_prompt, persona=self.config.AI_PERSONA, debug=self.config.DEBUG)
        self.rag_agent = RAGAgent(self.document_chain, self.retriever, debug=self.config.DEBUG, config=self.config)
        self.simple_agent = SimpleLLMAgent(self.document_chain, debug=self.config.DEBUG)

    def getConnector(self):
        if self.config.LLM_TYPE == "gemini":
            from modules.connectors.gemini_connector import GeminiConnector
            return GeminiConnector(self.config.LLM_AI_API_KEY, self.config.LLM_AI_MODEL, self.config.EMBEDDINGS_AI_MODEL, self.config.LLM_AI_TEMPERATURE)
        else:
            raise ValueError(f"Unsupported LLM type: {self.config.LLM_TYPE}")

    def call(self, question):
        decision = self.prompt_analyzer.decide(question)
        if decision == "rag":
            return self.rag_agent.answer(question)
        else:
            return self.simple_agent.answer(question)
