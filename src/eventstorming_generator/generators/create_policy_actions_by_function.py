from typing import Any, Dict, Optional
from .base import BaseGenerator
from ..utils import ESValueSummarizeWithFilter
from ..models import CreatePolicyActionsByFunctionOutput

class CreatePolicyActionsByFunction(BaseGenerator):
    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        self.inputs_types_to_check = ["summarizedESValue", "description"]
        super().__init__(model_name, model_kwargs, client, structured_output_class=CreatePolicyActionsByFunctionOutput)

    def _build_agent_role_prompt(self) -> str:
        return """Role: Policy Designer and Domain-Driven Design (DDD) Architect

Goal: To analyze business requirements and event-driven systems to derive optimal policies, automation rules, and integration patterns that maximize business value while maintaining system integrity.

Backstory: With over 15 years of hands-on experience in event-driven architectures, I have designed robust policy systems across numerous industries. My approach focuses on balancing technical precision with business needs, emphasizing maintainable implementations that respect domain boundaries while ensuring long-term scalability.

Operational Guidelines:
* Analyze complex business requirements to derive effective, scalable policies and automation rules
* Design robust event-driven workflows with precise policy triggers and actions that optimize system responsiveness
* Create maintainable policy implementations across bounded contexts while respecting domain boundaries
* Ensure bidirectional consistency between events, commands, and business rules through sophisticated validation patterns
* Identify optimal automation patterns and integration points that minimize coupling while maximizing system cohesion
* Implement idempotent policy handlers that gracefully handle failure scenarios and eventual consistency challenges
* Balance technical implementation details with business-driven policy design to ensure long-term business value
* Optimize cross-context communication with appropriate policy propagation strategies and message delivery guarantees"""

    def _build_task_guidelines_prompt(self) -> str:
        return f"""You need to analyse a given event storming model to derive a policy (where events trigger other events).

Please follow these rules:
1. By analysing the given requirements and the generated event streams, we need to derive possible business logic and create relevant policies that connect events to subsequent events.
2. The name of policy should be written in English, and the rest of the content (alias, etc.) should be written in {self.client.get("preferredLanguage")} language so that it is easily understood by the user.
3. Do not write comments in the output JSON object.
4. Each policy should follow these guidelines:
   - Policy names should be clear and action-oriented.
   - Reasons should explain the business value and purpose.
   - Consider the temporal aspects of event-to-event relationships.
   - Ensure policies don't create circular dependencies.
5. When creating policies, consider:
   - Business rules and constraints from requirements
   - Domain events and their business implications
   - Context relationships and interaction patterns
   - Eventual consistency requirements
   - Error handling and compensation scenarios
   - Performance implications of cross-context communication
6. Leverage the provided domain events to understand:
   - Event triggers and their business significance
   - Cross-context event flows and dependencies
   - Event-driven workflow patterns
7. Consider context relations when designing policies:
   - Respect bounded context boundaries
   - Align with defined interaction patterns (Pub/Sub, API calls, etc.)
   - Ensure policies support the specified context relationships
8. Validation criteria for each policy:
   - Must have clear trigger conditions (input events).
   - Must produce clear outcomes (output events).
   - Should respect bounded context boundaries.
   - Must be idempotent where possible.
   - Should handle failure scenarios gracefully.
   - Should align with defined context interaction patterns.
9. Avoid:
   - Tightly coupled policies across multiple contexts
   - Policies that could cause deadlocks
   - Over-complicated policy chains
   - Ambiguous or vague policy names
   - Policies that contradict defined context relationships
   - Policies that connect events within the same aggregate. Policies must only connect events between different aggregates."""

    def _build_inference_guidelines_prompt(self) -> str:
        return """
Inference Guidelines:
1. The process of reasoning should be directly related to the output result, not a reference to a general strategy.
2. Context Analysis: Thoroughly analyze the provided event storming model and functional requirements to understand the business objectives, domain boundaries, and integration points.
3. Domain Events Analysis: Examine the provided domain events to understand business workflows, event sequences, and cross-context interactions.
4. Context Relations Analysis: Review context relationships to understand interaction patterns, data flow directions, and integration constraints.
5. Policy Design: Derive clear and distinct policies that connect related source events with appropriate target events, ensuring each policy delivers unique business value while respecting context boundaries.
6. Cross-Context Validation: Ensure policies align with defined context interaction patterns and don't violate bounded context principles.
7. Validation: Verify that policies avoid duplication and circular dependencies. It is strictly forbidden to create a policy where a source event and a target event belong to the same aggregate. Such policies are invalid and must be filtered out.
"""

    def _build_request_format_prompt(self) -> str:
        return ESValueSummarizeWithFilter.get_guide_prompt()

    def _build_json_response_format(self) -> str:
        return """
{
    "inference": "<inference>",
    "result": {
        "extractedPolicies": [
            {
                "name": "<name>",
                "alias": "<alias>",
                "reason": "<reason>",
                "fromEventIds": ["<fromEventId1>", "<fromEventId2>"],
                "toEventIds": ["<toEventId1>", "<toEventId2>"]
            }
        ]
    }
}
"""

    def _build_json_example_input_format(self) -> Optional[Dict[str, Any]]:
        return {
            "Summarized Existing EventStorming Model": {
                "deletedProperties": ESValueSummarizeWithFilter.KEY_FILTER_TEMPLATES["aggregateInnerStickers"] + 
                    ESValueSummarizeWithFilter.KEY_FILTER_TEMPLATES["detailedProperties"],
                "boundedContexts": [
                    {
                        "id": "bc-reservation",
                        "name": "reservationservice",
                        "actors": [
                            {
                                "id": "act-customer",
                                "name": "Customer"
                            },
                            {
                                "id": "act-staff",
                                "name": "RestaurantStaff"
                            }
                        ],
                        "aggregates": [
                            {
                                "id": "agg-reservation",
                                "name": "Reservation",
                                "policies": [],
                                "commands": [
                                    {
                                        "id": "cmd-create-reservation",
                                        "name": "CreateReservation",
                                        "api_verb": "POST",
                                        "outputEvents": [
                                            {
                                                "id": "evt-reservation-created",
                                                "name": "ReservationCreated"
                                            }
                                        ]
                                    },
                                    {
                                        "id": "cmd-confirm-reservation",
                                        "name": "ConfirmReservation",
                                        "api_verb": "PATCH",
                                        "outputEvents": [
                                            {
                                                "id": "evt-reservation-confirmed",
                                                "name": "ReservationConfirmed"
                                            }
                                        ]
                                    }
                                ],
                                "events": [
                                    {
                                        "id": "evt-reservation-created",
                                        "name": "ReservationCreated",
                                    },
                                    {
                                        "id": "evt-reservation-confirmed",
                                        "name": "ReservationConfirmed",
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "id": "bc-kitchen",
                        "name": "kitchenservice",
                        "aggregates": [
                            {
                                "id": "agg-kitchen",
                                "name": "Kitchen",
                                "policies": [],
                                "commands": [
                                    {
                                        "id": "cmd-prepare-kitchen",
                                        "name": "PrepareKitchen",
                                        "api_verb": "POST",
                                        "outputEvents": [
                                            {
                                                "id": "evt-kitchen-prepared",
                                                "name": "KitchenPrepared"
                                            }
                                        ]
                                    }
                                ],
                                "events": [
                                    {
                                        "id": "evt-kitchen-prepared",
                                        "name": "KitchenPrepared",
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "id": "bc-table",
                        "name": "tableservice",
                        "aggregates": [
                            {
                                "id": "agg-table",
                                "name": "Table",
                                "policies": [],
                                "commands": [
                                    {
                                        "id": "cmd-assign-table",
                                        "name": "AssignTable",
                                        "api_verb": "PATCH",
                                        "outputEvents": [
                                            {
                                                "id": "evt-table-assigned",
                                                "name": "TableAssigned"
                                            }
                                        ]
                                    }
                                ],
                                "events": [
                                    {
                                        "id": "evt-table-assigned",
                                        "name": "TableAssigned",
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            "Functional Requirements": """# Functional Requirements: Restaurant Reservation System

## User Story
As a customer, I want to make a restaurant reservation and receive confirmation.
- Acceptance Criteria:
  - Reservation should be created with customer details and party size.
  - System should automatically assign an appropriate table.
  - Kitchen should be notified for preparation.
  - Customer should receive a confirmation.

## Key Domain Events
- `ReservationCreated`: A new reservation is created by the customer.
- `TableAssigned`: A table has been assigned to the reservation.
- `KitchenNotified`: The kitchen has been notified for preparation.
- `ReservationConfirmed`: The reservation is fully confirmed.

## DDL Snippet
```sql
CREATE TABLE reservations (
    reservation_id INT PRIMARY KEY,
    customer_id INT,
    party_size INT,
    status VARCHAR(50) -- 'PENDING', 'CONFIRMED'
);
```

## Context Relations
- **Name**: ReservationToKitchen
- **Type**: Pub/Sub
- **Interaction**: Reservation Service publishes `ReservationConfirmed` events. The Kitchen Service subscribes to trigger preparation.
- **Reason**: The kitchen needs to prepare for confirmed reservations.
"""
        }

    def _build_json_example_output_format(self) -> Dict[str, Any]:
        return {
            "inference": """Based on the functional requirements and event storming model, two policies are derived to automate the reservation workflow. The user story requires automatic table assignment and kitchen notification. The 'ReservationToKitchen' context relation explicitly defines a Pub/Sub pattern where the Kitchen Service subscribes to `ReservationConfirmed` events.

1.  **AutoTableAssignmentPolicy**: The requirement "System should automatically assign an appropriate table" implies that after a `ReservationCreated` event, a `TableAssigned` event should follow without manual intervention. This policy connects `evt-reservation-created` to `evt-table-assigned`, automating the process across the Reservation and Table bounded contexts.

2.  **KitchenPreparationPolicy**: The requirement "Kitchen should be notified for preparation" and the `ReservationToKitchen` context relation guide this policy. It listens for the `ReservationConfirmed` event and triggers the `KitchenPrepared` event in the Kitchen context. This directly implements the specified Pub/Sub interaction, ensuring the kitchen is notified to prepare for the confirmed reservation.""",
            "result": {
                "extractedPolicies": [
                    {
                        "name": "AutoTableAssignment",
                        "alias": "Automatic Table Assignment",
                        "reason": "Fulfills the requirement that when a customer creates a reservation, the system must automatically assign an appropriate table.",
                        "fromEventIds": ["evt-reservation-created"],
                        "toEventIds": ["evt-table-assigned"]
                    },
                    {
                        "name": "KitchenPreparation",
                        "alias": "Kitchen Preparation Notification",
                        "reason": "Implements a Pub/Sub pattern to notify the kitchen for preparation once a reservation is confirmed. This is defined in the relationship between the Reservation and Kitchen contexts.",
                        "fromEventIds": ["evt-reservation-confirmed"],
                        "toEventIds": ["evt-kitchen-prepared"]
                    }
                ]
            }
        }
    
    def _build_json_user_query_input_format(self) -> Dict[str, Any]:
        inputs = self.client.get("inputs")
        return {
            "Summarized Existing EventStorming Model": inputs.get("summarizedESValue"),

            "Functional Requirements": inputs.get("description"),

            "Final Check": """
* Do not create a duplicate policy if there is already an existing policy connecting the same set of input and output events.
* CRITICAL RULE: Do not create a policy where an Event triggers another Event within the same Aggregate. This is an invalid design, as such logic should be handled internally within the aggregate itself, not through a policy.
* Ensure all policies that cross Aggregate or Bounded Context boundaries are justified by the requirements.
* Verify that each policy serves a distinct business purpose and is not redundant.
"""
        }