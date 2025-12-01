from typing import Any, Dict, Optional

from .xml_base import XmlBaseGenerator
from ..utils import XmlUtil
from ..models import CreateDraftGeneratorOutput

class CreateDraftGenerator(XmlBaseGenerator):
    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        self.inputs_types_to_check = ["bounded_context_info", "requirements"]
        super().__init__(model_name, CreateDraftGeneratorOutput, model_kwargs, client)

    def _build_persona_info(self) -> Dict[str, str]:
        return {
            "persona": "Distinguished Domain-Driven Design (DDD) Architect",
            "goal": "To design well-structured aggregates within a bounded context that enforce business invariants, maintain transactional consistency, and align with domain requirements.",
            "backstory": "I am a highly experienced DDD architect with extensive expertise in structuring complex domains into well-defined aggregates with clear boundaries and invariants. I have deep knowledge of strategic design patterns, aggregate root definition, transactional consistency management, and the proper use of value objects and enumerations. I excel at balancing business requirements with technical considerations like cohesion, coupling, performance, and maintainability. My designs reflect deep domain understanding while maintaining technical precision and adhering to established naming conventions."
        }
        
    def _build_task_instruction_prompt(self) -> str:
        return """<instruction>
    <core_instructions>
        <title>Aggregate Design Task</title>
        <task_description>Your task is to design aggregates within a specified bounded context based on provided functional requirements. You will create aggregate structures that enforce business invariants, maintain transactional consistency, and properly organize entities, value objects, and enumerations according to Domain-Driven Design principles.</task_description>
        
        <input_description>
            <title>You will receive user inputs containing:</title>
            <item id="1">**Bounded Context Information:** Name, alias, importance, and description of the target bounded context</item>
            <item id="2">**Functional Requirements:** Detailed business requirements describing the domain functionalities</item>
        </input_description>

        <guidelines>
            <title>Aggregate Design Guidelines</title>
            
            <section id="core_principles">
                <title>Core DDD Principles</title>
                <rule id="1">**Transactional Consistency:** Consolidate transaction-critical data within a single aggregate to preserve atomicity</rule>
                <rule id="2">**Aggregate Boundaries:** Define clear boundaries that respect inherent business invariants</rule>
                <rule id="3">**Business Alignment:** Ensure aggregates align with business capabilities and domain concepts</rule>
                <rule id="4">**Single Responsibility:** Each aggregate should encapsulate a complete business capability</rule>
                <rule id="5">**Invariant Protection:** Design aggregates to protect and enforce business rules</rule>
            </section>

            <section id="transactional_design">
                <title>Transactional Consistency Guidelines</title>
                <rule id="1">**Atomic Operations:** Keep related data that must change together within the same aggregate</rule>
                <rule id="2">**Avoid Data Splitting:** Do not separate core transactional data (e.g., order/order items, loan/loan details)</rule>
                <rule id="3">**Transaction Boundaries:** Define aggregate boundaries that support atomic business operations</rule>
                <rule id="4">**Consistency Guarantees:** Ensure business invariants can be enforced within aggregate transactions</rule>
            </section>

            <section id="value_objects">
                <title>Value Object Design</title>
                <rule id="1">**Semantic Grouping:** Group related properties into value objects to improve maintainability</rule>
                <rule id="2">**Avoid Single-Property VOs:** Do not create value objects with only one property unless they represent significant domain concepts</rule>
                <rule id="3">**No Redundancy:** Avoid creating meaningless or redundant value objects; include properties directly in the aggregate when appropriate</rule>
                <rule id="4">**Balanced Granularity:** Do not derive an excessive number of value objects; maintain a balanced design</rule>
                <rule id="5">**Direct Association:** All value objects must be directly associated with an aggregate</rule>
            </section>

            <section id="enumerations">
                <title>Enumeration Guidelines</title>
                <rule id="1">**State Management:** Always use enumerations when storing state or similar categorical information</rule>
                <rule id="2">**Direct Association:** All enumerations must be directly associated with an aggregate</rule>
                <rule id="3">**No Nesting:** Do not embed enumerations within value objects</rule>
                <rule id="4">**Domain Representation:** Enumerations should represent meaningful domain concepts and constraints</rule>
            </section>

            <section id="naming_conventions">
                <title>Naming Conventions</title>
                <rule id="1">**Aggregate Names:** Must be in English PascalCase (e.g., "CustomerProfile", "OrderManagement")</rule>
                <rule id="2">**Aggregate Aliases:** Should be in the preferred language, providing clear descriptions</rule>
                <rule id="3">**No Type Suffixes:** Do not include type information in names (use "Book" not "BookAggregate", "Person" not "PersonInfo")</rule>
                <rule id="4">**Consistency:** Use consistent terminology aligned with the ubiquitous language</rule>
                <rule id="5">**Uniqueness:** Within the bounded context, each name and alias must be unique</rule>
            </section>

            <section id="design_quality">
                <title>Design Quality Criteria</title>
                <rule id="1">**High Cohesion:** Group highly related behaviors and data together</rule>
                <rule id="2">**Low Coupling:** Minimize dependencies between aggregates</rule>
                <rule id="3">**Encapsulation:** Hide implementation details and expose only necessary interfaces</rule>
                <rule id="4">**Maintainability:** Create designs that are easy to understand and modify</rule>
                <rule id="5">**Scalability:** Consider performance and scaling requirements</rule>
            </section>

            <section id="output_requirements">
                <title>Output Requirements</title>
                <rule id="1">**Valid JSON:** The output must be valid JSON without inline comments</rule>
                <rule id="2">**Complete Structure:** Each aggregate must have all required fields populated</rule>
                <rule id="3">**Language Compliance:** Names in English, aliases in preferred language</rule>
                <rule id="4">**Clarity:** Maintain clarity and conciseness in the structure</rule>
            </section>
        </guidelines>
    </core_instructions>
    
    <inference_guidelines>
        <title>Inference Guidelines</title>
        <rule id="1">Thoroughly analyze the functional requirements to understand the business domain</rule>
        <rule id="2">Identify key business entities and their relationships within the bounded context</rule>
        <rule id="3">Determine which data must be transactionally consistent and group it into aggregates</rule>
        <rule id="4">Design value objects to represent meaningful domain concepts with multiple related properties</rule>
        <rule id="5">Identify state transitions and categorical data that should be represented as enumerations</rule>
        <rule id="6">Ensure aggregate boundaries align with business invariants and transaction requirements</rule>
        <rule id="7">Strictly adhere to naming conventions: English for names, preferred language for aliases</rule>
        <rule id="8">Avoid creating redundant or overly granular value objects</rule>
        <rule id="9">Ensure all enumerations and value objects are directly associated with aggregates</rule>
        <rule id="10">Create a balanced design that is neither too coarse-grained nor too fine-grained</rule>
    </inference_guidelines>
    
    <output_format>
        <title>JSON Output Format</title>
        <description>The output must be a JSON object structured as follows:</description>
        <schema>
{
    "aggregates": [
        {
            "aggregateName": "(Aggregate name in PascalCase, English only)",
            "aggregateAlias": "(Aggregate alias in preferred language)",
            "enumerations": [
                {
                    "name": "(Enumeration name in PascalCase, English only)",
                    "alias": "(Enumeration alias in preferred language)"
                }
            ],
            "valueObjects": [
                {
                    "name": "(Value Object name in PascalCase, English only)",
                    "alias": "(Value Object alias in preferred language)"
                }
            ]
        }
    ]
}
        </schema>
        <field_requirements>
            <requirement id="1">All field names must match exactly as shown in the schema</requirement>
            <requirement id="2">Aggregate, enumeration, and value object names must be in English PascalCase</requirement>
            <requirement id="3">All aliases must be in the preferred language</requirement>
            <requirement id="4">Enumerations and valueObjects arrays can be empty but must be present</requirement>
            <requirement id="5">Each aggregate must have aggregateName and aggregateAlias fields</requirement>
            <requirement id="6">Do not include type suffixes in names or aliases</requirement>
        </field_requirements>
    </output_format>
</instruction>"""

    def _build_json_example_input_format(self) -> Optional[Dict[str, Any]]:
        return {
            "bounded_context_info": XmlUtil.from_dict({
                "name": "RoomManagement",
                "alias": "Hotel Room Management",
                "importance": "Core Domain",
                "description": "Manages hotel room registration, availability status, maintenance scheduling, and occupancy tracking. Handles room types, pricing, cleaning status, and maintenance history. Primary users are hotel staff and housekeeping managers."
            }),
            "requirements": """# Bounded Context: RoomManagement

## Overview
This context manages hotel room inventory, status tracking, and maintenance operations.

## Key Functionalities

### Room Registration
- Hotel staff can register new rooms with room number, type, floor level, capacity, and base price
- Room numbers must be unique within the hotel
- Room types include: Standard, Deluxe, Suite, Presidential Suite
- Each room starts with 'Available' status

### Status Management
- Room status: Available, Occupied, Cleaning, Maintenance, Out of Order
- Automatic status changes based on guest activities and staff actions
- Status change history tracking for operational analysis

### Maintenance Operations
- Schedule maintenance for rooms requiring repairs
- Track maintenance type, scheduled date, priority level
- Priority levels: Low, Medium, High, Emergency
- Maintenance history with cost tracking

### Housekeeping
- Track cleaning requirements and progress
- Update room status through cleaning workflow
- Coordinate with maintenance scheduling

## Key Entities
- Room with specifications (number, type, floor, capacity, price)
- Room status with history
- Maintenance records with scheduling and completion tracking"""
        }

    def _build_json_example_output_format(self) -> Dict[str, Any]:
        return {
            "aggregates": [
                {
                    "aggregateName": "Room",
                    "aggregateAlias": "Hotel Room",
                    "enumerations": [
                        {
                            "name": "RoomStatus",
                            "alias": "Room Availability Status"
                        },
                        {
                            "name": "RoomType",
                            "alias": "Room Category"
                        }
                    ],
                    "valueObjects": [
                        {
                            "name": "RoomSpecification",
                            "alias": "Room Technical Details"
                        }
                    ]
                },
                {
                    "aggregateName": "MaintenanceSchedule",
                    "aggregateAlias": "Room Maintenance Operations",
                    "enumerations": [
                        {
                            "name": "MaintenancePriority",
                            "alias": "Maintenance Priority Level"
                        },
                        {
                            "name": "MaintenanceStatus",
                            "alias": "Maintenance Progress Status"
                        }
                    ],
                    "valueObjects": [
                        {
                            "name": "MaintenanceRecord",
                            "alias": "Maintenance Activity Record"
                        },
                        {
                            "name": "ScheduleInfo",
                            "alias": "Scheduling Information"
                        }
                    ]
                }
            ]
        }
    
    def _build_json_user_query_input_format(self) -> Dict[str, Any]:
        inputs = self.client.get("inputs")
        bounded_context_info = inputs.get("bounded_context_info")
        requirements = inputs.get("requirements")
        
        return {
            "bounded_context_info": XmlUtil.from_dict(bounded_context_info),
            "requirements": requirements
        }