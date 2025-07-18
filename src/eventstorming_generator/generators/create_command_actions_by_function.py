from typing import Any, Dict, Optional
from .base import BaseGenerator
from ..utils import ESValueSummarizeWithFilter
from ..models import CreateCommandActionsByFunctionOutput

class CreateCommandActionsByFunction(BaseGenerator):
    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        self.inputs_types_to_check = ["summarizedESValue", "description", "targetAggregate"]
        super().__init__(model_name, model_kwargs, client, structured_output_class=CreateCommandActionsByFunctionOutput)

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

Traceability Rules:
1. For every created element (Command, Event, ReadModel) and each of their properties, you MUST provide a `sourceReferences`.
2. The `sourceReferences` links the generated element back to the specific text in the "Functional Requirements" it was derived from. The requirements will have line numbers prepended to each line (e.g., "1: ...", "2: ...").
3. The format for `sourceReferences` is an array of Position Arrays: `[[[<start_line_number>, "<start_word_combination>"], [<end_line_number>, "<end_word_combination>"]]]`.
4. The "word_combination" MUST be a direct quote of 2-3 consecutive words from the specified line in the "Functional Requirements" to ensure it can be uniquely located. Avoid using single, common words. For example, instead of just "student", use "student to enroll".
5. If an element is inferred from multiple places, you can add multiple Position Arrays to the list. Example: `[[[10, "enroll in a course"], [10, "start learning"]], [[25, "FOREIGN KEY"], [25, "(course_id) REFERENCES"]]]`

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
   - Specify the actor (User, System, Admin, etc.)
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

Domain Events Integration:
1. Leverage predefined domain events from the functional requirements:
   - Use existing event names and descriptions as reference
   - Ensure generated events align with business semantics
   - Consider event sequencing and dependencies
2. Map user actions to appropriate domain events:
   - Connect UI actions to meaningful business events
   - Maintain consistency between event names and business vocabulary

Context Relations Consideration:
1. Account for inter-context relationships:
   - Identify external events that may trigger commands
   - Consider Pub/Sub patterns for loose coupling
   - Plan for eventual consistency across contexts
2. Integration patterns:
   - Use appropriate interaction patterns (Pub/Sub, API calls, etc.)
   - Ensure proper data ownership and boundary management
   - Consider performance and reliability implications

Avoid:
1. Duplicate commands or events
2. CRUD operations disguised as business operations
3. Comments in the output JSON
4. Overly complex command/event structures
5. Using commands/events for simple queries
6. Ignoring predefined domain events and context relationships

Best Practices:
1. Keep commands focused on single responsibility
2. Ensure events capture complete state changes
3. Design for eventual consistency
4. Consider security and authorization requirements
5. Plan for versioning and backward compatibility
6. Align with existing domain vocabulary and event definitions
7. Respect context boundaries and integration patterns"""

    def _build_inference_guidelines_prompt(self) -> str:
        return """
