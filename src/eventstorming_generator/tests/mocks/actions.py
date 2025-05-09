from ...models import ActionModel

user_info = {"uid": "test_user"}
information = {"projectId": "test_project"}
        
actions = [
    ActionModel(
        objectType="BoundedContext",
        type="create",
        ids={
            "boundedContextId": "bc-bookManagement"
        },
        args={
            "boundedContextName": "BookManagement",
            "boundedContextAlias": "Book Management",
            "description": "Book Management Description"
        }
    ),

    ActionModel(
        objectType="Aggregate",
        type="create",
        ids={
            "boundedContextId": "bc-bookManagement",
            "aggregateId": "agg-book"
        },
        args={
            "aggregateName": "Book",
            "aggregateAlias": "Book",
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
            ]
        }
    )
]