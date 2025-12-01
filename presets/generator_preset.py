from typing import Any, Dict, Optional

from .xml_base import XmlBaseGenerator
from ..utils import XmlUtil
from ..models import <OutputModelName>Output

class <GeneratorName>(XmlBaseGenerator):
    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        self.inputs_types_to_check = []
        super().__init__(model_name, <OutputModelName>Output, model_kwargs, client)

    def _build_persona_info(self) -> Dict[str, str]:
        return {
            "persona": "",
            "goal": "",
            "backstory": ""
        }
        
    def _build_task_instruction_prompt(self) -> str:
        return """<instruction>
    <core_instructions>
    </core_instructions>
    
    <inference_guidelines>
        <title>Inference Guidelines</title>
    </inference_guidelines>
    
    <output_format>
        <title>JSON Output Format</title>
        <description>The output must be a JSON object structured as follows:</description>
        <schema>

        </schema>
    </output_format>
</instruction>"""

    def _build_json_example_input_format(self) -> Optional[Dict[str, Any]]:
        return {
        }

    def _build_json_example_output_format(self) -> Dict[str, Any]:
        return {
        }
    
    def _build_json_user_query_input_format(self) -> Dict[str, Any]:
        inputs = self.client.get("inputs")
        return {
        }