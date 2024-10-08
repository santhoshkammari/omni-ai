import os
import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

# Log in to huggingface and grant authorization to huggingchat
from dotenv import load_dotenv
load_dotenv()
from src.main.prompts import Prompts
EMAIL = os.getenv("HUGGINGFACE_EMAIL")
PASSWD = os.getenv("HUGGINGFACE_PASSWD")

class OmniCore:
    def __init__(self,model = 0,system_prompt = ""):
        self.cookies = self.setup_login()
        self.system_prompt = system_prompt
        self.DEFAULT_MODELS = [
            'meta-llama/Meta-Llama-3.1-70B-Instruct',
                               'CohereForAI/c4ai-command-r-plus-08-2024',
                               'Qwen/Qwen2.5-72B-Instruct',
                               'meta-llama/Llama-3.2-11B-Vision-Instruct',
                               'NousResearch/Hermes-3-Llama-3.1-8B',
                               'mistralai/Mistral-Nemo-Instruct-2407',
                               'microsoft/Phi-3.5-mini-instruct'
                               ]
        self.current_model = model
        self.chatbot  = self.setup_chatbot()


    def setup_login(self):
        cookie_path_dir = "cookies/"  # NOTE: trailing slash (/) is required to avoid errors
        sign = Login(EMAIL, PASSWD)
        cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)
        return cookies

    def setup_chatbot(self):
        chatbot = hugchat.ChatBot(cookies=self.cookies.get_dict(),
                                  default_llm=self.current_model,
                                  system_prompt=self.system_prompt)
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
        return Prompts.QUERY_PROMPT.format(query=query)
        # return query

    def invoke(self,query,web_search=False):
        res = self.chatbot.chat(query,web_search=web_search)
        result = res.wait_until_done()
        return result

if __name__ == '__main__':
    chatbot = OmniCore()
    chatbot.print_stream("give me python code to add two numpy arrays sum ")

from hugchat.types.model import Model

