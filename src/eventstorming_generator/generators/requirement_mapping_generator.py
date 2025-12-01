from typing import Any, Dict, Optional

from .xml_base import XmlBaseGenerator
from ..utils import EsTraceUtil, XmlUtil
from ..models import RequirementMappingGeneratorOutput

class RequirementMappingGenerator(XmlBaseGenerator):
    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        self.inputs_types_to_check = ["line_numbered_requirements", "boundedContexts"]
        super().__init__(model_name, RequirementMappingGeneratorOutput, model_kwargs, client)

    def _build_persona_info(self) -> Dict[str, str]:
        return {
            "persona": "Expert Domain-Driven Design (DDD) Analyst",
            "goal": "To analyze functional requirements and map them to appropriate Bounded Contexts based on domain relevance and responsibility alignment.",
            "backstory": "I am a highly experienced domain analyst specializing in requirement analysis and domain modeling. I have extensive knowledge of domain-driven design principles and context boundaries, requirement decomposition and functional analysis, business capability mapping and context responsibility analysis, and traceability between requirements and architectural components. My expertise lies in understanding the nuances of functional requirements and accurately identifying which bounded contexts are responsible for implementing specific functionalities."
        }
        
    def _build_task_instruction_prompt(self) -> str:
        return """<instruction>
    <core_instructions>
        <title>Requirement to Bounded Context Mapping Task</title>
        <task_description>Your task is to analyze the provided functional requirements and map each relevant portion to the appropriate Bounded Contexts. You will identify which lines of the requirements document are relevant to each bounded context based on domain responsibility and functional alignment.</task_description>
        
        <input_description>
            <title>You will receive user inputs containing:</title>
            <item id="1">**Functional Requirements:** Multi-line text describing the business requirements and functionalities</item>
            <item id="2">**Bounded Contexts:** List of bounded contexts with their names, aliases, importance levels, and descriptions</item>
        </input_description>

        <guidelines>
            <title>Requirement Mapping Guidelines</title>
            
            <section id="core_principles">
                <title>Core Principles</title>
                <rule id="1">**Responsibility Alignment:** Map requirements to contexts based on the context's defined responsibilities and scope</rule>
                <rule id="2">**Domain Language Matching:** Look for terminology and concepts that align with each context's ubiquitous language</rule>
                <rule id="3">**Functional Cohesion:** Group related requirement lines that belong to the same functional area</rule>
                <rule id="4">**Multiple Mappings Allowed:** A requirement line can be mapped to multiple contexts if it has cross-cutting concerns or involves inter-context collaboration</rule>
                <rule id="5">**Completeness:** Ensure all relevant requirement lines are mapped to at least one context</rule>
            </section>

            <section id="mapping_criteria">
                <title>Mapping Criteria</title>
                <rule id="1">**Direct Responsibility:** Map requirements that directly describe functionalities owned by the context</rule>
                <rule id="2">**Data Ownership:** Map requirements that involve data entities owned by the context</rule>
                <rule id="3">**Business Capability:** Map requirements that align with the business capabilities of the context</rule>
                <rule id="4">**Use Case Involvement:** Map requirements where the context plays a primary or supporting role</rule>
                <rule id="5">**Integration Points:** Identify requirements that describe interactions between contexts</rule>
            </section>

            <section id="line_number_handling">
                <title>Line Number Handling</title>
                <rule id="1">**1-Based Indexing:** Line numbers start from 1, not 0</rule>
                <rule id="2">**Inclusive Ranges:** Both start and end line numbers are inclusive</rule>
                <rule id="3">**Continuous Ranges:** Group consecutive related lines into a single range [start, end]</rule>
                <rule id="4">**Multiple Ranges:** Use multiple ranges when related content appears in different sections</rule>
                <rule id="5">**Granularity:** Capture meaningful sections - not too broad (entire document) or too narrow (single words)</rule>
            </section>

            <section id="context_coverage">
                <title>Context Coverage</title>
                <rule id="1">**All Contexts Included:** Every bounded context should have a mapping entry, even if refs is empty</rule>
                <rule id="2">**Relevance Threshold:** Only include requirement lines that have clear relevance to the context</rule>
                <rule id="3">**Primary vs Secondary:** Some contexts will be primary owners of requirements, others may be secondary participants</rule>
                <rule id="4">**Generic Domain Patterns:** Generic domains typically handle common cross-cutting concerns</rule>
            </section>

            <section id="analysis_approach">
                <title>Analysis Approach</title>
                <rule id="1">**Read Thoroughly:** Carefully read and understand all functional requirements</rule>
                <rule id="2">**Understand Contexts:** Review each bounded context's description and responsibilities</rule>
                <rule id="3">**Identify Keywords:** Look for domain-specific terms and concepts in requirements</rule>
                <rule id="4">**Trace Responsibilities:** Match requirement functionalities to context responsibilities</rule>
                <rule id="5">**Cross-Reference:** Verify that mappings align with DDD principles and context boundaries</rule>
            </section>
        </guidelines>
    </core_instructions>
    
    <inference_guidelines>
        <title>Inference Guidelines</title>
        <rule id="1">Begin by reading through all functional requirements to understand the overall system</rule>
        <rule id="2">Study each bounded context's description to understand its scope and responsibilities</rule>
        <rule id="3">Go through the requirements line by line, identifying which contexts are relevant</rule>
        <rule id="4">For each requirement section, ask: "Which context(s) would be responsible for implementing this?"</rule>
        <rule id="5">Look for explicit mentions of entities, processes, or capabilities that belong to specific contexts</rule>
        <rule id="6">Consider both direct ownership and collaborative involvement when mapping</rule>
        <rule id="7">Group consecutive related lines into continuous ranges for cleaner output</rule>
        <rule id="8">Ensure every bounded context has an entry in the output, even if it has no relevant requirements</rule>
        <rule id="9">Validate that critical requirements are not missed and are mapped to appropriate contexts</rule>
        <rule id="10">Double-check that line number ranges are correct and within the bounds of the requirements document</rule>
    </inference_guidelines>
    
    <output_format>
        <title>JSON Output Format</title>
        <description>The output must be a JSON object structured as follows:</description>
        <schema>
{
    "contextMappings": [
        {
            "boundedContextName": "(Exact name of the bounded context from input)",
            "refs": [
                [start_line, end_line],
                [start_line, end_line],
                ...
            ]
        }
    ]
}
        </schema>
        <field_requirements>
            <requirement id="1">boundedContextName must exactly match the name field from the input bounded contexts</requirement>
            <requirement id="2">refs is an array of two-element arrays, where each inner array represents [start_line, end_line]</requirement>
            <requirement id="3">Line numbers are 1-based (first line is line 1)</requirement>
            <requirement id="4">Both start_line and end_line are inclusive</requirement>
            <requirement id="5">refs can be an empty array [] if no requirements are relevant to that context</requirement>
            <requirement id="6">Include all bounded contexts from the input, even if they have empty refs</requirement>
            <requirement id="7">Ranges should not overlap within the same context, but can overlap across different contexts</requirement>
        </field_requirements>
    </output_format>
</instruction>"""

    def _build_json_example_input_format(self) -> Optional[Dict[str, Any]]:
        requirements = """# E-Learning Platform Requirements

## Overview
We need to build an online learning platform where instructors can create and manage courses, and students can enroll, learn, and track their progress.

## Key Functionalities

### Course Management
- Instructors can create courses with titles, descriptions, and pricing
- Courses can be organized into modules and lessons
- Support for video content, reading materials, and quizzes
- Course publishing workflow (Draft → Published → Archived)

### Student Enrollment
- Students can browse available courses
- Enrollment process with payment
- Access control based on enrollment status
- Certificate issuance upon completion

### Learning Experience
- Video playback with progress tracking
- Quiz taking and scoring
- Progress tracking across courses
- Discussion forums for each course

### Payment Processing
- Support for various payment methods
- Pricing in multiple currencies
- Refund handling
- Payment history tracking

### User Management
- User registration and authentication
- Profile management
- Role-based access (Student, Instructor, Admin)
- Email notifications for important events"""

        bounded_contexts = [
            {
                "name": "CourseManagement",
                "alias": "Course Management",
                "importance": "Core Domain",
                "description": "This context manages the entire lifecycle of courses created by instructors. It handles course creation, modification, deletion, content organization (modules, lessons, videos, materials, quizzes), pricing, and publishing workflow."
            },
            {
                "name": "StudentEnrollment",
                "alias": "Student Enrollment",
                "importance": "Core Domain",
                "description": "This context manages the student enrollment process. It handles course browsing, enrollment requests, access control, certificate issuance, and manages the relationship between students and courses."
            },
            {
                "name": "LearningProgress",
                "alias": "Learning Progress",
                "importance": "Core Domain",
                "description": "This context tracks student learning activities and progress. It manages video viewing progress, quiz taking and scoring, overall course completion rate calculation, and discussion participation."
            },
            {
                "name": "PaymentProcessing",
                "alias": "Payment Processing",
                "importance": "Generic Domain",
                "description": "This context handles payment transactions. It provides standard payment features including support for various payment methods, multi-currency processing, refund handling, and payment history management."
            },
            {
                "name": "UserManagement",
                "alias": "User Management",
                "importance": "Generic Domain",
                "description": "This context manages user accounts and authentication. It handles user registration, login/logout, profile management, role-based access control (Student/Instructor/Admin), and email notifications."
            }
        ]

        return {
            "functional_requirements": EsTraceUtil.add_line_numbers_to_description(requirements),
            "bounded_contexts": XmlUtil.from_dict(bounded_contexts)
        }

    def _build_json_example_output_format(self) -> Dict[str, Any]:
        return {
            "contextMappings": [
                {
                    "boundedContextName": "CourseManagement",
                    "refs": [
                        [8, 12],
                        [28, 28]
                    ]
                },
                {
                    "boundedContextName": "StudentEnrollment",
                    "refs": [
                        [14, 18]
                    ]
                },
                {
                    "boundedContextName": "LearningProgress",
                    "refs": [
                        [20, 24]
                    ]
                },
                {
                    "boundedContextName": "PaymentProcessing",
                    "refs": [
                        [16, 16],
                        [26, 30]
                    ]
                },
                {
                    "boundedContextName": "UserManagement",
                    "refs": [
                        [32, 36]
                    ]
                }
            ]
        }
    
    def _build_json_user_query_input_format(self) -> Dict[str, Any]:
        inputs = self.client.get("inputs")
        line_numbered_requirements = inputs.get("line_numbered_requirements")
        bounded_contexts = inputs.get("boundedContexts")
        
        return {
            "functional_requirements": line_numbered_requirements,
            "bounded_contexts": XmlUtil.from_dict(bounded_contexts)
        }