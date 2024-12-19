import json
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict
import aipromptlite
import streamlit as st
from ailitellm import yieldai

from aichatlite.utils import constants as const

st.set_page_config(layout="wide", initial_sidebar_state='collapsed')

def get_available_prompts():
    prompt_names = [_ for _ in dir(aipromptlite) if _.isupper()]
    prompt_names.sort()
    return ['CLAUDE_SYSTEM_PROMPT']+ prompt_names

from datetime import datetime

today_date = datetime.now().strftime('%a %d %b %Y, %I:%M%p')
class BasePrompt:
    TODAY_DATE = f"""The current date is {datetime.now().strftime("%Y-%m-%d")}.\n"""
    ARTIFACT =  """Always wrap code, scripts, or executable content in <artifact_area> tags. This includes:
       - Python code snippets
       - Complete scripts or functions
       - Any other executable code
    Example:
    <artifact_area>
    def hello_world():
        print("Hello, World!")
    </artifact_area>
You will Keep explanations and non-code content outside of the <artifact_area> tags.
DO NOT FORGET TO WRAP PYTHON CODE TO WRAP IN <artifact_area> tags."""
REASONING_SBS_PROMPT = """You are an AI assistant that explains your reasoning step by step. For EVERY response, without exception, provide a SINGLE JSON object with the following structure:

    {
        "title": "Brief title of the step",
        "content": "Detailed explanation of your thoughts and reasoning for this step",
        "next_action": "One of: 'continue', 'reflect', or 'final_answer'",
        "confidence": A number between 0 and 1 indicating your confidence in this step
    }

    Critical Instructions:
    1. ALWAYS respond with a SINGLE, valid JSON object. Never include multiple JSON objects or any text outside the JSON structure.
    2. Use the 'content' field to show your work, explore multiple angles, and explain your reasoning. All your thoughts and explanations should be within this field.
    3. Use 'next_action' to indicate if you need another step ('continue'), want to reflect on your progress ('reflect'), or are ready to give the final answer ('final_answer').
    4. Use 'confidence' to guide your approach: above 0.8 means continue, 0.5-0.7 suggests minor adjustments, below 0.5 means consider a different approach.
    5. After every 3 steps, use 'reflect' as the next_action to perform a self-reflection on your reasoning.
    6. For mathematical problems, show all work explicitly in the 'content' field.
    7. If you need to explore multiple solutions, do so within a single JSON response by including all explorations in the 'content' field.

    Remember: Your ENTIRE response, for EVERY interaction, must be a SINGLE, valid JSON object. Do not include any text or explanations outside of this JSON structure.
    """+f"Today Date&Time : {today_date}"

WORKING_SYSTEM_PROMPT1 = f"""
<claude_info> The assistant is Claude, created by Anthropic. 
The current date is {datetime.now().strftime("%Y-%m-%d")}. 
 If it seems like the user is expecting Claude to do so, it clarifies the situation and asks the human to paste the relevant text or image content directly into the conversation. 
 If it is asked to assist with tasks involving the expression of views held by a significant number of people, Claude provides assistance with the task regardless of its own views. 
 If asked about controversial topics, it tries to provide careful thoughts and clear information. 
 It refine and expands the requested information without explicitly saying that the topic is sensitive, and without claiming to be presenting objective facts and starts by giving this rephrased with plan to perform. 
 When presented with a math problem, logic problem, or other problem benefiting from systematic thinking, Claude thinks through it step by step before giving its final answer. If Claude cannot or will not perform a task, it tells the user this without apologizing to them. It avoids starting its responses with “I’m sorry” or “I apologize”. If Claude is asked about a very obscure person, object, or topic, i.e. if it is asked for the kind of information that is unlikely to be found more than once or twice on the internet, Claude ends its response by reminding the user that although it tries to be accurate, it may hallucinate in response to questions like this. It uses the term ‘hallucinate’ to describe this since the user will understand what it means. If Claude mentions or cites particular articles, papers, or books, it always lets the human know that it doesn’t have access to search or a database and may hallucinate citations, so the human should double check its citations. Claude is very smart and intellectually curious. It enjoys hearing what humans think on an issue and engaging in discussion on a wide variety of topics. If the user seems unhappy with Claude or Claude’s behavior, Claude tells them that although it cannot retain or learn from the current conversation, they can press the ‘thumbs down’ button below Claude’s response and provide feedback to Anthropic. If the user asks for a very long task that cannot be completed in a single response, Claude offers to do the task piecemeal and get feedback from the user as it completes each part of the task. Claude uses markdown for code. Immediately after closing coding markdown, Claude asks the user if they would like it to explain or break down the code. It does not explain or break down the code unless the user explicitly requests it. </claude_info>


Claude provides thorough responses to more complex and open-ended questions or to anything where a long response is requested, but concise responses to simpler questions and tasks. All else being equal, it tries to give the most correct and concise answer it can to the user’s message. Rather than giving a long response, it gives a concise response and offers to elaborate if further information may be helpful.

Claude is happy to help with analysis, question answering, math, coding, creative writing, teaching, role-play, general discussion, and all sorts of other tasks.

Claude will  Always wrap code, scripts, or executable content in <artifact_area> tags. This includes:
       - Python code snippets
       - Complete scripts or functions
       - Any other executable code
    Example:
    <artifact_area>
    def hello_world():
        print("Hello, World!")
    </artifact_area>
Claude will Keep explanations and non-code content outside of the <artifact_area> tags.
DO NOT FORGET TO WRAP PYTHON CODE TO WRAP IN <artifact_area> tags.

Claude responds directly to all human messages without unnecessary affirmations or filler phrases like “Certainly!”, “Of course!”, “Absolutely!”, “Great!”, “Sure!”, etc. Specifically, Claude avoids starting responses with the word “Certainly” in any way.

Claude follows this information in all languages, and always responds to the user in the language they use or request. The information above is provided to Claude by Anthropic. Claude never mentions the information above unless it is directly pertinent to the human’s query. Claude is now being connected with a human.

    """


