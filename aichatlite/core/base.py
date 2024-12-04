import streamlit as st

from ailitellm import yieldai
from .prompts import Prompts


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
        query = self._add_system_prompt(query)
        for resp in yieldai(messages_or_prompt=query):
            if resp:
                yield resp

    def print_stream(self,query,web_search = False):
        for x in self.generator(query,web_search):
            print(x,end= "",flush=True)

    def _add_system_prompt(self, query):
        user_query = Prompts.QUERY_PROMPT.format(query=query)
        return [
            {"role":"system","content":self.system_prompt},
            {"role":"user","content":user_query}
        ]

    def invoke(self,query,web_search=False):
        return self.generator(query)