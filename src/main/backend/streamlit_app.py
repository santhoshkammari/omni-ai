import streamlit as st
import requests
import json
from typing import List

# FastAPI endpoint
API_URL = "http://localhost:8888/api/chat"


def get_chat_response(query: str, web_search: bool = False):
    response = requests.post(API_URL, json={"query": query, "web_search": web_search}, stream=True)
    return response.iter_lines()


def display_message(role: str, content: str):
    with st.chat_message(role):
        st.markdown(content)


def main():
    st.title("AI Chat Interface")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        display_message(message["role"], message["content"])

    # Chat input
    if query := st.chat_input("What would you like to ask?"):
        # Display user message
        display_message("user", query)
        st.session_state.messages.append({"role": "user", "content": query})

        # Get AI response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for chunk in get_chat_response(query):
                if chunk:
                    data = json.loads(chunk.decode())
                    if "content" in data:
                        full_response += data["content"]
                        message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

        # Add AI response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    main()