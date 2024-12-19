from typing import List, Dict

AVAILABLE_MODELS: List[str] = [
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
    "gpt-4-0125-preview",
    "gpt-4-1106-preview",
    "gpt-3.5-turbo-0125",
]

AGENT_TYPES: List[str] = [
    "QuestionAnswer",
    "Reasoning",
    "CodeAssistant",
    "DataAnalysis"
]

MODELS_TITLE_MAP: Dict[str, str] = {
    "General": "claude-3-opus-20240229",
    "Fast": "claude-3-haiku-20240307",
    "Balanced": "claude-3-sonnet-20240229"
}

ARTIFACT_COLUMN_HEIGHT: int = 500
CHAT_HISTORY_LIMIT: int = 100

DEFAULT_SYSTEM_PROMPTS = {
    "QuestionAnswer": """You are a helpful AI assistant focused on providing clear, concise answers.""",
    "Reasoning": """You are an AI assistant that explains reasoning step by step.""",
    "CodeAssistant": """You are an AI programming assistant. Always wrap code in <artifact_area> tags.""",
    "DataAnalysis": """You are an AI data analysis assistant focused on helping with data-related tasks."""
}