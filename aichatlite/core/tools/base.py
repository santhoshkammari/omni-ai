import asyncio
from abc import ABC, abstractmethod
from typing import Literal

from ezyagent import HFAgent
from ezyagent.core._types._huggingface import HFModelType

from ..agents.compression_agent import CompressionAgent
from ..agents.regenearate_query_agent import QueryReGenerator


class BaseSearch(ABC):
    def __init__(
        self,
        name: str,
        model: HFModelType = "huggingface:Qwen/Qwen2.5-72B-Instruct",
        compressor: CompressionAgent = None,
        compress_type: Literal['full', 'chunk'] = 'full',
        query_regenerator: QueryReGenerator = None
    ):
        self._name: str = name
        self._model: HFModelType = model
        self._compressor = compressor
        self._compress_type = compress_type
        self._fetch_result: str | None = None
        self._compress_result: str | None = None
        self._query_regenerator = query_regenerator or QueryReGenerator()

    @property
    def name(self) -> str:
        return self._name

    @property
    def model(self) -> HFModelType:
        return self._model

    @property
    def compressor(self) -> CompressionAgent:
        return self._compressor

    @property
    def compress_type(self) -> Literal['full', 'chunk']:
        return self._compress_type

    @property
    def fetch_result(self) -> str | None:
        return self._fetch_result

    @property
    def compress_result(self) -> str | None:
        return self._compress_result


    @abstractmethod
    def fetch(self,query:str):
        pass

    def compress(self, query: str = None):
        compressor = self._compressor or CompressionAgent()

        match self._compress_type:
            case 'full':
                _func = compressor.compress
            case 'chunk':
                _func = compressor.chunk_based_compress
            case _:
                raise ValueError("Invalid compress type. Use 'full' or 'chunk'")

        content_to_compress = query or self._fetch_result
        if content_to_compress is None:
            raise ValueError("No content to compress")

        self._compress_result = _func(content_to_compress)

        return self._compress_result

    def new_query(self,ctx:str|list=""):
        res = self._query_regenerator.regenerate(ctx=ctx)
        return res