Inference Guidelines:
1. The process of reasoning should be directly related to the output result, not a reference to a general strategy.
2. Directional Focus: Prioritize key business objectives and ensure that the generated actions align with domain-driven design, CQRS, and event sourcing principles.
3. Validation and Consistency: Carefully evaluate business rules, validation constraints, state transitions, and property specifications to ensure architectural consistency.
4. Traceability: For each generated element and its properties, determine the `sourceReferences` by finding the exact line and word combination in the functional requirements that justifies its creation. This reference must be precise and verifiable.
5. Integration and Duplication Avoidance: Verify that new actions integrate with existing Commands, Events, and ReadModels without causing duplication.
6. Edge Cases and Error Handling: Consider potential error scenarios and boundary conditions.
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
                    "sourceReferences": [[["<start_line_number>", "<start_word_combination>"], ["<end_line_number>", "<end_word_combination>"]]],
                    "properties": [
                        {
                            "name": "<propertyName>",
                            "type?": "<propertyType>", // If the type is String, do not specify the type.
                            "isKey?": <true|false>, // Write only if there is a primary key.
                            "sourceReferences": [[["<start_line_number>", "<start_word_combination>"], ["<end_line_number>", "<end_word_combination>"]]]
                        }
                    ],

                    "outputEventIds": ["<outputEventId>"], // List of event IDs triggered by this command. Each ID MUST correspond to an event defined in the 'eventActions' section below OR an existing event from the 'Summarized Existing EventStorming Model'.
                    "actor": "<actorName>"
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
                    "sourceReferences": [[["<start_line_number>", "<start_word_combination>"], ["<end_line_number>", "<end_word_combination>"]]],

                    "properties": [
                        {
                            "name": "<propertyName>",
                            "type?": "<propertyType>",
                            "isKey?": <true|false>,
                            "sourceReferences": [[["<start_line_number>", "<start_word_combination>"], ["<end_line_number>", "<end_word_combination>"]]]
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
                    "sourceReferences": [[["<start_line_number>", "<start_word_combination>"], ["<end_line_number>", "<end_word_combination>"]]],
                    "queryParameters": [
                        {
                            "name": "<propertyName>",
                            "type?": "<propertyType>",
                            "isKey?": <true|false>,
                            "sourceReferences": [[["<start_line_number>", "<start_word_combination>"], ["<end_line_number>", "<end_word_combination>"]]]
                        }
                    ],

                    "actor": "<actorName>"
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
                        "id": "bc-course",
                        "name": "CourseManagement",
                        "actors": [
                            {
                                "id": "act-student",
                                "name": "Student"
                            },
                            {
                                "id": "act-instructor",
                                "name": "Instructor"
                            }
                        ],
                        "aggregates": [
                            {
                                "id": "agg-course",
                                "name": "Course",
                                "properties": [
                                    {
                                        "name": "courseId",
                                        "type": "Long",
                                        "isKey": True
                                    },
                                    {
                                        "name": "title"
                                    },
                                    {
                                        "name": "instructorId",
                                        "type": "Long"
                                    },
                                    {
                                        "name": "price",
                                        "type": "Double"
                                    },
                                    {
                                        "name": "status",
                                        "type": "CourseStatus"
                                    }
                                ],
                                "enumerations": [
                                    {
                                        "id": "enum-course-status",
                                        "name": "CourseStatus",
                                        "items": ["DRAFT", "PUBLISHED", "ARCHIVED"]
                                    }
                                ],
                                "commands": [
                                    {
                                        "id": "cmd-create-course",
                                        "name": "CreateCourse",
                                        "properties": [
                                            {"name": "title"},
                                            {"name": "instructorId", "type": "Long"}
                                        ],
                                        "outputEvents": [
                                            {
                                                "id": "evt-course-created",
                                                "name": "CourseCreated"
                                            }
                                        ]
                                    }
                                ],
                                "events": [
                                    {
                                        "id": "evt-course-created",
                                        "name": "CourseCreated"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            "description": """
1: # Functional Requirements for Course Enrollment
2: 
3: ## User Story
4: As a student, I want to enroll in a course so I can start learning. The system must verify my eligibility and process my payment if the course is not free. Upon successful enrollment, my status should be updated, and I should receive a confirmation.
5: 
6: ## Key Events
7: - `StudentEnrolled`: Triggered when a student successfully enrolls in a course.
8: - `EnrollmentFailed`: Triggered if enrollment cannot be completed due to reasons like course full, payment failure, or prerequisites not met.
9: - `CoursePublished`: A course must be in 'Published' state to allow enrollment.
10: 
11: ## DDL
12: ```sql
13: -- Courses Table
14: CREATE TABLE courses (
15:     course_id INT PRIMARY KEY,
16:     title VARCHAR(255) NOT NULL,
17:     instructor_id INT NOT NULL,
18:     price DECIMAL(10, 2) NOT NULL,
19:     status ENUM('DRAFT', 'PUBLISHED', 'ARCHIVED') NOT NULL,
20:     max_students INT,
21:     current_students INT DEFAULT 0
22: );
23: 
24: -- Enrollments Table
25: CREATE TABLE enrollments (
26:     enrollment_id INT PRIMARY KEY,
27:     course_id INT NOT NULL,
28:     student_id INT NOT NULL,
29:     enrollment_date DATETIME NOT NULL,
30:     status ENUM('ACTIVE', 'COMPLETED', 'CANCELLED') NOT NULL,
31:     FOREIGN KEY (course_id) REFERENCES courses(course_id)
32: );
33: ```
34: 
35: ## Context Relations
36: ### CourseToPaymentIntegration
37: - **Type**: API
38: - **Direction**: calls
39: - **Target Context**: PaymentService
40: - **Reason**: To process enrollment fees for paid courses.
41: - **Interaction Pattern**: Synchronous API call to process payment. The enrollment is confirmed only after successful payment confirmation.
""",
            "targetAggregate": "Course"
        }

    def _build_json_example_output_format(self) -> Dict[str, Any]:
        return {
            "inference": "Based on the functional requirements, the primary user action is for a student to enroll in a course. This translates to an `EnrollStudent` command within the `Course` aggregate. This command requires `courseId` and `studentId` as inputs. It must check if the course is published and not full. Upon successful validation and external payment processing, it triggers a `StudentEnrolled` event. The event contains all necessary data to reflect the state change, including enrollment details. A `CourseDetails` read model is also proposed to allow users to view course information before enrolling.",
            "result": {
                "commandActions": [
                    {
                        "actionName": "EnrollStudentInCourse",
                        "objectType": "Command",
                        "ids": {
                            "aggregateId": "agg-course",
                            "commandId": "cmd-enroll-student"
                        },
                        "args": {
                            "commandName": "EnrollStudent",
                            "commandAlias": "Enroll in Course",
                            "api_verb": "POST",
                            "sourceReferences": [[["4", "want to enroll"], ["4", "in a course"]]],
                            "properties": [
                                {
                                    "name": "courseId",
                                    "type": "Long",
                                    "isKey": True,
                                    "sourceReferences": [[["27", "course_id INT"], ["27", "INT NOT NULL"]]]
                                },
                                {
                                    "name": "studentId",
                                    "type": "Long",
                                    "sourceReferences": [[["28", "student_id INT"], ["28", "INT NOT NULL"]]]
                                }
                            ],
                            "outputEventIds": ["evt-student-enrolled"],
                            "actor": "Student"
                        }
                    }
                ],
                "eventActions": [
                    {
                        "actionName": "StudentEnrolledEvent",
                        "objectType": "Event",
                        "ids": {
                            "aggregateId": "agg-course",
                            "eventId": "evt-student-enrolled"
                        },
                        "args": {
                            "eventName": "StudentEnrolled",
                            "eventAlias": "Student Enrolled in Course",
                            "sourceReferences": [[["7", "`StudentEnrolled`: Triggered"], ["7", "successfully enrolls"]]],
                            "properties": [
                                {
                                    "name": "enrollmentId",
                                    "type": "Long",
                                    "isKey": True,
                                    "sourceReferences": [[["26", "enrollment_id INT"], ["26", "PRIMARY KEY"]]]
                                },
                                {
                                    "name": "courseId",
                                    "type": "Long",
                                    "sourceReferences": [[["27", "course_id INT"], ["27", "INT NOT NULL"]]]
                                },
                                {
                                    "name": "studentId",
                                    "type": "Long",
                                    "sourceReferences": [[["28", "student_id INT"], ["28", "INT NOT NULL"]]]
                                },
                                {
                                    "name": "enrollmentDate",
                                    "type": "Date",
                                    "sourceReferences": [[["29", "enrollment_date DATETIME"], ["29", "DATETIME NOT NULL"]]]
                                }
                            ]
                        }
                    }
                ],
                "readModelActions": [
                    {
                        "actionName": "CourseDetailsReadModel",
                        "objectType": "ReadModel",
                        "ids": {
                            "aggregateId": "agg-course",
                            "readModelId": "read-course-details"
                        },
                        "args": {
                            "readModelName": "CourseDetails",
                            "readModelAlias": "View Course Details",
                            "isMultipleResult": False,
                            "sourceReferences": [[["4", "enroll in a course"], ["4", "start learning"]]],
                            "queryParameters": [
                                {
                                    "name": "courseId",
                                    "type": "Long",
                                    "isKey": True,
                                    "sourceReferences": [[["15", "course_id INT"], ["15", "PRIMARY KEY"]]]
                                }
                            ],
                            "actor": "Student"
                        }
                    }
                ]
            }
        }
    
    def _build_required_events_constraint(self) -> str:
        """필수 이벤트 제약 조건 빌드"""
        inputs = self.client.get("inputs", {})
        required_events = inputs.get("requiredEventNames", [])
        
        if not required_events:
            return ""
            
        event_list = ", ".join(f"'{event}'" for event in required_events)
        return f"""
CRITICAL REQUIREMENT - Required Events Generation:
The following events MUST be included in the eventActions result:
{event_list}

These events are specifically requested by the user and are mandatory. Ensure each of these events:
1. Is included in the eventActions array with proper structure
2. Has appropriate properties based on business semantics
3. Has meaningful display names (aliases) in {self.client.get("preferredLanguage")}
4. Is connected to relevant commands via outputEventIds where appropriate

IMPORTANT: If any of these required events are missing from the final result, the generation will be considered incomplete and may need to be retried.
"""
    
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
* `sourceReferences` are added to all generated elements and their properties, correctly linking them to the functional requirements.

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

Domain Events Alignment:
* Generated events align with predefined domain events from functional requirements
* Event names and semantics are consistent with business vocabulary
* Event sequencing and dependencies are properly handled

Context Relations Integration:
* External context interactions are considered (API calls, Pub/Sub patterns)
* Integration patterns respect bounded context boundaries
* Inter-context event flows are properly designed
* Data ownership and consistency boundaries are maintained

Best Practices:
* Commands maintain single responsibility
* No CRUD operations disguised as business operations
* Appropriate pagination for list operations
* Proper error handling considerations
* Security and authorization requirements included
* Eventual consistency patterns are considered

{self._build_required_events_constraint()}"""
        }