from typing import Generator, Optional
import time
import streamlit as st
from aichatlite.utils.schema import ChatMessage


class ChatService:
    def __init__(self, model_service):
        self.model_service = model_service

    def add_message(self, role: str, content: str):
        if "messages" not in st.session_state:
            st.session_state.messages = []

        message = ChatMessage(
            role=role,
            content=content,
            timestamp=time.time()
        )
        st.session_state.messages.append(message)

        if len(st.session_state.messages) > st.session_state.config.CHAT_HISTORY_LIMIT:
            st.session_state.messages = st.session_state.messages[
                                        -st.session_state.config.CHAT_HISTORY_LIMIT:
                                        ]

    def handle_chat(self, prompt: str) -> Generator:
        self.add_message("user", prompt)

        system_prompt = st.session_state.config.SYSTEM_PROMPTS[
            st.session_state.agent_type
        ]

        response_generator = self.model_service.generate_response(
            prompt,
            system_prompt,
            st.session_state.model_params
        )

        return self._process_response(response_generator)

    def _process_response(self, generator: Generator) -> Generator:
        chat_content = ""
        artifact_content = ""
        in_artifact = False

        for chunk in generator:
            if "<artifact_area>" in chunk:
                in_artifact = True
                chunk = chunk.replace("<artifact_area>", "")
            elif "</artifact_area>" in chunk:
                in_artifact = False
                chunk = chunk.replace("</artifact_area>", "")

            if in_artifact:
                artifact_content += chunk
                st.session_state.artifact_content = artifact_content
            else:
                chat_content += chunk
                st.session_state.chat_content = chat_content

            yield chunk

        if chat_content:
            self.add_message("assistant", chat_content)
