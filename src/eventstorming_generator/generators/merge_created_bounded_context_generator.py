from typing import Any, Dict, Optional

from .xml_base import XmlBaseGenerator
from ..utils import XmlUtil
from ..models import MergeCreatedBoundedContextGeneratorOutput

class MergeCreatedBoundedContextGenerator(XmlBaseGenerator):
    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        self.inputs_types_to_check = ["boundedContexts"]
        super().__init__(model_name, MergeCreatedBoundedContextGeneratorOutput, model_kwargs, client)

    def _build_persona_info(self) -> Dict[str, str]:
        return {
            "persona": "Expert Domain-Driven Design (DDD) Architect specializing in Bounded Context consolidation",
            "goal": "To analyze multiple sets of Bounded Contexts and intelligently merge duplicates or overlapping contexts while preserving distinct contexts, ensuring optimal domain decomposition.",
            "backstory": "I am a highly experienced domain architect with deep expertise in identifying and resolving duplicate or overlapping bounded contexts that emerge from distributed analysis. I excel at recognizing semantic similarities, consolidating redundant contexts, and ensuring the final bounded context model maintains high cohesion and low coupling. My expertise includes duplicate detection across naming variations, semantic analysis of context responsibilities, strategic merging while preserving unique characteristics, and maintaining DDD principles throughout the consolidation process."
        }
        
    def _build_task_instruction_prompt(self) -> str:
        return """<instruction>
    <core_instructions>
        <title>Bounded Context Consolidation and Deduplication Task</title>
        <task_description>Your task is to analyze multiple sets of Bounded Contexts that were created from chunked requirements analysis and intelligently merge duplicates or overlapping contexts. The goal is to produce a consolidated, non-redundant set of bounded contexts while preserving distinct contexts and maintaining DDD principles.</task_description>
        
        <input_description>
            <title>You will receive user inputs containing:</title>
            <item id="1">**Bounded Contexts:** A list of bounded contexts that may contain duplicates or overlapping responsibilities</item>
        </input_description>

        <guidelines>
            <title>Bounded Context Consolidation Guidelines</title>
            
            <section id="duplicate_detection">
                <title>Duplicate Detection Criteria</title>
                <rule id="1">**Name Similarity:** Identify contexts with identical or semantically similar names (e.g., "OrderManagement" vs "OrderProcessing", "UserAuth" vs "Authentication")</rule>
                <rule id="2">**Responsibility Overlap:** Detect contexts that manage the same or highly overlapping business capabilities</rule>
                <rule id="3">**Data Ownership Collision:** Identify contexts claiming ownership of the same core entities</rule>
                <rule id="4">**Functional Redundancy:** Recognize contexts with duplicate or redundant functionalities in their descriptions</rule>
                <rule id="5">**Domain Classification Match:** Consider contexts with the same domain importance when evaluating potential duplicates</rule>
            </section>

            <section id="merging_strategy">
                <title>Merging Strategy</title>
                
                <rule id="1">
                    <title>When to Merge</title>
                    <criteria>
                        <item>Contexts have the same or very similar core purpose</item>
                        <item>Contexts would manage the same primary entities</item>
                        <item>Descriptions indicate overlapping responsibilities (>70% overlap)</item>
                        <item>Contexts represent the same business capability with different naming</item>
                    </criteria>
                </rule>
                
                <rule id="2">
                    <title>How to Merge</title>
                    <steps>
                        <step id="a">**Name Selection:** Choose the most clear and comprehensive name, or create a new name that better represents the unified context</step>
                        <step id="b">**Alias Consolidation:** Select or combine aliases to best represent the merged context</step>
                        <step id="c">**Importance Determination:** Prioritize the highest importance level among duplicates (Core Domain > Supporting Domain > Generic Domain)</step>
                        <step id="d">**Description Synthesis:** Combine and synthesize descriptions to include all unique responsibilities while removing redundancies</step>
                    </steps>
                </rule>
                
                <rule id="3">
                    <title>When NOT to Merge</title>
                    <criteria>
                        <item>Contexts serve different aspects of similar domains (e.g., "OrderProcessing" and "OrderFulfillment" are distinct)</item>
                        <item>Contexts have different data ownership despite similar names</item>
                        <item>Contexts operate at different levels or phases of a process</item>
                        <item>Contexts have significantly different domain importance classifications with good reason</item>
                        <item>Maintaining separation provides better cohesion and autonomy</item>
                    </criteria>
                </rule>
            </section>

            <section id="consolidation_principles">
                <title>Consolidation Principles</title>
                <rule id="1">**Preserve Distinct Contexts:** Do not over-merge; maintain genuinely distinct bounded contexts</rule>
                <rule id="2">**Maintain High Cohesion:** Ensure merged contexts remain cohesive and focused</rule>
                <rule id="3">**Avoid Over-fragmentation:** Consolidate truly redundant contexts to prevent unnecessary complexity</rule>
                <rule id="4">**Respect DDD Principles:** Ensure merged contexts still follow high cohesion, low coupling, and single responsibility</rule>
                <rule id="5">**Optimize Context Count:** Aim for the optimal range of 3-15 bounded contexts after merging</rule>
            </section>

            <section id="naming_conventions">
                <title>Naming Conventions for Merged Contexts</title>
                <rule id="1">**Name:** Must be in English PascalCase; choose the clearest or create a better unified name</rule>
                <rule id="2">**Alias:** Should be in the preferred language; consolidate or improve upon source aliases</rule>
                <rule id="3">**Clarity:** Names should clearly indicate the merged context's comprehensive responsibility</rule>
                <rule id="4">**Consistency:** Maintain consistent terminology across all merged contexts</rule>
            </section>

            <section id="description_synthesis">
                <title>Description Synthesis Guidelines</title>
                <rule id="1">**Comprehensiveness:** Include all unique responsibilities from source contexts</rule>
                <rule id="2">**Deduplication:** Remove redundant or duplicate statements</rule>
                <rule id="3">**Clarity:** Ensure the description clearly defines the merged context's scope and purpose</rule>
                <rule id="4">**Structure:** Organize the description logically, grouping related responsibilities</rule>
            </section>
        </guidelines>
    </core_instructions>
    
    <inference_guidelines>
        <title>Inference Guidelines</title>
        <rule id="1">Start by analyzing all provided bounded contexts to identify potential duplicates or overlaps</rule>
        <rule id="2">Group contexts that appear to be duplicates or have significant overlap</rule>
        <rule id="3">For each group, determine if merging is appropriate based on the merging strategy criteria</rule>
        <rule id="4">Carefully evaluate contexts that seem similar but may serve distinct purposes</rule>
        <rule id="5">When merging, synthesize names, aliases, and descriptions to create comprehensive, non-redundant definitions</rule>
        <rule id="6">Always choose the highest importance level when merging contexts with different importance classifications</rule>
        <rule id="7">Preserve contexts that are genuinely distinct, even if they operate in related domains</rule>
        <rule id="8">Ensure the final merged set maintains an optimal number of contexts (3-15) without over-consolidation or under-consolidation</rule>
        <rule id="9">Validate that each merged context maintains high cohesion and clear boundaries</rule>
        <rule id="10">Double-check that no genuine business capabilities have been lost in the merging process</rule>
    </inference_guidelines>
    
    <output_format>
        <title>JSON Output Format</title>
        <description>The output must be a JSON object structured as follows:</description>
        <schema>
{
    "mergedBoundedContexts": [
        {
            "name": "(Merged Bounded Context name in PascalCase, English only)",
            "alias": "(Merged Bounded Context alias in preferred language)",
            "importance": "Core Domain" || "Supporting Domain" || "Generic Domain",
            "description": "(Comprehensive description synthesized from merged contexts, in preferred language)"
        }
    ]
}
        </schema>
        <field_requirements>
            <requirement id="1">All field names must match exactly as shown in the schema</requirement>
            <requirement id="2">Bounded Context names must be in English PascalCase</requirement>
            <requirement id="3">Alias and description must be in the preferred language</requirement>
            <requirement id="4">Importance must be one of the three specified values</requirement>
            <requirement id="5">Each merged bounded context must have all four fields populated</requirement>
            <requirement id="6">The output must contain only non-duplicate, consolidated bounded contexts</requirement>
        </field_requirements>
    </output_format>
</instruction>"""

    def _build_json_example_input_format(self) -> Optional[Dict[str, Any]]:
        return {
            "boundedContexts": XmlUtil.from_dict([
                {
                    "name": "CourseManagement",
                    "alias": "Course Management",
                    "importance": "Core Domain",
                    "description": "This context manages the creation and modification of courses. It handles course titles, descriptions, pricing, and basic course information management."
                },
                {
                    "name": "CourseAdministration",
                    "alias": "Course Administration",
                    "importance": "Core Domain",
                    "description": "This context is responsible for managing courses created by instructors. It handles course content organization including modules, lessons, videos, materials, quizzes, and the publishing workflow from draft to published state."
                },
                {
                    "name": "StudentEnrollment",
                    "alias": "Student Enrollment",
                    "importance": "Core Domain",
                    "description": "This context manages student enrollment in courses. It handles course browsing, enrollment requests, and enrollment status tracking."
                },
                {
                    "name": "EnrollmentManagement",
                    "alias": "Enrollment Management",
                    "importance": "Core Domain",
                    "description": "This context handles the enrollment process for students. It manages access control based on enrollment, certificate issuance, and the relationship between students and courses."
                },
                {
                    "name": "LearningProgress",
                    "alias": "Learning Progress",
                    "importance": "Core Domain",
                    "description": "This context tracks student learning activities. It manages video viewing progress, quiz taking and scoring, and overall course completion tracking."
                },
                {
                    "name": "PaymentProcessing",
                    "alias": "Payment Processing",
                    "importance": "Generic Domain",
                    "description": "This context handles payment transactions for course enrollments. It supports various payment methods and multi-currency processing."
                },
                {
                    "name": "PaymentGateway",
                    "alias": "Payment Gateway",
                    "importance": "Generic Domain",
                    "description": "This context manages payment operations. It provides payment processing features, refund handling, and payment history management."
                },
                {
                    "name": "UserManagement",
                    "alias": "User Management",
                    "importance": "Generic Domain",
                    "description": "This context manages user accounts and authentication. It handles user registration, login/logout, and profile management."
                },
                {
                    "name": "Authentication",
                    "alias": "Authentication",
                    "importance": "Generic Domain",
                    "description": "This context handles user authentication and authorization. It manages role-based access control for Students, Instructors, and Admins."
                },
                {
                    "name": "NotificationService",
                    "alias": "Notification Service",
                    "importance": "Supporting Domain",
                    "description": "This context handles email notifications for important events in the system."
                }
            ])
        }

    def _build_json_example_output_format(self) -> Dict[str, Any]:
        return {
            "mergedBoundedContexts": [
                {
                    "name": "CourseManagement",
                    "alias": "Course Management",
                    "importance": "Core Domain",
                    "description": "This context manages the entire lifecycle of courses created by instructors. It handles course creation, modification, deletion, basic course information (titles, descriptions, pricing), content organization (modules, lessons, videos, materials, quizzes), and the publishing workflow from draft to published to archived state."
                },
                {
                    "name": "StudentEnrollment",
                    "alias": "Student Enrollment",
                    "importance": "Core Domain",
                    "description": "This context manages the complete student enrollment process. It handles course browsing, enrollment requests, enrollment status tracking, access control based on enrollment status, certificate issuance upon completion, and manages the relationship between students and courses."
                },
                {
                    "name": "LearningProgress",
                    "alias": "Learning Progress",
                    "importance": "Core Domain",
                    "description": "This context tracks student learning activities and progress. It manages video viewing progress, quiz taking and scoring, overall course completion tracking, and learning outcome measurement."
                },
                {
                    "name": "PaymentProcessing",
                    "alias": "Payment Processing",
                    "importance": "Generic Domain",
                    "description": "This context handles all payment-related operations for course enrollments. It supports various payment methods, multi-currency processing, refund handling, payment history management, and payment transaction processing."
                },
                {
                    "name": "UserManagement",
                    "alias": "User Management",
                    "importance": "Generic Domain",
                    "description": "This context manages user accounts, authentication, and authorization. It handles user registration, login/logout, profile management, role-based access control (Student, Instructor, Admin), and authentication mechanisms."
                },
                {
                    "name": "NotificationService",
                    "alias": "Notification Service",
                    "importance": "Supporting Domain",
                    "description": "This context handles email notifications for important events in the system."
                }
            ]
        }
    
    def _build_json_user_query_input_format(self) -> Dict[str, Any]:
        inputs = self.client.get("inputs")
        bounded_contexts = inputs.get("boundedContexts", [])
        
        return {
            "boundedContexts": XmlUtil.from_dict(bounded_contexts)
        }