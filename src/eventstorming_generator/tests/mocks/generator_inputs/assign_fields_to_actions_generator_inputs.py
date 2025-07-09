assign_fields_to_actions_generator_inputs = {
    "description": "A user has an address.",
    "existingActions": [
        {"objectType": "Aggregate", "ids": {"aggregateId": "agg-user"}, "args": {"aggregateName": "User", "properties": []}},
        {"objectType": "ValueObject", "ids": {"aggregateId": "agg-user", "valueObjectId": "vo-address"}, "args": {"valueObjectName": "Address", "properties": []}}
    ],
    "missingFields": ["last_login_at", "postal_code"]
}