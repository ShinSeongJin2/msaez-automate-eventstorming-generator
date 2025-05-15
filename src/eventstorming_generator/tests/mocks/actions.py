from ...models import ActionModel

user_info = {"uid": "test_user"}
information = {"projectId": "test_project"}

actionsCollection = [
    [
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
        ),

        ActionModel(
            objectType="Event",
            type="create",
            ids={
                "boundedContextId": "bc-bookManagement",
                "aggregateId": "agg-book",
                "eventId": "evt-bookLoaned"
            },
            args={
                "eventName": "BookLoaned",
                "eventAlias": "Book Loaned",

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
        ),

        ActionModel(
            objectType="ReadModel",
            type="create",
            ids={
                "boundedContextId": "bc-bookManagement",
                "aggregateId": "agg-book",
                "readModelId": "rm-bookLoaned"
            },
            args={
                "readModelName": "BookLoaned",
                "readModelAlias": "Book Loaned",
                "isMultipleResult": False,

                "queryParameters": [
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
                
                "actor": "User"
            }
        ),


        ActionModel(
            objectType="BoundedContext",
            type="create",
            ids={
                "boundedContextId": "bc-userManagement"
            },
            args={
                "boundedContextName": "UserManagement",
                "boundedContextAlias": "User Management",
                "description": "User Management Description"
            }
        ),

        ActionModel(
            objectType="Aggregate",
            type="create",
            ids={
                "boundedContextId": "bc-userManagement",
                "aggregateId": "agg-user"
            },
            args={
                "aggregateName": "User",
                "aggregateAlias": "User",
                "properties": [
                    {
                        "name": "userId",
                        "type": "String",
                        "isKey": True
                    },
                    {
                        "name": "userName",
                        "type": "String"
                    }
                ]
            }
        ),

        ActionModel(
            objectType="Command",
            type="create",
            ids={
                "boundedContextId": "bc-userManagement",
                "aggregateId": "agg-user",
                "commandId": "cmd-registerUser"
            },
            args={
                "commandName": "RegisterUser",
                "commandAlias": "Register User",
                "api_verb": "POST",

                "properties": [
                    {
                        "name": "userId",
                        "type": "String",
                        "isKey": True
                    },
                    {
                        "name": "userName",
                        "type": "String"
                    }
                ],

                "outputEventIds": ["evt-userRegistered"],
                "actor": "User"
            }
        ),

        ActionModel(
        objectType="Event",
        type="create",
        ids={
            "boundedContextId": "bc-userManagement",
            "aggregateId": "agg-user",
            "eventId": "evt-userRegistered"
        },
        args={
            "eventName": "UserRegistered",
            "eventAlias": "User Registered",

            "properties": [
                {
                    "name": "userId",
                    "type": "String",
                    "isKey": True
                },
                {
                    "name": "userName",
                    "type": "String"
                }
            ]
        }
    )
    ],
    [
        ActionModel(
            objectType="Event",
            type="update",
            ids={
                "boundedContextId": "bc-bookManagement",
                "aggregateId": "agg-book",
                "eventId": "evt-bookLoaned"
            },
            args={
                "outputCommandIds": [{
                    "commandId": "cmd-registerUser",
                    "reason": "Mocked",
                    "name": "Register User",
                    "alias": "Register User"
                }]
            }
        )
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