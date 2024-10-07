from typing import List

WORD_LLAMA_DIM:int = 256

AVAILABLE_MODELS:List[str] = [
    'microsoft/Phi-3.5-mini-instruct',
    'Qwen/Qwen2.5-72B-Instruct',
    'CohereForAI/c4ai-command-r-plus-08-2024',
        'NousResearch/Hermes-3-Llama-3.1-8B',
        'mistralai/Mistral-Nemo-Instruct-2407',
        'meta-llama/Meta-Llama-3.1-70B-Instruct',
        'meta-llama/Llama-3.2-11B-Vision-Instruct'
    ]

AGENT_TYPES:List[str] = [
        "QuestionAnswer",
        "Assistant",
        "Agent",
        "CoT",
        "Reader",
        "Interpreter"
    ]