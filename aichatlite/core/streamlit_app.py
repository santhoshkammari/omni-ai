import json
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict, Any

import aipromptlite
from aichatlite.core.tools.base import BaseSearch

from .core import st

from .baseprompt import BasePrompt
from .utils import const
from .omni_mixin import OmniMixin
from .prompts import Prompts
from .streamlit_css import OmniAiChatCSS
from aichatlite.core.utils.prompt_names_fetcher import get_available_prompts
from .agents.regenearate_query_agent import QueryReGenerator
from .tools import WikipediaSearch,YouTubeSearch,ArxivSearch,BingSearch,GoogleSearch,GitHubSearch

st.set_page_config(layout="wide", initial_sidebar_state='collapsed')


@dataclass
class AppConfig:
    AVAILABLE_MODELS: List[str] = field(default_factory=lambda: const.AVAILABLE_MODELS)
    AGENT_TYPES: List[str] = field(default_factory=lambda: const.AGENT_TYPES)
    AGENTS: List[str] = field(default_factory=lambda: const.AGENTS)
    BASE_PROMPT: BasePrompt = BasePrompt()
    AVAILABLE_PROMPTS: List[str] = field(default_factory=get_available_prompts)
    MODELS_TITLE_MAP: Dict[str, str] = field(default_factory=lambda: const.MODELS_TITLE_MAP)
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
            "current_prompt": getattr(aipromptlite, "CLAUDE_SYS_PROMPT"),
            "query": None,
            "knowledge_base_data":"",
            "messages": [],  # Add this for better history management
            "model_cache": {},  # Add this for model caching
            "chat_content": "",
            "artifact_content": ""
        }

    @classmethod
    def load_from_file(cls, config_path: Path):
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


class UIManager:
    def __init__(self, config):
        self.config = config

    def render_sidebar(self):
        st.sidebar.title("Chat History")


@dataclass
class UserMessage:
    content: str


@dataclass
class AIMessage:
    content: str


class ChatManager:
    def __init__(self, chat_id: str, config: AppConfig):
        self.chat_id = chat_id
        self.config = config

    def add_message(self, message: AIMessage | UserMessage):
        st.session_state.messages.append(message)
        if len(st.session_state.messages) > self.config.CHAT_HISTORY_LIMIT:
            st.session_state.messages.pop(0)


