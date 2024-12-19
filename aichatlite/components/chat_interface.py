from typing import Callable
import streamlit as st

from aichatlite.utils.state import StateManager


class ChatInterface:
    def __init__(self, on_submit: Callable[[str], None]):
        self.on_submit = on_submit
        self.state_manager = StateManager()

    def render(self):
        with st.container():
            self._render_messages()
            self._render_input()

    def _render_messages(self):
        messages = self.state_manager.get_state("messages", [])
        for msg in messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    def _render_input(self):
        if prompt := st.chat_input("How can I help you today?"):
            self.state_manager.update_chat_state({
                "role": "user",
                "content": prompt
            })
            self.on_submit(prompt)