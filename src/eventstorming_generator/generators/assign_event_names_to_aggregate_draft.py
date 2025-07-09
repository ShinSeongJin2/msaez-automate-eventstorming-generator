from typing import Any, Dict, Optional, List
from .base import BaseGenerator
from ..models import AssignEventNamesToAggregateDraftOutput

class AssignEventNamesToAggregateDraft(BaseGenerator):
    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        self.inputs_types_to_check = ["aggregates", "eventNames", "boundedContextName"]
        super().__init__(model_name, model_kwargs, client, structured_output_class=AssignEventNamesToAggregateDraftOutput)

    def _build_agent_role_prompt(self) -> str:
        return """Role: Senior Domain-Driven Design Expert and Event Modeling Specialist

Goal: To accurately assign domain events to the most appropriate aggregate within a bounded context based on business semantics, aggregate responsibilities, and domain-driven design principles.

Backstory: With deep expertise in domain-driven design and event-driven architecture, I excel at understanding business domains and correctly mapping events to their owning aggregates. I understand that each aggregate should be responsible for events that represent state changes within its own boundary, and I can identify which aggregate should naturally own specific business events based on their semantic meaning and the aggregate's responsibilities.

Operational Guidelines:
* Analyze business events and determine which aggregate should be responsible for generating each event
* Consider aggregate boundaries and responsibilities when making assignments
* Ensure events are assigned to aggregates that naturally own the business concept being represented
* Apply domain-driven design principles to maintain proper aggregate isolation
* Consider the semantic meaning of events and map them to the most appropriate aggregate
* Ensure consistent event ownership patterns within the bounded context
* Balance event distribution across aggregates while maintaining logical consistency"""

    def _build_task_guidelines_prompt(self) -> str:
        return f"""You need to assign a list of event names to the most appropriate aggregates within a bounded context.

Please follow these rules:

Event Assignment Principles:
1. Semantic Ownership: Assign events to aggregates that semantically own the business concept
   - Example: "OrderCreated" should be assigned to "Order" aggregate
   - Example: "CustomerRegistered" should be assigned to "Customer" aggregate
   - Example: "PaymentProcessed" should be assigned to "Payment" aggregate

2. Business Responsibility: Consider which aggregate is responsible for the business operation
   - Events should be owned by the aggregate that triggers the state change
   - The aggregate that enforces business rules should own related events
   - Consider the primary entity that the event describes

3. Domain Boundaries: Respect aggregate boundaries and responsibilities
   - Events should not cross aggregate boundaries inappropriately
   - Each event should have a clear owning aggregate
   - Avoid splitting related events across multiple aggregates unnecessarily

4. Naming Patterns: Use naming conventions to guide assignment
   - Events typically follow "[AggregateName][Action]" pattern
   - Look for aggregate names within event names as strong indicators
   - Consider business process flows and state transitions

Assignment Strategy:
1. Analyze each event name for semantic clues about its domain concept
2. Match events to aggregates based on business responsibility
3. Consider the aggregate that would naturally trigger or own the event
4. Ensure balanced distribution while maintaining logical consistency
5. If an event could belong to multiple aggregates, choose the most semantically appropriate one

Language Conventions:
1. All technical names (aggregates, events) should be processed in English
2. Display names and descriptions should be in {self.client.get("preferredLanguage")}
3. Maintain consistency with existing naming patterns

Best Practices:
1. Each event should be assigned to exactly one aggregate
2. All provided events must be assigned (no events should be left unassigned)
3. Assignment should be based on business logic, not technical convenience
4. Consider future maintainability and logical consistency
5. Ensure assignments align with domain-driven design principles

Avoid:
1. Assigning events to aggregates with no semantic relationship
2. Leaving any events unassigned
3. Splitting logically related events across different aggregates unnecessarily
4. Making assignments based solely on alphabetical or random criteria
5. Ignoring business semantics in favor of technical convenience"""

    def _build_inference_guidelines_prompt(self) -> str:
        return """
Inference Guidelines:
1. Semantic Analysis: Carefully analyze the semantic meaning of each event name to understand what business concept it represents
2. Aggregate Responsibility: Consider which aggregate is most responsible for the business operation that would trigger this event
3. Domain Logic: Apply domain-driven design principles to ensure proper aggregate ownership
4. Business Process Flow: Consider the natural flow of business processes and which aggregate would logically generate each event
5. Consistency Validation: Ensure that similar types of events are consistently assigned to appropriate aggregates
"""

    def _build_request_format_prompt(self) -> str:
        return """
Input Format:
- boundedContextName: The name of the bounded context containing the aggregates
- aggregates: List of aggregate objects with their names and properties
- eventNames: List of event names that need to be assigned to aggregates

The goal is to assign each event name to the most appropriate aggregate based on business semantics and domain-driven design principles.
"""

    def _build_json_response_format(self) -> str:
        return """
{
    "inference": "<detailed_reasoning_for_assignments>",
    "result": [
        {
            "aggregateName": "<aggregateName>",
            "eventNames": ["<eventName1>", "<eventName2>", ...]
        }
    ]
}
"""

    def _build_json_example_input_format(self) -> Optional[Dict[str, Any]]:
        return {
            "boundedContextName": "OrderManagement",
            "aggregates": [
                {
                    "id": "agg-order",
                    "name": "Order",
                    "displayName": "주문",
                    "properties": [
                        {"name": "orderId", "type": "Long", "isKey": True},
                        {"name": "customerId", "type": "Long"},
                        {"name": "status", "type": "OrderStatus"},
                        {"name": "totalAmount", "type": "Double"}
                    ]
                },
                {
                    "id": "agg-customer",
                    "name": "Customer", 
                    "displayName": "고객",
                    "properties": [
                        {"name": "customerId", "type": "Long", "isKey": True},
                        {"name": "name", "type": "String"},
                        {"name": "email", "type": "String"}
                    ]
                },
                {
                    "id": "agg-payment",
                    "name": "Payment",
                    "displayName": "결제",
                    "properties": [
                        {"name": "paymentId", "type": "Long", "isKey": True},
                        {"name": "orderId", "type": "Long"},
                        {"name": "amount", "type": "Double"}
                    ]
                }
            ],
            "eventNames": [
                "OrderCreated",
                "OrderStatusChanged", 
                "CustomerRegistered",
                "PaymentProcessed",
                "OrderCancelled",
                "CustomerEmailUpdated"
            ]
        }

    def _build_json_example_output_format(self) -> Dict[str, Any]:
        return {
            "inference": "Analyzed each event based on semantic meaning and aggregate responsibility. OrderCreated and OrderStatusChanged clearly belong to Order aggregate as they represent order lifecycle events. CustomerRegistered and CustomerEmailUpdated belong to Customer aggregate as they represent customer-related state changes. PaymentProcessed belongs to Payment aggregate as it represents payment-specific operations. OrderCancelled belongs to Order aggregate as it represents an order state transition.",
            "result": [
                {
                    "aggregateName": "Order",
                    "eventNames": ["OrderCreated", "OrderStatusChanged", "OrderCancelled"]
                },
                {
                    "aggregateName": "Customer", 
                    "eventNames": ["CustomerRegistered", "CustomerEmailUpdated"]
                },
                {
                    "aggregateName": "Payment",
                    "eventNames": ["PaymentProcessed"]
                }
            ]
        }

    def _build_json_user_query_input_format(self) -> Dict[str, Any]:
        inputs = self.client.get("inputs")
        return {
            "boundedContextName": inputs.get("boundedContextName"),
            "aggregates": inputs.get("aggregates"),
            "eventNames": inputs.get("eventNames"),
            "instructions": f"""
Assign each event name to the most appropriate aggregate based on:

1. Business Semantics: Which aggregate naturally owns the business concept represented by the event?
2. Aggregate Responsibility: Which aggregate is responsible for the business operation that triggers this event?
3. Domain Logic: Apply DDD principles to ensure proper aggregate ownership
4. Naming Patterns: Use event naming conventions as guidance for assignment

Requirements:
* Every event must be assigned to exactly one aggregate
* No events should be left unassigned
* Assignments should be based on business logic and domain semantics
* Maintain consistency with domain-driven design principles
* Consider the natural business process flow

Language: Use {self.client.get("preferredLanguage")} for explanations and reasoning.
"""
        } 