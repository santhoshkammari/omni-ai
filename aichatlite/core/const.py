from typing import List, Dict

WORD_LLAMA_DIM:int = 1024  #Options: [64, 128, 256, 512, 1024]

# AVAILABLE_MODELS:List[str] = ['nvidia/Llama-3.1-Nemotron-70B-Instruct-HF','meta-llama/Meta-Llama-3.1-70B-Instruct', 'CohereForAI/c4ai-command-r-plus-08-2024',
#                      'Qwen/Qwen2.5-72B-Instruct',
#                      'meta-llama/Llama-3.2-11B-Vision-Instruct', 'NousResearch/Hermes-3-Llama-3.1-8B',
#                      'mistralai/Mistral-Nemo-Instruct-2407', 'microsoft/Phi-3.5-mini-instruct']

AVAILABLE_MODELS:List[str] = [
    "Qwen/Qwen2.5-72B-Instruct",
    "Qwen/QwQ-32B-Preview",
    "Qwen/Qwen2.5-Coder-32B-Instruct",
    "NousResearch/Hermes-3-Llama-3.1-8B",
    "microsoft/Phi-3.5-mini-instruct"
]

MODELS_TITLE_MAP: Dict[str, str] = {
    "Coding": "Qwen/Qwen2.5-Coder-32B-Instruct",
    "General": "Qwen/Qwen2.5-72B-Instruct",
    "Preview": "Qwen/QwQ-32B-Preview",
    "Conversational": "NousResearch/Hermes-3-Llama-3.1-8B",
    "Mini": "microsoft/Phi-3.5-mini-instruct"
}

AGENT_TYPES:List[str] = [
    "QuestionAnswer",
    "Reasoning",
    "FastSearchAI",
    "DeepSearchAI",
    "IntelligentSearchAI"
    ]



## height adjustments
ARTIFACT_COLUMN_HEIGHT:int = 500