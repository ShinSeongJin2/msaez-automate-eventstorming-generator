from typing import Any, Dict, Optional
from .base import BaseGenerator
from ..utils import ESValueSummarizeWithFilter

class CreatePolicyActionsByFunction(BaseGenerator):
    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        self.inputs_types_to_check = ["summarizedESValue", "description"]
        super().__init__(model_name, model_kwargs, client)

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
        return f"""You need to analyse a given event stemming model to derive a policy (where events lead to commands).

Please follow these rules:
1. By analysing the given requirements and the generated event streams, we need to derive possible business logic and create relevant policies.
2. The name of policy should be written in English, and the rest of the content (alias, etc.) should be written in {self.client.get("preferredLanguage")} language so that it is easily understood by the user.
3. Do not write comments in the output JSON object.
4. Each policy should follow these guidelines:
   - Policy names should be clear and action-oriented
   - Reasons should explain the business value and purpose
   - Consider the temporal aspects of event-command relationships
   - Ensure policies don't create circular dependencies
5. When creating policies, consider:
   - Business rules and constraints from requirements
   - Eventual consistency requirements
   - Error handling and compensation scenarios
   - Performance implications of cross-context communication
6. Validation criteria for each policy:
   - Must have clear trigger conditions
   - Should respect bounded context boundaries
   - Must be idempotent where possible
   - Should handle failure scenarios gracefully
7. Avoid:
   - Tightly coupled policies across multiple contexts
   - Policies that could cause deadlocks
   - Over-complicated policy chains
   - Ambiguous or vague policy names"""

    def _build_inference_guidelines_prompt(self) -> str:
        return """
Inference Guidelines:
1. The process of reasoning should be directly related to the output result, not a reference to a general strategy.
2. Context Analysis: Thoroughly analyze the provided event storming model and functional requirements to understand the business objectives, domain boundaries, and integration points.
3. Policy Design: Derive clear and distinct policies that connect related events with appropriate commands, ensuring each policy delivers unique business value.
4. Validation: Verify that policies avoid duplication, circular dependencies, and only span across aggregates or bounded contexts when necessary.
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
                "fromEventId": "<fromEventId>",
                "toCommandId": "<toCommandId>"
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
                                        "outputCommands": []
                                    },
                                    {
                                        "id": "evt-reservation-confirmed",
                                        "name": "ReservationConfirmed",
                                        "outputCommands": []
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
                                        "outputCommands": []
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
                                        "outputCommands": []
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            "Functional Requirements": {
                "userStories": [
                    {
                        "title": "Restaurant Reservation Process",
                        "description": "As a customer, I want to make a restaurant reservation and receive confirmation",
                        "acceptance": [
                            "Reservation should be created with customer details and party size",
                            "System should automatically assign appropriate table",
                            "Kitchen should be notified for preparation",
                            "Customer should receive confirmation"
                        ]
                    }
                ],
                "entities": {
                    "Reservation": {
                        "properties": [
                            {"name": "reservationId", "type": "String", "required": True, "isPrimaryKey": True},
                            {"name": "customerId", "type": "String", "required": True},
                            {"name": "partySize", "type": "Integer", "required": True},
                            {"name": "dateTime", "type": "Date", "required": True},
                            {"name": "status", "type": "enum", "required": True, "values": ["Pending", "Confirmed", "Cancelled"]},
                            {"name": "specialRequests", "type": "String", "required": False}
                        ]
                    }
                },
                "businessRules": [
                    {
                        "name": "TableAssignment",
                        "description": "Tables must be assigned based on party size and availability"
                    },
                    {
                        "name": "KitchenPreparation",
                        "description": "Kitchen must be notified 2 hours before reservation time"
                    }
                ]
            }
        }

    def _build_json_example_output_format(self) -> Dict[str, Any]:
        return {
            "inference": """Based on the detailed analysis of the event storming model and functional requirements, three distinct policies have been derived. The "TableAssignmentPolicy" connects the "ReservationCreated" event to the "AssignTable" command, ensuring that table assignment is automatically triggered upon reservation creation. The "KitchenPreparationPolicy" links the "ReservationConfirmed" event to the "PrepareKitchen" command, initiating kitchen preparation as soon as the reservation is confirmed. Lastly, the "ReservationConfirmationPolicy" ties the "TableAssigned" event to the "ConfirmReservation" command, finalizing the reservation process through a status update. Each policy is carefully designed to span across aggregate boundaries while avoiding duplication and circular dependencies, thereby delivering clear and actionable business value.""",
            "result": {
                "extractedPolicies": [
                    {
                        "name": "TableAssignmentPolicy",
                        "alias": "Table Assignment Automation",
                        "reason": "Automatically assign appropriate table upon reservation creation",
                        "fromEventId": "evt-reservation-created",
                        "toCommandId": "cmd-assign-table"
                    },
                    {
                        "name": "KitchenPreparationPolicy",
                        "alias": "Kitchen Preparation Trigger",
                        "reason": "Initiate kitchen preparation process when reservation is confirmed",
                        "fromEventId": "evt-reservation-confirmed",
                        "toCommandId": "cmd-prepare-kitchen"
                    },
                    {
                        "name": "ReservationConfirmationPolicy",
                        "alias": "Reservation Status Update",
                        "reason": "Update reservation status after successful table assignment",
                        "fromEventId": "evt-table-assigned",
                        "toCommandId": "cmd-confirm-reservation"
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
* Do not create a duplicate policy if there is already any existing policy connecting the same Event to the same Command
* Do not create a policy where an Event triggers a Command within the same Aggregate
* Ensure all policies cross Aggregate or Bounded Context boundaries
* Verify that each policy serves a distinct business purpose and is not redundant
"""
        }