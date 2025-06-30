from ...models import ActionModel

user_info = {"uid": "test_user"}
information = {"projectId": "test_project"}

actionsCollection = [
    [
        # 1. Bounded Context: OrderManagement
        ActionModel(
            objectType="BoundedContext",
            type="create",
            ids={"boundedContextId": "bc-orderManagement"},
            args={
                "boundedContextName": "OrderManagement",
                "boundedContextAlias": "Order Management",
                "description": "Handles all logic related to customer orders.",
            },
        ),
        # 2. Aggregate: Order
        ActionModel(
            objectType="Aggregate",
            type="create",
            ids={"boundedContextId": "bc-orderManagement", "aggregateId": "agg-order"},
            args={
                "aggregateName": "Order",
                "aggregateAlias": "Order",
                "properties": [
                    {"name": "orderId", "type": "String", "isKey": True},
                    {"name": "productId", "type": "ProductId"},
                    {"name": "orderStatus", "type": "OrderStatus"},
                ],
            },
        ),
        # 3. Value Object: ProductId
        ActionModel(
            objectType="ValueObject",
            type="create",
            ids={
                "boundedContextId": "bc-orderManagement",
                "aggregateId": "agg-order",
                "valueObjectId": "vo-productId",
            },
            args={
                "valueObjectName": "ProductId",
                "properties": [{"name": "id", "type": "String", "isKey": True}],
            },
        ),
        # 4. Enumeration: OrderStatus
        ActionModel(
            objectType="Enumeration",
            type="create",
            ids={
                "boundedContextId": "bc-orderManagement",
                "aggregateId": "agg-order",
                "enumerationId": "enum-orderStatus",
            },
            args={
                "enumerationName": "OrderStatus",
                "properties": [
                    {"name": "PLACED"},
                    {"name": "SHIPPED"},
                    {"name": "DELIVERED"},
                ],
            },
        ),
        # 5. Command: PlaceOrder -> triggers OrderPlaced event
        ActionModel(
            objectType="Command",
            type="create",
            ids={
                "boundedContextId": "bc-orderManagement",
                "aggregateId": "agg-order",
                "commandId": "cmd-placeOrder",
            },
            args={
                "commandName": "PlaceOrder",
                "commandAlias": "Place Order",
                "api_verb": "POST",
                "properties": [
                    {"name": "productId", "type": "ProductId"},
                    {"name": "userId", "type": "String"},
                ],
                "outputEventIds": ["evt-orderPlaced"],
                "actor": "Customer",
            },
        ),
        # 6. Event: OrderPlaced
        ActionModel(
            objectType="Event",
            type="create",
            ids={
                "boundedContextId": "bc-orderManagement",
                "aggregateId": "agg-order",
                "eventId": "evt-orderPlaced",
            },
            args={
                "eventName": "OrderPlaced",
                "eventAlias": "Order Placed",
                "properties": [
                    {"name": "orderId", "type": "String", "isKey": True},
                    {"name": "productId", "type": "ProductId"},
                    {"name": "userId", "type": "String"},
                ],
            },
        ),
        # 7. Bounded Context: NotificationManagement
        ActionModel(
            objectType="BoundedContext",
            type="create",
            ids={"boundedContextId": "bc-notificationManagement"},
            args={
                "boundedContextName": "NotificationManagement",
                "boundedContextAlias": "Notification Management",
                "description": "Handles user notifications.",
            },
        ),
        # 8. Aggregate: Notification
        ActionModel(
            objectType="Aggregate",
            type="create",
            ids={
                "boundedContextId": "bc-notificationManagement",
                "aggregateId": "agg-notification",
            },
            args={
                "aggregateName": "Notification",
                "aggregateAlias": "Notification",
                "properties": [
                    {"name": "notificationId", "type": "String", "isKey": True},
                    {"name": "userId", "type": "String"},
                    {"name": "message", "type": "String"},
                ],
            },
        ),
        # 9. Policy: Listens for OrderPlaced, triggers NotificationDispatchRequested
        ActionModel(
            objectType="Policy",
            type="create",
            ids={
                "policyId": "pol-notifyOnOrderPlacement",
            },
            args={
                "policyName": "NotifyOnOrderPlacement",
                "policyAlias": "Notify on Order Placement",
                "inputEventIds": ["evt-orderPlaced"],
                "outputEventIds": ["evt-notificationDispatchRequested"],
                "reason": "Automatically notify users when an order is placed."
            },
        ),
        # 10. Event: NotificationDispatchRequested
        ActionModel(
            objectType="Event",
            type="create",
            ids={
                "boundedContextId": "bc-notificationManagement",
                "aggregateId": "agg-notification",
                "eventId": "evt-notificationDispatchRequested",
            },
            args={
                "eventName": "NotificationDispatchRequested",
                "eventAlias": "Notification Dispatch Requested",
                "properties": [
                    {"name": "orderId", "type": "String"},
                    {"name": "userId", "type": "String"},
                ],
            },
        )
    ],
    [
        # 11. ReadModel: Notify
        ActionModel(
            objectType="ReadModel",
            type="create",
            ids={
                "boundedContextId": "bc-notificationManagement",
                "aggregateId": "agg-notification",
                "readModelId": "rm-notify",
            },
            args={
                "readModelName": "Notify",
                "readModelAlias": "Notify",
                "isMultipleResult": False,
                "queryParameters": [
                    {"name": "orderId", "type": "String"},
                    {"name": "userId", "type": "String"},
                ],
                "actor": "User"
            },
        ),
        # 12. Command: Notify -> triggers NotificationSent event
        ActionModel(
            objectType="Command",
            type="create",
            ids={
                "boundedContextId": "bc-notificationManagement",
                "aggregateId": "agg-notification",
                "commandId": "cmd-notify",
            },
            args={
                "commandName": "Notify",
                "commandAlias": "Notify",
                "api_verb": "POST",
                "properties": [
                    {"name": "notificationId", "type": "String", "isKey": True},
                    {"name": "orderId", "type": "String"},
                    {"name": "userId", "type": "String"},
                ],
                "outputEventIds": ["evt-notificationSent"],
                "actor": "User",
            },
        ),
        # 13. Event: NotificationSent
        ActionModel(
            objectType="Event",
            type="create",
            ids={
                "boundedContextId": "bc-notificationManagement",
                "aggregateId": "agg-notification",
                "eventId": "evt-notificationSent",
            },
            args={
                "eventName": "NotificationSent",
                "eventAlias": "Notification Sent",
                "properties": [
                    {"name": "notificationId", "type": "String", "isKey": True},
                    {"name": "userId", "type": "String"},
                ],
            },
        ),
    ]
]

