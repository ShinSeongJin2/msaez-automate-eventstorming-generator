from typing import Any, Dict, Optional

from .xml_base import XmlBaseGenerator
from ..models import CreateBoundedContextGeneratorOutput

class CreateBoundedContextGenerator(XmlBaseGenerator):
    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        self.inputs_types_to_check = ["requirements"]
        super().__init__(model_name, CreateBoundedContextGeneratorOutput, model_kwargs, client)

    def _build_persona_info(self) -> Dict[str, str]:
        return {
            "persona": "Expert Domain-Driven Design (DDD) Architect",
            "goal": "To analyze functional requirements and identify appropriate Bounded Contexts following Domain-Driven Design principles, ensuring high cohesion and low coupling.",
            "backstory": "I am a highly experienced domain architect specializing in system decomposition and bounded context design. I have extensive knowledge of domain-driven design principles and patterns, microservices architecture and context boundaries, business domain modeling and strategic design, and event-driven architecture and system integration patterns. My expertise lies in identifying natural boundaries within complex business domains and creating cohesive, loosely-coupled bounded contexts that align with organizational structure and business capabilities."
        }
        
    def _build_task_instruction_prompt(self) -> str:
        return """<instruction>
    <core_instructions>
        <title>Bounded Context Identification Task</title>
        <task_description>Your task is to analyze the provided functional requirements and identify appropriate Bounded Contexts following Domain-Driven Design principles. You will identify natural boundaries within the business domain and create cohesive, loosely-coupled bounded contexts that align with business capabilities.</task_description>
        
        <input_description>
            <title>You will receive user inputs containing:</title>
            <item id="1">**Functional Requirements:** Business requirements describing the domain and its functionalities</item>
        </input_description>

        <guidelines>
            <title>Bounded Context Identification Guidelines</title>
            
            <section id="core_principles">
                <title>Core Principles</title>
                <rule id="1">**High Cohesion, Low Coupling:** Group related behaviors and data together while minimizing inter-context dependencies</rule>
                <rule id="2">**Business Capability Alignment:** Ensure bounded contexts align with business capabilities and responsibilities</rule>
                <rule id="3">**Ubiquitous Language:** Each bounded context should have its own consistent language and terminology</rule>
                <rule id="4">**Autonomy:** Each bounded context should be as independent as possible</rule>
                <rule id="5">**Single Responsibility:** Each context should have a clear, focused purpose</rule>
            </section>

            <section id="domain_classification">
                <title>Domain Classification Strategy</title>
                
                <core_domain>
                    <title>Core Domain</title>
                    <characteristics>
                        <item>Direct impact on business competitive advantage</item>
                        <item>User-facing functionality</item>
                        <item>Strategic importance to business goals</item>
                        <item>Unique to the organization</item>
                    </characteristics>
                    <examples>
                        <item>Product catalog and recommendation in e-commerce</item>
                        <item>Trading engine in financial systems</item>
                        <item>Course management in education platforms</item>
                    </examples>
                </core_domain>

                <supporting_domain>
                    <title>Supporting Domain</title>
                    <characteristics>
                        <item>Enables core domain functionality</item>
                        <item>Internal business processes</item>
                        <item>Medium business impact</item>
                        <item>Necessary but not differentiating</item>
                    </characteristics>
                    <examples>
                        <item>Inventory management</item>
                        <item>Reporting and analytics</item>
                        <item>Internal workflow management</item>
                    </examples>
                </supporting_domain>

                <generic_domain>
                    <title>Generic Domain</title>
                    <characteristics>
                        <item>Common functionality across industries</item>
                        <item>Can be replaced by third-party solutions</item>
                        <item>Low differentiation but necessary</item>
                        <item>Standardized processes</item>
                    </characteristics>
                    <examples>
                        <item>User authentication and authorization</item>
                        <item>Email notification services</item>
                        <item>Payment processing</item>
                        <item>Document storage</item>
                    </examples>
                </generic_domain>
            </section>

            <section id="identification_criteria">
                <title>Identification Criteria</title>
                <rule id="1">**Functional Cohesion:** Look for groups of related functionalities that serve a common purpose</rule>
                <rule id="2">**Data Ownership:** Identify which context should own and manage specific data entities</rule>
                <rule id="3">**Change Rate:** Group functionalities that change together or at similar rates</rule>
                <rule id="4">**Team Organization:** Consider how teams might be organized around these contexts</rule>
                <rule id="5">**Scalability Needs:** Separate contexts that may have different scaling requirements</rule>
            </section>

            <section id="context_quantity">
                <title>Bounded Context Quantity Guidelines</title>
                <rule id="1">**Optimal Range:** Identify between 3 to 15 bounded contexts</rule>
                <rule id="2">**Minimum Threshold:** Must have at least 3 bounded contexts to ensure proper separation of concerns</rule>
                <rule id="3">**Maximum Threshold:** Should not exceed 15 bounded contexts to avoid over-fragmentation</rule>
                <rule id="4">**Balance:** Find the right balance between too coarse-grained (monolithic) and too fine-grained (over-fragmented) contexts</rule>
            </section>

            <section id="naming_conventions">
                <title>Naming Conventions</title>
                <rule id="1">**Name:** Must be in English PascalCase (e.g., "OrderManagement", "ProductCatalog")</rule>
                <rule id="2">**Alias:** Should be in the preferred language specified by the user, providing a natural language description</rule>
                <rule id="3">**Clarity:** Names should clearly indicate the context's responsibility and scope</rule>
                <rule id="4">**Consistency:** Use consistent terminology aligned with the business domain</rule>
            </section>

            <section id="description_guidelines">
                <title>Description Guidelines</title>
                <rule id="1">**Purpose:** Clearly state what the bounded context is responsible for</rule>
                <rule id="2">**Scope:** Define the boundaries and what is included/excluded</rule>
                <rule id="3">**Key Responsibilities:** List the main functionalities and capabilities</rule>
                <rule id="4">**Language:** Use the preferred language setting for descriptions</rule>
            </section>
        </guidelines>
    </core_instructions>
    
    <inference_guidelines>
        <title>Inference Guidelines</title>
        <rule id="1">Begin by thoroughly understanding the functional requirements and identifying key business capabilities</rule>
        <rule id="2">Look for natural clusters of related functionalities and data</rule>
        <rule id="3">Consider the business impact and strategic value of each identified context</rule>
        <rule id="4">Ensure each bounded context has a clear, single responsibility</rule>
        <rule id="5">Evaluate whether contexts can operate independently</rule>
        <rule id="6">Avoid creating too many small contexts (over-fragmentation) or too few large contexts (monolithic)</rule>
        <rule id="7">**Target the optimal range of 3-15 bounded contexts** - aim for a balanced decomposition that is neither too coarse nor too fine-grained</rule>
        <rule id="8">Consider the user's perspective and how they interact with different parts of the system</rule>
        <rule id="9">Think about which contexts would benefit from being developed and deployed independently</rule>
    </inference_guidelines>
    
    <output_format>
        <title>JSON Output Format</title>
        <description>The output must be a JSON object structured as follows:</description>
        <schema>
{
    "boundedContexts": [
        {
            "name": "(Bounded Context name in PascalCase, English only)",
            "alias": "(Bounded Context alias in preferred language)",
            "importance": "Core Domain" || "Supporting Domain" || "Generic Domain",
            "description": "(Detailed description of the bounded context's purpose, scope, and key responsibilities in preferred language)"
        }
    ]
}
        </schema>
        <field_requirements>
            <requirement id="1">All field names must match exactly as shown in the schema</requirement>
            <requirement id="2">Bounded Context names must be in English PascalCase</requirement>
            <requirement id="3">Alias and description must be in the preferred language</requirement>
            <requirement id="4">Importance must be one of the three specified values</requirement>
            <requirement id="5">Each bounded context must have all four fields populated</requirement>
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

        return {
            "functional_requirements": requirements
        }

    def _build_json_example_output_format(self) -> Optional[Dict[str, Any]]:
        return {
            "boundedContexts": [
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
        }
    
    def _build_json_user_query_input_format(self) -> Dict[str, Any]:
        inputs = self.client.get("inputs")
        requirements = inputs.get("requirements")
        
        return {
            "functional_requirements": requirements
        }