import json
import time
import streamlit as st
import requests

# FastAPI endpoint
API_URL = "http://localhost:8888/api/chat"

def get_chat_response(query: str, web_search: bool = False):
    response = requests.post(API_URL, json={"query": query, "web_search": web_search}, stream=True)
    return response.iter_lines()

# def data_stream():
#     data = "the sample query to test \n what is \n workds < artifact _area > and lets just see artend now back to nromal"
#     flag = True
#     for x in data.split(" "):
#         if x == 'artifact':
#             flag = False
#         elif x == 'artend':
#             flag = True
#
#         yield x, flag

def data_stream(query):
    flag = True
    for x in get_chat_response(query):
        if isinstance(x, bytes):
            x = json.loads(x.decode("utf-8")).get('content', "")
        if x == 'artifact':
            flag = not flag

        yield x, flag

def update_chat_col(generator, chat_placeholder, artifact_placeholder):
    ch,ap = "",""
    for item, flag in generator:
        if flag:
            ch+=item
            chat_placeholder.write(ch)
        else:
            ap+=item
            artifact_placeholder.write(ap)

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

        if st.button("Send"):
            st.session_state.messages.append({"role": "user", "content": query})
            response_generator = data_stream(query)
            chat_placeholder = st.empty()
            artifact_placeholder = artifact_col.empty()
            update_chat_col(response_generator, chat_placeholder, artifact_placeholder)

if __name__ == "__main__":
    main()