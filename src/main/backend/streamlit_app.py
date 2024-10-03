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

    # Create two columns for chat and artifacts with a 50/50 width split
    chat_col, artifact_col = st.columns([1, 1])

    with chat_col:
        st.title("AI Chat Interface")

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "artifacts" not in st.session_state:
            st.session_state.artifacts = []

        # Display chat messages
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.write(f"**You:** {message['content']}")
            else:
                st.write(f"**AI:** {message['content']}")

        # Input text box for user query
        query = st.text_input("Ask your question here:")

        if query:
            # Display user message
            st.write(f"**You:** {query}")
            st.session_state.messages.append({"role": "user", "content": query})

            # Initialize artifact and token buffer
            artifact_count = len(st.session_state.artifacts)
            current_artifact = ""
            in_artifact = False
            artifact_tokens = []

            # Stream AI response and handle artifacts
            for chunk in get_chat_response(query):
                if chunk:
                    data = json.loads(chunk.decode())
                    if "content" in data:
                        content = data["content"]

                        # Buffering tokens to identify artifacts
                        if len(artifact_tokens) > 4:
                            artifact_tokens = artifact_tokens[1:] + [content]
                        else:
                            artifact_tokens.append(content)

                        artifact_area = "".join(artifact_tokens)

                        # Check for artifact start/end
                        if "<artifact_area>" in artifact_area:
                            in_artifact = True
                            content = content.replace("<artifact_area>", "")
                            artifact_count += 1
                            st.write(f"\n[Artifact {artifact_count}]")
                        elif "</artifact_area>" in artifact_area:
                            in_artifact = False
                            content = content.replace("</artifact_area>", "")
                            if current_artifact:
                                st.session_state.artifacts.append(current_artifact.strip())
                                current_artifact = ""

                        # Handle content display
                        if in_artifact:
                            current_artifact += content
                        else:
                            st.write(content)

            # Append response to chat history
            st.session_state.messages.append({"role": "assistant", "content": 'Response streamed above'})

    # Artifacts section on the right
    with artifact_col:
        st.title("Artifacts")
        if st.session_state.artifacts:
            for i, artifact in enumerate(st.session_state.artifacts, 1):
                st.write(f"**Artifact {i}:**")
                st.code(artifact)

if __name__ == "__main__":
    main()
