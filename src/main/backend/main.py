import os

from hugchat import hugchat
from hugchat.login import Login
from configparser import ConfigParser

# Log in to huggingface and grant authorization to huggingchat
from dotenv import load_dotenv
load_dotenv()

config_parser = ConfigParser()
config_parser.read("/home/ntlpt59/MAIN/omni-ai/src/main/backend/config.ini")
EMAIL = os.getenv("HUGGINGFACE_EMAIL")
PASSWD = os.getenv("HUGGINGFACE_PASSWD")

class OmniAIChat:
    def __init__(self):
        self.cookies = self.setup_login()
        self.DEFAULT_MODELS = ['meta-llama/Meta-Llama-3.1-70B-Instruct',
                               'CohereForAI/c4ai-command-r-plus-08-2024',
                               'Qwen/Qwen2.5-72B-Instruct',
                               'meta-llama/Llama-3.2-11B-Vision-Instruct',
                               'NousResearch/Hermes-3-Llama-3.1-8B',
                               'mistralai/Mistral-Nemo-Instruct-2407',
                               'microsoft/Phi-3.5-mini-instruct'
                               ]
        self.chatbot  = self.setup_chatbot()


    def setup_login(self):
        cookie_path_dir = "./cookies/" # NOTE: trailing slash (/) is required to avoid errors
        sign = Login(EMAIL, PASSWD)
        cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)
        return cookies

    def setup_chatbot(self):
        chatbot = hugchat.ChatBot(cookies=self.cookies.get_dict(),
                                  default_llm=config_parser['MODEL_CONFIG'][
                                      'MODEL_NAME'])
        return chatbot


    def generator(self,query,web_search= False):
        """
        Generator function to stream responses from the chatbot.
        """
        query = self._add_system_prompt(query)
        for resp in self.chatbot.chat(
            query,
            stream=True,
            web_search=web_search
        ):
            if resp:
                yield resp['token']

    def print_stream(self,query,web_search = False):
        for x in self.generator(query,web_search):
            print(x,end= "",flush=True)

    def _add_system_prompt(self, query):
        """
        Enhances the user query with a system prompt that encourages structured thinking,
        comprehensive analysis, and formatted output with specific artifact areas for code.
        """
        system_prompt = f"""
        You are an AI assistant created by OmniAI. Approach each query with careful consideration and analytical thinking. When responding:

        1. Thoroughly analyze complex and open-ended questions, but be concise for simpler tasks.
        2. Break down problems systematically before providing final answers.
        3. Engage in discussions on a wide variety of topics with intellectual curiosity.
        4. For long tasks that can't be completed in one response, offer to do them piecemeal and get user feedback.
        5. Use markdown for code formatting.
        6. Wrap only the code or scripts in <artifact_area> tags. This includes:
           - Python code snippets
           - Complete scripts or functions
           - Any other executable code
           - Thought/ thinking pad or area
           
        7. Keep explanations, analyses, and non-code content outside of the <artifact_area> tags.
        8. Avoid unnecessary affirmations or filler phrases at the start of responses.
        9. Respond in the same language as the user's query.
        10. Do not apologize if you cannot or will not perform a task; simply state that you cannot do it.
        11. If asked about very obscure topics, remind the user at the end that you may hallucinate in such cases.
        12. If citing sources, inform the user that you don't have access to a current database and they should verify any citations.

        Original query: {query}

        Respond to this query following the guidelines above, ensuring only actual code is wrapped in <artifact_area> tags.
        """
        return system_prompt


if __name__ == '__main__':
    chatbot = OmniAIChat()
    chatbot.print_stream("give me python code to add two numpy arrays sum ")


