from .stream_base import st


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
                    padding-top: 1rem;
                    padding-bottom: 1rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
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


