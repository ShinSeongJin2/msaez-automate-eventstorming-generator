create_policy_actions_by_function_inputs = {
    "targetBoundedContext": {
        "_type": "org.uengine.modeling.model.BoundedContext",
        "aggregates": [],
        "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
        "description": "[{\"type\":\"userStory\",\"text\":\"도서 관리 화면에서는 새로운 도서를 등록하고 현재 보유한 도서들의 상태를 관리할 수 있어야 해. 도서 등록 시에는 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받아야 해. ISBN은 13자리 숫자여야 하고 중복 확인이 필요해. 카테고리는 소설/비소설/학술/잡지 중에서 선택할 수 있어야 해. 등록된 도서는 처음에 '대출가능' 상태가 되고, 이후 대출/반납 상황에 따라 '대출중', '예약중' 상태로 자동으로 변경되어야 해. 도서가 훼손되거나 분실된 경우 '폐기' 처리가 가능해야 해며, 폐기된 도서는 더 이상 대출이 불가능해야 해.\"}]",
        "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c",
        "elementView": {
            "_type": "org.uengine.modeling.model.BoundedContext",
            "height": 590,
            "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c",
            "style": "{}",
            "width": 560,
            "x": 650,
            "y": 450
        },
        "gitURL": None,
        "hexagonalView": {
            "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
            "height": 350,
            "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c",
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
        "definitionId": "163972132_es_0ef8941a61478455167111b05b128cea"
    },
    "description": "{\"userStories\":[{\"title\":\"도서 등록 및 관리\",\"description\":\"사용자는 도서 관리 화면에서 새로운 도서를 등록하고, 등록된 도서의 대출 상태를 관리할 수 있다. 신규 등록 시 도서명, ISBN, 저자, 출판사, 카테고리 정보를 필수 입력 받고, ISBN은 13자리 숫자이며 중복 체크가 수행된다. 등록 후 도서는 초기 '대출가능' 상태로 표시되며, 대출, 반납, 예약 등의 이벤트에 따라 상태가 자동 갱신된다. 또한, 도서가 훼손되거나 분실된 경우, '폐기' 처리를 통해 대출 기능에서 제외된다.\",\"acceptance\":[\"도서 등록 시 도서명, ISBN, 저자, 출판사, 카테고리 정보를 반드시 입력해야 한다.\",\"ISBN은 13자리 숫자여야 하며, 중복 체크 로직이 구현되어 있다.\",\"카테고리는 소설, 비소설, 학술, 잡지 중에서 선택할 수 있다.\",\"등록된 도서는 초기 상태가 '대출가능'이며, 대출/반납/예약에 따라 상태가 자동 변경된다.\",\"도서가 훼손되거나 분실되면 '폐기' 처리되어 대출 기능에서 제외된다.\"]}],\"entities\":{\"Book\":{\"properties\":[{\"name\":\"bookTitle\",\"type\":\"String\",\"required\":true},{\"name\":\"ISBN\",\"type\":\"String\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"author\",\"type\":\"String\",\"required\":true},{\"name\":\"publisher\",\"type\":\"String\",\"required\":true},{\"name\":\"category\",\"type\":\"enum\",\"required\":true,\"values\":[\"소설\",\"비소설\",\"학술\",\"잡지\"]},{\"name\":\"status\",\"type\":\"enum\",\"required\":true,\"values\":[\"대출가능\",\"대출중\",\"예약중\",\"폐기\"]}]}},\"businessRules\":[{\"name\":\"ISBN 형식 검증\",\"description\":\"ISBN은 13자리 숫자로 구성되어야 하며, 입력된 ISBN은 기존 등록 도서와 중복되지 않아야 한다.\"},{\"name\":\"초기 대출 상태\",\"description\":\"신규 등록된 도서는 자동으로 '대출가능' 상태로 설정된다.\"},{\"name\":\"상태 전이 관리\",\"description\":\"대출, 반납, 예약, 훼손 또는 분실 이벤트 발생 시 도서의 상태는 각각 '대출중', '예약중', '폐기'로 자동 갱신된다.\"},{\"name\":\"폐기 처리\",\"description\":\"도서가 '폐기' 상태일 경우 더 이상 대출이 불가능하다.\"}],\"interfaces\":{\"BookManagement\":{\"sections\":[{\"name\":\"도서 등록\",\"type\":\"form\",\"fields\":[{\"name\":\"bookTitle\",\"type\":\"text\",\"required\":true},{\"name\":\"ISBN\",\"type\":\"text\",\"required\":true},{\"name\":\"author\",\"type\":\"text\",\"required\":true},{\"name\":\"publisher\",\"type\":\"text\",\"required\":true},{\"name\":\"category\",\"type\":\"select\",\"required\":true}],\"actions\":[\"Register Book\"],\"filters\":[],\"resultTable\":{\"columns\":[],\"actions\":[]}},{\"name\":\"도서 상태 관리\",\"type\":\"table\",\"fields\":[],\"actions\":[\"Modify Status\",\"Discard Book\"],\"filters\":[\"category\",\"status\"],\"resultTable\":{\"columns\":[\"ISBN\",\"bookTitle\",\"author\",\"publisher\",\"category\",\"status\"],\"actions\":[\"View Details\"]}}]}}}",
    "esValue": {
        "elements": {
            "97f2473e-7068-21ee-652d-ba0a8f41dd2c": {
                "_type": "org.uengine.modeling.model.BoundedContext",
                "aggregates": [
                    {
                        "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                    }
                ],
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "description": "[{\"type\":\"userStory\",\"text\":\"도서 관리 화면에서는 새로운 도서를 등록하고 현재 보유한 도서들의 상태를 관리할 수 있어야 해. 도서 등록 시에는 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받아야 해. ISBN은 13자리 숫자여야 하고 중복 확인이 필요해. 카테고리는 소설/비소설/학술/잡지 중에서 선택할 수 있어야 해. 등록된 도서는 처음에 '대출가능' 상태가 되고, 이후 대출/반납 상황에 따라 '대출중', '예약중' 상태로 자동으로 변경되어야 해. 도서가 훼손되거나 분실된 경우 '폐기' 처리가 가능해야 해며, 폐기된 도서는 더 이상 대출이 불가능해야 해.\"}]",
                "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c",
                "elementView": {
                    "_type": "org.uengine.modeling.model.BoundedContext",
                    "height": 726,
                    "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c",
                    "style": "{}",
                    "width": 560,
                    "x": 650,
                    "y": 518
                },
                "gitURL": None,
                "hexagonalView": {
                    "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
                    "height": 350,
                    "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c",
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
                "definitionId": "163972132_es_0ef8941a61478455167111b05b128cea"
            },
            "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908": {
                "_type": "org.uengine.modeling.model.BoundedContext",
                "aggregates": [
                    {
                        "id": "30176142-717c-cc1a-0d59-771539ac988a"
                    }
                ],
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "description": "[{\"type\":\"userStory\",\"text\":\"대출/반납 화면에서는 회원이 도서를 대출하고 반납하는 것을 관리할 수 있어야 해. 대출 신청 시에는 회원번호와 이름으로 회원을 확인하고, 대출할 도서를 선택해야 해. 도서는 도서명이나 ISBN으로 검색할 수 있어야 해. 대출 기간은 7일/14일/30일 중에서 선택할 수 있어. 만약 대출하려는 도서가 이미 대출 중이라면, 예약 신청이 가능해야 해. 대출이 완료되면 해당 도서의 상태는 자동으로 '대출중'으로 변경되어야 해.\"}]",
                "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908",
                "elementView": {
                    "_type": "org.uengine.modeling.model.BoundedContext",
                    "height": 726,
                    "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908",
                    "style": "{}",
                    "width": 560,
                    "x": 1235,
                    "y": 518
                },
                "gitURL": None,
                "hexagonalView": {
                    "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
                    "height": 350,
                    "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908",
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
                "definitionId": "163972132_es_0ef8941a61478455167111b05b128cea"
            },
            "f81e4c75-040c-83ad-4656-65cfccc74cc2": {
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
                            "aa6acc4d-3773-6aa9-3cf2-d22a860272a8": {
                                "_type": "org.uengine.uml.model.Class",
                                "id": "aa6acc4d-3773-6aa9-3cf2-d22a860272a8",
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
                                    "id": "aa6acc4d-3773-6aa9-3cf2-d22a860272a8",
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
                                "parentId": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                            },
                            "3e68e3a2-7dd9-dab0-3d03-2753ba0a1233": {
                                "_type": "org.uengine.uml.model.enum",
                                "id": "3e68e3a2-7dd9-dab0-3d03-2753ba0a1233",
                                "name": "Category",
                                "displayName": "카테고리",
                                "nameCamelCase": "category",
                                "namePascalCase": "Category",
                                "namePlural": "categories",
                                "elementView": {
                                    "_type": "org.uengine.uml.model.enum",
                                    "id": "3e68e3a2-7dd9-dab0-3d03-2753ba0a1233",
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
                            "73640bd2-3239-18e6-0c05-22462730ed92": {
                                "_type": "org.uengine.uml.model.enum",
                                "id": "73640bd2-3239-18e6-0c05-22462730ed92",
                                "name": "Status",
                                "displayName": "도서상태",
                                "nameCamelCase": "status",
                                "namePascalCase": "Status",
                                "namePlural": "statuses",
                                "elementView": {
                                    "_type": "org.uengine.uml.model.enum",
                                    "id": "73640bd2-3239-18e6-0c05-22462730ed92",
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
                    "name": "97f2473e-7068-21ee-652d-ba0a8f41dd2c",
                    "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                },
                "commands": [],
                "description": None,
                "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2",
                "elementView": {
                    "_type": "org.uengine.modeling.model.Aggregate",
                    "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2",
                    "x": 650,
                    "y": 525,
                    "width": 130,
                    "height": 550
                },
                "events": [],
                "hexagonalView": {
                    "_type": "org.uengine.modeling.model.AggregateHexagonal",
                    "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2",
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
            "30176142-717c-cc1a-0d59-771539ac988a": {
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
                        },
                        {
                            "className": "BookId",
                            "isCopy": False,
                            "isKey": False,
                            "name": "bookId",
                            "nameCamelCase": "bookId",
                            "namePascalCase": "BookId",
                            "displayName": "",
                            "referenceClass": "Book",
                            "isOverrideField": True,
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "entities": {
                        "elements": {
                            "19aa4d64-6084-e826-7c69-0bd1896e6f79": {
                                "_type": "org.uengine.uml.model.Class",
                                "id": "19aa4d64-6084-e826-7c69-0bd1896e6f79",
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
                                    },
                                    {
                                        "className": "BookId",
                                        "isCopy": False,
                                        "isKey": False,
                                        "name": "bookId",
                                        "nameCamelCase": "bookId",
                                        "namePascalCase": "BookId",
                                        "displayName": "",
                                        "referenceClass": "Book",
                                        "isOverrideField": True,
                                        "_type": "org.uengine.model.FieldDescriptor"
                                    }
                                ],
                                "operations": [],
                                "elementView": {
                                    "_type": "org.uengine.uml.model.Class",
                                    "id": "19aa4d64-6084-e826-7c69-0bd1896e6f79",
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
                                "parentId": "30176142-717c-cc1a-0d59-771539ac988a"
                            },
                            "7ec1a4ec-7237-ab46-0c52-fe21ca1a9a09": {
                                "_type": "org.uengine.uml.model.enum",
                                "id": "7ec1a4ec-7237-ab46-0c52-fe21ca1a9a09",
                                "name": "TransactionType",
                                "displayName": "거래 유형",
                                "nameCamelCase": "transactionType",
                                "namePascalCase": "TransactionType",
                                "namePlural": "transactionTypes",
                                "elementView": {
                                    "_type": "org.uengine.uml.model.enum",
                                    "id": "7ec1a4ec-7237-ab46-0c52-fe21ca1a9a09",
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
                            },
                            "9b7dd1cc-d76b-2b36-1f93-9eb8930afef6": {
                                "_type": "org.uengine.uml.model.vo.Class",
                                "id": "9b7dd1cc-d76b-2b36-1f93-9eb8930afef6",
                                "name": "BookId",
                                "displayName": "",
                                "namePascalCase": "BookId",
                                "nameCamelCase": "bookId",
                                "fieldDescriptors": [
                                    {
                                        "className": "String",
                                        "isKey": True,
                                        "label": "- ISBN: String",
                                        "name": "ISBN",
                                        "nameCamelCase": "isbn",
                                        "namePascalCase": "Isbn",
                                        "displayName": "",
                                        "referenceClass": "Book",
                                        "isOverrideField": True,
                                        "_type": "org.uengine.model.FieldDescriptor"
                                    }
                                ],
                                "operations": [],
                                "elementView": {
                                    "_type": "org.uengine.uml.model.vo.address.Class",
                                    "id": "9b7dd1cc-d76b-2b36-1f93-9eb8930afef6",
                                    "x": 700,
                                    "y": 152,
                                    "width": 200,
                                    "height": 100,
                                    "style": "{}",
                                    "titleH": 50,
                                    "subEdgeH": 170,
                                    "fieldH": 150,
                                    "methodH": 30
                                },
                                "selected": False,
                                "parentOperations": [],
                                "relationType": None,
                                "isVO": True,
                                "relations": [],
                                "groupElement": None,
                                "isAggregateRoot": False,
                                "namePlural": "BookIds",
                                "isAbstract": False,
                                "isInterface": False
                            }
                        },
                        "relations": {}
                    },
                    "operations": []
                },
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "boundedContext": {
                    "name": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908",
                    "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                },
                "commands": [],
                "description": None,
                "id": "30176142-717c-cc1a-0d59-771539ac988a",
                "elementView": {
                    "_type": "org.uengine.modeling.model.Aggregate",
                    "id": "30176142-717c-cc1a-0d59-771539ac988a",
                    "x": 1235,
                    "y": 525,
                    "width": 130,
                    "height": 550
                },
                "events": [],
                "hexagonalView": {
                    "_type": "org.uengine.modeling.model.AggregateHexagonal",
                    "id": "30176142-717c-cc1a-0d59-771539ac988a",
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
            },
            "dc9f7be6-103e-0d9f-96b6-a1de4ae31d3f": {
                "alertURL": "/static/image/symbol/alert-icon.png",
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "checkAlert": True,
                "description": None,
                "id": "dc9f7be6-103e-0d9f-96b6-a1de4ae31d3f",
                "elementView": {
                    "angle": 0,
                    "height": 116,
                    "id": "dc9f7be6-103e-0d9f-96b6-a1de4ae31d3f",
                    "style": "{}",
                    "width": 100,
                    "x": 744,
                    "y": 250,
                    "_type": "org.uengine.modeling.model.Event"
                },
                "fieldDescriptors": [
                    {
                        "className": "String",
                        "isCopy": False,
                        "isKey": True,
                        "name": "ISBN",
                        "nameCamelCase": "isbn",
                        "namePascalCase": "Isbn",
                        "displayName": "",
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
                        "_type": "org.uengine.model.FieldDescriptor"
                    }
                ],
                "hexagonalView": {
                    "height": 0,
                    "id": "dc9f7be6-103e-0d9f-96b6-a1de4ae31d3f",
                    "style": "{}",
                    "width": 0,
                    "x": 0,
                    "y": 0,
                    "_type": "org.uengine.modeling.model.EventHexagonal"
                },
                "name": "BookRegistered",
                "displayName": "도서 등록됨",
                "nameCamelCase": "bookRegistered",
                "namePascalCase": "BookRegistered",
                "namePlural": "",
                "relationCommandInfo": [],
                "relationPolicyInfo": [],
                "rotateStatus": False,
                "selected": False,
                "trigger": "@PostPersist",
                "_type": "org.uengine.modeling.model.Event",
                "aggregate": {
                    "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                },
                "boundedContext": {
                    "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                }
            },
            "c763f4a6-b0e9-0a7e-e343-c8de448157bd": {
                "alertURL": "/static/image/symbol/alert-icon.png",
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "checkAlert": True,
                "description": None,
                "id": "c763f4a6-b0e9-0a7e-e343-c8de448157bd",
                "elementView": {
                    "angle": 0,
                    "height": 116,
                    "id": "c763f4a6-b0e9-0a7e-e343-c8de448157bd",
                    "style": "{}",
                    "width": 100,
                    "x": 744,
                    "y": 380,
                    "_type": "org.uengine.modeling.model.Event"
                },
                "fieldDescriptors": [
                    {
                        "className": "String",
                        "isCopy": False,
                        "isKey": True,
                        "name": "ISBN",
                        "nameCamelCase": "isbn",
                        "namePascalCase": "Isbn",
                        "displayName": "",
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
                        "_type": "org.uengine.model.FieldDescriptor"
                    },
                    {
                        "className": "Date",
                        "isCopy": False,
                        "isKey": False,
                        "name": "changedAt",
                        "nameCamelCase": "changedAt",
                        "namePascalCase": "ChangedAt",
                        "displayName": "",
                        "_type": "org.uengine.model.FieldDescriptor"
                    },
                    {
                        "className": "String",
                        "isCopy": False,
                        "isKey": False,
                        "name": "reason",
                        "nameCamelCase": "reason",
                        "namePascalCase": "Reason",
                        "displayName": "",
                        "_type": "org.uengine.model.FieldDescriptor"
                    }
                ],
                "hexagonalView": {
                    "height": 0,
                    "id": "c763f4a6-b0e9-0a7e-e343-c8de448157bd",
                    "style": "{}",
                    "width": 0,
                    "x": 0,
                    "y": 0,
                    "_type": "org.uengine.modeling.model.EventHexagonal"
                },
                "name": "BookStatusChanged",
                "displayName": "도서 상태 변경됨",
                "nameCamelCase": "bookStatusChanged",
                "namePascalCase": "BookStatusChanged",
                "namePlural": "",
                "relationCommandInfo": [],
                "relationPolicyInfo": [],
                "rotateStatus": False,
                "selected": False,
                "trigger": "@PostPersist",
                "_type": "org.uengine.modeling.model.Event",
                "aggregate": {
                    "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                },
                "boundedContext": {
                    "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                }
            },
            "bdad54b2-d2ba-9e60-f28e-4959a9d55f42": {
                "alertURL": "/static/image/symbol/alert-icon.png",
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "checkAlert": True,
                "description": None,
                "id": "bdad54b2-d2ba-9e60-f28e-4959a9d55f42",
                "elementView": {
                    "angle": 0,
                    "height": 116,
                    "id": "bdad54b2-d2ba-9e60-f28e-4959a9d55f42",
                    "style": "{}",
                    "width": 100,
                    "x": 744,
                    "y": 510,
                    "_type": "org.uengine.modeling.model.Event"
                },
                "fieldDescriptors": [
                    {
                        "className": "String",
                        "isCopy": False,
                        "isKey": True,
                        "name": "ISBN",
                        "nameCamelCase": "isbn",
                        "namePascalCase": "Isbn",
                        "displayName": "",
                        "_type": "org.uengine.model.FieldDescriptor"
                    },
                    {
                        "className": "String",
                        "isCopy": False,
                        "isKey": False,
                        "name": "discardReason",
                        "nameCamelCase": "discardReason",
                        "namePascalCase": "DiscardReason",
                        "displayName": "",
                        "_type": "org.uengine.model.FieldDescriptor"
                    },
                    {
                        "className": "Date",
                        "isCopy": False,
                        "isKey": False,
                        "name": "discardedAt",
                        "nameCamelCase": "discardedAt",
                        "namePascalCase": "DiscardedAt",
                        "displayName": "",
                        "_type": "org.uengine.model.FieldDescriptor"
                    }
                ],
                "hexagonalView": {
                    "height": 0,
                    "id": "bdad54b2-d2ba-9e60-f28e-4959a9d55f42",
                    "style": "{}",
                    "width": 0,
                    "x": 0,
                    "y": 0,
                    "_type": "org.uengine.modeling.model.EventHexagonal"
                },
                "name": "BookDiscarded",
                "displayName": "도서 폐기됨",
                "nameCamelCase": "bookDiscarded",
                "namePascalCase": "BookDiscarded",
                "namePlural": "",
                "relationCommandInfo": [],
                "relationPolicyInfo": [],
                "rotateStatus": False,
                "selected": False,
                "trigger": "@PostPersist",
                "_type": "org.uengine.modeling.model.Event",
                "aggregate": {
                    "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                },
                "boundedContext": {
                    "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                }
            },
            "9dfd77c4-7bb3-6a62-025d-633c63438cf6": {
                "_type": "org.uengine.modeling.model.Command",
                "outputEvents": [
                    "BookRegistered"
                ],
                "aggregate": {
                    "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                },
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "boundedContext": {
                    "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                },
                "controllerInfo": {
                    "apiPath": "registerbook",
                    "method": "POST",
                    "fullApiPath": ""
                },
                "fieldDescriptors": [
                    {
                        "className": "String",
                        "isCopy": False,
                        "isKey": True,
                        "name": "ISBN",
                        "nameCamelCase": "isbn",
                        "namePascalCase": "Isbn",
                        "displayName": "",
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
                        "_type": "org.uengine.model.FieldDescriptor"
                    }
                ],
                "description": None,
                "id": "9dfd77c4-7bb3-6a62-025d-633c63438cf6",
                "elementView": {
                    "_type": "org.uengine.modeling.model.Command",
                    "height": 116,
                    "id": "9dfd77c4-7bb3-6a62-025d-633c63438cf6",
                    "style": "{}",
                    "width": 100,
                    "x": 556,
                    "y": 250,
                    "z-index": 999
                },
                "hexagonalView": {
                    "_type": "org.uengine.modeling.model.CommandHexagonal",
                    "height": 0,
                    "id": "9dfd77c4-7bb3-6a62-025d-633c63438cf6",
                    "style": "{}",
                    "width": 0,
                    "x": 0,
                    "y": 0
                },
                "isRestRepository": False,
                "name": "RegisterBook",
                "displayName": "도서 등록",
                "nameCamelCase": "registerBook",
                "namePascalCase": "RegisterBook",
                "namePlural": "registerBooks",
                "relationCommandInfo": [],
                "relationEventInfo": [],
                "restRepositoryInfo": {
                    "method": "POST"
                },
                "rotateStatus": False,
                "selected": False,
                "trigger": "@PrePersist"
            },
            "279c5170-159b-2b0d-34fa-e2e42dd5e0a9": {
                "_type": "org.uengine.modeling.model.Command",
                "outputEvents": [
                    "BookStatusChanged"
                ],
                "aggregate": {
                    "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                },
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "boundedContext": {
                    "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                },
                "controllerInfo": {
                    "apiPath": "changebookstatus",
                    "method": "PUT",
                    "fullApiPath": ""
                },
                "fieldDescriptors": [
                    {
                        "className": "String",
                        "isCopy": False,
                        "isKey": True,
                        "name": "ISBN",
                        "nameCamelCase": "isbn",
                        "namePascalCase": "Isbn",
                        "displayName": "",
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
                        "_type": "org.uengine.model.FieldDescriptor"
                    },
                    {
                        "className": "String",
                        "isCopy": False,
                        "isKey": False,
                        "name": "reason",
                        "nameCamelCase": "reason",
                        "namePascalCase": "Reason",
                        "displayName": "",
                        "_type": "org.uengine.model.FieldDescriptor"
                    }
                ],
                "description": None,
                "id": "279c5170-159b-2b0d-34fa-e2e42dd5e0a9",
                "elementView": {
                    "_type": "org.uengine.modeling.model.Command",
                    "height": 116,
                    "id": "279c5170-159b-2b0d-34fa-e2e42dd5e0a9",
                    "style": "{}",
                    "width": 100,
                    "x": 556,
                    "y": 380,
                    "z-index": 999
                },
                "hexagonalView": {
                    "_type": "org.uengine.modeling.model.CommandHexagonal",
                    "height": 0,
                    "id": "279c5170-159b-2b0d-34fa-e2e42dd5e0a9",
                    "style": "{}",
                    "width": 0,
                    "x": 0,
                    "y": 0
                },
                "isRestRepository": False,
                "name": "ChangeBookStatus",
                "displayName": "도서 상태 변경",
                "nameCamelCase": "changeBookStatus",
                "namePascalCase": "ChangeBookStatus",
                "namePlural": "changeBookStatuses",
                "relationCommandInfo": [],
                "relationEventInfo": [],
                "restRepositoryInfo": {
                    "method": "PUT"
                },
                "rotateStatus": False,
                "selected": False,
                "trigger": "@PrePersist"
            },
            "b6d57c04-edb1-c660-ea90-b0ef48b57dd1": {
                "_type": "org.uengine.modeling.model.Command",
                "outputEvents": [
                    "BookDiscarded"
                ],
                "aggregate": {
                    "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                },
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "boundedContext": {
                    "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                },
                "controllerInfo": {
                    "apiPath": "discardbook",
                    "method": "PUT",
                    "fullApiPath": ""
                },
                "fieldDescriptors": [
                    {
                        "className": "String",
                        "isCopy": False,
                        "isKey": True,
                        "name": "ISBN",
                        "nameCamelCase": "isbn",
                        "namePascalCase": "Isbn",
                        "displayName": "",
                        "_type": "org.uengine.model.FieldDescriptor"
                    },
                    {
                        "className": "String",
                        "isCopy": False,
                        "isKey": False,
                        "name": "discardReason",
                        "nameCamelCase": "discardReason",
                        "namePascalCase": "DiscardReason",
                        "displayName": "",
                        "_type": "org.uengine.model.FieldDescriptor"
                    }
                ],
                "description": None,
                "id": "b6d57c04-edb1-c660-ea90-b0ef48b57dd1",
                "elementView": {
                    "_type": "org.uengine.modeling.model.Command",
                    "height": 116,
                    "id": "b6d57c04-edb1-c660-ea90-b0ef48b57dd1",
                    "style": "{}",
                    "width": 100,
                    "x": 556,
                    "y": 510,
                    "z-index": 999
                },
                "hexagonalView": {
                    "_type": "org.uengine.modeling.model.CommandHexagonal",
                    "height": 0,
                    "id": "b6d57c04-edb1-c660-ea90-b0ef48b57dd1",
                    "style": "{}",
                    "width": 0,
                    "x": 0,
                    "y": 0
                },
                "isRestRepository": False,
                "name": "DiscardBook",
                "displayName": "도서 폐기",
                "nameCamelCase": "discardBook",
                "namePascalCase": "DiscardBook",
                "namePlural": "discardBooks",
                "relationCommandInfo": [],
                "relationEventInfo": [],
                "restRepositoryInfo": {
                    "method": "PUT"
                },
                "rotateStatus": False,
                "selected": False,
                "trigger": "@PrePersist"
            },
            "76fa37dc-33e3-9cb1-a9e6-90695b09cb40": {
                "_type": "org.uengine.modeling.model.View",
                "id": "76fa37dc-33e3-9cb1-a9e6-90695b09cb40",
                "visibility": "public",
                "name": "BookList",
                "oldName": "",
                "displayName": "도서 목록",
                "namePascalCase": "BookList",
                "namePlural": "bookLists",
                "aggregate": {
                    "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                },
                "description": None,
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "boundedContext": {
                    "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                },
                "fieldDescriptors": [
                    {
                        "_type": "org.uengine.model.FieldDescriptor",
                        "name": "id",
                        "className": "Long",
                        "nameCamelCase": "id",
                        "namePascalCase": "Id",
                        "isKey": True
                    }
                ],
                "queryParameters": [
                    {
                        "className": "Category",
                        "isCopy": False,
                        "isKey": False,
                        "name": "category",
                        "nameCamelCase": "category",
                        "namePascalCase": "Category",
                        "displayName": "",
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
                        "_type": "org.uengine.model.FieldDescriptor"
                    }
                ],
                "queryOption": {
                    "apiPath": "",
                    "useDefaultUri": True,
                    "multipleResult": True
                },
                "controllerInfo": {
                    "url": ""
                },
                "elementView": {
                    "_type": "org.uengine.modeling.model.View",
                    "id": "76fa37dc-33e3-9cb1-a9e6-90695b09cb40",
                    "x": 556,
                    "y": 640,
                    "width": 100,
                    "height": 116,
                    "style": "{}",
                    "z-index": 999
                },
                "editingView": False,
                "dataProjection": "query-for-aggregate",
                "createRules": [
                    {
                        "_type": "viewStoreRule",
                        "operation": "CREATE",
                        "when": None,
                        "fieldMapping": [
                            {
                                "viewField": None,
                                "eventField": None,
                                "operator": "="
                            }
                        ],
                        "where": [
                            {
                                "viewField": None,
                                "eventField": None
                            }
                        ]
                    }
                ],
                "updateRules": [
                    {
                        "_type": "viewStoreRule",
                        "operation": "UPDATE",
                        "when": None,
                        "fieldMapping": [
                            {
                                "viewField": None,
                                "eventField": None,
                                "operator": "="
                            }
                        ],
                        "where": [
                            {
                                "viewField": None,
                                "eventField": None
                            }
                        ]
                    }
                ],
                "deleteRules": [
                    {
                        "_type": "viewStoreRule",
                        "operation": "DELETE",
                        "when": None,
                        "fieldMapping": [
                            {
                                "viewField": None,
                                "eventField": None
                            }
                        ],
                        "where": [
                            {
                                "viewField": None,
                                "eventField": None
                            }
                        ]
                    }
                ],
                "rotateStatus": False,
                "definitionId": ""
            },
            "cec595c2-bb4c-e116-de82-b514c8d38926": {
                "_type": "org.uengine.modeling.model.View",
                "id": "cec595c2-bb4c-e116-de82-b514c8d38926",
                "visibility": "public",
                "name": "BookDetails",
                "oldName": "",
                "displayName": "도서 상세정보",
                "namePascalCase": "BookDetails",
                "namePlural": "bookDetails",
                "aggregate": {
                    "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                },
                "description": None,
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "boundedContext": {
                    "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                },
                "fieldDescriptors": [
                    {
                        "_type": "org.uengine.model.FieldDescriptor",
                        "name": "id",
                        "className": "Long",
                        "nameCamelCase": "id",
                        "namePascalCase": "Id",
                        "isKey": True
                    }
                ],
                "queryParameters": [
                    {
                        "className": "String",
                        "isCopy": False,
                        "isKey": True,
                        "name": "ISBN",
                        "nameCamelCase": "isbn",
                        "namePascalCase": "Isbn",
                        "displayName": "",
                        "_type": "org.uengine.model.FieldDescriptor"
                    }
                ],
                "queryOption": {
                    "apiPath": "",
                    "useDefaultUri": True,
                    "multipleResult": False
                },
                "controllerInfo": {
                    "url": ""
                },
                "elementView": {
                    "_type": "org.uengine.modeling.model.View",
                    "id": "cec595c2-bb4c-e116-de82-b514c8d38926",
                    "x": 556,
                    "y": 770,
                    "width": 100,
                    "height": 116,
                    "style": "{}",
                    "z-index": 999
                },
                "editingView": False,
                "dataProjection": "query-for-aggregate",
                "createRules": [
                    {
                        "_type": "viewStoreRule",
                        "operation": "CREATE",
                        "when": None,
                        "fieldMapping": [
                            {
                                "viewField": None,
                                "eventField": None,
                                "operator": "="
                            }
                        ],
                        "where": [
                            {
                                "viewField": None,
                                "eventField": None
                            }
                        ]
                    }
                ],
                "updateRules": [
                    {
                        "_type": "viewStoreRule",
                        "operation": "UPDATE",
                        "when": None,
                        "fieldMapping": [
                            {
                                "viewField": None,
                                "eventField": None,
                                "operator": "="
                            }
                        ],
                        "where": [
                            {
                                "viewField": None,
                                "eventField": None
                            }
                        ]
                    }
                ],
                "deleteRules": [
                    {
                        "_type": "viewStoreRule",
                        "operation": "DELETE",
                        "when": None,
                        "fieldMapping": [
                            {
                                "viewField": None,
                                "eventField": None
                            }
                        ],
                        "where": [
                            {
                                "viewField": None,
                                "eventField": None
                            }
                        ]
                    }
                ],
                "rotateStatus": False,
                "definitionId": ""
            },
            "48266e6a-49b8-a87b-10d3-ba1702401d61": {
                "_type": "org.uengine.modeling.model.Actor",
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "boundedContext": {
                    "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                },
                "description": None,
                "id": "48266e6a-49b8-a87b-10d3-ba1702401d61",
                "elementView": {
                    "_type": "org.uengine.modeling.model.Actor",
                    "height": 100,
                    "id": "48266e6a-49b8-a87b-10d3-ba1702401d61",
                    "style": "{}",
                    "width": 100,
                    "x": 475,
                    "y": 250
                },
                "innerAggregate": {
                    "command": [],
                    "event": [],
                    "external": [],
                    "policy": [],
                    "view": []
                },
                "name": "사용자",
                "oldName": "",
                "rotateStatus": False
            },
            "39998ac0-1667-efba-4c66-936c1c7827ae": {
                "_type": "org.uengine.modeling.model.Actor",
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "boundedContext": {
                    "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                },
                "description": None,
                "id": "39998ac0-1667-efba-4c66-936c1c7827ae",
                "elementView": {
                    "_type": "org.uengine.modeling.model.Actor",
                    "height": 100,
                    "id": "39998ac0-1667-efba-4c66-936c1c7827ae",
                    "style": "{}",
                    "width": 100,
                    "x": 475,
                    "y": 380
                },
                "innerAggregate": {
                    "command": [],
                    "event": [],
                    "external": [],
                    "policy": [],
                    "view": []
                },
                "name": "사용자",
                "oldName": "",
                "rotateStatus": False
            },
            "14f9b8d9-e377-cec8-c1b5-45cd402bfad7": {
                "_type": "org.uengine.modeling.model.Actor",
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "boundedContext": {
                    "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                },
                "description": None,
                "id": "14f9b8d9-e377-cec8-c1b5-45cd402bfad7",
                "elementView": {
                    "_type": "org.uengine.modeling.model.Actor",
                    "height": 100,
                    "id": "14f9b8d9-e377-cec8-c1b5-45cd402bfad7",
                    "style": "{}",
                    "width": 100,
                    "x": 475,
                    "y": 510
                },
                "innerAggregate": {
                    "command": [],
                    "event": [],
                    "external": [],
                    "policy": [],
                    "view": []
                },
                "name": "사용자",
                "oldName": "",
                "rotateStatus": False
            },
            "c4db0e92-3b28-e623-3a23-a8403a3ddff7": {
                "_type": "org.uengine.modeling.model.Actor",
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "boundedContext": {
                    "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                },
                "description": None,
                "id": "c4db0e92-3b28-e623-3a23-a8403a3ddff7",
                "elementView": {
                    "_type": "org.uengine.modeling.model.Actor",
                    "height": 100,
                    "id": "c4db0e92-3b28-e623-3a23-a8403a3ddff7",
                    "style": "{}",
                    "width": 100,
                    "x": 475,
                    "y": 640
                },
                "innerAggregate": {
                    "command": [],
                    "event": [],
                    "external": [],
                    "policy": [],
                    "view": []
                },
                "name": "사용자",
                "oldName": "",
                "rotateStatus": False,
                "displayName": ""
            },
            "5a6c7a17-38f7-5f5a-23c5-11c2dd454202": {
                "_type": "org.uengine.modeling.model.Actor",
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "boundedContext": {
                    "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                },
                "description": None,
                "id": "5a6c7a17-38f7-5f5a-23c5-11c2dd454202",
                "elementView": {
                    "_type": "org.uengine.modeling.model.Actor",
                    "height": 100,
                    "id": "5a6c7a17-38f7-5f5a-23c5-11c2dd454202",
                    "style": "{}",
                    "width": 100,
                    "x": 475,
                    "y": 770
                },
                "innerAggregate": {
                    "command": [],
                    "event": [],
                    "external": [],
                    "policy": [],
                    "view": []
                },
                "name": "사용자",
                "oldName": "",
                "rotateStatus": False,
                "displayName": ""
            },
            "b12ad8fd-6404-c544-5ff8-b5bc1fdcae20": {
                "alertURL": "/static/image/symbol/alert-icon.png",
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "checkAlert": True,
                "description": None,
                "id": "b12ad8fd-6404-c544-5ff8-b5bc1fdcae20",
                "elementView": {
                    "angle": 0,
                    "height": 116,
                    "id": "b12ad8fd-6404-c544-5ff8-b5bc1fdcae20",
                    "style": "{}",
                    "width": 100,
                    "x": 1329,
                    "y": 250,
                    "_type": "org.uengine.modeling.model.Event"
                },
                "fieldDescriptors": [
                    {
                        "className": "String",
                        "isCopy": False,
                        "isKey": True,
                        "name": "loanId",
                        "nameCamelCase": "loanId",
                        "namePascalCase": "LoanId",
                        "displayName": "",
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
                        "_type": "org.uengine.model.FieldDescriptor"
                    }
                ],
                "hexagonalView": {
                    "height": 0,
                    "id": "b12ad8fd-6404-c544-5ff8-b5bc1fdcae20",
                    "style": "{}",
                    "width": 0,
                    "x": 0,
                    "y": 0,
                    "_type": "org.uengine.modeling.model.EventHexagonal"
                },
                "name": "Loaned",
                "displayName": "도서 대출 완료",
                "nameCamelCase": "loaned",
                "namePascalCase": "Loaned",
                "namePlural": "",
                "relationCommandInfo": [],
                "relationPolicyInfo": [],
                "rotateStatus": False,
                "selected": False,
                "trigger": "@PostPersist",
                "_type": "org.uengine.modeling.model.Event",
                "aggregate": {
                    "id": "30176142-717c-cc1a-0d59-771539ac988a"
                },
                "boundedContext": {
                    "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                }
            },
            "7134ee93-d752-ba68-bcd8-c39788567f0f": {
                "alertURL": "/static/image/symbol/alert-icon.png",
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "checkAlert": True,
                "description": None,
                "id": "7134ee93-d752-ba68-bcd8-c39788567f0f",
                "elementView": {
                    "angle": 0,
                    "height": 116,
                    "id": "7134ee93-d752-ba68-bcd8-c39788567f0f",
                    "style": "{}",
                    "width": 100,
                    "x": 1329,
                    "y": 380,
                    "_type": "org.uengine.modeling.model.Event"
                },
                "fieldDescriptors": [
                    {
                        "className": "String",
                        "isCopy": False,
                        "isKey": True,
                        "name": "loanId",
                        "nameCamelCase": "loanId",
                        "namePascalCase": "LoanId",
                        "displayName": "",
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
                        "_type": "org.uengine.model.FieldDescriptor"
                    },
                    {
                        "className": "Date",
                        "isCopy": False,
                        "isKey": False,
                        "name": "returnedDate",
                        "nameCamelCase": "returnedDate",
                        "namePascalCase": "ReturnedDate",
                        "displayName": "",
                        "_type": "org.uengine.model.FieldDescriptor"
                    }
                ],
                "hexagonalView": {
                    "height": 0,
                    "id": "7134ee93-d752-ba68-bcd8-c39788567f0f",
                    "style": "{}",
                    "width": 0,
                    "x": 0,
                    "y": 0,
                    "_type": "org.uengine.modeling.model.EventHexagonal"
                },
                "name": "Returned",
                "displayName": "도서 반납 완료",
                "nameCamelCase": "returned",
                "namePascalCase": "Returned",
                "namePlural": "",
                "relationCommandInfo": [],
                "relationPolicyInfo": [],
                "rotateStatus": False,
                "selected": False,
                "trigger": "@PostPersist",
                "_type": "org.uengine.modeling.model.Event",
                "aggregate": {
                    "id": "30176142-717c-cc1a-0d59-771539ac988a"
                },
                "boundedContext": {
                    "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                }
            },
            "e5cb69a8-8001-cf81-d4da-fffd1401afe5": {
                "alertURL": "/static/image/symbol/alert-icon.png",
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "checkAlert": True,
                "description": None,
                "id": "e5cb69a8-8001-cf81-d4da-fffd1401afe5",
                "elementView": {
                    "angle": 0,
                    "height": 116,
                    "id": "e5cb69a8-8001-cf81-d4da-fffd1401afe5",
                    "style": "{}",
                    "width": 100,
                    "x": 1329,
                    "y": 510,
                    "_type": "org.uengine.modeling.model.Event"
                },
                "fieldDescriptors": [
                    {
                        "className": "String",
                        "isCopy": False,
                        "isKey": True,
                        "name": "reservationId",
                        "nameCamelCase": "reservationId",
                        "namePascalCase": "ReservationId",
                        "displayName": "",
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
                        "_type": "org.uengine.model.FieldDescriptor"
                    },
                    {
                        "className": "Date",
                        "isCopy": False,
                        "isKey": False,
                        "name": "reservedDate",
                        "nameCamelCase": "reservedDate",
                        "namePascalCase": "ReservedDate",
                        "displayName": "",
                        "_type": "org.uengine.model.FieldDescriptor"
                    }
                ],
                "hexagonalView": {
                    "height": 0,
                    "id": "e5cb69a8-8001-cf81-d4da-fffd1401afe5",
                    "style": "{}",
                    "width": 0,
                    "x": 0,
                    "y": 0,
                    "_type": "org.uengine.modeling.model.EventHexagonal"
                },
                "name": "Reserved",
                "displayName": "도서 예약 완료",
                "nameCamelCase": "reserved",
                "namePascalCase": "Reserved",
                "namePlural": "",
                "relationCommandInfo": [],
                "relationPolicyInfo": [],
                "rotateStatus": False,
                "selected": False,
                "trigger": "@PostPersist",
                "_type": "org.uengine.modeling.model.Event",
                "aggregate": {
                    "id": "30176142-717c-cc1a-0d59-771539ac988a"
                },
                "boundedContext": {
                    "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                }
            },
            "7a421b31-a5ff-c17c-076f-a700e59be8fd": {
                "_type": "org.uengine.modeling.model.Command",
                "outputEvents": [
                    "Loaned"
                ],
                "aggregate": {
                    "id": "30176142-717c-cc1a-0d59-771539ac988a"
                },
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "boundedContext": {
                    "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                },
                "controllerInfo": {
                    "apiPath": "loanbook",
                    "method": "POST",
                    "fullApiPath": ""
                },
                "fieldDescriptors": [
                    {
                        "className": "String",
                        "isCopy": False,
                        "isKey": True,
                        "name": "memberNumber",
                        "nameCamelCase": "memberNumber",
                        "namePascalCase": "MemberNumber",
                        "displayName": "",
                        "_type": "org.uengine.model.FieldDescriptor"
                    },
                    {
                        "className": "String",
                        "isCopy": False,
                        "isKey": False,
                        "name": "memberName",
                        "nameCamelCase": "memberName",
                        "namePascalCase": "MemberName",
                        "displayName": "",
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
                        "_type": "org.uengine.model.FieldDescriptor"
                    }
                ],
                "description": None,
                "id": "7a421b31-a5ff-c17c-076f-a700e59be8fd",
                "elementView": {
                    "_type": "org.uengine.modeling.model.Command",
                    "height": 116,
                    "id": "7a421b31-a5ff-c17c-076f-a700e59be8fd",
                    "style": "{}",
                    "width": 100,
                    "x": 1141,
                    "y": 250,
                    "z-index": 999
                },
                "hexagonalView": {
                    "_type": "org.uengine.modeling.model.CommandHexagonal",
                    "height": 0,
                    "id": "7a421b31-a5ff-c17c-076f-a700e59be8fd",
                    "style": "{}",
                    "width": 0,
                    "x": 0,
                    "y": 0
                },
                "isRestRepository": False,
                "name": "LoanBook",
                "displayName": "도서 대출 신청",
                "nameCamelCase": "loanBook",
                "namePascalCase": "LoanBook",
                "namePlural": "loanBooks",
                "relationCommandInfo": [],
                "relationEventInfo": [],
                "restRepositoryInfo": {
                    "method": "POST"
                },
                "rotateStatus": False,
                "selected": False,
                "trigger": "@PrePersist"
            },
            "621d4bda-16fd-1bda-d837-89991959fbb2": {
                "_type": "org.uengine.modeling.model.Command",
                "outputEvents": [
                    "Returned"
                ],
                "aggregate": {
                    "id": "30176142-717c-cc1a-0d59-771539ac988a"
                },
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "boundedContext": {
                    "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                },
                "controllerInfo": {
                    "apiPath": "returnbook",
                    "method": "POST",
                    "fullApiPath": ""
                },
                "fieldDescriptors": [
                    {
                        "className": "String",
                        "isCopy": False,
                        "isKey": True,
                        "name": "loanId",
                        "nameCamelCase": "loanId",
                        "namePascalCase": "LoanId",
                        "displayName": "",
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
                        "_type": "org.uengine.model.FieldDescriptor"
                    }
                ],
                "description": None,
                "id": "621d4bda-16fd-1bda-d837-89991959fbb2",
                "elementView": {
                    "_type": "org.uengine.modeling.model.Command",
                    "height": 116,
                    "id": "621d4bda-16fd-1bda-d837-89991959fbb2",
                    "style": "{}",
                    "width": 100,
                    "x": 1141,
                    "y": 380,
                    "z-index": 999
                },
                "hexagonalView": {
                    "_type": "org.uengine.modeling.model.CommandHexagonal",
                    "height": 0,
                    "id": "621d4bda-16fd-1bda-d837-89991959fbb2",
                    "style": "{}",
                    "width": 0,
                    "x": 0,
                    "y": 0
                },
                "isRestRepository": False,
                "name": "ReturnBook",
                "displayName": "도서 반납 처리",
                "nameCamelCase": "returnBook",
                "namePascalCase": "ReturnBook",
                "namePlural": "returnBooks",
                "relationCommandInfo": [],
                "relationEventInfo": [],
                "restRepositoryInfo": {
                    "method": "POST"
                },
                "rotateStatus": False,
                "selected": False,
                "trigger": "@PrePersist"
            },
            "e9506a41-7406-7ded-e91a-81c2dd99da75": {
                "_type": "org.uengine.modeling.model.Command",
                "outputEvents": [
                    "Reserved"
                ],
                "aggregate": {
                    "id": "30176142-717c-cc1a-0d59-771539ac988a"
                },
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "boundedContext": {
                    "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                },
                "controllerInfo": {
                    "apiPath": "reservebook",
                    "method": "POST",
                    "fullApiPath": ""
                },
                "fieldDescriptors": [
                    {
                        "className": "String",
                        "isCopy": False,
                        "isKey": True,
                        "name": "memberNumber",
                        "nameCamelCase": "memberNumber",
                        "namePascalCase": "MemberNumber",
                        "displayName": "",
                        "_type": "org.uengine.model.FieldDescriptor"
                    },
                    {
                        "className": "String",
                        "isCopy": False,
                        "isKey": False,
                        "name": "memberName",
                        "nameCamelCase": "memberName",
                        "namePascalCase": "MemberName",
                        "displayName": "",
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
                        "_type": "org.uengine.model.FieldDescriptor"
                    }
                ],
                "description": None,
                "id": "e9506a41-7406-7ded-e91a-81c2dd99da75",
                "elementView": {
                    "_type": "org.uengine.modeling.model.Command",
                    "height": 116,
                    "id": "e9506a41-7406-7ded-e91a-81c2dd99da75",
                    "style": "{}",
                    "width": 100,
                    "x": 1141,
                    "y": 510,
                    "z-index": 999
                },
                "hexagonalView": {
                    "_type": "org.uengine.modeling.model.CommandHexagonal",
                    "height": 0,
                    "id": "e9506a41-7406-7ded-e91a-81c2dd99da75",
                    "style": "{}",
                    "width": 0,
                    "x": 0,
                    "y": 0
                },
                "isRestRepository": False,
                "name": "ReserveBook",
                "displayName": "도서 예약 신청",
                "nameCamelCase": "reserveBook",
                "namePascalCase": "ReserveBook",
                "namePlural": "reserveBooks",
                "relationCommandInfo": [],
                "relationEventInfo": [],
                "restRepositoryInfo": {
                    "method": "POST"
                },
                "rotateStatus": False,
                "selected": False,
                "trigger": "@PrePersist"
            },
            "692ff79a-552f-1049-965c-f6c780405f7a": {
                "_type": "org.uengine.modeling.model.View",
                "id": "692ff79a-552f-1049-965c-f6c780405f7a",
                "visibility": "public",
                "name": "LoanHistory",
                "oldName": "",
                "displayName": "대출/반납/예약 이력 조회",
                "namePascalCase": "LoanHistory",
                "namePlural": "loanHistories",
                "aggregate": {
                    "id": "30176142-717c-cc1a-0d59-771539ac988a"
                },
                "description": None,
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "boundedContext": {
                    "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                },
                "fieldDescriptors": [
                    {
                        "_type": "org.uengine.model.FieldDescriptor",
                        "name": "id",
                        "className": "Long",
                        "nameCamelCase": "id",
                        "namePascalCase": "Id",
                        "isKey": True
                    }
                ],
                "queryParameters": [
                    {
                        "className": "String",
                        "isCopy": False,
                        "isKey": True,
                        "name": "memberNumber",
                        "nameCamelCase": "memberNumber",
                        "namePascalCase": "MemberNumber",
                        "displayName": "",
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
                        "_type": "org.uengine.model.FieldDescriptor"
                    }
                ],
                "queryOption": {
                    "apiPath": "",
                    "useDefaultUri": True,
                    "multipleResult": True
                },
                "controllerInfo": {
                    "url": ""
                },
                "elementView": {
                    "_type": "org.uengine.modeling.model.View",
                    "id": "692ff79a-552f-1049-965c-f6c780405f7a",
                    "x": 1141,
                    "y": 640,
                    "width": 100,
                    "height": 116,
                    "style": "{}",
                    "z-index": 999
                },
                "editingView": False,
                "dataProjection": "query-for-aggregate",
                "createRules": [
                    {
                        "_type": "viewStoreRule",
                        "operation": "CREATE",
                        "when": None,
                        "fieldMapping": [
                            {
                                "viewField": None,
                                "eventField": None,
                                "operator": "="
                            }
                        ],
                        "where": [
                            {
                                "viewField": None,
                                "eventField": None
                            }
                        ]
                    }
                ],
                "updateRules": [
                    {
                        "_type": "viewStoreRule",
                        "operation": "UPDATE",
                        "when": None,
                        "fieldMapping": [
                            {
                                "viewField": None,
                                "eventField": None,
                                "operator": "="
                            }
                        ],
                        "where": [
                            {
                                "viewField": None,
                                "eventField": None
                            }
                        ]
                    }
                ],
                "deleteRules": [
                    {
                        "_type": "viewStoreRule",
                        "operation": "DELETE",
                        "when": None,
                        "fieldMapping": [
                            {
                                "viewField": None,
                                "eventField": None
                            }
                        ],
                        "where": [
                            {
                                "viewField": None,
                                "eventField": None
                            }
                        ]
                    }
                ],
                "rotateStatus": False,
                "definitionId": ""
            },
            "de913c2b-ea86-6d51-9b46-f66a42712964": {
                "_type": "org.uengine.modeling.model.View",
                "id": "de913c2b-ea86-6d51-9b46-f66a42712964",
                "visibility": "public",
                "name": "LoanCurrentStatus",
                "oldName": "",
                "displayName": "회원별 대출 현황",
                "namePascalCase": "LoanCurrentStatus",
                "namePlural": "loanCurrentStatuses",
                "aggregate": {
                    "id": "30176142-717c-cc1a-0d59-771539ac988a"
                },
                "description": None,
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "boundedContext": {
                    "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                },
                "fieldDescriptors": [
                    {
                        "_type": "org.uengine.model.FieldDescriptor",
                        "name": "id",
                        "className": "Long",
                        "nameCamelCase": "id",
                        "namePascalCase": "Id",
                        "isKey": True
                    }
                ],
                "queryParameters": [
                    {
                        "className": "String",
                        "isCopy": False,
                        "isKey": True,
                        "name": "memberNumber",
                        "nameCamelCase": "memberNumber",
                        "namePascalCase": "MemberNumber",
                        "displayName": "",
                        "_type": "org.uengine.model.FieldDescriptor"
                    }
                ],
                "queryOption": {
                    "apiPath": "",
                    "useDefaultUri": True,
                    "multipleResult": True
                },
                "controllerInfo": {
                    "url": ""
                },
                "elementView": {
                    "_type": "org.uengine.modeling.model.View",
                    "id": "de913c2b-ea86-6d51-9b46-f66a42712964",
                    "x": 1141,
                    "y": 770,
                    "width": 100,
                    "height": 116,
                    "style": "{}",
                    "z-index": 999
                },
                "editingView": False,
                "dataProjection": "query-for-aggregate",
                "createRules": [
                    {
                        "_type": "viewStoreRule",
                        "operation": "CREATE",
                        "when": None,
                        "fieldMapping": [
                            {
                                "viewField": None,
                                "eventField": None,
                                "operator": "="
                            }
                        ],
                        "where": [
                            {
                                "viewField": None,
                                "eventField": None
                            }
                        ]
                    }
                ],
                "updateRules": [
                    {
                        "_type": "viewStoreRule",
                        "operation": "UPDATE",
                        "when": None,
                        "fieldMapping": [
                            {
                                "viewField": None,
                                "eventField": None,
                                "operator": "="
                            }
                        ],
                        "where": [
                            {
                                "viewField": None,
                                "eventField": None
                            }
                        ]
                    }
                ],
                "deleteRules": [
                    {
                        "_type": "viewStoreRule",
                        "operation": "DELETE",
                        "when": None,
                        "fieldMapping": [
                            {
                                "viewField": None,
                                "eventField": None
                            }
                        ],
                        "where": [
                            {
                                "viewField": None,
                                "eventField": None
                            }
                        ]
                    }
                ],
                "rotateStatus": False,
                "definitionId": ""
            },
            "4eee8a0f-e72d-24b4-ae8f-e2493a1da402": {
                "_type": "org.uengine.modeling.model.Actor",
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "boundedContext": {
                    "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                },
                "description": None,
                "id": "4eee8a0f-e72d-24b4-ae8f-e2493a1da402",
                "elementView": {
                    "_type": "org.uengine.modeling.model.Actor",
                    "height": 100,
                    "id": "4eee8a0f-e72d-24b4-ae8f-e2493a1da402",
                    "style": "{}",
                    "width": 100,
                    "x": 1060,
                    "y": 250
                },
                "innerAggregate": {
                    "command": [],
                    "event": [],
                    "external": [],
                    "policy": [],
                    "view": []
                },
                "name": "사용자",
                "oldName": "",
                "rotateStatus": False
            },
            "11a22b70-9ac7-bbf2-66b1-60647ca80752": {
                "_type": "org.uengine.modeling.model.Actor",
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "boundedContext": {
                    "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                },
                "description": None,
                "id": "11a22b70-9ac7-bbf2-66b1-60647ca80752",
                "elementView": {
                    "_type": "org.uengine.modeling.model.Actor",
                    "height": 100,
                    "id": "11a22b70-9ac7-bbf2-66b1-60647ca80752",
                    "style": "{}",
                    "width": 100,
                    "x": 1060,
                    "y": 380
                },
                "innerAggregate": {
                    "command": [],
                    "event": [],
                    "external": [],
                    "policy": [],
                    "view": []
                },
                "name": "사용자",
                "oldName": "",
                "rotateStatus": False
            },
            "1a0d724e-ff36-0fe6-4887-b34b87958b31": {
                "_type": "org.uengine.modeling.model.Actor",
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "boundedContext": {
                    "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                },
                "description": None,
                "id": "1a0d724e-ff36-0fe6-4887-b34b87958b31",
                "elementView": {
                    "_type": "org.uengine.modeling.model.Actor",
                    "height": 100,
                    "id": "1a0d724e-ff36-0fe6-4887-b34b87958b31",
                    "style": "{}",
                    "width": 100,
                    "x": 1060,
                    "y": 510
                },
                "innerAggregate": {
                    "command": [],
                    "event": [],
                    "external": [],
                    "policy": [],
                    "view": []
                },
                "name": "사용자",
                "oldName": "",
                "rotateStatus": False
            },
            "d889f16d-4519-6b8a-7e56-f1dd4141235c": {
                "_type": "org.uengine.modeling.model.Actor",
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "boundedContext": {
                    "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                },
                "description": None,
                "id": "d889f16d-4519-6b8a-7e56-f1dd4141235c",
                "elementView": {
                    "_type": "org.uengine.modeling.model.Actor",
                    "height": 100,
                    "id": "d889f16d-4519-6b8a-7e56-f1dd4141235c",
                    "style": "{}",
                    "width": 100,
                    "x": 1060,
                    "y": 640
                },
                "innerAggregate": {
                    "command": [],
                    "event": [],
                    "external": [],
                    "policy": [],
                    "view": []
                },
                "name": "사용자",
                "oldName": "",
                "rotateStatus": False,
                "displayName": ""
            },
            "76c5c940-5d8a-b57e-9c93-49ded3868763": {
                "_type": "org.uengine.modeling.model.Actor",
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "boundedContext": {
                    "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                },
                "description": None,
                "id": "76c5c940-5d8a-b57e-9c93-49ded3868763",
                "elementView": {
                    "_type": "org.uengine.modeling.model.Actor",
                    "height": 100,
                    "id": "76c5c940-5d8a-b57e-9c93-49ded3868763",
                    "style": "{}",
                    "width": 100,
                    "x": 1060,
                    "y": 770
                },
                "innerAggregate": {
                    "command": [],
                    "event": [],
                    "external": [],
                    "policy": [],
                    "view": []
                },
                "name": "사용자",
                "oldName": "",
                "rotateStatus": False,
                "displayName": ""
            }
        },
        "relations": {
            "40fb55f4-95bf-4b7a-13a8-691f894d3429": {
                "_type": "org.uengine.modeling.model.Relation",
                "name": "",
                "id": "40fb55f4-95bf-4b7a-13a8-691f894d3429",
                "sourceElement": {
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
                                "19aa4d64-6084-e826-7c69-0bd1896e6f79": {
                                    "_type": "org.uengine.uml.model.Class",
                                    "id": "19aa4d64-6084-e826-7c69-0bd1896e6f79",
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
                                        "id": "19aa4d64-6084-e826-7c69-0bd1896e6f79",
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
                                    "parentId": "30176142-717c-cc1a-0d59-771539ac988a"
                                },
                                "7ec1a4ec-7237-ab46-0c52-fe21ca1a9a09": {
                                    "_type": "org.uengine.uml.model.enum",
                                    "id": "7ec1a4ec-7237-ab46-0c52-fe21ca1a9a09",
                                    "name": "TransactionType",
                                    "displayName": "거래 유형",
                                    "nameCamelCase": "transactionType",
                                    "namePascalCase": "TransactionType",
                                    "namePlural": "transactionTypes",
                                    "elementView": {
                                        "_type": "org.uengine.uml.model.enum",
                                        "id": "7ec1a4ec-7237-ab46-0c52-fe21ca1a9a09",
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
                        "name": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908",
                        "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                    },
                    "commands": [],
                    "description": None,
                    "id": "30176142-717c-cc1a-0d59-771539ac988a",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Aggregate",
                        "id": "30176142-717c-cc1a-0d59-771539ac988a",
                        "x": 1235,
                        "y": 450,
                        "width": 130,
                        "height": 400
                    },
                    "events": [],
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.AggregateHexagonal",
                        "id": "30176142-717c-cc1a-0d59-771539ac988a",
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
                },
                "targetElement": {
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
                                "aa6acc4d-3773-6aa9-3cf2-d22a860272a8": {
                                    "_type": "org.uengine.uml.model.Class",
                                    "id": "aa6acc4d-3773-6aa9-3cf2-d22a860272a8",
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
                                        "id": "aa6acc4d-3773-6aa9-3cf2-d22a860272a8",
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
                                    "parentId": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                                },
                                "3e68e3a2-7dd9-dab0-3d03-2753ba0a1233": {
                                    "_type": "org.uengine.uml.model.enum",
                                    "id": "3e68e3a2-7dd9-dab0-3d03-2753ba0a1233",
                                    "name": "Category",
                                    "displayName": "카테고리",
                                    "nameCamelCase": "category",
                                    "namePascalCase": "Category",
                                    "namePlural": "categories",
                                    "elementView": {
                                        "_type": "org.uengine.uml.model.enum",
                                        "id": "3e68e3a2-7dd9-dab0-3d03-2753ba0a1233",
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
                                "73640bd2-3239-18e6-0c05-22462730ed92": {
                                    "_type": "org.uengine.uml.model.enum",
                                    "id": "73640bd2-3239-18e6-0c05-22462730ed92",
                                    "name": "Status",
                                    "displayName": "도서상태",
                                    "nameCamelCase": "status",
                                    "namePascalCase": "Status",
                                    "namePlural": "statuses",
                                    "elementView": {
                                        "_type": "org.uengine.uml.model.enum",
                                        "id": "73640bd2-3239-18e6-0c05-22462730ed92",
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
                        "name": "97f2473e-7068-21ee-652d-ba0a8f41dd2c",
                        "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                    },
                    "commands": [],
                    "description": None,
                    "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Aggregate",
                        "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2",
                        "x": 650,
                        "y": 450,
                        "width": 130,
                        "height": 400
                    },
                    "events": [],
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.AggregateHexagonal",
                        "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2",
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
                "from": "30176142-717c-cc1a-0d59-771539ac988a",
                "to": "f81e4c75-040c-83ad-4656-65cfccc74cc2",
                "relationView": {
                    "id": "40fb55f4-95bf-4b7a-13a8-691f894d3429",
                    "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                    "from": "30176142-717c-cc1a-0d59-771539ac988a",
                    "to": "f81e4c75-040c-83ad-4656-65cfccc74cc2",
                    "needReconnect": True,
                    "value": "[[1170,456],[715,456]]"
                },
                "hexagonalView": {
                    "_type": "org.uengine.modeling.model.RelationHexagonal",
                    "from": "30176142-717c-cc1a-0d59-771539ac988a",
                    "id": "40fb55f4-95bf-4b7a-13a8-691f894d3429",
                    "needReconnect": True,
                    "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                    "to": "f81e4c75-040c-83ad-4656-65cfccc74cc2",
                    "value": None
                },
                "sourceMultiplicity": "1",
                "targetMultiplicity": "1",
                "displayName": ""
            },
            "73d6bd51-2b4d-5480-b155-7ed5bc740b4d": {
                "_type": "org.uengine.modeling.model.Relation",
                "name": "",
                "id": "73d6bd51-2b4d-5480-b155-7ed5bc740b4d",
                "sourceElement": {
                    "_type": "org.uengine.modeling.model.Command",
                    "outputEvents": [
                        "BookRegistered"
                    ],
                    "aggregate": {
                        "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                    },
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                    },
                    "controllerInfo": {
                        "apiPath": "registerbook",
                        "method": "POST",
                        "fullApiPath": ""
                    },
                    "fieldDescriptors": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "ISBN",
                            "nameCamelCase": "isbn",
                            "namePascalCase": "Isbn",
                            "displayName": "",
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
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "description": None,
                    "id": "9dfd77c4-7bb3-6a62-025d-633c63438cf6",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Command",
                        "height": 116,
                        "id": "9dfd77c4-7bb3-6a62-025d-633c63438cf6",
                        "style": "{}",
                        "width": 100,
                        "x": 556,
                        "y": 250,
                        "z-index": 999
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.CommandHexagonal",
                        "height": 0,
                        "id": "9dfd77c4-7bb3-6a62-025d-633c63438cf6",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0
                    },
                    "isRestRepository": False,
                    "name": "RegisterBook",
                    "displayName": "도서 등록",
                    "nameCamelCase": "registerBook",
                    "namePascalCase": "RegisterBook",
                    "namePlural": "registerBooks",
                    "relationCommandInfo": [],
                    "relationEventInfo": [],
                    "restRepositoryInfo": {
                        "method": "POST"
                    },
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PrePersist"
                },
                "targetElement": {
                    "alertURL": "/static/image/symbol/alert-icon.png",
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "checkAlert": True,
                    "description": None,
                    "id": "dc9f7be6-103e-0d9f-96b6-a1de4ae31d3f",
                    "elementView": {
                        "angle": 0,
                        "height": 116,
                        "id": "dc9f7be6-103e-0d9f-96b6-a1de4ae31d3f",
                        "style": "{}",
                        "width": 100,
                        "x": 744,
                        "y": 250,
                        "_type": "org.uengine.modeling.model.Event"
                    },
                    "fieldDescriptors": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "ISBN",
                            "nameCamelCase": "isbn",
                            "namePascalCase": "Isbn",
                            "displayName": "",
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
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "hexagonalView": {
                        "height": 0,
                        "id": "dc9f7be6-103e-0d9f-96b6-a1de4ae31d3f",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0,
                        "_type": "org.uengine.modeling.model.EventHexagonal"
                    },
                    "name": "BookRegistered",
                    "displayName": "도서 등록됨",
                    "nameCamelCase": "bookRegistered",
                    "namePascalCase": "BookRegistered",
                    "namePlural": "",
                    "relationCommandInfo": [],
                    "relationPolicyInfo": [],
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PostPersist",
                    "_type": "org.uengine.modeling.model.Event",
                    "aggregate": {
                        "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                    },
                    "boundedContext": {
                        "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                    }
                },
                "from": "9dfd77c4-7bb3-6a62-025d-633c63438cf6",
                "to": "dc9f7be6-103e-0d9f-96b6-a1de4ae31d3f",
                "relationView": {
                    "id": "73d6bd51-2b4d-5480-b155-7ed5bc740b4d",
                    "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                    "from": "9dfd77c4-7bb3-6a62-025d-633c63438cf6",
                    "to": "dc9f7be6-103e-0d9f-96b6-a1de4ae31d3f",
                    "needReconnect": True,
                    "value": "[[606,252],[694,252]]"
                },
                "hexagonalView": {
                    "_type": "org.uengine.modeling.model.RelationHexagonal",
                    "from": "9dfd77c4-7bb3-6a62-025d-633c63438cf6",
                    "id": "73d6bd51-2b4d-5480-b155-7ed5bc740b4d",
                    "needReconnect": True,
                    "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                    "to": "dc9f7be6-103e-0d9f-96b6-a1de4ae31d3f",
                    "value": None
                },
                "sourceMultiplicity": "1",
                "targetMultiplicity": "1"
            },
            "6f42b17c-7bd9-9117-931f-b86209dcb1a8": {
                "_type": "org.uengine.modeling.model.Relation",
                "name": "",
                "id": "6f42b17c-7bd9-9117-931f-b86209dcb1a8",
                "sourceElement": {
                    "_type": "org.uengine.modeling.model.Command",
                    "outputEvents": [
                        "BookStatusChanged"
                    ],
                    "aggregate": {
                        "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                    },
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                    },
                    "controllerInfo": {
                        "apiPath": "changebookstatus",
                        "method": "PUT",
                        "fullApiPath": ""
                    },
                    "fieldDescriptors": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "ISBN",
                            "nameCamelCase": "isbn",
                            "namePascalCase": "Isbn",
                            "displayName": "",
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
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": False,
                            "name": "reason",
                            "nameCamelCase": "reason",
                            "namePascalCase": "Reason",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "description": None,
                    "id": "279c5170-159b-2b0d-34fa-e2e42dd5e0a9",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Command",
                        "height": 116,
                        "id": "279c5170-159b-2b0d-34fa-e2e42dd5e0a9",
                        "style": "{}",
                        "width": 100,
                        "x": 556,
                        "y": 380,
                        "z-index": 999
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.CommandHexagonal",
                        "height": 0,
                        "id": "279c5170-159b-2b0d-34fa-e2e42dd5e0a9",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0
                    },
                    "isRestRepository": False,
                    "name": "ChangeBookStatus",
                    "displayName": "도서 상태 변경",
                    "nameCamelCase": "changeBookStatus",
                    "namePascalCase": "ChangeBookStatus",
                    "namePlural": "changeBookStatuses",
                    "relationCommandInfo": [],
                    "relationEventInfo": [],
                    "restRepositoryInfo": {
                        "method": "PUT"
                    },
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PrePersist"
                },
                "targetElement": {
                    "alertURL": "/static/image/symbol/alert-icon.png",
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "checkAlert": True,
                    "description": None,
                    "id": "c763f4a6-b0e9-0a7e-e343-c8de448157bd",
                    "elementView": {
                        "angle": 0,
                        "height": 116,
                        "id": "c763f4a6-b0e9-0a7e-e343-c8de448157bd",
                        "style": "{}",
                        "width": 100,
                        "x": 744,
                        "y": 380,
                        "_type": "org.uengine.modeling.model.Event"
                    },
                    "fieldDescriptors": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "ISBN",
                            "nameCamelCase": "isbn",
                            "namePascalCase": "Isbn",
                            "displayName": "",
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
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Date",
                            "isCopy": False,
                            "isKey": False,
                            "name": "changedAt",
                            "nameCamelCase": "changedAt",
                            "namePascalCase": "ChangedAt",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": False,
                            "name": "reason",
                            "nameCamelCase": "reason",
                            "namePascalCase": "Reason",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "hexagonalView": {
                        "height": 0,
                        "id": "c763f4a6-b0e9-0a7e-e343-c8de448157bd",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0,
                        "_type": "org.uengine.modeling.model.EventHexagonal"
                    },
                    "name": "BookStatusChanged",
                    "displayName": "도서 상태 변경됨",
                    "nameCamelCase": "bookStatusChanged",
                    "namePascalCase": "BookStatusChanged",
                    "namePlural": "",
                    "relationCommandInfo": [],
                    "relationPolicyInfo": [],
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PostPersist",
                    "_type": "org.uengine.modeling.model.Event",
                    "aggregate": {
                        "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                    },
                    "boundedContext": {
                        "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                    }
                },
                "from": "279c5170-159b-2b0d-34fa-e2e42dd5e0a9",
                "to": "c763f4a6-b0e9-0a7e-e343-c8de448157bd",
                "relationView": {
                    "id": "6f42b17c-7bd9-9117-931f-b86209dcb1a8",
                    "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                    "from": "279c5170-159b-2b0d-34fa-e2e42dd5e0a9",
                    "to": "c763f4a6-b0e9-0a7e-e343-c8de448157bd",
                    "needReconnect": True,
                    "value": "[[606,380],[694,380]]"
                },
                "hexagonalView": {
                    "_type": "org.uengine.modeling.model.RelationHexagonal",
                    "from": "279c5170-159b-2b0d-34fa-e2e42dd5e0a9",
                    "id": "6f42b17c-7bd9-9117-931f-b86209dcb1a8",
                    "needReconnect": True,
                    "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                    "to": "c763f4a6-b0e9-0a7e-e343-c8de448157bd",
                    "value": None
                },
                "sourceMultiplicity": "1",
                "targetMultiplicity": "1"
            },
            "68915ca5-a8d0-c4a5-3de7-222f4c8d8059": {
                "_type": "org.uengine.modeling.model.Relation",
                "name": "",
                "id": "68915ca5-a8d0-c4a5-3de7-222f4c8d8059",
                "sourceElement": {
                    "_type": "org.uengine.modeling.model.Command",
                    "outputEvents": [
                        "BookDiscarded"
                    ],
                    "aggregate": {
                        "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                    },
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                    },
                    "controllerInfo": {
                        "apiPath": "discardbook",
                        "method": "PUT",
                        "fullApiPath": ""
                    },
                    "fieldDescriptors": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "ISBN",
                            "nameCamelCase": "isbn",
                            "namePascalCase": "Isbn",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": False,
                            "name": "discardReason",
                            "nameCamelCase": "discardReason",
                            "namePascalCase": "DiscardReason",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "description": None,
                    "id": "b6d57c04-edb1-c660-ea90-b0ef48b57dd1",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Command",
                        "height": 116,
                        "id": "b6d57c04-edb1-c660-ea90-b0ef48b57dd1",
                        "style": "{}",
                        "width": 100,
                        "x": 556,
                        "y": 510,
                        "z-index": 999
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.CommandHexagonal",
                        "height": 0,
                        "id": "b6d57c04-edb1-c660-ea90-b0ef48b57dd1",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0
                    },
                    "isRestRepository": False,
                    "name": "DiscardBook",
                    "displayName": "도서 폐기",
                    "nameCamelCase": "discardBook",
                    "namePascalCase": "DiscardBook",
                    "namePlural": "discardBooks",
                    "relationCommandInfo": [],
                    "relationEventInfo": [],
                    "restRepositoryInfo": {
                        "method": "PUT"
                    },
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PrePersist"
                },
                "targetElement": {
                    "alertURL": "/static/image/symbol/alert-icon.png",
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "checkAlert": True,
                    "description": None,
                    "id": "bdad54b2-d2ba-9e60-f28e-4959a9d55f42",
                    "elementView": {
                        "angle": 0,
                        "height": 116,
                        "id": "bdad54b2-d2ba-9e60-f28e-4959a9d55f42",
                        "style": "{}",
                        "width": 100,
                        "x": 744,
                        "y": 510,
                        "_type": "org.uengine.modeling.model.Event"
                    },
                    "fieldDescriptors": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "ISBN",
                            "nameCamelCase": "isbn",
                            "namePascalCase": "Isbn",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": False,
                            "name": "discardReason",
                            "nameCamelCase": "discardReason",
                            "namePascalCase": "DiscardReason",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Date",
                            "isCopy": False,
                            "isKey": False,
                            "name": "discardedAt",
                            "nameCamelCase": "discardedAt",
                            "namePascalCase": "DiscardedAt",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "hexagonalView": {
                        "height": 0,
                        "id": "bdad54b2-d2ba-9e60-f28e-4959a9d55f42",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0,
                        "_type": "org.uengine.modeling.model.EventHexagonal"
                    },
                    "name": "BookDiscarded",
                    "displayName": "도서 폐기됨",
                    "nameCamelCase": "bookDiscarded",
                    "namePascalCase": "BookDiscarded",
                    "namePlural": "",
                    "relationCommandInfo": [],
                    "relationPolicyInfo": [],
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PostPersist",
                    "_type": "org.uengine.modeling.model.Event",
                    "aggregate": {
                        "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                    },
                    "boundedContext": {
                        "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                    }
                },
                "from": "b6d57c04-edb1-c660-ea90-b0ef48b57dd1",
                "to": "bdad54b2-d2ba-9e60-f28e-4959a9d55f42",
                "relationView": {
                    "id": "68915ca5-a8d0-c4a5-3de7-222f4c8d8059",
                    "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                    "from": "b6d57c04-edb1-c660-ea90-b0ef48b57dd1",
                    "to": "bdad54b2-d2ba-9e60-f28e-4959a9d55f42",
                    "needReconnect": True,
                    "value": "[[606,512],[694,512]]"
                },
                "hexagonalView": {
                    "_type": "org.uengine.modeling.model.RelationHexagonal",
                    "from": "b6d57c04-edb1-c660-ea90-b0ef48b57dd1",
                    "id": "68915ca5-a8d0-c4a5-3de7-222f4c8d8059",
                    "needReconnect": True,
                    "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                    "to": "bdad54b2-d2ba-9e60-f28e-4959a9d55f42",
                    "value": None
                },
                "sourceMultiplicity": "1",
                "targetMultiplicity": "1"
            },
            "6b1b17ec-5f86-f717-4d56-c65562851bf7": {
                "_type": "org.uengine.modeling.model.Relation",
                "name": "",
                "id": "6b1b17ec-5f86-f717-4d56-c65562851bf7",
                "sourceElement": {
                    "_type": "org.uengine.modeling.model.Command",
                    "outputEvents": [
                        "Loaned"
                    ],
                    "aggregate": {
                        "id": "30176142-717c-cc1a-0d59-771539ac988a"
                    },
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                    },
                    "controllerInfo": {
                        "apiPath": "loanbook",
                        "method": "POST",
                        "fullApiPath": ""
                    },
                    "fieldDescriptors": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "memberNumber",
                            "nameCamelCase": "memberNumber",
                            "namePascalCase": "MemberNumber",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": False,
                            "name": "memberName",
                            "nameCamelCase": "memberName",
                            "namePascalCase": "MemberName",
                            "displayName": "",
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
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "description": None,
                    "id": "7a421b31-a5ff-c17c-076f-a700e59be8fd",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Command",
                        "height": 116,
                        "id": "7a421b31-a5ff-c17c-076f-a700e59be8fd",
                        "style": "{}",
                        "width": 100,
                        "x": 1141,
                        "y": 250,
                        "z-index": 999
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.CommandHexagonal",
                        "height": 0,
                        "id": "7a421b31-a5ff-c17c-076f-a700e59be8fd",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0
                    },
                    "isRestRepository": False,
                    "name": "LoanBook",
                    "displayName": "도서 대출 신청",
                    "nameCamelCase": "loanBook",
                    "namePascalCase": "LoanBook",
                    "namePlural": "loanBooks",
                    "relationCommandInfo": [],
                    "relationEventInfo": [],
                    "restRepositoryInfo": {
                        "method": "POST"
                    },
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PrePersist"
                },
                "targetElement": {
                    "alertURL": "/static/image/symbol/alert-icon.png",
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "checkAlert": True,
                    "description": None,
                    "id": "b12ad8fd-6404-c544-5ff8-b5bc1fdcae20",
                    "elementView": {
                        "angle": 0,
                        "height": 116,
                        "id": "b12ad8fd-6404-c544-5ff8-b5bc1fdcae20",
                        "style": "{}",
                        "width": 100,
                        "x": 1329,
                        "y": 250,
                        "_type": "org.uengine.modeling.model.Event"
                    },
                    "fieldDescriptors": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "loanId",
                            "nameCamelCase": "loanId",
                            "namePascalCase": "LoanId",
                            "displayName": "",
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
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "hexagonalView": {
                        "height": 0,
                        "id": "b12ad8fd-6404-c544-5ff8-b5bc1fdcae20",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0,
                        "_type": "org.uengine.modeling.model.EventHexagonal"
                    },
                    "name": "Loaned",
                    "displayName": "도서 대출 완료",
                    "nameCamelCase": "loaned",
                    "namePascalCase": "Loaned",
                    "namePlural": "",
                    "relationCommandInfo": [],
                    "relationPolicyInfo": [],
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PostPersist",
                    "_type": "org.uengine.modeling.model.Event",
                    "aggregate": {
                        "id": "30176142-717c-cc1a-0d59-771539ac988a"
                    },
                    "boundedContext": {
                        "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                    }
                },
                "from": "7a421b31-a5ff-c17c-076f-a700e59be8fd",
                "to": "b12ad8fd-6404-c544-5ff8-b5bc1fdcae20",
                "relationView": {
                    "id": "6b1b17ec-5f86-f717-4d56-c65562851bf7",
                    "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                    "from": "7a421b31-a5ff-c17c-076f-a700e59be8fd",
                    "to": "b12ad8fd-6404-c544-5ff8-b5bc1fdcae20",
                    "needReconnect": True,
                    "value": "[[1191,252],[1279,252]]"
                },
                "hexagonalView": {
                    "_type": "org.uengine.modeling.model.RelationHexagonal",
                    "from": "7a421b31-a5ff-c17c-076f-a700e59be8fd",
                    "id": "6b1b17ec-5f86-f717-4d56-c65562851bf7",
                    "needReconnect": True,
                    "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                    "to": "b12ad8fd-6404-c544-5ff8-b5bc1fdcae20",
                    "value": None
                },
                "sourceMultiplicity": "1",
                "targetMultiplicity": "1"
            },
            "c962a7d8-870a-f0de-ca15-dc79298c7567": {
                "_type": "org.uengine.modeling.model.Relation",
                "name": "",
                "id": "c962a7d8-870a-f0de-ca15-dc79298c7567",
                "sourceElement": {
                    "_type": "org.uengine.modeling.model.Command",
                    "outputEvents": [
                        "Returned"
                    ],
                    "aggregate": {
                        "id": "30176142-717c-cc1a-0d59-771539ac988a"
                    },
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                    },
                    "controllerInfo": {
                        "apiPath": "returnbook",
                        "method": "POST",
                        "fullApiPath": ""
                    },
                    "fieldDescriptors": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "loanId",
                            "nameCamelCase": "loanId",
                            "namePascalCase": "LoanId",
                            "displayName": "",
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
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "description": None,
                    "id": "621d4bda-16fd-1bda-d837-89991959fbb2",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Command",
                        "height": 116,
                        "id": "621d4bda-16fd-1bda-d837-89991959fbb2",
                        "style": "{}",
                        "width": 100,
                        "x": 1141,
                        "y": 380,
                        "z-index": 999
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.CommandHexagonal",
                        "height": 0,
                        "id": "621d4bda-16fd-1bda-d837-89991959fbb2",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0
                    },
                    "isRestRepository": False,
                    "name": "ReturnBook",
                    "displayName": "도서 반납 처리",
                    "nameCamelCase": "returnBook",
                    "namePascalCase": "ReturnBook",
                    "namePlural": "returnBooks",
                    "relationCommandInfo": [],
                    "relationEventInfo": [],
                    "restRepositoryInfo": {
                        "method": "POST"
                    },
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PrePersist"
                },
                "targetElement": {
                    "alertURL": "/static/image/symbol/alert-icon.png",
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "checkAlert": True,
                    "description": None,
                    "id": "7134ee93-d752-ba68-bcd8-c39788567f0f",
                    "elementView": {
                        "angle": 0,
                        "height": 116,
                        "id": "7134ee93-d752-ba68-bcd8-c39788567f0f",
                        "style": "{}",
                        "width": 100,
                        "x": 1329,
                        "y": 380,
                        "_type": "org.uengine.modeling.model.Event"
                    },
                    "fieldDescriptors": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "loanId",
                            "nameCamelCase": "loanId",
                            "namePascalCase": "LoanId",
                            "displayName": "",
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
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Date",
                            "isCopy": False,
                            "isKey": False,
                            "name": "returnedDate",
                            "nameCamelCase": "returnedDate",
                            "namePascalCase": "ReturnedDate",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "hexagonalView": {
                        "height": 0,
                        "id": "7134ee93-d752-ba68-bcd8-c39788567f0f",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0,
                        "_type": "org.uengine.modeling.model.EventHexagonal"
                    },
                    "name": "Returned",
                    "displayName": "도서 반납 완료",
                    "nameCamelCase": "returned",
                    "namePascalCase": "Returned",
                    "namePlural": "",
                    "relationCommandInfo": [],
                    "relationPolicyInfo": [],
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PostPersist",
                    "_type": "org.uengine.modeling.model.Event",
                    "aggregate": {
                        "id": "30176142-717c-cc1a-0d59-771539ac988a"
                    },
                    "boundedContext": {
                        "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                    }
                },
                "from": "621d4bda-16fd-1bda-d837-89991959fbb2",
                "to": "7134ee93-d752-ba68-bcd8-c39788567f0f",
                "relationView": {
                    "id": "c962a7d8-870a-f0de-ca15-dc79298c7567",
                    "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                    "from": "621d4bda-16fd-1bda-d837-89991959fbb2",
                    "to": "7134ee93-d752-ba68-bcd8-c39788567f0f",
                    "needReconnect": True,
                    "value": "[[1191,380],[1279,380]]"
                },
                "hexagonalView": {
                    "_type": "org.uengine.modeling.model.RelationHexagonal",
                    "from": "621d4bda-16fd-1bda-d837-89991959fbb2",
                    "id": "c962a7d8-870a-f0de-ca15-dc79298c7567",
                    "needReconnect": True,
                    "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                    "to": "7134ee93-d752-ba68-bcd8-c39788567f0f",
                    "value": None
                },
                "sourceMultiplicity": "1",
                "targetMultiplicity": "1"
            },
            "ceaa5350-4648-a1dc-426c-4ecd5d4542fa": {
                "_type": "org.uengine.modeling.model.Relation",
                "name": "",
                "id": "ceaa5350-4648-a1dc-426c-4ecd5d4542fa",
                "sourceElement": {
                    "_type": "org.uengine.modeling.model.Command",
                    "outputEvents": [
                        "Reserved"
                    ],
                    "aggregate": {
                        "id": "30176142-717c-cc1a-0d59-771539ac988a"
                    },
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                    },
                    "controllerInfo": {
                        "apiPath": "reservebook",
                        "method": "POST",
                        "fullApiPath": ""
                    },
                    "fieldDescriptors": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "memberNumber",
                            "nameCamelCase": "memberNumber",
                            "namePascalCase": "MemberNumber",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": False,
                            "name": "memberName",
                            "nameCamelCase": "memberName",
                            "namePascalCase": "MemberName",
                            "displayName": "",
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
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "description": None,
                    "id": "e9506a41-7406-7ded-e91a-81c2dd99da75",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Command",
                        "height": 116,
                        "id": "e9506a41-7406-7ded-e91a-81c2dd99da75",
                        "style": "{}",
                        "width": 100,
                        "x": 1141,
                        "y": 510,
                        "z-index": 999
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.CommandHexagonal",
                        "height": 0,
                        "id": "e9506a41-7406-7ded-e91a-81c2dd99da75",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0
                    },
                    "isRestRepository": False,
                    "name": "ReserveBook",
                    "displayName": "도서 예약 신청",
                    "nameCamelCase": "reserveBook",
                    "namePascalCase": "ReserveBook",
                    "namePlural": "reserveBooks",
                    "relationCommandInfo": [],
                    "relationEventInfo": [],
                    "restRepositoryInfo": {
                        "method": "POST"
                    },
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PrePersist"
                },
                "targetElement": {
                    "alertURL": "/static/image/symbol/alert-icon.png",
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "checkAlert": True,
                    "description": None,
                    "id": "e5cb69a8-8001-cf81-d4da-fffd1401afe5",
                    "elementView": {
                        "angle": 0,
                        "height": 116,
                        "id": "e5cb69a8-8001-cf81-d4da-fffd1401afe5",
                        "style": "{}",
                        "width": 100,
                        "x": 1329,
                        "y": 510,
                        "_type": "org.uengine.modeling.model.Event"
                    },
                    "fieldDescriptors": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "reservationId",
                            "nameCamelCase": "reservationId",
                            "namePascalCase": "ReservationId",
                            "displayName": "",
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
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Date",
                            "isCopy": False,
                            "isKey": False,
                            "name": "reservedDate",
                            "nameCamelCase": "reservedDate",
                            "namePascalCase": "ReservedDate",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "hexagonalView": {
                        "height": 0,
                        "id": "e5cb69a8-8001-cf81-d4da-fffd1401afe5",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0,
                        "_type": "org.uengine.modeling.model.EventHexagonal"
                    },
                    "name": "Reserved",
                    "displayName": "도서 예약 완료",
                    "nameCamelCase": "reserved",
                    "namePascalCase": "Reserved",
                    "namePlural": "",
                    "relationCommandInfo": [],
                    "relationPolicyInfo": [],
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PostPersist",
                    "_type": "org.uengine.modeling.model.Event",
                    "aggregate": {
                        "id": "30176142-717c-cc1a-0d59-771539ac988a"
                    },
                    "boundedContext": {
                        "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                    }
                },
                "from": "e9506a41-7406-7ded-e91a-81c2dd99da75",
                "to": "e5cb69a8-8001-cf81-d4da-fffd1401afe5",
                "relationView": {
                    "id": "ceaa5350-4648-a1dc-426c-4ecd5d4542fa",
                    "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                    "from": "e9506a41-7406-7ded-e91a-81c2dd99da75",
                    "to": "e5cb69a8-8001-cf81-d4da-fffd1401afe5",
                    "needReconnect": True,
                    "value": "[[1191,512],[1279,512]]"
                },
                "hexagonalView": {
                    "_type": "org.uengine.modeling.model.RelationHexagonal",
                    "from": "e9506a41-7406-7ded-e91a-81c2dd99da75",
                    "id": "ceaa5350-4648-a1dc-426c-4ecd5d4542fa",
                    "needReconnect": True,
                    "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                    "to": "e5cb69a8-8001-cf81-d4da-fffd1401afe5",
                    "value": None
                },
                "sourceMultiplicity": "1",
                "targetMultiplicity": "1"
            }
        },
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
    "boundedContextDisplayName": "도서 관리",
    "esAliasTransManager": {
        "esValue": {
            "elements": {
                "97f2473e-7068-21ee-652d-ba0a8f41dd2c": {
                    "_type": "org.uengine.modeling.model.BoundedContext",
                    "aggregates": [
                        {
                            "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                        }
                    ],
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "description": "[{\"type\":\"userStory\",\"text\":\"도서 관리 화면에서는 새로운 도서를 등록하고 현재 보유한 도서들의 상태를 관리할 수 있어야 해. 도서 등록 시에는 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받아야 해. ISBN은 13자리 숫자여야 하고 중복 확인이 필요해. 카테고리는 소설/비소설/학술/잡지 중에서 선택할 수 있어야 해. 등록된 도서는 처음에 '대출가능' 상태가 되고, 이후 대출/반납 상황에 따라 '대출중', '예약중' 상태로 자동으로 변경되어야 해. 도서가 훼손되거나 분실된 경우 '폐기' 처리가 가능해야 해며, 폐기된 도서는 더 이상 대출이 불가능해야 해.\"}]",
                    "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.BoundedContext",
                        "height": 726,
                        "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c",
                        "style": "{}",
                        "width": 560,
                        "x": 650,
                        "y": 518
                    },
                    "gitURL": None,
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
                        "height": 350,
                        "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c",
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
                    "definitionId": "163972132_es_0ef8941a61478455167111b05b128cea"
                },
                "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908": {
                    "_type": "org.uengine.modeling.model.BoundedContext",
                    "aggregates": [
                        {
                            "id": "30176142-717c-cc1a-0d59-771539ac988a"
                        }
                    ],
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "description": "[{\"type\":\"userStory\",\"text\":\"대출/반납 화면에서는 회원이 도서를 대출하고 반납하는 것을 관리할 수 있어야 해. 대출 신청 시에는 회원번호와 이름으로 회원을 확인하고, 대출할 도서를 선택해야 해. 도서는 도서명이나 ISBN으로 검색할 수 있어야 해. 대출 기간은 7일/14일/30일 중에서 선택할 수 있어. 만약 대출하려는 도서가 이미 대출 중이라면, 예약 신청이 가능해야 해. 대출이 완료되면 해당 도서의 상태는 자동으로 '대출중'으로 변경되어야 해.\"}]",
                    "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.BoundedContext",
                        "height": 726,
                        "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908",
                        "style": "{}",
                        "width": 560,
                        "x": 1235,
                        "y": 518
                    },
                    "gitURL": None,
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
                        "height": 350,
                        "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908",
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
                    "definitionId": "163972132_es_0ef8941a61478455167111b05b128cea"
                },
                "f81e4c75-040c-83ad-4656-65cfccc74cc2": {
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
                                "aa6acc4d-3773-6aa9-3cf2-d22a860272a8": {
                                    "_type": "org.uengine.uml.model.Class",
                                    "id": "aa6acc4d-3773-6aa9-3cf2-d22a860272a8",
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
                                        "id": "aa6acc4d-3773-6aa9-3cf2-d22a860272a8",
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
                                    "parentId": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                                },
                                "3e68e3a2-7dd9-dab0-3d03-2753ba0a1233": {
                                    "_type": "org.uengine.uml.model.enum",
                                    "id": "3e68e3a2-7dd9-dab0-3d03-2753ba0a1233",
                                    "name": "Category",
                                    "displayName": "카테고리",
                                    "nameCamelCase": "category",
                                    "namePascalCase": "Category",
                                    "namePlural": "categories",
                                    "elementView": {
                                        "_type": "org.uengine.uml.model.enum",
                                        "id": "3e68e3a2-7dd9-dab0-3d03-2753ba0a1233",
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
                                "73640bd2-3239-18e6-0c05-22462730ed92": {
                                    "_type": "org.uengine.uml.model.enum",
                                    "id": "73640bd2-3239-18e6-0c05-22462730ed92",
                                    "name": "Status",
                                    "displayName": "도서상태",
                                    "nameCamelCase": "status",
                                    "namePascalCase": "Status",
                                    "namePlural": "statuses",
                                    "elementView": {
                                        "_type": "org.uengine.uml.model.enum",
                                        "id": "73640bd2-3239-18e6-0c05-22462730ed92",
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
                        "name": "97f2473e-7068-21ee-652d-ba0a8f41dd2c",
                        "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                    },
                    "commands": [],
                    "description": None,
                    "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Aggregate",
                        "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2",
                        "x": 650,
                        "y": 525,
                        "width": 130,
                        "height": 550
                    },
                    "events": [],
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.AggregateHexagonal",
                        "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2",
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
                "30176142-717c-cc1a-0d59-771539ac988a": {
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
                            },
                            {
                                "className": "BookId",
                                "isCopy": False,
                                "isKey": False,
                                "name": "bookId",
                                "nameCamelCase": "bookId",
                                "namePascalCase": "BookId",
                                "displayName": "",
                                "referenceClass": "Book",
                                "isOverrideField": True,
                                "_type": "org.uengine.model.FieldDescriptor"
                            }
                        ],
                        "entities": {
                            "elements": {
                                "19aa4d64-6084-e826-7c69-0bd1896e6f79": {
                                    "_type": "org.uengine.uml.model.Class",
                                    "id": "19aa4d64-6084-e826-7c69-0bd1896e6f79",
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
                                        },
                                        {
                                            "className": "BookId",
                                            "isCopy": False,
                                            "isKey": False,
                                            "name": "bookId",
                                            "nameCamelCase": "bookId",
                                            "namePascalCase": "BookId",
                                            "displayName": "",
                                            "referenceClass": "Book",
                                            "isOverrideField": True,
                                            "_type": "org.uengine.model.FieldDescriptor"
                                        }
                                    ],
                                    "operations": [],
                                    "elementView": {
                                        "_type": "org.uengine.uml.model.Class",
                                        "id": "19aa4d64-6084-e826-7c69-0bd1896e6f79",
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
                                    "parentId": "30176142-717c-cc1a-0d59-771539ac988a"
                                },
                                "7ec1a4ec-7237-ab46-0c52-fe21ca1a9a09": {
                                    "_type": "org.uengine.uml.model.enum",
                                    "id": "7ec1a4ec-7237-ab46-0c52-fe21ca1a9a09",
                                    "name": "TransactionType",
                                    "displayName": "거래 유형",
                                    "nameCamelCase": "transactionType",
                                    "namePascalCase": "TransactionType",
                                    "namePlural": "transactionTypes",
                                    "elementView": {
                                        "_type": "org.uengine.uml.model.enum",
                                        "id": "7ec1a4ec-7237-ab46-0c52-fe21ca1a9a09",
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
                                },
                                "9b7dd1cc-d76b-2b36-1f93-9eb8930afef6": {
                                    "_type": "org.uengine.uml.model.vo.Class",
                                    "id": "9b7dd1cc-d76b-2b36-1f93-9eb8930afef6",
                                    "name": "BookId",
                                    "displayName": "",
                                    "namePascalCase": "BookId",
                                    "nameCamelCase": "bookId",
                                    "fieldDescriptors": [
                                        {
                                            "className": "String",
                                            "isKey": True,
                                            "label": "- ISBN: String",
                                            "name": "ISBN",
                                            "nameCamelCase": "isbn",
                                            "namePascalCase": "Isbn",
                                            "displayName": "",
                                            "referenceClass": "Book",
                                            "isOverrideField": True,
                                            "_type": "org.uengine.model.FieldDescriptor"
                                        }
                                    ],
                                    "operations": [],
                                    "elementView": {
                                        "_type": "org.uengine.uml.model.vo.address.Class",
                                        "id": "9b7dd1cc-d76b-2b36-1f93-9eb8930afef6",
                                        "x": 700,
                                        "y": 152,
                                        "width": 200,
                                        "height": 100,
                                        "style": "{}",
                                        "titleH": 50,
                                        "subEdgeH": 170,
                                        "fieldH": 150,
                                        "methodH": 30
                                    },
                                    "selected": False,
                                    "parentOperations": [],
                                    "relationType": None,
                                    "isVO": True,
                                    "relations": [],
                                    "groupElement": None,
                                    "isAggregateRoot": False,
                                    "namePlural": "BookIds",
                                    "isAbstract": False,
                                    "isInterface": False
                                }
                            },
                            "relations": {}
                        },
                        "operations": []
                    },
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "name": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908",
                        "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                    },
                    "commands": [],
                    "description": None,
                    "id": "30176142-717c-cc1a-0d59-771539ac988a",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Aggregate",
                        "id": "30176142-717c-cc1a-0d59-771539ac988a",
                        "x": 1235,
                        "y": 525,
                        "width": 130,
                        "height": 550
                    },
                    "events": [],
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.AggregateHexagonal",
                        "id": "30176142-717c-cc1a-0d59-771539ac988a",
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
                },
                "dc9f7be6-103e-0d9f-96b6-a1de4ae31d3f": {
                    "alertURL": "/static/image/symbol/alert-icon.png",
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "checkAlert": True,
                    "description": None,
                    "id": "dc9f7be6-103e-0d9f-96b6-a1de4ae31d3f",
                    "elementView": {
                        "angle": 0,
                        "height": 116,
                        "id": "dc9f7be6-103e-0d9f-96b6-a1de4ae31d3f",
                        "style": "{}",
                        "width": 100,
                        "x": 744,
                        "y": 250,
                        "_type": "org.uengine.modeling.model.Event"
                    },
                    "fieldDescriptors": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "ISBN",
                            "nameCamelCase": "isbn",
                            "namePascalCase": "Isbn",
                            "displayName": "",
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
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "hexagonalView": {
                        "height": 0,
                        "id": "dc9f7be6-103e-0d9f-96b6-a1de4ae31d3f",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0,
                        "_type": "org.uengine.modeling.model.EventHexagonal"
                    },
                    "name": "BookRegistered",
                    "displayName": "도서 등록됨",
                    "nameCamelCase": "bookRegistered",
                    "namePascalCase": "BookRegistered",
                    "namePlural": "",
                    "relationCommandInfo": [],
                    "relationPolicyInfo": [],
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PostPersist",
                    "_type": "org.uengine.modeling.model.Event",
                    "aggregate": {
                        "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                    },
                    "boundedContext": {
                        "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                    }
                },
                "c763f4a6-b0e9-0a7e-e343-c8de448157bd": {
                    "alertURL": "/static/image/symbol/alert-icon.png",
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "checkAlert": True,
                    "description": None,
                    "id": "c763f4a6-b0e9-0a7e-e343-c8de448157bd",
                    "elementView": {
                        "angle": 0,
                        "height": 116,
                        "id": "c763f4a6-b0e9-0a7e-e343-c8de448157bd",
                        "style": "{}",
                        "width": 100,
                        "x": 744,
                        "y": 380,
                        "_type": "org.uengine.modeling.model.Event"
                    },
                    "fieldDescriptors": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "ISBN",
                            "nameCamelCase": "isbn",
                            "namePascalCase": "Isbn",
                            "displayName": "",
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
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Date",
                            "isCopy": False,
                            "isKey": False,
                            "name": "changedAt",
                            "nameCamelCase": "changedAt",
                            "namePascalCase": "ChangedAt",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": False,
                            "name": "reason",
                            "nameCamelCase": "reason",
                            "namePascalCase": "Reason",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "hexagonalView": {
                        "height": 0,
                        "id": "c763f4a6-b0e9-0a7e-e343-c8de448157bd",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0,
                        "_type": "org.uengine.modeling.model.EventHexagonal"
                    },
                    "name": "BookStatusChanged",
                    "displayName": "도서 상태 변경됨",
                    "nameCamelCase": "bookStatusChanged",
                    "namePascalCase": "BookStatusChanged",
                    "namePlural": "",
                    "relationCommandInfo": [],
                    "relationPolicyInfo": [],
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PostPersist",
                    "_type": "org.uengine.modeling.model.Event",
                    "aggregate": {
                        "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                    },
                    "boundedContext": {
                        "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                    }
                },
                "bdad54b2-d2ba-9e60-f28e-4959a9d55f42": {
                    "alertURL": "/static/image/symbol/alert-icon.png",
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "checkAlert": True,
                    "description": None,
                    "id": "bdad54b2-d2ba-9e60-f28e-4959a9d55f42",
                    "elementView": {
                        "angle": 0,
                        "height": 116,
                        "id": "bdad54b2-d2ba-9e60-f28e-4959a9d55f42",
                        "style": "{}",
                        "width": 100,
                        "x": 744,
                        "y": 510,
                        "_type": "org.uengine.modeling.model.Event"
                    },
                    "fieldDescriptors": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "ISBN",
                            "nameCamelCase": "isbn",
                            "namePascalCase": "Isbn",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": False,
                            "name": "discardReason",
                            "nameCamelCase": "discardReason",
                            "namePascalCase": "DiscardReason",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Date",
                            "isCopy": False,
                            "isKey": False,
                            "name": "discardedAt",
                            "nameCamelCase": "discardedAt",
                            "namePascalCase": "DiscardedAt",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "hexagonalView": {
                        "height": 0,
                        "id": "bdad54b2-d2ba-9e60-f28e-4959a9d55f42",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0,
                        "_type": "org.uengine.modeling.model.EventHexagonal"
                    },
                    "name": "BookDiscarded",
                    "displayName": "도서 폐기됨",
                    "nameCamelCase": "bookDiscarded",
                    "namePascalCase": "BookDiscarded",
                    "namePlural": "",
                    "relationCommandInfo": [],
                    "relationPolicyInfo": [],
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PostPersist",
                    "_type": "org.uengine.modeling.model.Event",
                    "aggregate": {
                        "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                    },
                    "boundedContext": {
                        "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                    }
                },
                "9dfd77c4-7bb3-6a62-025d-633c63438cf6": {
                    "_type": "org.uengine.modeling.model.Command",
                    "outputEvents": [
                        "BookRegistered"
                    ],
                    "aggregate": {
                        "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                    },
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                    },
                    "controllerInfo": {
                        "apiPath": "registerbook",
                        "method": "POST",
                        "fullApiPath": ""
                    },
                    "fieldDescriptors": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "ISBN",
                            "nameCamelCase": "isbn",
                            "namePascalCase": "Isbn",
                            "displayName": "",
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
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "description": None,
                    "id": "9dfd77c4-7bb3-6a62-025d-633c63438cf6",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Command",
                        "height": 116,
                        "id": "9dfd77c4-7bb3-6a62-025d-633c63438cf6",
                        "style": "{}",
                        "width": 100,
                        "x": 556,
                        "y": 250,
                        "z-index": 999
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.CommandHexagonal",
                        "height": 0,
                        "id": "9dfd77c4-7bb3-6a62-025d-633c63438cf6",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0
                    },
                    "isRestRepository": False,
                    "name": "RegisterBook",
                    "displayName": "도서 등록",
                    "nameCamelCase": "registerBook",
                    "namePascalCase": "RegisterBook",
                    "namePlural": "registerBooks",
                    "relationCommandInfo": [],
                    "relationEventInfo": [],
                    "restRepositoryInfo": {
                        "method": "POST"
                    },
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PrePersist"
                },
                "279c5170-159b-2b0d-34fa-e2e42dd5e0a9": {
                    "_type": "org.uengine.modeling.model.Command",
                    "outputEvents": [
                        "BookStatusChanged"
                    ],
                    "aggregate": {
                        "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                    },
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                    },
                    "controllerInfo": {
                        "apiPath": "changebookstatus",
                        "method": "PUT",
                        "fullApiPath": ""
                    },
                    "fieldDescriptors": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "ISBN",
                            "nameCamelCase": "isbn",
                            "namePascalCase": "Isbn",
                            "displayName": "",
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
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": False,
                            "name": "reason",
                            "nameCamelCase": "reason",
                            "namePascalCase": "Reason",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "description": None,
                    "id": "279c5170-159b-2b0d-34fa-e2e42dd5e0a9",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Command",
                        "height": 116,
                        "id": "279c5170-159b-2b0d-34fa-e2e42dd5e0a9",
                        "style": "{}",
                        "width": 100,
                        "x": 556,
                        "y": 380,
                        "z-index": 999
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.CommandHexagonal",
                        "height": 0,
                        "id": "279c5170-159b-2b0d-34fa-e2e42dd5e0a9",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0
                    },
                    "isRestRepository": False,
                    "name": "ChangeBookStatus",
                    "displayName": "도서 상태 변경",
                    "nameCamelCase": "changeBookStatus",
                    "namePascalCase": "ChangeBookStatus",
                    "namePlural": "changeBookStatuses",
                    "relationCommandInfo": [],
                    "relationEventInfo": [],
                    "restRepositoryInfo": {
                        "method": "PUT"
                    },
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PrePersist"
                },
                "b6d57c04-edb1-c660-ea90-b0ef48b57dd1": {
                    "_type": "org.uengine.modeling.model.Command",
                    "outputEvents": [
                        "BookDiscarded"
                    ],
                    "aggregate": {
                        "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                    },
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                    },
                    "controllerInfo": {
                        "apiPath": "discardbook",
                        "method": "PUT",
                        "fullApiPath": ""
                    },
                    "fieldDescriptors": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "ISBN",
                            "nameCamelCase": "isbn",
                            "namePascalCase": "Isbn",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": False,
                            "name": "discardReason",
                            "nameCamelCase": "discardReason",
                            "namePascalCase": "DiscardReason",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "description": None,
                    "id": "b6d57c04-edb1-c660-ea90-b0ef48b57dd1",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Command",
                        "height": 116,
                        "id": "b6d57c04-edb1-c660-ea90-b0ef48b57dd1",
                        "style": "{}",
                        "width": 100,
                        "x": 556,
                        "y": 510,
                        "z-index": 999
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.CommandHexagonal",
                        "height": 0,
                        "id": "b6d57c04-edb1-c660-ea90-b0ef48b57dd1",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0
                    },
                    "isRestRepository": False,
                    "name": "DiscardBook",
                    "displayName": "도서 폐기",
                    "nameCamelCase": "discardBook",
                    "namePascalCase": "DiscardBook",
                    "namePlural": "discardBooks",
                    "relationCommandInfo": [],
                    "relationEventInfo": [],
                    "restRepositoryInfo": {
                        "method": "PUT"
                    },
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PrePersist"
                },
                "76fa37dc-33e3-9cb1-a9e6-90695b09cb40": {
                    "_type": "org.uengine.modeling.model.View",
                    "id": "76fa37dc-33e3-9cb1-a9e6-90695b09cb40",
                    "visibility": "public",
                    "name": "BookList",
                    "oldName": "",
                    "displayName": "도서 목록",
                    "namePascalCase": "BookList",
                    "namePlural": "bookLists",
                    "aggregate": {
                        "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                    },
                    "description": None,
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                    },
                    "fieldDescriptors": [
                        {
                            "_type": "org.uengine.model.FieldDescriptor",
                            "name": "id",
                            "className": "Long",
                            "nameCamelCase": "id",
                            "namePascalCase": "Id",
                            "isKey": True
                        }
                    ],
                    "queryParameters": [
                        {
                            "className": "Category",
                            "isCopy": False,
                            "isKey": False,
                            "name": "category",
                            "nameCamelCase": "category",
                            "namePascalCase": "Category",
                            "displayName": "",
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
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "queryOption": {
                        "apiPath": "",
                        "useDefaultUri": True,
                        "multipleResult": True
                    },
                    "controllerInfo": {
                        "url": ""
                    },
                    "elementView": {
                        "_type": "org.uengine.modeling.model.View",
                        "id": "76fa37dc-33e3-9cb1-a9e6-90695b09cb40",
                        "x": 556,
                        "y": 640,
                        "width": 100,
                        "height": 116,
                        "style": "{}",
                        "z-index": 999
                    },
                    "editingView": False,
                    "dataProjection": "query-for-aggregate",
                    "createRules": [
                        {
                            "_type": "viewStoreRule",
                            "operation": "CREATE",
                            "when": None,
                            "fieldMapping": [
                                {
                                    "viewField": None,
                                    "eventField": None,
                                    "operator": "="
                                }
                            ],
                            "where": [
                                {
                                    "viewField": None,
                                    "eventField": None
                                }
                            ]
                        }
                    ],
                    "updateRules": [
                        {
                            "_type": "viewStoreRule",
                            "operation": "UPDATE",
                            "when": None,
                            "fieldMapping": [
                                {
                                    "viewField": None,
                                    "eventField": None,
                                    "operator": "="
                                }
                            ],
                            "where": [
                                {
                                    "viewField": None,
                                    "eventField": None
                                }
                            ]
                        }
                    ],
                    "deleteRules": [
                        {
                            "_type": "viewStoreRule",
                            "operation": "DELETE",
                            "when": None,
                            "fieldMapping": [
                                {
                                    "viewField": None,
                                    "eventField": None
                                }
                            ],
                            "where": [
                                {
                                    "viewField": None,
                                    "eventField": None
                                }
                            ]
                        }
                    ],
                    "rotateStatus": False,
                    "definitionId": ""
                },
                "cec595c2-bb4c-e116-de82-b514c8d38926": {
                    "_type": "org.uengine.modeling.model.View",
                    "id": "cec595c2-bb4c-e116-de82-b514c8d38926",
                    "visibility": "public",
                    "name": "BookDetails",
                    "oldName": "",
                    "displayName": "도서 상세정보",
                    "namePascalCase": "BookDetails",
                    "namePlural": "bookDetails",
                    "aggregate": {
                        "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                    },
                    "description": None,
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                    },
                    "fieldDescriptors": [
                        {
                            "_type": "org.uengine.model.FieldDescriptor",
                            "name": "id",
                            "className": "Long",
                            "nameCamelCase": "id",
                            "namePascalCase": "Id",
                            "isKey": True
                        }
                    ],
                    "queryParameters": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "ISBN",
                            "nameCamelCase": "isbn",
                            "namePascalCase": "Isbn",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "queryOption": {
                        "apiPath": "",
                        "useDefaultUri": True,
                        "multipleResult": False
                    },
                    "controllerInfo": {
                        "url": ""
                    },
                    "elementView": {
                        "_type": "org.uengine.modeling.model.View",
                        "id": "cec595c2-bb4c-e116-de82-b514c8d38926",
                        "x": 556,
                        "y": 770,
                        "width": 100,
                        "height": 116,
                        "style": "{}",
                        "z-index": 999
                    },
                    "editingView": False,
                    "dataProjection": "query-for-aggregate",
                    "createRules": [
                        {
                            "_type": "viewStoreRule",
                            "operation": "CREATE",
                            "when": None,
                            "fieldMapping": [
                                {
                                    "viewField": None,
                                    "eventField": None,
                                    "operator": "="
                                }
                            ],
                            "where": [
                                {
                                    "viewField": None,
                                    "eventField": None
                                }
                            ]
                        }
                    ],
                    "updateRules": [
                        {
                            "_type": "viewStoreRule",
                            "operation": "UPDATE",
                            "when": None,
                            "fieldMapping": [
                                {
                                    "viewField": None,
                                    "eventField": None,
                                    "operator": "="
                                }
                            ],
                            "where": [
                                {
                                    "viewField": None,
                                    "eventField": None
                                }
                            ]
                        }
                    ],
                    "deleteRules": [
                        {
                            "_type": "viewStoreRule",
                            "operation": "DELETE",
                            "when": None,
                            "fieldMapping": [
                                {
                                    "viewField": None,
                                    "eventField": None
                                }
                            ],
                            "where": [
                                {
                                    "viewField": None,
                                    "eventField": None
                                }
                            ]
                        }
                    ],
                    "rotateStatus": False,
                    "definitionId": ""
                },
                "48266e6a-49b8-a87b-10d3-ba1702401d61": {
                    "_type": "org.uengine.modeling.model.Actor",
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                    },
                    "description": None,
                    "id": "48266e6a-49b8-a87b-10d3-ba1702401d61",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Actor",
                        "height": 100,
                        "id": "48266e6a-49b8-a87b-10d3-ba1702401d61",
                        "style": "{}",
                        "width": 100,
                        "x": 475,
                        "y": 250
                    },
                    "innerAggregate": {
                        "command": [],
                        "event": [],
                        "external": [],
                        "policy": [],
                        "view": []
                    },
                    "name": "사용자",
                    "oldName": "",
                    "rotateStatus": False
                },
                "39998ac0-1667-efba-4c66-936c1c7827ae": {
                    "_type": "org.uengine.modeling.model.Actor",
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                    },
                    "description": None,
                    "id": "39998ac0-1667-efba-4c66-936c1c7827ae",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Actor",
                        "height": 100,
                        "id": "39998ac0-1667-efba-4c66-936c1c7827ae",
                        "style": "{}",
                        "width": 100,
                        "x": 475,
                        "y": 380
                    },
                    "innerAggregate": {
                        "command": [],
                        "event": [],
                        "external": [],
                        "policy": [],
                        "view": []
                    },
                    "name": "사용자",
                    "oldName": "",
                    "rotateStatus": False
                },
                "14f9b8d9-e377-cec8-c1b5-45cd402bfad7": {
                    "_type": "org.uengine.modeling.model.Actor",
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                    },
                    "description": None,
                    "id": "14f9b8d9-e377-cec8-c1b5-45cd402bfad7",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Actor",
                        "height": 100,
                        "id": "14f9b8d9-e377-cec8-c1b5-45cd402bfad7",
                        "style": "{}",
                        "width": 100,
                        "x": 475,
                        "y": 510
                    },
                    "innerAggregate": {
                        "command": [],
                        "event": [],
                        "external": [],
                        "policy": [],
                        "view": []
                    },
                    "name": "사용자",
                    "oldName": "",
                    "rotateStatus": False
                },
                "c4db0e92-3b28-e623-3a23-a8403a3ddff7": {
                    "_type": "org.uengine.modeling.model.Actor",
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                    },
                    "description": None,
                    "id": "c4db0e92-3b28-e623-3a23-a8403a3ddff7",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Actor",
                        "height": 100,
                        "id": "c4db0e92-3b28-e623-3a23-a8403a3ddff7",
                        "style": "{}",
                        "width": 100,
                        "x": 475,
                        "y": 640
                    },
                    "innerAggregate": {
                        "command": [],
                        "event": [],
                        "external": [],
                        "policy": [],
                        "view": []
                    },
                    "name": "사용자",
                    "oldName": "",
                    "rotateStatus": False,
                    "displayName": ""
                },
                "5a6c7a17-38f7-5f5a-23c5-11c2dd454202": {
                    "_type": "org.uengine.modeling.model.Actor",
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                    },
                    "description": None,
                    "id": "5a6c7a17-38f7-5f5a-23c5-11c2dd454202",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Actor",
                        "height": 100,
                        "id": "5a6c7a17-38f7-5f5a-23c5-11c2dd454202",
                        "style": "{}",
                        "width": 100,
                        "x": 475,
                        "y": 770
                    },
                    "innerAggregate": {
                        "command": [],
                        "event": [],
                        "external": [],
                        "policy": [],
                        "view": []
                    },
                    "name": "사용자",
                    "oldName": "",
                    "rotateStatus": False,
                    "displayName": ""
                },
                "b12ad8fd-6404-c544-5ff8-b5bc1fdcae20": {
                    "alertURL": "/static/image/symbol/alert-icon.png",
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "checkAlert": True,
                    "description": None,
                    "id": "b12ad8fd-6404-c544-5ff8-b5bc1fdcae20",
                    "elementView": {
                        "angle": 0,
                        "height": 116,
                        "id": "b12ad8fd-6404-c544-5ff8-b5bc1fdcae20",
                        "style": "{}",
                        "width": 100,
                        "x": 1329,
                        "y": 250,
                        "_type": "org.uengine.modeling.model.Event"
                    },
                    "fieldDescriptors": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "loanId",
                            "nameCamelCase": "loanId",
                            "namePascalCase": "LoanId",
                            "displayName": "",
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
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "hexagonalView": {
                        "height": 0,
                        "id": "b12ad8fd-6404-c544-5ff8-b5bc1fdcae20",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0,
                        "_type": "org.uengine.modeling.model.EventHexagonal"
                    },
                    "name": "Loaned",
                    "displayName": "도서 대출 완료",
                    "nameCamelCase": "loaned",
                    "namePascalCase": "Loaned",
                    "namePlural": "",
                    "relationCommandInfo": [],
                    "relationPolicyInfo": [],
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PostPersist",
                    "_type": "org.uengine.modeling.model.Event",
                    "aggregate": {
                        "id": "30176142-717c-cc1a-0d59-771539ac988a"
                    },
                    "boundedContext": {
                        "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                    }
                },
                "7134ee93-d752-ba68-bcd8-c39788567f0f": {
                    "alertURL": "/static/image/symbol/alert-icon.png",
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "checkAlert": True,
                    "description": None,
                    "id": "7134ee93-d752-ba68-bcd8-c39788567f0f",
                    "elementView": {
                        "angle": 0,
                        "height": 116,
                        "id": "7134ee93-d752-ba68-bcd8-c39788567f0f",
                        "style": "{}",
                        "width": 100,
                        "x": 1329,
                        "y": 380,
                        "_type": "org.uengine.modeling.model.Event"
                    },
                    "fieldDescriptors": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "loanId",
                            "nameCamelCase": "loanId",
                            "namePascalCase": "LoanId",
                            "displayName": "",
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
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Date",
                            "isCopy": False,
                            "isKey": False,
                            "name": "returnedDate",
                            "nameCamelCase": "returnedDate",
                            "namePascalCase": "ReturnedDate",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "hexagonalView": {
                        "height": 0,
                        "id": "7134ee93-d752-ba68-bcd8-c39788567f0f",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0,
                        "_type": "org.uengine.modeling.model.EventHexagonal"
                    },
                    "name": "Returned",
                    "displayName": "도서 반납 완료",
                    "nameCamelCase": "returned",
                    "namePascalCase": "Returned",
                    "namePlural": "",
                    "relationCommandInfo": [],
                    "relationPolicyInfo": [],
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PostPersist",
                    "_type": "org.uengine.modeling.model.Event",
                    "aggregate": {
                        "id": "30176142-717c-cc1a-0d59-771539ac988a"
                    },
                    "boundedContext": {
                        "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                    }
                },
                "e5cb69a8-8001-cf81-d4da-fffd1401afe5": {
                    "alertURL": "/static/image/symbol/alert-icon.png",
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "checkAlert": True,
                    "description": None,
                    "id": "e5cb69a8-8001-cf81-d4da-fffd1401afe5",
                    "elementView": {
                        "angle": 0,
                        "height": 116,
                        "id": "e5cb69a8-8001-cf81-d4da-fffd1401afe5",
                        "style": "{}",
                        "width": 100,
                        "x": 1329,
                        "y": 510,
                        "_type": "org.uengine.modeling.model.Event"
                    },
                    "fieldDescriptors": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "reservationId",
                            "nameCamelCase": "reservationId",
                            "namePascalCase": "ReservationId",
                            "displayName": "",
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
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Date",
                            "isCopy": False,
                            "isKey": False,
                            "name": "reservedDate",
                            "nameCamelCase": "reservedDate",
                            "namePascalCase": "ReservedDate",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "hexagonalView": {
                        "height": 0,
                        "id": "e5cb69a8-8001-cf81-d4da-fffd1401afe5",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0,
                        "_type": "org.uengine.modeling.model.EventHexagonal"
                    },
                    "name": "Reserved",
                    "displayName": "도서 예약 완료",
                    "nameCamelCase": "reserved",
                    "namePascalCase": "Reserved",
                    "namePlural": "",
                    "relationCommandInfo": [],
                    "relationPolicyInfo": [],
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PostPersist",
                    "_type": "org.uengine.modeling.model.Event",
                    "aggregate": {
                        "id": "30176142-717c-cc1a-0d59-771539ac988a"
                    },
                    "boundedContext": {
                        "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                    }
                },
                "7a421b31-a5ff-c17c-076f-a700e59be8fd": {
                    "_type": "org.uengine.modeling.model.Command",
                    "outputEvents": [
                        "Loaned"
                    ],
                    "aggregate": {
                        "id": "30176142-717c-cc1a-0d59-771539ac988a"
                    },
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                    },
                    "controllerInfo": {
                        "apiPath": "loanbook",
                        "method": "POST",
                        "fullApiPath": ""
                    },
                    "fieldDescriptors": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "memberNumber",
                            "nameCamelCase": "memberNumber",
                            "namePascalCase": "MemberNumber",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": False,
                            "name": "memberName",
                            "nameCamelCase": "memberName",
                            "namePascalCase": "MemberName",
                            "displayName": "",
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
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "description": None,
                    "id": "7a421b31-a5ff-c17c-076f-a700e59be8fd",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Command",
                        "height": 116,
                        "id": "7a421b31-a5ff-c17c-076f-a700e59be8fd",
                        "style": "{}",
                        "width": 100,
                        "x": 1141,
                        "y": 250,
                        "z-index": 999
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.CommandHexagonal",
                        "height": 0,
                        "id": "7a421b31-a5ff-c17c-076f-a700e59be8fd",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0
                    },
                    "isRestRepository": False,
                    "name": "LoanBook",
                    "displayName": "도서 대출 신청",
                    "nameCamelCase": "loanBook",
                    "namePascalCase": "LoanBook",
                    "namePlural": "loanBooks",
                    "relationCommandInfo": [],
                    "relationEventInfo": [],
                    "restRepositoryInfo": {
                        "method": "POST"
                    },
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PrePersist"
                },
                "621d4bda-16fd-1bda-d837-89991959fbb2": {
                    "_type": "org.uengine.modeling.model.Command",
                    "outputEvents": [
                        "Returned"
                    ],
                    "aggregate": {
                        "id": "30176142-717c-cc1a-0d59-771539ac988a"
                    },
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                    },
                    "controllerInfo": {
                        "apiPath": "returnbook",
                        "method": "POST",
                        "fullApiPath": ""
                    },
                    "fieldDescriptors": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "loanId",
                            "nameCamelCase": "loanId",
                            "namePascalCase": "LoanId",
                            "displayName": "",
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
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "description": None,
                    "id": "621d4bda-16fd-1bda-d837-89991959fbb2",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Command",
                        "height": 116,
                        "id": "621d4bda-16fd-1bda-d837-89991959fbb2",
                        "style": "{}",
                        "width": 100,
                        "x": 1141,
                        "y": 380,
                        "z-index": 999
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.CommandHexagonal",
                        "height": 0,
                        "id": "621d4bda-16fd-1bda-d837-89991959fbb2",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0
                    },
                    "isRestRepository": False,
                    "name": "ReturnBook",
                    "displayName": "도서 반납 처리",
                    "nameCamelCase": "returnBook",
                    "namePascalCase": "ReturnBook",
                    "namePlural": "returnBooks",
                    "relationCommandInfo": [],
                    "relationEventInfo": [],
                    "restRepositoryInfo": {
                        "method": "POST"
                    },
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PrePersist"
                },
                "e9506a41-7406-7ded-e91a-81c2dd99da75": {
                    "_type": "org.uengine.modeling.model.Command",
                    "outputEvents": [
                        "Reserved"
                    ],
                    "aggregate": {
                        "id": "30176142-717c-cc1a-0d59-771539ac988a"
                    },
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                    },
                    "controllerInfo": {
                        "apiPath": "reservebook",
                        "method": "POST",
                        "fullApiPath": ""
                    },
                    "fieldDescriptors": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "memberNumber",
                            "nameCamelCase": "memberNumber",
                            "namePascalCase": "MemberNumber",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": False,
                            "name": "memberName",
                            "nameCamelCase": "memberName",
                            "namePascalCase": "MemberName",
                            "displayName": "",
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
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "description": None,
                    "id": "e9506a41-7406-7ded-e91a-81c2dd99da75",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Command",
                        "height": 116,
                        "id": "e9506a41-7406-7ded-e91a-81c2dd99da75",
                        "style": "{}",
                        "width": 100,
                        "x": 1141,
                        "y": 510,
                        "z-index": 999
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.CommandHexagonal",
                        "height": 0,
                        "id": "e9506a41-7406-7ded-e91a-81c2dd99da75",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0
                    },
                    "isRestRepository": False,
                    "name": "ReserveBook",
                    "displayName": "도서 예약 신청",
                    "nameCamelCase": "reserveBook",
                    "namePascalCase": "ReserveBook",
                    "namePlural": "reserveBooks",
                    "relationCommandInfo": [],
                    "relationEventInfo": [],
                    "restRepositoryInfo": {
                        "method": "POST"
                    },
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PrePersist"
                },
                "692ff79a-552f-1049-965c-f6c780405f7a": {
                    "_type": "org.uengine.modeling.model.View",
                    "id": "692ff79a-552f-1049-965c-f6c780405f7a",
                    "visibility": "public",
                    "name": "LoanHistory",
                    "oldName": "",
                    "displayName": "대출/반납/예약 이력 조회",
                    "namePascalCase": "LoanHistory",
                    "namePlural": "loanHistories",
                    "aggregate": {
                        "id": "30176142-717c-cc1a-0d59-771539ac988a"
                    },
                    "description": None,
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                    },
                    "fieldDescriptors": [
                        {
                            "_type": "org.uengine.model.FieldDescriptor",
                            "name": "id",
                            "className": "Long",
                            "nameCamelCase": "id",
                            "namePascalCase": "Id",
                            "isKey": True
                        }
                    ],
                    "queryParameters": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "memberNumber",
                            "nameCamelCase": "memberNumber",
                            "namePascalCase": "MemberNumber",
                            "displayName": "",
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
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "queryOption": {
                        "apiPath": "",
                        "useDefaultUri": True,
                        "multipleResult": True
                    },
                    "controllerInfo": {
                        "url": ""
                    },
                    "elementView": {
                        "_type": "org.uengine.modeling.model.View",
                        "id": "692ff79a-552f-1049-965c-f6c780405f7a",
                        "x": 1141,
                        "y": 640,
                        "width": 100,
                        "height": 116,
                        "style": "{}",
                        "z-index": 999
                    },
                    "editingView": False,
                    "dataProjection": "query-for-aggregate",
                    "createRules": [
                        {
                            "_type": "viewStoreRule",
                            "operation": "CREATE",
                            "when": None,
                            "fieldMapping": [
                                {
                                    "viewField": None,
                                    "eventField": None,
                                    "operator": "="
                                }
                            ],
                            "where": [
                                {
                                    "viewField": None,
                                    "eventField": None
                                }
                            ]
                        }
                    ],
                    "updateRules": [
                        {
                            "_type": "viewStoreRule",
                            "operation": "UPDATE",
                            "when": None,
                            "fieldMapping": [
                                {
                                    "viewField": None,
                                    "eventField": None,
                                    "operator": "="
                                }
                            ],
                            "where": [
                                {
                                    "viewField": None,
                                    "eventField": None
                                }
                            ]
                        }
                    ],
                    "deleteRules": [
                        {
                            "_type": "viewStoreRule",
                            "operation": "DELETE",
                            "when": None,
                            "fieldMapping": [
                                {
                                    "viewField": None,
                                    "eventField": None
                                }
                            ],
                            "where": [
                                {
                                    "viewField": None,
                                    "eventField": None
                                }
                            ]
                        }
                    ],
                    "rotateStatus": False,
                    "definitionId": ""
                },
                "de913c2b-ea86-6d51-9b46-f66a42712964": {
                    "_type": "org.uengine.modeling.model.View",
                    "id": "de913c2b-ea86-6d51-9b46-f66a42712964",
                    "visibility": "public",
                    "name": "LoanCurrentStatus",
                    "oldName": "",
                    "displayName": "회원별 대출 현황",
                    "namePascalCase": "LoanCurrentStatus",
                    "namePlural": "loanCurrentStatuses",
                    "aggregate": {
                        "id": "30176142-717c-cc1a-0d59-771539ac988a"
                    },
                    "description": None,
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                    },
                    "fieldDescriptors": [
                        {
                            "_type": "org.uengine.model.FieldDescriptor",
                            "name": "id",
                            "className": "Long",
                            "nameCamelCase": "id",
                            "namePascalCase": "Id",
                            "isKey": True
                        }
                    ],
                    "queryParameters": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": True,
                            "name": "memberNumber",
                            "nameCamelCase": "memberNumber",
                            "namePascalCase": "MemberNumber",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "queryOption": {
                        "apiPath": "",
                        "useDefaultUri": True,
                        "multipleResult": True
                    },
                    "controllerInfo": {
                        "url": ""
                    },
                    "elementView": {
                        "_type": "org.uengine.modeling.model.View",
                        "id": "de913c2b-ea86-6d51-9b46-f66a42712964",
                        "x": 1141,
                        "y": 770,
                        "width": 100,
                        "height": 116,
                        "style": "{}",
                        "z-index": 999
                    },
                    "editingView": False,
                    "dataProjection": "query-for-aggregate",
                    "createRules": [
                        {
                            "_type": "viewStoreRule",
                            "operation": "CREATE",
                            "when": None,
                            "fieldMapping": [
                                {
                                    "viewField": None,
                                    "eventField": None,
                                    "operator": "="
                                }
                            ],
                            "where": [
                                {
                                    "viewField": None,
                                    "eventField": None
                                }
                            ]
                        }
                    ],
                    "updateRules": [
                        {
                            "_type": "viewStoreRule",
                            "operation": "UPDATE",
                            "when": None,
                            "fieldMapping": [
                                {
                                    "viewField": None,
                                    "eventField": None,
                                    "operator": "="
                                }
                            ],
                            "where": [
                                {
                                    "viewField": None,
                                    "eventField": None
                                }
                            ]
                        }
                    ],
                    "deleteRules": [
                        {
                            "_type": "viewStoreRule",
                            "operation": "DELETE",
                            "when": None,
                            "fieldMapping": [
                                {
                                    "viewField": None,
                                    "eventField": None
                                }
                            ],
                            "where": [
                                {
                                    "viewField": None,
                                    "eventField": None
                                }
                            ]
                        }
                    ],
                    "rotateStatus": False,
                    "definitionId": ""
                },
                "4eee8a0f-e72d-24b4-ae8f-e2493a1da402": {
                    "_type": "org.uengine.modeling.model.Actor",
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                    },
                    "description": None,
                    "id": "4eee8a0f-e72d-24b4-ae8f-e2493a1da402",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Actor",
                        "height": 100,
                        "id": "4eee8a0f-e72d-24b4-ae8f-e2493a1da402",
                        "style": "{}",
                        "width": 100,
                        "x": 1060,
                        "y": 250
                    },
                    "innerAggregate": {
                        "command": [],
                        "event": [],
                        "external": [],
                        "policy": [],
                        "view": []
                    },
                    "name": "사용자",
                    "oldName": "",
                    "rotateStatus": False
                },
                "11a22b70-9ac7-bbf2-66b1-60647ca80752": {
                    "_type": "org.uengine.modeling.model.Actor",
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                    },
                    "description": None,
                    "id": "11a22b70-9ac7-bbf2-66b1-60647ca80752",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Actor",
                        "height": 100,
                        "id": "11a22b70-9ac7-bbf2-66b1-60647ca80752",
                        "style": "{}",
                        "width": 100,
                        "x": 1060,
                        "y": 380
                    },
                    "innerAggregate": {
                        "command": [],
                        "event": [],
                        "external": [],
                        "policy": [],
                        "view": []
                    },
                    "name": "사용자",
                    "oldName": "",
                    "rotateStatus": False
                },
                "1a0d724e-ff36-0fe6-4887-b34b87958b31": {
                    "_type": "org.uengine.modeling.model.Actor",
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                    },
                    "description": None,
                    "id": "1a0d724e-ff36-0fe6-4887-b34b87958b31",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Actor",
                        "height": 100,
                        "id": "1a0d724e-ff36-0fe6-4887-b34b87958b31",
                        "style": "{}",
                        "width": 100,
                        "x": 1060,
                        "y": 510
                    },
                    "innerAggregate": {
                        "command": [],
                        "event": [],
                        "external": [],
                        "policy": [],
                        "view": []
                    },
                    "name": "사용자",
                    "oldName": "",
                    "rotateStatus": False
                },
                "d889f16d-4519-6b8a-7e56-f1dd4141235c": {
                    "_type": "org.uengine.modeling.model.Actor",
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                    },
                    "description": None,
                    "id": "d889f16d-4519-6b8a-7e56-f1dd4141235c",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Actor",
                        "height": 100,
                        "id": "d889f16d-4519-6b8a-7e56-f1dd4141235c",
                        "style": "{}",
                        "width": 100,
                        "x": 1060,
                        "y": 640
                    },
                    "innerAggregate": {
                        "command": [],
                        "event": [],
                        "external": [],
                        "policy": [],
                        "view": []
                    },
                    "name": "사용자",
                    "oldName": "",
                    "rotateStatus": False,
                    "displayName": ""
                },
                "76c5c940-5d8a-b57e-9c93-49ded3868763": {
                    "_type": "org.uengine.modeling.model.Actor",
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "boundedContext": {
                        "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                    },
                    "description": None,
                    "id": "76c5c940-5d8a-b57e-9c93-49ded3868763",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Actor",
                        "height": 100,
                        "id": "76c5c940-5d8a-b57e-9c93-49ded3868763",
                        "style": "{}",
                        "width": 100,
                        "x": 1060,
                        "y": 770
                    },
                    "innerAggregate": {
                        "command": [],
                        "event": [],
                        "external": [],
                        "policy": [],
                        "view": []
                    },
                    "name": "사용자",
                    "oldName": "",
                    "rotateStatus": False,
                    "displayName": ""
                }
            },
            "relations": {
                "40fb55f4-95bf-4b7a-13a8-691f894d3429": {
                    "_type": "org.uengine.modeling.model.Relation",
                    "name": "",
                    "id": "40fb55f4-95bf-4b7a-13a8-691f894d3429",
                    "sourceElement": {
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
                                    "19aa4d64-6084-e826-7c69-0bd1896e6f79": {
                                        "_type": "org.uengine.uml.model.Class",
                                        "id": "19aa4d64-6084-e826-7c69-0bd1896e6f79",
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
                                            "id": "19aa4d64-6084-e826-7c69-0bd1896e6f79",
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
                                        "parentId": "30176142-717c-cc1a-0d59-771539ac988a"
                                    },
                                    "7ec1a4ec-7237-ab46-0c52-fe21ca1a9a09": {
                                        "_type": "org.uengine.uml.model.enum",
                                        "id": "7ec1a4ec-7237-ab46-0c52-fe21ca1a9a09",
                                        "name": "TransactionType",
                                        "displayName": "거래 유형",
                                        "nameCamelCase": "transactionType",
                                        "namePascalCase": "TransactionType",
                                        "namePlural": "transactionTypes",
                                        "elementView": {
                                            "_type": "org.uengine.uml.model.enum",
                                            "id": "7ec1a4ec-7237-ab46-0c52-fe21ca1a9a09",
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
                            "name": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908",
                            "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                        },
                        "commands": [],
                        "description": None,
                        "id": "30176142-717c-cc1a-0d59-771539ac988a",
                        "elementView": {
                            "_type": "org.uengine.modeling.model.Aggregate",
                            "id": "30176142-717c-cc1a-0d59-771539ac988a",
                            "x": 1235,
                            "y": 450,
                            "width": 130,
                            "height": 400
                        },
                        "events": [],
                        "hexagonalView": {
                            "_type": "org.uengine.modeling.model.AggregateHexagonal",
                            "id": "30176142-717c-cc1a-0d59-771539ac988a",
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
                    },
                    "targetElement": {
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
                                    "aa6acc4d-3773-6aa9-3cf2-d22a860272a8": {
                                        "_type": "org.uengine.uml.model.Class",
                                        "id": "aa6acc4d-3773-6aa9-3cf2-d22a860272a8",
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
                                            "id": "aa6acc4d-3773-6aa9-3cf2-d22a860272a8",
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
                                        "parentId": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                                    },
                                    "3e68e3a2-7dd9-dab0-3d03-2753ba0a1233": {
                                        "_type": "org.uengine.uml.model.enum",
                                        "id": "3e68e3a2-7dd9-dab0-3d03-2753ba0a1233",
                                        "name": "Category",
                                        "displayName": "카테고리",
                                        "nameCamelCase": "category",
                                        "namePascalCase": "Category",
                                        "namePlural": "categories",
                                        "elementView": {
                                            "_type": "org.uengine.uml.model.enum",
                                            "id": "3e68e3a2-7dd9-dab0-3d03-2753ba0a1233",
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
                                    "73640bd2-3239-18e6-0c05-22462730ed92": {
                                        "_type": "org.uengine.uml.model.enum",
                                        "id": "73640bd2-3239-18e6-0c05-22462730ed92",
                                        "name": "Status",
                                        "displayName": "도서상태",
                                        "nameCamelCase": "status",
                                        "namePascalCase": "Status",
                                        "namePlural": "statuses",
                                        "elementView": {
                                            "_type": "org.uengine.uml.model.enum",
                                            "id": "73640bd2-3239-18e6-0c05-22462730ed92",
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
                            "name": "97f2473e-7068-21ee-652d-ba0a8f41dd2c",
                            "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                        },
                        "commands": [],
                        "description": None,
                        "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2",
                        "elementView": {
                            "_type": "org.uengine.modeling.model.Aggregate",
                            "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2",
                            "x": 650,
                            "y": 450,
                            "width": 130,
                            "height": 400
                        },
                        "events": [],
                        "hexagonalView": {
                            "_type": "org.uengine.modeling.model.AggregateHexagonal",
                            "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2",
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
                    "from": "30176142-717c-cc1a-0d59-771539ac988a",
                    "to": "f81e4c75-040c-83ad-4656-65cfccc74cc2",
                    "relationView": {
                        "id": "40fb55f4-95bf-4b7a-13a8-691f894d3429",
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "from": "30176142-717c-cc1a-0d59-771539ac988a",
                        "to": "f81e4c75-040c-83ad-4656-65cfccc74cc2",
                        "needReconnect": True,
                        "value": "[[1170,456],[715,456]]"
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.RelationHexagonal",
                        "from": "30176142-717c-cc1a-0d59-771539ac988a",
                        "id": "40fb55f4-95bf-4b7a-13a8-691f894d3429",
                        "needReconnect": True,
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "to": "f81e4c75-040c-83ad-4656-65cfccc74cc2",
                        "value": None
                    },
                    "sourceMultiplicity": "1",
                    "targetMultiplicity": "1",
                    "displayName": ""
                },
                "73d6bd51-2b4d-5480-b155-7ed5bc740b4d": {
                    "_type": "org.uengine.modeling.model.Relation",
                    "name": "",
                    "id": "73d6bd51-2b4d-5480-b155-7ed5bc740b4d",
                    "sourceElement": {
                        "_type": "org.uengine.modeling.model.Command",
                        "outputEvents": [
                            "BookRegistered"
                        ],
                        "aggregate": {
                            "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                        },
                        "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                        "boundedContext": {
                            "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                        },
                        "controllerInfo": {
                            "apiPath": "registerbook",
                            "method": "POST",
                            "fullApiPath": ""
                        },
                        "fieldDescriptors": [
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": True,
                                "name": "ISBN",
                                "nameCamelCase": "isbn",
                                "namePascalCase": "Isbn",
                                "displayName": "",
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
                                "_type": "org.uengine.model.FieldDescriptor"
                            }
                        ],
                        "description": None,
                        "id": "9dfd77c4-7bb3-6a62-025d-633c63438cf6",
                        "elementView": {
                            "_type": "org.uengine.modeling.model.Command",
                            "height": 116,
                            "id": "9dfd77c4-7bb3-6a62-025d-633c63438cf6",
                            "style": "{}",
                            "width": 100,
                            "x": 556,
                            "y": 250,
                            "z-index": 999
                        },
                        "hexagonalView": {
                            "_type": "org.uengine.modeling.model.CommandHexagonal",
                            "height": 0,
                            "id": "9dfd77c4-7bb3-6a62-025d-633c63438cf6",
                            "style": "{}",
                            "width": 0,
                            "x": 0,
                            "y": 0
                        },
                        "isRestRepository": False,
                        "name": "RegisterBook",
                        "displayName": "도서 등록",
                        "nameCamelCase": "registerBook",
                        "namePascalCase": "RegisterBook",
                        "namePlural": "registerBooks",
                        "relationCommandInfo": [],
                        "relationEventInfo": [],
                        "restRepositoryInfo": {
                            "method": "POST"
                        },
                        "rotateStatus": False,
                        "selected": False,
                        "trigger": "@PrePersist"
                    },
                    "targetElement": {
                        "alertURL": "/static/image/symbol/alert-icon.png",
                        "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                        "checkAlert": True,
                        "description": None,
                        "id": "dc9f7be6-103e-0d9f-96b6-a1de4ae31d3f",
                        "elementView": {
                            "angle": 0,
                            "height": 116,
                            "id": "dc9f7be6-103e-0d9f-96b6-a1de4ae31d3f",
                            "style": "{}",
                            "width": 100,
                            "x": 744,
                            "y": 250,
                            "_type": "org.uengine.modeling.model.Event"
                        },
                        "fieldDescriptors": [
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": True,
                                "name": "ISBN",
                                "nameCamelCase": "isbn",
                                "namePascalCase": "Isbn",
                                "displayName": "",
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
                                "_type": "org.uengine.model.FieldDescriptor"
                            }
                        ],
                        "hexagonalView": {
                            "height": 0,
                            "id": "dc9f7be6-103e-0d9f-96b6-a1de4ae31d3f",
                            "style": "{}",
                            "width": 0,
                            "x": 0,
                            "y": 0,
                            "_type": "org.uengine.modeling.model.EventHexagonal"
                        },
                        "name": "BookRegistered",
                        "displayName": "도서 등록됨",
                        "nameCamelCase": "bookRegistered",
                        "namePascalCase": "BookRegistered",
                        "namePlural": "",
                        "relationCommandInfo": [],
                        "relationPolicyInfo": [],
                        "rotateStatus": False,
                        "selected": False,
                        "trigger": "@PostPersist",
                        "_type": "org.uengine.modeling.model.Event",
                        "aggregate": {
                            "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                        },
                        "boundedContext": {
                            "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                        }
                    },
                    "from": "9dfd77c4-7bb3-6a62-025d-633c63438cf6",
                    "to": "dc9f7be6-103e-0d9f-96b6-a1de4ae31d3f",
                    "relationView": {
                        "id": "73d6bd51-2b4d-5480-b155-7ed5bc740b4d",
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "from": "9dfd77c4-7bb3-6a62-025d-633c63438cf6",
                        "to": "dc9f7be6-103e-0d9f-96b6-a1de4ae31d3f",
                        "needReconnect": True,
                        "value": "[[606,252],[694,252]]"
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.RelationHexagonal",
                        "from": "9dfd77c4-7bb3-6a62-025d-633c63438cf6",
                        "id": "73d6bd51-2b4d-5480-b155-7ed5bc740b4d",
                        "needReconnect": True,
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "to": "dc9f7be6-103e-0d9f-96b6-a1de4ae31d3f",
                        "value": None
                    },
                    "sourceMultiplicity": "1",
                    "targetMultiplicity": "1"
                },
                "6f42b17c-7bd9-9117-931f-b86209dcb1a8": {
                    "_type": "org.uengine.modeling.model.Relation",
                    "name": "",
                    "id": "6f42b17c-7bd9-9117-931f-b86209dcb1a8",
                    "sourceElement": {
                        "_type": "org.uengine.modeling.model.Command",
                        "outputEvents": [
                            "BookStatusChanged"
                        ],
                        "aggregate": {
                            "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                        },
                        "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                        "boundedContext": {
                            "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                        },
                        "controllerInfo": {
                            "apiPath": "changebookstatus",
                            "method": "PUT",
                            "fullApiPath": ""
                        },
                        "fieldDescriptors": [
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": True,
                                "name": "ISBN",
                                "nameCamelCase": "isbn",
                                "namePascalCase": "Isbn",
                                "displayName": "",
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
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": False,
                                "name": "reason",
                                "nameCamelCase": "reason",
                                "namePascalCase": "Reason",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            }
                        ],
                        "description": None,
                        "id": "279c5170-159b-2b0d-34fa-e2e42dd5e0a9",
                        "elementView": {
                            "_type": "org.uengine.modeling.model.Command",
                            "height": 116,
                            "id": "279c5170-159b-2b0d-34fa-e2e42dd5e0a9",
                            "style": "{}",
                            "width": 100,
                            "x": 556,
                            "y": 380,
                            "z-index": 999
                        },
                        "hexagonalView": {
                            "_type": "org.uengine.modeling.model.CommandHexagonal",
                            "height": 0,
                            "id": "279c5170-159b-2b0d-34fa-e2e42dd5e0a9",
                            "style": "{}",
                            "width": 0,
                            "x": 0,
                            "y": 0
                        },
                        "isRestRepository": False,
                        "name": "ChangeBookStatus",
                        "displayName": "도서 상태 변경",
                        "nameCamelCase": "changeBookStatus",
                        "namePascalCase": "ChangeBookStatus",
                        "namePlural": "changeBookStatuses",
                        "relationCommandInfo": [],
                        "relationEventInfo": [],
                        "restRepositoryInfo": {
                            "method": "PUT"
                        },
                        "rotateStatus": False,
                        "selected": False,
                        "trigger": "@PrePersist"
                    },
                    "targetElement": {
                        "alertURL": "/static/image/symbol/alert-icon.png",
                        "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                        "checkAlert": True,
                        "description": None,
                        "id": "c763f4a6-b0e9-0a7e-e343-c8de448157bd",
                        "elementView": {
                            "angle": 0,
                            "height": 116,
                            "id": "c763f4a6-b0e9-0a7e-e343-c8de448157bd",
                            "style": "{}",
                            "width": 100,
                            "x": 744,
                            "y": 380,
                            "_type": "org.uengine.modeling.model.Event"
                        },
                        "fieldDescriptors": [
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": True,
                                "name": "ISBN",
                                "nameCamelCase": "isbn",
                                "namePascalCase": "Isbn",
                                "displayName": "",
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
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Date",
                                "isCopy": False,
                                "isKey": False,
                                "name": "changedAt",
                                "nameCamelCase": "changedAt",
                                "namePascalCase": "ChangedAt",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": False,
                                "name": "reason",
                                "nameCamelCase": "reason",
                                "namePascalCase": "Reason",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            }
                        ],
                        "hexagonalView": {
                            "height": 0,
                            "id": "c763f4a6-b0e9-0a7e-e343-c8de448157bd",
                            "style": "{}",
                            "width": 0,
                            "x": 0,
                            "y": 0,
                            "_type": "org.uengine.modeling.model.EventHexagonal"
                        },
                        "name": "BookStatusChanged",
                        "displayName": "도서 상태 변경됨",
                        "nameCamelCase": "bookStatusChanged",
                        "namePascalCase": "BookStatusChanged",
                        "namePlural": "",
                        "relationCommandInfo": [],
                        "relationPolicyInfo": [],
                        "rotateStatus": False,
                        "selected": False,
                        "trigger": "@PostPersist",
                        "_type": "org.uengine.modeling.model.Event",
                        "aggregate": {
                            "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                        },
                        "boundedContext": {
                            "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                        }
                    },
                    "from": "279c5170-159b-2b0d-34fa-e2e42dd5e0a9",
                    "to": "c763f4a6-b0e9-0a7e-e343-c8de448157bd",
                    "relationView": {
                        "id": "6f42b17c-7bd9-9117-931f-b86209dcb1a8",
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "from": "279c5170-159b-2b0d-34fa-e2e42dd5e0a9",
                        "to": "c763f4a6-b0e9-0a7e-e343-c8de448157bd",
                        "needReconnect": True,
                        "value": "[[606,380],[694,380]]"
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.RelationHexagonal",
                        "from": "279c5170-159b-2b0d-34fa-e2e42dd5e0a9",
                        "id": "6f42b17c-7bd9-9117-931f-b86209dcb1a8",
                        "needReconnect": True,
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "to": "c763f4a6-b0e9-0a7e-e343-c8de448157bd",
                        "value": None
                    },
                    "sourceMultiplicity": "1",
                    "targetMultiplicity": "1"
                },
                "68915ca5-a8d0-c4a5-3de7-222f4c8d8059": {
                    "_type": "org.uengine.modeling.model.Relation",
                    "name": "",
                    "id": "68915ca5-a8d0-c4a5-3de7-222f4c8d8059",
                    "sourceElement": {
                        "_type": "org.uengine.modeling.model.Command",
                        "outputEvents": [
                            "BookDiscarded"
                        ],
                        "aggregate": {
                            "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                        },
                        "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                        "boundedContext": {
                            "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                        },
                        "controllerInfo": {
                            "apiPath": "discardbook",
                            "method": "PUT",
                            "fullApiPath": ""
                        },
                        "fieldDescriptors": [
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": True,
                                "name": "ISBN",
                                "nameCamelCase": "isbn",
                                "namePascalCase": "Isbn",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": False,
                                "name": "discardReason",
                                "nameCamelCase": "discardReason",
                                "namePascalCase": "DiscardReason",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            }
                        ],
                        "description": None,
                        "id": "b6d57c04-edb1-c660-ea90-b0ef48b57dd1",
                        "elementView": {
                            "_type": "org.uengine.modeling.model.Command",
                            "height": 116,
                            "id": "b6d57c04-edb1-c660-ea90-b0ef48b57dd1",
                            "style": "{}",
                            "width": 100,
                            "x": 556,
                            "y": 510,
                            "z-index": 999
                        },
                        "hexagonalView": {
                            "_type": "org.uengine.modeling.model.CommandHexagonal",
                            "height": 0,
                            "id": "b6d57c04-edb1-c660-ea90-b0ef48b57dd1",
                            "style": "{}",
                            "width": 0,
                            "x": 0,
                            "y": 0
                        },
                        "isRestRepository": False,
                        "name": "DiscardBook",
                        "displayName": "도서 폐기",
                        "nameCamelCase": "discardBook",
                        "namePascalCase": "DiscardBook",
                        "namePlural": "discardBooks",
                        "relationCommandInfo": [],
                        "relationEventInfo": [],
                        "restRepositoryInfo": {
                            "method": "PUT"
                        },
                        "rotateStatus": False,
                        "selected": False,
                        "trigger": "@PrePersist"
                    },
                    "targetElement": {
                        "alertURL": "/static/image/symbol/alert-icon.png",
                        "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                        "checkAlert": True,
                        "description": None,
                        "id": "bdad54b2-d2ba-9e60-f28e-4959a9d55f42",
                        "elementView": {
                            "angle": 0,
                            "height": 116,
                            "id": "bdad54b2-d2ba-9e60-f28e-4959a9d55f42",
                            "style": "{}",
                            "width": 100,
                            "x": 744,
                            "y": 510,
                            "_type": "org.uengine.modeling.model.Event"
                        },
                        "fieldDescriptors": [
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": True,
                                "name": "ISBN",
                                "nameCamelCase": "isbn",
                                "namePascalCase": "Isbn",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": False,
                                "name": "discardReason",
                                "nameCamelCase": "discardReason",
                                "namePascalCase": "DiscardReason",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Date",
                                "isCopy": False,
                                "isKey": False,
                                "name": "discardedAt",
                                "nameCamelCase": "discardedAt",
                                "namePascalCase": "DiscardedAt",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            }
                        ],
                        "hexagonalView": {
                            "height": 0,
                            "id": "bdad54b2-d2ba-9e60-f28e-4959a9d55f42",
                            "style": "{}",
                            "width": 0,
                            "x": 0,
                            "y": 0,
                            "_type": "org.uengine.modeling.model.EventHexagonal"
                        },
                        "name": "BookDiscarded",
                        "displayName": "도서 폐기됨",
                        "nameCamelCase": "bookDiscarded",
                        "namePascalCase": "BookDiscarded",
                        "namePlural": "",
                        "relationCommandInfo": [],
                        "relationPolicyInfo": [],
                        "rotateStatus": False,
                        "selected": False,
                        "trigger": "@PostPersist",
                        "_type": "org.uengine.modeling.model.Event",
                        "aggregate": {
                            "id": "f81e4c75-040c-83ad-4656-65cfccc74cc2"
                        },
                        "boundedContext": {
                            "id": "97f2473e-7068-21ee-652d-ba0a8f41dd2c"
                        }
                    },
                    "from": "b6d57c04-edb1-c660-ea90-b0ef48b57dd1",
                    "to": "bdad54b2-d2ba-9e60-f28e-4959a9d55f42",
                    "relationView": {
                        "id": "68915ca5-a8d0-c4a5-3de7-222f4c8d8059",
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "from": "b6d57c04-edb1-c660-ea90-b0ef48b57dd1",
                        "to": "bdad54b2-d2ba-9e60-f28e-4959a9d55f42",
                        "needReconnect": True,
                        "value": "[[606,512],[694,512]]"
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.RelationHexagonal",
                        "from": "b6d57c04-edb1-c660-ea90-b0ef48b57dd1",
                        "id": "68915ca5-a8d0-c4a5-3de7-222f4c8d8059",
                        "needReconnect": True,
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "to": "bdad54b2-d2ba-9e60-f28e-4959a9d55f42",
                        "value": None
                    },
                    "sourceMultiplicity": "1",
                    "targetMultiplicity": "1"
                },
                "6b1b17ec-5f86-f717-4d56-c65562851bf7": {
                    "_type": "org.uengine.modeling.model.Relation",
                    "name": "",
                    "id": "6b1b17ec-5f86-f717-4d56-c65562851bf7",
                    "sourceElement": {
                        "_type": "org.uengine.modeling.model.Command",
                        "outputEvents": [
                            "Loaned"
                        ],
                        "aggregate": {
                            "id": "30176142-717c-cc1a-0d59-771539ac988a"
                        },
                        "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                        "boundedContext": {
                            "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                        },
                        "controllerInfo": {
                            "apiPath": "loanbook",
                            "method": "POST",
                            "fullApiPath": ""
                        },
                        "fieldDescriptors": [
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": True,
                                "name": "memberNumber",
                                "nameCamelCase": "memberNumber",
                                "namePascalCase": "MemberNumber",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": False,
                                "name": "memberName",
                                "nameCamelCase": "memberName",
                                "namePascalCase": "MemberName",
                                "displayName": "",
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
                                "_type": "org.uengine.model.FieldDescriptor"
                            }
                        ],
                        "description": None,
                        "id": "7a421b31-a5ff-c17c-076f-a700e59be8fd",
                        "elementView": {
                            "_type": "org.uengine.modeling.model.Command",
                            "height": 116,
                            "id": "7a421b31-a5ff-c17c-076f-a700e59be8fd",
                            "style": "{}",
                            "width": 100,
                            "x": 1141,
                            "y": 250,
                            "z-index": 999
                        },
                        "hexagonalView": {
                            "_type": "org.uengine.modeling.model.CommandHexagonal",
                            "height": 0,
                            "id": "7a421b31-a5ff-c17c-076f-a700e59be8fd",
                            "style": "{}",
                            "width": 0,
                            "x": 0,
                            "y": 0
                        },
                        "isRestRepository": False,
                        "name": "LoanBook",
                        "displayName": "도서 대출 신청",
                        "nameCamelCase": "loanBook",
                        "namePascalCase": "LoanBook",
                        "namePlural": "loanBooks",
                        "relationCommandInfo": [],
                        "relationEventInfo": [],
                        "restRepositoryInfo": {
                            "method": "POST"
                        },
                        "rotateStatus": False,
                        "selected": False,
                        "trigger": "@PrePersist"
                    },
                    "targetElement": {
                        "alertURL": "/static/image/symbol/alert-icon.png",
                        "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                        "checkAlert": True,
                        "description": None,
                        "id": "b12ad8fd-6404-c544-5ff8-b5bc1fdcae20",
                        "elementView": {
                            "angle": 0,
                            "height": 116,
                            "id": "b12ad8fd-6404-c544-5ff8-b5bc1fdcae20",
                            "style": "{}",
                            "width": 100,
                            "x": 1329,
                            "y": 250,
                            "_type": "org.uengine.modeling.model.Event"
                        },
                        "fieldDescriptors": [
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": True,
                                "name": "loanId",
                                "nameCamelCase": "loanId",
                                "namePascalCase": "LoanId",
                                "displayName": "",
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
                                "_type": "org.uengine.model.FieldDescriptor"
                            }
                        ],
                        "hexagonalView": {
                            "height": 0,
                            "id": "b12ad8fd-6404-c544-5ff8-b5bc1fdcae20",
                            "style": "{}",
                            "width": 0,
                            "x": 0,
                            "y": 0,
                            "_type": "org.uengine.modeling.model.EventHexagonal"
                        },
                        "name": "Loaned",
                        "displayName": "도서 대출 완료",
                        "nameCamelCase": "loaned",
                        "namePascalCase": "Loaned",
                        "namePlural": "",
                        "relationCommandInfo": [],
                        "relationPolicyInfo": [],
                        "rotateStatus": False,
                        "selected": False,
                        "trigger": "@PostPersist",
                        "_type": "org.uengine.modeling.model.Event",
                        "aggregate": {
                            "id": "30176142-717c-cc1a-0d59-771539ac988a"
                        },
                        "boundedContext": {
                            "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                        }
                    },
                    "from": "7a421b31-a5ff-c17c-076f-a700e59be8fd",
                    "to": "b12ad8fd-6404-c544-5ff8-b5bc1fdcae20",
                    "relationView": {
                        "id": "6b1b17ec-5f86-f717-4d56-c65562851bf7",
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "from": "7a421b31-a5ff-c17c-076f-a700e59be8fd",
                        "to": "b12ad8fd-6404-c544-5ff8-b5bc1fdcae20",
                        "needReconnect": True,
                        "value": "[[1191,252],[1279,252]]"
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.RelationHexagonal",
                        "from": "7a421b31-a5ff-c17c-076f-a700e59be8fd",
                        "id": "6b1b17ec-5f86-f717-4d56-c65562851bf7",
                        "needReconnect": True,
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "to": "b12ad8fd-6404-c544-5ff8-b5bc1fdcae20",
                        "value": None
                    },
                    "sourceMultiplicity": "1",
                    "targetMultiplicity": "1"
                },
                "c962a7d8-870a-f0de-ca15-dc79298c7567": {
                    "_type": "org.uengine.modeling.model.Relation",
                    "name": "",
                    "id": "c962a7d8-870a-f0de-ca15-dc79298c7567",
                    "sourceElement": {
                        "_type": "org.uengine.modeling.model.Command",
                        "outputEvents": [
                            "Returned"
                        ],
                        "aggregate": {
                            "id": "30176142-717c-cc1a-0d59-771539ac988a"
                        },
                        "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                        "boundedContext": {
                            "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                        },
                        "controllerInfo": {
                            "apiPath": "returnbook",
                            "method": "POST",
                            "fullApiPath": ""
                        },
                        "fieldDescriptors": [
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": True,
                                "name": "loanId",
                                "nameCamelCase": "loanId",
                                "namePascalCase": "LoanId",
                                "displayName": "",
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
                                "_type": "org.uengine.model.FieldDescriptor"
                            }
                        ],
                        "description": None,
                        "id": "621d4bda-16fd-1bda-d837-89991959fbb2",
                        "elementView": {
                            "_type": "org.uengine.modeling.model.Command",
                            "height": 116,
                            "id": "621d4bda-16fd-1bda-d837-89991959fbb2",
                            "style": "{}",
                            "width": 100,
                            "x": 1141,
                            "y": 380,
                            "z-index": 999
                        },
                        "hexagonalView": {
                            "_type": "org.uengine.modeling.model.CommandHexagonal",
                            "height": 0,
                            "id": "621d4bda-16fd-1bda-d837-89991959fbb2",
                            "style": "{}",
                            "width": 0,
                            "x": 0,
                            "y": 0
                        },
                        "isRestRepository": False,
                        "name": "ReturnBook",
                        "displayName": "도서 반납 처리",
                        "nameCamelCase": "returnBook",
                        "namePascalCase": "ReturnBook",
                        "namePlural": "returnBooks",
                        "relationCommandInfo": [],
                        "relationEventInfo": [],
                        "restRepositoryInfo": {
                            "method": "POST"
                        },
                        "rotateStatus": False,
                        "selected": False,
                        "trigger": "@PrePersist"
                    },
                    "targetElement": {
                        "alertURL": "/static/image/symbol/alert-icon.png",
                        "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                        "checkAlert": True,
                        "description": None,
                        "id": "7134ee93-d752-ba68-bcd8-c39788567f0f",
                        "elementView": {
                            "angle": 0,
                            "height": 116,
                            "id": "7134ee93-d752-ba68-bcd8-c39788567f0f",
                            "style": "{}",
                            "width": 100,
                            "x": 1329,
                            "y": 380,
                            "_type": "org.uengine.modeling.model.Event"
                        },
                        "fieldDescriptors": [
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": True,
                                "name": "loanId",
                                "nameCamelCase": "loanId",
                                "namePascalCase": "LoanId",
                                "displayName": "",
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
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Date",
                                "isCopy": False,
                                "isKey": False,
                                "name": "returnedDate",
                                "nameCamelCase": "returnedDate",
                                "namePascalCase": "ReturnedDate",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            }
                        ],
                        "hexagonalView": {
                            "height": 0,
                            "id": "7134ee93-d752-ba68-bcd8-c39788567f0f",
                            "style": "{}",
                            "width": 0,
                            "x": 0,
                            "y": 0,
                            "_type": "org.uengine.modeling.model.EventHexagonal"
                        },
                        "name": "Returned",
                        "displayName": "도서 반납 완료",
                        "nameCamelCase": "returned",
                        "namePascalCase": "Returned",
                        "namePlural": "",
                        "relationCommandInfo": [],
                        "relationPolicyInfo": [],
                        "rotateStatus": False,
                        "selected": False,
                        "trigger": "@PostPersist",
                        "_type": "org.uengine.modeling.model.Event",
                        "aggregate": {
                            "id": "30176142-717c-cc1a-0d59-771539ac988a"
                        },
                        "boundedContext": {
                            "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                        }
                    },
                    "from": "621d4bda-16fd-1bda-d837-89991959fbb2",
                    "to": "7134ee93-d752-ba68-bcd8-c39788567f0f",
                    "relationView": {
                        "id": "c962a7d8-870a-f0de-ca15-dc79298c7567",
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "from": "621d4bda-16fd-1bda-d837-89991959fbb2",
                        "to": "7134ee93-d752-ba68-bcd8-c39788567f0f",
                        "needReconnect": True,
                        "value": "[[1191,380],[1279,380]]"
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.RelationHexagonal",
                        "from": "621d4bda-16fd-1bda-d837-89991959fbb2",
                        "id": "c962a7d8-870a-f0de-ca15-dc79298c7567",
                        "needReconnect": True,
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "to": "7134ee93-d752-ba68-bcd8-c39788567f0f",
                        "value": None
                    },
                    "sourceMultiplicity": "1",
                    "targetMultiplicity": "1"
                },
                "ceaa5350-4648-a1dc-426c-4ecd5d4542fa": {
                    "_type": "org.uengine.modeling.model.Relation",
                    "name": "",
                    "id": "ceaa5350-4648-a1dc-426c-4ecd5d4542fa",
                    "sourceElement": {
                        "_type": "org.uengine.modeling.model.Command",
                        "outputEvents": [
                            "Reserved"
                        ],
                        "aggregate": {
                            "id": "30176142-717c-cc1a-0d59-771539ac988a"
                        },
                        "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                        "boundedContext": {
                            "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                        },
                        "controllerInfo": {
                            "apiPath": "reservebook",
                            "method": "POST",
                            "fullApiPath": ""
                        },
                        "fieldDescriptors": [
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": True,
                                "name": "memberNumber",
                                "nameCamelCase": "memberNumber",
                                "namePascalCase": "MemberNumber",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": False,
                                "name": "memberName",
                                "nameCamelCase": "memberName",
                                "namePascalCase": "MemberName",
                                "displayName": "",
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
                                "_type": "org.uengine.model.FieldDescriptor"
                            }
                        ],
                        "description": None,
                        "id": "e9506a41-7406-7ded-e91a-81c2dd99da75",
                        "elementView": {
                            "_type": "org.uengine.modeling.model.Command",
                            "height": 116,
                            "id": "e9506a41-7406-7ded-e91a-81c2dd99da75",
                            "style": "{}",
                            "width": 100,
                            "x": 1141,
                            "y": 510,
                            "z-index": 999
                        },
                        "hexagonalView": {
                            "_type": "org.uengine.modeling.model.CommandHexagonal",
                            "height": 0,
                            "id": "e9506a41-7406-7ded-e91a-81c2dd99da75",
                            "style": "{}",
                            "width": 0,
                            "x": 0,
                            "y": 0
                        },
                        "isRestRepository": False,
                        "name": "ReserveBook",
                        "displayName": "도서 예약 신청",
                        "nameCamelCase": "reserveBook",
                        "namePascalCase": "ReserveBook",
                        "namePlural": "reserveBooks",
                        "relationCommandInfo": [],
                        "relationEventInfo": [],
                        "restRepositoryInfo": {
                            "method": "POST"
                        },
                        "rotateStatus": False,
                        "selected": False,
                        "trigger": "@PrePersist"
                    },
                    "targetElement": {
                        "alertURL": "/static/image/symbol/alert-icon.png",
                        "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                        "checkAlert": True,
                        "description": None,
                        "id": "e5cb69a8-8001-cf81-d4da-fffd1401afe5",
                        "elementView": {
                            "angle": 0,
                            "height": 116,
                            "id": "e5cb69a8-8001-cf81-d4da-fffd1401afe5",
                            "style": "{}",
                            "width": 100,
                            "x": 1329,
                            "y": 510,
                            "_type": "org.uengine.modeling.model.Event"
                        },
                        "fieldDescriptors": [
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": True,
                                "name": "reservationId",
                                "nameCamelCase": "reservationId",
                                "namePascalCase": "ReservationId",
                                "displayName": "",
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
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Date",
                                "isCopy": False,
                                "isKey": False,
                                "name": "reservedDate",
                                "nameCamelCase": "reservedDate",
                                "namePascalCase": "ReservedDate",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            }
                        ],
                        "hexagonalView": {
                            "height": 0,
                            "id": "e5cb69a8-8001-cf81-d4da-fffd1401afe5",
                            "style": "{}",
                            "width": 0,
                            "x": 0,
                            "y": 0,
                            "_type": "org.uengine.modeling.model.EventHexagonal"
                        },
                        "name": "Reserved",
                        "displayName": "도서 예약 완료",
                        "nameCamelCase": "reserved",
                        "namePascalCase": "Reserved",
                        "namePlural": "",
                        "relationCommandInfo": [],
                        "relationPolicyInfo": [],
                        "rotateStatus": False,
                        "selected": False,
                        "trigger": "@PostPersist",
                        "_type": "org.uengine.modeling.model.Event",
                        "aggregate": {
                            "id": "30176142-717c-cc1a-0d59-771539ac988a"
                        },
                        "boundedContext": {
                            "id": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908"
                        }
                    },
                    "from": "e9506a41-7406-7ded-e91a-81c2dd99da75",
                    "to": "e5cb69a8-8001-cf81-d4da-fffd1401afe5",
                    "relationView": {
                        "id": "ceaa5350-4648-a1dc-426c-4ecd5d4542fa",
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "from": "e9506a41-7406-7ded-e91a-81c2dd99da75",
                        "to": "e5cb69a8-8001-cf81-d4da-fffd1401afe5",
                        "needReconnect": True,
                        "value": "[[1191,512],[1279,512]]"
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.RelationHexagonal",
                        "from": "e9506a41-7406-7ded-e91a-81c2dd99da75",
                        "id": "ceaa5350-4648-a1dc-426c-4ecd5d4542fa",
                        "needReconnect": True,
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "to": "e5cb69a8-8001-cf81-d4da-fffd1401afe5",
                        "value": None
                    },
                    "sourceMultiplicity": "1",
                    "targetMultiplicity": "1"
                }
            },
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
            "97f2473e-7068-21ee-652d-ba0a8f41dd2c": "bc-bookManagement",
            "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908": "bc-loanManagement",
            "f81e4c75-040c-83ad-4656-65cfccc74cc2": "agg-book",
            "aa6acc4d-3773-6aa9-3cf2-d22a860272a8": "agg-root-book",
            "3e68e3a2-7dd9-dab0-3d03-2753ba0a1233": "enum-category",
            "73640bd2-3239-18e6-0c05-22462730ed92": "enum-status",
            "30176142-717c-cc1a-0d59-771539ac988a": "agg-loanTransaction",
            "19aa4d64-6084-e826-7c69-0bd1896e6f79": "agg-root-loanTransaction",
            "7ec1a4ec-7237-ab46-0c52-fe21ca1a9a09": "enum-transactionType",
            "9b7dd1cc-d76b-2b36-1f93-9eb8930afef6": "vo-bookId",
            "dc9f7be6-103e-0d9f-96b6-a1de4ae31d3f": "evt-bookRegistered",
            "c763f4a6-b0e9-0a7e-e343-c8de448157bd": "evt-bookStatusChanged",
            "bdad54b2-d2ba-9e60-f28e-4959a9d55f42": "evt-bookDiscarded",
            "9dfd77c4-7bb3-6a62-025d-633c63438cf6": "cmd-registerBook",
            "279c5170-159b-2b0d-34fa-e2e42dd5e0a9": "cmd-changeBookStatus",
            "b6d57c04-edb1-c660-ea90-b0ef48b57dd1": "cmd-discardBook",
            "76fa37dc-33e3-9cb1-a9e6-90695b09cb40": "rm-bookList",
            "cec595c2-bb4c-e116-de82-b514c8d38926": "rm-bookDetails",
            "48266e6a-49b8-a87b-10d3-ba1702401d61": "act-사용자",
            "39998ac0-1667-efba-4c66-936c1c7827ae": "act-사용자-2",
            "14f9b8d9-e377-cec8-c1b5-45cd402bfad7": "act-사용자-3",
            "c4db0e92-3b28-e623-3a23-a8403a3ddff7": "act-사용자-4",
            "5a6c7a17-38f7-5f5a-23c5-11c2dd454202": "act-사용자-5",
            "b12ad8fd-6404-c544-5ff8-b5bc1fdcae20": "evt-loaned",
            "7134ee93-d752-ba68-bcd8-c39788567f0f": "evt-returned",
            "e5cb69a8-8001-cf81-d4da-fffd1401afe5": "evt-reserved",
            "7a421b31-a5ff-c17c-076f-a700e59be8fd": "cmd-loanBook",
            "621d4bda-16fd-1bda-d837-89991959fbb2": "cmd-returnBook",
            "e9506a41-7406-7ded-e91a-81c2dd99da75": "cmd-reserveBook",
            "692ff79a-552f-1049-965c-f6c780405f7a": "rm-loanHistory",
            "de913c2b-ea86-6d51-9b46-f66a42712964": "rm-loanCurrentStatus",
            "4eee8a0f-e72d-24b4-ae8f-e2493a1da402": "act-사용자-6",
            "11a22b70-9ac7-bbf2-66b1-60647ca80752": "act-사용자-7",
            "1a0d724e-ff36-0fe6-4887-b34b87958b31": "act-사용자-8",
            "d889f16d-4519-6b8a-7e56-f1dd4141235c": "act-사용자-9",
            "76c5c940-5d8a-b57e-9c93-49ded3868763": "act-사용자-10",
            "40fb55f4-95bf-4b7a-13a8-691f894d3429": "agg-loanTransaction-to-agg-book",
            "73d6bd51-2b4d-5480-b155-7ed5bc740b4d": "cmd-registerBook-to-evt-bookRegistered",
            "6f42b17c-7bd9-9117-931f-b86209dcb1a8": "cmd-changeBookStatus-to-evt-bookStatusChanged",
            "68915ca5-a8d0-c4a5-3de7-222f4c8d8059": "cmd-discardBook-to-evt-bookDiscarded",
            "6b1b17ec-5f86-f717-4d56-c65562851bf7": "cmd-loanBook-to-evt-loaned",
            "c962a7d8-870a-f0de-ca15-dc79298c7567": "cmd-returnBook-to-evt-returned",
            "ceaa5350-4648-a1dc-426c-4ecd5d4542fa": "cmd-reserveBook-to-evt-reserved"
        },
        "aliasToUUIDDic": {
            "bc-bookManagement": "97f2473e-7068-21ee-652d-ba0a8f41dd2c",
            "bc-loanManagement": "4fc9eb9f-f332-e3e6-43d3-0bb9f1b16908",
            "agg-book": "f81e4c75-040c-83ad-4656-65cfccc74cc2",
            "agg-root-book": "aa6acc4d-3773-6aa9-3cf2-d22a860272a8",
            "enum-category": "3e68e3a2-7dd9-dab0-3d03-2753ba0a1233",
            "enum-status": "73640bd2-3239-18e6-0c05-22462730ed92",
            "agg-loanTransaction": "30176142-717c-cc1a-0d59-771539ac988a",
            "agg-root-loanTransaction": "19aa4d64-6084-e826-7c69-0bd1896e6f79",
            "enum-transactionType": "7ec1a4ec-7237-ab46-0c52-fe21ca1a9a09",
            "vo-bookId": "9b7dd1cc-d76b-2b36-1f93-9eb8930afef6",
            "evt-bookRegistered": "dc9f7be6-103e-0d9f-96b6-a1de4ae31d3f",
            "evt-bookStatusChanged": "c763f4a6-b0e9-0a7e-e343-c8de448157bd",
            "evt-bookDiscarded": "bdad54b2-d2ba-9e60-f28e-4959a9d55f42",
            "cmd-registerBook": "9dfd77c4-7bb3-6a62-025d-633c63438cf6",
            "cmd-changeBookStatus": "279c5170-159b-2b0d-34fa-e2e42dd5e0a9",
            "cmd-discardBook": "b6d57c04-edb1-c660-ea90-b0ef48b57dd1",
            "rm-bookList": "76fa37dc-33e3-9cb1-a9e6-90695b09cb40",
            "rm-bookDetails": "cec595c2-bb4c-e116-de82-b514c8d38926",
            "act-사용자": "48266e6a-49b8-a87b-10d3-ba1702401d61",
            "act-사용자-2": "39998ac0-1667-efba-4c66-936c1c7827ae",
            "act-사용자-3": "14f9b8d9-e377-cec8-c1b5-45cd402bfad7",
            "act-사용자-4": "c4db0e92-3b28-e623-3a23-a8403a3ddff7",
            "act-사용자-5": "5a6c7a17-38f7-5f5a-23c5-11c2dd454202",
            "evt-loaned": "b12ad8fd-6404-c544-5ff8-b5bc1fdcae20",
            "evt-returned": "7134ee93-d752-ba68-bcd8-c39788567f0f",
            "evt-reserved": "e5cb69a8-8001-cf81-d4da-fffd1401afe5",
            "cmd-loanBook": "7a421b31-a5ff-c17c-076f-a700e59be8fd",
            "cmd-returnBook": "621d4bda-16fd-1bda-d837-89991959fbb2",
            "cmd-reserveBook": "e9506a41-7406-7ded-e91a-81c2dd99da75",
            "rm-loanHistory": "692ff79a-552f-1049-965c-f6c780405f7a",
            "rm-loanCurrentStatus": "de913c2b-ea86-6d51-9b46-f66a42712964",
            "act-사용자-6": "4eee8a0f-e72d-24b4-ae8f-e2493a1da402",
            "act-사용자-7": "11a22b70-9ac7-bbf2-66b1-60647ca80752",
            "act-사용자-8": "1a0d724e-ff36-0fe6-4887-b34b87958b31",
            "act-사용자-9": "d889f16d-4519-6b8a-7e56-f1dd4141235c",
            "act-사용자-10": "76c5c940-5d8a-b57e-9c93-49ded3868763",
            "agg-loanTransaction-to-agg-book": "40fb55f4-95bf-4b7a-13a8-691f894d3429",
            "cmd-registerBook-to-evt-bookRegistered": "73d6bd51-2b4d-5480-b155-7ed5bc740b4d",
            "cmd-changeBookStatus-to-evt-bookStatusChanged": "6f42b17c-7bd9-9117-931f-b86209dcb1a8",
            "cmd-discardBook-to-evt-bookDiscarded": "68915ca5-a8d0-c4a5-3de7-222f4c8d8059",
            "cmd-loanBook-to-evt-loaned": "6b1b17ec-5f86-f717-4d56-c65562851bf7",
            "cmd-returnBook-to-evt-returned": "c962a7d8-870a-f0de-ca15-dc79298c7567",
            "cmd-reserveBook-to-evt-reserved": "ceaa5350-4648-a1dc-426c-4ecd5d4542fa"
        }
    },
    "summarizedESValue": {
        "deletedProperties": [
            "aggregate.entities",
            "aggregate.enumerations",
            "aggregate.valueObjects",
            "properties",
            "items"
        ],
        "boundedContexts": [
            {
                "id": "bc-bookManagement",
                "name": "BookManagement",
                "actors": [
                    {
                        "id": "act-사용자",
                        "name": "사용자"
                    }
                ],
                "aggregates": [
                    {
                        "id": "agg-book",
                        "name": "Book",
                        "commands": [
                            {
                                "id": "cmd-registerBook",
                                "name": "RegisterBook",
                                "api_verb": "POST",
                                "isRestRepository": False,
                                "outputEvents": [
                                    {
                                        "id": "evt-bookRegistered",
                                        "name": "BookRegistered"
                                    }
                                ]
                            },
                            {
                                "id": "cmd-changeBookStatus",
                                "name": "ChangeBookStatus",
                                "api_verb": "PUT",
                                "isRestRepository": False,
                                "outputEvents": [
                                    {
                                        "id": "evt-bookStatusChanged",
                                        "name": "BookStatusChanged"
                                    }
                                ]
                            },
                            {
                                "id": "cmd-discardBook",
                                "name": "DiscardBook",
                                "api_verb": "PUT",
                                "isRestRepository": False,
                                "outputEvents": [
                                    {
                                        "id": "evt-bookDiscarded",
                                        "name": "BookDiscarded"
                                    }
                                ]
                            }
                        ],
                        "events": [
                            {
                                "id": "evt-bookRegistered",
                                "name": "BookRegistered"
                            },
                            {
                                "id": "evt-bookStatusChanged",
                                "name": "BookStatusChanged"
                            },
                            {
                                "id": "evt-bookDiscarded",
                                "name": "BookDiscarded"
                            }
                        ],
                        "readModels": [
                            {
                                "id": "rm-bookList",
                                "name": "BookList",
                                "isMultipleResult": False
                            },
                            {
                                "id": "rm-bookDetails",
                                "name": "BookDetails",
                                "isMultipleResult": False
                            }
                        ]
                    }
                ]
            },
            {
                "id": "bc-loanManagement",
                "name": "LoanManagement",
                "actors": [
                    {
                        "id": "act-사용자-6",
                        "name": "사용자"
                    }
                ],
                "aggregates": [
                    {
                        "id": "agg-loanTransaction",
                        "name": "LoanTransaction",
                        "commands": [
                            {
                                "id": "cmd-loanBook",
                                "name": "LoanBook",
                                "api_verb": "POST",
                                "isRestRepository": False,
                                "outputEvents": [
                                    {
                                        "id": "evt-loaned",
                                        "name": "Loaned"
                                    }
                                ]
                            },
                            {
                                "id": "cmd-returnBook",
                                "name": "ReturnBook",
                                "api_verb": "POST",
                                "isRestRepository": False,
                                "outputEvents": [
                                    {
                                        "id": "evt-returned",
                                        "name": "Returned"
                                    }
                                ]
                            },
                            {
                                "id": "cmd-reserveBook",
                                "name": "ReserveBook",
                                "api_verb": "POST",
                                "isRestRepository": False,
                                "outputEvents": [
                                    {
                                        "id": "evt-reserved",
                                        "name": "Reserved"
                                    }
                                ]
                            }
                        ],
                        "events": [
                            {
                                "id": "evt-loaned",
                                "name": "Loaned"
                            },
                            {
                                "id": "evt-returned",
                                "name": "Returned"
                            },
                            {
                                "id": "evt-reserved",
                                "name": "Reserved"
                            }
                        ],
                        "readModels": [
                            {
                                "id": "rm-loanHistory",
                                "name": "LoanHistory",
                                "isMultipleResult": False
                            },
                            {
                                "id": "rm-loanCurrentStatus",
                                "name": "LoanCurrentStatus",
                                "isMultipleResult": False
                            }
                        ]
                    }
                ]
            }
        ]
    },
    "subjectText": "Creating policies for 도서 관리 Bounded Context"
}