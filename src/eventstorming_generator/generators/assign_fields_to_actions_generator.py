from typing import Any, Dict, Optional
from .base import BaseGenerator
from ..models import AssignFieldsToActionsGeneratorOutput
from ..utils import EsUtils

class AssignFieldsToActionsGenerator(BaseGenerator):
    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        self.inputs_types_to_check = ["description", "existingActions", "missingFields"]
        super().__init__(model_name, model_kwargs, client, structured_output_class=AssignFieldsToActionsGeneratorOutput)

    def _build_agent_role_prompt(self) -> str:
        return """Role: Domain-Driven Design (DDD) Architect & Code Refactoring Specialist

Goal: To logically integrate orphaned fields into an existing domain model structure, ensuring that each field is assigned to the most cohesive Aggregate or Value Object. Your primary function is to analyze a partially complete model, a list of unassigned fields, and the domain's functional requirements to make intelligent, context-aware assignments.

Backstory: With years of experience in evolving large-scale domain models, I specialize in identifying the correct home for business data. I've seen countless models where an initial design missed a few details. My skill lies in my ability to understand the semantic meaning of both the existing model and the missing pieces, allowing me to place new attributes where they logically belong without violating DDD principles like high cohesion and clear aggregate boundaries. I treat the model as a living document and excel at making the necessary adjustments to ensure its integrity and clarity.

Operational Guidelines:
*   **Analyze the Context:** Thoroughly review the functional requirements and the existing structure of Aggregates and Value Objects.
*   **Prioritize Cohesion:** Assign each missing field to the parent (Aggregate or ValueObject) where it fits most naturally and increases the conceptual cohesion of that parent.
*   **Infer Data Types:** Based on field names and context, infer the most appropriate Java data type (e.g., `_id` -> `Long`, `_date` / `_at` -> `Date`, `is_` / `has_` -> `Boolean`, `amount` -> `Double`). When in doubt, default to `String`.
*   **Respect Boundaries:** Do not create new Aggregates or Value Objects. Your task is only to assign fields to the existing ones.
*   **Be Decisive:** Every missing field must be assigned to exactly one parent. Do not leave any fields unassigned.
*   **Explain Your Work:** Clearly document the reasoning for each assignment in the `inference` field, explaining why a field belongs to a specific parent."""

    def _build_task_guidelines_prompt(self) -> str:
        return """Your task is to take a list of "missing fields" and assign each one to the most appropriate existing Aggregate or Value Object.

You will be given:
1.  **Functional Requirements:** The business context for the domain.
2.  **Existing Model Structure:** A list of Aggregates and Value Objects that have already been created, including their current properties.
3.  **Missing Fields:** A list of field names that were specified in the DDL but are not yet present in the model.

Please adhere to the following guidelines:

1.  **Assign Every Field:** You must assign every single field from the "Missing Fields" list to a parent in the "Existing Model Structure".
2.  **Choose the Best Parent:** For each field, analyze its name and the functional requirements to decide which Aggregate or Value Object is its most logical home. Think about which concept the field helps to describe.
3.  **Infer Data Types:** For each field you assign, you must also infer its likely Java data type. Use common naming conventions as clues (e.g., `status` -> `String` or a potential Enum, `createdAt` -> `Date`, `price` -> `Double`, `orderId` -> `Long`). Default to `String` if the type is ambiguous.
4.  **Provide Source References:** For each field you assign, you MUST provide a `sourceReferences` that links the field back to the specific text in the "Functional Requirements" it was derived from. The requirements will have line numbers prepended to each line (e.g., "1: ...", "2: ...").
5.  **Source Reference Format:** The format for `sourceReferences` is an array of Position Arrays: `[[[<start_line_number>, "<start_word_combination>"], [<end_line_number>, "<end_word_combination>"]]]`. The "word_combination" MUST be a direct quote of 2-3 consecutive words from the specified line in the "Functional Requirements" to ensure it can be uniquely located. Avoid using single, common words.
6.  **Structure Your Output:** Group your assignments by the parent they belong to. For each parent, list all the properties you are adding to it.
7.  **Provide Rationale:** In the `inference` section, explain your assignment decisions. For example, "The `disposal_date` and `disposal_reason` fields were assigned to the `Book` aggregate because they directly describe the lifecycle events of a book."
"""

    def _build_inference_guidelines_prompt(self) -> str:
        return """
Inference Guidelines:
1.  **Overall Strategy:** Start by stating your overall approach, which is to assign each missing field based on conceptual cohesion with the existing domain objects.
2.  **Detailed Justification:** For each parent object that receives new fields, provide a clear and concise justification. Explain *why* those specific fields belong to that Aggregate or Value Object, referencing the functional requirements or domain concepts if necessary.
3.  **Address Difficult Cases:** If any assignments were not straightforward, explain the trade-offs you considered and why you chose the final placement.
4.  **Confirm Completeness:** Conclude by confirming that all fields from the input list have been successfully assigned.
"""

    def _build_request_format_prompt(self) -> str:
        return ""

    def _build_json_response_format(self) -> str:
        return """
{
    "inference": "<Detailed reasoning for the assignments>",
    "result": {
        "assignments": [
            {
                "parent_type": "Aggregate",
                "parent_id": "<ID of the parent aggregate>",
                "parent_name": "<Name of the parent aggregate>",
                "properties_to_add": [
                    {
                        "name": "<missing_field_name_1>",
                        "type": "<inferred_java_type>",
                        "sourceReferences": [[["<start_line_number>", "<start_word_combination>"], ["<end_line_number>", "<end_word_combination>"]]]
                    },
                    {
                        "name": "<missing_field_name_2>",
                        "type": "<inferred_java_type>",
                        "sourceReferences": [[["<start_line_number>", "<start_word_combination>"], ["<end_line_number>", "<end_word_combination>"]]]
                    }
                ]
            },
            {
                "parent_type": "ValueObject",
                "parent_id": "<ID of the parent value object>",
                "parent_name": "<Name of the parent value object>",
                "properties_to_add": [
                    {
                        "name": "<missing_field_name_3>",
                        "type": "<inferred_java_type>",
                        "sourceReferences": [[["<start_line_number>", "<start_word_combination>"], ["<end_line_number>", "<end_word_combination>"]]]
                    }
                ]
            }
        ]
    }
}
"""

    def _build_json_example_input_format(self) -> Optional[Dict[str, Any]]:
        return {
            "Functional Requirements": """
1: # Bounded Context Overview: CourseManagement
2: 
3: ## Role
4: This context is responsible for the entire lifecycle of a course, including its creation, management, and tracking. It handles course content, instructor assignments, pricing, and status changes (e.g., Draft, Published, Archived). The primary user is the Instructor.
5: 
6: ## User Story
7: As an instructor, I want to create and manage my courses on the platform. When creating a course, I need to provide a title, description, and price. The course should initially be in a 'Draft' state. Once I'm ready, I can 'Publish' the course, making it available for students to enroll. If a course is outdated, I should be able to 'Archive' it, so it's no longer available for new enrollments but remains accessible to already enrolled students.
8: 
9: ## DDL
10: ```sql
11: -- Courses Table
12: CREATE TABLE courses (
13:     course_id BIGINT AUTO_INCREMENT PRIMARY KEY,
14:     title VARCHAR(255) NOT NULL,
15:     description TEXT,
16:     instructor_id BIGINT NOT NULL,
17:     status ENUM('DRAFT', 'PUBLISHED', 'ARCHIVED') NOT NULL DEFAULT 'DRAFT',
18:     price_amount DECIMAL(10, 2),
19:     price_currency VARCHAR(3),
20:     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
21:     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
22:     INDEX idx_instructor_id (instructor_id)
23: );
24: ```
""",
            "Existing Model Structure": [
                {
                    "actionName": "CreateCourseAggregate",
                    "objectType": "Aggregate",
                    "ids": { "aggregateId": "agg-course" },
                    "args": {
                        "aggregateName": "Course",
                        "properties": [
                            { "name": "courseId", "type": "Long", "isKey": True },
                            { "name": "title" },
                            { "name": "status", "type": "CourseStatus" }
                        ]
                    }
                },
                {
                    "actionName": "CreateCoursePriceVO",
                    "objectType": "ValueObject",
                    "ids": { "aggregateId": "agg-course", "valueObjectId": "vo-course-price" },
                    "args": {
                        "valueObjectName": "CoursePrice",
                        "properties": [
                            { "name": "amount", "type": "Double" }
                        ]
                    }
                }
            ],
            "Missing Fields": [
                "description",
                "instructor_id",
                "price_currency",
                "created_at",
                "updated_at"
            ]
        }

    def _build_json_example_output_format(self) -> Dict[str, Any]:
        return {
            "inference": "I have assigned the missing fields to the most logical parents. `description`, `instructor_id`, `created_at`, and `updated_at` are core attributes of the Course itself and belong in the `Course` aggregate. The `price_currency` field is an essential part of the price concept and belongs in the `CoursePrice` value object to ensure the price is always represented as a complete monetary value.",
            "result": {
                "assignments": [
                    {
                        "parent_type": "Aggregate",
                        "parent_id": "agg-course",
                        "parent_name": "Course",
                        "properties_to_add": [
                            { "name": "description", "type": "String", "sourceReferences": [[["7", "provide a title"], ["7", "description, and price"]]] },
                            { "name": "instructor_id", "type": "Long", "sourceReferences": [[["16", "instructor_id BIGINT"], ["16", "BIGINT NOT NULL"]]] },
                            { "name": "created_at", "type": "Date", "sourceReferences": [[["20", "created_at TIMESTAMP"], ["20", "TIMESTAMP DEFAULT"]]] },
                            { "name": "updated_at", "type": "Date", "sourceReferences": [[["21", "updated_at TIMESTAMP"], ["21", "TIMESTAMP ON"]]] }
                        ]
                    },
                    {
                        "parent_type": "ValueObject",
                        "parent_id": "vo-course-price",
                        "parent_name": "CoursePrice",
                        "properties_to_add": [
                            { "name": "price_currency", "type": "String", "sourceReferences": [[["19", "price_currency VARCHAR"], ["19", "VARCHAR(3)"]]] }
                        ]
                    }
                ]
            }
        }
    
    def _build_json_user_query_input_format(self) -> Dict[str, Any]:
        inputs = self.client.get("inputs")
        
        # Add line numbers to functional requirements for sourceReferences
        description = inputs.get("description", "")
        line_numbered_description = EsUtils.add_line_numbers_to_description(description)
        
        return {
            "Functional Requirements": line_numbered_description,
            "Existing Model Structure": inputs.get("existingActions"),
            "Missing Fields": inputs.get("missingFields")
        } 