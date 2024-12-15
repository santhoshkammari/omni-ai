from typing import Literal

from ezyagent.core._types._huggingface import HFModelType
from .base import BaseSearch
from ..agents.compression_agent import CompressionAgent

try:
    from visionlite import vision
except:
    pass

class ArxivSearch(BaseSearch):
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
            enhanced_query = query + " arxiv result"
            self._fetch_result = vision(enhanced_query)
        except:
            self._fetch_result = "No results Found"
        return self._fetch_result