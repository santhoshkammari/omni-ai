import time

from .handle_google_searchai import *
from .handle_google_searchai import deep_google_search,google_searchai
class FeatureHandlerMain:
    def __init__(self, chatbot, agent_type, query, web_search,system_prompt="",
                 kb_data=""):
        self.chatbot = chatbot
        self.agent_type = agent_type
        self.query = query
        self.web_search = web_search
        self.system_prompt = system_prompt
        self.kb_data = kb_data  # Knowledge base data for reasoning agents

    def add_knowledge_base_to_query(self,kb_data=""):
        if kb_data:
            self.kb_data+=kb_data
            return f"\n\n### [KNOWLEDGE_BASE_DATA_START]:\n\n{self.kb_data} [KNOWLEDGE_BASE_DATA_END]\n\n" + f"Now Answer \n {self.query}"
        return self.query

    def generate(self,kb_data=""):
        if self.agent_type == "QuestionAnswer":
            query= self.add_knowledge_base_to_query(kb_data=kb_data)
            return self.chatbot.generator(query,
                                          system_prompt=self.system_prompt)
        elif self.agent_type == "Reasoning":
            return self.chatbot.generator(self.query,
                                         system_prompt=self.system_prompt)
        elif self.agent_type in ["GoogleSearchAI","DeepGoogleSearchAI"]:
            st = time.perf_counter()
            try:
                google_results = google_searchai(self.query) if self.agent_type=="GoogleSearchAI" else deep_google_search(self.query)
            except:
                google_results = "No Results Found in Google Search"
            et = time.perf_counter()
            gr_tt = et-st
            print(f'Google results Time taken : {gr_tt}s')
            enhanced_query = (f"Google Results for {self.query} is {google_results}"
                              f"\n\n Now based on google results answer {self.query}"
                              f"Start by saying Using Google Results or Google results not Found"
                              f"and continue your response")
            return self.chatbot.generator(enhanced_query,
                                            system_prompt=self.system_prompt)
        else:
            return "None"
