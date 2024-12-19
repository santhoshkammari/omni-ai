from dataclasses import dataclass, field
from typing import Dict, List, Optional
from pathlib import Path
import json
from .constants import *


@dataclass
class AppConfig:
    AVAILABLE_MODELS: List[str] = field(default_factory=lambda: AVAILABLE_MODELS)
    AGENT_TYPES: List[str] = field(default_factory=lambda: AGENT_TYPES)
    MODELS_TITLE_MAP: Dict[str, str] = field(default_factory=lambda: MODELS_TITLE_MAP)
    ARTIFACT_COLUMN_HEIGHT: int = ARTIFACT_COLUMN_HEIGHT
    CHAT_HISTORY_LIMIT: int = CHAT_HISTORY_LIMIT
    SYSTEM_PROMPTS: Dict[str, str] = field(default_factory=lambda: DEFAULT_SYSTEM_PROMPTS)

    @property
    def default_states(self) -> Dict:
        return {
            "messages": [],
            "current_chat_id": None,
            "selected_model": self.AVAILABLE_MODELS[0],
            "agent_type": self.AGENT_TYPES[0],
            "chat_content": "",
            "artifact_content": "",
            "model_params": {
                "temperature": 0.7,
                "max_tokens": 256,
                "top_p": 0.9,
                "presence_penalty": 0.0,
                "frequency_penalty": 0.0,
                "max_context": 4000,
            }
        }

    @classmethod
    def load_from_file(cls, config_path: Path) -> 'AppConfig':
        if config_path.exists():
            with config_path.open() as f:
                return cls(**json.load(f))
        return cls()