class OmniAIChatApp(OmniMixin):

    def __init__(self, config_path: Optional[Path] = None):
        self.config = AppConfig.load_from_file(config_path) if config_path else AppConfig.get_default_config()
        self.theme = ModernUITheme()
        self.ui_manager = UIManager(config=self.config)
        self.chat_manager = ChatManager(chat_id=str(uuid.uuid4()),
                                        config=self.config)
        self.sidebar = st.sidebar
        self.main_area = st.container()
        self.current_query = ""
        self.initialize_session_state()

    def initialize_session_state(self):
        for key, default_value in self.config.DEFAULT_STATES.items():
            if key not in st.session_state:
                st.session_state[key] = default_value

    def render_chat_interface(self):
        with self.main_area:
            OmniAiChatCSS.render_main()
            OmniAiChatCSS.render_title()

            col1, col2 = st.columns([53, 47], gap='small')
            self.chat_col = col1.container()
            self.main_col2_tab1, self.main_col2_tab2,self.knowledge_base_tab = col2.tabs(["Artifact", "Settings","KnowledgeBase"])
            self.artifact_col = self.main_col2_tab1.container(height=self.config.ARTIFACT_COLUMN_HEIGHT, border=True)

            # self.handle_knowledge_base_tab()
            with self.chat_col:
                self.handle_chat_history_and_stream_component()
                self.handle_chat_and_feature_component()

    def update_current_query(self,query):
        st.session_state.query = query
        self.current_query = query

    def handle_chat_and_feature_component(self):
        chat_and_feature_container = st.container()
        with chat_and_feature_container:
            chat_input_and_upload_component = st.container()
            features_component = self.main_col2_tab2.container()

        with chat_input_and_upload_component:
            self.chat_holder = st.container()

            col1, col2 = self.chat_holder.columns([6, 1], gap='small', vertical_alignment='bottom')

            with col1:
                query = st.text_area(placeholder="How can Claude help you today?",
                                         label="query",
                                         label_visibility='hidden',
                                         value="python code to sum two arrays, example for [1,2] and [3,4]"
                                     )
                self.update_current_query(query)

            with col2.popover("", icon=":material/attach_file_add:"):
                st.session_state.uploaded_file = st.file_uploader('uploaded_file', label_visibility='hidden',
                                                                  accept_multiple_files=True,
                                                                  key="file_uploader_key"
                                                                  )

            with col2.popover("", icon=":material/settings:"):
                st.subheader("Model Parameters")

                # Core parameters
                temperature = st.slider('Creativity (temperature)',
                                        min_value=0.0,
                                        max_value=1.0,
                                        value=0.7,
                                        step=0.1,
                                        help="Controls randomness in responses. Higher values make output more random.")

                max_tokens = st.slider('Max words ( tokens)',
                                       min_value=1,
                                       max_value=2000,
                                       value=256,
                                       step=1,
                                       help="Maximum length of generated response.")

                # Advanced parameters
                with st.expander("Advanced Settings"):
                    top_p = st.slider('Top P',
                                      min_value=0.0,
                                      max_value=1.0,
                                      value=0.9,
                                      step=0.1,
                                      help="Controls diversity via nucleus sampling")

                    presence_penalty = st.slider('Presence Penalty',
                                                 min_value=-2.0,
                                                 max_value=2.0,
                                                 value=0.0,
                                                 step=0.1,
                                                 help="Penalizes new tokens based on their presence in text so far")

                    frequency_penalty = st.slider('Frequency Penalty',
                                                  min_value=-2.0,
                                                  max_value=2.0,
                                                  value=0.0,
                                                  step=0.1,
                                                  help="Penalizes new tokens based on their frequency in text so far")

                # Response format settings
                st.subheader("Response Settings")

                # Context window settings
                max_context = st.select_slider('Max Context Length',
                                               options=[1000, 2000, 4000, 8000, 16000, 32000],
                                               value=4000,
                                               help="Maximum number of tokens to use for context")

                # Message formatting
                message_format = st.radio('Message Format',
                                          options=['Markdown', 'Plain Text', 'HTML'],
                                          horizontal=True)

                memory_type = st.selectbox('Conversation Memory',
                                           options=['All Messages', 'Last 10 Messages', 'Last 5 Messages', 'None'],
                                           help="Control how much conversation history to maintain")

        with features_component:
            selected_model = self.handle_selection_container()

            if st.session_state.chatbot is None or st.session_state.selected_model != selected_model:
                system_prompt = self.get_system_prompt(st.session_state.agent_type)
                chatbot_instance = self.create_chat_instance(selected_model, system_prompt)
                # chatbot_instance.chatbot.new_conversation(
                #     modelIndex=self.AVAILABLE_MODELS.index(selected_model),
                #     system_prompt=system_prompt,
                #     switch_to=True)
                st.session_state.chatbot = chatbot_instance
                st.session_state.selected_model = selected_model

        if query:
            st.session_state.messages.append(UserMessage(content=f'Query:{query}'))
            st.session_state.messages.append(AIMessage(content=f"AI: {st.session_state.chat_content}"))
            st.session_state.chat_content = ""
            st.session_state.artifact_content = ""
            kb_data = self.handle_knowledge_base_tab(query)
            self.start_action(kb_data)

    def handle_chat_history_and_stream_component(self):
        self.history_and_stream_area = st.container(height=420)

        with self.history_and_stream_area:
            self.history_part = st.sidebar.container()
            self.chat_message_col = st.container()

        with self.history_part.expander("Chat Conversation"):
            messages = st.session_state.messages.copy()
            nm = messages.copy()
            for i in range(0, len(messages)):
                if isinstance(messages[i], AIMessage) and (i + 2) < len(messages):
                    nm[i] = messages[i + 2]
            for message in nm[:-1]:
                if isinstance(message, UserMessage):
                    st.success(message.content)
                else:
                    div_content = f"""<div class='chat-message'>{message.content}</div>"""
                    st.markdown(div_content, unsafe_allow_html=True)

    def handle_selection_container(self):
        # sc1, sc2, sc3, sc4,sc5 = st.columns([1,1,1,1,1], gap='small')
        s1, s11 = st.columns([1, 1], gap='small')
        s2, s21 = st.columns([1, 1], gap='small')
        s3, s31 = st.columns([1, 1], gap='small')
        s4, s41 = st.columns([1, 1], gap='small')

        with s1.popover('Model', icon=":material/model_training:"):
            st.success('Available Models')
            models = list(self.config.MODELS_TITLE_MAP.keys()) + self.config.AVAILABLE_MODELS
            selected_model = st.radio(
                "Available Models",
                label_visibility='hidden',
                options=models
            )
            if selected_model not in self.config.AVAILABLE_MODELS:
                selected_model = self.config.MODELS_TITLE_MAP.get(selected_model, self.config.AVAILABLE_MODELS[0])

        with s2.popover('TaskType', icon=":material/psychology:"):
            st.success('TaskType')
            agent_type = st.radio("TaskType", self.config.AGENT_TYPES,
                                  label_visibility="hidden",
                                  key="agent_type",
                                  )
            if st.session_state.agent_type is None or st.session_state.agent_type != agent_type:
                st.session_state.agent_type = agent_type

        with s3.popover("Style", icon=":material/palette:"):
            st.success('Model Prompts')
            prompt_name = st.radio("Model Prompts",
                                   get_available_prompts(),
                                   label_visibility="hidden",
                                   key="prompt_name"
                                   )

            if prompt_name != 'CLAUDE_SYSTEM_PROMPT':
                st.session_state.current_prompt = getattr(aipromptlite, prompt_name)

            custom_prompt = st.text_area('System Prompt',
                                         placeholder=st.session_state.current_prompt,
                                         height=100
                                         )
            if custom_prompt:
                st.session_state.current_prompt = custom_prompt

        with s4.popover("Agents", icon=":material/engineering:"):
            st.success("Agents")
            agents = ['None', self.config.AGENTS]
            selected_agent = st.radio(
                "Available Agents",
                label_visibility='hidden',
                options=agents,
                help="Upcoming"
            )

        with st.popover("Experiments", icon=":material/experiment:"):
            st.subheader("Advanced Settings")
            st.button("Save Settings", key="save_settings")

        s11.success(selected_model)
        s21.success(agent_type)
        s31.success(prompt_name)
        s41.success(selected_agent)

        return selected_model

    def start_action(self,kb_data=""):
        # self.handle_chat_history_rendering()
        self.handle_chat_input_and_stream(kb_data)

    def handle_chat_input_and_stream(self,kb_data=""):
        system_prompt = self.add_time_and_artifact_to_system_prompt(
            system_prompt=st.session_state.current_prompt)
        self.artifact_placeholder = self.artifact_col.empty()
        self.chat_placeholder = self.chat_message_col.empty()
        response_generator = self.get_chat_response(st.session_state.chatbot,
                                                    st.session_state.agent_type,
                                                    st.session_state.query,
                                                    web_search=st.session_state.web_search,
                                                    system_prompt=system_prompt,
                                                    kb_data=kb_data)

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
                    st.session_state.chat_content = chat_content
                    format_content = f"""<div class='chat-message'>{chat_content}</div>"""
                    self.chat_placeholder.markdown(format_content, unsafe_allow_html=True)
                else:
                    artifact_content += cleaned_chunk
                    artifact_content = clean_text(artifact_content)
                    st.session_state.artifact_content = artifact_content
                    self.artifact_placeholder.code(artifact_content)

        # Process the stream until complete
        while generation_flag:
            process_stream()

        # Final render of both areas
        if chat_content:
            self.chat_placeholder.markdown(chat_content, unsafe_allow_html=True)
        if artifact_content:
            self.artifact_placeholder.code(artifact_content, unsafe_allow_html=True)

    def run(self):
        self.ui_manager.render_sidebar()
        self.render_chat_interface()

    def get_system_prompt(self, agent_type):
        if agent_type == "AIResearcher":
            return Prompts.REASONING_SBS_PROMPT
        else:
            return Prompts.WORKING_SYSTEM_PROMPT1

    def add_time_and_artifact_to_system_prompt(self, system_prompt):
        return BasePrompt.TODAY_DATE + system_prompt + "\n" + BasePrompt.ARTIFACT

    def handle_knowledge_base_tab(self,query):
        kb_data = ""
        with self.knowledge_base_tab:
            st.subheader("Knowledge Base")
            st.text("Under construction")
            contents= ["hai","this ","is"]
            with st.expander("KB") as main_expander:
                for c in contents:
                    with st.popover('idx'):
                        st.write(c)

            with st.popover("wikipedia"):
                kb_data = KnowledgeItem.render('wikipedia', query=query,
                                               query_regen_tool=QueryReGenerator(),
                                               tool=WikipediaSearch("wikipedia"))
            with st.popover("google"):
                kb_data = KnowledgeItem.render('google', query=query,
                                               query_regen_tool=QueryReGenerator(),
                                               tool=GoogleSearch("google"))

            with st.popover("bing"):
                kb_data = KnowledgeItem.render('bing', query=query,
                                               query_regen_tool=QueryReGenerator(),
                                               tool=BingSearch("bing"))

            with st.popover("arxiv"):
                kb_data = KnowledgeItem.render('arxiv', query=query,
                                               query_regen_tool=QueryReGenerator(),
                                               tool=ArxivSearch("arxiv"))

            with st.popover("github"):
                kb_data = KnowledgeItem.render('github', query=query,
                                               query_regen_tool=QueryReGenerator(),
                                               tool=GitHubSearch("github"))

            with st.popover("youtube"):
                kb_data = KnowledgeItem.render('youtube', query=query,
                                               query_regen_tool=QueryReGenerator(),
                                               tool=YouTubeSearch("youtube"))
        return kb_data


