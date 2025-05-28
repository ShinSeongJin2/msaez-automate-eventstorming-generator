from typing import Any, Dict, Optional
from .base import BaseGenerator
from ..models import ESValueSummaryGeneratorOutput

class ESValueSummaryGenerator(BaseGenerator):
    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        self.inputs_types_to_check = ["context", "elementIds"]
        super().__init__(model_name, model_kwargs, client, structured_output_class=ESValueSummaryGeneratorOutput)

    def _build_agent_role_prompt(self) -> str:
        return """Role: Context Analyzer and Domain-Driven Design Specialist

Goal: To analyze Event Storming elements and provide accurately prioritized, contextually relevant sorting that enhances domain understanding and supports effective model implementation.

Backstory: With extensive experience across numerous complex domain modeling projects, I have developed exceptional analytical capabilities in Domain-Driven Design and Event Storming methodologies. My approach combines rigorous semantic analysis with practical implementation knowledge, focusing on identifying meaningful relationships between domain elements that others might overlook. I excel at recognizing both explicit and implicit dependencies critical to domain integrity.

Operational Guidelines:
* Systematically analyze semantic relationships between Event Storming elements (Commands, Events, Aggregates) in complex domain models
* Apply DDD tactical and strategic patterns to identify critical domain concepts
* Perform contextual relevance analysis based on specific business scenarios
* Prioritize elements according to their significance within the given context
* Distinguish between core domain concepts and supporting elements
* Optimize information organization while maintaining semantic coherence
* Identify implicit dependencies not explicitly modeled but critical for domain understanding
* Present results in a structured format that reflects natural domain workflows"""

    def _build_task_guidelines_prompt(self) -> str:
        return """You are given a list of IDs for each element used in event stemming, and you need to return them sorted in order of relevance to the context in which they were passed.

Please follow these rules:
1. Do not write comments in the output JSON object.

Here's what each prefix in the element IDs means:
- bc-: Bounded Context
- act-: Actor
- agg-: Aggregate
- cmd-: Command
- evt-: Event
- rm-: Read Model
- enum-: Enumeration
- vo-: Value Object

For example, "bc-bookManagement" represents a Bounded Context named "bookManagement"."""

    def _build_inference_guidelines_prompt(self) -> str:
        return """
Inference Guidelines:
1. The process of reasoning should be directly related to the output result, not a reference to a general strategy.

2. Contextual Analysis:
    - Analyze the given context to understand the primary business domain and the specific scenario.
    - Identify the core elements and their relationships within the context.
    - Determine how each element relates to the overall business process or user interaction.

3. Element Relationships:
    - Examine the dependencies and connections between different EventStorming elements.
    - Identify direct relationships, such as commands triggering events or aggregates containing entities.
    - Consider indirect relationships, such as read models being updated by events.

4. Sorting Strategy:
    - Prioritize elements that are directly involved in the main process or scenario described in the context.
    - Place elements with direct relationships closer together in the sorted list.
    - Consider the order of operations or the flow of data when determining the sequence.
    - Elements with less direct relevance should be placed lower in the priority.

5. Additional Considerations:
    - Think about any potential side effects or downstream impacts of the main process.
    - Consider how the ordering of elements might affect system understanding, documentation, or future development.
    - Identify any elements that might have implications for other parts of the system.
"""

    def _build_json_response_format(self) -> str:
        return """
{
    "result": {
        "sortedElementIds": [
            "<id1>",
            ...
        ]
    }
} 
"""

    def _build_json_example_input_format(self) -> Optional[Dict[str, Any]]:
        return {
            "Context": "Adding cancel order command to Order aggregate",
            "EventStorming Element Ids": [
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
            "result": {
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
        }
    
    def _build_json_user_query_input_format(self) -> Dict[str, Any]:
        inputs = self.client.get("inputs")
        return {
            "Context": inputs.get("context"),
            "EventStorming Element Ids": inputs.get("elementIds"),
        }