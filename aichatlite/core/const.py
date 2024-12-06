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
    "microsoft/Phi-3.5-mini-instruct",
    "meta-llama/Llama-3.1-8B-Instruct",
    "meta-llama/Llama-3.2-1B-Instruct",
    "meta-llama/Llama-3.2-3B-Instruct",
    "01-ai/Yi-1.5-34B-Chat",
    "codellama/CodeLlama-34b-Instruct-hf",
    "google/gemma-1.1-7b-it",
    "google/gemma-2-2b-it",
    "google/gemma-2-9b-it",
    "google/gemma-2b-it",
    "HuggingFaceH4/starchat2-15b-v0.1",
    "HuggingFaceH4/zephyr-7b-alpha",
    "HuggingFaceH4/zephyr-7b-beta",
    "meta-llama/Llama-2-7b-chat-hf",
    "meta-llama/Meta-Llama-3-8B-Instruct",
    "microsoft/DialoGPT-medium",
    "microsoft/Phi-3-mini-4k-instruct",
    "mistralai/Mistral-7B-Instruct-v0.2",
    "mistralai/Mistral-7B-Instruct-v0.3",
    "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO",
    "Qwen/Qwen2.5-1.5B-Instruct",
    "Qwen/Qwen2.5-3B-Instruct",
    "tiiuae/falcon-7b-instruct",
    "uschreiber/llama3.2"
]

MODELS_TITLE_MAP: Dict[str, str] = {
    "General": "Qwen/Qwen2.5-72B-Instruct",
    "Coding": "Qwen/Qwen2.5-Coder-32B-Instruct",
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