class KnowledgeItem:
    @classmethod
    def render(self, name, query="",
               query_regen_tool: QueryReGenerator = None,
               tool: BaseSearch = None):
        if f'old_{name}_query' not in st.session_state:
            st.session_state[f"old_{name}_query"] = query
        if f'{name}_gen_query' not in st.session_state:
            st.session_state[f'{name}_gen_query'] = query
        if f'{name}_gen_query_ctx' not in st.session_state:
            st.session_state[f'{name}_gen_query_ctx'] = [query]
        if f'{name}_gen_query_content' not in st.session_state:
            st.session_state[f'{name}_gen_query_content'] = ""

        if st.session_state[f'old_{name}_query'] != query:
            st.session_state[f'{name}_gen_query'] = query
            st.session_state[f'old_{name}_query'] = query
            st.session_state[f'{name}_gen_query_ctx'] = [query]
            st.session_state[f'{name}_gen_query_content'] = ""

        st.success(st.session_state[f'{name}_gen_query'])

        regen, fetch, compress, add_to_kb = st.columns([1, 1, 1, 1])
        content = st.empty()
        regen_button_status = regen.button(f"{name}_Gen", icon=':material/youtube_searched_for:',
                                           help="RegenQuery")
        fetch_button_status = fetch.button(f"{name}_Fetch", icon=':material/call_received:', help="FetchData")
        compress_button_status = compress.button(f"{name}_Comp", icon=':material/compress:', help="Compress")
        kb_button_status = add_to_kb.button(f"{name}_KB", icon=':material/chat_add_on:', help="Add to KnowledgeBase")

        if regen_button_status:
            st.session_state[f'{name}_gen_query'] = query_regen_tool.regenerate(st.session_state[f'{name}_gen_query_ctx'])
            st.session_state[f'{name}_gen_query_ctx'].append(st.session_state[f'{name}_gen_query'])

        if fetch_button_status:
            with st.spinner(f"fetching {name}..."):
                wiki_content = tool.fetch(st.session_state[f'{name}_gen_query'])
            st.session_state[f'{name}_gen_query_content'] += wiki_content

        if compress_button_status:
            with st.spinner("compressing data..."):
                compressed_data = tool.compress(st.session_state[f'{name}_gen_query_content'])
            st.session_state[f'{name}_gen_query_content'] = compressed_data

        if kb_button_status:
            with st.spinner("Adding kb..."):
                st.session_state[f'knowledge_base_data'] += st.session_state[f'{name}_gen_query_content']

        with content.expander("content"):
            st.write(st.session_state[f'{name}_gen_query_content'])

        return st.session_state[f'knowledge_base_data']
