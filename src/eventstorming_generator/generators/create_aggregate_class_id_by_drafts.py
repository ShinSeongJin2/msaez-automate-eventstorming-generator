from typing import Any, Dict, Optional
from .base import BaseGenerator
from ..utils import ESValueSummarizeWithFilter

class CreateAggregateClassIdByDrafts(BaseGenerator):
    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        self.inputs_types_to_check = ["summarizedESValue", "draftOption", "targetReferences"]
        super().__init__(model_name, model_kwargs, client)

    def _build_agent_role_prompt(self) -> str:
        return """Role: Senior Domain-Driven Design (DDD) Expert

Goal: To create optimal, unidirectional reference structures between aggregates that maintain domain integrity while minimizing coupling, ensuring proper implementation of value objects and aggregate references based on DDD principles.

Backstory: With decades of hands-on experience implementing DDD in complex enterprise systems, I've developed deep expertise in strategic context mapping and aggregate relationship management. My methodical approach is driven by a commitment to clean architecture principles and optimal domain modeling. My work consistently balances technical excellence with business domain alignment, prioritizing maintainable and scalable solutions that protect domain invariants across aggregate boundaries.

Operational Guidelines:
* Analyze aggregate relationships comprehensively before recommending reference structures
* Always implement strictly unidirectional references between aggregates, never bidirectional
* Select reference direction based on lifecycle dependency, stability, and query patterns
* Only replicate truly immutable or near-immutable properties across aggregate boundaries
* Provide clear justification for all design decisions based on DDD principles
* Optimize reference structures for query performance while maintaining domain integrity
* Balance technical considerations with domain model clarity and business rules
* Ensure all recommendations follow proper ValueObject patterns for aggregate references"""

    def _build_task_guidelines_prompt(self) -> str:
        return """You will need to create the appropriate ValueObject that references other Aggregates as foreign keys, based on the provided EventStorming configuration draft.

Please follow these rules:
1. Foreign Key Value Object Generation:
   * CRITICAL: Only implement ONE DIRECTION of reference between aggregates
   * When choosing direction, consider:
     - Which aggregate is the owner of the relationship
     - Which side is more stable and less likely to change
     - Query patterns and performance requirements
   * Example: In Order-Customer relationship, Order should reference Customer (not vice-versa)

2. Relationship Direction Decision:
   * NEVER create bidirectional references, even if suggested in the draft
   * For each pair of aggregates, choose only ONE direction based on:
     - Lifecycle dependency (dependent aggregate references the independent one)
     - Business invariants (aggregate enforcing rules references required data)
     - Access patterns (optimize for most frequent queries)

3. Property Replication:
   * Only replicate properties that are highly unlikely to change (e.g., birthDate, gender)
   * These near-immutable properties are safe for caching as they remain constant throughout the entity's lifecycle
   * Strictly avoid replicating volatile properties that change frequently
   * Each replicated property must be justified based on its immutability and business value
   * Examples of safe-to-replicate properties:
     - Date of birth (remains constant)
     - Gender (rarely changes)
     - Country of birth (permanent)
   * Examples of properties to avoid replicating:
     - Address (frequently changes)
     - Email (moderately volatile)
     - Phone number (changes occasionally)

4. Technical Considerations:
   * Handle composite keys appropriately when referenced Aggregate uses multiple identifiers
   * Include proper indexing hints for foreign key fields
   * Consider implementing lazy loading for referenced data
   * Maintain referential integrity through proper constraints

5. Edge Cases:
   * Handle null references and optional relationships
   * Consider cascade operations impact
   * Plan for reference cleanup in case of Aggregate deletion
   * Implement proper validation for circular references

6. Output Format:
   * Provide clean JSON without comments
   * Use consistent property naming
   * Include all required metadata
   * Specify proper data types and constraints

7. Output Limit
   * Generate the appropriate ValueObject only for the referceAggregate corresponding to the given targetReferences. However, if the creation of a ValueObject for a given targetReferences also creates bidirectional references, only one of them should be created as a ValueObject."""

    def _build_inference_guidelines_prompt(self) -> str:
        return """
Inference Guidelines:
1. The process of reasoning should be directly related to the output result, not a reference to a general strategy.
2. Begin by comprehensively analyzing the provided aggregate relationships and domain context.
3. Focus on key aspects:
   - **Domain Alignment:** Assess how the value object and its references integrate into the broader business domain.
   - **Unidirectional Relationship:** Ensure that references are implemented in a strictly unidirectional manner; choose the direction based on aggregate dependency, lifecycle, and stability.
   - **Property Considerations:** Identify and replicate only those properties that are immutable and critical for maintaining referential integrity.
"""

    def _build_request_format_prompt(self) -> str:
        return ESValueSummarizeWithFilter.get_guide_prompt()

    def _build_json_response_format(self) -> str:
        return """
{
    "inference": "<inference>",
    "result": {
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
                    "properties": [
                        {
                            "name": "<propertyName>",
                            ["type": "<propertyType>"], // If the type is String, do not specify the type.
                            ["isKey": true] // Write only if there is a primary key.
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
            },

            "Suggested Structure": {
                "OrderManagement": [
                    {
                        "aggregate": {
                            "name": "Order",
                            "alias": "Order"
                        },
                        "enumerations": [],
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
                        "enumerations": [],
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
            },

            "Target References": ["OrderReference", "CustomerReference"]
        }

    def _build_json_example_output_format(self) -> Dict[str, Any]:
        return {
            "inference": """- Unidirectional Reference Selection: Among the aggregates in the model (Order and Customer), the decision was made to establish a one-way reference from the Order aggregate to the Customer aggregate. This aligns with the requirement to avoid bidirectional references, ensuring that only one direction is implemented.
