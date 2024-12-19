import streamlit as st
from pathlib import Path
from config.app_config import AppConfig
from components.chat_interface import ChatInterface
from components.model_settings import ModelSettings
from components.styles import AppStyles
from services.chat_service import ChatService
from services.model_service import ModelService


def init_session_state(config: AppConfig):
    if "config" not in st.session_state:
        st.session_state.config = config

    for key, value in config.default_states.items():
        if key not in st.session_state:
            st.session_state[key] = value


def main():
    st.set_page_config(
        page_title="AI Chat Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    config = AppConfig.load_from_file(Path("config.json"))
    init_session_state(config)

    AppStyles.apply()

    model_service = ModelService()
    chat_service = ChatService(model_service)

    model_settings = ModelSettings()
    chat_interface = ChatInterface(
        on_submit=lambda prompt: chat_service.handle_chat(prompt)
    )

    # Render UI
    model_settings.render()

    col1, col2 = st.columns([6, 4])

    with col1:
        chat_interface.render()

    with col2:
        st.subheader("Artifact")
        if st.session_state.artifact_content:
            st.code(st.session_state.artifact_content)


if __name__ == "__main__":
    main()