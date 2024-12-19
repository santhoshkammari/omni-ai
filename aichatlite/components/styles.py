import streamlit as st


class AppStyles:
    @staticmethod
    def apply():
        st.markdown("""
            <style>
                .stApp {
                    background-color: #FAFAFA;
                }

                .chat-message {
                    padding: 1rem;
                    border-radius: 0.5rem;
                    margin-bottom: 1rem;
                    border: 1px solid #E0E0E0;
                }

                .user-message {
                    background-color: #F0F7FF;
                }

                .assistant-message {
                    background-color: #FFFFFF;
                }

                .artifact-area {
                    background-color: #F5F5F5;
                    padding: 1rem;
                    border-radius: 0.5rem;
                    font-family: monospace;
                }
            </style>
        """, unsafe_allow_html=True)
