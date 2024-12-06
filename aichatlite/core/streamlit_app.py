import time
import uuid

import aipromptlite
from spacy.symbols import agent

from .base import st
from datetime import datetime

from .baseprompt import BasePrompt
from .const import *
from .omni_mixin import OmniMixin
from .prompts import Prompts
from .streamlit_css import OmniAiChatCSS
from ..utils.prompt_names_fetcher import get_available_prompts

st.set_page_config(layout="wide", initial_sidebar_state='collapsed')


class OmniAIChatApp(OmniMixin):
    AVAILABLE_MODELS: List[str] = AVAILABLE_MODELS
    AGENT_TYPES: List[str] = AGENT_TYPES

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
            st.session_state.agent_type = self.AGENT_TYPES[0]
        if "web_search" not in st.session_state:
            st.session_state.web_search = False
        if "current_prompt" not in st.session_state:
            st.session_state.current_prompt = getattr(aipromptlite, "AILITE_X_CLAUDE_PROMPT")


    def render_sidebar(self):
        st.sidebar.title("Chat History")
        if st.sidebar.button("New Chat"):
            self.create_new_chat()

        for chat_id, chat_info in st.session_state.chats.items():
            if st.sidebar.button(f"{chat_info['name']} - {chat_info['timestamp'][:10]}"):
                st.session_state.current_chat_id = chat_id

        st.sidebar.write("Model Information")
        for k,v in MODELS_TITLE_MAP.items():
            st.sidebar.write(f'{k} - {v}')

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
            OmniAiChatCSS.render_title()

            col1, col2 = st.columns([53,47],gap='small')

            self.chat_col = col1
            self.artifact_col = col2.container(height=ARTIFACT_COLUMN_HEIGHT,border=True)

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
            key="metrics_button_{}".format(datetime.now().timestamp()),
            disabled=True
        )


    def handle_user_input(self):
        # Create a container for the input area
        input_container = st.container()
        selection_container = st.container()

        with input_container:
            OmniAiChatCSS.render_chat_history_area()
            self.chat_history_area = st.container()
            self.chat_holder = self.chat_history_area.empty()

            col1, col2 = st.columns([6, 1], gap='small',vertical_alignment='bottom')

            with col1:
                if query := st.chat_input(placeholder="How can Claude help you today?"):
                    query+=""

            with col2:
                self.metrics_container = st.empty()
                self.update_metrics()



        with selection_container:
            sc1, sc2, sc3,sc4,sc5 = st.columns([15, 15, 15,15,35],gap='small'  )
            with sc1.popover('Model'):
                models = list(MODELS_TITLE_MAP.keys()) + AVAILABLE_MODELS
                selected_model = st.radio(
                    "Available Models",
                    label_visibility='hidden',
                    options=models
                )
                if selected_model not in AVAILABLE_MODELS:
                    selected_model = MODELS_TITLE_MAP.get(selected_model, AVAILABLE_MODELS[0])

            with sc2.popover('Type'):
                agent_type = st.radio("Agent type", self.AGENT_TYPES,
                                      label_visibility="hidden",
                                      key="agent_type",
                                      )
                if st.session_state.agent_type is None or st.session_state.agent_type != agent_type:
                    st.session_state.agent_type = agent_type

            with sc4.popover("", icon="🔗"):
                st.session_state.uploaded_file = st.file_uploader('uploaded_file', label_visibility='hidden',
                                 accept_multiple_files=True)
                st.success(f"File {st.session_state.uploaded_file} uploaded successfully!")


            with sc3.popover("Style"):
                prompt_name = st.radio("Select a model",
                                       get_available_prompts(),
                                       label_visibility="hidden",
                                       key="prompt_name"
                                       )
                if prompt_name != 'DEFAULT_PROMPT':
                    st.session_state.current_prompt = getattr(aipromptlite, prompt_name)



            if st.session_state.chatbot is None or st.session_state.selected_model != selected_model:
                system_prompt = self.get_system_prompt(st.session_state.agent_type)
                chatbot_instance = self.create_chat_instance(selected_model,system_prompt)
                # chatbot_instance.chatbot.new_conversation(
                #     modelIndex=self.AVAILABLE_MODELS.index(selected_model),
                #     system_prompt=system_prompt,
                #     switch_to=True)
                st.session_state.chatbot = chatbot_instance
                st.session_state.selected_model = selected_model



        if query or st.session_state.uploaded_file:
            print(f'file name: {st.session_state.uploaded_file}')
            if not st.session_state.current_chat_id:
                self.create_new_chat()

            current_chat = st.session_state.chats[st.session_state.current_chat_id]

            if st.session_state.uploaded_file:
                file_data = []
                for f in st.session_state.uploaded_file:
                    file_data.append({
                        "bytes": f.read(),
                        "name": f.name,
                        "extension": f.name.lower().split('.')[-1]
                    })

                print(file_data[0]['name'])


                # if file_extension in ['pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff']:
                #     with st.spinner("Analyzing pdf ..."):
                #         query = self.handle_files(query,file_content,file_extension)

                current_chat["messages"].append({
                    "role": "user",
                    "content": f"Uploaded file:",
                    "file": ""
                })
                st.session_state.uploaded_file = None

            if query:
                current_chat["messages"].append({"role": "user", "content": query})

            self.process_ai_response(query,web_search = st.session_state.web_search,
                                     system_prompt = st.session_state.current_prompt)

    def process_ai_response(self, query: str, web_search=False,system_prompt=""):
        system_prompt = self.add_time_and_artifact_to_system_prompt(system_prompt=system_prompt)
        chat_placeholder = st.empty()
        artifact_placeholder = self.artifact_col.empty()

        response_generator = self.get_chat_response(st.session_state.chatbot, st.session_state.agent_type,query,web_search=web_search,
                                                    system_prompt=system_prompt)
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

    def get_system_prompt(self, agent_type):
        if agent_type == "AIResearcher":
            return Prompts.REASONING_SBS_PROMPT
        else:
            return Prompts.WORKING_SYSTEM_PROMPT1

    def add_time_and_artifact_to_system_prompt(self, system_prompt):
        return BasePrompt.TODAY_DATE + system_prompt + "\n" + BasePrompt.ARTIFACT