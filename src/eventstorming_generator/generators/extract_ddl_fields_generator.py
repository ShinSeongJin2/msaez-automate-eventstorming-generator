from typing import Any, Dict, Optional
from .base import BaseGenerator
from ..models import ExtractDDLFieldsGeneratorOutput

class ExtractDDLFieldsGenerator(BaseGenerator):
    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        self.inputs_types_to_check = ["ddl"]
        super().__init__(model_name, model_kwargs, client, structured_output_class=ExtractDDLFieldsGeneratorOutput)

    def _build_agent_role_prompt(self) -> str:
        return """Role: SQL Parsing Specialist

Goal: To accurately extract all field (column) names from provided Data Definition Language (DDL) text, regardless of SQL dialect or formatting inconsistencies. Your primary function is to identify all `CREATE TABLE` statements and list the columns defined within them.

Backstory: I am a highly specialized parsing engine designed to understand and deconstruct SQL DDL. I have been trained on a vast corpus of SQL schemas from various databases like MySQL, PostgreSQL, Oracle, and SQL Server. I can cut through complex formatting, comments, and varied syntax to reliably identify the fundamental column definitions that form the blueprint of a database table. My sole focus is precision and completeness in field extraction.

Operational Guidelines:
* Scan the input text specifically for `CREATE TABLE` statements.
* For each table found, meticulously parse the column definitions between the parentheses `()`.
* Extract only the column names. Ignore data types, constraints (like `NOT NULL`, `PRIMARY KEY`, `FOREIGN KEY`), default values, and comments.
* If the DDL contains multiple `CREATE TABLE` statements, extract and consolidate column names from all of them into a single list.
* Do not infer or create any names. Only extract what is explicitly defined in the DDL.
* Return an empty list if no `CREATE TABLE` statements are found or if the DDL is empty."""

    def _build_task_guidelines_prompt(self) -> str:
        return """Your task is to analyze the provided DDL (Data Definition Language) string and extract every field name from it.

Please adhere to the following guidelines:

1.  **Focus only on column names:** Identify all `CREATE TABLE` statements and extract the names of the columns defined within them.
2.  **Ignore everything else:** Do not include data types, constraints (`PRIMARY KEY`, `NOT NULL`, etc.), table names, or comments in your output list.
3.  **Consolidate all fields:** If there are multiple tables defined, gather all column names from all tables into one single list.
4.  **Handle inconsistencies:** The DDL might have inconsistent formatting, comments, or vary in SQL dialect. Your process should be robust enough to handle this.
5.  **No DDL, no fields:** If the input DDL is empty or contains no `CREATE TABLE` statements, return an empty list for `ddl_fields`.
6.  **Uniqueness:** Ensure the final list of fields contains no duplicates. Each field name should appear only once, even if it's defined in multiple tables."""

    def _build_inference_guidelines_prompt(self) -> str:
        return """
Inference Guidelines:
1.  **State the Goal:** Begin by stating the primary goal, which is to extract all unique column names from the provided DDL.
2.  **Describe the Process:** Briefly explain the steps taken, such as scanning for `CREATE TABLE` statements, parsing the column definitions, and filtering out non-column name elements.
3.  **Mention Tables Found (Optional):** If useful for clarity, mention the names of the tables from which fields were extracted.
4.  **Confirm Consolidation:** Note that fields from all identified tables have been consolidated into a single, unique list.
5.  **Acknowledge Empty Input:** If the DDL was empty or lacked `CREATE TABLE` statements, explicitly state that this is why the field list is empty.
"""

    def _build_request_format_prompt(self) -> str:
        return ""

    def _build_json_response_format(self) -> str:
        return """
{
    "inference": "<inference>",
    "result": {
        "ddl_fields": [
            "<field_name_1>",
            "<field_name_2>"
        ]
    }
}
"""

    def _build_json_example_input_format(self) -> Optional[Dict[str, Any]]:
        return {
            "DDL": """
-- Courses Table
CREATE TABLE `courses` (
    `course_id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    instructor_id BIGINT NOT NULL,
    -- Status of the course
    status ENUM('DRAFT', 'PUBLISHED', 'ARCHIVED') NOT NULL DEFAULT 'DRAFT',
    price_amount DECIMAL(10, 2),
    price_currency VARCHAR(3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_instructor_id (instructor_id)
);

-- Table for tracking student enrollments
CREATE TABLE enrollments(
    enrollment_id BIGINT PRIMARY KEY,
    student_id BIGINT,
    course_id BIGINT, -- Foreign key to courses
    enrollment_date DATE
);
"""
        }

    def _build_json_example_output_format(self) -> Dict[str, Any]:
        return {
            "inference": "I have scanned the provided DDL, identified two tables: `courses` and `enrollments`. I extracted all column names from both definitions, ignored data types and constraints, and consolidated them into a single unique list.",
            "result": {
                "ddl_fields": [
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
                    "enrollment_date"
                ]
            }
        }
    
    def _build_json_user_query_input_format(self) -> Dict[str, Any]:
        inputs = self.client.get("inputs")
        return {
            "DDL": inputs.get("ddl")
        } 