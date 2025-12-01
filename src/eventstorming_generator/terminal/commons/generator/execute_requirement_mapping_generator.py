from ...terminal_helper import TerminalHelper
from ....generators import RequirementMappingGenerator
from ....models import RequirementMappingGeneratorOutput
from ..mocks import requirement_mapping_generator_inputs
from ....utils import EsTraceUtil

def execute_requirement_mapping_generator(is_save_to_temp: bool = True) -> RequirementMappingGeneratorOutput:
    return TerminalHelper.run_generator(
        RequirementMappingGenerator, {
            "line_numbered_requirements": EsTraceUtil.add_line_numbers_to_description(
                requirement_mapping_generator_inputs.get("requirements")
            ),
            "boundedContexts": requirement_mapping_generator_inputs.get("boundedContexts")
        }, "normal", is_save_to_temp
    )