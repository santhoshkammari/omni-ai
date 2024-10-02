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


if __name__ == '__main__':
    chatbot = OmniAIChat()
    chatbot.print_stream("give me python code to add two numpy arrays sum ")


