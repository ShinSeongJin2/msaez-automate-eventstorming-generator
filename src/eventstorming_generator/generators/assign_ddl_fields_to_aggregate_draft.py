from typing import Any, Dict, Optional
from .base import BaseGenerator
from ..models import AssignDDLFieldsToAggregateDraftOutput

class AssignDDLFieldsToAggregateDraft(BaseGenerator):
    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        self.inputs_types_to_check = ["description", "aggregateDrafts", "allDdlFields"]
        super().__init__(model_name, model_kwargs, client, structured_output_class=AssignDDLFieldsToAggregateDraftOutput)

    def _build_agent_role_prompt(self) -> str:
        return """Role: Domain-Driven Design (DDD) Data Modeling Specialist

Goal: To analyze the functional requirements and aggregate draft structures within a bounded context, then intelligently assign DDL fields to the most appropriate aggregates based on domain semantics and data relationships. Your primary function is to ensure that every field from the DDL is assigned to exactly one aggregate, creating a complete and semantically correct mapping.

Backstory: With extensive experience in database design and domain modeling, I specialize in bridging the gap between technical database schemas and business domain models. I understand how to interpret DDL field names, data types, and relationships to determine which aggregate should own which data. My expertise lies in analyzing business context, understanding aggregate boundaries, and making intelligent decisions about data ownership that maintain both technical correctness and domain coherence.

Operational Guidelines:
* **Analyze Domain Context:** Thoroughly understand the functional requirements and business context to make informed decisions about data ownership.
* **Respect Aggregate Boundaries:** Ensure that each field is assigned to the aggregate that naturally owns that data from a business perspective.
* **Maintain Completeness:** Every DDL field must be assigned to exactly one aggregate - no field should be left unassigned.
* **Consider Relationships:** Analyze field naming patterns (e.g., foreign keys, timestamps, status fields) to determine logical ownership.
* **Prioritize Semantic Cohesion:** Group related fields together and assign them to aggregates where they form a cohesive concept.
* **Handle Edge Cases:** When field ownership is ambiguous, prioritize the aggregate that would most directly use or modify that data.
* **Provide Clear Reasoning:** Document your decision-making process for each assignment to ensure transparency and maintainability."""

    def _build_task_guidelines_prompt(self) -> str:
        return """Your task is to analyze a bounded context's DDL fields and assign each field to the most appropriate aggregate draft.

You will be given:
1. **Functional Requirements:** The business context and domain description for the bounded context.
2. **Aggregate Drafts:** A list of planned aggregates with their names and basic structure information.
3. **All DDL Fields:** A complete list of field names extracted from the bounded context's DDL.

Please adhere to the following guidelines:

Assignment Rules:
1. **Complete Coverage:** Every field in the "All DDL Fields" list must be assigned to exactly one aggregate.
2. **No Duplicates:** Each field should appear only once across all aggregate assignments.
3. **Semantic Alignment:** Assign fields to aggregates based on business logic and domain semantics, not just naming patterns.
4. **Primary Entity Focus:** Core identifying fields (IDs, primary keys) should typically go to their corresponding aggregate.

Field Analysis Guidelines:
5. **ID Fields:** Fields ending with "_id" or containing "id" typically belong to the aggregate they identify or reference.
6. **Timestamp Fields:** Created/updated timestamps usually belong to the main entity they track.
7. **Status/State Fields:** Status and state fields belong to the aggregate whose lifecycle they describe.
8. **Descriptive Fields:** Name, description, and similar fields belong to the entity they describe.
9. **Foreign Key Analysis:** Foreign key fields should be assigned based on the relationship direction and ownership.

Domain Context Considerations:
10. **Business Logic:** Consider which aggregate would naturally create, modify, or validate each field.
11. **Transaction Boundaries:** Fields that change together in business operations should typically be in the same aggregate.
12. **Data Lifecycle:** Consider the lifecycle of data - which aggregate controls when this data is created, updated, or deleted.

Output Requirements:
13. **Justify Assignments:** Provide clear reasoning for your field assignments, especially for ambiguous cases.
14. **Ensure Completeness:** Verify that all input DDL fields are covered in your output assignments.
15. **Handle Missing Aggregates:** If a field clearly belongs to an aggregate concept not in the draft list, assign it to the most closely related existing aggregate and note this in your reasoning."""

    def _build_inference_guidelines_prompt(self) -> str:
        return """
Inference Guidelines:
1. **Start with Context Analysis:** Begin by understanding the overall business domain and the role of each planned aggregate.
2. **Group Related Fields:** Identify clusters of related fields that naturally belong together.
3. **Apply Domain Logic:** Use business understanding to determine which aggregate should own each field or field group.
4. **Handle Ambiguous Cases:** For fields that could belong to multiple aggregates, explain your reasoning and prioritize based on:
   - Which aggregate would most directly use the field
   - Which aggregate controls the field's lifecycle
   - Business transaction boundaries
5. **Verify Completeness:** Ensure every DDL field is assigned and no field is duplicated across aggregates.
6. **Document Edge Cases:** Clearly explain any assignments where the field might not perfectly fit the aggregate but represents the best available option.
"""

    def _build_request_format_prompt(self) -> str:
        return ""

    def _build_json_response_format(self) -> str:
        return """
{
    "inference": "<Detailed reasoning for the field assignments, including analysis of the domain context and explanation of assignment decisions>",
    "result": {
        "aggregateFieldAssignments": [
            {
                "aggregateName": "<name_of_aggregate>",
                "ddl_fields": [
                    "<field_name_1>",
                    "<field_name_2>"
                ]
            }
        ]
    }
}
"""

    def _build_json_example_input_format(self) -> Optional[Dict[str, Any]]:
        return {
            "Functional Requirements": """
# Bounded Context Overview: CourseManagement

## Role
This context is responsible for the entire lifecycle of a course, including its creation, management, and tracking. It handles course content, instructor assignments, pricing, and status changes (e.g., Draft, Published, Archived). It also manages student enrollments in courses.

## User Story
As an instructor, I want to create and manage my courses on the platform. When creating a course, I need to provide a title, description, and price. Students can enroll in published courses, and I need to track these enrollments.

## Key Events
- CourseCreated
- CoursePublished  
- CoursePriceUpdated
- CourseArchived
- StudentEnrolled
- StudentDropped
""",
            "Aggregate Drafts": [
                {
                    "name": "Course",
                    "alias": "Online Course"
                },
                {
                    "name": "Enrollment", 
                    "alias": "Course Enrollment"
                }
            ],
            "All DDL Fields": [
                "course_id",
                "title", 
                "description",
                "instructor_id",
                "status",
                "price_amount",
                "price_currency", 
                "created_at",
                "updated_at",
                "enrollment_id",
                "student_id",
                "enrollment_date",
                "completion_status"
            ]
        }

    def _build_json_example_output_format(self) -> Dict[str, Any]:
        return {
            "inference": "I analyzed the CourseManagement domain and assigned fields based on aggregate ownership principles. Course-related fields (course_id, title, description, instructor_id, status, price_amount, price_currency, created_at, updated_at) naturally belong to the Course aggregate as they describe course properties and lifecycle. Enrollment-related fields (enrollment_id, student_id, course_id reference would be handled through relationships, enrollment_date, completion_status) belong to the Enrollment aggregate as they track the student-course relationship and enrollment lifecycle.",
            "result": {
                "aggregateFieldAssignments": [
                    {
                        "aggregateName": "Course",
                        "ddl_fields": [
                            "course_id",
                            "title",
                            "description", 
                            "instructor_id",
                            "status",
                            "price_amount",
                            "price_currency",
                            "created_at",
                            "updated_at"
                        ]
                    },
                    {
                        "aggregateName": "Enrollment",
                        "ddl_fields": [
                            "enrollment_id",
                            "student_id", 
                            "enrollment_date",
                            "completion_status"
                        ]
                    }
                ]
            }
        }
    
    def _build_json_user_query_input_format(self) -> Dict[str, Any]:
        inputs = self.client.get("inputs")
        return {
            "Functional Requirements": inputs.get("description"),
            "Aggregate Drafts": inputs.get("aggregateDrafts"),
            "All DDL Fields": inputs.get("allDdlFields")
        } 