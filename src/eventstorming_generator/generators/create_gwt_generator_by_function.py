from typing import Any, Dict, Optional
from .xml_base import XmlBaseGenerator
from ..models import CreateGWTGeneratorByFunctionOutput
from ..utils import XmlUtil

class CreateGWTGeneratorByFunction(XmlBaseGenerator):
    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        self.inputs_types_to_check = ["summarizedESValue", "description", "targetCommandAlias"]
        super().__init__(model_name, CreateGWTGeneratorByFunctionOutput, model_kwargs, client)

    def _build_persona_info(self) -> Dict[str, str]:
        return {
            "persona": "Senior Domain-Driven Design (DDD) Expert and Test Engineering Specialist",
            "goal": "To create precise, comprehensive Given-When-Then (GWT) scenarios that validate domain behaviors in event-driven architectures while transforming business requirements into structured, executable acceptance criteria.",
            "backstory": "With extensive experience in behavior-driven development, I've mastered the art of identifying and testing domain invariants, business constraints, and state transitions across aggregate lifecycles. My approach combines rigorous technical precision with business readability, enabling me to detect edge cases and boundary conditions that might compromise domain integrity. I excel at maintaining consistency between commands, events, and aggregate states, ensuring proper causality and temporal relationships throughout the testing process."
        }

    def _build_task_instruction_prompt(self) -> str:
        return f"""<instruction>
    <core_instructions>
        <title>GWT Scenario Generation Task</title>
        <task_description>You need to extract the right GWT (Given, When, Then) cases from the user's requirements and add them to the right commands in the given bounded context.</task_description>
        
        <output_rules>
            <title>Output Format</title>
            <rule id="json_structure">The output must be a JSON object with two keys: "inference" and "result".</rule>
            <rule id="inference">The "inference" value should contain detailed reasoning about the GWT design decisions, focusing on domain logic, test coverage, and adherence to requirements. It should not be a reference to general strategies.</rule>
            <rule id="result">The "result" value must be an object containing a "gwts" key, which is a list of GWT scenarios.</rule>
        </output_rules>

        <operational_guidelines>
            <title>Operational Guidelines</title>
            <rule id="validation">Craft GWT scenarios that precisely validate domain behaviors and business rules.</rule>
            <rule id="invariants">Identify and test all invariants and business constraints within bounded contexts.</rule>
            <rule id="state_transitions">Create test scenarios that verify correct state transitions across aggregate lifecycles.</rule>
            <rule id="flow_validation">Ensure complete command-event flow validation with proper causality relationships.</rule>
            <rule id="consistency">Design test cases that maintain consistency between commands, events, and aggregate states.</rule>
            <rule id="edge_cases">Detect and address edge cases and boundary conditions that might compromise domain integrity.</rule>
            <rule id="complexity">Capture complex business process validations through meaningful test examples.</rule>
            <rule id="readability">Balance technical precision with business readability in all test specifications.</rule>
            <rule id="best_practices">Implement best practices from Behavior-Driven Development (BDD) and Test-Driven Development (TDD).</rule>
            <rule id="requirements_transformation">Transform abstract business requirements into concrete, executable acceptance criteria.</rule>
        </operational_guidelines>

        <gwt_rules>
            <title>GWT Generation Rules</title>
            <rule id="analysis">
                <title>Requirements Analysis</title>
                <item>Extract all relevant GWT scenarios from the provided requirements.</item>
                <item>Each GWT must be directly related to the specified command ID.</item>
                <item>Ensure full coverage of acceptance criteria and business rules.</item>
                <item>Consider domain events and their business meanings for comprehensive test coverage.</item>
                <item>Take into account context relationships when designing cross-boundary scenarios.</item>
            </rule>
            <rule id="structure">
                <title>GWT Structure</title>
                <item>Scenario: A brief, descriptive text explaining what business scenario or validation rule this GWT test covers (e.g., "Valid stock addition to existing product", "Rejection of negative stock quantity", "Error when adding stock to discontinued product").</item>
                <item>Given: For update/delete commands, this must reference a valid Aggregate state. For a create command, `aggregateValues` should be empty (`{{}}`) for a successful creation. For a failure scenario (e.g., duplicate key), it should contain only the minimal conflicting properties.</item>
                <item>When: Must match Command properties exactly as defined in the schema.</item>
                <item>Then: For a positive scenario, this must include all mandatory Event properties with expected outcomes. For a negative scenario, `eventValues` should contain an `error` key with a descriptive error code string (e.g., `{{"error": "PRODUCT_IS_DISCONTINUED"}}`).</item>
            </rule>
            <rule id="quality">
                <title>Quality Guidelines</title>
                <item>Generate multiple unique, non-duplicated GWT scenarios, each testing a specific aspect or rule.</item>
                <item>CRITICAL: Include both positive (happy-path) and negative scenarios. Negative scenarios should cover validation rules (e.g., invalid input), business constraint violations, and boundary/edge cases.</item>
                <item>Use realistic, concrete data for property values (e.g., "Clean Code" instead of "Sample Product"), not generic placeholders.</item>
                <item>Ensure property values are realistic and type-compatible.</item>
            </rule>
            <rule id="mapping">
                <title>Property Mapping and Value Assignment</title>
                <item>Given: Use only properties defined in the Aggregate.</item>
                <item>When: Include all required Command parameters.</item>
                <item>Then: Map to all relevant Event properties using event definitions.</item>
                <item>CRITICAL: `aggregateValues`, `commandValues`, and `eventValues` must be valid dictionaries with meaningful, actual values. NEVER use `null` or empty values. Exclude irrelevant properties entirely rather than using "N/A".</item>
            </rule>
            <rule id="validation_rules">
                <title>Validation Rules</title>
                <item>Verify all business constraints are covered, including boundary conditions and edge cases.</item>
                <item>Consider state transitions and their validity, including proper error scenarios.</item>
                <item>Incorporate context relationship patterns when applicable.</item>
            </rule>
            <rule id="event_driven">
                <title>Event-Driven Considerations</title>
                <item>Use provided event definitions to understand expected outcomes and ensure `Then` scenarios align with event details.</item>
                <item>Consider event-driven workflows and state changes.</item>
            </rule>
        </gwt_rules>

        <inference_guidelines>
            <title>Inference Guidelines</title>
            <rule id="relevance">The process of reasoning must be directly related to the output result, not a reference to a general strategy.</rule>
            <rule id="assessment">Evaluate the provided business requirements, domain context, and target command details to determine the core testing scenarios.</rule>
            <rule id="mapping_validation">Ensure that the inferred GWT scenarios accurately map Aggregates, Commands, and Events based on the business rules and domain constraints.</rule>
            <rule id="synthesis">Integrate domain expertise to synthesize concise and precise GWT scenarios from the analyzed inputs, while considering edge cases, error handling, and consistency.</rule>
        </inference_guidelines>
    </core_instructions>
</instruction>"""
    
    def _build_json_example_input_format(self) -> Optional[Dict[str, Any]]:
        return {
            "current_bounded_context": XmlUtil.from_dict({
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
            }),
            
            "functional_requirements": """# Bounded Context Overview: Inventory Management

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
            
            "target_command_id": "cmd-addStock"
        }

    def _build_json_example_output_format(self) -> Dict[str, Any]:
        return {
            "inference": """The generated output scenarios are based on a detailed analysis of the provided aggregate, command, and event definitions within the current bounded context. For 'cmd-addStock', the inference emphasizes that the 'Product' aggregate starts with specific attributes (e.g., productId, name, initial quantity, and status) and reflects a successful stock update when the 'AddStock' command is executed, resulting in a 'StockAdded' event with an updated total quantity. This systematic approach ensures that the command's GWT scenario correctly captures the intended business logic and the underlying domain constraints, providing robust and comprehensive test coverage.""",
            "result": {
                "gwts": [
                    {
                        "scenario": "Valid stock addition to existing product",
                        "given": {
                            "aggregateName": "Product",
                            "aggregateValues": {
                                "productId": "PROD-001",
                                "name": "High-Performance Gaming Mouse",
                                "quantity": 100,
                                "status": "AVAILABLE"
                            }
                        },
                        "when": {
                            "commandName": "AddStock",
                            "commandValues": {
                                "productId": "PROD-001",
                                "quantity": 50
                            }
                        },
                        "then": {
                            "eventName": "StockAdded",
                            "eventValues": {
                                "productId": "PROD-001",
                                "quantity": 50,
                                "newTotalQuantity": 150
                            }
                        }
                    },
                    {
                        "scenario": "Rejection of negative stock quantity",
                        "given": {
                            "aggregateName": "Product",
                            "aggregateValues": {
                                "productId": "PROD-001",
                                "name": "High-Performance Gaming Mouse",
                                "quantity": 100,
                                "status": "AVAILABLE"
                            }
                        },
                        "when": {
                            "commandName": "AddStock",
                            "commandValues": {
                                "productId": "PROD-001",
                                "quantity": -10
                            }
                        },
                        "then": {
                            "eventName": "StockAdded",
                            "eventValues": {
                                "error": "INVALID_STOCK_QUANTITY"
                            }
                        }
                    },
                    {
                        "scenario": "Error when adding stock to discontinued product",
                        "given": {
                            "aggregateName": "Product",
                            "aggregateValues": {
                                "productId": "PROD-002",
                                "name": "Vintage Mechanical Keyboard",
                                "quantity": 15,
                                "status": "DISCONTINUED"
                            }
                        },
                        "when": {
                            "commandName": "AddStock",
                            "commandValues": {
                                "productId": "PROD-002",
                                "quantity": 50
                            }
                        },
                        "then": {
                            "eventName": "StockAdded",
                            "eventValues": {
                                "error": "PRODUCT_IS_DISCONTINUED"
                            }
                        }
                    }
                ]
            }
        }
    
    def _build_json_user_query_input_format(self) -> Dict[str, Any]:
        inputs = self.client.get("inputs")
        return {
            "current_bounded_context": XmlUtil.from_dict(inputs.get("summarizedESValue")),
            "functional_requirements": inputs.get("description"),
            "target_command_id": inputs.get("targetCommandAlias"),
        }