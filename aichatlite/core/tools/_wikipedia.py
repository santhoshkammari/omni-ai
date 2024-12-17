import time
from typing import Literal

from ezyagent.core._types._huggingface import HFModelType
from .base import BaseSearch
from ..agents.compression_agent import CompressionAgent
from langchain_community.document_loaders import WikipediaLoader



class WikipediaSearch(BaseSearch):
    def __init__(
        self,
        name: str,
        model: HFModelType = "huggingface:Qwen/Qwen2.5-72B-Instruct",
        compressor: CompressionAgent = None,
        compress_type: Literal['full', 'chunk'] = 'full'
    ):
        super().__init__(
            name=name,
            model=model,
            compressor=compressor,
            compress_type=compress_type
        )

    def fetch(self, query: str):
        try:
            # enhance the query with "wikipedia result" for more accurate search
            enhanced_query = query + " wikipedia result"
            # self._fetch_result = vision(enhanced_query,k=5)
            docs = WikipediaLoader(query=enhanced_query,
                                                 load_max_docs=2).load()
            self._fetch_result = "\n".join([p.page_content for p in docs])
        except:
            self._fetch_result = "No results Found"
        return self._fetch_result













