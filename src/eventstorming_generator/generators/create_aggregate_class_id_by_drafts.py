from typing import Any, Dict, Optional
import json

from .xml_base import XmlBaseGenerator
from ..utils import ESValueSummarizeWithFilter, XmlUtil
from ..models import CreateAggregateClassIdByDraftsOutput

class CreateAggregateClassIdByDrafts(XmlBaseGenerator):
    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        self.inputs_types_to_check = ["summarizedESValue", "draftOption", "targetReferences"]
        super().__init__(model_name, CreateAggregateClassIdByDraftsOutput, model_kwargs, client)

    def _build_persona_info(self) -> Dict[str, str]:
        return {
            "persona": "Senior Domain-Driven Design (DDD) Expert",
            "goal": "To create optimal, unidirectional reference structures between aggregates that maintain domain integrity while minimizing coupling, ensuring proper implementation of value objects and aggregate references based on DDD principles.",
            "backstory": "With decades of hands-on experience implementing DDD in complex enterprise systems, I've developed deep expertise in strategic context mapping and aggregate relationship management. My methodical approach is driven by a commitment to clean architecture principles and optimal domain modeling. My work consistently balances technical excellence with business domain alignment, prioritizing maintainable and scalable solutions that protect domain invariants across aggregate boundaries."
        }

    def _build_task_instruction_prompt(self) -> str:
        return """<instruction>
    <core_instructions>
        <title>ValueObject Reference Generation Task</title>
        <task_description>Your task is to create the appropriate ValueObject that references another Aggregate as a foreign key, based on the provided EventStorming configuration draft. You must generate the ValueObject only for the `referenceAggregate` corresponding to the given `targetReferences`.</task_description>
    </core_instructions>
    
    <guidelines>
        <title>Guidelines for Reference Generation</title>
        <rule id="1">
            <title>Strictly Unidirectional References</title>
            <description>
                - CRITICAL: You MUST implement only ONE-WAY references between aggregates. NEVER create bidirectional references.
                - If the draft suggests a two-way relationship (e.g., Order refers to Customer AND Customer refers to Order), you MUST choose only ONE direction to implement. For instance, implement Order -> Customer and ignore Customer -> Order.
                - For every bidirectional relationship identified in the input, you must implement one direction in the `actions` list and explicitly declare the other direction as omitted in the `omittedReferences` list in the output.
            </description>
        </rule>
        <rule id="2">
            <title>Direction Selection Criteria</title>
            <description>
                When deciding the direction of a reference, consider the following criteria to make an informed choice:
                - **Lifecycle Dependency:** The dependent aggregate should reference the independent one (e.g., an Order's lifecycle depends on a Customer, so Order references Customer).
                - **Business Invariants:** The aggregate that enforces business rules should reference the data it needs to validate those rules.
                - **Stability:** The more stable aggregate should be the one that is referenced.
                - **Query Patterns:** Optimize for the most frequent and critical data access patterns.
            </description>
        </rule>
        <rule id="3">
            <title>Property Replication Rules</title>
            <description>
                - Only replicate properties that are highly unlikely to change (i.e., immutable or near-immutable), such as a birth date, gender, or country of origin.
                - Strictly AVOID replicating volatile properties that change frequently, like an address, email, or phone number.
                - Each replicated property must be justified by its immutability and business value for the reference. Include only the minimum required properties.
            </description>
        </rule>
        <rule id="4">
            <title>Technical & Implementation Details</title>
            <description>
                - Handle composite keys appropriately if a referenced Aggregate uses multiple identifiers.
                - Ensure all recommendations follow proper ValueObject patterns for aggregate references.
                - Before finalizing, double-check to confirm you have not created any bidirectional references.
                - The `fromAggregate` and `toAggregate` fields in the `args` must accurately reflect the source and target of the reference. `toAggregate` must be identical to `referenceClass`.
            </description>
        </rule>
    </guidelines>
    
    <inference_guidelines>
        <title>Inference Guidelines</title>
        <rule id="1">**Domain Analysis:** Begin by comprehensively analyzing the provided aggregate relationships and domain context.</rule>
        <rule id="2">**Unidirectional Enforcement:** State clearly which reference direction was chosen and why, based on the principles of dependency, lifecycle, and stability. Explicitly mention that the reverse direction was intentionally omitted.</rule>
        <rule id="3">**Property Justification:** Justify the inclusion of any replicated properties by confirming their immutability and necessity for the reference.</rule>
        <rule id="4">**Direct Relation to Output:** The reasoning process should be directly related to the output result, not a general strategy.</rule>
    </inference_guidelines>

    <output_format>
        <title>JSON Output Format</title>
        <description>The output must be a JSON object structured as follows. Provide clean JSON without comments.</description>
        <schema>
{
    "actions": [
        {
            "objectType": "ValueObject",
            "ids": {
                "boundedContextId": "<boundedContextId>",
                "aggregateId": "<aggregateId>",
                "valueObjectId": "<valueObjectId>"
            },
            "args": {
                "valueObjectName": "<valueObjectName>",
                "referenceClass": "<referenceClassName>",
                "fromAggregate": "<source_aggregate_name>",
                "toAggregate": "<target_aggregate_name>",
                "properties": [
                    {
                        "name": "<propertyName>",
                        ["type": "<propertyType>"], // If the type is String, do not specify the type.
                        ["isKey": true] // Write only if there is a primary key.
                    }
                ]
            }
        }
    ],
    "omittedReferences": [
        {
            "fromAggregate": "<source_aggregate_name>",
            "toAggregate": "<target_aggregate_name>",
            "reason": "<reason_for_omission>"
        }
    ]
}
        </schema>
    </output_format>
</instruction>"""

    def _build_json_example_input_format(self) -> Optional[Dict[str, Any]]:
        deleted_properties = ESValueSummarizeWithFilter.KEY_FILTER_TEMPLATES["aggregateOuterStickers"] + ESValueSummarizeWithFilter.KEY_FILTER_TEMPLATES["aggregateInnerStickers"]
        return {
            "summarized_existing_eventstorming_model": XmlUtil.from_dict({
                "deletedProperties": deleted_properties,
                "boundedContexts": [
                    {
                        "id": "bc-order",
                        "name": "orderservice",
                        "aggregates": [
                            {
                                "id": "agg-order",
                                "name": "Order",
                                "properties": [
                                    {
                                        "name": "orderId",
                                        "type": "Long",
                                        "isKey": True
                                    },
                                    {
                                        "name": "orderDate",
                                        "type": "Date"
                                    },
                                    {
                                        "name": "totalAmount",
                                        "type": "Integer"
                                    }
                                ]
                            },
                            {
                                "id": "agg-customer",
                                "name": "Customer",
                                "properties": [
                                    {
                                        "name": "customerId",
                                        "type": "Long",
                                        "isKey": True
                                    },
                                    {
                                        "name": "name"
                                    },
                                    {
                                        "name": "gender"
                                    },
                                    {
                                        "name": "birthDate",
                                        "type": "Date"
                                    },
                                    {
                                        "name": "email"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }),
            
            "suggested_structure": XmlUtil.from_dict({
                "OrderManagement": [
                    {
                        "aggregate": {
                            "name": "Order",
                            "alias": "Order"
                        },
                        "valueObjects": [
                            {
                                "name": "CustomerReference",
                                "alias": "Customer Reference",
                                "referencedAggregate": {
                                    "name": "Customer",
                                    "alias": "Customer"
                                }
                            }
                        ]
                    }
                ],
                "CustomerManagement": [
                    {
                        "aggregate": {
                            "name": "Customer",
                            "alias": "Customer"
                        },
                        "valueObjects": [
                            {
                                "name": "OrderReference",
                                "alias": "Order Reference",
                                "referencedAggregate": {
                                    "name": "Order",
                                    "alias": "Order"
                                }
                            }
                        ]
                    }
                ]
            }),

            "target_references": XmlUtil.from_dict(["OrderReference", "CustomerReference"])
        }

    def _build_json_example_output_format(self) -> Dict[str, Any]:
        return {
            "omittedReferences": [
                {
                    "fromAggregate": "Customer",
                    "toAggregate": "Order",
                    "reason": "A reference from Customer to Order was omitted to enforce a unidirectional relationship. The Order's lifecycle is dependent on the Customer, making Customer the more stable aggregate that should be referenced."
                }
            ],
            "actions": [
                {
                    "objectType": "ValueObject",
                    "ids": {
                        "boundedContextId": "bc-order",
                        "aggregateId": "agg-order",
                        "valueObjectId": "vo-customer-id"
                    },
                    "args": {
                        "fromAggregate": "Order",
                        "toAggregate": "Customer",
                        "valueObjectName": "CustomerReference",
                        "referenceClass": "Customer",
                        "properties": [
                            {
                                "name": "customerId",
                                "type": "Long",
                                "isKey": True
                            },
                            {
                                "name": "gender"
                            },
                            {
                                "name": "birthDate",
                                "type": "Date"
                            }
                        ]
                    }
                }
            ]
        }
    
    def _build_json_user_query_input_format(self) -> Dict[str, Any]:
        inputs = self.client.get("inputs")
        return {
            "summarized_existing_eventstorming_model": XmlUtil.from_dict(inputs.get("summarizedESValue")),
            "suggested_structure": XmlUtil.from_dict(inputs.get("draftOption")),
            "target_references": XmlUtil.from_dict(inputs.get("targetReferences"))
        }

    def _post_process_to_structured_output(self, output: CreateAggregateClassIdByDraftsOutput) -> CreateAggregateClassIdByDraftsOutput:
        try:
            filtered_actions = []
            for action in output.actions:
                from_aggregate = action.args.fromAggregate.lower()
                to_aggregate = action.args.toAggregate.lower()

                is_exist = False
                for omitted_reference in output.omittedReferences:
                    omitted_from_aggregate = omitted_reference.fromAggregate.lower()
                    omitted_to_aggregate = omitted_reference.toAggregate.lower()

                    if omitted_from_aggregate == from_aggregate and omitted_to_aggregate == to_aggregate:
                        is_exist = True
                        break
    
                if not is_exist:
                    filtered_actions.append(action)
        
            output.actions = filtered_actions
            return output
        except (json.JSONDecodeError, AttributeError):
            raise ValueError("Invalid JSON format")