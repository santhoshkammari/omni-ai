from pathlib import Path

import PyPDF2
import streamlit as st
from omni_ai import OmniAIChat
from typing import List, Tuple, Generator
from datetime import datetime
import os
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import io

st.set_page_config(layout="wide", initial_sidebar_state='collapsed')


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
        self.sidebar = st.sidebar
        self.main_area = st.container()
        self.initialize_session_state()

    def initialize_session_state(self):
        if "chats" not in st.session_state:
            st.session_state.chats = {}
        if "current_chat_id" not in st.session_state:
            st.session_state.current_chat_id = None
        if "chatbot" not in st.session_state:
            st.session_state.chatbot = None
        if "selected_model" not in st.session_state:
            st.session_state.selected_model = None
        if "sidebar_state" not in st.session_state:
            st.session_state.sidebar_state = "expanded"
        if "uploaded_file" not in st.session_state:
            st.session_state.uploaded_file = None

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
    def update_chat_col(generator: Generator, chat_placeholder: st.empty, artifact_placeholder: st.empty) -> Tuple[
        str, str]:
        chat_content, artifact_content = "", ""
        for item, flag in generator:
            if flag:
                chat_content += item
                chat_content = chat_content.replace("<artifact_area>", "")
                chat_placeholder.markdown(chat_content)
            else:
                artifact_content += item
                if artifact_content[-2:] == "</": artifact_content = artifact_content[:-2]
                artifact_content = artifact_content.replace("artifact_area>", "")
                artifact_placeholder.code(artifact_content)
        return chat_content, artifact_content


    @staticmethod
    def perform_ocr(file_content: bytes, file_type: str) -> str:
        reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        num_pages = len(reader.pages)

        content = ""
        for page in range(num_pages):
            content += reader.pages[page].extract_text()

        return content

    def render_sidebar(self):
        st.sidebar.title("Chat History")
        if st.sidebar.button("New Chat"):
            self.create_new_chat()

        for chat_id, chat_info in st.session_state.chats.items():
            if st.sidebar.button(f"{chat_info['name']} - {chat_info['timestamp'][:10]}"):
                st.session_state.current_chat_id = chat_id

    def create_new_chat(self):
        chat_id = datetime.now().strftime("%Y%m%d%H%M%S")
        st.session_state.chats[chat_id] = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "name": f"Chat {len(st.session_state.chats) + 1}",
            "messages": []
        }
        st.session_state.current_chat_id = chat_id

    def render_chat_interface(self):
        with self.main_area:
            st.title("OmniAI Chat Interface")

            col1, col2 = st.columns([4, 3])
            with col1:
                selected_model = st.selectbox("Select a model", self.AVAILABLE_MODELS)
            if st.session_state.chatbot is None or st.session_state.selected_model != selected_model:
                st.session_state.chatbot = self.create_chat_instance(selected_model)
                st.session_state.selected_model = selected_model

            self.chat_col = col1
            self.artifact_col = col2

            with self.chat_col:
                self.handle_user_input()
                self.display_chat_messages()

    def display_chat_messages(self):
        if st.session_state.current_chat_id:
            for message in reversed(st.session_state.chats[st.session_state.current_chat_id]["messages"]):
                with st.chat_message(message["role"]):
                    if message["role"] == "user" and "file" in message:
                        st.markdown(f"Attached file: {message['file']}")
                    st.markdown(message["content"])

    def handle_user_input(self):
        # Create a container for the input area
        input_container = st.container()

        def upload_file():
            uploaded_file = st.file_uploader("Choose a file", type=["pdf"], key="file_uploader",
                                             label_visibility="collapsed")
            if uploaded_file is not None:
                st.session_state.uploaded_file = uploaded_file
                st.success(f"File {uploaded_file.name} uploaded successfully!")
                print(f"Uploaded file type: {type(uploaded_file)}")

        with input_container:
            # Use columns to create a layout similar to Claude's interface
            col1, col2 = st.columns([6, 1], gap='small')

            with col1:
                query = st.text_area("Ask your question here:", key="user_input", height=100)

            with col2:
                st.write("")
                st.write("")
                send_button = st.button(label="", key="send_button", icon=":material/arrow_upward:", type="primary")
                upload_button = st.button(label="", on_click=upload_file, key="upload_button", icon=":material/attach_file:", type="primary")

        # Handle file upload
        if 'uploaded_file' in st.session_state and st.session_state.uploaded_file is not None:
            file_name = st.session_state.uploaded_file.name
            st.write(f"Uploaded file: {file_name}")

        if send_button and (query or getattr(st.session_state, 'uploaded_file', None)):
            if not st.session_state.current_chat_id:
                self.create_new_chat()

            current_chat = st.session_state.chats[st.session_state.current_chat_id]

            if st.session_state.uploaded_file:
                file_content = st.session_state.uploaded_file.read()
                file_name = st.session_state.uploaded_file.name
                file_extension = file_name.lower().split('.')[-1]

                if file_extension in ['pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff']:
                    ocr_text = self.perform_ocr(file_content, file_extension)
                    query += f"\n\nAttached PDF content (OCR):\n{ocr_text}"
                else:
                    query += f"\n\nAttached file content:\n{file_content.decode('utf-8')}"

                current_chat["messages"].append({
                    "role": "user",
                    "content": f"Uploaded file: {file_name}",
                    "file": file_name
                })
                st.session_state.uploaded_file = None

            if query:
                current_chat["messages"].append({"role": "user", "content": query})

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

        current_chat = st.session_state.chats[st.session_state.current_chat_id]
        current_chat["messages"].append({"role": "assistant", "content": chat_content})
        if artifact_content:
            current_chat["messages"].append({"role": "artifact", "content": artifact_content})

    def run(self):
        self.render_sidebar()
        self.render_chat_interface()


def main():
    app = OmniAIChatApp()
    app.run()


if __name__ == "__main__":
    main()