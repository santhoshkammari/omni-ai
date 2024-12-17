from parselite import parse, FastParser
from searchlite import google, bing
from wordllama import WordLlama

llm = WordLlama.load()
import time

def vision(query,k=1,max_urls=5,animation=False,
           allow_pdf_extraction=True,
           allow_youtube_urls_extraction=False
           ):
    start_time = time.time()
    urls = google(query, max_urls=max_urls, animation=animation)
    urls_time = time.time() - start_time

    start_time = time.time()
    contents = parse(urls, allow_pdf_extraction=allow_pdf_extraction,
                     allow_youtube_urls_extraction=allow_youtube_urls_extraction)
    parse_time = time.time() - start_time

    start_time = time.time()
    res = llm.topk(query, llm.split("".join(contents)), k=k)
    llm_time = time.time() - start_time

    updated_res = "\n".join(res) + "\n\nURLS:\n" + "\n".join(urls)
    print(
                  f"\n\nTime taken for URLs: {urls_time:.2f} seconds\n" + \
                  f"Time taken for parsing: {parse_time:.2f} seconds\n" + \
                  f"Time taken for LLM: {llm_time:.2f} seconds")


if __name__ == '__main__':
    res = vision("pushpa 2 release date? wikipedia result", k=5)
