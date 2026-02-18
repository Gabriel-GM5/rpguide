import os
import sys
from unittest.mock import patch, MagicMock

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

from modules.connectors_manager import PromptAnalyzerAgent


def test_prompt_analyzer_agent_comprehensive():
    """Comprehensive test for PromptAnalyzerAgent decision making"""
    
    # Mock LLM that returns different values based on question
    mock_llm = MagicMock()
    
    # Test cases: (question, expected_result, llm_response)
    test_cases = [
        # Questions that should be classified as RAG due to keywords
        ("Find the document about AI", "rag", "rag"),
        ("Where is the information located?", "rag", "rag"), 
        ("Which file contains the data?", "rag", "rag"),
        ("Reference the source material", "rag", "rag"),
        ("Cite the document", "rag", "rag"),
        ("Summarize the PDF", "rag", "rag"),
        ("Give me a detailed analysis of this", "rag", "rag"),
        ("Explain how to use this documentation", "rag", "rag"),
        
        # Questions that should be classified as simple
        ("What is your name?", "simple", "simple"),
        ("How are you today?", "simple", "simple"),
        ("Tell me a joke", "simple", "simple"),
        ("Hello there!", "simple", "simple"),
        ("What time is it?", "simple", "simple"),
        
        # Edge cases with long questions (should trigger RAG)
        ("Can you explain in detail the complex algorithm that was discussed in the meeting about AI and machine learning, including the mathematical formulas and implementation details that were presented in the technical document?", "rag", "rag"),
        
        # Questions with mixed content
        ("What is the weather today and where can I find information about it?", "simple", "simple"),  # Simple question despite mentioning info
    ]
    
    for question, expected, llm_response in test_cases:
        # Mock LLM to return specific response
        mock_llm.invoke.return_value = llm_response
        
        agent = PromptAnalyzerAgent(
            llm=mock_llm,
            prompt_template="test template",
            persona="Test Persona",
            debug=False
        )
        
        result = agent.decide(question)
        assert result == expected, f"Failed for question: '{question}' - Expected: {expected}, Got: {result}"


def test_prompt_analyzer_agent_with_exceptions():
    """Test PromptAnalyzerAgent behavior when LLM fails"""
    
    mock_llm = MagicMock()
    # Simulate LLM failure (exception)
    mock_llm.invoke.side_effect = Exception("LLM connection error")
    
    agent = PromptAnalyzerAgent(
        llm=mock_llm,
        prompt_template="test template",
        persona="Test Persona",
        debug=False
    )
    
    # These should fall back to heuristic detection
    rag_questions = [
        "find the document",
        "where is the information",
        "reference to the source"
    ]
    
    simple_questions = [
        "what is your name?",
        "how are you?",
        "tell me a joke"
    ]
    
    # Test RAG keyword detection (should still return rag)
    for question in rag_questions:
        result = agent.decide(question)
        assert result == "rag", f"Failed for RAG question: {question}"
    
    # Test simple questions
    for question in simple_questions:
        result = agent.decide(question)
        assert result == "simple", f"Failed for simple question: {question}"


def test_prompt_analyzer_agent_edge_cases():
    """Test edge cases for PromptAnalyzerAgent"""
    
    mock_llm = MagicMock()
    mock_llm.invoke.side_effect = Exception("LLM error")
    
    agent = PromptAnalyzerAgent(
        llm=mock_llm,
        prompt_template="test template",
        persona="Test Persona",
        debug=False
    )
    
    # Empty question
    result = agent.decide("")
    assert result == "simple"
    
    # None question (should be handled gracefully)
    result = agent.decide(None)
    assert result == "simple"  # Should default to simple
    
    # Very long question with no keywords
    long_question = "a" * 300  # Long question without RAG keywords
    result = agent.decide(long_question)
    assert result == "rag"  # Should be classified as rag due to length
    
    # Question with RAG keywords but at end
    question_with_rag_keywords = "How do I use this tool and find the documentation for it"
    result = agent.decide(question_with_rag_keywords)
    assert result == "rag"  # Should detect 'documentation' keyword


def test_prompt_analyzer_agent_heuristic_rules():
    """Test specific heuristic rules in PromptAnalyzerAgent"""
    
    mock_llm = MagicMock()
    mock_llm.invoke.side_effect = Exception("LLM error")
    
    agent = PromptAnalyzerAgent(
        llm=mock_llm,
        prompt_template="test template",
        persona="Test Persona",
        debug=False
    )
    
    # Test the RAG keyword detection
    assert "find" in agent.RAG_KEYWORDS
    assert "search" in agent.RAG_KEYWORDS
    assert "where" in agent.RAG_KEYWORDS
    assert "which" in agent.RAG_KEYWORDS
    assert "reference" in agent.RAG_KEYWORDS
    assert "cite" in agent.RAG_KEYWORDS
    assert "document" in agent.RAG_KEYWORDS
    assert "docs" in agent.RAG_KEYWORDS
    assert "source" in agent.RAG_KEYWORDS
    assert "file" in agent.RAG_KEYWORDS
    assert "pdf" in agent.RAG_KEYWORDS
    
    # Test that the keywords work as expected
    test_questions = [
        ("Find information about AI", "rag"),
        ("Search for documents", "rag"),
        ("Where can I find the manual?", "rag"),
        ("Which file has the data?", "rag"),
        ("Reference the source document", "rag"),
        ("Cite the PDF file", "rag"),
        ("What is your name?", "simple"),
    ]
    
    for question, expected in test_questions:
        result = agent.decide(question)
        assert result == expected, f"Failed for: {question}"