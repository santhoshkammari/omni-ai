try:
    from visionlite import vision
except:
    pass

def google_searchai(query,k=3,max_urls=5):
    return vision(
        query=query,
        k=k,
        max_urls=max_urls
    )

def deep_google_search(query,k=6,max_urls=10):
    return vision(
        query=query,
        k=k,
        max_urls=max_urls
    )

