from typing import Any, Dict, Optional
from .base import BaseGenerator
from ..utils import ESValueSummarizeWithFilter
from ..models import CreateAggregateActionsByFunctionOutput

class CreateAggregateActionsByFunction(BaseGenerator):
    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        self.inputs_types_to_check = ["summarizedESValue", "targetBoundedContext", "description", "draftOption", "targetAggregate"]
        super().__init__(model_name, model_kwargs, client, structured_output_class=CreateAggregateActionsByFunctionOutput)

    def _build_agent_role_prompt(self) -> str:
        return """Role: Domain-Driven Design (DDD) Architect and Strategic Modeling Expert

Goal: To translate complex business domains into well-structured software designs by creating precise bounded contexts, cohesive aggregates, and event-driven architectures that accurately capture domain knowledge, enforce business invariants, and provide adaptable models that evolve with changing business requirements.

Backstory: Drawing on over 15 years of experience implementing complex enterprise systems across diverse industries, I've developed deep expertise in strategic and tactical domain modeling. My methodical approach balances technical implementation with business needs, emphasizing clean domain boundaries and semantic integrity. I've successfully guided organizations through complex domain transformations by identifying core concepts and designing systems that speak the language of the business. My working style prioritizes correctness, maintainability, and elegant expression of domain concepts, allowing me to navigate even the most intricate business domains with clarity and precision.

Operational Guidelines:
* Prioritize identifying and implementing ubiquitous language patterns consistently across domain models and technical implementations
* Apply tactical DDD patterns (aggregates, entities, value objects, repositories, domain services) with precision to solve specific domain problems
* Enforce strict aggregate boundaries to maintain data consistency and transaction isolation
* Design event streams that capture complete domain state transitions and history
* Recommend appropriate bounded context integration patterns based on team relationships and communication needs
* Balance technical constraints with business requirements to create pragmatic domain models
* Leverage value objects to encapsulate related attributes and validation rules
* Use enumerations strategically to model discrete states, categories, and classification schemes
* Provide clear guidance on maintaining consistency within transaction boundaries
* Focus on designing models that evolve gracefully with changing business requirements"""

    def _build_task_guidelines_prompt(self) -> str:
        return """In your current event storming model, you need to write actions to add elements inside a particular Bounded Context following the structure provided by the user.

Please adhere to the following guidelines:

Data Type Rules:
1. For Aggregate properties, use:
   - Basic Java types: String, Long, Integer, Double, Boolean, Date
   - Custom types must be defined as either Enumeration or ValueObject.
2. For collections, use the 'List<ClassName>' syntax (e.g., List<String>).

Type Reference and Enumeration Rules:
3. When to use Enumerations:
   - When a property represents a fixed set of values or categories.
   - When the property value must be one of a predefined list.
   - When the property name ends with words such as Type, Status, Category, Level, Phase, or Stage.
   - Specifically, when storing state or status information, an Enumeration must be used.
   Example cases:
     • category → BookCategory (Enumeration)
     • status → OrderStatus (Enumeration)
     • type → ProductType (Enumeration)
     • level → MembershipLevel (Enumeration)
     • paymentMethod → PaymentMethod (Enumeration)

4. When to use ValueObjects:
   - When a group of related properties forms a meaningful concept and immutability is required.
   - **All ValueObjects must be directly associated with their Aggregate.** Do not define ValueObjects that are nested within or used by other ValueObjects.
   - Unless there is a special case, avoid creating meaningless ValueObjects. Instead, incorporate such properties directly within the Aggregate.
   - Refrain from creating an excessive number of ValueObjects.
   Example cases:
     • address → Address (street, city, zipCode)
     • period → DateRange (startDate, endDate)
     • money → Money (amount, currency)
     • contact → ContactInfo (phone, email, address)

Naming and Language Conventions:
5. Object names (classes, properties, methods) must be in English.
6. Supporting content (aliases, descriptions) must adhere to the preferred language setting.

Structural Rules:
7. Aggregates:
   - Must have exactly one primary key attribute.
   - For composite keys, create a ValueObject and use it as the primary key.
   - Reference other Aggregates using their class names rather than IDs.
   - Avoid creating separate transaction objects when the main Aggregate can manage its lifecycle. Do not duplicate properties by creating Transaction ValueObjects if they overlap with the main Aggregate.
   - Use the Aggregate root to manage state transitions and history. Consider Event Sourcing for tracking historical changes if needed.

8. ValueObjects:
   - Must be directly linked to an Aggregate; avoid defining ValueObjects that are internally nested or that represent subordinate structures.
   - Should encapsulate multiple, related properties and be immutable.
   - Prevent the creation of trivial or redundant ValueObjects by including properties directly in the Aggregate unless a special case dictates otherwise.
   - Do not generate an excessive number of ValueObjects.

Creation Guidelines:
9. Create only:
   - Aggregates listed under 'Aggregate to create'.
   - All ValueObjects from the provided structure that have a direct association with the Aggregate.
   - Enumerations for any property requiring a fixed set of values.
   - All supporting types needed for the properties.

10. Property Type Selection:
    - Opt for specific types over generic ones.
    - Example mappings:
      • startDate → Date
      • currentCapacity → Integer
      • price → Double
      • category → Enumeration
      • status → Enumeration

Type Dependency Resolution:
11. Before finalizing your result:
    - Validate all property types.
    - Create Enumerations for properties representing classifications, statuses, or types.
    - Ensure that all custom types are clearly defined.
    - Verify the appropriate usage of ValueObjects versus Enumerations.

Constraints:
12. Rules:
    - Only reference existing Aggregates without altering them.
    - Do not recreate types that already exist in the system.
    - Avoid including comments in the output JSON object.
    - Prevent duplicate elements in the model.
    - Do not use ValueObjects for properties that should be defined as Enumerations.
    - Refrain from appending type names (e.g., 'Enumeration' or 'ValueObject') to object names; use base names only (e.g., 'BookStatus' rather than 'BookStatusEnumeration').
    - Ensure names are unique across both new and existing elements, with no duplicates.

13. Required Elements:
    - Every ValueObject and Enumeration must be directly associated with an Aggregate.
    - Every generated ValueObject and Enumeration must be included as a named attribute in at least one Aggregate.
    - Implement all elements specified in the user's structure.
    - Accurately map all relationships.
    - Provide corresponding definitions for all custom types."""

    def _build_inference_guidelines_prompt(self) -> str:
        return """
Inference Guidelines:
1. The reasoning should directly inform the output result with specific design decisions rather than generic strategies.
2. Begin by thoroughly understanding the task requirements and the overall domain context.
3. Evaluate key design aspects, including domain alignment, adherence to Domain-Driven Design (DDD) principles, and technical feasibility.
4. Analyze the relationships and dependencies between Aggregates, ValueObjects, and Enumerations precisely.
5. Ensure that all design decisions comply with DDD best practices.
6. When properties represent state or status information, enforce the use of Enumerations to clearly define valid values.
7. Verify that every ValueObject and Enumeration is directly associated with an Aggregate; avoid nested or subordinate ValueObject definitions.
8. Avoid creating unnecessary or excessive ValueObjects; integrate properties directly into the Aggregate unless a distinct ValueObject offers significant encapsulation.
"""

    def _build_request_format_prompt(self) -> str:
        return ESValueSummarizeWithFilter.get_guide_prompt()

    def _build_json_response_format(self) -> str:
        if self.structured_output_class:
            return ""

        return """
{
    "inference": "<inference>",
    "result": {
        // aggregateId can be used when defining Enumeration, ValueObject that belong to an Aggregate.
        "aggregateActions": [
            {
                // Write the ActionName that you utilized in the previous steps
                "actionName": "<actionName>",
                "objectType": "Aggregate",
                "ids": {
                    "aggregateId": "<aggregateId>"
                },
                "args": {
                    "aggregateName": "<aggregateName>",
                    "aggregateAlias": "<aggregateAlias>",

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

        // ValueObjects are immutable objects defined by their attributes rather than their identity.
        // They are used to group related attributes that should be treated as a single unit.
        "valueObjectActions": [
            {
                "actionName": "<actionName>",
                "objectType": "ValueObject",
                "ids": {
                    "aggregateId": "<aggregateId>",
                    "valueObjectId": "<valueObjectId>"
                },
                "args": {
                    "valueObjectName": "<valueObjectName>",
                    "valueObjectAlias": "<valueObjectAlias>",

                    "properties": [
                        {
                            "name": "<propertyName>",
                            ["type": "<propertyType>"], // If the type is String, do not specify the type.
                            ["isKey": true], // Write only if there is a primary key.
                            ["isForeignProperty": true] // Whether it is a foreign key. Write only if this attribute references another table's attribute.
                        }
                    ]
                }
            }
        ],

        // If the type of property you want to add to the aggregate does not have an appropriate default Java type, you can create a new type as an enumeration.
        "enumerationActions": [
            {
                "actionName": "<actionName>",
                "objectType": "Enumeration",
                "ids": {
                    "aggregateId": "<aggregateId>",
                    "enumerationId": "<enumerationId>"
                },
                "args": {
                    "enumerationName": "<enumerationName>",
                    "enumerationAlias": "<enumerationAlias>",
                    
                    "properties": [
                        {
                            "name": "<propertyName>" // Must be in English
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
                        "actors": [
                            { "id": "act-customer", "name": "Customer" },
                            { "id": "act-admin", "name": "Admin" }
                        ],
                        "aggregates": [
                            {
                                "id": "agg-product",
                                "name": "Product",
                                "properties": [
                                    { "name": "productId", "type": "Long", "isKey": True },
                                    { "name": "name" },
                                    { "name": "price", "type": "Double" },
                                    { "name": "category", "type": "ProductCategory" },
                                    { "name": "stock", "type": "Integer" }
                                ],
                                "entities": [],
                                "enumerations": [
                                    {
                                        "id": "enum-product-category",
                                        "name": "ProductCategory",
                                        "items": ["ELECTRONICS", "FURNITURE", "CLOTHING", "FOOD"]
                                    }
                                ],
                                "valueObjects": [
                                    {
                                        "id": "vo-product-dimensions",
                                        "name": "ProductDimensions",
                                        "properties": [
                                            { "name": "length", "type": "Double" },
                                            { "name": "width", "type": "Double" },
                                            { "name": "height", "type": "Double" }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ],
            },
            
            "Bounded Context to Generate Actions": "orderservice",
            
            "Functional Requirements": {
                "userStories": [
                    {
                        "title": "Place New Order",
                        "description": "As a customer, I want to place a new order with my selected products to complete my purchase.",
                        "acceptance": [
                            "All selected products must be available in stock.",
                            "Customer information must be valid.",
                            "Payment should be processed successfully."
                        ]
                    },
                    {
                        "title": "View Order History",
                        "description": "As a customer, I want to view my past orders and their statuses.",
                        "acceptance": [
                            "Orders must be sorted by order date.",
                            "Order details are displayed correctly.",
                            "Filtering by order status is available."
                        ]
                    }
                ],
                "entities": {
                    "Customer": {
                        "properties": [
                            { "name": "customerId", "type": "Long", "required": True, "isPrimaryKey": True },
                            { "name": "name", "type": "String", "required": True },
                            { "name": "email", "type": "String", "required": True }
                        ]
                    },
                    "Order": {
                        "properties": [
                            { "name": "orderId", "type": "Long", "required": True, "isPrimaryKey": True },
                            { "name": "customerId", "type": "Long", "required": True, "isForeignKey": True, "foreignEntity": "Customer" },
                            { "name": "orderDate", "type": "Date", "required": True },
                            { "name": "totalAmount", "type": "Integer", "required": True }
                        ]
                    }
                },
                "businessRules": [
                    { "name": "ValidOrderTotal", "description": "Order total must be a positive value." },
                    { "name": "CustomerExists", "description": "Order must be associated with an existing customer." }
                ],
                "interfaces": {
                    "NewOrder": {
                        "sections": [
                            {
                                "name": "OrderDetails",
                                "type": "form",
                                "fields": [
                                    { "name": "customerId", "type": "text", "required": True },
                                    { "name": "orderDate", "type": "date", "required": True },
                                    { "name": "totalAmount", "type": "number", "required": True }
                                ]
                            },
                            {
                                "name": "ProductSelection",
                                "type": "table",
                                "filters": [ "category", "priceRange" ],
                                "resultTable": {
                                    "columns": [ "productId", "name", "price", "stock" ],
                                    "actions": [ "select", "viewDetails" ]
                                }
                            }
                        ]
                    },
                    "OrderHistory": {
                        "sections": [
                            {
                                "name": "PastOrders",
                                "type": "table",
                                "filters": [ "dateRange", "status" ],
                                "resultTable": {
                                    "columns": [ "orderId", "orderDate", "totalAmount", "status" ],
                                    "actions": [ "viewDetails", "reorder" ]
                                }
                            }
                        ]
                    }
                }
            },
            
            "Suggested Structure": [
                {
                    "aggregate": {
                        "name": "Order",
                        "alias": "Customer Order"
                    },
                    "enumerations": [
                        {
                            "name": "OrderStatus",
                            "alias": "Order Status"
                        }
                    ],
                    "valueObjects": [
                        {
                            "name": "ShippingAddress",
                            "alias": "Shipping Address"
                        },
                        {
                            "name": "PaymentDetail",
                            "alias": "Payment Detail"
                        }
                    ]
                }
            ],
            
            "Aggregate to create": {
                "name": "Order",
                "alias": "Customer Order"
            }
        }

    def _build_json_example_output_format(self) -> Dict[str, Any]:
        return {
            "inference": "The Customer Order aggregate has been created successfully. OrderStatus enumeration defines the order states, while ShippingAddress and PaymentDetail value objects encapsulate address and payment information respectively.",
            "result": {
                "aggregateActions": [
                    {
                        "actionName": "CreateOrderAggregate",
                        "objectType": "Aggregate",
                        "ids": {
                            "aggregateId": "agg-order"
                        },
                        "args": {
                            "aggregateName": "Order",
                            "aggregateAlias": "Customer Order",
                            "properties": [
                                { "name": "orderId", "type": "Long", "isKey": True },
                                { "name": "customerId", "type": "Long" },
                                { "name": "orderDate", "type": "Date" },
                                { "name": "totalAmount", "type": "Integer" },
                                { "name": "shippingAddress", "type": "ShippingAddress" },
                                { "name": "paymentDetail", "type": "PaymentDetail" },
                                { "name": "status", "type": "OrderStatus" }
                            ]
                        }
                    }
                ],
                "valueObjectActions": [
                    {
                        "actionName": "CreateShippingAddressVO",
                        "objectType": "ValueObject",
                        "ids": {
                            "aggregateId": "agg-order",
                            "valueObjectId": "vo-shipping-address"
                        },
                        "args": {
                            "valueObjectName": "ShippingAddress",
                            "valueObjectAlias": "Shipping Address",
                            "properties": [
                                { "name": "street" },
                                { "name": "city" },
                                { "name": "state" },
                                { "name": "zipCode" }
                            ]
                        }
                    },
                    {
                        "actionName": "CreatePaymentDetailVO",
                        "objectType": "ValueObject",
                        "ids": {
                            "aggregateId": "agg-order",
                            "valueObjectId": "vo-payment-detail"
                        },
                        "args": {
                            "valueObjectName": "PaymentDetail",
                            "valueObjectAlias": "Payment Detail",
                            "properties": [
                                { "name": "cardNumber" },
                                { "name": "cardHolder" },
                                { "name": "expirationDate", "type": "Date" },
                                { "name": "securityCode" }
                            ]
                        }
                    }
                ],
                "enumerationActions": [
                    {
                        "actionName": "CreateOrderStatusEnum",
                        "objectType": "Enumeration",
                        "ids": {
                            "aggregateId": "agg-order",
                            "enumerationId": "enum-order-status"
                        },
                        "args": {
                            "enumerationName": "OrderStatus",
                            "enumerationAlias": "Order Status",
                            "properties": [
                                { "name": "PENDING" },
                                { "name": "CONFIRMED" },
                                { "name": "SHIPPED" },
                                { "name": "DELIVERED" },
                                { "name": "CANCELLED" }
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

            "Bounded Context to Generate Actions": inputs.get("targetBoundedContext").get("name"),

            "Functional Requirements": inputs.get("description"),

            "Suggested Structure": inputs.get("draftOption"),

            "Aggregate to create": inputs.get("targetAggregate"),

            "Final Check": f"""
1. Language and Naming:
   * Object names (classes, methods, properties): English only
   * Alias properties: {self.client.get("preferredLanguage")} only
   * Follow consistent naming patterns
   * Use domain-specific terminology
""",
        }