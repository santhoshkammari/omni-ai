from .handle_google_searchai import *
from .handle_google_searchai import deep_google_search,google_searchai
class FeatureHandlerMain:
    def __init__(self, chatbot, agent_type, query, web_search,system_prompt=""):
        self.chatbot = chatbot
        self.agent_type = agent_type
        self.query = query
        self.web_search = web_search
        self.system_prompt = system_prompt

    def generate(self):
        if self.agent_type == "QuestionAnswer":
            return self.chatbot.generator(self.query,
                                          system_prompt=self.system_prompt)
        elif self.agent_type == "Reasoning":
            return self.chatbot.generator(self.query,
                                         system_prompt=self.system_prompt)
        elif self.agent_type in ["GoogleSearchAI","DeepGoogleSearchAI"]:
            google_results = google_searchai(self.query) if self.agent_type=="GoogleSearchAI" else deep_google_search(self.query)
            enhanced_query = (f"Google Results for {self.query} is {google_results}"
                              f"\n\n Now based on google results answer {self.query}"
                              f"Start by saying Using Google Results or Google results not Found"
                              f"and continue your response")
            return self.chatbot.generator(enhanced_query,
                                            system_prompt=self.system_prompt)
        else:
            return "None"
