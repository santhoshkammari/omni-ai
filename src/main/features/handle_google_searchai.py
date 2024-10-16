from inqs import google_search, deep_google_search, search_ai, google_search_ai


def google_search_ai(query):
    results = google_search_ai(query)
    for word in results.split(" "):
        yield word

def google_search(query):
    results = google_search(query)
    for word in results.split(" "):
        yield word


def deep_google_search(query):
    results = deep_google_search(query)
    for word in results.split(" "):
        yield word

def search_ai(query):
    results = search_ai(query)
    for word in results.split(" "):
        yield word