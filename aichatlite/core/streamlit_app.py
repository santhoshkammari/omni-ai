import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict

import aipromptlite

from .base import st
from datetime import datetime

from .baseprompt import BasePrompt
from .utils import const
from .omni_mixin import OmniMixin
from .prompts import Prompts
from .streamlit_css import OmniAiChatCSS
from ..utils.prompt_names_fetcher import get_available_prompts

st.set_page_config(layout="wide", initial_sidebar_state='collapsed')

@dataclass
class AppConfig:
    AVAILABLE_MODELS: List[str] = field(default_factory=lambda :const.AVAILABLE_MODELS)
    AGENT_TYPES: List[str] = field(default_factory=lambda :const.AGENT_TYPES)
    BASE_PROMPT: BasePrompt = BasePrompt()
    AVAILABLE_PROMPTS: List[str] = field(default_factory=get_available_prompts)
    MODELS_TITLE_MAP: Dict[str, str] = field(default_factory=lambda :const.MODELS_TITLE_MAP)
    ARTIFACT_COLUMN_HEIGHT: int = const.ARTIFACT_COLUMN_HEIGHT
    ENABLE_EXPERIMENTAL: bool = False
    CHAT_HISTORY_LIMIT: int = 100
    def __post_init__(self):
        self.DEFAULT_STATES = {
            "chats": {},
            "current_chat_id": None,
            "chatbot": None,
            "selected_model": const.AVAILABLE_MODELS[0],  # Set default model
            "sidebar_state": "expanded",
            "uploaded_file": None,
            "agent_type": const.AGENT_TYPES[0],
            "web_search": False,
            "current_prompt": "",
            "query": None,
            "chat_history": [],  # Add this for better history management
            "model_cache": {},  # Add this for model caching
        }


    @classmethod
    def load_from_file(cls, config_path:Path):
        if config_path.exists():
            with config_path.open() as f:
                config_data = json.load(f)
                return cls(**config_data)
        return cls()

    @staticmethod
    def get_default_config() -> 'AppConfig':
        return AppConfig()

class ModernUITheme:
    @staticmethod
    def apply_dark_mode() -> None:
        st.markdown("""
            <style>
            .stApp {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
            .stButton>button {
                background-color: #2E2E2E;
                color: #FFFFFF;
            }
            </style>
            """, unsafe_allow_html=True)

