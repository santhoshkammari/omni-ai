import aipromptlite

def get_available_prompts():
    prompt_names = [_ for _ in dir(aipromptlite) if _.isupper()]
    prompt_names.sort()
    return ['DEFAULT_PROMPT']+ prompt_names
# def get_available_prompts():
#     prompt_groups = {
#         'Code': ['PYTHON_CODER_PROMPT', 'CLAUDE_CODER_PROMPT'],
#         'Reason': ['AI_TECH_LEAD_PROMPT', 'BRAINSTORM_BUDDY_PROMPT'],
#         'Explain': ['PREDICTIVE_QUESTION_PROMPT', 'AILITE_CLAUDE_SYSTEM_PROMPT']
#     }
#     return prompt_groups
