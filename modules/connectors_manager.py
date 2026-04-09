from enum import Enum
from typing import Optional

from modules.prompts_manager import PromptsManager
from modules.docs_manager import DocsManager
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS


class RoutingDecision(str, Enum):
    RAG = "rag"
    SIMPLE = "simple"


def _connector_gemini(cfg):
    from modules.connectors.gemini_connector import GeminiConnector
    return GeminiConnector(cfg.LLM_AI_API_KEY, cfg.LLM_AI_MODEL, cfg.EMBEDDINGS_AI_MODEL, cfg.LLM_AI_TEMPERATURE)


def _connector_openai(cfg):
    from modules.connectors.openai_connector import OpenAIConnector
    return OpenAIConnector(cfg.LLM_AI_API_KEY, cfg.LLM_AI_BASE_URL, cfg.LLM_AI_MODEL, cfg.EMBEDDINGS_AI_MODEL, cfg.LLM_AI_TEMPERATURE)


def _connector_lmstudio(cfg):
    from modules.connectors.lmstudio_connector import LMStudioConnector
    return LMStudioConnector(cfg.LLM_AI_BASE_URL, cfg.LLM_AI_MODEL, cfg.EMBEDDINGS_AI_MODEL, cfg.LLM_AI_TEMPERATURE)


def _connector_ollama(cfg):
    from modules.connectors.ollama_connector import OllamaConnector
    return OllamaConnector(cfg.LLM_AI_BASE_URL, cfg.LLM_AI_MODEL, cfg.EMBEDDINGS_AI_MODEL, cfg.LLM_AI_TEMPERATURE)


def _connector_anthropic(cfg):
    from modules.connectors.anthropic_connector import AnthropicConnector
    return AnthropicConnector(cfg.LLM_AI_API_KEY, cfg.LLM_AI_MODEL, cfg.LLM_AI_TEMPERATURE)


_CONNECTOR_REGISTRY: dict = {
    "gemini": _connector_gemini,
    "openai": _connector_openai,
    "lmstudio": _connector_lmstudio,
    "ollama": _connector_ollama,
    "anthropic": _connector_anthropic,
}


class PromptAnalyzerAgent:
    RAG_KEYWORDS: frozenset = frozenset({
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
    })

    def __init__(self, llm, prompt_template: str = "", persona: str = None, debug: bool = False):
        self.llm = llm
        self.debug = debug
        self.prompt_template = prompt_template
        self.persona = persona or "General purpose assistant"

    def decide(self, question: str) -> RoutingDecision:
        if not question:
            return RoutingDecision.SIMPLE

        prompt = self.prompt_template.replace("{QUESTION}", question).replace("{PERSONA}", self.persona)

        try:
            resp = self.llm.invoke(prompt)
            if resp is None:
                raise ValueError("empty response")
            r = str(resp).lower()
            if "rag" in r:
                if self.debug:
                    print("[DEBUG] Analyzer chose: rag")
                return RoutingDecision.RAG
            if "simple" in r or "direct" in r or "llm" in r:
                if self.debug:
                    print("[DEBUG] Analyzer chose: simple")
                return RoutingDecision.SIMPLE
        except Exception:
            pass

        return self._heuristic_decide(question)

    def _heuristic_decide(self, question: str) -> RoutingDecision:
        q = question.lower()
        if any(kw in q for kw in self.RAG_KEYWORDS):
            if self.debug:
                print("[DEBUG] Analyzer heuristic chose: rag")
            return RoutingDecision.RAG
        if len(q) > 200 or "summarize" in q or "detailed" in q:
            if self.debug:
                print("[DEBUG] Analyzer heuristic chose: rag")
            return RoutingDecision.RAG
        if self.debug:
            print("[DEBUG] Analyzer heuristic chose: simple")
        return RoutingDecision.SIMPLE


class RAGAgent:
    def __init__(self, document_chain, retriever, debug: bool = False, config=None):
        self.document_chain = document_chain
        self.retriever = retriever
        self.debug = debug
        self.config = config

    def answer(self, question: str) -> str:
        if self.debug:
            print("[DEBUG] Using agent: RAGAgent")

        if self.retriever is None:
            if self.debug:
                print("[DEBUG] Warning: No documents loaded, RAG cannot proceed")
            if self.config and hasattr(self.config, "texts"):
                return self.config.texts.get("rag.no.knowledge.base", "ERROR")
            return "ERROR"

        context = self.retriever.invoke(question)
        return self.document_chain.invoke({"input": question, "context": context})


class SimpleLLMAgent:
    def __init__(self, document_chain, debug: bool = False):
        self.document_chain = document_chain
        self.debug = debug

    def answer(self, question: str) -> str:
        if self.debug:
            print("[DEBUG] Using agent: SimpleLLMAgent")
        return self.document_chain.invoke({"input": question, "context": ""})


class ConnectorManager:
    def __init__(self, config):
        self.config = config
        self.connector = self.get_connector()
        prompts_mgr = PromptsManager(config)
        self.prompts = prompts_mgr.get_prompts()
        self.document_chain = self._build_document_chain()
        docs = DocsManager(config).getDocs()
        self.retriever = self._build_retriever(docs)
        analyzer_prompt = prompts_mgr.get_analyzer_prompt()
        self.prompt_analyzer = PromptAnalyzerAgent(
            self.connector.llm, analyzer_prompt, persona=self.config.AI_PERSONA, debug=self.config.DEBUG
        )
        self.rag_agent = RAGAgent(self.document_chain, self.retriever, debug=self.config.DEBUG, config=self.config)
        self.simple_agent = SimpleLLMAgent(self.document_chain, debug=self.config.DEBUG)

    def _build_document_chain(self):
        return create_stuff_documents_chain(self.connector.llm, self.prompts)

    def _build_retriever(self, docs) -> Optional[object]:
        if not docs or self.connector.embeddings is None:
            return None
        splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
        chunks = splitter.split_documents(docs)
        vector_store = FAISS.from_documents(chunks, self.connector.embeddings)
        return vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"score_threshold": 0.3, "k": 4},
        )

    def get_connector(self):
        llm_type = self.config.LLM_TYPE
        factory = _CONNECTOR_REGISTRY.get(llm_type)
        if factory is None:
            raise ValueError(f"Unsupported LLM type: {llm_type}")
        return factory(self.config)

    def call(self, question: str) -> str:
        decision = self.prompt_analyzer.decide(question)
        if decision == RoutingDecision.RAG:
            return self.rag_agent.answer(question)
        return self.simple_agent.answer(question)