actions_for_fake_test = [
    ActionModel(
        objectType="ValueObject",
        type="create",
        ids={
            "boundedContextId": "bc-bookManagement",
            "aggregateId": "agg-book",
            "valueObjectId": "vo-bookAuthor"
        },
        args={
            "valueObjectName": "BookAuthor",
            "properties": [
                {
                    "name": "bookAuthorId",
                    "type": "String",
                    "isKey": True
                },
                {
                    "name": "bookAuthorName",
                    "type": "String"
                }
            ]
        }
    ),

    ActionModel(
        objectType="Enumeration",
        type="create",
        ids={
            "boundedContextId": "bc-bookManagement",
            "aggregateId": "agg-book",
            "enumerationId": "enum-bookStatus"
        },
        args={
            "enumerationName": "BookStatus",
            "properties": [
                {
                    "name": "RENTED"
                },
                {
                    "name": "RETURNED"
                }
            ]
        }
    ),

    ActionModel(
        objectType="Command",
        type="create",
        ids={
            "boundedContextId": "bc-bookManagement",
            "aggregateId": "agg-book",
            "commandId": "cmd-loanBook"
        },
        args={
            "commandName": "LoanBook",
            "commandAlias": "Loan Book",
            "api_verb": "POST",

            "properties": [
                {
                    "name": "bookId",
                    "type": "String",
                    "isKey": True
                },
                {
                    "name": "bookTitle",
                    "type": "String"
                }
            ],

            "outputEventIds": ["evt-bookLoaned"],
            "actor": "User"
        }
    )
]