class OmniAIChatApp(OmniMixin):

    def __init__(self,config_path:Optional[Path]=None):
        self.config = AppConfig.load_from_file(config_path) if config_path else AppConfig.get_default_config()
        self.theme = ModernUITheme()
        self.sidebar = st.sidebar
        self.main_area = st.container()
        self.initialize_session_state()

    def initialize_session_state(self):
        for key, default_value in self.config.DEFAULT_STATES.items():
            if key not in st.session_state:
                st.session_state[key] = default_value


    def render_sidebar(self):
        st.sidebar.title("Chat History")

        for chat_id, chat_info in st.session_state.chats.items():
            if st.sidebar.button(f"{chat_info['name']} - {chat_info['timestamp'][:10]}"):
                st.session_state.current_chat_id = chat_id

        st.sidebar.write("Model Information")
        for k,v in self.config.MODELS_TITLE_MAP.items():
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
            self.artifact_col = col2.container(height=self.config.ARTIFACT_COLUMN_HEIGHT,border=True)

            with self.chat_col:
                self.display_chat_messages()
                self.handle_user_input()

    def display_chat_messages(self):
        self.chat_message_col = st.container(height=400)


    def handle_selection_container(self):
        sc1, sc2, sc3, sc4,sc5 = st.columns([1,1,1,1,1], gap='small')
        with sc1.popover('Model',icon=":material/model_training:"):
            st.success('Available Models')
            models = list(self.config.MODELS_TITLE_MAP.keys()) + self.config.AVAILABLE_MODELS
            selected_model = st.radio(
                "Available Models",
                label_visibility='hidden',
                options=models
            )
            if selected_model not in self.config.AVAILABLE_MODELS:
                selected_model = self.config.MODELS_TITLE_MAP.get(selected_model, self.config.AVAILABLE_MODELS[0])

        with sc2.popover('Type',icon=":material/tune:"):
            st.success('TaskType')
            agent_type = st.radio("TaskType", self.config.AGENT_TYPES,
                                  label_visibility="hidden",
                                  key="agent_type",
                                  )
            if st.session_state.agent_type is None or st.session_state.agent_type != agent_type:
                st.session_state.agent_type = agent_type



        with sc3.popover("Style",icon=":material/palette:"):
            st.success('Model Prompts')
            prompt_name = st.radio("Model Prompts",
                                   get_available_prompts(),
                                   label_visibility="hidden",
                                   key="prompt_name"
                                   )
            if prompt_name != 'DEFAULT_PROMPT':
                st.session_state.current_prompt = getattr(aipromptlite, prompt_name)

        with sc4.popover("Tools",icon=":material/build_circle:"):
            st.subheader("Tools")
            st.button("Clear Chat History", key="clear_chat_history")
            st.button("Restart Chatbot", key="restart_chatbot")
            st.button("Reset Settings", key="reset_settings")

            st.button("Save Chat", key="save_chat")
            st.button("Load Chat", key="load_chat")
            st.toggle("WebSearch")

        with sc5.popover("exp",icon=":material/experiment:"):
            st.subheader("Advanced Settings")
            st.button("Save Settings", key="save_settings")



        return selected_model


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
                        st.session_state.query = query

                with col2.popover("",icon=":material/attach_file_add:"):
                    st.session_state.uploaded_file = st.file_uploader('uploaded_file', label_visibility='hidden',
                                                                      accept_multiple_files=True,
                                                                      key="file_uploader_key"
                                                                      )

            with selection_container:
                selected_model = self.handle_selection_container()

                if st.session_state.chatbot is None or st.session_state.selected_model != selected_model:
                    system_prompt = self.get_system_prompt(st.session_state.agent_type)
                    chatbot_instance = self.create_chat_instance(selected_model,system_prompt)
                    # chatbot_instance.chatbot.new_conversation(
                    #     modelIndex=self.AVAILABLE_MODELS.index(selected_model),
                    #     system_prompt=system_prompt,
                    #     switch_to=True)
                    st.session_state.chatbot = chatbot_instance
                    st.session_state.selected_model = selected_model

            if query:
                self.start_action()

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

    def start_action(self):
        system_prompt = self.add_time_and_artifact_to_system_prompt(
            system_prompt=st.session_state.current_prompt)
        self.artifact_placeholder = self.artifact_col.empty()
        self.chat_placeholder = self.chat_message_col.empty()
        response_generator = self.get_chat_response(st.session_state.chatbot,
                                                    st.session_state.agent_type,
                                                    st.session_state.query,
                                                    web_search=st.session_state.web_search,
                                                    system_prompt=system_prompt)

        # Initialize accumulators
        chat_content = ""
        artifact_content = ""
        current_mode = "chat"  # Start in chat mode
        generation_flag = True

        TRASH_TAGS = [
            "<artifact_area>",
            "artifact<",
            "```python",
            "##/normal_content>",
            "##normal_content>",
            "artifact_area>",
            "artifactarea>",
            "artifactive>",
            "```",
            "<code_or_keypoints>",
            "<code_or",
            "code_or",
            "_keypoints>",
            "_area>",
            "python",
            "```",
            "</",
            "<"
        ]

        def is_artifact_tag(text):
            return "artifact" in text

        def clean_text(text):
            for tag in TRASH_TAGS:
                text = text.replace(tag, "")
            return text

        def process_stream():
            nonlocal chat_content, artifact_content, current_mode, generation_flag

            for chunk in response_generator:
                if chunk is None:
                    generation_flag = False
                    continue

                # Check for mode switches
                if is_artifact_tag(chunk):
                    if current_mode == "chat":
                        current_mode = "artifact"
                    else:
                        current_mode = "chat"
                    continue

                # Clean the chunk
                cleaned_chunk = clean_text(chunk)

                # Append to appropriate content
                if current_mode == "chat":
                    chat_content += cleaned_chunk
                    chat_content = clean_text(chat_content)
                    self.chat_placeholder.markdown(chat_content)
                else:
                    artifact_content += cleaned_chunk
                    artifact_content = clean_text(artifact_content)
                    self.artifact_placeholder.code(artifact_content)

        # Process the stream until complete
        while generation_flag:
            process_stream()

        # Final render of both areas
        if chat_content:
            self.chat_placeholder.markdown(chat_content)
        if artifact_content:
            self.artifact_placeholder.code(artifact_content)