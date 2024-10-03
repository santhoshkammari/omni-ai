import streamlit as st
from omni_ai import OmniAIChat
from typing import List, Tuple, Generator

st.set_page_config(layout="wide")


class OmniAIChatApp:
    AVAILABLE_MODELS: List[str] = [
        'microsoft/Phi-3.5-mini-instruct',
        'Qwen/Qwen2.5-72B-Instruct',
        'meta-llama/Meta-Llama-3.1-70B-Instruct',
        'NousResearch/Hermes-3-Llama-3.1-8B',
        'mistralai/Mistral-Nemo-Instruct-2407',
        'meta-llama/Llama-3.2-11B-Vision-Instruct',
        'CohereForAI/c4ai-command-r-plus-08-2024',

    ]

    def __init__(self):
        self.chat_col, self.artifact_col = st.columns([1, 1])
        self.initialize_session_state()

    def initialize_session_state(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "artifacts" not in st.session_state:
            st.session_state.artifacts = []
        if "chatbot" not in st.session_state:
            st.session_state.chatbot = None
        if "selected_model" not in st.session_state:
            st.session_state.selected_model = None

    @staticmethod
    def create_chat_instance(model: str) -> OmniAIChat:
        return OmniAIChat(model=model)

    @staticmethod
    def get_chat_response(chatbot: OmniAIChat, query: str, web_search: bool = False) -> Generator:
        return chatbot.generator(query, web_search=web_search)

    @staticmethod
    def data_stream(generator: Generator) -> Generator[Tuple[str, bool], None, None]:
        flag = True
        for chunk in generator:
            if chunk == 'artifact':
                flag = not flag
            yield chunk, flag

    @staticmethod
    def update_chat_col(generator: Generator, chat_placeholder: st.empty, artifact_placeholder: st.empty) -> Tuple[str, str]:
        chat_content, artifact_content = "", ""
        for item, flag in generator:
            if flag:
                chat_content += item
                chat_placeholder.markdown(chat_content)
            else:
                artifact_content += item
                artifact_placeholder.markdown(artifact_content)
        return chat_content, artifact_content

    def render_chat_interface(self):
        with self.chat_col:
            st.title("OmniAI Chat Interface")
            selected_model = st.selectbox("Select a model", self.AVAILABLE_MODELS)

            if st.session_state.chatbot is None or st.session_state.selected_model != selected_model:
                st.session_state.chatbot = self.create_chat_instance(selected_model)
                st.session_state.selected_model = selected_model

            self.display_chat_messages()
            self.handle_user_input()

    def display_chat_messages(self):
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def handle_user_input(self):
        query = st.chat_input("Ask your question here:")
        if query:
            st.session_state.messages.append({"role": "user", "content": query})
            with st.chat_message("user"):
                st.markdown(query)

            with st.chat_message("assistant"):
                self.process_ai_response(query)

    def process_ai_response(self, query: str):
        chat_placeholder = st.empty()
        artifact_placeholder = self.artifact_col.empty()

        response_generator = self.get_chat_response(st.session_state.chatbot, query)
        chat_content, artifact_content = self.update_chat_col(
            self.data_stream(response_generator),
            chat_placeholder,
            artifact_placeholder
        )

        st.session_state.messages.append({"role": "assistant", "content": chat_content})
        if artifact_content:
            st.session_state.artifacts.append(artifact_content)

    def run(self):
        self.render_chat_interface()

def main():
    app = OmniAIChatApp()
    app.run()

if __name__ == "__main__":
    main()