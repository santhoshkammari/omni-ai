from typing import Literal

from ezyagent.core._types._huggingface import HFModelType
from parselite import parse
from wordllama import WordLlama

from .base import BaseSearch
from ..agents.compression_agent import CompressionAgent

try:
    from visionlite import vision
except:
    pass
class YouTubeSearch(BaseSearch):
    def __init__(
        self,
        name: str,
        model: HFModelType = "huggingface:Qwen/Qwen2.5-72B-Instruct",
        compressor: CompressionAgent = None,
        compress_type: Literal['full', 'chunk'] = 'full'
    ):
        self.llm = WordLlama.load()
        super().__init__(
            name=name,
            model=model,
            compressor=compressor,
            compress_type=compress_type
        )

    def fetch(self, query: str):
        try:
            enhanced_query = query + " youtube result"
            from youtube_search import YoutubeSearch
            results = YoutubeSearch(enhanced_query, max_results=3)
            video_ids = [r['id'] for r in results.videos]
            urls = [f"https://www.youtube.com/watch?v={video_id}" for video_id in video_ids]
            contents = parse(urls, allow_pdf_extraction=True,
                             allow_youtube_urls_extraction=True)
            res = self.llm.topk(query, self.llm.split("".join(contents)),k=5)
            self._fetch_result = "\n".join(res) + "\n\nURLS:\n" + "\n".join(urls)
        except:
            self._fetch_result = "No results Found"
        return self._fetch_result