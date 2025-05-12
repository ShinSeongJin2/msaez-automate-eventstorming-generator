from typing import Any, Dict, Optional
from .base import BaseGenerator

class SanityCheckGenerator(BaseGenerator):
    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        self.inputs_types_to_check = ["text"]
        super().__init__(model_name, model_kwargs, client)
        
        self.client["disableLanguageGuide"] = True

    def _build_agent_role_prompt(self) -> str:
        return "You are a very useful assistant."

    def _build_task_guidelines_prompt(self) -> str:
        return "Please return the text entered by the user as-is in a JSON object."

    def _build_json_response_format(self) -> str:
        return """
{
    "output": "<text entered by the user>"
}
"""

    def _build_json_example_input_format(self) -> Optional[Dict[str, Any]]:
        return {
            "text": "Nice to meet you"
        }

    def _build_json_example_output_format(self) -> Dict[str, Any]:
        return {
            "output": "Nice to meet you"
        }
    
    def _build_json_user_query_input_format(self) -> Dict[str, Any]:
        inputs = self.client.get("inputs")
        return {
            "text": inputs.get("text")
        }