import streamlit as st
import requests
import json

# FastAPI endpoint
API_URL = "http://localhost:8888/api/chat"

def get_chat_response(query: str, web_search: bool = False):
    response = requests.post(API_URL, json={"query": query, "web_search": web_search}, stream=True)
    return response.iter_lines()

def main():
    st.set_page_config(layout="wide")

    # Custom CSS for Claude-like layout
    st.markdown("""
    <style>
    .stApp {
        max-width: 100%;
        padding-top: 0 !important;
    }
    .main {
    display: flex;
    height: 100vh;
    flex-direction: column;
    margin-top: 0;
    padding-top: 0;
    }

    .chat-container {
        display: flex;
        flex-grow: 1;
        overflow: hidden;
        padding-top: 1rem;
    }
    .chat-column {
        flex: 2;
        display: flex;
        flex-direction: column;
        padding: 0 1rem;
        overflow-y: auto;
    }
    .artifact-column {
        flex: 1;
        padding: 0 1rem;
        background-color: #f0f2f6;
        border-left: 1px solid #ddd;
        overflow-y: auto;
    }
    .chat-messages {
        flex-grow: 1;
        overflow-y: auto;
        margin-bottom: 1rem;
    }
    .chat-input {
        position: sticky;
        bottom: 0;
        background-color: white;
        padding: 1rem 0;
    }
    .stTextInput > div > div > input {
        border-radius: 20px;
        border: 1px solid #ddd;
        padding: 0.5rem 1rem;
    }
    .stMarkdown {
        max-width: 100%;
    }
    .stTitle {
        margin-top: 0;
        padding-top: 0;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    # Create two columns for chat and artifacts
    chat_col, artifact_col = st.columns([2, 1])

    with chat_col:
        st.markdown('<div class="chat-column">', unsafe_allow_html=True)
        st.title("AI Chat Interface")

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages
        st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        st.markdown('</div>', unsafe_allow_html=True)

        # Chat input at the bottom of the chat column
        st.markdown('<div class="chat-input">', unsafe_allow_html=True)
        query = st.text_input("What would you like to ask?", key="chat_input")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with artifact_col:
        st.markdown('<div class="artifact-column">', unsafe_allow_html=True)
        st.header("Artifacts")
        artifact_placeholders = []
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if query:
        # Display user message
        with chat_col:
            st.chat_message("user").markdown(query)
        st.session_state.messages.append({"role": "user", "content": query})

        # Get AI response
        with chat_col:
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                current_artifact = ""
                in_artifact = False
                artifact_count = len(st.session_state.get("artifacts", []))
                artifact_tokens = []
                for id, chunk in enumerate(get_chat_response(query)):
                    if chunk:
                        data = json.loads(chunk.decode())
                        if "content" in data:
                            content = data["content"]

                            if id > 4:
                                artifact_tokens = artifact_tokens[1:] + [content]
                            else:
                                artifact_tokens.append(content)

                            artifact_area = "".join(artifact_tokens)

                            # Check for artifact area start/end
                            if "<artifact_area>" in artifact_area:
                                in_artifact = True
                                content = content.replace("<artifact_area>", "")
                                artifact_count += 1
                                full_response += f"[Artifact {artifact_count}]"
                                with artifact_col:
                                    artifact_placeholders.append(st.empty())
                            elif "</artifact_area>" in artifact_area:
                                in_artifact = False
                                content = content.replace("</artifact_area>", "")
                                if current_artifact:
                                    if "artifacts" not in st.session_state:
                                        st.session_state.artifacts = []
                                    st.session_state.artifacts.append(current_artifact.strip())
                                    current_artifact = ""

                            # Add content to appropriate place
                            if in_artifact:
                                current_artifact += content
                                artifact_placeholders[-1].code(current_artifact + "▌")
                            else:
                                full_response += content

                            message_placeholder.markdown(full_response + "▌")

                # Final update
                message_placeholder.markdown(full_response)
                if current_artifact:  # In case the last artifact wasn't closed
                    if "artifacts" not in st.session_state:
                        st.session_state.artifacts = []
                    st.session_state.artifacts.append(current_artifact.strip())

        # Add AI response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
