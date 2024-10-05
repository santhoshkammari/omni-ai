from typing import Any, Dict, List, Optional, Union, Tuple

import aiohttp
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, ChatMessage, HumanMessage, SystemMessage, AIMessageChunk
from langchain_core.outputs import ChatGeneration, ChatGenerationChunk, ChatResult
import requests
import json
import asyncio

class CustomChatOllama(BaseChatModel):
    model: str = "qwen2.5:7b-instruct"
    base_url: str = "http://192.168.162.49:8888"
    temperature: float = 0.0
    num_predict:int =8000

    @property
    def _llm_type(self) -> str:
        return "custom-ollama-chat"

    def _convert_messages_to_prompt(self, messages: List[BaseMessage]) -> List[Dict[str, str]]:
        updated_messages = []
        for message in messages:
            if isinstance(message, SystemMessage):
                updated_messages.append({"role": "system", "content": message.content})
            elif isinstance(message, HumanMessage):
                updated_messages.append({"role": "user", "content": message.content})
            elif isinstance(message, AIMessage):
                updated_messages.append({"role": "assistant", "content": message.content})
            elif isinstance(message, ChatMessage):
                updated_messages.append({"role": message.role.lower(), "content": message.content})
        return updated_messages

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        updated_messages = self._convert_messages_to_prompt(messages)
        response = requests.post(
            f"{self.base_url}/chat",
            json={
                "messages": updated_messages,
                "model": self.model,
                "temperature": self.temperature,
                "num_predict": kwargs.get("num_predict", 2048)
            },
            stream=True
        )

        full_response = ""
        for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
            if chunk:
                full_response += chunk
                if run_manager:
                    run_manager.on_llm_new_token(chunk)

        chat_generation = ChatGeneration(
            message=AIMessage(content=full_response),
            generation_info={"finish_reason": "stop"}
        )
        return ChatResult(generations=[chat_generation])

    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Union[ChatGenerationChunk, List[ChatGenerationChunk]]:
        updated_messages = self._convert_messages_to_prompt(messages)
        response = requests.post(
            f"{self.base_url}/chat",
            json={
                "messages": updated_messages,
                "model": self.model,
                "temperature": self.temperature,
                "num_predict": kwargs.get("num_predict", 2048)
            },
            stream=True
        )

        for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
            if chunk:
                chat_chunk = ChatGenerationChunk(
                    message=AIMessageChunk(content=chunk),
                    generation_info=None
                )
                if run_manager:
                    run_manager.on_llm_new_token(chunk)
                yield chat_chunk

    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        updated_messages = self._convert_messages_to_prompt(messages)
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/chat",
                json={
                    "messages": updated_messages,
                    "model": self.model,
                    "temperature": self.temperature,
                    "num_predict": kwargs.get("num_predict", 2048)
                }
            ) as response:
                full_response = await response.text()

        chat_generation = ChatGeneration(
            message=AIMessage(content=full_response),
            generation_info={"finish_reason": "stop"}
        )
        return ChatResult(generations=[chat_generation])

    async def _abatch(
        self,
        messages: List[List[BaseMessage]],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> List[ChatResult]:
        updated_messages_list = [self._convert_messages_to_prompt(msg) for msg in messages]
        async with aiohttp.ClientSession() as session:
            tasks = [
                session.post(
                    f"{self.base_url}/chat",
                    json={
                        "messages": updated_messages,
                        "model": self.model,
                        "temperature": self.temperature,
                        "num_predict": kwargs.get("num_predict", 2048)
                    }
                )
                for updated_messages in updated_messages_list
            ]
            responses = await asyncio.gather(*tasks)
            results = []
            for response in responses:
                full_response = await response.text()
                chat_generation = ChatGeneration(
                    message=AIMessage(content=full_response),
                    generation_info={"finish_reason": "stop"}
                )
                results.append(ChatResult(generations=[chat_generation]))
        return results

    def pstream(self,messages):
        for x in self.stream(messages):
            print(x.content,end = "", flush=True)

