from .handle_google_searchai import *


from .handle_search_ai import handle_search_ai

class FeatureHandlerMain:
    def __init__(self, chatbot, agent_type, query, web_search,system_prompt=""):
        self.chatbot = chatbot
        self.agent_type = agent_type
        self.query = query
        self.web_search = web_search
        self.system_prompt = system_prompt

    def generate(self):
        match self.agent_type:
            case "QuestionAnswer":
                return self.chatbot.generator(self.query,
                                              system_prompt = self.system_prompt)
            case "FastSearchAI":
                return handle_search_ai(chatbot=self.chatbot, query=self.query, k=2)
            case "DeepSearchAI":
                return handle_search_ai(chatbot=self.chatbot, query=self.query, k=5)
            case "IntelligentSearchAI":
                return handle_search_ai(chatbot=self.chatbot, query=self.query, k=10)
            case _:
                return "None"