from typing import Tuple, Generator


class OmniCore:
    def __init__(self,model = 0,system_prompt = ""):
        self.system_prompt = system_prompt
        self.DEFAULT_MODELS = [
    "Qwen/Qwen2.5-72B-Instruct",
    "Qwen/QwQ-32B-Preview",
    "Qwen/Qwen2.5-Coder-32B-Instruct",
    "NousResearch/Hermes-3-Llama-3.1-8B",
    "microsoft/Phi-3.5-mini-instruct"
]
        self.current_model = model


    def generator(self,query,web_search= False,system_prompt = ""):
        messages = self._add_system_prompt(query,
                                        system_prompt=system_prompt)
        for resp in yieldai(messages_or_prompt=messages):
            if resp:
                yield resp

    def print_stream(self,query,web_search = False):
        for x in self.generator(query,web_search):
            print(x,end= "",flush=True)

    def _add_system_prompt(self, query,system_prompt= ""):
        return [
            {"role":"system","content":system_prompt or self.system_prompt},
            {"role":"user","content":query}
        ]

    def invoke(self,query,web_search=False):
        return self.generator(query)


class OmniMixin:
    @staticmethod
    def create_chat_instance(model: str,system_prompt) -> OmniCore:
        return OmniCore(model=model,system_prompt = system_prompt)

    @staticmethod
    def get_chat_response(chatbot: OmniCore, agent_type:str, query: str, web_search: bool = False,
                          system_prompt="") -> Generator:
        return chatbot.generator(query,
                               system_prompt=system_prompt)

    @staticmethod
    def data_stream(generator: Generator) -> Generator[Tuple[str, bool], None, None]:
        flag = True
        for chunk in generator:
            if chunk.strip().lower() == 'artifact':
                flag = not flag
            yield chunk, flag

    @staticmethod
    def update_chat_col(generator: Generator, chat_placeholder: st.empty, artifact_placeholder: st.empty,
                        chat_holder: st.empty) -> Tuple[
        str, str]:
        chat_content, artifact_content = "", ""
        artifact_placeholder_markdown_flag = True  # false means code
        start_flag_artifact_placeholder = True
        previous_back_tick = False
        python_script_start_tag = False
        for item, flag in generator:
            if flag:
                start_flag_artifact_placeholder = True
                chat_content += item
                chat_content = OmniMixin.filter_chat_content(chat_content)
                chat_holder.markdown('<div class="chat-history">' + chat_content + '</div>', unsafe_allow_html=True)

            else:
                artifact_content += item
                if item =="```":
                    previous_back_tick = True
                    continue
                if previous_back_tick and item == "python":
                    python_script_start_tag = True
                    previous_back_tick = False
                    continue
                if item == "```" and python_script_start_tag:
                    python_script_start_tag = False
                    continue

                if start_flag_artifact_placeholder and (item.lower() in ["```", "python", "```python",
                                                                         "class","def"]):
                    artifact_placeholder_markdown_flag = False
                    start_flag_artifact_placeholder = False

                artifact_content = OmniMixin.filter_artifact_content(artifact_content)

                # if artifact_placeholder_markdown_flag:
                #     artifact_placeholder.markdown(artifact_content)
                # else:
                artifact_placeholder.code(artifact_content)
        return chat_content, artifact_content

    @staticmethod
    def handle_files(query, file_content, file_extension):
        if file_extension=="pdf":
            # handler = PdfHandler(file_content=file_content,
            #                      word_llama_dim=WORD_LLAMA_DIM)
            # context = handler.run(query,k=5)
            context = ""
            prompt= f"<context>\n\n ### Attached PDF content:\n\n{context}\n</context>\n" + query
        else:
            prompt = query
        return prompt

    @staticmethod
    def filter_chat_content(chat_content):
        chat_content = chat_content.replace("<artifact_area>", "")
        chat_content = chat_content.replace("artifact<", "")
        chat_content = chat_content.replace("<", "##")
        chat_content = chat_content.replace("```python", "")
        chat_content = chat_content.replace("##/normal_content>", "")
        chat_content = chat_content.replace("##normal_content>", "")
        return chat_content

    @staticmethod
    def filter_artifact_content(artifact_content):
        if artifact_content[-2:] == "</": artifact_content = artifact_content[:-2]
        artifact_content = artifact_content.replace("artifact_area>", "")
        artifact_content = artifact_content.replace("artifactarea>", "")
        artifact_content = artifact_content.replace("artifactive>", "")
        artifact_content = artifact_content.replace("```python", "")
        # artifact_content = artifact_content.replace("python", "")
        artifact_content = artifact_content.replace("```", "")
        artifact_content = artifact_content.replace("<code_or_keypoints>", "")
        artifact_content = artifact_content.replace("<code_or", "")
        artifact_content = artifact_content.replace("code_or", "")
        artifact_content = artifact_content.replace("_keypoints>", "")
        return artifact_content

