import gradio as gr
import json
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Generator, Tuple


class OmniCore:
    def __init__(self, model=0, system_prompt=""):
        self.system_prompt = system_prompt
        self.DEFAULT_MODELS = [
            "Qwen/Qwen2.5-72B-Instruct",
            "Qwen/QwQ-32B-Preview",
            "Qwen/Qwen2.5-Coder-32B-Instruct",
            "NousResearch/Hermes-3-Llama-3.1-8B",
            "microsoft/Phi-3.5-mini-instruct"
        ]
        self.current_model = model

    def generator(self, query, web_search=False, system_prompt=""):
        messages = self._add_system_prompt(query, system_prompt=system_prompt)
        # Simulated response generator - replace with actual implementation
        yield "This is a sample response"

    def _add_system_prompt(self, query, system_prompt=""):
        return [
            {"role": "system", "content": system_prompt or self.system_prompt},
            {"role": "user", "content": query}
        ]


def create_chat_instance(model: str, system_prompt: str) -> OmniCore:
    return OmniCore(model=model, system_prompt=system_prompt)


class ChatState:
    def __init__(self):
        self.messages = []
        self.current_model = "Qwen/Qwen2.5-72B-Instruct"
        self.chat_history = []
        self.artifact_content = ""


def process_message(message: str, state: ChatState, system_prompt: str) -> Tuple[List[Tuple[str, str]], str]:
    if not message.strip():
        return state.chat_history, state.artifact_content

    # Create chat instance
    chat_instance = create_chat_instance(state.current_model, system_prompt)

    # Generate response
    response_text = ""
    artifact_text = ""
    is_artifact_mode = False

    for chunk in chat_instance.generator(message, system_prompt=system_prompt):
        if "<artifact_area>" in chunk:
            is_artifact_mode = not is_artifact_mode
            continue

        if is_artifact_mode:
            artifact_text += chunk
        else:
            response_text += chunk

    # Update chat history
    state.chat_history.append((message, response_text))
    state.artifact_content = artifact_text

    return state.chat_history, state.artifact_content


def create_gradio_interface():
    # Initialize state
    state = ChatState()

    # Define the system prompt
    default_system_prompt = f"""You are Claude, an AI assistant. Current date: {datetime.now().strftime('%Y-%m-%d')}
    Always wrap code and executable content in <artifact_area> tags."""

    # Create the interface
    with gr.Blocks(css="""
        .container { max-width: 800px; margin: auto; padding: 20px; }
        .chat-window { height: 400px; overflow-y: auto; }
        .artifact-window { background: #f5f5f5; padding: 10px; border-radius: 5px; }
    """) as interface:
        gr.Markdown("# AI Chat Interface")

        with gr.Row():
            with gr.Column(scale=2):
                chatbot = gr.Chatbot(label="Chat History")
                msg = gr.Textbox(label="Message", placeholder="Type your message here...")

            with gr.Column(scale=1):
                artifact_output = gr.Code(label="Artifact Output", language="python")

        with gr.Row():
            model_dropdown = gr.Dropdown(
                choices=["Qwen/Qwen2.5-72B-Instruct", "Qwen/QwQ-32B-Preview"],
                value=state.current_model,
                label="Select Model"
            )
            system_prompt_input = gr.Textbox(
                value=default_system_prompt,
                label="System Prompt",
                lines=3
            )

        # Handle message submission
        def on_message(message: str, history: List[Tuple[str, str]], state: ChatState):
            new_history, new_artifact = process_message(
                message,
                state,
                system_prompt_input.value
            )
            return "", new_history, new_artifact

        msg.submit(
            on_message,
            inputs=[msg, chatbot, gr.State(state)],
            outputs=[msg, chatbot, artifact_output]
        )

        # Handle model selection
        def update_model(model: str, state: ChatState):
            state.current_model = model

        model_dropdown.change(
            update_model,
            inputs=[model_dropdown, gr.State(state)]
        )

    return interface


if __name__ == "__main__":
    interface = create_gradio_interface()
    interface.launch(share=True, server_port=7860)