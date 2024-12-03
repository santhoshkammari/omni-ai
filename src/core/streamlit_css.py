from .base import st

class OmniAiChatCSS:
    @staticmethod
    def render_main():
        st.markdown("""
            <style>
                /* Anthropic-inspired color palette */
                :root {
                    --background-primary: #FAF9F7;
                    --text-primary: #1A1818;
                    --accent-color: #C16B47;
                    --border-color: #E5E5E5;
                    --sidebar-bg: #FFFFFF;
                }

                /* Global styles */
                .stApp {
                    background-color: var(--background-primary);
                    font-family: "SF Pro Display", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
                    height: 100vh;
                }

                /* Container adjustments */
                [data-testid="stAppViewContainer"] {
                    height: 100vh;
                    overflow: hidden;
                    background-color: var(--background-primary);
                }

                .block-container {
                    padding: 1rem;
                    max-width: 1200px;
                    margin: 0 auto;
                }

                /* Sidebar styling */
                .stSidebar {
                    background-color: var(--sidebar-bg);
                    border-right: 1px solid var(--border-color);
                }

                .stSidebar .block-container {
                    padding-top: 2rem;
                }

                /* Button styling */
                .stButton > button {
                    background-color: white;
                    color: var(--text-primary);
                    border: 1px solid var(--border-color);
                    border-radius: 8px;
                    padding: 0.5rem 1rem;
                    font-weight: 500;
                    transition: all 0.2s ease;
                }

                .stButton > button:hover {
                    background-color: #F5F5F5;
                    border-color: var(--accent-color);
                }

                /* Select box styling */
                .stSelectbox > div {
                    background-color: white;
                    border: 1px solid var(--border-color);
                    border-radius: 8px;
                }

                /* Chat input styling */
                .stTextInput > div > div > input {
                    background-color: white;
                    border: 1px solid var(--border-color);
                    border-radius: 8px;
                    padding: 0.75rem;
                }

                /* Chat message styling */
                [data-testid="stChatMessage"] {
                    background-color: white;
                    border: 1px solid var(--border-color);
                    border-radius: 12px;
                    padding: 1rem;
                    margin: 0.5rem 0;
                }

                /* Scrollbar styling */
                ::-webkit-scrollbar {
                    width: 6px;
                    height: 6px;
                }

                ::-webkit-scrollbar-track {
                    background: transparent;
                }

                ::-webkit-scrollbar-thumb {
                    background: #888;
                    border-radius: 3px;
                }

                ::-webkit-scrollbar-thumb:hover {
                    background: #666;
                }
            </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_title():
        st.markdown("""
            <style>
                /* Title styling */
                .stApp > header {
                    background-color: transparent;
                    height: auto !important;
                    padding: 1rem 0 !important;
                }

                .app-title {
                    font-size: 28px;
                    color: var(--text-primary);
                    font-weight: 600;
                    text-align: left;
                    padding: 1rem 0;
                    margin: 0;
                    letter-spacing: -0.02em;
                }

                /* Selector width adjustment */
                div[data-baseweb="select"] > div {
                    width: 300px !important;
                }
            </style>
            """, unsafe_allow_html=True)

        st.markdown("<h1 class='app-title'>OmniAI Chat Interface</h1>", unsafe_allow_html=True)

    @staticmethod
    def render_chat_history_area():
        st.markdown("""
            <style>
                .chat-history {
                    height: calc(100vh - 200px);
                    overflow-y: auto;
                    overflow-x: hidden;
                    padding: 1rem;
                    background-color: white;
                    border-radius: 12px;
                    border: 1px solid var(--border-color);
                }

                .chat-history > div {
                    max-width: 800px;
                    margin: 0 auto;
                }

                /* Message bubbles */
                .chat-message {
                    margin: 1rem 0;
                    padding: 1rem;
                    border-radius: 8px;
                    max-width: 80%;
                }

                .user-message {
                    background-color: #F0F0F0;
                    margin-left: auto;
                }

                .assistant-message {
                    background-color: white;
                    border: 1px solid var(--border-color);
                    margin-right: auto;
                }
            </style>
        """, unsafe_allow_html=True)