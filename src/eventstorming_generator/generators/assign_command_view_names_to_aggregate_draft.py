from typing import Any, Dict, Optional
from .base import BaseGenerator
from ..models import AssignCommandViewNamesToAggregateDraftOutput

class AssignCommandViewNamesToAggregateDraft(BaseGenerator):
    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        self.inputs_types_to_check = ["aggregateDrafts", "siteMap"]
        super().__init__(model_name, model_kwargs, client, structured_output_class=AssignCommandViewNamesToAggregateDraftOutput)

    def _build_agent_role_prompt(self) -> str:
        return """Role: Senior Business Analyst and Domain Expert for UI/UX to Domain Model Mapping

Goal: To analyze user interface site map specifications and extract meaningful business commands and read operations, mapping them to appropriate domain aggregates following Domain-Driven Design principles.

Backstory: With extensive experience in translating user interface requirements into domain models, I specialize in identifying the underlying business operations represented by UI elements and pages. My approach focuses on understanding the business intent behind each UI component and mapping it to appropriate domain actions within the correct aggregate boundaries. I excel at recognizing patterns in site maps, extracting implicit business operations, and ensuring proper aggregate assignment based on data ownership and business responsibilities.

Operational Guidelines:
* Analyze site map entries to identify underlying business operations and data access patterns
* Extract commands (write operations) and read models (query operations) based on UI functionality descriptions
* Map extracted operations to appropriate aggregates based on domain responsibility and data ownership
* Ensure proper separation of concerns between different aggregates
* Identify unique operations while avoiding duplication across different site map entries
* Apply Domain-Driven Design principles for aggregate boundary definition
* Focus on business semantics rather than technical implementation details
* Consider user workflows and business processes implicit in the site map structure"""

    def _build_task_guidelines_prompt(self) -> str:
        return f"""You need to analyze the provided site map and extract meaningful business commands and read models, then assign them to the appropriate aggregates.

Please follow these rules:

Site Map Analysis Guidelines:
1. Analyze each site map entry's title and description to identify business operations
2. Look for action verbs that indicate write operations (commands): create, update, delete, process, submit, approve, etc.
3. Look for query patterns that indicate read operations (read models): view, list, search, display, show, etc.
4. Consider the business context and workflows implied by the site map structure

Command Extraction Rules:
1. Extract commands based on business operations implied in site map descriptions
2. Use clear, business-meaningful command names following Verb + Noun pattern (e.g., ProcessPayment, CreateOrder)
3. Consider CRUD operations but focus on business semantics (e.g., "ApproveApplication" instead of "UpdateApplicationStatus")
4. Avoid duplicate commands - if multiple site map entries imply the same operation, extract it only once

Read Model Extraction Rules:
1. Extract read models for query operations and data display needs
2. Use descriptive names following Noun + Purpose pattern (e.g., OrderSummary, CustomerList)
3. Consider pagination and filtering needs for list operations
4. Focus on business data views rather than technical screens

Aggregate Assignment Guidelines:
1. Assign operations to aggregates based on data ownership and business responsibility
2. Commands should be assigned to the aggregate that owns the primary data being modified
3. Read models should be assigned to the aggregate that owns the primary data being queried
4. Consider aggregate boundaries and avoid cross-aggregate operations
5. When in doubt, assign to the most relevant aggregate based on business context

Naming Conventions:
1. All command and read model names must be in English
2. Use PascalCase for naming (e.g., ProcessLoanApplication, ViewLoanHistory)
3. Commands should be actionable verbs + nouns
4. Read models should be descriptive nouns that indicate the data being retrieved
5. Ensure names are business-meaningful and self-explanatory

Language and Format:
1. All technical names must be in English
2. Follow consistent naming patterns across all extracted elements
3. Ensure proper business terminology alignment

Deduplication Rules:
1. If multiple site map entries result in the same command or read model, include it only once
2. Use the most specific referencedId when deduplicating (prefer the entry that most directly implies the operation)
3. Ensure no duplicate operations within the same aggregate

Avoid:
1. Overly technical or implementation-specific names
2. Duplicate operations across different site map entries
3. Commands that don't represent actual business operations
4. Read models that are too granular or don't add business value
5. Incorrect aggregate assignment that violates domain boundaries"""

    def _build_inference_guidelines_prompt(self) -> str:
        return """
Inference Guidelines:
1. The reasoning process should directly relate to the extraction and assignment decisions, not general strategies.
2. Analytical Focus: Prioritize understanding business operations implied by UI components and ensuring proper domain model mapping.
3. Pattern Recognition: Identify recurring patterns in site map entries that suggest similar business operations across different contexts.
4. Domain Boundary Validation: Carefully evaluate aggregate assignments to ensure they respect domain boundaries and business ownership.
5. Operation Extraction: For each extracted command or read model, clearly justify why it was derived from the site map entry and why it was assigned to a specific aggregate.
6. Deduplication Logic: When similar operations are found across multiple site map entries, explain the deduplication decision and reference selection.
7. Business Context Consideration: Consider the broader business workflow and how extracted operations fit into the overall domain model.
"""

    def _build_json_response_format(self) -> str:
        return """
{
    "inference": "<detailed_reasoning_and_analysis>",
    "result": {
        "extractedCommands": [
            {
                "referencedId": "<site_map_entry_id>", // ID of the site map entry this command was extracted from
                "aggregateName": "<target_aggregate_name>", // Name of the aggregate this command should be assigned to
                "commandName": "<business_command_name>" // Business-meaningful command name following Verb+Noun pattern
            }
        ],
        "extractedReadModels": [
            {
                "referencedId": "<site_map_entry_id>", // ID of the site map entry this read model was extracted from
                "aggregateName": "<target_aggregate_name>", // Name of the aggregate this read model should be assigned to
                "readModelName": "<business_read_model_name>" // Business-meaningful read model name following Noun+Purpose pattern
            }
        ]
    }
}
"""

    def _build_json_example_input_format(self) -> Optional[Dict[str, Any]]:
        return {
            "Aggregate Drafts": [
                {
                    "name": "Product",
                    "alias": "Product Management"
                },
                {
                    "name": "Order",
                    "alias": "Order Processing"
                },
                {
                    "name": "Customer",
                    "alias": "Customer Management"
                }
            ],
            "Site Map": [
                {
                    "boundedContext": "Catalog",
                    "description": "Product catalog browsing, searching, and detailed product information display",
                    "id": "product-catalog",
                    "title": "Product Catalog"
                },
                {
                    "boundedContext": "Sales",
                    "description": "Shopping cart management, order creation, and checkout process",
                    "id": "shopping-cart",
                    "title": "Shopping Cart & Checkout"
                },
                {
                    "boundedContext": "Sales",
                    "description": "Order history viewing and order status tracking for customers",
                    "id": "order-tracking",
                    "title": "Order Management"
                },
                {
                    "boundedContext": "Inventory",
                    "description": "Product inventory management and stock level monitoring",
                    "id": "inventory-management",
                    "title": "Inventory Control"
                }
            ]
        }

    def _build_json_example_output_format(self) -> Dict[str, Any]:
        return {
            "inference": "Analyzing the site map entries, I identified several business operations: Product catalog browsing implies search and view operations for products. Shopping cart management involves adding/removing items and creating orders. Order tracking requires viewing order history and status. Inventory management involves stock monitoring and updates. Based on aggregate ownership, product-related operations are assigned to Product aggregate, order operations to Order aggregate, and inventory operations could be assigned to Product aggregate as they manage product stock levels. Deduplication was applied where similar operations were implied across different entries.",
            "result": {
                "extractedCommands": [
                    {
                        "referencedId": "shopping-cart",
                        "aggregateName": "Order",
                        "commandName": "CreateOrder"
                    },
                    {
                        "referencedId": "shopping-cart",
                        "aggregateName": "Order",
                        "commandName": "AddItemToCart"
                    },
                    {
                        "referencedId": "shopping-cart",
                        "aggregateName": "Order",
                        "commandName": "RemoveItemFromCart"
                    },
                    {
                        "referencedId": "inventory-management",
                        "aggregateName": "Product",
                        "commandName": "UpdateStock"
                    }
                ],
                "extractedReadModels": [
                    {
                        "referencedId": "product-catalog",
                        "aggregateName": "Product",
                        "readModelName": "ProductCatalog"
                    },
                    {
                        "referencedId": "product-catalog",
                        "aggregateName": "Product",
                        "readModelName": "ProductDetails"
                    },
                    {
                        "referencedId": "order-tracking",
                        "aggregateName": "Order",
                        "readModelName": "OrderHistory"
                    },
                    {
                        "referencedId": "order-tracking",
                        "aggregateName": "Order",
                        "readModelName": "OrderStatus"
                    },
                    {
                        "referencedId": "inventory-management",
                        "aggregateName": "Product",
                        "readModelName": "StockLevel"
                    }
                ]
            }
        }
    
    def _build_json_user_query_input_format(self) -> Dict[str, Any]:
        inputs = self.client.get("inputs")
        return {
            "Aggregate Drafts": inputs.get("aggregateDrafts"),
            "Site Map": inputs.get("siteMap")
        } 