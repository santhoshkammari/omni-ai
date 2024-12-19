import anthropic
from ailitellm import OpenAI
from typing import Generator, Dict


class ModelService:
    def __init__(self,client):
        self.client = client or OpenAI()

    def generate_response(
        self,
        prompt: str,
        system_prompt: str,
        params: Dict
    ) -> Generator:
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        response = self.client.messages.create(
            model=st.session_state.selected_model,
            messages=messages,
            max_tokens=params["max_tokens"],
            temperature=params["temperature"],
            top_p=params["top_p"],
            stream=True
        )

        for chunk in response:
            if chunk.delta.text:
                yield chunk.delta.text