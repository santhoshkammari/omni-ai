from src.main.base import st, OmniCore
from typing import List, Tuple, Generator

from src.main.const import WORD_LLAMA_DIM
from src.main.features import PdfHandler
from src.main.features.feature_main import FeatureHandlerMain


class OmniMixin:
    @staticmethod
    def create_chat_instance(model: str,system_prompt) -> OmniCore:
        return OmniCore(model=model,system_prompt = system_prompt)

    @staticmethod
    def get_chat_response(chatbot: OmniCore, agent_type:str, query: str, web_search: bool = False) -> Generator:
        handler = FeatureHandlerMain(chatbot=chatbot, agent_type=agent_type, query=query,web_search=web_search)
        return handler.generate()

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

                if artifact_placeholder_markdown_flag:
                    artifact_placeholder.markdown(artifact_content)
                else:
                    artifact_placeholder.code(artifact_content)
        return chat_content, artifact_content

    @staticmethod
    def handle_files(query, file_content, file_extension):
        if file_extension=="pdf":
            handler = PdfHandler(file_content=file_content,
                                 word_llama_dim=WORD_LLAMA_DIM)
            context = handler.run(query,k=5)
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
        artifact_content = artifact_content.replace("```python", "")
        # artifact_content = artifact_content.replace("python", "")
        artifact_content = artifact_content.replace("```", "")
        artifact_content = artifact_content.replace("<code_or_keypoints>", "")
        artifact_content = artifact_content.replace("<code_or", "")
        artifact_content = artifact_content.replace("code_or", "")
        artifact_content = artifact_content.replace("_keypoints>", "")
        return artifact_content
