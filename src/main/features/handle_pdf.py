import io
import re
from pathlib import Path
from typing import List

import PyPDF2
from wordllama import WordLlama


class PdfHandler:
    def __init__(self, file_path: str = None, file_content = None):
        self.file_path = file_path
        self.file_content = file_content
        self._validate()
        self.word_llama = WordLlama.load(dim=1024)

    def get_pdf_content(self):
        reader = PyPDF2.PdfReader(io.BytesIO(self.file_content))
        num_pages = len(reader.pages)
        content = ""
        for page in range(num_pages):
            content += reader.pages[page].extract_text()
        return content

    def run(self,query,k):
        pdf_text = self.get_pdf_content()
        relevant_chunks: List[str] = self.search_in_pdf(query, pdf_text,k)
        return "\n".join(relevant_chunks)

    def _validate(self):
        if self.file_path is None and self.file_content is None:
            raise ValueError("Either file_path or file_content must be provided.")

    def search_in_pdf(self, query, pdf_text,k):
        chunks = self.get_chunks(pdf_text)
        if len(chunks)>2:
            result = self.get_top_k(query=query,k = k,chunks=chunks)
        else:
            return chunks if chunks else [""]
        return result

    def get_chunks(self, pdf_text):
        chunks = re.split(r'(?<=[.])\s+', pdf_text)
        return chunks

    def get_top_k(self, query=None, k=None, chunks=None):
        return self.word_llama.topk(query,chunks,k)