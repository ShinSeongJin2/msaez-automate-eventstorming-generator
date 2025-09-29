from typing import Any, Dict, Optional
from .xml_base import XmlBaseGenerator
from ..models import ESValueSummaryGeneratorOutput

class ESValueSummaryGenerator(XmlBaseGenerator):
    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        self.inputs_types_to_check = ["context", "elementIds"]
        super().__init__(model_name, ESValueSummaryGeneratorOutput, model_kwargs, client)

    def _build_persona_info(self) -> Dict[str, str]:
        return {
            "persona": "Context Analyzer and Domain-Driven Design Specialist",
            "goal": "To analyze Event Storming elements and provide accurately prioritized, contextually relevant sorting that enhances domain understanding and supports effective model implementation.",
            "backstory": "With extensive experience across numerous complex domain modeling projects, I have developed exceptional analytical capabilities in Domain-Driven Design and Event Storming methodologies. My approach combines rigorous semantic analysis with practical implementation knowledge, focusing on identifying meaningful relationships between domain elements that others might overlook. I excel at recognizing both explicit and implicit dependencies critical to domain integrity."
        }

    def _build_task_instruction_prompt(self) -> str:
        return """<instruction>
    <core_instructions>
        <title>Task: Sort Event Storming Elements by Contextual Relevance</title>
        <task_description>You are given a list of IDs for each element used in event storming, and you need to return them sorted in order of relevance to the context in which they were passed.</task_description>
        
        <output_rules>
            <title>Output Format</title>
            <rule id="json_structure">The output must be a JSON object with a "sortedElementIds" key, which is an array of the sorted element IDs.</rule>
            <rule id="no_comments">Do not write comments in the output JSON object.</rule>
        </output_rules>

        <element_id_prefixes>
            <title>Element ID Prefixes</title>
            <rule id="bc">"bc-": Bounded Context (e.g., "bc-bookManagement")</rule>
            <rule id="act">"act-": Actor</rule>
            <rule id="agg">"agg-": Aggregate</rule>
            <rule id="cmd">"cmd-": Command</rule>
            <rule id="evt">"evt-": Event</rule>
            <rule id="rm">"rm-": Read Model</rule>
            <rule id="enum">"enum-": Enumeration</rule>
            <rule id="vo">"vo-": Value Object</rule>
        </element_id_prefixes>

        <inference_guidelines>
            <title>Inference Guidelines</title>
            <guideline id="direct_reasoning">The process of reasoning should be directly related to the output result, not a reference to a general strategy.</guideline>
            <guideline id="context_analysis">Analyze the given context to understand the primary business domain and the specific scenario. Identify the core elements and their relationships within the context. Determine how each element relates to the overall business process or user interaction.</guideline>
            <guideline id="element_relationships">Examine the dependencies and connections between different EventStorming elements. Identify direct relationships (e.g., commands triggering events) and consider indirect relationships (e.g., read models updated by events).</guideline>
            <guideline id="sorting_strategy">Prioritize elements directly involved in the main process described in the context. Place elements with direct relationships closer together. Consider the order of operations or data flow. Less relevant elements should be placed lower in priority.</guideline>
            <guideline id="additional_considerations">Consider potential side effects or downstream impacts. Think about how the ordering might affect system understanding, documentation, or future development. Identify any elements with implications for other parts of the system.</guideline>
        </inference_guidelines>
    </core_instructions>
</instruction>"""

    def _build_json_example_input_format(self) -> Optional[Dict[str, Any]]:
        return {
            "context": "Adding cancel order command to Order aggregate",
            "element_ids": [
                "bc-orderManagement",
                "bc-productCatalog",
                "bc-userManagement",
                "act-customer",
                "act-admin",
                "agg-order",
                "agg-product",
                "agg-user",
                "cmd-cancelOrder",
                "cmd-createOrder",
                "cmd-updateProduct",
                "evt-orderCanceled",
                "evt-orderCreated",
                "evt-productUpdated",
                "rm-orderHistory",
                "rm-productInventory",
                "enum-orderStatus",
                "enum-productCategory",
                "vo-address",
                "vo-money"
            ]
        }

    def _build_json_example_output_format(self) -> Dict[str, Any]:
        return {
            "sortedElementIds": [
                "bc-orderManagement",
                "agg-order",
                "cmd-cancelOrder",
                "evt-orderCanceled",
                "act-customer",
                "act-admin",
                "enum-orderStatus",
                "rm-orderHistory",
                "cmd-createOrder",
                "evt-orderCreated",
                "vo-money",
                "bc-productCatalog",
                "agg-product",
                "cmd-updateProduct",
                "evt-productUpdated",
                "rm-productInventory",
                "enum-productCategory",
                "bc-userManagement",
                "agg-user",
                "vo-address"
            ]
        }
    
    def _build_json_user_query_input_format(self) -> Dict[str, Any]:
        inputs = self.client.get("inputs")
        return {
            "context": inputs.get("context"),
            "element_ids": inputs.get("elementIds"),
        }