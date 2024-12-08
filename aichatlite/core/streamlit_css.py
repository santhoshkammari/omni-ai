from .core import st


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
                            font-family: 'Tiempos Text', 'Charter', 'Georgia', 'Cambria', 'Times New Roman', serif;
                            font-weight: 400;
                            font-size: 18px;
                            # line-height: 1.6;
                            color: rgb(17, 24, 28);
                            letter-spacing: -0.011em;
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