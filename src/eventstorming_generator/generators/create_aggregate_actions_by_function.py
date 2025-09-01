from typing import Any, Dict, Optional
from .base import BaseGenerator
from ..utils import ESValueSummarizeWithFilter
from ..models import CreateAggregateActionsByFunctionOutput

class CreateAggregateActionsByFunction(BaseGenerator):
    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        self.inputs_types_to_check = ["summarizedESValue", "targetBoundedContext", "description", "draftOption", "targetAggregate"]
        super().__init__(model_name, model_kwargs, client, structured_output_class=CreateAggregateActionsByFunctionOutput)

    def _build_agent_role_prompt(self) -> str:
        return """Role: Domain-Driven Design (DDD) Architect and Strategic Modeling Expert

Goal: To translate complex business domains into well-structured software designs by creating precise bounded contexts, cohesive aggregates, and event-driven architectures that accurately capture domain knowledge, enforce business invariants, and provide adaptable models that evolve with changing business requirements.

Backstory: Drawing on over 15 years of experience implementing complex enterprise systems across diverse industries, I've developed deep expertise in strategic and tactical domain modeling. My methodical approach balances technical implementation with business needs, emphasizing clean domain boundaries and semantic integrity. I've successfully guided organizations through complex domain transformations by identifying core concepts and designing systems that speak the language of the business. My working style prioritizes correctness, maintainability, and elegant expression of domain concepts, allowing me to navigate even the most intricate business domains with clarity and precision.

Operational Guidelines:
* Prioritize identifying and implementing ubiquitous language patterns consistently across domain models and technical implementations
* Apply tactical DDD patterns (aggregates, entities, value objects, repositories, domain services) with precision to solve specific domain problems
* Enforce strict aggregate boundaries to maintain data consistency and transaction isolation
* Design event streams that capture complete domain state transitions and history
* Recommend appropriate bounded context integration patterns based on team relationships and communication needs
* Balance technical constraints with business requirements to create pragmatic domain models
* Leverage value objects to encapsulate related attributes and validation rules
* Use enumerations strategically to model discrete states, categories, and classification schemes
* Provide clear guidance on maintaining consistency within transaction boundaries
* Focus on designing models that evolve gracefully with changing business requirements"""

    def _build_task_guidelines_prompt(self) -> str:
        return """In your current event storming model, you need to write actions to add elements inside a particular Bounded Context following the structure provided by the user.

Please adhere to the following guidelines:

Data Type Rules:
1. For Aggregate properties, use:
   - Basic Java types: String, Long, Integer, Double, Boolean, Date
   - Custom types must be defined as either Enumeration or ValueObject.
2. For collections, use the 'List<ClassName>' syntax (e.g., List<String>).

Type Reference and Enumeration Rules:
3. When to use Enumerations:
   - When a property represents a fixed set of values or categories.
   - When the property value must be one of a predefined list.
   - When the property name ends with words such as Type, Status, Category, Level, Phase, or Stage.
   - Specifically, when storing state or status information, an Enumeration must be used.
   Example cases:
     • category → BookCategory (Enumeration)
     • status → OrderStatus (Enumeration)
     • type → ProductType (Enumeration)
     • level → MembershipLevel (Enumeration)
     • paymentMethod → PaymentMethod (Enumeration)

4. When to use ValueObjects:
   - When a group of related properties forms a meaningful concept and immutability is required.
   - **All ValueObjects must be directly associated with their Aggregate.** Do not define ValueObjects that are nested within or used by other ValueObjects.
   - Unless there is a special case, avoid creating meaningless ValueObjects. Instead, incorporate such properties directly within the Aggregate.
   - Refrain from creating an excessive number of ValueObjects.
   Example cases:
     • address → Address (street, city, zipCode)
     • period → DateRange (startDate, endDate)
     • money → Money (amount, currency)
     • contact → ContactInfo (phone, email, address)

Traceability Rules:
8. For every created element (Aggregate, ValueObject, Enumeration) and each of their properties, you MUST provide a `refs`.
9. The `refs` links the generated element back to the specific text in the "Functional Requirements" it was derived from. The requirements will have line numbers prepended to each line (e.g., "1: ...", "2: ...").
10. The format for `refs` is an array of Position Arrays: `[[[<start_line_number>, "<start_word_combination>"], [<end_line_number>, "<end_word_combination>"]]]`.
11. The "word_combination" should be MINIMAL words (1-2 words) that uniquely identify the position in the line. Use the shortest possible phrase that can locate the specific part of requirements. For example: "course" instead of "create a course", "title" instead of "provide a title".
12. If an element is inferred from multiple places, you can add multiple Position Arrays to the list. Example: `[[[10, "title"], [10, "price"]], [[25, "courses"], [26, "title"]]]`

Naming and Language Conventions:
13. Object names (classes, properties, methods) must be in English.
14. Supporting content (aliases, descriptions) must adhere to the preferred language setting.

Structural Rules:
15. Aggregates:
   - Must have exactly one primary key attribute.
   - For composite keys, create a ValueObject and use it as the primary key.
   - Reference other Aggregates using their class names rather than IDs.
   - Avoid creating separate transaction objects when the main Aggregate can manage its lifecycle. Do not duplicate properties by creating Transaction ValueObjects if they overlap with the main Aggregate.
   - Use the Aggregate root to manage state transitions and history. Consider Event Sourcing for tracking historical changes if needed.

16. ValueObjects:
   - Must be directly linked to an Aggregate; avoid defining ValueObjects that are internally nested or that represent subordinate structures.
   - Should encapsulate multiple, related properties and be immutable.
   - Prevent the creation of trivial or redundant ValueObjects by including properties directly in the Aggregate unless a special case dictates otherwise.
   - Do not generate an excessive number of ValueObjects.

Event-Driven Design Considerations:
17. Domain Events Integration:
   - Consider how domain events influence aggregate state transitions and properties.
   - Ensure aggregates can produce and handle relevant domain events described in the functional requirements.
   - Include properties that support event sourcing and state tracking when events indicate state changes.
   - Map event data to appropriate aggregate properties and value objects.

18. Context Relationship Considerations:
    - Analyze context relationships (Pub/Sub, API calls, shared databases) to understand external dependencies.
    - For Pub/Sub relationships, ensure aggregates can publish and consume relevant events.
    - Consider how external context interactions affect aggregate design and required properties.
    - Include properties needed for integration patterns described in context relationships.

Creation Guidelines:
19. Create only:
    - Aggregates listed under 'Aggregate to create'.
    - All ValueObjects from the provided structure that have a direct association with the Aggregate.
    - Enumerations for any property requiring a fixed set of values.
    - All supporting types needed for the properties.
    - Properties that support domain events and context integration patterns.

20. Property Type Selection:
    - Opt for specific types over generic ones.
    - Consider event payload requirements when defining properties.
    - Example mappings:
      • startDate → Date
      • currentCapacity → Integer
      • price → Double
      • category → Enumeration
      • status → Enumeration

Type Dependency Resolution:
21. Before finalizing your result:
    - Validate all property types.
    - Create Enumerations for properties representing classifications, statuses, or types.
    - Ensure that all custom types are clearly defined.
    - Verify the appropriate usage of ValueObjects versus Enumerations.
    - Confirm that aggregate design supports required domain events and context interactions.

Constraints:
22. Rules:
    - Only reference existing Aggregates without altering them.
    - Do not recreate types that already exist in the system.
    - Avoid including comments in the output JSON object.
    - Prevent duplicate elements in the model.
    - Do not use ValueObjects for properties that should be defined as Enumerations.
    - Refrain from appending type names (e.g., 'Enumeration' or 'ValueObject') to object names; use base names only (e.g., 'BookStatus' rather than 'BookStatusEnumeration').
    - Ensure names are unique across both new and existing elements, with no duplicates.

23. Required Elements:
    - Every ValueObject and Enumeration must be directly associated with an Aggregate.
    - Every generated ValueObject and Enumeration must be included as a named attribute in at least one Aggregate.
    - Implement all elements specified in the user's structure.
    - Accurately map all relationships.
    - Provide corresponding definitions for all custom types.
    - Ensure aggregate design supports the event flows and context relationships described in functional requirements.

24. Evaluate context relationships and integration patterns:
    - Consider how Pub/Sub, API calls, or shared database patterns affect aggregate design.
    - Include properties needed for external system integration.
    - Ensure aggregate boundaries align with context relationship patterns.
25. For each generated element and its properties, determine the `refs` by finding the exact line and minimal word combination in the functional requirements that justifies its creation. Use the shortest possible phrase (1-2 words) that uniquely identifies the position.
"""

    def _build_inference_guidelines_prompt(self) -> str:
        return """
Inference Guidelines:
1. The reasoning should directly inform the output result with specific design decisions rather than generic strategies.
2. Begin by thoroughly understanding the task requirements and the overall domain context.
3. Evaluate key design aspects, including domain alignment, adherence to Domain-Driven Design (DDD) principles, and technical feasibility.
4. Analyze the relationships and dependencies between Aggregates, ValueObjects, and Enumerations precisely.
5. Ensure that all design decisions comply with DDD best practices.
6. When properties represent state or status information, enforce the use of Enumerations to clearly define valid values.
7. Verify that every ValueObject and Enumeration is directly associated with an Aggregate; avoid nested or subordinate ValueObject definitions.
8. Avoid creating unnecessary or excessive ValueObjects; integrate properties directly into the Aggregate unless a distinct ValueObject offers significant encapsulation.
9. Consider domain events and their impact on aggregate design:
   - Analyze which events the aggregate should produce or consume.
   - Ensure aggregate properties support event-driven state transitions.
   - Include necessary properties for event sourcing and audit trails when indicated by events.
10. Evaluate context relationships and integration patterns:
    - Consider how Pub/Sub, API calls, or shared database patterns affect aggregate design.
    - Include properties needed for external system integration.
    - Ensure aggregate boundaries align with context relationship patterns.
"""

    def _build_request_format_prompt(self) -> str:
        return ESValueSummarizeWithFilter.get_guide_prompt()

    def _build_json_response_format(self) -> str:
        return """
{
    "inference": "<inference>",
    "result": {
        // aggregateId can be used when defining Enumeration, ValueObject that belong to an Aggregate.
        "aggregateActions": [
            {
                // Write the ActionName that you utilized in the previous steps
                "actionName": "<actionName>",
                "objectType": "Aggregate",
                "ids": {
                    "aggregateId": "<aggregateId>"
                },
                "args": {
                    "aggregateName": "<aggregateName>",
                    "aggregateAlias": "<aggregateAlias>",
                    "refs": [[["<start_line_number>", "<minimal_start_phrase>"], ["<end_line_number>", "<minimal_end_phrase>"]]],

                    "properties": [
                        {
                            "name": "<propertyName>",
                            ["type": "<propertyType>"], // If the type is String, do not specify the type.
                            ["isKey": true], // Write only if there is a primary key.
                            "refs": [[["<start_line_number>", "<minimal_start_phrase>"], ["<end_line_number>", "<minimal_end_phrase>"]]]
                        }
                    ]
                }
            }
        ],

        // ValueObjects are immutable objects defined by their attributes rather than their identity.
        // They are used to group related attributes that should be treated as a single unit.
        "valueObjectActions": [
            {
                "actionName": "<actionName>",
                "objectType": "ValueObject",
                "ids": {
                    "aggregateId": "<aggregateId>",
                    "valueObjectId": "<valueObjectId>"
                },
                "args": {
                    "valueObjectName": "<valueObjectName>",
                    "valueObjectAlias": "<valueObjectAlias>",
                    "refs": [[["<start_line_number>", "<minimal_start_phrase>"], ["<end_line_number>", "<minimal_end_phrase>"]]],

                    "properties": [
                        {
                            "name": "<propertyName>",
                            ["type": "<propertyType>"], // If the type is String, do not specify the type.
                            ["isKey": true], // Write only if there is a primary key.
                            ["isForeignProperty": true], // Whether it is a foreign key. Write only if this attribute references another table's attribute.
                            "refs": [[["<start_line_number>", "<minimal_start_phrase>"], ["<end_line_number>", "<minimal_end_phrase>"]]]
                        }
                    ]
                }
            }
        ],

        // If the type of property you want to add to the aggregate does not have an appropriate default Java type, you can create a new type as an enumeration.
        "enumerationActions": [
            {
                "actionName": "<actionName>",
                "objectType": "Enumeration",
                "ids": {
                    "aggregateId": "<aggregateId>",
                    "enumerationId": "<enumerationId>"
                },
                "args": {
                    "enumerationName": "<enumerationName>",
                    "enumerationAlias": "<enumerationAlias>",
                    "refs": [[["<start_line_number>", "<minimal_start_phrase>"], ["<end_line_number>", "<minimal_end_phrase>"]]],
                    
                    "properties": [
                        {
                            "name": "<propertyName>", // Must be in English
                            "refs": [[["<start_line_number>", "<minimal_start_phrase>"], ["<end_line_number>", "<minimal_end_phrase>"]]]
                        }
                    ]
                }
            }
        ]
    }
}
"""

    def _build_json_example_input_format(self) -> Optional[Dict[str, Any]]:
        return {
            "Summarized Existing EventStorming Model": {
                "deletedProperties": ESValueSummarizeWithFilter.KEY_FILTER_TEMPLATES["aggregateOuterStickers"],
                "boundedContexts": [
                    {
                        "id": "bc-course",
                        "name": "CourseManagement",
                        "actors": [
                            { "id": "act-instructor", "name": "Instructor" },
                            { "id": "act-student", "name": "Student" }
                        ],
                        "aggregates": [
                            {
                                "id": "agg-user",
                                "name": "User",
                                "properties": [
                                    { "name": "userId", "type": "Long", "isKey": True },
                                    { "name": "name" },
                                    { "name": "email", "type": "String" }
                                ],
                                "entities": [],
                                "enumerations": [],
                                "valueObjects": []
                            }
                        ]
                    }
                ],
            },
            
            "Bounded Context to Generate Actions": "CourseManagement",
            
            "Functional Requirements": """
1: # Bounded Context Overview: CourseManagement
2: 
3: ## Role
4: This context is responsible for the entire lifecycle of a course, including its creation, management, and tracking. It handles course content, instructor assignments, pricing, and status changes (e.g., Draft, Published, Archived). The primary user is the Instructor.
5: 
6: ## User Story
7: As an instructor, I want to create and manage my courses on the platform. When creating a course, I need to provide a title, description, and price. The course should initially be in a 'Draft' state. Once I'm ready, I can 'Publish' the course, making it available for students to enroll. If a course is outdated, I should be able to 'Archive' it, so it's no longer available for new enrollments but remains accessible to already enrolled students.
8: 
9: ## Key Events
10: - CourseCreated
11: - CoursePublished
12: - CoursePriceUpdated
13: - CourseArchived
14: - StudentEnrolled
15: 
16: ## DDL
17: ```sql
18: -- Courses Table
19: CREATE TABLE courses (
20:     course_id BIGINT AUTO_INCREMENT PRIMARY KEY,
21:     title VARCHAR(255) NOT NULL,
22:     description TEXT,
23:     instructor_id BIGINT NOT NULL,
24:     status ENUM('DRAFT', 'PUBLISHED', 'ARCHIVED') NOT NULL DEFAULT 'DRAFT',
25:     price_amount DECIMAL(10, 2),
26:     price_currency VARCHAR(3),
27:     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
28:     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
29:     INDEX idx_instructor_id (instructor_id)
30: );
31: ```
32: 
33: ## Context Relations
34: ### CourseToPayment
35: - **Type**: API Call
36: - **Direction**: calls
37: - **Target Context**: PaymentService
38: - **Reason**: When a student enrolls in a course, the CourseManagement context needs to initiate a payment process synchronously.
39: - **Interaction Pattern**: Makes a REST API call to the PaymentService to process the course fee.
""",
            
            "Suggested Structure": [
                {
                    "aggregate": {
                        "name": "Course",
                        "alias": "Online Course"
                    },
                    "enumerations": [
                        {
                            "name": "CourseStatus",
                            "alias": "Course Status"
                        }
                    ],
                    "valueObjects": [
                        {
                            "name": "CoursePrice",
                            "alias": "Course Price"
                        }
                    ]
                }
            ],
            
            "Aggregate to create": {
                "name": "Course",
                "alias": "Online Course"
            }
        }

    def _build_json_example_output_format(self) -> Dict[str, Any]:
        return {
            "inference": "The Course aggregate is designed to manage educational content, encapsulating its core attributes and lifecycle. A `CourseStatus` enumeration is introduced to manage the state (Draft, Published, Archived), and a `CoursePrice` value object is created to handle monetary values consistently. This structure directly supports the functional requirements for creating, pricing, and managing online courses.",
            "result": {
                "aggregateActions": [
                    {
                        "actionName": "CreateCourseAggregate",
                        "objectType": "Aggregate",
                        "ids": {
                            "aggregateId": "agg-course"
                        },
                        "args": {
                            "aggregateName": "Course",
                            "aggregateAlias": "Online Course",
                            "refs": [[[4, "lifecycle"], [4, "course"]]],
                            "properties": [
                                { "name": "courseId", "type": "Long", "isKey": True, "refs": [[[20, "course_id"], [20, "KEY"]]] },
                                { "name": "title", "refs": [[[7, "provide"], [7, "title"]]] },
                                { "name": "description", "type": "String", "refs": [[[7, "title"], [7, "price"]]] },
                                { "name": "instructorId", "type": "Long", "refs": [[[23, "instructor_id"], [23, "NULL"]]] },
                                { "name": "price", "type": "CoursePrice", "refs": [[[7, "description"], [7, "price"]]] },
                                { "name": "status", "type": "CourseStatus", "refs": [[[4, "status"], [4, "changes"]]] },
                                { "name": "createdAt", "type": "Date", "refs": [[[27, "created_at"], [27, "DEFAULT"]]] },
                                { "name": "updatedAt", "type": "Date", "refs": [[[28, "updated_at"], [28, "DEFAULT"]]] }
                            ]
                        }
                    }
                ],
                "valueObjectActions": [
                    {
                        "actionName": "CreateCoursePriceVO",
                        "objectType": "ValueObject",
                        "ids": {
                            "aggregateId": "agg-course",
                            "valueObjectId": "vo-course-price"
                        },
                        "args": {
                            "valueObjectName": "CoursePrice",
                            "valueObjectAlias": "Course Price",
                            "refs": [[[7, "price"], [7, "price"]]],
                            "properties": [
                                { "name": "amount", "type": "Double", "refs": [[[25, "price_amount"], [25, "(10, 2)"]]] },
                                { "name": "currency", "refs": [[[26, "price_currency"], [26, "(3)"]]] }
                            ]
                        }
                    }
                ],
                "enumerationActions": [
                    {
                        "actionName": "CreateCourseStatusEnum",
                        "objectType": "Enumeration",
                        "ids": {
                            "aggregateId": "agg-course",
                            "enumerationId": "enum-course-status"
                        },
                        "args": {
                            "enumerationName": "CourseStatus",
                            "enumerationAlias": "Course Status",
                            "refs": [[[4, "status"], [4, "status"]]],
                            "properties": [
                                { "name": "DRAFT", "refs": [[[7, "Draft"], [7, "state"]]] },
                                { "name": "PUBLISHED", "refs": [[[7, "Publish"], [7, "course"]]] },
                                { "name": "ARCHIVED", "refs": [[[7, "Archive"], [7, "it"]]] }
                            ]
                        }
                    }
                ]
            }
        }
    
    def _build_json_user_query_input_format(self) -> Dict[str, Any]:
        inputs = self.client.get("inputs")
        
        final_check_prompt = f"""
1. Language and Naming:
   * Object names (classes, methods, properties): English only
   * Alias properties: {self.client.get("preferredLanguage")} only
   * Follow consistent naming patterns
   * Use domain-specific terminology

2. Event-Driven Design:
   * Consider domain events that influence aggregate state and properties
   * Include properties needed for event sourcing and state tracking
   * Ensure aggregates support required event publishing and consumption

3. Context Integration:
   * Analyze context relationships (Pub/Sub, API calls) for integration requirements
   * Include properties needed for external system interactions
   * Design aggregates to support described integration patterns
"""

        extracted_ddl_fields = inputs.get("extractedDdlFields")
        if extracted_ddl_fields:
            fields_str = ", ".join(extracted_ddl_fields)
            final_check_prompt += f"""
4. DDL Field Requirement:
   * The following fields from the DDL must be included in at least one of the generated Aggregates or ValueObjects: {fields_str}
"""
        
        return {
            "Summarized Existing EventStorming Model": inputs.get("summarizedESValue"),

            "Bounded Context to Generate Actions": inputs.get("targetBoundedContext").get("name"),

            "Functional Requirements": inputs.get("description"),

            "Suggested Structure": inputs.get("draftOption"),

            "Aggregate to create": inputs.get("targetAggregate"),

            "Final Check": final_check_prompt,
        }