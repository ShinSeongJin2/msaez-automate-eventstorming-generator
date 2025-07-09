from ...models import ActionModel

user_info = {"uid": "test_user"}
information = {"projectId": "test_project"}

bounded_context_id = '0faf38c9-6471-4a6e-b24a-d691ac7ab385'
aggregate_id = 'a932c245-ac83-4d8e-8fe3-eb787fe5943b'

actionsCollection = [
    [
        ActionModel(
            objectType='BoundedContext',
            type='create',
            ids={'boundedContextId': bounded_context_id},
            args={'boundedContextName': 'BookManagement', 'boundedContextAlias': '도서 관리'}
        ),

        ActionModel(
            objectType='Aggregate',
            type='create',
            ids={
                'boundedContextId': bounded_context_id,
                'aggregateId': aggregate_id
            },
            args={
                'aggregateName': 'Book',
                'aggregateAlias': '도서',
                'properties': [
                    {'name': 'bookId', 'type': 'Long', 'isKey': True, 'isForeignProperty': None},
                    {'name': 'title', 'type': None, 'isKey': None, 'isForeignProperty': None},
                    {'name': 'isbn', 'type': None, 'isKey': None, 'isForeignProperty': None},
                    {'name': 'author', 'type': None, 'isKey': None, 'isForeignProperty': None},
                    {'name': 'publisher', 'type': None, 'isKey': None, 'isForeignProperty': None},
                    {'name': 'category', 'type': 'BookCategory', 'isKey': None, 'isForeignProperty': None},
                    {'name': 'status', 'type': 'BookStatus', 'isKey': None, 'isForeignProperty': None},
                    {'name': 'registrationDate', 'type': 'Date', 'isKey': None, 'isForeignProperty': None},
                    {'name': 'disposalDate', 'type': 'Date', 'isKey': None, 'isForeignProperty': None},
                    {'name': 'disposalReason', 'type': 'String', 'isKey': None, 'isForeignProperty': None},
                    {'name': 'createdAt', 'type': 'Date', 'isKey': None, 'isForeignProperty': None},
                    {'name': 'updatedAt', 'type': 'Date', 'isKey': None, 'isForeignProperty': None},
                    {'name': 'statusHistory', 'type': 'List<BookStatusHistoryRecord>', 'isKey': None, 'isForeignProperty': None},
                ]
            },
            actionName='CreateBookAggregate'
        ),

        ActionModel(
            objectType='ValueObject',
            type='create',
            ids={
                'boundedContextId': bounded_context_id,
                'aggregateId': aggregate_id,
                'valueObjectId': '129018ed-d272-4a92-af35-52185f611b37'
            },
            args={
                'valueObjectName': 'BookStatusHistoryRecord',
                'valueObjectAlias': '도서 상태 이력',
                'properties': [
                    {'name': 'historyId', 'type': 'Long', 'isKey': True, 'isForeignProperty': None},
                    {'name': 'previousStatus', 'type': 'BookStatus', 'isKey': None, 'isForeignProperty': None},
                    {'name': 'newStatus', 'type': 'BookStatus', 'isKey': None, 'isForeignProperty': None},
                    {'name': 'changeReason', 'type': None, 'isKey': None, 'isForeignProperty': None},
                    {'name': 'changedBy', 'type': None, 'isKey': None, 'isForeignProperty': None},
                    {'name': 'changeDate', 'type': 'Date', 'isKey': None, 'isForeignProperty': None},
                ]
            },
            actionName='CreateBookStatusHistoryRecordVO'
        ),

        ActionModel(
            objectType='Enumeration',
            type='create',
            ids={
                'boundedContextId': bounded_context_id,
                'aggregateId': aggregate_id,
                'enumerationId': '14e13172-626a-4b56-8533-4ebcc8eab732'
            },
            args={
                'enumerationName': 'BookStatus',
                'enumerationAlias': '도서 상태',
                'properties': [
                    {'name': 'AVAILABLE'},
                    {'name': 'ON_LOAN'},
                    {'name': 'RESERVED'},
                    {'name': 'DISCARDED'},
                ]
            },
            actionName='CreateBookStatusEnum'
        ),
        
        ActionModel(
            objectType='Enumeration',
            type='create',
            ids={
                'boundedContextId': bounded_context_id,
                'aggregateId': aggregate_id,
                'enumerationId': 'a53763bc-5beb-4a39-b1af-518b4d2da65c'
            },
            args={
                'enumerationName': 'BookCategory',
                'enumerationAlias': '도서 카테고리',
                'properties': [
                    {'name': 'NOVEL'},
                    {'name': 'NONFICTION'},
                    {'name': 'ACADEMIC'},
                    {'name': 'MAGAZINE'},
                ]
            },
            actionName='CreateBookCategoryEnum'
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