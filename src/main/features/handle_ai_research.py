import json
import re
import time

from src.main.base import OmniCore


class AIResearcher:
    def generate_response(self,prompt, chatbot:OmniCore, max_steps=5, minimum_steps=3,web_search = False):
        def get_step_data(prompt):
            output = chatbot.invoke(prompt,web_search=web_search)
            try:
                if '```json' in output:
                    json_string = re.findall('```json\s*(.*)\s*```', output, re.DOTALL)
                    data_dict = json.loads(json_string[0])
                else:
                    data_dict = json.loads(output.strip())
            except:
                data_dict = {}
            return data_dict

        steps = []
        step_count = 1
        total_thinking_time = 0

        while True and step_count <= max_steps:
            start_time = time.time()
            prompt += "\nRemember: Your ENTIRE response, for EVERY interaction, must be a SINGLE, valid JSON object. Do not include any text or explanations outside of this JSON structure.\n"""
            step_data = get_step_data(prompt)  # Increased max_tokens for each step
            end_time = time.time()
            thinking_time = end_time - start_time
            total_thinking_time += thinking_time

            # Handle the case where 'confidence' key is not present
            confidence = step_data.get('confidence', 0.5)  # Default to 0.5 if not present
            next_action = step_data.get('next_action', 'continue')
            step_title:str  = f"Step {step_count}: {step_data.get('title', 'Untitled Step')}"
            step_content:str = step_data.get('content', 'No content provided')

            steps.append((step_title,step_content,
                          next_action,
                          str(thinking_time),
                          str(confidence)))

            if next_action == 'final_answer' and step_count < minimum_steps:  # Increased minimum steps to 15
                prompt = "Please continue your analysis with at least 5 more steps before providing the final answer."
            elif next_action == 'final_answer' or int(confidence) == 1:
                break
            elif next_action == 'reflect' or step_count % 3 == 0:
                prompt = "Please perform a detailed self-reflection on your reasoning so far, considering potential biases and alternative viewpoints."

            step_count += 1

            # Yield after each step for Streamlit to update

            current_step_response = ("artifact " if step_count==2 else "") + step_title+"\n"+step_content
            for yield_x in current_step_response.split(" "):
                yield yield_x+" "

        # Generate final answer
        prompt = "Please provide a comprehensive final answer based on your reasoning above, summarizing key points and addressing any uncertainties in a single JSON please."

        start_time = time.time()
        prompt += "\nRemember: Your ENTIRE response, for EVERY interaction, must be a SINGLE, valid JSON object. Do not include any text or explanations outside of this JSON structure.\n"""
        final_data = get_step_data(prompt)  # Increased max_tokens for final answer
        end_time = time.time()
        thinking_time = end_time - start_time
        total_thinking_time += thinking_time

        # Handle the case where 'confidence' key is not present in final_data
        final_confidence = final_data.get('confidence', 1.0)
        final_data = final_data.get('content', 'No final answer provided')

        steps.append(
            ("Final Answer", final_data, thinking_time, final_confidence))

        final_data = "artifact " + final_data
        for yield_x in final_data.split(" "):
            yield yield_x+" "