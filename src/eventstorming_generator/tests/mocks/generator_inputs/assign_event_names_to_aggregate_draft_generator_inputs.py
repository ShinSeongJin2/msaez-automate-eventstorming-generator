assign_event_names_to_aggregate_draft_generator_inputs = {
    "boundedContextName": "OrderManagement",
    "aggregates": [
        {
            "id": "agg-order",
            "name": "Order",
            "displayName": "주문",
            "properties": [
                {"name": "orderId", "type": "Long", "isKey": True},
                {"name": "customerId", "type": "Long"},
                {"name": "status", "type": "OrderStatus"},
                {"name": "totalAmount", "type": "Double"},
                {"name": "orderDate", "type": "Date"}
            ]
        },
        {
            "id": "agg-customer",
            "name": "Customer", 
            "displayName": "고객",
            "properties": [
                {"name": "customerId", "type": "Long", "isKey": True},
                {"name": "name", "type": "String"},
                {"name": "email", "type": "String"},
                {"name": "phoneNumber", "type": "String"}
            ]
        },
        {
            "id": "agg-payment",
            "name": "Payment",
            "displayName": "결제",
            "properties": [
                {"name": "paymentId", "type": "Long", "isKey": True},
                {"name": "orderId", "type": "Long"},
                {"name": "amount", "type": "Double"},
                {"name": "paymentMethod", "type": "String"},
                {"name": "status", "type": "PaymentStatus"}
            ]
        },
        {
            "id": "agg-product",
            "name": "Product",
            "displayName": "상품",
            "properties": [
                {"name": "productId", "type": "Long", "isKey": True},
                {"name": "name", "type": "String"},
                {"name": "price", "type": "Double"},
                {"name": "stockQuantity", "type": "Integer"}
            ]
        }
    ],
    "eventNames": [
        "OrderCreated",
        "OrderStatusChanged", 
        "OrderCancelled",
        "OrderCompleted",
        "CustomerRegistered",
        "CustomerEmailUpdated",
        "CustomerPhoneUpdated",
        "PaymentProcessed",
        "PaymentFailed",
        "PaymentRefunded",
        "ProductCreated",
        "ProductPriceUpdated",
        "ProductStockUpdated",
        "ProductDiscontinued"
    ]
}