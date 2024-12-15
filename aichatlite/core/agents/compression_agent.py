from typing import List

from ezyagent import AgentPool
from ezyagent.core._types._huggingface import HFModelType
from wordllama import WordLlama

_COMPRESSION_PROMPT = """You are a highly skilled content compression expert. 
Your task is to compress the given text while maintaining its original meaning and as much detail as possible. Use concise language and avoid any unnecessary words. 
The compressed text should be as short as possible without losing the core message. 
Provide only the compressed text in your response.
"""


class CompressionAgent:
    """
    A class to handle text compression using a specified model and agent pool.

    Methods:
    --------
    compress(tasks_or_queries: List | str) -> List[str] | str:
        Compresses a single string or a list of strings. Returns a compressed string if a single string is provided,
        otherwise returns a list of compressed strings.

    chunk_based_compress(content: str) -> str:
        Compresses a large string by splitting it into chunks, compressing each chunk, and then joining the results.
        Returns a single compressed string.
    """

    def __init__(self, model: HFModelType | None = None):
        self.pool = AgentPool(model=model,
                              system_prompt=_COMPRESSION_PROMPT)

    def compress(self, tasks_or_queries: List | str) -> List[str] | str:
        if isinstance(tasks_or_queries, str):
            updated_tasks_or_queries = [tasks_or_queries]
        else:
            updated_tasks_or_queries = tasks_or_queries
        results = self.pool.run(updated_tasks_or_queries)
        contents = [r.content for r in results]
        return contents[0] if isinstance(tasks_or_queries, str) else contents

    def chunk_based_compress(self, content: str) -> List[str] | str:
        llm = WordLlama.load()
        tasks = llm.split(content)
        results = self.pool.run(tasks)
        contents = [r.content for r in results]
        return "\n".join(contents)
