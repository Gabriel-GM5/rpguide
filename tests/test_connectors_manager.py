import os
import sys
from unittest.mock import patch, MagicMock

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

from modules.connectors_manager import (
    PromptAnalyzerAgent,
    RAGAgent,
    SimpleLLMAgent,
    ConnectorManager,
    RoutingDecision,
    _CONNECTOR_REGISTRY,
)


def test_routing_decision_enum():
    """RoutingDecision values compare equal to their string counterparts."""
    assert RoutingDecision.RAG == "rag"
    assert RoutingDecision.SIMPLE == "simple"
    assert RoutingDecision.RAG != RoutingDecision.SIMPLE


def test_connector_registry_keys():
    """All expected provider keys are present in _CONNECTOR_REGISTRY."""
    expected = {"gemini", "openai", "lmstudio", "ollama", "anthropic"}
    assert expected == set(_CONNECTOR_REGISTRY.keys())


def test_prompt_analyzer_agent_init():
    """Test PromptAnalyzerAgent initialization"""
    mock_llm = MagicMock()

    agent = PromptAnalyzerAgent(
        llm=mock_llm,
        prompt_template="test template",
        persona="Test Persona",
        debug=True,
    )

    assert agent.llm == mock_llm
    assert agent.prompt_template == "test template"
    assert agent.persona == "Test Persona"
    assert agent.debug is True


def test_prompt_analyzer_rag_keywords_immutable():
    """RAG_KEYWORDS must be a frozenset."""
    assert isinstance(PromptAnalyzerAgent.RAG_KEYWORDS, frozenset)


def test_prompt_analyzer_agent_decide():
    """Test PromptAnalyzerAgent decide method returns RoutingDecision."""
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = "rag"

    agent = PromptAnalyzerAgent(
        llm=mock_llm,
        prompt_template="test template",
        persona="Test Persona",
        debug=False,
    )

    result = agent.decide("test question")
    assert result == RoutingDecision.RAG

    mock_llm.invoke.return_value = "simple"
    result = agent.decide("test question")
    assert result == RoutingDecision.SIMPLE

    # Empty question always returns SIMPLE without calling LLM
    mock_llm.invoke.reset_mock()
    result = agent.decide("")
    assert result == RoutingDecision.SIMPLE
    mock_llm.invoke.assert_not_called()


def test_prompt_analyzer_heuristic_decide():
    """_heuristic_decide returns correct decisions without LLM involvement."""
    mock_llm = MagicMock()
    agent = PromptAnalyzerAgent(llm=mock_llm, prompt_template="", persona="Test", debug=False)

    assert agent._heuristic_decide("find the document") == RoutingDecision.RAG
    assert agent._heuristic_decide("where is it") == RoutingDecision.RAG
    assert agent._heuristic_decide("summarize this") == RoutingDecision.RAG
    assert agent._heuristic_decide("a" * 201) == RoutingDecision.RAG
    assert agent._heuristic_decide("hello there") == RoutingDecision.SIMPLE
    assert agent._heuristic_decide("tell me a joke") == RoutingDecision.SIMPLE


def test_prompt_analyzer_agent_heuristic_fallback():
    """When the LLM raises, decide falls back to _heuristic_decide."""
    mock_llm = MagicMock()
    mock_llm.invoke.side_effect = Exception("LLM error")

    agent = PromptAnalyzerAgent(
        llm=mock_llm,
        prompt_template="test template",
        persona="Test Persona",
        debug=False,
    )

    rag_questions = [
        "find the document",
        "where is the information",
        "which file contains",
        "reference to the source",
    ]
    for question in rag_questions:
        assert agent.decide(question) == RoutingDecision.RAG, f"Failed for: {question}"

    long_question = "This is a very long question that should trigger RAG because it's over 200 characters and contains multiple words to test the system properly with detailed analysis."
    assert agent.decide(long_question) == RoutingDecision.RAG

    assert agent.decide("summarize this document") == RoutingDecision.RAG

    simple_questions = ["What is your name?", "How are you?", "Tell me a joke", "Hello there"]
    for question in simple_questions:
        assert agent.decide(question) == RoutingDecision.SIMPLE, f"Failed for: {question}"


def test_rag_agent_init():
    """Test RAGAgent initialization"""
    mock_document_chain = MagicMock()
    mock_retriever = MagicMock()

    agent = RAGAgent(
        document_chain=mock_document_chain,
        retriever=mock_retriever,
        debug=True,
        config=None,
    )

    assert agent.document_chain == mock_document_chain
    assert agent.retriever == mock_retriever
    assert agent.debug is True


