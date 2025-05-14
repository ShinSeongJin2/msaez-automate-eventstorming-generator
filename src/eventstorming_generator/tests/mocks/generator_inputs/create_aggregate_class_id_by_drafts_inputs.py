create_aggregate_class_id_by_drafts_inputs = {
    "draftOption": {
        "BookManagement": [
            {
                "aggregate": {
                    "name": "Book",
                    "alias": "도서"
                },
                "enumerations": [
                    {
                        "name": "Category",
                        "alias": "카테고리"
                    },
                    {
                        "name": "Status",
                        "alias": "도서상태"
                    }
                ],
                "valueObjects": []
            }
        ],
        "LoanManagement": [
            {
                "aggregate": {
                    "name": "LoanTransaction",
                    "alias": "대출/반납 거래"
                },
                "enumerations": [
                    {
                        "name": "TransactionType",
                        "alias": "거래 유형"
                    }
                ],
                "valueObjects": [
                    {
                        "name": "BookReference",
                        "alias": "도서 참조",
                        "referencedAggregate": {
                            "name": "Book",
                            "alias": "도서"
                        }
                    }
                ]
            }
        ]
    },
    "esValue": {
        "elements": {
            "9534a201-5709-2279-022f-47b7a1848b1f": {
                "_type": "org.uengine.modeling.model.BoundedContext",
                "aggregates": [
                    {
                        "id": "ff155dca-57e7-325f-720d-51a66c606f5e"
                    }
                ],
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "description": "[{\"type\":\"userStory\",\"text\":\"도서 관리 화면에서는 새로운 도서를 등록하고 현재 보유한 도서들의 상태를 관리할 수 있어야 해. 도서 등록 시에는 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받아야 해. ISBN은 13자리 숫자여야 하고 중복 확인이 필요해. 카테고리는 소설/비소설/학술/잡지 중에서 선택할 수 있어야 해. 등록된 도서는 처음에 '대출가능' 상태가 되고, 이후 대출/반납 상황에 따라 '대출중', '예약중' 상태로 자동으로 변경되어야 해. 도서가 훼손되거나 분실된 경우 '폐기' 처리가 가능해야 해며, 폐기된 도서는 더 이상 대출이 불가능해야 해.\"}]",
                "id": "9534a201-5709-2279-022f-47b7a1848b1f",
                "elementView": {
                    "_type": "org.uengine.modeling.model.BoundedContext",
                    "height": 590,
                    "id": "9534a201-5709-2279-022f-47b7a1848b1f",
                    "style": "{}",
                    "width": 560,
                    "x": 650,
                    "y": 450
                },
                "gitURL": None,
                "hexagonalView": {
                    "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
                    "height": 350,
                    "id": "9534a201-5709-2279-022f-47b7a1848b1f",
                    "style": "{}",
                    "width": 350,
                    "x": 235,
                    "y": 365
                },
                "members": [],
                "name": "BookManagement",
                "displayName": "도서 관리",
                "oldName": "",
                "policies": [],
                "portGenerated": None,
                "preferredPlatform": "template-spring-boot",
                "preferredPlatformConf": {},
                "rotateStatus": False,
                "tempId": "",
                "templatePerElements": {},
                "views": [],
                "definitionId": "163972132_es_9b15cefec6c1e88801f66e18231de4a6"
            },
            "5782787e-3129-dfa6-0228-99246a0507a5": {
                "_type": "org.uengine.modeling.model.BoundedContext",
                "aggregates": [
                    {
                        "id": "ab09c1d7-158c-1569-bde8-76c87397353f"
                    }
                ],
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "description": "[{\"type\":\"userStory\",\"text\":\"대출/반납 화면에서는 회원이 도서를 대출하고 반납하는 것을 관리할 수 있어야 해. 대출 신청 시에는 회원번호와 이름으로 회원을 확인하고, 대출할 도서를 선택해야 해. 도서는 도서명이나 ISBN으로 검색할 수 있어야 해. 대출 기간은 7일/14일/30일 중에서 선택할 수 있어. 만약 대출하려는 도서가 이미 대출 중이라면, 예약 신청이 가능해야 해. 대출이 완료되면 해당 도서의 상태는 자동으로 '대출중'으로 변경되어야 해.\"}]",
                "id": "5782787e-3129-dfa6-0228-99246a0507a5",
                "elementView": {
                    "_type": "org.uengine.modeling.model.BoundedContext",
                    "height": 590,
                    "id": "5782787e-3129-dfa6-0228-99246a0507a5",
                    "style": "{}",
                    "width": 560,
                    "x": 1235,
                    "y": 450
                },
                "gitURL": None,
                "hexagonalView": {
                    "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
                    "height": 350,
                    "id": "5782787e-3129-dfa6-0228-99246a0507a5",
                    "style": "{}",
                    "width": 350,
                    "x": 235,
                    "y": 365
                },
                "members": [],
                "name": "LoanManagement",
                "displayName": "대출/반납 관리",
                "oldName": "",
                "policies": [],
                "portGenerated": 8080,
                "preferredPlatform": "template-spring-boot",
                "preferredPlatformConf": {},
                "rotateStatus": False,
                "tempId": "",
                "templatePerElements": {},
                "views": [],
                "definitionId": "163972132_es_9b15cefec6c1e88801f66e18231de4a6"
            },
            "ff155dca-57e7-325f-720d-51a66c606f5e": {
                "aggregateRoot": {
                    "_type": "org.uengine.modeling.model.AggregateRoot",
                    "fieldDescriptors": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "ISBN",
                            "nameCamelCase": "isbn",
                            "namePascalCase": "Isbn",
                            "displayName": "",
                            "referenceClass": None,
                            "isOverrideField": False,
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": False,
                            "name": "bookTitle",
                            "nameCamelCase": "bookTitle",
                            "namePascalCase": "BookTitle",
                            "displayName": "",
                            "referenceClass": None,
                            "isOverrideField": False,
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": False,
                            "name": "author",
                            "nameCamelCase": "author",
                            "namePascalCase": "Author",
                            "displayName": "",
                            "referenceClass": None,
                            "isOverrideField": False,
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": False,
                            "name": "publisher",
                            "nameCamelCase": "publisher",
                            "namePascalCase": "Publisher",
                            "displayName": "",
                            "referenceClass": None,
                            "isOverrideField": False,
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Category",
                            "isCopy": False,
                            "isKey": False,
                            "name": "category",
                            "nameCamelCase": "category",
                            "namePascalCase": "Category",
                            "displayName": "",
                            "referenceClass": None,
                            "isOverrideField": False,
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Status",
                            "isCopy": False,
                            "isKey": False,
                            "name": "status",
                            "nameCamelCase": "status",
                            "namePascalCase": "Status",
                            "displayName": "",
                            "referenceClass": None,
                            "isOverrideField": False,
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "entities": {
                        "elements": {
                            "db402125-8037-a260-d3f4-8393dd469d87": {
                                "_type": "org.uengine.uml.model.Class",
                                "id": "db402125-8037-a260-d3f4-8393dd469d87",
                                "name": "Book",
                                "namePascalCase": "Book",
                                "nameCamelCase": "book",
                                "namePlural": "Books",
                                "fieldDescriptors": [
                                    {
                                        "className": "String",
                                        "isCopy": False,
                                        "isKey": True,
                                        "name": "ISBN",
                                        "displayName": "",
                                        "nameCamelCase": "isbn",
                                        "namePascalCase": "Isbn",
                                        "_type": "org.uengine.model.FieldDescriptor",
                                        "inputUI": None,
                                        "options": None
                                    },
                                    {
                                        "className": "String",
                                        "isCopy": False,
                                        "isKey": False,
                                        "name": "bookTitle",
                                        "displayName": "",
                                        "nameCamelCase": "bookTitle",
                                        "namePascalCase": "BookTitle",
                                        "_type": "org.uengine.model.FieldDescriptor",
                                        "inputUI": None,
                                        "options": None
                                    },
                                    {
                                        "className": "String",
                                        "isCopy": False,
                                        "isKey": False,
                                        "name": "author",
                                        "displayName": "",
                                        "nameCamelCase": "author",
                                        "namePascalCase": "Author",
                                        "_type": "org.uengine.model.FieldDescriptor",
                                        "inputUI": None,
                                        "options": None
                                    },
                                    {
                                        "className": "String",
                                        "isCopy": False,
                                        "isKey": False,
                                        "name": "publisher",
                                        "displayName": "",
                                        "nameCamelCase": "publisher",
                                        "namePascalCase": "Publisher",
                                        "_type": "org.uengine.model.FieldDescriptor",
                                        "inputUI": None,
                                        "options": None
                                    },
                                    {
                                        "className": "Category",
                                        "isCopy": False,
                                        "isKey": False,
                                        "name": "category",
                                        "displayName": "",
                                        "nameCamelCase": "category",
                                        "namePascalCase": "Category",
                                        "_type": "org.uengine.model.FieldDescriptor",
                                        "inputUI": None,
                                        "options": None
                                    },
                                    {
                                        "className": "Status",
                                        "isCopy": False,
                                        "isKey": False,
                                        "name": "status",
                                        "displayName": "",
                                        "nameCamelCase": "status",
                                        "namePascalCase": "Status",
                                        "_type": "org.uengine.model.FieldDescriptor",
                                        "inputUI": None,
                                        "options": None
                                    }
                                ],
                                "operations": [],
                                "elementView": {
                                    "_type": "org.uengine.uml.model.Class",
                                    "id": "db402125-8037-a260-d3f4-8393dd469d87",
                                    "x": 200,
                                    "y": 200,
                                    "width": 200,
                                    "height": 100,
                                    "style": "{}",
                                    "titleH": 50,
                                    "subEdgeH": 120,
                                    "fieldH": 90,
                                    "methodH": 30
                                },
                                "selected": False,
                                "relations": [],
                                "parentOperations": [],
                                "relationType": None,
                                "isVO": False,
                                "isAbstract": False,
                                "isInterface": False,
                                "isAggregateRoot": True,
                                "parentId": "ff155dca-57e7-325f-720d-51a66c606f5e"
                            },
                            "4c295aed-6977-7d81-e1f7-b7d341a9f484": {
                                "_type": "org.uengine.uml.model.enum",
                                "id": "4c295aed-6977-7d81-e1f7-b7d341a9f484",
                                "name": "Category",
                                "displayName": "카테고리",
                                "nameCamelCase": "category",
                                "namePascalCase": "Category",
                                "namePlural": "categories",
                                "elementView": {
                                    "_type": "org.uengine.uml.model.enum",
                                    "id": "4c295aed-6977-7d81-e1f7-b7d341a9f484",
                                    "x": 700,
                                    "y": 456,
                                    "width": 200,
                                    "height": 100,
                                    "style": "{}",
                                    "titleH": 50,
                                    "subEdgeH": 50
                                },
                                "selected": False,
                                "items": [
                                    {
                                        "value": "NOVEL"
                                    },
                                    {
                                        "value": "NONFICTION"
                                    },
                                    {
                                        "value": "ACADEMIC"
                                    },
                                    {
                                        "value": "MAGAZINE"
                                    }
                                ],
                                "useKeyValue": False,
                                "relations": []
                            },
                            "127283ec-5a2a-a5f7-bcb8-2e93b8acc656": {
                                "_type": "org.uengine.uml.model.enum",
                                "id": "127283ec-5a2a-a5f7-bcb8-2e93b8acc656",
                                "name": "Status",
                                "displayName": "도서상태",
                                "nameCamelCase": "status",
                                "namePascalCase": "Status",
                                "namePlural": "statuses",
                                "elementView": {
                                    "_type": "org.uengine.uml.model.enum",
                                    "id": "127283ec-5a2a-a5f7-bcb8-2e93b8acc656",
                                    "x": 950,
                                    "y": 456,
                                    "width": 200,
                                    "height": 100,
                                    "style": "{}",
                                    "titleH": 50,
                                    "subEdgeH": 50
                                },
                                "selected": False,
                                "items": [
                                    {
                                        "value": "AVAILABLE"
                                    },
                                    {
                                        "value": "BORROWED"
                                    },
                                    {
                                        "value": "RESERVED"
                                    },
                                    {
                                        "value": "DISCARDED"
                                    }
                                ],
                                "useKeyValue": False,
                                "relations": []
                            }
                        },
                        "relations": {}
                    },
                    "operations": []
                },
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "boundedContext": {
                    "name": "9534a201-5709-2279-022f-47b7a1848b1f",
                    "id": "9534a201-5709-2279-022f-47b7a1848b1f"
                },
                "commands": [],
                "description": None,
                "id": "ff155dca-57e7-325f-720d-51a66c606f5e",
                "elementView": {
                    "_type": "org.uengine.modeling.model.Aggregate",
                    "id": "ff155dca-57e7-325f-720d-51a66c606f5e",
                    "x": 650,
                    "y": 450,
                    "width": 130,
                    "height": 400
                },
                "events": [],
                "hexagonalView": {
                    "_type": "org.uengine.modeling.model.AggregateHexagonal",
                    "id": "ff155dca-57e7-325f-720d-51a66c606f5e",
                    "x": 0,
                    "y": 0,
                    "subWidth": 0,
                    "width": 0
                },
                "name": "Book",
                "displayName": "도서",
                "nameCamelCase": "book",
                "namePascalCase": "Book",
                "namePlural": "books",
                "rotateStatus": False,
                "selected": False,
                "_type": "org.uengine.modeling.model.Aggregate"
            },
            "ab09c1d7-158c-1569-bde8-76c87397353f": {
                "aggregateRoot": {
                    "_type": "org.uengine.modeling.model.AggregateRoot",
                    "fieldDescriptors": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "loanId",
                            "nameCamelCase": "loanId",
                            "namePascalCase": "LoanId",
                            "displayName": "",
                            "referenceClass": None,
                            "isOverrideField": False,
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": False,
                            "name": "memberNumber",
                            "nameCamelCase": "memberNumber",
                            "namePascalCase": "MemberNumber",
                            "displayName": "",
                            "referenceClass": None,
                            "isOverrideField": False,
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": False,
                            "name": "bookISBN",
                            "nameCamelCase": "bookIsbn",
                            "namePascalCase": "BookIsbn",
                            "displayName": "",
                            "referenceClass": None,
                            "isOverrideField": False,
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Integer",
                            "isCopy": False,
                            "isKey": False,
                            "name": "loanPeriod",
                            "nameCamelCase": "loanPeriod",
                            "namePascalCase": "LoanPeriod",
                            "displayName": "",
                            "referenceClass": None,
                            "isOverrideField": False,
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Date",
                            "isCopy": False,
                            "isKey": False,
                            "name": "loanDate",
                            "nameCamelCase": "loanDate",
                            "namePascalCase": "LoanDate",
                            "displayName": "",
                            "referenceClass": None,
                            "isOverrideField": False,
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "TransactionType",
                            "isCopy": False,
                            "isKey": False,
                            "name": "transactionType",
                            "nameCamelCase": "transactionType",
                            "namePascalCase": "TransactionType",
                            "displayName": "",
                            "referenceClass": None,
                            "isOverrideField": False,
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "entities": {
                        "elements": {
                            "ad85c5be-8f77-b11c-84dc-c2222ae32be2": {
                                "_type": "org.uengine.uml.model.Class",
                                "id": "ad85c5be-8f77-b11c-84dc-c2222ae32be2",
                                "name": "LoanTransaction",
                                "namePascalCase": "LoanTransaction",
                                "nameCamelCase": "loanTransaction",
                                "namePlural": "LoanTransactions",
                                "fieldDescriptors": [
                                    {
                                        "className": "String",
                                        "isCopy": False,
                                        "isKey": True,
                                        "name": "loanId",
                                        "displayName": "",
                                        "nameCamelCase": "loanId",
                                        "namePascalCase": "LoanId",
                                        "_type": "org.uengine.model.FieldDescriptor",
                                        "inputUI": None,
                                        "options": None
                                    },
                                    {
                                        "className": "String",
                                        "isCopy": False,
                                        "isKey": False,
                                        "name": "memberNumber",
                                        "displayName": "",
                                        "nameCamelCase": "memberNumber",
                                        "namePascalCase": "MemberNumber",
                                        "_type": "org.uengine.model.FieldDescriptor",
                                        "inputUI": None,
                                        "options": None
                                    },
                                    {
                                        "className": "String",
                                        "isCopy": False,
                                        "isKey": False,
                                        "name": "bookISBN",
                                        "displayName": "",
                                        "nameCamelCase": "bookIsbn",
                                        "namePascalCase": "BookIsbn",
                                        "_type": "org.uengine.model.FieldDescriptor",
                                        "inputUI": None,
                                        "options": None
                                    },
                                    {
                                        "className": "Integer",
                                        "isCopy": False,
                                        "isKey": False,
                                        "name": "loanPeriod",
                                        "displayName": "",
                                        "nameCamelCase": "loanPeriod",
                                        "namePascalCase": "LoanPeriod",
                                        "_type": "org.uengine.model.FieldDescriptor",
                                        "inputUI": None,
                                        "options": None
                                    },
                                    {
                                        "className": "Date",
                                        "isCopy": False,
                                        "isKey": False,
                                        "name": "loanDate",
                                        "displayName": "",
                                        "nameCamelCase": "loanDate",
                                        "namePascalCase": "LoanDate",
                                        "_type": "org.uengine.model.FieldDescriptor",
                                        "inputUI": None,
                                        "options": None
                                    },
                                    {
                                        "className": "TransactionType",
                                        "isCopy": False,
                                        "isKey": False,
                                        "name": "transactionType",
                                        "displayName": "",
                                        "nameCamelCase": "transactionType",
                                        "namePascalCase": "TransactionType",
                                        "_type": "org.uengine.model.FieldDescriptor",
                                        "inputUI": None,
                                        "options": None
                                    }
                                ],
                                "operations": [],
                                "elementView": {
                                    "_type": "org.uengine.uml.model.Class",
                                    "id": "ad85c5be-8f77-b11c-84dc-c2222ae32be2",
                                    "x": 200,
                                    "y": 200,
                                    "width": 200,
                                    "height": 100,
                                    "style": "{}",
                                    "titleH": 50,
                                    "subEdgeH": 120,
                                    "fieldH": 90,
                                    "methodH": 30
                                },
                                "selected": False,
                                "relations": [],
                                "parentOperations": [],
                                "relationType": None,
                                "isVO": False,
                                "isAbstract": False,
                                "isInterface": False,
                                "isAggregateRoot": True,
                                "parentId": "ab09c1d7-158c-1569-bde8-76c87397353f"
                            },
                            "01b163f3-9fe5-0274-4cde-e6f47a48de5b": {
                                "_type": "org.uengine.uml.model.enum",
                                "id": "01b163f3-9fe5-0274-4cde-e6f47a48de5b",
                                "name": "TransactionType",
                                "displayName": "거래 유형",
                                "nameCamelCase": "transactionType",
                                "namePascalCase": "TransactionType",
                                "namePlural": "transactionTypes",
                                "elementView": {
                                    "_type": "org.uengine.uml.model.enum",
                                    "id": "01b163f3-9fe5-0274-4cde-e6f47a48de5b",
                                    "x": 700,
                                    "y": 456,
                                    "width": 200,
                                    "height": 100,
                                    "style": "{}",
                                    "titleH": 50,
                                    "subEdgeH": 50
                                },
                                "selected": False,
                                "items": [
                                    {
                                        "value": "LOAN"
                                    },
                                    {
                                        "value": "RETURN"
                                    },
                                    {
                                        "value": "RESERVATION"
                                    }
                                ],
                                "useKeyValue": False,
                                "relations": []
                            }
                        },
                        "relations": {}
                    },
                    "operations": []
                },
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "boundedContext": {
                    "name": "5782787e-3129-dfa6-0228-99246a0507a5",
                    "id": "5782787e-3129-dfa6-0228-99246a0507a5"
                },
                "commands": [],
                "description": None,
                "id": "ab09c1d7-158c-1569-bde8-76c87397353f",
                "elementView": {
                    "_type": "org.uengine.modeling.model.Aggregate",
                    "id": "ab09c1d7-158c-1569-bde8-76c87397353f",
                    "x": 1235,
                    "y": 450,
                    "width": 130,
                    "height": 400
                },
                "events": [],
                "hexagonalView": {
                    "_type": "org.uengine.modeling.model.AggregateHexagonal",
                    "id": "ab09c1d7-158c-1569-bde8-76c87397353f",
                    "x": 0,
                    "y": 0,
                    "subWidth": 0,
                    "width": 0
                },
                "name": "LoanTransaction",
                "displayName": "대출/반납 거래",
                "nameCamelCase": "loanTransaction",
                "namePascalCase": "LoanTransaction",
                "namePlural": "loanTransactions",
                "rotateStatus": False,
                "selected": False,
                "_type": "org.uengine.modeling.model.Aggregate"
            }
        },
        "relations": {},
        "basePlatform": None,
        "basePlatformConf": {},
        "toppingPlatforms": [],
        "toppingPlatformsConf": {},
        "scm": {
            "tag": None,
            "org": None,
            "repo": None,
            "forkedOrg": None,
            "forkedRepo": None
        },
        "version": 3,
        "k8sValue": {
            "elements": {},
            "relations": {}
        }
    },
    "userInfo": {
        "name": "shinseongjin@uengine.org",
        "uid": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
    },
    "information": {
        "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
        "authorEmail": "shinseongjin@uengine.org",
        "projectId": "163972132_es_05d136ce0010c9a1f5e2fde77b3fa549",
    },
    "targetReferences": [
        "BookReference"
    ],
    "esAliasTransManager": {
        "esValue": {
            "elements": {
                "9534a201-5709-2279-022f-47b7a1848b1f": {
                    "_type": "org.uengine.modeling.model.BoundedContext",
                    "aggregates": [
                        {
                            "id": "ff155dca-57e7-325f-720d-51a66c606f5e"
                        }
                    ],
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "description": "[{\"type\":\"userStory\",\"text\":\"도서 관리 화면에서는 새로운 도서를 등록하고 현재 보유한 도서들의 상태를 관리할 수 있어야 해. 도서 등록 시에는 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받아야 해. ISBN은 13자리 숫자여야 하고 중복 확인이 필요해. 카테고리는 소설/비소설/학술/잡지 중에서 선택할 수 있어야 해. 등록된 도서는 처음에 '대출가능' 상태가 되고, 이후 대출/반납 상황에 따라 '대출중', '예약중' 상태로 자동으로 변경되어야 해. 도서가 훼손되거나 분실된 경우 '폐기' 처리가 가능해야 해며, 폐기된 도서는 더 이상 대출이 불가능해야 해.\"}]",
                    "id": "9534a201-5709-2279-022f-47b7a1848b1f",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.BoundedContext",
                        "height": 590,
                        "id": "9534a201-5709-2279-022f-47b7a1848b1f",
                        "style": "{}",
                        "width": 560,
                        "x": 650,
                        "y": 450
                    },
                    "gitURL": None,
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
                        "height": 350,
                        "id": "9534a201-5709-2279-022f-47b7a1848b1f",
                        "style": "{}",
                        "width": 350,
                        "x": 235,
                        "y": 365
                    },
                    "members": [],
                    "name": "BookManagement",
                    "displayName": "도서 관리",
                    "oldName": "",
                    "policies": [],
                    "portGenerated": None,
                    "preferredPlatform": "template-spring-boot",
                    "preferredPlatformConf": {},
                    "rotateStatus": False,
                    "tempId": "",
                    "templatePerElements": {},
                    "views": [],
                    "definitionId": "163972132_es_9b15cefec6c1e88801f66e18231de4a6"
                },
                "5782787e-3129-dfa6-0228-99246a0507a5": {
                    "_type": "org.uengine.modeling.model.BoundedContext",
                    "aggregates": [
                        {
                            "id": "ab09c1d7-158c-1569-bde8-76c87397353f"
                        }
                    ],
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "description": "[{\"type\":\"userStory\",\"text\":\"대출/반납 화면에서는 회원이 도서를 대출하고 반납하는 것을 관리할 수 있어야 해. 대출 신청 시에는 회원번호와 이름으로 회원을 확인하고, 대출할 도서를 선택해야 해. 도서는 도서명이나 ISBN으로 검색할 수 있어야 해. 대출 기간은 7일/14일/30일 중에서 선택할 수 있어. 만약 대출하려는 도서가 이미 대출 중이라면, 예약 신청이 가능해야 해. 대출이 완료되면 해당 도서의 상태는 자동으로 '대출중'으로 변경되어야 해.\"}]",
                    "id": "5782787e-3129-dfa6-0228-99246a0507a5",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.BoundedContext",
                        "height": 590,
                        "id": "5782787e-3129-dfa6-0228-99246a0507a5",
                        "style": "{}",
                        "width": 560,
                        "x": 1235,
                        "y": 450
                    },
                    "gitURL": None,
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
                        "height": 350,
                        "id": "5782787e-3129-dfa6-0228-99246a0507a5",
                        "style": "{}",
                        "width": 350,
                        "x": 235,
                        "y": 365
                    },
                    "members": [],
                    "name": "LoanManagement",
                    "displayName": "대출/반납 관리",
                    "oldName": "",
                    "policies": [],
                    "portGenerated": 8080,
                    "preferredPlatform": "template-spring-boot",
                    "preferredPlatformConf": {},
                    "rotateStatus": False,
                    "tempId": "",
                    "templatePerElements": {},
                    "views": [],
                    "definitionId": "163972132_es_9b15cefec6c1e88801f66e18231de4a6"
                },
                "ff155dca-57e7-325f-720d-51a66c606f5e": {
                    "aggregateRoot": {
                        "_type": "org.uengine.modeling.model.AggregateRoot",
                        "fieldDescriptors": [
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": True,
                                "name": "ISBN",
                                "nameCamelCase": "isbn",
                                "namePascalCase": "Isbn",
                                "displayName": "",
                                "referenceClass": None,
                                "isOverrideField": False,
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": False,
                                "name": "bookTitle",
                                "nameCamelCase": "bookTitle",
                                "namePascalCase": "BookTitle",
                                "displayName": "",
                                "referenceClass": None,
                                "isOverrideField": False,
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": False,
                                "name": "author",
                                "nameCamelCase": "author",
                                "namePascalCase": "Author",
                                "displayName": "",
                                "referenceClass": None,
                                "isOverrideField": False,
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": False,
                                "name": "publisher",
                                "nameCamelCase": "publisher",
                                "namePascalCase": "Publisher",
                                "displayName": "",
                                "referenceClass": None,
                                "isOverrideField": False,
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Category",
                                "isCopy": False,
                                "isKey": False,
                                "name": "category",
                                "nameCamelCase": "category",
                                "namePascalCase": "Category",
                                "displayName": "",
                                "referenceClass": None,
                                "isOverrideField": False,
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Status",
                                "isCopy": False,
                                "isKey": False,
                                "name": "status",
                                "nameCamelCase": "status",
                                "namePascalCase": "Status",
                                "displayName": "",
                                "referenceClass": None,
                                "isOverrideField": False,
                                "_type": "org.uengine.model.FieldDescriptor"
                            }
                        ],
                        "entities": {
                            "elements": {
                                "db402125-8037-a260-d3f4-8393dd469d87": {
                                    "_type": "org.uengine.uml.model.Class",
                                    "id": "db402125-8037-a260-d3f4-8393dd469d87",
                                    "name": "Book",
                                    "namePascalCase": "Book",
                                    "nameCamelCase": "book",
                                    "namePlural": "Books",
                                    "fieldDescriptors": [
                                        {
                                            "className": "String",
                                            "isCopy": False,
                                            "isKey": True,
                                            "name": "ISBN",
                                            "displayName": "",
                                            "nameCamelCase": "isbn",
                                            "namePascalCase": "Isbn",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None
                                        },
                                        {
                                            "className": "String",
                                            "isCopy": False,
                                            "isKey": False,
                                            "name": "bookTitle",
                                            "displayName": "",
                                            "nameCamelCase": "bookTitle",
                                            "namePascalCase": "BookTitle",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None
                                        },
                                        {
                                            "className": "String",
                                            "isCopy": False,
                                            "isKey": False,
                                            "name": "author",
                                            "displayName": "",
                                            "nameCamelCase": "author",
                                            "namePascalCase": "Author",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None
                                        },
                                        {
                                            "className": "String",
                                            "isCopy": False,
                                            "isKey": False,
                                            "name": "publisher",
                                            "displayName": "",
                                            "nameCamelCase": "publisher",
                                            "namePascalCase": "Publisher",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None
                                        },
                                        {
                                            "className": "Category",
                                            "isCopy": False,
                                            "isKey": False,
                                            "name": "category",
                                            "displayName": "",
                                            "nameCamelCase": "category",
                                            "namePascalCase": "Category",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None
                                        },
                                        {
                                            "className": "Status",
                                            "isCopy": False,
                                            "isKey": False,
                                            "name": "status",
                                            "displayName": "",
                                            "nameCamelCase": "status",
                                            "namePascalCase": "Status",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None
                                        }
                                    ],
                                    "operations": [],
                                    "elementView": {
                                        "_type": "org.uengine.uml.model.Class",
                                        "id": "db402125-8037-a260-d3f4-8393dd469d87",
                                        "x": 200,
                                        "y": 200,
                                        "width": 200,
                                        "height": 100,
                                        "style": "{}",
                                        "titleH": 50,
                                        "subEdgeH": 120,
                                        "fieldH": 90,
                                        "methodH": 30
                                    },
                                    "selected": False,
                                    "relations": [],
                                    "parentOperations": [],
                                    "relationType": None,
                                    "isVO": False,
                                    "isAbstract": False,
                                    "isInterface": False,
                                    "isAggregateRoot": True,
                                    "parentId": "ff155dca-57e7-325f-720d-51a66c606f5e"
                                },
                                "4c295aed-6977-7d81-e1f7-b7d341a9f484": {
                                    "_type": "org.uengine.uml.model.enum",
                                    "id": "4c295aed-6977-7d81-e1f7-b7d341a9f484",
                                    "name": "Category",
                                    "displayName": "카테고리",
                                    "nameCamelCase": "category",
                                    "namePascalCase": "Category",
                                    "namePlural": "categories",
                                    "elementView": {
                                        "_type": "org.uengine.uml.model.enum",
                                        "id": "4c295aed-6977-7d81-e1f7-b7d341a9f484",
                                        "x": 700,
                                        "y": 456,
                                        "width": 200,
                                        "height": 100,
                                        "style": "{}",
                                        "titleH": 50,
                                        "subEdgeH": 50
                                    },
                                    "selected": False,
                                    "items": [
                                        {
                                            "value": "NOVEL"
                                        },
                                        {
                                            "value": "NONFICTION"
                                        },
                                        {
                                            "value": "ACADEMIC"
                                        },
                                        {
                                            "value": "MAGAZINE"
                                        }
                                    ],
                                    "useKeyValue": False,
                                    "relations": []
                                },
                                "127283ec-5a2a-a5f7-bcb8-2e93b8acc656": {
                                    "_type": "org.uengine.uml.model.enum",
                                    "id": "127283ec-5a2a-a5f7-bcb8-2e93b8acc656",
                                    "name": "Status",
                                    "displayName": "도서상태",
                                    "nameCamelCase": "status",
                                    "namePascalCase": "Status",
                                    "namePlural": "statuses",
                                    "elementView": {
                                        "_type": "org.uengine.uml.model.enum",
                                        "id": "127283ec-5a2a-a5f7-bcb8-2e93b8acc656",
                                        "x": 950,
                                        "y": 456,
                                        "width": 200,
                                        "height": 100,
                                        "style": "{}",
                                        "titleH": 50,
                                        "subEdgeH": 50
                                    },
                                    "selected": False,
                                    "items": [
                                        {
                                            "value": "AVAILABLE"
                                        },
                                        {
                                            "value": "BORROWED"
                                        },
                                        {
                                            "value": "RESERVED"
                                        },
                                        {
                                            "value": "DISCARDED"
                                        }
                                    ],
                                    "useKeyValue": False,
                                    "relations": []
                                }
                            },
                            "relations": {}
                        },
                        "operations": []
                    },
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "name": "9534a201-5709-2279-022f-47b7a1848b1f",
                        "id": "9534a201-5709-2279-022f-47b7a1848b1f"
                    },
                    "commands": [],
                    "description": None,
                    "id": "ff155dca-57e7-325f-720d-51a66c606f5e",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Aggregate",
                        "id": "ff155dca-57e7-325f-720d-51a66c606f5e",
                        "x": 650,
                        "y": 450,
                        "width": 130,
                        "height": 400
                    },
                    "events": [],
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.AggregateHexagonal",
                        "id": "ff155dca-57e7-325f-720d-51a66c606f5e",
                        "x": 0,
                        "y": 0,
                        "subWidth": 0,
                        "width": 0
                    },
                    "name": "Book",
                    "displayName": "도서",
                    "nameCamelCase": "book",
                    "namePascalCase": "Book",
                    "namePlural": "books",
                    "rotateStatus": False,
                    "selected": False,
                    "_type": "org.uengine.modeling.model.Aggregate"
                },
                "ab09c1d7-158c-1569-bde8-76c87397353f": {
                    "aggregateRoot": {
                        "_type": "org.uengine.modeling.model.AggregateRoot",
                        "fieldDescriptors": [
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": True,
                                "name": "loanId",
                                "nameCamelCase": "loanId",
                                "namePascalCase": "LoanId",
                                "displayName": "",
                                "referenceClass": None,
                                "isOverrideField": False,
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": False,
                                "name": "memberNumber",
                                "nameCamelCase": "memberNumber",
                                "namePascalCase": "MemberNumber",
                                "displayName": "",
                                "referenceClass": None,
                                "isOverrideField": False,
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": False,
                                "name": "bookISBN",
                                "nameCamelCase": "bookIsbn",
                                "namePascalCase": "BookIsbn",
                                "displayName": "",
                                "referenceClass": None,
                                "isOverrideField": False,
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Integer",
                                "isCopy": False,
                                "isKey": False,
                                "name": "loanPeriod",
                                "nameCamelCase": "loanPeriod",
                                "namePascalCase": "LoanPeriod",
                                "displayName": "",
                                "referenceClass": None,
                                "isOverrideField": False,
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Date",
                                "isCopy": False,
                                "isKey": False,
                                "name": "loanDate",
                                "nameCamelCase": "loanDate",
                                "namePascalCase": "LoanDate",
                                "displayName": "",
                                "referenceClass": None,
                                "isOverrideField": False,
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "TransactionType",
                                "isCopy": False,
                                "isKey": False,
                                "name": "transactionType",
                                "nameCamelCase": "transactionType",
                                "namePascalCase": "TransactionType",
                                "displayName": "",
                                "referenceClass": None,
                                "isOverrideField": False,
                                "_type": "org.uengine.model.FieldDescriptor"
                            }
                        ],
                        "entities": {
                            "elements": {
                                "ad85c5be-8f77-b11c-84dc-c2222ae32be2": {
                                    "_type": "org.uengine.uml.model.Class",
                                    "id": "ad85c5be-8f77-b11c-84dc-c2222ae32be2",
                                    "name": "LoanTransaction",
                                    "namePascalCase": "LoanTransaction",
                                    "nameCamelCase": "loanTransaction",
                                    "namePlural": "LoanTransactions",
                                    "fieldDescriptors": [
                                        {
                                            "className": "String",
                                            "isCopy": False,
                                            "isKey": True,
                                            "name": "loanId",
                                            "displayName": "",
                                            "nameCamelCase": "loanId",
                                            "namePascalCase": "LoanId",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None
                                        },
                                        {
                                            "className": "String",
                                            "isCopy": False,
                                            "isKey": False,
                                            "name": "memberNumber",
                                            "displayName": "",
                                            "nameCamelCase": "memberNumber",
                                            "namePascalCase": "MemberNumber",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None
                                        },
                                        {
                                            "className": "String",
                                            "isCopy": False,
                                            "isKey": False,
                                            "name": "bookISBN",
                                            "displayName": "",
                                            "nameCamelCase": "bookIsbn",
                                            "namePascalCase": "BookIsbn",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None
                                        },
                                        {
                                            "className": "Integer",
                                            "isCopy": False,
                                            "isKey": False,
                                            "name": "loanPeriod",
                                            "displayName": "",
                                            "nameCamelCase": "loanPeriod",
                                            "namePascalCase": "LoanPeriod",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None
                                        },
                                        {
                                            "className": "Date",
                                            "isCopy": False,
                                            "isKey": False,
                                            "name": "loanDate",
                                            "displayName": "",
                                            "nameCamelCase": "loanDate",
                                            "namePascalCase": "LoanDate",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None
                                        },
                                        {
                                            "className": "TransactionType",
                                            "isCopy": False,
                                            "isKey": False,
                                            "name": "transactionType",
                                            "displayName": "",
                                            "nameCamelCase": "transactionType",
                                            "namePascalCase": "TransactionType",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None
                                        }
                                    ],
                                    "operations": [],
                                    "elementView": {
                                        "_type": "org.uengine.uml.model.Class",
                                        "id": "ad85c5be-8f77-b11c-84dc-c2222ae32be2",
                                        "x": 200,
                                        "y": 200,
                                        "width": 200,
                                        "height": 100,
                                        "style": "{}",
                                        "titleH": 50,
                                        "subEdgeH": 120,
                                        "fieldH": 90,
                                        "methodH": 30
                                    },
                                    "selected": False,
                                    "relations": [],
                                    "parentOperations": [],
                                    "relationType": None,
                                    "isVO": False,
                                    "isAbstract": False,
                                    "isInterface": False,
                                    "isAggregateRoot": True,
                                    "parentId": "ab09c1d7-158c-1569-bde8-76c87397353f"
                                },
                                "01b163f3-9fe5-0274-4cde-e6f47a48de5b": {
                                    "_type": "org.uengine.uml.model.enum",
                                    "id": "01b163f3-9fe5-0274-4cde-e6f47a48de5b",
                                    "name": "TransactionType",
                                    "displayName": "거래 유형",
                                    "nameCamelCase": "transactionType",
                                    "namePascalCase": "TransactionType",
                                    "namePlural": "transactionTypes",
                                    "elementView": {
                                        "_type": "org.uengine.uml.model.enum",
                                        "id": "01b163f3-9fe5-0274-4cde-e6f47a48de5b",
                                        "x": 700,
                                        "y": 456,
                                        "width": 200,
                                        "height": 100,
                                        "style": "{}",
                                        "titleH": 50,
                                        "subEdgeH": 50
                                    },
                                    "selected": False,
                                    "items": [
                                        {
                                            "value": "LOAN"
                                        },
                                        {
                                            "value": "RETURN"
                                        },
                                        {
                                            "value": "RESERVATION"
                                        }
                                    ],
                                    "useKeyValue": False,
                                    "relations": []
                                }
                            },
                            "relations": {}
                        },
                        "operations": []
                    },
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "name": "5782787e-3129-dfa6-0228-99246a0507a5",
                        "id": "5782787e-3129-dfa6-0228-99246a0507a5"
                    },
                    "commands": [],
                    "description": None,
                    "id": "ab09c1d7-158c-1569-bde8-76c87397353f",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Aggregate",
                        "id": "ab09c1d7-158c-1569-bde8-76c87397353f",
                        "x": 1235,
                        "y": 450,
                        "width": 130,
                        "height": 400
                    },
                    "events": [],
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.AggregateHexagonal",
                        "id": "ab09c1d7-158c-1569-bde8-76c87397353f",
                        "x": 0,
                        "y": 0,
                        "subWidth": 0,
                        "width": 0
                    },
                    "name": "LoanTransaction",
                    "displayName": "대출/반납 거래",
                    "nameCamelCase": "loanTransaction",
                    "namePascalCase": "LoanTransaction",
                    "namePlural": "loanTransactions",
                    "rotateStatus": False,
                    "selected": False,
                    "_type": "org.uengine.modeling.model.Aggregate"
                }
            },
            "relations": {},
            "basePlatform": None,
            "basePlatformConf": {},
            "toppingPlatforms": [],
            "toppingPlatformsConf": {},
            "scm": {
                "tag": None,
                "org": None,
                "repo": None,
                "forkedOrg": None,
                "forkedRepo": None
            },
            "version": 3,
            "k8sValue": {
                "elements": {},
                "relations": {}
            }
        },
        "UUIDToAliasDic": {
            "9534a201-5709-2279-022f-47b7a1848b1f": "bc-bookManagement",
            "5782787e-3129-dfa6-0228-99246a0507a5": "bc-loanManagement",
            "ff155dca-57e7-325f-720d-51a66c606f5e": "agg-book",
            "db402125-8037-a260-d3f4-8393dd469d87": "agg-root-book",
            "4c295aed-6977-7d81-e1f7-b7d341a9f484": "enum-category",
            "127283ec-5a2a-a5f7-bcb8-2e93b8acc656": "enum-status",
            "ab09c1d7-158c-1569-bde8-76c87397353f": "agg-loanTransaction",
            "ad85c5be-8f77-b11c-84dc-c2222ae32be2": "agg-root-loanTransaction",
            "01b163f3-9fe5-0274-4cde-e6f47a48de5b": "enum-transactionType"
        },
        "aliasToUUIDDic": {
            "bc-bookManagement": "9534a201-5709-2279-022f-47b7a1848b1f",
            "bc-loanManagement": "5782787e-3129-dfa6-0228-99246a0507a5",
            "agg-book": "ff155dca-57e7-325f-720d-51a66c606f5e",
            "agg-root-book": "db402125-8037-a260-d3f4-8393dd469d87",
            "enum-category": "4c295aed-6977-7d81-e1f7-b7d341a9f484",
            "enum-status": "127283ec-5a2a-a5f7-bcb8-2e93b8acc656",
            "agg-loanTransaction": "ab09c1d7-158c-1569-bde8-76c87397353f",
            "agg-root-loanTransaction": "ad85c5be-8f77-b11c-84dc-c2222ae32be2",
            "enum-transactionType": "01b163f3-9fe5-0274-4cde-e6f47a48de5b"
        }
    },
    "summarizedESValue": {
        "deletedProperties": [
            "aggregate.commands",
            "aggregate.events",
            "aggregate.readModels"
        ],
        "boundedContexts": [
            {
                "id": "bc-bookManagement",
                "name": "BookManagement",
                "actors": [],
                "aggregates": [
                    {
                        "id": "agg-book",
                        "name": "Book",
                        "properties": [
                            {
                                "name": "ISBN",
                                "isKey": True
                            },
                            {
                                "name": "bookTitle"
                            },
                            {
                                "name": "author"
                            },
                            {
                                "name": "publisher"
                            },
                            {
                                "name": "category",
                                "type": "Category"
                            },
                            {
                                "name": "status",
                                "type": "Status"
                            }
                        ],
                        "entities": [],
                        "enumerations": [
                            {
                                "id": "enum-category",
                                "name": "Category",
                                "items": [
                                    "NOVEL",
                                    "NONFICTION",
                                    "ACADEMIC",
                                    "MAGAZINE"
                                ]
                            },
                            {
                                "id": "enum-status",
                                "name": "Status",
                                "items": [
                                    "AVAILABLE",
                                    "BORROWED",
                                    "RESERVED",
                                    "DISCARDED"
                                ]
                            }
                        ],
                        "valueObjects": []
                    }
                ]
            },
            {
                "id": "bc-loanManagement",
                "name": "LoanManagement",
                "actors": [],
                "aggregates": [
                    {
                        "id": "agg-loanTransaction",
                        "name": "LoanTransaction",
                        "properties": [
                            {
                                "name": "loanId",
                                "isKey": True
                            },
                            {
                                "name": "memberNumber"
                            },
                            {
                                "name": "bookISBN"
                            },
                            {
                                "name": "loanPeriod",
                                "type": "Integer"
                            },
                            {
                                "name": "loanDate",
                                "type": "Date"
                            },
                            {
                                "name": "transactionType",
                                "type": "TransactionType"
                            }
                        ],
                        "entities": [],
                        "enumerations": [
                            {
                                "id": "enum-transactionType",
                                "name": "TransactionType",
                                "items": [
                                    "LOAN",
                                    "RETURN",
                                    "RESERVATION"
                                ]
                            }
                        ],
                        "valueObjects": []
                    }
                ]
            }
        ]
    },
    "subjectText": "Creating ID Classes for BookReference"
}