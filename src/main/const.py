from typing import List

WORD_LLAMA_DIM:int = 1024  #Options: [64, 128, 256, 512, 1024]

AVAILABLE_MODELS:List[str] = [
    'microsoft/Phi-3.5-mini-instruct',
    'meta-llama/Meta-Llama-3.1-70B-Instruct',
    'Qwen/Qwen2.5-72B-Instruct',
    'CohereForAI/c4ai-command-r-plus-08-2024',
        'NousResearch/Hermes-3-Llama-3.1-8B',
        'mistralai/Mistral-Nemo-Instruct-2407',
        'meta-llama/Llama-3.2-11B-Vision-Instruct'
    ]

AGENT_TYPES:List[str] = [
    "QuestionAnswer",
    "AIResearcher",
    "Agent",
        "CoT",
        "Reader",
        "Interpreter"
    ]

## height adjustments
ARTIFACT_COLUMN_HEIGHT:int = 750