- Domain & Lifecycle Considerations: The Customer aggregate is recognized as the stable, independent entity, making it the ideal candidate for being referenced by the Order. This approach addresses lifecycle dependencies and reflects real-world business invariants.
- Property Replication: Only properties that are immutable and critical for maintaining referential integrity—namely, the primary key (customerId), alongside near-immutable properties such as gender and birthDate—are replicated. This minimizes redundancy and avoids the pitfalls of copying volatile data.
Overall, this inference ensures that the generated ValueObject adheres to the design rules, maintains domain clarity, and promotes referential integrity without creating unwanted bidirectional dependencies.""",
            "result": {
                "actions": [
                    {
                        "objectType": "ValueObject",
                        "ids": {
                            "boundedContextId": "bc-order",
                            "aggregateId": "agg-order",
                            "valueObjectId": "vo-customer-id"
                        },
                        "args": {
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
        }
    
    def _build_json_user_query_input_format(self) -> Dict[str, Any]:
        inputs = self.client.get("inputs")
        return {
            "Summarized Existing EventStorming Model": inputs.get("summarizedESValue"),

            "Suggested Structure": inputs.get("draftOption"),

            "Target References": inputs.get("targetReferences"),

            "Final Check": """
CRITICAL RULES FOR REFERENCE GENERATION:
1. STRICT UNIDIRECTIONAL REFERENCE ONLY:
   - When draft shows two-way relationship, you MUST choose only ONE direction
   - Never generate both directions of references
   - Example: If Order->Customer and Customer->Order are in draft, implement ONLY Order->Customer

2. Direction Selection Criteria:
   - Choose based on dependency (dependent entity references independent one)
   - Consider lifecycle management (e.g., Order depends on Customer)
   - Optimize for most common query patterns

3. Property Guidelines:
   - Avoid adding properties that might change
   - Include only the minimum required reference properties

4. Implementation Check:
   - Verify you're generating only ONE direction of reference
   - Double-check you haven't created any bidirectional references
`"""
        }