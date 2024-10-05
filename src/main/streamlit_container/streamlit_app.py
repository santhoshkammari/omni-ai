import time

import PyPDF2
from .stream_base import st
from src.main.omni_ai import OmniAIChat
from typing import List, Tuple, Generator
from datetime import datetime
import io

from src.main.streamlit_container.streamlit_css import OmniAiChatCSS

st.set_page_config(layout="wide", initial_sidebar_state='collapsed')


class OmniAIChatApp:
    AVAILABLE_MODELS: List[str] = [
        'CohereForAI/c4ai-command-r-plus-08-2024',
        'Qwen/Qwen2.5-72B-Instruct',
        'NousResearch/Hermes-3-Llama-3.1-8B',
        'mistralai/Mistral-Nemo-Instruct-2407',
        'meta-llama/Meta-Llama-3.1-70B-Instruct',
        'meta-llama/Llama-3.2-11B-Vision-Instruct',
        'microsoft/Phi-3.5-mini-instruct',

    ]
    AGENT_TYPES: List[str] = [
        "QuestionAnswer",
        "Assistant",
        "Agent",
        "CoT",
        "Reader",
        "Interpreter"
    ]

    def __init__(self):
        self.sidebar = st.sidebar
        self.main_area = st.container()
        self.initialize_session_state()
        self.chunks_per_second = 0
        self.elapsed_time = 0

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
        if "agent_type" not in st.session_state:
            st.session_state.agent_type = "QuestionAnswer"
        if "web_search" not in st.session_state:
            st.session_state.web_search = False

    @staticmethod
    def create_chat_instance(model: str) -> OmniAIChat:
        return OmniAIChat(model=model)

    @staticmethod
    def get_chat_response(chatbot: OmniAIChat, query: str, web_search: bool = False) -> Generator:
        return chatbot.generator(query, web_search=web_search)
        # from src.main.ollama_api import CustomChatOllama
        # llm = CustomChatOllama()
        # for x in llm.stream(query):
        #     yield x.content


    @staticmethod
    def data_stream(generator: Generator) -> Generator[Tuple[str, bool], None, None]:
        flag = True
        for chunk in generator:
            if chunk == 'artifact':
                flag = not flag
            yield chunk, flag

    @staticmethod
    def perform_ocr(file_content: bytes, file_type: str) -> str:
        reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        num_pages = len(reader.pages)

        content = ""
        for page in range(num_pages):
            content += reader.pages[page].extract_text()

        return content

    @staticmethod
    def update_chat_col(generator: Generator, chat_placeholder: st.empty, artifact_placeholder: st.empty,
                        chat_holder: st.empty) -> Tuple[
        str, str]:
        chat_content, artifact_content = "", ""
        for item, flag in generator:
            if flag:
                chat_content += item
                chat_content = chat_content.replace("<artifact_area>", "")
                chat_content = chat_content.replace("artifact<", "")
                # chat_placeholder.write(chat_content)
                chat_content = chat_content.replace("<","##")
                # chat_placeholder.write('<div class="chat-history">' + chat_content + '</div>', unsafe_allow_html=True)
                chat_holder.markdown('<div class="chat-history">' + chat_content + '</div>', unsafe_allow_html=True)

            else:
                artifact_content += item
                if artifact_content[-2:] == "</": artifact_content = artifact_content[:-2]
                artifact_content = artifact_content.replace("artifact_area>", "")
                artifact_content = artifact_content.replace("```python", "")
                artifact_content = artifact_content.replace("python", "")
                artifact_content = artifact_content.replace("```", "")
                artifact_placeholder.code(artifact_content)
                # artifact_placeholder.code(artifact_content)
        return chat_content, artifact_content




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
            OmniAiChatCSS.render_main()
            st.markdown("""
                <style>
                .stApp > header {
                    background-color: transparent;
                    height: auto !important;
                    padding-top: 0 !important;
                    padding-bottom: 0 !important;
                }
                .small-title {
                    font-size: 24px;
                    # color: #4a4a4a;
                    font-weight: 600;
                    text-align: center;
                    padding: 5px 0;
                    margin: 0;
                    # background-color: #f0f0f0;
                }
                </style>
                """, unsafe_allow_html=True)

            st.markdown("<h1 class='small-title'>OmniAI Chat Interface</h1>", unsafe_allow_html=True)


            # Custom CSS

            st.write("""
                    <style>
                    div[data-baseweb="select"] > div {
                        width: 300px !important;
                    }
                    
                    </style>
                    """, unsafe_allow_html=True)

            col1, col2 = st.columns([1,1],gap='small')

            self.chat_col = col1
            self.artifact_col = col2.container(height=500,border=True)

            with self.chat_col:
                self.handle_user_input()
                # self.display_chat_messages()

    def display_chat_messages(self):
        if st.session_state.current_chat_id:
            for message in reversed(st.session_state.chats[st.session_state.current_chat_id]["messages"]):
                with st.chat_message(message["role"]):
                    if message["role"] == "user" and "file" in message:
                        st.write(f"Attached file: {message['file']}")
                    st.write(message["content"])

    def update_metrics(self):
        self.metrics_container.button(
            label=f"{self.chunks_per_second}/s, {self.elapsed_time}s",
            key="metrics_button_{}".format(self.chunks_per_second),
            disabled=True
        )

    def handle_user_input(self):
        # Create a container for the input area
        input_container = st.container()
        selection_container = st.container()

        def upload_file():
            uploaded_file = st.file_uploader("Choose a file", type=["pdf"], key="dfd",
                                             label_visibility="collapsed")

            if uploaded_file is not None:
                st.session_state.uploaded_file = uploaded_file
                st.success(f"File {uploaded_file.name} uploaded successfully!")
                print(f"Uploaded file type: {type(uploaded_file)}")

        with input_container:
            st.markdown("""
                <style>
                .chat-history {
                     height: 50vh;
                     width: 100vh;
            overflow-y: auto;
            overflow-x: hidden;
            white-space: normal;
            word-wrap: break-word;
                }
                </style>
            """, unsafe_allow_html=True)

            # Use columns to create a layout similar to Claude's interface
            self.chat_history_area = st.container()
            self.chat_holder = self.chat_history_area.empty()

            col1, col2 = st.columns([6, 1], gap='small',vertical_alignment='bottom')

            with col1:
                query = st.text_area(label="user_input",placeholder = "Ask your question here:", key="user_input", height=100,
                                     label_visibility="collapsed",
                                     value="explain python class using very small code example and explanation"
                                     )
                splitterd_query = query.split()
                if splitterd_query and splitterd_query[-1].lower() == 'google':
                    st.session_state.web_search = True


            with col2:
                send_button = st.button(label="", key="send_button", icon=":material/arrow_upward:", type="primary")
                self.metrics_container = st.empty()
                self.update_metrics()



        with selection_container:
            sc1,sc2 = st.columns([1,1])
            with sc1:
                selected_model = st.selectbox("Select a model", self.AVAILABLE_MODELS, label_visibility="collapsed",
                                              key="model")

            with sc2:
                agent_type = st.selectbox("Agent type",self.AGENT_TYPES,
                                              label_visibility="collapsed",
                                              key="agent_type")
                if st.session_state.agent_type is None or st.session_state.agent_type != agent_type:
                    st.session_state.agent_type = agent_type


            if st.session_state.chatbot is None or st.session_state.selected_model != selected_model:
                st.session_state.chatbot = self.create_chat_instance(selected_model)
                st.session_state.selected_model = selected_model

        uploaded_file = st.file_uploader("file uploading", type=["pdf"], key="file_uploader",
                                         label_visibility="collapsed")

        if uploaded_file is not None:
            st.session_state.uploaded_file = uploaded_file
            st.success(f"File {uploaded_file.name} uploaded successfully!")


        if send_button and (query or getattr(st.session_state, 'uploaded_file', None)):
            if not st.session_state.current_chat_id:
                self.create_new_chat()

            current_chat = st.session_state.chats[st.session_state.current_chat_id]

            if st.session_state.uploaded_file:
                file_content = st.session_state.uploaded_file.read()
                file_name = st.session_state.uploaded_file.name
                file_extension = file_name.lower().split('.')[-1]
                print("file Processing")

                if file_extension in ['pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff']:
                    ocr_text = self.perform_ocr(file_content, file_extension)
                    query += f"\n\nAttached PDF content (OCR):\n{ocr_text}"


                current_chat["messages"].append({
                    "role": "user",
                    "content": f"Uploaded file: {file_name}",
                    "file": file_name
                })
                st.session_state.uploaded_file = None

            if query:
                current_chat["messages"].append({"role": "user", "content": query})

            self.process_ai_response(query,web_search = st.session_state.web_search)

    def process_ai_response(self, query: str,web_search=False):
        chat_placeholder = st.empty()
        artifact_placeholder = self.artifact_col.empty()

        response_generator = self.get_chat_response(st.session_state.chatbot, query,web_search=web_search)
        # Initialize chunk counting and timing
        start_time = time.time()
        chunk_count = 0

        def chunk_counting_stream(generator):
            nonlocal chunk_count
            for chunk, flag in self.data_stream(generator):
                chunk_count += 1
                yield chunk, flag

        chat_content, artifact_content = self.update_chat_col(
            chunk_counting_stream(response_generator),
            chat_placeholder,
            artifact_placeholder,
            self.chat_holder
        )

        # Calculate chunks per second
        end_time = time.time()
        elapsed_time = end_time - start_time
        chunks_per_second = chunk_count / elapsed_time if elapsed_time > 0 else 0

        # Display chunks per second
        self.chunks_per_second = int(chunks_per_second)
        self.elapsed_time = int(elapsed_time)
        self.total_tokens = chunk_count
        st.sidebar.text(f"Tokens/s : {self.chunks_per_second}")
        st.sidebar.text(f"Inference: {int(elapsed_time)}s")
        st.sidebar.text(f"Total tokens: {chunk_count}")
        self.update_metrics()

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

