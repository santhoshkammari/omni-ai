import os
import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

# Log in to huggingface and grant authorization to huggingchat
from dotenv import load_dotenv
load_dotenv()
from src.main.prompts import Prompts
from ailitellm import yieldai

class OmniCore:
    def __init__(self,model = 0,system_prompt = ""):
        self.system_prompt = system_prompt
        self.DEFAULT_MODELS = [
    "Qwen/Qwen2.5-72B-Instruct",
    "Qwen/QwQ-32B-Preview",
    "Qwen/Qwen2.5-Coder-32B-Instruct",
    "NousResearch/Hermes-3-Llama-3.1-8B",
    "microsoft/Phi-3.5-mini-instruct"
]
        self.current_model = model


    def generator(self,query,web_search= False):
        """
        Generator function to stream responses from the chatbot.
        """
        query = self._add_system_prompt(query)
        for resp in yieldai(messages_or_prompt=query):
            if resp:
                yield resp

    def print_stream(self,query,web_search = False):
        for x in self.generator(query,web_search):
            print(x,end= "",flush=True)

    def _add_system_prompt(self, query):
        """
        Enhances the user query with a system prompt that encourages structured thinking,
        comprehensive analysis, and formatted output with specific artifact areas for code.
        """
        user_query = Prompts.QUERY_PROMPT.format(query=query)
        return [
            {"role":"system","content":self.system_prompt},
            {"role":"user","content":user_query}
        ]
        # return query

    def invoke(self,query,web_search=False):
        res = self.chatbot.chat(query,web_search=web_search)
        result = res.wait_until_done()
        return result

if __name__ == '__main__':
    chatbot = OmniCore()
    chatbot.print_stream("give me python code to add two numpy arrays sum ")

from hugchat.types.model import Model

