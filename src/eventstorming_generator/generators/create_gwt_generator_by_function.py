from typing import Any, Dict, Optional
from .base import BaseGenerator
from ..utils import ESValueSummarizeWithFilter
from ..models import CreateGWTGeneratorByFunctionOutput

class CreateGWTGeneratorByFunction(BaseGenerator):
    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        self.inputs_types_to_check = ["summarizedESValue", "description", "targetCommandAliases"]
        super().__init__(model_name, model_kwargs, client, structured_output_class=CreateGWTGeneratorByFunctionOutput)

    def _build_agent_role_prompt(self) -> str:
        return """Role: Senior Domain-Driven Design (DDD) Expert and Test Engineering Specialist

Goal: To create precise, comprehensive Given-When-Then (GWT) scenarios that validate domain behaviors in event-driven architectures while transforming business requirements into structured, executable acceptance criteria.

Backstory: With extensive experience in behavior-driven development, I've mastered the art of identifying and testing domain invariants, business constraints, and state transitions across aggregate lifecycles. My approach combines rigorous technical precision with business readability, enabling me to detect edge cases and boundary conditions that might compromise domain integrity. I excel at maintaining consistency between commands, events, and aggregate states, ensuring proper causality and temporal relationships throughout the testing process.

Operational Guidelines:
* Craft GWT scenarios that precisely validate domain behaviors and business rules
* Identify and test all invariants and business constraints within bounded contexts
* Create test scenarios that verify correct state transitions across aggregate lifecycles
* Ensure complete command-event flow validation with proper causality relationships
* Design test cases that maintain consistency between commands, events, and aggregate states
* Detect and address edge cases and boundary conditions that might compromise domain integrity
* Capture complex business process validations through meaningful test examples
* Balance technical precision with business readability in all test specifications
* Implement best practices from Behavior-Driven Development (BDD) and Test-Driven Development (TDD)
* Transform abstract business requirements into concrete, executable acceptance criteria"""

    def _build_task_guidelines_prompt(self) -> str:
        return f"""You need to extract the right GWT (Given, When, Then) cases from the user's requirements and add them to the right commands in the given bounded context.

Please follow these rules:
1. Requirements Analysis:
   - Extract all relevant GWT scenarios from the provided requirements
   - Each GWT must be directly related to the specified command IDs
   - Ensure full coverage of acceptance criteria and business rules
   - Consider domain events and their business meanings for comprehensive test coverage
   - Take into account context relationships when designing cross-boundary scenarios

2. GWT Structure:
   - Given: Must reference valid Aggregate state with realistic property values
   - When: Must match Command properties exactly as defined in the schema
   - Then: Must include all mandatory Event properties with expected outcomes
   - Leverage event definitions to ensure proper event property mapping

3. Quality Guidelines:
   - Generate unique, non-duplicated GWT scenarios
   - Each scenario should test a specific aspect or business rule
   - Include both positive and negative test scenarios
   - Ensure property values are realistic and type-compatible
   - Consider event descriptions and business meanings for realistic test data

4. Property Mapping:
   - Given: Use only properties defined in the Aggregate
   - When: Include all required Command parameters
   - Then: Map to all relevant Event properties using event definitions
   - Use "N/A" only for truly unrelated properties

5. Validation Rules:
   - Verify all business constraints are covered
   - Include boundary conditions and edge cases
   - Consider state transitions and their validity
   - Check for proper error scenarios
   - Incorporate context relationship patterns when applicable

6. Event-Driven Considerations:
   - Use provided event definitions to understand expected outcomes
   - Ensure Then scenarios align with event descriptions and display names
   - Consider event-driven workflows and state changes

7. Context Boundary Awareness:
   - Be mindful of context relationships when designing scenarios
   - Consider how external context interactions might affect test scenarios
   - Include scenarios that validate proper boundary interactions

8. Output Format:
   - Provide clean JSON without comments
   - Use consistent property naming
   - Ensure all required fields are populated
   - Maintain proper value types for each property"""

    def _build_inference_guidelines_prompt(self) -> str:
        return """
Inference Guidelines:
1. The process of reasoning should be directly related to the output result, not a reference to a general strategy.
2. Context Assessment: Evaluate the provided business requirements, domain context, and target command details to determine the core testing scenarios.
3. Validation & Mapping: Ensure that the inferred GWT scenarios accurately map Aggregates, Commands, and Events based on the business rules and domain constraints.
4. Synthesis & Decision Making: Integrate domain expertise to synthesize concise and precise GWT scenarios from the analyzed inputs, while considering edge cases, error handling, and consistency.
"""

    def _build_request_format_prompt(self) -> str:
        return ESValueSummarizeWithFilter.get_guide_prompt()

    def _build_json_response_format(self) -> str:
        return """
{
   "inference": "<inference>",
   "result": [
        {
            "targetCommandId": "<targetCommandId>",
            "gwts": [
                {
                    "given": {
                        "name": "<givenName>", // You can write the name of Aggregate
                        "values": {
                            // There are three types of attribute values you can write.
                            // 1. Write an actual possible value(You can write String, Number, Boolean, Array, Object, etc.)
                            // 2. If the current value is empty, write null.
                            // 3. If the attribute seems unrelated to this GWT, write "N/A".
                            "<attributeName>": <attributeValue|null|"N/A">
                        }
                    },

                    "when": {
                        "name": "<whenName>", // You can write the name of Command
                        "values": {
                            "<attributeName>": <attributeValue|null|"N/A">
                        }
                    },

                    "then": {
                        "name": "<thenName>", // You can write the name of Event
                        "values": {
                            "<attributeName>": <attributeValue|null|"N/A">
                        }
                    }
                }
            ]
        }
    ]
}
"""

    def _build_json_example_input_format(self) -> Optional[Dict[str, Any]]:
        return {
            "Current Bounded Context": {
                "deletedProperties": [],
                "boundedContexts": [
                    {
                        "id": "bc-inventory",
                        "name": "inventory",
                        "aggregates": [
                            {
                                "id": "agg-product",
                                "name": "Product",
                                "properties": [
                                    {
                                        "name": "productId",
                                        "type": "String",
                                        "isKey": True
                                    },
                                    {
                                        "name": "name",
                                        "type": "String"
                                    },
                                    {
                                        "name": "quantity",
                                        "type": "Integer"
                                    },
                                    {
                                        "name": "status",
                                        "type": "ProductStatus"
                                    },
                                    {
                                        "name": "category",
                                        "type": "Category"
                                    }
                                ],
                                "entities": [
                                    {
                                        "id": "ent-category",
                                        "name": "Category",
                                        "properties": [
                                            {
                                                "name": "categoryId",
                                                "type": "String"
                                            },
                                            {
                                                "name": "name",
                                                "type": "String"
                                            },
                                            {
                                                "name": "description",
                                                "type": "String"
                                            }
                                        ]
                                    }
                                ],
                                "enumerations": [
                                    {
                                        "id": "enum-productStatus",
                                        "name": "ProductStatus",
                                        "items": [
                                            "AVAILABLE",
                                            "OUT_OF_STOCK",
                                            "DISCONTINUED"
                                        ]
                                    }
                                ],
                                "commands": [
                                    {
                                        "id": "cmd-addStock",
                                        "name": "AddStock",
                                        "api_verb": "PATCH",
                                        "isRestRepository": True,
                                        "outputEvents": [
                                            {
                                                "id": "evt-stockAdded",
                                                "name": "StockAdded"
                                            }
                                        ],
                                        "properties": [
                                            {
                                                "name": "productId",
                                                "type": "String"
                                            },
                                            {
                                                "name": "quantity",
                                                "type": "Integer"
                                            }
                                        ]
                                    },
                                    {
                                        "id": "cmd-discontinueProduct",
                                        "name": "DiscontinueProduct",
                                        "api_verb": "PATCH",
                                        "isRestRepository": True,
                                        "outputEvents": [
                                            {
                                                "id": "evt-productDiscontinued",
                                                "name": "ProductDiscontinued"
                                            }
                                        ],
                                        "properties": [
                                            {
                                                "name": "productId",
                                                "type": "String"
                                            },
                                            {
                                                "name": "reason",
                                                "type": "String"
                                            }
                                        ]
                                    }
                                ],
                                "events": [
                                    {
                                        "id": "evt-stockAdded",
                                        "name": "StockAdded",
                                        "properties": [
                                            {
                                                "name": "productId",
                                                "type": "String"
                                            },
                                            {
                                                "name": "quantity",
                                                "type": "Integer"
                                            },
                                            {
                                                "name": "newTotalQuantity",
                                                "type": "Integer"
                                            }
                                        ]
                                    },
                                    {
                                        "id": "evt-productDiscontinued",
                                        "name": "ProductDiscontinued",
                                        "properties": [
                                            {
                                                "name": "productId",
                                                "type": "String"
                                            },
                                            {
                                                "name": "reason",
                                                "type": "String"
                                            },
                                            {
                                                "name": "discontinuedDate",
                                                "type": "Date"
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            
            "Functional Requirements": """# Bounded Context Overview: Inventory Management

## Role
Manages product stock levels, including additions, and discontinuations. The primary user is an inventory manager responsible for maintaining accurate inventory records.

# Requirements

## User Stories

### Add Stock to Product
As an inventory manager, I want to add stock to existing products so that we can maintain accurate inventory levels.
**Acceptance Criteria:**
- Stock quantity must be a positive number.
- The product must exist in the system.
- The system should update the total quantity after addition.
- Stock addition should be logged for audit.

### Discontinue Product
As a product manager, I want to discontinue products that are no longer sold so that they are not available for future orders.
**Acceptance Criteria:**
- Must provide a reason for discontinuation.
- The product status should be updated to DISCONTINUED.
- The discontinuation date should be recorded.
- Cannot discontinue already discontinued products.

## Business Rules
- **StockQuantityValidation:** Stock quantity must be greater than zero.
- **DiscontinuationReason:** Reason for discontinuation is mandatory and must be descriptive.

## Key Events
- **StockAdded:** Triggered when stock is added to a product, increasing its quantity.
- **ProductDiscontinued:** Occurs when a product is marked as discontinued and is no longer available for sale.
- **StockBelowThreshold:** Fired when the stock level of a product drops below a predefined threshold.

## DDL

-- Products Table
CREATE TABLE products (
    product_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    status ENUM('AVAILABLE', 'OUT_OF_STOCK', 'DISCONTINUED') NOT NULL,
    category_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

-- Categories Table
CREATE TABLE categories (
    category_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

## Context Relations

### InventoryToSales
- **Type:** Pub/Sub
- **Direction:** sends to Sales Management
- **Reason:** To inform the sales system about changes in stock levels to reflect available inventory.
- **Interaction Pattern:** The inventory context publishes stock change events (e.g., stock added/decreased), which are subscribed to by the sales system.
""",
            
            "Target Command Ids": "cmd-addStock, cmd-discontinueProduct"
        }

    def _build_json_example_output_format(self) -> Dict[str, Any]:
        return {
            "inference": """The generated output scenarios are based on a detailed analysis of the provided aggregate, command, and event definitions within the current bounded context. For 'cmd-addStock', the inference emphasizes that the 'Product' aggregate starts with specific attributes (e.g., productId, name, initial quantity, and status) and reflects a successful stock update when the 'AddStock' command is executed, resulting in a 'StockAdded' event with an updated total quantity. For 'cmd-discontinueProduct', the scenario verifies that an appropriate state transition occurs by incorporating a valid discontinuation reason and recording a discontinuation date in the 'ProductDiscontinued' event. This systematic approach ensures that each command's GWT scenario correctly captures both the intended business logic and the underlying domain constraints, providing robust and comprehensive test coverage.""",
            "result": [
                {
                    "targetCommandId": "cmd-addStock",
                    "gwts": [
                        {
                            "given": {
                                "name": "Product",
                                "values": {
                                    "productId": "PROD-001",
                                    "name": "Sample Product",
                                    "quantity": 100,
                                    "status": "AVAILABLE"
                                }
                            },
                            "when": {
                                "name": "AddStock",
                                "values": {
                                    "productId": "PROD-001",
                                    "quantity": 50
                                }
                            },
                            "then": {
                                "name": "StockAdded",
                                "values": {
                                    "productId": "PROD-001",
                                    "quantity": 50,
                                    "newTotalQuantity": 150
                                }
                            }
                        }
                    ]
                },
                {
                    "targetCommandId": "cmd-discontinueProduct",
                    "gwts": [
                        {
                            "given": {
                                "name": "Product",
                                "values": {
                                    "productId": "PROD-001",
                                    "name": "Sample Product",
                                    "status": "AVAILABLE"
                                }
                            },
                            "when": {
                                "name": "DiscontinueProduct",
                                "values": {
                                    "productId": "PROD-001",
                                    "reason": "Product replaced by newer model"
                                }
                            },
                            "then": {
                                "name": "ProductDiscontinued",
                                "values": {
                                    "productId": "PROD-001",
                                    "reason": "Product replaced by newer model",
                                    "discontinuedDate": "2024-03-20T00:00:00Z"
                                }
                            }
                        }
                    ]
                }
            ]
        }
    
    def _build_json_user_query_input_format(self) -> Dict[str, Any]:
        inputs = self.client.get("inputs")
        return {
            "Current Bounded Context": inputs.get("summarizedESValue"),

            "Functional Requirements": inputs.get("description"),

            "Target Command Ids": ", ".join(inputs.get("targetCommandAliases")),

            "Final Check List": """
* Make sure each command has an appropriate GWT from the user's requirements.
* Make sure your scenarios reflect the best use of GWT in your code generation.
* The generated GWT must have the properties found in the Aggregate, Command, and Event presented.
* Consider the provided event definitions and their business meanings when creating Then scenarios.
* Take into account context relationships and their interaction patterns when designing cross-boundary test scenarios.
* Ensure event-driven workflows are properly validated through the GWT scenarios.
"""
        }