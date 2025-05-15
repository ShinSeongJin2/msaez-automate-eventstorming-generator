from typing import Any, Dict, Optional
from .base import BaseGenerator
from ..utils import ESValueSummarizeWithFilter

class CreateCommandActionsByFunction(BaseGenerator):
    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        self.inputs_types_to_check = ["summarizedESValue", "description", "targetAggregate"]
        super().__init__(model_name, model_kwargs, client)

    def _build_agent_role_prompt(self) -> str:
        return """Role: Senior Domain-Driven Design Architect and Event-Driven Systems Expert

Goal: To design precise, robust domain models and event-driven architectures that translate complex business requirements into well-structured, maintainable systems following DDD principles and event sourcing patterns.

Backstory: With extensive experience implementing complex enterprise systems, I've mastered the practical application of domain-driven design and event-driven architecture patterns across diverse business domains. My approach combines technical rigor with pragmatic solutions, ensuring systems remain maintainable while addressing real business needs. I excel at identifying domain boundaries, creating consistent messaging patterns, and designing systems that properly encapsulate business operations.

Operational Guidelines:
* Translate business requirements into precise domain models with clear aggregate boundaries and well-structured commands
* Design robust event-driven systems with consistent messaging patterns and proper domain isolation
* Implement CQRS and event sourcing patterns according to industry best practices
* Create scalable, resilient microservice architectures with proper context mapping
* Apply DDD tactical patterns (aggregates, entities, value objects, repositories, services) with careful consideration of invariants
* Ensure systems follow clean architecture principles for testability and loose coupling
* Balance technical excellence with pragmatic solutions that address real business needs
* Identify domain events that accurately capture meaningful state changes within bounded contexts
* Develop command hierarchies that properly encapsulate business operations and enforce domain rules"""

    def _build_task_guidelines_prompt(self) -> str:
        return f"""You need to write an action that adds the appropriate commands, events, and ReadModels to a given Aggregate to reflect the user's needs.

Please follow these rules:

Data Type Guidelines:
1. Use appropriate Java data types:
   - Basic types: String, Long, Integer, Double, Boolean, Date
   - Collection types: List<Type>, Set<Type>
   - Custom types must be defined as Enumeration, ValueObject within the Aggregate
2. Avoid using String type when a more specific type exists (e.g., use Date for dates, Integer for counts)
3. For arrays/collections, always use List<Type> format (e.g., List<String>)

Naming and Language Conventions:
1. Technical names (classes, properties, methods) must be in English
2. Display names and descriptions (aliases) must be in {self.client.get("preferredLanguage")}
3. Use clear, descriptive names that reflect business concepts
4. Follow naming patterns:
   - Commands: Verb + Noun (e.g., CreateOrder, UpdateCustomer)
   - Events: Noun + Past Participle (e.g., OrderCreated, CustomerUpdated)
   - ReadModels: Noun + Purpose (e.g., OrderSummary, CustomerDetails)

Command and Event Guidelines:
1. Each command must:
   - Have a corresponding event (e.g., CreateOrder -> OrderCreated)
   - Include necessary validation parameters
   - Specify the actor (user, system, admin, etc.)
2. For update/delete operations:
   - Always include the Aggregate's primary key
   - Include only the fields being modified
3. Events must:
   - Contain all relevant data for state changes
   - Include any cascading effects on other aggregates
   - Reference the originating command

ReadModel Guidelines:
1. Use ReadModels for:
   - Query operations (instead of commands/events)
   - Complex data aggregation
   - Performance optimization
2. Include:
   - Clear filtering/search criteria
   - Pagination parameters when returning lists
   - Necessary joins with other aggregates

Business Logic Extraction:
1. Focus on business operations rather than CRUD:
   - Identify domain-specific actions (e.g., "ApproveOrder" instead of "UpdateOrderStatus")
   - Consider business rules and constraints
   - Include validation requirements
2. Consider cascading effects:
   - Identify related commands in other aggregates
   - Example: CreateOrder might trigger DecreaseInventory in Item aggregate
3. Handle business scenarios:
   - State transitions
   - Validation rules
   - Business process flows

Avoid:
1. Duplicate commands or events
2. CRUD operations disguised as business operations
3. Comments in the output JSON
4. Overly complex command/event structures
5. Using commands/events for simple queries

Best Practices:
1. Keep commands focused on single responsibility
2. Ensure events capture complete state changes
3. Design for eventual consistency
4. Consider security and authorization requirements
5. Plan for versioning and backward compatibility"""

    def _build_inference_guidelines_prompt(self) -> str:
        return """
Inference Guidelines:
1. The process of reasoning should be directly related to the output result, not a reference to a general strategy.
2. Directional Focus: Prioritize key business objectives and ensure that the generated actions align with domain-driven design, CQRS, and event sourcing principles.
3. Validation and Consistency: Carefully evaluate business rules, validation constraints, state transitions, and property specifications to ensure architectural consistency.
4. Integration and Duplication Avoidance: Verify that new actions integrate with existing Commands, Events, and ReadModels without causing duplication.
5. Edge Cases and Error Handling: Consider potential error scenarios and boundary conditions.
"""

    def _build_request_format_prompt(self) -> str:
        return ESValueSummarizeWithFilter.get_guide_prompt()

    def _build_json_response_format(self) -> str:
        return """
{
    "inference": "<inference>",
    "result": {
        // Generate commands in the aggregate to satisfy the given functional requirements.
        "commandActions": [
            {
                // Write the ActionName that you utilized in the previous steps
                "actionName": "<actionName>",
                "objectType": "Command",
                "ids": {
                    "aggregateId": "<aggregateId>",
                    "commandId": "<commandId>"
                },
                "args": {
                    "commandName": "<commandName>",
                    "commandAlias": "<commandAlias>",
                    "api_verb": <"POST" | "PUT" | "PATCH" | "DELETE">,

                    "properties": [
                        {
                            "name": "<propertyName>",
                            "type?": "<propertyType>" // If the type is String, do not specify the type.
                            "isKey?": <true|false> // Write only if there is a primary key.
                        }
                    ],

                    "outputEventIds": ["<outputEventId>"], // List of event IDs generated by this command. Must write existing event IDs.
                    "actor?": "<actorName>" // Write the role of the actor only when the user, not the system, is the actor.
                }
            }
        ],

        // Generate events in the aggregate to satisfy the given functional requirements.
        "eventActions": [
            {
                "actionName": "<actionName>",
                "objectType": "Event",
                "ids": {
                    "aggregateId": "<aggregateId>",
                    "eventId": "<eventId>"
                },
                "args": {
                    "eventName": "<eventName>",
                    "eventAlias": "<eventAlias>",

                    "properties": [
                        {
                            "name": "<propertyName>",
                            "type?": "<propertyType>",
                            "isKey?": <true|false>
                        }
                    ]
                }
            }
        ],

        // Generate read models in the aggregate to satisfy the given functional requirements.
        "readModelActions": [
            {
                "actionName": "<actionName>",
                "objectType": "ReadModel",
                "ids": {
                    "aggregateId": "<aggregateId>",
                    "readModelId": "<readModelId>"
                },
                "args": {
                    "readModelName": "<readModelName>",
                    "readModelAlias": "<readModelAlias>",
                    "isMultipleResult": <true|false>,

                    "queryParameters": [
                        {
                            "name": "<propertyName>",
                            "type?": "<propertyType>",
                            "isKey?": <true|false>
                        }
                    ],

                    "actor?": "<actorName>"
                }
            }
        ]
    }
}
"""

    def _build_json_example_input_format(self) -> Optional[Dict[str, Any]]:
        return {
            "Summarized Existing EventStorming Model": {
                "deletedProperties": [],
                "boundedContexts": [
                    {
                        "id": "bc-hotel",
                        "name": "hotelservice",
                        "actors": [
                            {
                                "id": "act-guest",
                                "name": "Guest"
                            },
                            {
                                "id": "act-system",
                                "name": "System"
                            }
                        ],
                        "aggregates": [
                            {
                                "id": "agg-booking",
                                "name": "Booking",
                                "properties": [
                                    {
                                        "name": "bookingId",
                                        "type": "Long",
                                        "isKey": True
                                    },
                                    {
                                        "name": "guestId",
                                        "type": "Long",
                                        "isForeignProperty": True
                                    },
                                    {
                                        "name": "roomId",
                                        "type": "Long",
                                        "isForeignProperty": True
                                    },
                                    {
                                        "name": "checkInDate",
                                        "type": "Date"
                                    },
                                    {
                                        "name": "checkOutDate",
                                        "type": "Date"
                                    },
                                    {
                                        "name": "status",
                                        "type": "BookingStatus"
                                    },
                                    {
                                        "name": "totalAmount",
                                        "type": "Integer"
                                    }
                                ],
                                "enumerations": [
                                    {
                                        "id": "enum-booking-status",
                                        "name": "BookingStatus",
                                        "items": ["PENDING", "CONFIRMED", "CHECKED_IN", "CHECKED_OUT", "CANCELLED"]
                                    },
                                    {
                                        "id": "enum-meal-plan",
                                        "name": "MealPlan",
                                        "items": ["NO_MEAL", "BREAKFAST_ONLY", "HALF_BOARD", "FULL_BOARD"]
                                    }
                                ],
                                "valueObjects": [
                                    {
                                        "id": "vo-guest-details",
                                        "name": "GuestDetails",
                                        "properties": [
                                            {
                                                "name": "name"
                                            },
                                            {
                                                "name": "email"
                                            },
                                            {
                                                "name": "phoneNumber"
                                            },
                                            {
                                                "name": "membershipLevel"
                                            }
                                        ]
                                    },
                                    {
                                        "id": "vo-booking-preferences",
                                        "name": "BookingPreferences",
                                        "properties": [
                                            {
                                                "name": "numberOfGuests",
                                                "type": "Integer"
                                            },
                                            {
                                                "name": "mealPlan",
                                                "type": "MealPlan"
                                            },
                                            {
                                                "name": "specialRequests"
                                            }
                                        ]
                                    }
                                ],
                                "commands": [
                                    {
                                        "id": "cmd-check-room-availability",
                                        "name": "CheckRoomAvailability",
                                        "api_verb": "GET",
                                        "isRestRepository": False,
                                        "properties": [
                                            {
                                                "name": "checkInDate",
                                                "type": "Date"
                                            },
                                            {
                                                "name": "checkOutDate",
                                                "type": "Date"
                                            }
                                        ],
                                        "outputEvents": [
                                            {
                                                "id": "evt-room-availability-checked",
                                                "name": "RoomAvailabilityChecked"
                                            }
                                        ]
                                    }
                                ],
                                "events": [
                                    {
                                        "id": "evt-room-availability-checked",
                                        "name": "RoomAvailabilityChecked",
                                        "outputCommands": [
                                            {
                                                "id": "cmd-calculate-room-price",
                                                "name": "CalculateRoomPrice",
                                                "policyId": "pol-roomPriceCalculation",
                                                "policyName": "RoomPriceCalculation"
                                            }
                                        ]
                                    },
                                    {
                                        "id": "evt-room-price-calculated",
                                        "name": "RoomPriceCalculated",
                                        "outputCommands": []
                                    }
                                ],
                                "readModels": []
                            },
                            {
                                "id": "agg-room",
                                "name": "Room",
                                "properties": [
                                    {
                                        "name": "roomId",
                                        "type": "Long",
                                        "isKey": True
                                    },
                                    {
                                        "name": "roomNumber"
                                    },
                                    {
                                        "name": "roomType",
                                        "type": "RoomType"
                                    },
                                    {
                                        "name": "basePrice",
                                        "type": "Double"
                                    },
                                    {
                                        "name": "status",
                                        "type": "RoomStatus"
                                    }
                                ],
                                "enumerations": [
                                    {
                                        "id": "enum-room-type",
                                        "name": "RoomType",
                                        "items": ["STANDARD", "DELUXE", "SUITE"]
                                    },
                                    {
                                        "id": "enum-room-status",
                                        "name": "RoomStatus",
                                        "items": ["AVAILABLE", "OCCUPIED", "MAINTENANCE"]
                                    }
                                ],
                                "commands": [
                                    {
                                        "id": "cmd-calculate-room-price",
                                        "name": "CalculateRoomPrice",
                                        "api_verb": "POST",
                                        "isRestRepository": False,
                                        "properties": [
                                            {
                                                "name": "roomId",
                                                "type": "Long",
                                                "isKey": True
                                            },
                                            {
                                                "name": "checkInDate",
                                                "type": "Date"
                                            },
                                            {
                                                "name": "checkOutDate",
                                                "type": "Date"
                                            },
                                            {
                                                "name": "numberOfGuests",
                                                "type": "Integer"
                                            },
                                            {
                                                "name": "roomType",
                                                "type": "RoomType"
                                            }
                                        ],
                                        "outputEvents": [
                                            {
                                                "id": "evt-room-price-calculated",
                                                "name": "RoomPriceCalculated"
                                            }
                                        ]
                                    },
                                    {
                                        "id": "cmd-update-room-status",
                                        "name": "UpdateRoomStatus",
                                        "api_verb": "PATCH",
                                        "isRestRepository": True,
                                        "properties": [
                                            {
                                                "name": "roomId",
                                                "type": "Long",
                                                "isKey": True
                                            },
                                            {
                                                "name": "status",
                                                "type": "RoomStatus"
                                            },
                                            {
                                                "name": "reason"
                                            }
                                        ],
                                        "outputEvents": [
                                            {
                                                "id": "evt-room-status-updated",
                                                "name": "RoomStatusUpdated"
                                            }
                                        ]
                                    }
                                ],
                                "events": [
                                    {
                                        "id": "evt-room-status-updated",
                                        "name": "RoomStatusUpdated",
                                        "outputCommands": [
                                            {
                                                "id": "cmd-notify-housekeeping",
                                                "name": "NotifyHousekeeping",
                                                "policyId": "pol-notifyHousekeeping",
                                                "policyName": "NotifyHousekeeping"
                                            }
                                        ]
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
                        "title": "Create New Room Booking",
                        "description": "As a guest, I want to book a hotel room with my preferences so that I can secure my stay",
                        "acceptance": [
                            "All required guest information must be provided",
                            "Room type must be selected through search popup",
                            "Valid check-in and check-out dates must be selected",
                            "Meal plan must be chosen from available options"
                        ]
                    }
                ],
                "entities": {
                    "Booking": {
                        "properties": [
                            {"name": "bookingNumber", "type": "String", "required": True, "isPrimaryKey": True},
                            {"name": "guestId", "type": "String", "required": True, "isForeignKey": True, "foreignEntity": "Guest"},
                            {"name": "roomType", "type": "String", "required": True},
                            {"name": "checkInDate", "type": "Date", "required": True},
                            {"name": "checkOutDate", "type": "Date", "required": True},
                            {"name": "numberOfGuests", "type": "Integer", "required": True},
                            {"name": "mealPlan", "type": "enum", "required": True, "values": ["No Meal", "Breakfast Only", "Half Board", "Full Board"]},
                            {"name": "specialRequests", "type": "String", "required": False},
                            {"name": "status", "type": "enum", "required": True, "values": ["Active", "Completed", "Cancelled"]},
                            {"name": "totalAmount", "type": "Integer", "required": True}
                        ]
                    }
                },
                "businessRules": [
                    {
                        "name": "ValidBookingDates",
                        "description": "Check-out date must be after check-in date"
                    },
                    {
                        "name": "RequiredFields", 
                        "description": "All fields except special requests are mandatory for booking"
                    }
                ],
                "interfaces": {
                    "RoomBooking": {
                        "sections": [
                            {
                                "name": "BookingDetails",
                                "type": "form",
                                "fields": [
                                    {"name": "roomType", "type": "search", "required": True},
                                    {"name": "checkInDate", "type": "date", "required": True},
                                    {"name": "checkOutDate", "type": "date", "required": True},
                                    {"name": "numberOfGuests", "type": "number", "required": True},
                                    {"name": "mealPlan", "type": "select", "required": True},
                                    {"name": "specialRequests", "type": "textarea", "required": False}
                                ],
                                "actions": ["Submit", "Clear"]
                            }
                        ]
                    }
                }
            },

            "Target Aggregate To Generate Actions": "Booking"
        }

    def _build_json_example_output_format(self) -> Dict[str, Any]:
        return {
            "inference": "In this solution, we analyzed the summarized event storming model and the functional requirements to identify 'Booking' as the critical aggregate. The analysis revealed that the business scenario mandates distinct actions for creating, confirming, and canceling a booking. Accordingly, each action is mapped to a specific command—CreateBooking, ConfirmBooking, and CancelBooking—with corresponding events (BookingCreated, BookingConfirmed, BookingCancelled) ensuring every command triggers a consistent state transition. The design further incorporates read models to support query operations, applying precise data types (e.g., Long, Date, and Enum) and enforcing strict validation rules such as valid booking dates and mandatory field presence. By aligning with domain-driven design, CQRS, and event sourcing principles, this approach minimizes duplication, assigns roles (e.g., Guest and System) appropriately, and maintains overall architectural consistency.",
            "result": {
                "commandActions": [
                    {
                        "actionName": "CreateBookingCommand",
                        "objectType": "Command",
                        "ids": {
                            "aggregateId": "agg-booking",
                            "commandId": "cmd-create-booking"
                        },
                        "args": {
                            "commandName": "CreateBooking",
                            "commandAlias": "Create New Booking",
                            "api_verb": "POST",
                            "properties": [
                                {
                                    "name": "guestId",
                                    "type": "Long"
                                },
                                {
                                    "name": "roomId",
                                    "type": "Long"
                                },
                                {
                                    "name": "checkInDate",
                                    "type": "Date"
                                },
                                {
                                    "name": "checkOutDate",
                                    "type": "Date"
                                },
                                {
                                    "name": "numberOfGuests",
                                    "type": "Integer"
                                },
                                {
                                    "name": "mealPlan",
                                    "type": "MealPlan"
                                },
                                {
                                    "name": "specialRequests",
                                    "type": "String"
                                }
                            ],
                            "outputEventIds": ["evt-booking-created"],
                            "actor": "Guest"
                        }
                    },
                    {
                        "actionName": "ConfirmBookingCommand",
                        "objectType": "Command",
                        "ids": {
                            "aggregateId": "agg-booking",
                            "commandId": "cmd-confirm-booking"
                        },
                        "args": {
                            "commandName": "ConfirmBooking",
                            "commandAlias": "Confirm Booking",
                            "api_verb": "PATCH",
                            "properties": [
                                {
                                    "name": "bookingId",
                                    "type": "Long",
                                    "isKey": True
                                },
                                {
                                    "name": "paymentId",
                                    "type": "String"
                                }
                            ],
                            "outputEventIds": ["evt-booking-confirmed"]
                        }
                    },
                    {
                        "actionName": "CancelBookingCommand",
                        "objectType": "Command",
                        "ids": {
                            "aggregateId": "agg-booking",
                            "commandId": "cmd-cancel-booking"
                        },
                        "args": {
                            "commandName": "CancelBooking",
                            "commandAlias": "Cancel Booking",
                            "api_verb": "PATCH",
                            "properties": [
                                {
                                    "name": "bookingId",
                                    "type": "Long",
                                    "isKey": True
                                },
                                {
                                    "name": "cancellationReason",
                                    "type": "String"
                                }
                            ],
                            "outputEventIds": ["evt-booking-cancelled"],
                            "actor": "Guest"
                        }
                    }
                ],
                "eventActions": [
                    {
                        "actionName": "BookingCreatedEvent",
                        "objectType": "Event",
                        "ids": {
                            "aggregateId": "agg-booking",
                            "eventId": "evt-booking-created"
                        },
                        "args": {
                            "eventName": "BookingCreated",
                            "eventAlias": "Booking Created",
                            "properties": [
                                {
                                    "name": "bookingId",
                                    "type": "Long",
                                    "isKey": True
                                },
                                {
                                    "name": "guestId",
                                    "type": "Long"
                                },
                                {
                                    "name": "roomId",
                                    "type": "Long"
                                },
                                {
                                    "name": "checkInDate",
                                    "type": "Date"
                                },
                                {
                                    "name": "checkOutDate",
                                    "type": "Date"
                                },
                                {
                                    "name": "numberOfGuests",
                                    "type": "Integer"
                                },
                                {
                                    "name": "mealPlan",
                                    "type": "MealPlan"
                                },
                                {
                                    "name": "status",
                                    "type": "BookingStatus"
                                },
                                {
                                    "name": "totalAmount",
                                    "type": "Integer"
                                }
                            ]
                        }
                    },
                    {
                        "actionName": "BookingConfirmedEvent",
                        "objectType": "Event",
                        "ids": {
                            "aggregateId": "agg-booking",
                            "eventId": "evt-booking-confirmed"
                        },
                        "args": {
                            "eventName": "BookingConfirmed",
                            "eventAlias": "Booking Confirmed",
                            "properties": [
                                {
                                    "name": "bookingId",
                                    "type": "Long",
                                    "isKey": True
                                },
                                {
                                    "name": "paymentId",
                                    "type": "String"
                                },
                                {
                                    "name": "confirmedAt",
                                    "type": "Date"
                                }
                            ]
                        }
                    },
                    {
                        "actionName": "BookingCancelledEvent",
                        "objectType": "Event",
                        "ids": {
                            "aggregateId": "agg-booking",
                            "eventId": "evt-booking-cancelled"
                        },
                        "args": {
                            "eventName": "BookingCancelled",
                            "eventAlias": "Booking Cancelled",
                            "properties": [
                                {
                                    "name": "bookingId",
                                    "type": "Long",
                                    "isKey": True
                                },
                                {
                                    "name": "cancellationReason",
                                    "type": "String"
                                },
                                {
                                    "name": "cancelledAt",
                                    "type": "Date"
                                },
                                {
                                    "name": "refundAmount",
                                    "type": "Integer"
                                }
                            ]
                        }
                    }
                ],
                "readModelActions": [
                    {
                        "actionName": "BookingSummaryReadModel",
                        "objectType": "ReadModel",
                        "ids": {
                            "aggregateId": "agg-booking",
                            "readModelId": "read-booking-summary"
                        },
                        "args": {
                            "readModelName": "BookingSummary",
                            "readModelAlias": "Booking Summary",
                            "isMultipleResult": True,
                            "queryParameters": [
                                {
                                    "name": "bookingId",
                                    "type": "Long",
                                    "isKey": True
                                },
                                {
                                    "name": "guestName",
                                    "type": "String"
                                },
                                {
                                    "name": "roomNumber",
                                    "type": "String"
                                },
                                {
                                    "name": "checkInDate",
                                    "type": "Date"
                                },
                                {
                                    "name": "checkOutDate",
                                    "type": "Date"
                                },
                                {
                                    "name": "status",
                                    "type": "BookingStatus"
                                },
                                {
                                    "name": "totalAmount",
                                    "type": "Integer"
                                }
                            ],
                            "actor": "Guest"
                        }
                    },
                    {
                        "actionName": "BookingDetailsReadModel",
                        "objectType": "ReadModel",
                        "ids": {
                            "aggregateId": "agg-booking",
                            "readModelId": "read-booking-details"
                        },
                        "args": {
                            "readModelName": "BookingDetails",
                            "readModelAlias": "Booking Details",
                            "isMultipleResult": False,
                            "queryParameters": [
                                {
                                    "name": "bookingId",
                                    "type": "Long",
                                    "isKey": True
                                },
                                {
                                    "name": "guestDetails",
                                    "type": "GuestDetails"
                                },
                                {
                                    "name": "roomDetails",
                                    "type": "RoomDetails"
                                },
                                {
                                    "name": "bookingPreferences",
                                    "type": "BookingPreferences"
                                },
                                {
                                    "name": "paymentHistory",
                                    "type": "List<PaymentRecord>"
                                },
                                {
                                    "name": "status",
                                    "type": "BookingStatus"
                                },
                                {
                                    "name": "createdAt",
                                    "type": "Date"
                                },
                                {
                                    "name": "lastModifiedAt",
                                    "type": "Date"
                                }
                            ],
                            "actor": "Guest"
                        }
                    }
                ]
            }
        }
    
    def _build_json_user_query_input_format(self) -> Dict[str, Any]:
        inputs = self.client.get("inputs")
        return {
            "Summarized Existing EventStorming Model": inputs.get("summarizedESValue"),

            "Functional Requirements": inputs.get("description"),

            "Target Aggregate To Generate Actions": inputs.get("targetAggregate").get("name"),

            "Final Check": f"""
Data Validation:
* All property names use appropriate data types (String, Long, Integer, Double, Boolean, Date, etc.)
* Complex types (Address, Money, Email, etc.) are used instead of String where applicable
* Collections are properly defined using List<Type> format
* Primary keys and foreign keys are correctly specified

Naming Conventions:
* All technical names (Commands, Events, ReadModels) are in English
* All display names (aliases) are in {self.client.get("preferredLanguage")}
* Commands follow Verb + Noun pattern (e.g., CreateOrder)
* Events follow Noun + Past Participle pattern (e.g., OrderCreated)
* ReadModels follow Noun + Purpose pattern (e.g., OrderSummary)

Structural Integrity:
* No duplicate Commands, Events, or ReadModels across Aggregates
* Each Command has corresponding Event(s)
* Event properties capture complete state changes
* ReadModels support all required query operations

Business Logic:
* All user requirements are fully addressed
* Business rules and validations are incorporated
* Proper actor assignments for Commands and ReadModels
* State transitions are properly handled

Best Practices:
* Commands maintain single responsibility
* No CRUD operations disguised as business operations
* Appropriate pagination for list operations
* Proper error handling considerations
* Security and authorization requirements included
"""
        }