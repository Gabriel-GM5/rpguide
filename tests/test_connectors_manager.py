import os
import sys
from unittest.mock import patch, MagicMock

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

from modules.connectors_manager import PromptAnalyzerAgent, RAGAgent, SimpleLLMAgent, ConnectorManager


def test_prompt_analyzer_agent_init():
    """Test PromptAnalyzerAgent initialization"""
    mock_llm = MagicMock()
    
    agent = PromptAnalyzerAgent(
        llm=mock_llm,
        prompt_template="test template",
        persona="Test Persona",
        debug=True
    )
    
    assert agent.llm == mock_llm
    assert agent.prompt_template == "test template"
    assert agent.persona == "Test Persona"
    assert agent.debug is True


def test_prompt_analyzer_agent_decide():
    """Test PromptAnalyzerAgent decide method"""
    # Mock LLM that returns 'rag'
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = "rag"
    
    agent = PromptAnalyzerAgent(
        llm=mock_llm,
        prompt_template="test template",
        persona="Test Persona",
        debug=False
    )
    
    result = agent.decide("test question")
    assert result == "rag"
    
    # Test with LLM that returns 'simple'
    mock_llm.invoke.return_value = "simple"
    result = agent.decide("test question")
    assert result == "simple"
    
    # Test with empty question
    result = agent.decide("")
    assert result == "simple"


def test_prompt_analyzer_agent_heuristic():
    """Test PromptAnalyzerAgent heuristic decision making"""
    mock_llm = MagicMock()
    mock_llm.invoke.side_effect = Exception("LLM error")  # Simulate LLM failure
    
    agent = PromptAnalyzerAgent(
        llm=mock_llm,
        prompt_template="test template",
        persona="Test Persona",
        debug=False
    )
    
    # Test RAG keywords detection
    rag_questions = [
        "find the document",
        "where is the information",
        "which file contains",
        "reference to the source"
    ]
    
    for question in rag_questions:
        result = agent.decide(question)
        assert result == "rag", f"Failed for question: {question}"
    
    # Test long question
    long_question = "This is a very long question that should trigger RAG because it's over 200 characters and contains multiple words to test the system properly with detailed analysis."
    result = agent.decide(long_question)
    assert result == "rag"
    
    # Test summarize keyword
    result = agent.decide("summarize this document")
    assert result == "rag"
    
    # Test simple questions
    simple_questions = [
        "What is your name?",
        "How are you?",
        "Tell me a joke",
        "Hello there"
    ]
    
    for question in simple_questions:
        result = agent.decide(question)
        assert result == "simple", f"Failed for question: {question}"


def test_rag_agent_init():
    """Test RAGAgent initialization"""
    mock_document_chain = MagicMock()
    mock_retriever = MagicMock()
    
    agent = RAGAgent(
        document_chain=mock_document_chain,
        retriever=mock_retriever,
        debug=True,
        config=None
    )
    
    assert agent.document_chain == mock_document_chain
    assert agent.retriever == mock_retriever
    assert agent.debug is True


def test_rag_agent_answer():
    """Test RAGAgent answer method"""
    mock_document_chain = MagicMock()
    mock_retriever = MagicMock()
    
    # Test with retriever available
    agent = RAGAgent(
        document_chain=mock_document_chain,
        retriever=mock_retriever,
        debug=False,
        config=None
    )
    
    mock_retriever.invoke.return_value = ["context1", "context2"]
    mock_document_chain.invoke.return_value = "test response"
    
    result = agent.answer("test question")
    assert result == "test response"
    
    # Test with no retriever (should return error)
    agent_no_retriever = RAGAgent(
        document_chain=mock_document_chain,
        retriever=None,
        debug=False,
        config=MagicMock(texts={'rag.no.knowledge.base': 'No knowledge base available'})
    )
    
    result = agent_no_retriever.answer("test question")
    assert result == "No knowledge base available"


def test_simple_llm_agent_init():
    """Test SimpleLLMAgent initialization"""
    mock_document_chain = MagicMock()
    
    agent = SimpleLLMAgent(
        document_chain=mock_document_chain,
        debug=True
    )
    
    assert agent.document_chain == mock_document_chain
    assert agent.debug is True


def test_simple_llm_agent_answer():
    """Test SimpleLLMAgent answer method"""
    mock_document_chain = MagicMock()
    
    agent = SimpleLLMAgent(
        document_chain=mock_document_chain,
        debug=False
    )
    
    mock_document_chain.invoke.return_value = "simple response"
    
    result = agent.answer("test question")
    assert result == "simple response"


def test_connector_manager_init():
    """Test ConnectorManager initialization"""
    # Mock config
    mock_config = MagicMock()
    mock_config.LLM_TYPE = "gemini"
    mock_config.AI_PERSONA = "Test Persona"
    mock_config.DEBUG = False
    
    # Mock the getConnector method to return a mock connector
    with patch('modules.connectors.gemini_connector.GeminiConnector') as mock_connector_class:
        mock_connector = MagicMock()
        mock_connector_class.return_value = mock_connector
        
        # Mock other components that will be called
        with patch('modules.prompts_manager.PromptsManager') as mock_prompts_mgr, \
             patch('modules.docs_manager.DocsManager') as mock_docs_mgr:
            
            mock_prompts_instance = MagicMock()
            mock_prompts_instance.get_prompts.return_value = "test_prompts"
            mock_prompts_mgr.return_value = mock_prompts_instance
            
            mock_docs_instance = MagicMock()
            mock_docs_instance.getDocs.return_value = ["doc1", "doc2"]
            mock_docs_mgr.return_value = mock_docs_instance
            
            # Mock text splitting and FAISS creation
            with patch('modules.connectors_manager.RecursiveCharacterTextSplitter') as mock_splitter, \
                 patch('modules.connectors_manager.FAISS') as mock_faiss:
                
                mock_splitter_instance = MagicMock()
                mock_splitter.return_value = mock_splitter_instance
                mock_splitter_instance.split_documents.return_value = ["chunk1", "chunk2"]
                
                mock_faiss.from_documents.return_value = "test_vector_store"
                mock_faiss.as_retriever.return_value = "test_retriever"
                
                # Create the ConnectorManager
                connector_manager = ConnectorManager(mock_config)
                
                # Verify it was initialized correctly
                assert hasattr(connector_manager, 'prompt_analyzer')
                assert hasattr(connector_manager, 'rag_agent')
                assert hasattr(connector_manager, 'simple_agent')
                assert hasattr(connector_manager, 'retriever')
                assert connector_manager.retriever == "test_retriever"