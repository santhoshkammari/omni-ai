from .handle_google_searchai import *
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
                                          system_prompt = self.system_prompt)
        else:
            return "None"