from src.main.features.handle_ai_research import AIResearcher
from .handle_google_searchai import *
class FeatureHandlerMain:
    def __init__(self, chatbot, agent_type, query, web_search):
        self.chatbot = chatbot
        self.agent_type = agent_type
        self.query = query
        self.web_search = web_search

    def generate(self):
        if self.agent_type == "QuestionAnswer":
            return self.chatbot.generator(self.query, web_search=self.web_search)
        elif self.agent_type == "Reasoning":
            ai_researcher = AIResearcher()
            return ai_researcher.generate_response(self.query,self.chatbot,web_search=self.web_search)
        elif self.agent_type == "GoogleSearchAI":
            return google_search_ai(self.query)
        elif self.agent_type == "SearchAI":
            return search_ai(self.query)
        elif self.agent_type == "GoogleSearch":
            return google_search(self.query)
        elif self.agent_type == "DeepGoogleSearch":
            return deep_google_search(self.query)

