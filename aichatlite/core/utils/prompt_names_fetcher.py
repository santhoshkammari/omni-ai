import aipromptlite

def get_available_prompts():
    prompt_names = [_ for _ in dir(aipromptlite) if _.isupper()]
    prompt_names.sort()
    return ['DEFAULT_PROMPT']+ prompt_names