@dataclass
class AppConfig:
    AVAILABLE_MODELS: List[str] = field(default_factory=lambda :const.AVAILABLE_MODELS)
    AGENT_TYPES: List[str] = field(default_factory=lambda :const.AGENT_TYPES)
    AGENTS: List[str] = field(default_factory=lambda :const.AGENTS)
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
            "current_prompt": getattr(aipromptlite, "CLAUDE_SYS_PROMPT"),
            "query": None,
            "messages": [],  # Add this for better history management
            "model_cache": {},  # Add this for model caching
            "chat_content":"",
            "artifact_content":""
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

class UIManager:
    def __init__(self,config):
        self.config = config


    def render_sidebar(self):
        st.sidebar.title("Chat History")


@dataclass
class UserMessage:
    content:str

@dataclass
class AIMessage:
    content: str

class ChatManager:
    def __init__(self, chat_id: str,config:AppConfig):
        self.chat_id = chat_id
        self.config = config

    def add_message(self, message: AIMessage|UserMessage):
        st.session_state.messages.append(message)
        if len(st.session_state.messages) > self.config.CHAT_HISTORY_LIMIT:
            st.session_state.messages.pop(0)



class OmniAiChatCSS:
    @staticmethod
    def render_main():
        st.markdown("""
            <style>
                /* Core variables */
                :root {
                    --background-primary: #FDFBF9;
                    --text-primary: #18181B;
                    --text-secondary: #71717A;
                    --border-color: #E4E4E7;
                }

                /* Base styles */
                .stApp {
                    background-color: var(--background-primary);
                    font-family: 'Tiempos Text', BlinkMacSystemFont, sans-serif;
                }

                /* Container adjustments */
                [data-testid="stAppViewContainer"] {
                    padding-top: 0 !important;
                }

                .block-container {
                    padding-top: 0 !important;
                    padding-bottom: 0 !important;
                    max-width: none;
                }

                /* Streamlit elements adjustments */
                .stSelectbox [data-testid="stMarkdown"] {
                    display: none;
                }

                /* Remove box styling from select boxes */
                .stSelectbox > div > div {
                    background: transparent !important;
                    border: none !important;
                    padding: 0 !important;
                }

                .stSelectbox {
                    color: var(--text-secondary);
                }

                /* Chat input styling */
                .stTextInput > div > div > input {
                    border: 1px solid var(--border-color);
                    border-radius: 8px;
                    padding: 0.75rem;
                    font-size: 0.95rem;
                }

                /* Message styling */
                [data-testid="stChatMessage"] {
                    background: transparent;
                    border: none;
                    padding: 1rem 0;
                    margin: 0;
                }

                /* Sidebar refinements */
                .stSidebar {
                    background-color: white;
                    border-right: 1px solid var(--border-color);
                }

                .stSidebar .block-container {
                    padding: 1.5rem 1rem;
                }

                /* Header/Navigation bar */
                .nav-header {
                    position: sticky;
                    top: 0;
                    background: white;
                    border-bottom: 1px solid var(--border-color);
                    padding: 0.5rem 1rem;
                    z-index: 100;
                    font-size: 0.9rem;
                    color: var(--text-secondary);
                }

                /* Remove unnecessary padding */
                .css-18e3th9, .css-1d391kg {
                    padding: 1rem 0;
                }

                /* File uploader styling */
                [data-testid="stFileUploader"] {
                    padding: 1rem 0;
                }

                /* Metrics button */
                .stButton > button[disabled] {
                    background: transparent !important;
                    border: none !important;
                    color: var(--text-secondary) !important;
                    padding: 0 !important;
                    font-size: 0.85rem;
                }

                /* Custom scrollbar */
                ::-webkit-scrollbar {
                    width: 6px;
                    height: 6px;
                }

                ::-webkit-scrollbar-track {
                    background: transparent;
                }

                ::-webkit-scrollbar-thumb {
                    background: #D4D4D8;
                    border-radius: 3px;
                }
            </style>
        """, unsafe_allow_html=True)

        st.markdown("""
                    <style>
                        /* First, try to use Tiempos if available */
                        @font-face {
                            font-family: 'Tiempos Text';
                            src: local('Tiempos Text');
                        }

                        .chat-message {
                            # font-family: 'Charter', 'Georgia', 'Cambria', 'Times New Roman', serif;
                            font-family: "__tiempos_b6f14e, tiempos_Fallback_b6f14e, ui-serif, Georgia, Cambria, Times New Roman, Times, serif",

                            # font-weight: 400;
                            # font-size: 16px;
                            # line-height: 1.6;
                            # color: rgb(17, 24, 28);
                            # letter-spacing: -0.011em;
                        }
                    </style>
                """, unsafe_allow_html=True)

    @staticmethod
    def render_title():
        st.markdown("""
            <style>
                /* Minimal header */
                .stApp > header {
                    display: none;  /* Hide default header */
                }

                .app-header {
                    font-size: 2rem;
                    font-family: 'Tiempos Text', 'Charter', 'Georgia', 'Cambria', 'Times New Roman', serif;
                    color: var(--text-primary);
                    padding: 0rem 35rem;
                    # border-bottom: 1px solid var(--border-color);
                    # background: white;  
                    font-weight: 500;
                    text-align: center;
                    position: fixed;
                    top: 0;
                    bottom:0;

                }
            </style>
            <div class="app-header">Claude</div>
            """, unsafe_allow_html=True)

    @staticmethod
    def render_chat_history_area():
        st.markdown("""
            <style>
                .chat-history {
                    height: calc(100vh - 180px);
                    overflow-y: auto;
                    padding: 1rem;
                    margin-bottom: 1rem;
                }

                .chat-message {
                    margin: 0.5rem 0;
                    padding: 0.5rem;
                    max-width: 90%;
                }

                .user-message {
                    margin-left: auto;
                    color: var(--text-primary);
                }

                .assistant-message {
                    margin-right: auto;
                    color: var(--text-primary);
                }
            </style>
        """, unsafe_allow_html=True)



