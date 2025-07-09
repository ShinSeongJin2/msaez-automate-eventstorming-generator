assign_ddl_fields_to_aggregate_draft_generator_inputs = {
    "description": """
# Bounded Context Overview: OrderManagement

## Role
This context is responsible for the entire lifecycle of an order, including its creation, management, and fulfillment. It handles order items, customer information, payment processing, and shipping management. It also manages inventory allocation and stock updates.

## User Story
As a customer, I want to place orders for products on the e-commerce platform. When creating an order, I need to provide shipping information and payment details. The system should track order status from creation to delivery, manage inventory, and handle payment processing.

## Key Events
- OrderCreated
- OrderConfirmed
- PaymentProcessed
- OrderShipped
- OrderDelivered
- OrderCancelled
- InventoryAllocated
- InventoryReleased

## Business Rules
- Orders must have at least one order item
- Payment must be processed before shipping
- Inventory is allocated when order is confirmed
- Order status progresses: Draft -> Confirmed -> Shipped -> Delivered
""",
    "aggregateDrafts": [
        {
            "name": "Order",
            "alias": "Customer Order"
        },
        {
            "name": "OrderItem",
            "alias": "Order Line Item"
        },
        {
            "name": "Payment",
            "alias": "Order Payment"
        },
        {
            "name": "Shipment",
            "alias": "Order Shipment"
        }
    ],
    "allDdlFields": [
        "order_id",
        "customer_id",
        "order_date",
        "order_status",
        "total_amount",
        "currency",
        "shipping_address",
        "billing_address",
        "order_notes",
        "created_at",
        "updated_at",
        "order_item_id",
        "product_id",
        "quantity",
        "unit_price",
        "item_total",
        "product_name",
        "product_sku",
        "payment_id",
        "payment_method",
        "payment_status",
        "payment_amount",
        "payment_date",
        "transaction_id",
        "payment_gateway",
        "shipment_id",
        "tracking_number",
        "shipping_carrier",
        "shipping_method",
        "shipped_date",
        "estimated_delivery_date",
        "actual_delivery_date",
        "shipment_status"
    ]
}