def test_rag_agent_answer():
    """Test RAGAgent answer method"""
    mock_document_chain = MagicMock()
    mock_retriever = MagicMock()

    agent = RAGAgent(
        document_chain=mock_document_chain,
        retriever=mock_retriever,
        debug=False,
        config=None,
    )

    mock_retriever.invoke.return_value = ["context1", "context2"]
    mock_document_chain.invoke.return_value = "test response"

    result = agent.answer("test question")
    assert result == "test response"

    # No retriever → localised fallback message
    agent_no_retriever = RAGAgent(
        document_chain=mock_document_chain,
        retriever=None,
        debug=False,
        config=MagicMock(texts={"rag.no.knowledge.base": "No knowledge base available"}),
    )
    result = agent_no_retriever.answer("test question")
    assert result == "No knowledge base available"


def test_simple_llm_agent_init():
    """Test SimpleLLMAgent initialization"""
    mock_document_chain = MagicMock()

    agent = SimpleLLMAgent(document_chain=mock_document_chain, debug=True)

    assert agent.document_chain == mock_document_chain
    assert agent.debug is True


def test_simple_llm_agent_answer():
    """Test SimpleLLMAgent answer method"""
    mock_document_chain = MagicMock()

    agent = SimpleLLMAgent(document_chain=mock_document_chain, debug=False)

    mock_document_chain.invoke.return_value = "simple response"
    result = agent.answer("test question")
    assert result == "simple response"
    mock_document_chain.invoke.assert_called_once_with({"input": "test question", "context": ""})


def _make_connector_manager(mock_config, mock_connector):
    """Helper: build a ConnectorManager with fully mocked internals."""
    with patch("modules.connectors_manager.ConnectorManager.get_connector", return_value=mock_connector), \
         patch("modules.prompts_manager.PromptsManager") as mock_prompts_mgr, \
         patch("modules.docs_manager.DocsManager") as mock_docs_mgr, \
         patch("modules.connectors_manager.RecursiveCharacterTextSplitter") as mock_splitter, \
         patch("modules.connectors_manager.FAISS") as mock_faiss:

        mock_prompts_instance = MagicMock()
        mock_prompts_instance.get_prompts.return_value = "test_prompts"
        mock_prompts_instance.get_analyzer_prompt.return_value = ""
        mock_prompts_mgr.return_value = mock_prompts_instance

        mock_docs_instance = MagicMock()
        mock_docs_instance.getDocs.return_value = ["doc1"]
        mock_docs_mgr.return_value = mock_docs_instance

        mock_splitter_instance = MagicMock()
        mock_splitter.return_value = mock_splitter_instance
        mock_splitter_instance.split_documents.return_value = ["chunk1"]

        mock_vs = MagicMock()
        mock_faiss.from_documents.return_value = mock_vs

        return ConnectorManager(mock_config)


def test_connector_manager_init():
    """Test ConnectorManager initialization"""
    mock_config = MagicMock()
    mock_config.LLM_TYPE = "gemini"
    mock_config.AI_PERSONA = "Test Persona"
    mock_config.DEBUG = False

    mock_connector = MagicMock()
    mock_connector.embeddings = MagicMock()

    cm = _make_connector_manager(mock_config, mock_connector)

    assert hasattr(cm, "prompt_analyzer")
    assert hasattr(cm, "rag_agent")
    assert hasattr(cm, "simple_agent")
    assert hasattr(cm, "retriever")


def test_connector_manager_build_retriever_no_docs():
    """_build_retriever returns None when docs list is empty."""
    mock_config = MagicMock()
    mock_config.AI_PERSONA = "Test"
    mock_config.DEBUG = False

    mock_connector = MagicMock()
    mock_connector.embeddings = MagicMock()

    cm = ConnectorManager.__new__(ConnectorManager)
    cm.config = mock_config
    cm.connector = mock_connector

    with patch("modules.connectors_manager.FAISS") as mock_faiss:
        result = cm._build_retriever([])
        mock_faiss.from_documents.assert_not_called()
        assert result is None


def test_connector_manager_build_retriever_no_embeddings():
    """_build_retriever returns None when connector has no embeddings."""
    mock_config = MagicMock()
    mock_connector = MagicMock()
    mock_connector.embeddings = None

    cm = ConnectorManager.__new__(ConnectorManager)
    cm.config = mock_config
    cm.connector = mock_connector

    with patch("modules.connectors_manager.FAISS") as mock_faiss:
        result = cm._build_retriever(["doc1"])
        mock_faiss.from_documents.assert_not_called()
        assert result is None


