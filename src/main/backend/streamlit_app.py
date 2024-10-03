import streamlit as st
import requests
import json

# FastAPI endpoint
API_URL = "http://localhost:8888/api/chat"


def get_chat_response(query: str, web_search: bool = False):
    response = requests.post(API_URL, json={"query": query, "web_search": web_search}, stream=True)
    return response.iter_lines()


def main():
    st.title("AI Chat Interface")

    # Create a two-column layout
    col1, col2 = st.columns([2, 1])

    # Initialize chat history and artifacts
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "artifacts" not in st.session_state:
        st.session_state.artifacts = []

    with col1:
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if query := st.chat_input("What would you like to ask?"):
            # Display user message
            st.chat_message("user").markdown(query)
            st.session_state.messages.append({"role": "user", "content": query})

            # Get AI response
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                current_artifact = ""
                in_artifact = False
                artifact_count = len(st.session_state.artifacts)

                for chunk in get_chat_response(query):
                    if chunk:
                        data = json.loads(chunk.decode())
                        if "content" in data:
                            content = data["content"]

                            # Check for artifact area start/end
                            if "artifact" in content:
                                in_artifact = True
                                content = content.replace("<artifact_area>", "")
                                artifact_count += 1
                                full_response += f"[Artifact {artifact_count}]"
                            elif "</" in content:
                                in_artifact = False
                                content = content.replace("</artifact_area>", "")
                                if current_artifact:
                                    st.session_state.artifacts.append(current_artifact.strip())
                                    current_artifact = ""

                            # Add content to appropriate place
                            if in_artifact:
                                current_artifact += content
                            else:
                                full_response += content

                            message_placeholder.markdown(full_response + "▌")

                # Final update
                message_placeholder.markdown(full_response)
                if current_artifact:  # In case the last artifact wasn't closed
                    st.session_state.artifacts.append(current_artifact.strip())

            # Add AI response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})

    with col2:
        st.header("Artifacts")
        for i, artifact in enumerate(st.session_state.artifacts, 1):
            with st.expander(f"Artifact {i}"):
                st.code(artifact)


if __name__ == "__main__":
    main()