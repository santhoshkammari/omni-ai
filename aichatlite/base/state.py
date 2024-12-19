from dataclasses import dataclass
from typing import Any, Dict, Optional, TypeVar, Generic
from datetime import datetime
import streamlit as st
import json
from pathlib import Path

T = TypeVar('T')


@dataclass
class StateValue(Generic[T]):
    """Wrapper for state values with metadata"""
    value: T
    last_updated: datetime
    version: int = 1


class StateManager:
    """Centralized state management for Streamlit application"""

    def __init__(self):
        self._initialize_default_states()

    def _initialize_default_states(self):
        """Initialize default states if they don't exist"""
        default_states = {
            "messages": [],
            "current_chat_id": None,
            "selected_model": None,
            "agent_type": None,
            "chat_content": "",
            "artifact_content": "",
            "model_params": {},
            "conversation_history": [],
            "ui_state": {
                "sidebar_expanded": True,
                "show_settings": False,
                "current_tab": "chat"
            },
            "cached_responses": {}
        }

        for key, default_value in default_states.items():
            if key not in st.session_state:
                self.set_state(key, default_value)

    def set_state(self, key: str, value: Any, persist: bool = False):
        """Set a state value with metadata"""
        state_value = StateValue(
            value=value,
            last_updated=datetime.now()
        )
        st.session_state[key] = state_value

        if persist:
            self._persist_state(key, state_value)

    def get_state(self, key: str, default: Any = None) -> Any:
        """Get a state value, returning default if not found"""
        state_value = st.session_state.get(key)
        if state_value is None:
            return default
        return state_value.value

    def update_state(self, key: str, value: Any, persist: bool = False):
        """Update an existing state value"""
        if key in st.session_state:
            current_state = st.session_state[key]
            new_state = StateValue(
                value=value,
                last_updated=datetime.now(),
                version=current_state.version + 1
            )
            st.session_state[key] = new_state

            if persist:
                self._persist_state(key, new_state)

    def _persist_state(self, key: str, state_value: StateValue):
        """Persist state to disk"""
        storage_dir = Path("./storage/state")
        storage_dir.mkdir(parents=True, exist_ok=True)

        state_file = storage_dir / f"{key}.json"
        state_data = {
            "value": state_value.value,
            "last_updated": state_value.last_updated.isoformat(),
            "version": state_value.version
        }

        with state_file.open("w") as f:
            json.dump(state_data, f)

    def clear_state(self, key: str):
        """Clear a specific state value"""
        if key in st.session_state:
            del st.session_state[key]

    def clear_all_states(self):
        """Clear all state values"""
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        self._initialize_default_states()

    # Specialized state handlers
    def update_chat_state(self, message: Dict):
        """Update chat-specific state"""
        messages = self.get_state("messages", [])
        messages.append(message)
        self.set_state("messages", messages)

        # Update conversation history
        history = self.get_state("conversation_history", [])
        history.append({
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        self.set_state("conversation_history", history)

    def update_model_params(self, params: Dict):
        """Update model parameters"""
        current_params = self.get_state("model_params", {})
        current_params.update(params)
        self.set_state("model_params", current_params)

    def get_conversation_context(self, limit: int = 5) -> list:
        """Get recent conversation context"""
        messages = self.get_state("messages", [])
        return messages[-limit:] if messages else []

    def cache_response(self, query: str, response: str):
        """Cache a query response"""
        cached_responses = self.get_state("cached_responses", {})
        cached_responses[query] = {
            "response": response,
            "timestamp": datetime.now().isoformat()
        }
        self.set_state("cached_responses", cached_responses)