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
                },
                {
                    "name": "bookAuthor",
                    "type": "BookAuthor"
                },
                {
                    "name": "bookStatus",
                    "type": "BookStatus"
                }
            ]
        }
    ),

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
    )
]