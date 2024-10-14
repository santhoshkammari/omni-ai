from src.main.base import st


class OmniAiChatCSS:
    @staticmethod
    def render_main():
        st.markdown("""
            <style>
                #root > div:nth-child(1) > div > div > div > div > section > div {
                    padding-top: 1;
                }
                .main {
                    overflow: hidden;
                }
                .stApp {
                    height: 100vh;
                }
                [data-testid="stAppViewContainer"] {
                    height: 100vh;
                    overflow: hidden;
                }
                [data-testid="stVerticalBlock"] {
                    # height: calc(100vh - 4rem);  /* Adjust if you have a header */
                    overflow-y: auto;
                }
                .block-container {
                    padding-top: 0.5rem;
                    padding-bottom: 0.5rem;
                    padding-left: 0.5rem;
                    padding-right:0.5rem;
                    margin-right:0;
                    margin-top:0;
                    margin-left:0;
                    margin-bottom:0;
                }
                .stSidebar {
                    margin-top: 0;
                }
                .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
                .css-1d391kg {
                    padding-top: 1rem;
                }
            </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_title():
        st.markdown("""
                        <style>
                        .stApp > header {
                            background-color: transparent;
                            height: auto !important;
                            padding-top: 0 !important;
                            padding-bottom: 0 !important;
                        }
                        .small-title {
                            font-size: 24px;
                            # color: #4a4a4a;
                            font-weight: 600;
                            text-align: center;
                            padding: 5px 0;
                            margin: 0;
                            # background-color: #f0f0f0;
                        }
                        </style>
                        """, unsafe_allow_html=True)

        st.markdown("<h1 class='small-title'>OmniAI Chat Interface</h1>", unsafe_allow_html=True)

        # Custom CSS

        st.write("""
                            <style>
                            div[data-baseweb="select"] > div {
                                width: 300px !important;
                            }

                            </style>
                            """, unsafe_allow_html=True)

    @staticmethod
    def render_chat_history_area():
        st.markdown("""
                        <style>
                        .chat-history {
                             height: 65vh;
                    overflow-y: auto;
                    overflow-x: hidden;
                    white-space: normal;
                    word-wrap: break-word;
                    margin-right:0
                        }
                        </style>
                    """, unsafe_allow_html=True)



