from .....models import *

merge_created_bounded_context_generator_util_inputs = {
    "boundedContextInfos": [
        BoundedContextInfoModel(
            name="OrderProcessing",
            alias="Order Processing",
            importance="Core Domain",
            description="This context manages order creation and initial processing. It handles order placement, order validation, order status tracking, and basic order information management."
        ),
        BoundedContextInfoModel(
            name="OrderManagement",
            alias="Order Management",
            importance="Core Domain",
            description="This context is responsible for managing customer orders throughout their lifecycle. It handles order modifications, cancellations, order history, and coordination between order-related processes."
        ),
        BoundedContextInfoModel(
            name="InventoryControl",
            alias="Inventory Control",
            importance="Supporting Domain",
            description="This context manages product stock levels. It handles inventory tracking, stock updates when orders are placed, and low-stock alerts."
        ),
        BoundedContextInfoModel(
            name="StockManagement",
            alias="Stock Management",
            importance="Supporting Domain",
            description="This context handles warehouse inventory operations. It manages stock replenishment, inventory adjustments, and product availability checks."
        ),
        BoundedContextInfoModel(
            name="PaymentGateway",
            alias="Payment Gateway",
            importance="Generic Domain",
            description="This context processes payment transactions. It supports credit cards, digital wallets, and handles payment authorization and capture."
        ),
        BoundedContextInfoModel(
            name="PaymentProcessing",
            alias="Payment Processing",
            importance="Generic Domain",
            description="This context manages payment operations for customer purchases. It handles payment method validation, transaction processing, refund processing, and payment history tracking."
        ),
        BoundedContextInfoModel(
            name="ShippingService",
            alias="Shipping Service",
            importance="Supporting Domain",
            description="This context manages product delivery. It handles shipping carrier integration, shipment tracking, and delivery status updates."
        ),
        BoundedContextInfoModel(
            name="DeliveryManagement",
            alias="Delivery Management",
            importance="Supporting Domain",
            description="This context coordinates the delivery process. It manages shipping address validation, delivery scheduling, and shipment notifications to customers."
        ),
        BoundedContextInfoModel(
            name="CustomerAccount",
            alias="Customer Account",
            importance="Generic Domain",
            description="This context manages customer account information. It handles customer registration, profile updates, and saved preferences."
        ),
        BoundedContextInfoModel(
            name="UserProfile",
            alias="User Profile",
            importance="Generic Domain",
            description="This context handles user authentication and profile management. It manages login credentials, password resets, and personal information management."
        ),
        BoundedContextInfoModel(
            name="ProductCatalog",
            alias="Product Catalog",
            importance="Core Domain",
            description="This context manages the product catalog. It handles product creation, categorization, pricing, descriptions, images, product search, and filtering capabilities."
        ),
        BoundedContextInfoModel(
            name="NotificationEngine",
            alias="Notification Engine",
            importance="Supporting Domain",
            description="This context sends notifications to customers. It handles email notifications for order confirmations and shipping updates."
        ),
        BoundedContextInfoModel(
            name="AlertSystem",
            alias="Alert System",
            importance="Supporting Domain",
            description="This context manages customer communications. It sends SMS alerts, push notifications, and promotional messages to customers."
        )
    ]
}