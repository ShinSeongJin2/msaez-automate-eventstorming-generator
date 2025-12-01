from typing import Any, Dict, Optional

from .xml_base import XmlBaseGenerator
from ..utils import XmlUtil
from ..models import MergeDraftGeneratorOutput

class MergeDraftGenerator(XmlBaseGenerator):
    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        self.inputs_types_to_check = ["targetDrafts", "targetBoundedContextNames"]
        super().__init__(model_name, MergeDraftGeneratorOutput, model_kwargs, client)

    def _build_persona_info(self) -> Dict[str, str]:
        return {
            "persona": "Distinguished Domain-Driven Design (DDD) Integration Architect",
            "goal": "To merge and consolidate aggregate drafts across bounded contexts, eliminating redundancies and establishing proper cross-context references through ID Value Objects.",
            "backstory": "I am a highly experienced DDD architect specializing in strategic design and context integration. I excel at identifying duplicate aggregates across bounded contexts, establishing proper aggregate references using ID Value Objects, and ensuring consistency in domain model design. My expertise includes managing cross-context dependencies, maintaining referential integrity, and creating cohesive domain models that respect bounded context boundaries while enabling necessary collaborations."
        }
        
    def _build_task_instruction_prompt(self) -> str:
        return """<instruction>
    <core_instructions>
        <title>Draft Merging Task</title>
        <task_description>Your task is to merge aggregate drafts created for multiple bounded contexts. You will consolidate drafts by eliminating duplicate aggregates, establishing proper cross-aggregate references using ID Value Objects, and ensuring consistency across the entire domain model. This is an incremental process where you merge target bounded contexts while considering previously accumulated drafts.</task_description>
        
        <input_description>
            <title>You will receive user inputs containing:</title>
            <item id="1">**Target Drafts:** Draft aggregates for each bounded context that need to be merged</item>
            <item id="2">**Accumulated Drafts:** Previously merged drafts from other bounded contexts (fixed and should not be modified)</item>
            <item id="3">**Target Bounded Context Names:** Names of bounded contexts to process in this merge operation</item>
        </input_description>

        <guidelines>
            <title>Draft Merging Guidelines</title>
            
            <section id="incremental_merging">
                <title>Incremental Merging Process</title>
                <rule id="1">**Target Processing:** Only generate merged drafts for bounded contexts specified in targetBoundedContextNames</rule>
                <rule id="2">**Accumulated Drafts are Fixed:** Accumulated drafts represent previously finalized merges and must not be modified</rule>
                <rule id="3">**Forward Compatibility:** When merging current targets, consider that accumulated drafts were created first and design accordingly</rule>
                <rule id="4">**Progressive Accumulation:** Each merge operation builds upon previous results, gradually creating the complete domain model</rule>
            </section>

            <section id="duplicate_detection">
                <title>Duplicate Aggregate Detection</title>
                <rule id="1">**Name and Alias Check:** Aggregates are duplicates if both aggregateName AND aggregateAlias match</rule>
                <rule id="2">**Cross-Context Uniqueness:** Ensure the same aggregate does not exist in different bounded contexts</rule>
                <rule id="3">**Consolidation Strategy:** When duplicates are found, keep one instance and reference it from other contexts using ID Value Objects</rule>
                <rule id="4">**Semantic Analysis:** Consider domain semantics - aggregates with similar names but different contexts may represent different concepts</rule>
            </section>

            <section id="id_value_objects">
                <title>ID Value Object Creation</title>
                <rule id="1">**Cross-Aggregate References:** When one aggregate references another (within same or different BC), create an ID Value Object</rule>
                <rule id="2">**Naming Convention:** ID Value Object names should follow pattern: '<ReferencedAggregateName>Id' (e.g., 'CustomerId', 'OrderId')</rule>
                <rule id="3">**Alias Convention:** ID Value Object aliases should clearly indicate the reference (e.g., 'Customer ID Reference', '고객 ID 참조')</rule>
                <rule id="4">**Separate Storage:** Store ID Value Objects in the dedicated IDValueObjects array, not in the regular valueObjects array</rule>
                <rule id="5">**Reference Information:** Each ID Value Object must include referencedAggregateName and referencedAggregateAlias</rule>
                <rule id="6">**Same-Context References:** ID Value Objects are also used when referencing aggregates within the same bounded context</rule>
            </section>

            <section id="reference_resolution">
                <title>Reference Resolution Guidelines</title>
                <rule id="1">**Identify Dependencies:** Analyze which aggregates need to reference others based on domain relationships</rule>
                <rule id="2">**Unidirectional References:** Maintain unidirectional references to avoid circular dependencies</rule>
                <rule id="3">**Ownership Analysis:** Determine which aggregate owns the reference based on lifecycle and business ownership</rule>
                <rule id="4">**Accumulated Draft Alignment:** When target aggregates reference accumulated draft aggregates, ensure exact name/alias matching</rule>
            </section>

            <section id="structure_preservation">
                <title>Structure Preservation</title>
                <rule id="1">**Maintain ValueObjects:** Keep non-reference value objects in the valueObjects array</rule>
                <rule id="2">**Maintain Enumerations:** Preserve all enumerations in the enumerations array</rule>
                <rule id="3">**No Data Loss:** Ensure all domain elements from target drafts are preserved or properly consolidated</rule>
                <rule id="4">**Consistency:** Maintain consistent naming and structural patterns across all bounded contexts</rule>
            </section>

            <section id="naming_conventions">
                <title>Naming Conventions</title>
                <rule id="1">**Aggregate Names:** Must be in English PascalCase (e.g., "CustomerProfile", "Order")</rule>
                <rule id="2">**Aggregate Aliases:** Should be in the preferred language, providing clear descriptions</rule>
                <rule id="3">**No Type Suffixes:** Do not include type information in names (use "Order" not "OrderAggregate")</rule>
                <rule id="4">**Consistency:** Use consistent terminology aligned with the ubiquitous language</rule>
                <rule id="5">**Uniqueness:** Across all bounded contexts, each aggregate name should be unique</rule>
            </section>

            <section id="output_requirements">
                <title>Output Requirements</title>
                <rule id="1">**Valid JSON:** The output must be valid JSON without inline comments</rule>
                <rule id="2">**Target Contexts Only:** Only include bounded contexts from targetBoundedContextNames in the output</rule>
                <rule id="3">**Complete Structure:** Each aggregate must have all required fields populated</rule>
                <rule id="4">**Language Compliance:** Names in English, aliases in preferred language</rule>
                <rule id="5">**Separate Arrays:** Keep valueObjects, enumerations, and IDValueObjects in their respective arrays</rule>
            </section>
        </guidelines>
    </core_instructions>
    
    <inference_guidelines>
        <title>Inference Guidelines</title>
        <rule id="1">Thoroughly analyze both target drafts and accumulated drafts to understand the complete domain model</rule>
        <rule id="2">Identify duplicate aggregates by comparing both names and aliases across all bounded contexts</rule>
        <rule id="3">Determine which aggregates need to reference others based on domain relationships and dependencies</rule>
        <rule id="4">Create ID Value Objects for all cross-aggregate references, including same-context references</rule>
        <rule id="5">Ensure accumulated drafts remain unchanged and align new merges with existing structures</rule>
        <rule id="6">Maintain referential integrity by verifying referenced aggregates exist in either target or accumulated drafts</rule>
        <rule id="7">Strictly adhere to naming conventions: English for names, preferred language for aliases</rule>
        <rule id="8">Preserve all domain elements (enumerations, value objects) during the merge process</rule>
        <rule id="9">Only output merged drafts for bounded contexts specified in targetBoundedContextNames</rule>
        <rule id="10">Consider the incremental nature of merging - design target drafts to align with accumulated drafts</rule>
    </inference_guidelines>
    
    <output_format>
        <title>JSON Output Format</title>
        <description>The output must be a JSON object structured as follows:</description>
        <schema>
{
    "mergedDrafts": [
        {
            "boundedContextName": "(Bounded context name from targetBoundedContextNames)",
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
                    ],
                    "IDValueObjects": [
                        {
                            "name": "(ID Value Object name in PascalCase, English only, typically '<AggregateName>Id')",
                            "alias": "(ID Value Object alias in preferred language)",
                            "referencedAggregateName": "(Name of the referenced aggregate)",
                            "referencedAggregateAlias": "(Alias of the referenced aggregate)"
                        }
                    ]
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
            <requirement id="4">Arrays (enumerations, valueObjects, IDValueObjects) can be empty but must be present</requirement>
            <requirement id="5">Only include bounded contexts from targetBoundedContextNames in mergedDrafts</requirement>
            <requirement id="6">Each ID Value Object must have referencedAggregateName and referencedAggregateAlias</requirement>
            <requirement id="7">Do not include type suffixes in names or aliases</requirement>
        </field_requirements>
    </output_format>
</instruction>"""

    def _build_json_example_input_format(self) -> Optional[Dict[str, Any]]:
        return {
            "target_drafts": XmlUtil.from_dict({
                "OrderManagement": {
                    "aggregates": [
                        {
                            "aggregateName": "Order",
                            "aggregateAlias": "Order Information",
                            "enumerations": [
                                {
                                    "name": "OrderStatus",
                                    "alias": "Order Status"
                                }
                            ],
                            "valueObjects": [
                                {
                                    "name": "OrderItem",
                                    "alias": "Order Item Details"
                                },
                                {
                                    "name": "ShippingAddress",
                                    "alias": "Shipping Address"
                                }
                            ]
                        }
                    ]
                },
                "DeliveryManagement": {
                    "aggregates": [
                        {
                            "aggregateName": "Delivery",
                            "aggregateAlias": "Delivery Information",
                            "enumerations": [
                                {
                                    "name": "DeliveryStatus",
                                    "alias": "Delivery Status"
                                }
                            ],
                            "valueObjects": [
                                {
                                    "name": "DeliveryRoute",
                                    "alias": "Delivery Route"
                                }
                            ]
                        }
                    ]
                }
            }),
            "accumulated_drafts": XmlUtil.from_dict({
                "CustomerManagement": {
                    "aggregates": [
                        {
                            "aggregateName": "Customer",
                            "aggregateAlias": "Customer Profile",
                            "enumerations": [
                                {
                                    "name": "CustomerType",
                                    "alias": "Customer Type"
                                }
                            ],
                            "valueObjects": [
                                {
                                    "name": "ContactInfo",
                                    "alias": "Contact Information"
                                }
                            ],
                            "IDValueObjects": []
                        }
                    ]
                },
                "ProductCatalog": {
                    "aggregates": [
                        {
                            "aggregateName": "Product",
                            "aggregateAlias": "Product Information",
                            "enumerations": [
                                {
                                    "name": "ProductCategory",
                                    "alias": "Product Category"
                                }
                            ],
                            "valueObjects": [
                                {
                                    "name": "ProductSpec",
                                    "alias": "Product Specification"
                                }
                            ],
                            "IDValueObjects": []
                        }
                    ]
                }
            }),
            "target_bounded_context_names": ["OrderManagement"]
        }

    def _build_json_example_output_format(self) -> Dict[str, Any]:
        return {
            "mergedDrafts": [
                {
                    "boundedContextName": "OrderManagement",
                    "aggregates": [
                        {
                            "aggregateName": "Order",
                            "aggregateAlias": "Order Information",
                            "enumerations": [
                                {
                                    "name": "OrderStatus",
                                    "alias": "Order Status"
                                }
                            ],
                            "valueObjects": [
                                {
                                    "name": "OrderItem",
                                    "alias": "Order Item Details"
                                },
                                {
                                    "name": "ShippingAddress",
                                    "alias": "Shipping Address"
                                }
                            ],
                            "IDValueObjects": [
                                {
                                    "name": "CustomerId",
                                    "alias": "Customer ID Reference",
                                    "referencedAggregateName": "Customer",
                                    "referencedAggregateAlias": "Customer Profile"
                                },
                                {
                                    "name": "ProductId",
                                    "alias": "Product ID Reference",
                                    "referencedAggregateName": "Product",
                                    "referencedAggregateAlias": "Product Information"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    
    def _build_json_user_query_input_format(self) -> Dict[str, Any]:
        inputs = self.client.get("inputs")
        target_drafts = inputs.get("targetDrafts", {})
        accumulated_drafts = inputs.get("accumulatedDrafts", {})
        target_bounded_context_names = inputs.get("targetBoundedContextNames", [])
        
        return {
            "target_drafts": XmlUtil.from_dict(target_drafts),
            "accumulated_drafts": XmlUtil.from_dict(accumulated_drafts),
            "target_bounded_context_names": target_bounded_context_names
        }