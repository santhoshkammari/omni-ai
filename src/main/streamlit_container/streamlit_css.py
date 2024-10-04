from .stream_base import st
class OmniAiChatCSS:
    @staticmethod
    def render_main():
        st.markdown("""
                                <style>
                                /* Remove top margin from main container */
                                .main .block-container {
                                    padding-top: 0rem;
                                    padding-bottom: 0rem;
                                    padding-left: 1rem;
                                    padding-right: 1rem;
                                }

                                /* Adjust header margins */
                                .main .block-container > div:first-child {
                                    margin-top: 0;
                                    padding-top: 1rem;
                                }

                                /* Remove extra padding from Streamlit elements */
                                .stApp {
                                    margin-top: -5rem;
                                    overflow: hidden;
                                }
                                .stSidebar {
                                    margin-top: 5rem;
                                }

                                .css-18e3th9 {
                                    padding-top: 0rem;
                                    padding-bottom: 0rem;
                                    padding-left: 1rem;
                                    padding-right: 1rem;
                                }

                                /* Ensure content starts at the top */
                                .css-1d391kg {
                                    padding-top: 1rem;
                                }
                                </style>
                                """, unsafe_allow_html=True)
