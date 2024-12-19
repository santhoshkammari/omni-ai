from ailitellm import OpenAI, ailite_model, HFModelType
from typing import Generator, Dict, List


class ModelService:
    def __init__(self,
                 default_model:HFModelType|str='NousResearch/Hermes-3-Llama-3.1-8B',
                 client=None):
        self.default_model:str =default_model
        self.client = client or OpenAI()

    def gen(
        self,
        prompt: str,
        system_prompt: str="",
        params: Dict={},
        model: str=None,
        ctx: List[Dict] = []
    ) -> Generator:
        messages = [
                       {
                           "role": "system",
                           "content": system_prompt
                       }
                   ] + ctx + [
                       {
                           "role": "user",
                           "content": prompt
                       }
                   ]

        response = self.client.chat.completions.create(
            model=model or self.default_model,
            messages=messages,
            max_tokens=params.get("max_tokens", 4000),
            temperature=params.get("temperature",0),
            top_p=params.get("top_p",0.95),
            stream=True
        )

        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    def chat(
        self,
        prompt: str,
        system_prompt: str="",
        model: str=None,
        params: Dict={},
        ctx: List[Dict] = []
    ) -> Generator:

        return self.gen(prompt=prompt, system_prompt=system_prompt, params=params, ctx=ctx, model=model)

if __name__ == '__main__':
    model = ModelService()
    for m in model.chat("hi"):
        print(m,flush=True)
