from typing import Any, Iterator, List, Optional

import anthropic as anthropic_sdk
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatGeneration, ChatResult


class _AnthropicChatModel(BaseChatModel):
    """Minimal BaseChatModel wrapper around the Anthropic Messages API."""

    api_key: str
    model: str
    temperature: float = 0.0

    @property
    def _llm_type(self) -> str:
        return "anthropic"

    def _generate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None, **kwargs: Any) -> ChatResult:
        client = anthropic_sdk.Anthropic(api_key=self.api_key)

        system_prompt: Optional[str] = None
        human_messages: List[dict] = []

        for msg in messages:
            if isinstance(msg, SystemMessage):
                system_prompt = str(msg.content)
            elif isinstance(msg, HumanMessage):
                human_messages.append({"role": "user", "content": str(msg.content)})
            elif isinstance(msg, AIMessage):
                human_messages.append({"role": "assistant", "content": str(msg.content)})
            else:
                human_messages.append({"role": "user", "content": str(msg.content)})

        create_kwargs: dict = {
            "model": self.model,
            "max_tokens": 4096,
            "temperature": self.temperature,
            "messages": human_messages,
        }
        if system_prompt:
            create_kwargs["system"] = system_prompt
        if stop:
            create_kwargs["stop_sequences"] = stop

        response = client.messages.create(**create_kwargs)
        text = response.content[0].text if response.content else ""
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=text))])


class AnthropicConnector:
    """Anthropic connector.

    Note: Anthropic does not provide an embeddings API.
    Setting ``embeddings`` to ``None`` disables RAG; the ConnectorManager
    falls back to SimpleLLMAgent when no embeddings are available.
    """

    def __init__(self, api_key: str, llm_model: str, temperature: float):
        self.llm = _AnthropicChatModel(
            api_key=api_key,
            model=llm_model,
            temperature=temperature,
        )
        self.embeddings = None

    def ask(self, question: str):
        return self.llm.invoke(question)