class OmniAIChatApp(OmniMixin):

    def __init__(self,config_path:Optional[Path]=None):
        self.config = AppConfig.load_from_file(config_path) if config_path else AppConfig.get_default_config()
        self.theme = ModernUITheme()
        self.ui_manager=UIManager(config=self.config)
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

            col1, col2 = st.columns([53,47],gap='small')
            self.chat_col = col1.container()
            self.main_col2_tab1,self.main_col2_tab2 = col2.tabs(["Artifact","Settings"])
            self.artifact_col = self.main_col2_tab1.container(height=self.config.ARTIFACT_COLUMN_HEIGHT,border=True)

            with self.chat_col:
                self.handle_chat_history_and_stream_component()
                self.handle_chat_and_feature_component()


    def handle_chat_and_feature_component(self):
        chat_and_feature_container = st.container()
        with chat_and_feature_container:
            chat_input_and_upload_component = st.container()
            features_component = self.main_col2_tab2.container()

        with chat_input_and_upload_component:
            self.chat_holder = st.container()

            col1, col2 = self.chat_holder.columns([6, 1], gap='small',vertical_alignment='bottom')

            with col1:
                if query := st.text_area(placeholder="How can Claude help you today?",
                                         label="UserQueryInput",
                                         label_visibility='hidden',
                                         height=68):
                    st.session_state.query = query
                    self.current_query = query



            with col2.popover("",icon=":material/attach_file_add:"):
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
                chatbot_instance = self.create_chat_instance(selected_model,system_prompt)
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
            self.start_action()


    def handle_chat_history_and_stream_component(self):
        self.history_and_stream_area = st.container(height=420)

        with self.history_and_stream_area:
            self.history_part = st.sidebar.container()
            self.chat_message_col = st.container()


        with self.history_part.expander("Chat Conversation"):
            messages = st.session_state.messages.copy()
            nm = messages.copy()
            for i in range(0, len(messages)):
                if isinstance(messages[i], AIMessage) and (i+2)<len(messages):
                    nm[i]=messages[i+2]
            for message in nm[:-1]:
                if isinstance(message, UserMessage):
                    st.success(message.content)
                else:
                    div_content = f"""<div class='chat-message'>{message.content}</div>"""
                    st.markdown(div_content,unsafe_allow_html=True)

    def handle_selection_container(self):
        # sc1, sc2, sc3, sc4,sc5 = st.columns([1,1,1,1,1], gap='small')
        s1,s11 = st.columns([1,1],gap='small')
        s2,s21 = st.columns([1,1],gap='small')
        s3,s31 = st.columns([1,1],gap='small')
        s4,s41 = st.columns([1,1],gap='small')

        with s1.popover('Model',icon=":material/model_training:"):
            st.success('Available Models')
            models = list(self.config.MODELS_TITLE_MAP.keys()) + self.config.AVAILABLE_MODELS
            selected_model = st.radio(
                "Available Models",
                label_visibility='hidden',
                options=models
            )
            if selected_model not in self.config.AVAILABLE_MODELS:
                selected_model = self.config.MODELS_TITLE_MAP.get(selected_model, self.config.AVAILABLE_MODELS[0])

        with s2.popover('TaskType',icon=":material/psychology:"):
            st.success('TaskType')
            agent_type = st.radio("TaskType", self.config.AGENT_TYPES,
                                  label_visibility="hidden",
                                  key="agent_type",
                                  )
            if st.session_state.agent_type is None or st.session_state.agent_type != agent_type:
                st.session_state.agent_type = agent_type


        with s3.popover("Style",icon=":material/palette:"):
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


        with s4.popover("Agents",icon=":material/engineering:"):
            st.success("Agents")
            agents = ['None',self.config.AGENTS]
            selected_agent = st.radio(
                    "Available Agents",
                    label_visibility='hidden',
                    options=agents,
                help="Upcoming"
                )

        with st.popover("Experiments",icon=":material/experiment:"):
            st.subheader("Advanced Settings")
            st.button("Save Settings", key="save_settings")


        s11.success(selected_model)
        s21.success(agent_type)
        s31.success(prompt_name)
        s41.success(selected_agent)

        return selected_model



    def start_action(self):
        # self.handle_chat_history_rendering()
        self.handle_chat_input_and_stream()


    def handle_chat_input_and_stream(self):
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
                    st.session_state.chat_content=chat_content
                    format_content = f"""<div class='chat-message'>{chat_content}</div>"""
                    self.chat_placeholder.markdown(format_content,unsafe_allow_html=True)
                else:
                    artifact_content += cleaned_chunk
                    artifact_content = clean_text(artifact_content)
                    st.session_state.artifact_content=artifact_content
                    self.artifact_placeholder.code(artifact_content)


        # Process the stream until complete
        while generation_flag:
            process_stream()

        # Final render of both areas
        if chat_content:
            self.chat_placeholder.markdown(chat_content,unsafe_allow_html=True)
        if artifact_content:
            self.artifact_placeholder.code(artifact_content,unsafe_allow_html=True)

    def run(self):
        self.ui_manager.render_sidebar()
        self.render_chat_interface()

    def get_system_prompt(self, agent_type):
        if agent_type == "AIResearcher":
            return REASONING_SBS_PROMPT
        else:
            return WORKING_SYSTEM_PROMPT1

    def add_time_and_artifact_to_system_prompt(self, system_prompt):
        return BasePrompt.TODAY_DATE + system_prompt + "\n" + BasePrompt.ARTIFACT


if __name__ == '__main__':
    app = OmniAIChatApp()
    app.run()