def test_connector_manager_get_connector_unknown_type():
    """get_connector raises ValueError for unknown LLM_TYPE."""
    mock_config = MagicMock()
    mock_config.LLM_TYPE = "unknown_provider"

    cm = ConnectorManager.__new__(ConnectorManager)
    cm.config = mock_config

    try:
        cm.get_connector()
        assert False, "Should have raised ValueError"
    except ValueError as exc:
        assert "unknown_provider" in str(exc)


def test_connector_manager_anthropic_no_rag():
    """When connector.embeddings is None (Anthropic), retriever must be None."""
    mock_config = MagicMock()
    mock_config.LLM_TYPE = "anthropic"
    mock_config.AI_PERSONA = "Test"
    mock_config.DEBUG = False

    mock_connector = MagicMock()
    mock_connector.embeddings = None

    with patch("modules.connectors_manager.ConnectorManager.get_connector", return_value=mock_connector), \
         patch("modules.prompts_manager.PromptsManager") as mock_prompts_mgr, \
         patch("modules.docs_manager.DocsManager") as mock_docs_mgr, \
         patch("modules.connectors_manager.FAISS") as mock_faiss:

        mock_prompts_instance = MagicMock()
        mock_prompts_instance.get_prompts.return_value = "test_prompts"
        mock_prompts_instance.get_analyzer_prompt.return_value = ""
        mock_prompts_mgr.return_value = mock_prompts_instance

        mock_docs_instance = MagicMock()
        mock_docs_instance.getDocs.return_value = ["doc1"]
        mock_docs_mgr.return_value = mock_docs_instance

        cm = ConnectorManager(mock_config)

    assert cm.retriever is None
    mock_faiss.from_documents.assert_not_called()


def test_connector_manager_supported_types():
    """Verify all supported LLM_TYPE values map to the expected connector class."""
    cases = [
        ("gemini", "modules.connectors.gemini_connector", "GeminiConnector"),
        ("openai", "modules.connectors.openai_connector", "OpenAIConnector"),
        ("lmstudio", "modules.connectors.lmstudio_connector", "LMStudioConnector"),
        ("ollama", "modules.connectors.ollama_connector", "OllamaConnector"),
        ("anthropic", "modules.connectors.anthropic_connector", "AnthropicConnector"),
    ]
    for llm_type, module_path, class_name in cases:
        mock_config = MagicMock()
        mock_config.LLM_TYPE = llm_type

        cm = ConnectorManager.__new__(ConnectorManager)
        cm.config = mock_config

        with patch(f"{module_path}.{class_name}") as mock_cls:
            mock_cls.return_value = MagicMock(embeddings=MagicMock())
            cm.get_connector()
            assert mock_cls.called, f"{class_name} was not instantiated for LLM_TYPE={llm_type}"


def test_connector_manager_call_routes_to_rag():
    """call() delegates to RAGAgent when analyzer returns RAG."""
    mock_config = MagicMock()
    mock_config.AI_PERSONA = "Test"
    mock_config.DEBUG = False

    mock_connector = MagicMock()
    mock_connector.embeddings = MagicMock()

    cm = _make_connector_manager(mock_config, mock_connector)
    cm.prompt_analyzer = MagicMock()
    cm.prompt_analyzer.decide.return_value = RoutingDecision.RAG
    cm.rag_agent = MagicMock()
    cm.rag_agent.answer.return_value = "rag answer"
    cm.simple_agent = MagicMock()

    result = cm.call("find me a document")
    assert result == "rag answer"
    cm.rag_agent.answer.assert_called_once_with("find me a document")
    cm.simple_agent.answer.assert_not_called()


def test_connector_manager_call_routes_to_simple():
    """call() delegates to SimpleLLMAgent when analyzer returns SIMPLE."""
    mock_config = MagicMock()
    mock_config.AI_PERSONA = "Test"
    mock_config.DEBUG = False

    mock_connector = MagicMock()
    mock_connector.embeddings = MagicMock()

    cm = _make_connector_manager(mock_config, mock_connector)
    cm.prompt_analyzer = MagicMock()
    cm.prompt_analyzer.decide.return_value = RoutingDecision.SIMPLE
    cm.rag_agent = MagicMock()
    cm.simple_agent = MagicMock()
    cm.simple_agent.answer.return_value = "simple answer"

    result = cm.call("hello there")
    assert result == "simple answer"
    cm.simple_agent.answer.assert_called_once_with("hello there")
    cm.rag_agent.answer.assert_not_called()
