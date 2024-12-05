from ..base import OmniCore
from visionlite import vision

class HandleSearchAI:
    def __init__(self,system_prompt=""):
        self.system_prompt = system_prompt

    def handle_search_ai(self,chatbot:OmniCore, query:str,k=1):
        context = vision(query,k=k,max_urls=5) # google search using chromedriver
        prompt = """
        <context>
        ### Search results:
        {context}
        </context>
        if context is empty , theh start by saying '# SEARCH RESULTS ARE EMPTY'
        user query: 
        
        {query}
        """.format(context=context, query=query)
        return chatbot.generator(prompt,system_prompt=self.system_prompt)

