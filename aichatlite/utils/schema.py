from dataclasses import dataclass
import time


@dataclass
class ChatMessage:
    role: str
    content: str
    timestamp: float