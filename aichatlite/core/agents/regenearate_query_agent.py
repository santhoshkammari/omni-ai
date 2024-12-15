import asyncio

from ezyagent.core._types._huggingface import HFModelType
from ezyagent import HFAgent

class QueryReGenerator:
    def __init__(self,model: HFModelType = "huggingface:Qwen/Qwen2.5-72B-Instruct"):
        self._model = model

    def regenerate(self,ctx:str|list=""):
        if isinstance(ctx,list):
            ctx = ", ".join(ctx)

        agent = HFAgent(model=self._model)(
            "Your are query regenerator,"
            "Your task is to regenerate the query as the query generated"
            "previously is not valid / no good results found in google search"
            "so based on the provided [CONTEXT] ( which is the previous"
            "queries that are failed , generate the new query [NEW_QUERY]"
            "Example:"
            "[CONTEXT]\nwhat is lates tranformers news, what transformers introducted newly\n"
            "[NEW_QUERY]new features introduced in transformers \n"
        )
        res = asyncio.run(agent(f"[CONTEXT]\n{ctx}\n[NEW_QUERY]")).content
        res = res.replace("[NEW_QUERY]", "").strip()
        return res