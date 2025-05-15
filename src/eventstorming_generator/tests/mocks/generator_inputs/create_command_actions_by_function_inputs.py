create_command_actions_by_function_inputs = {
    "targetBoundedContext": {
        "_type": "org.uengine.modeling.model.BoundedContext",
        "aggregates": [],
        "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
        "description": "[{\"type\":\"userStory\",\"text\":\"도서 관리 화면에서는 새로운 도서를 등록하고 현재 보유한 도서들의 상태를 관리할 수 있어야 해. 도서 등록 시에는 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받아야 해. ISBN은 13자리 숫자여야 하고 중복 확인이 필요해. 카테고리는 소설/비소설/학술/잡지 중에서 선택할 수 있어야 해. 등록된 도서는 처음에 '대출가능' 상태가 되고, 이후 대출/반납 상황에 따라 '대출중', '예약중' 상태로 자동으로 변경되어야 해. 도서가 훼손되거나 분실된 경우 '폐기' 처리가 가능해야 해며, 폐기된 도서는 더 이상 대출이 불가능해야 해.\"}]",
        "id": "0d4a84aa-370f-8c08-2617-ab46c3d4b90b",
        "elementView": {
            "_type": "org.uengine.modeling.model.BoundedContext",
            "height": 590,
            "id": "0d4a84aa-370f-8c08-2617-ab46c3d4b90b",
            "style": "{}",
            "width": 560,
            "x": 650,
            "y": 450
        },
        "gitURL": None,
        "hexagonalView": {
            "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
            "height": 350,
            "id": "0d4a84aa-370f-8c08-2617-ab46c3d4b90b",
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
        "definitionId": "163972132_es_e2b927f329062519cf6cda2285d0e30a"
    },
    "targetAggregate": {
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
                    "f504e7a6-1dee-9475-efa8-1399561ac950": {
                        "_type": "org.uengine.uml.model.Class",
                        "id": "f504e7a6-1dee-9475-efa8-1399561ac950",
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
                            "id": "f504e7a6-1dee-9475-efa8-1399561ac950",
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
                        "parentId": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1"
                    },
                    "a2e83a99-2a61-a1cb-cb8b-4afbc3cc1e0d": {
                        "_type": "org.uengine.uml.model.enum",
                        "id": "a2e83a99-2a61-a1cb-cb8b-4afbc3cc1e0d",
                        "name": "Category",
                        "displayName": "카테고리",
                        "nameCamelCase": "category",
                        "namePascalCase": "Category",
                        "namePlural": "categories",
                        "elementView": {
                            "_type": "org.uengine.uml.model.enum",
                            "id": "a2e83a99-2a61-a1cb-cb8b-4afbc3cc1e0d",
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
                    "9b1f89ac-6b6a-6f35-590a-e50c744d910f": {
                        "_type": "org.uengine.uml.model.enum",
                        "id": "9b1f89ac-6b6a-6f35-590a-e50c744d910f",
                        "name": "Status",
                        "displayName": "도서상태",
                        "nameCamelCase": "status",
                        "namePascalCase": "Status",
                        "namePlural": "statuses",
                        "elementView": {
                            "_type": "org.uengine.uml.model.enum",
                            "id": "9b1f89ac-6b6a-6f35-590a-e50c744d910f",
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
            "name": "0d4a84aa-370f-8c08-2617-ab46c3d4b90b",
            "id": "0d4a84aa-370f-8c08-2617-ab46c3d4b90b"
        },
        "commands": [],
        "description": None,
        "id": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1",
        "elementView": {
            "_type": "org.uengine.modeling.model.Aggregate",
            "id": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1",
            "x": 650,
            "y": 450,
            "width": 130,
            "height": 400
        },
        "events": [],
        "hexagonalView": {
            "_type": "org.uengine.modeling.model.AggregateHexagonal",
            "id": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1",
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
    "description": "{\"userStories\":[{\"title\":\"도서 등록 및 관리\",\"description\":\"사용자는 도서 관리 화면에서 새로운 도서를 등록하고, 등록된 도서의 대출 상태를 관리할 수 있다. 신규 등록 시 도서명, ISBN, 저자, 출판사, 카테고리 정보를 필수 입력 받고, ISBN은 13자리 숫자이며 중복 체크가 수행된다. 등록 후 도서는 초기 '대출가능' 상태로 표시되며, 대출, 반납, 예약 등의 이벤트에 따라 상태가 자동 갱신된다. 또한, 도서가 훼손되거나 분실된 경우, '폐기' 처리를 통해 대출 기능에서 제외된다.\",\"acceptance\":[\"도서 등록 시 도서명, ISBN, 저자, 출판사, 카테고리 정보를 반드시 입력해야 한다.\",\"ISBN은 13자리 숫자여야 하며, 중복 체크 로직이 구현되어 있다.\",\"카테고리는 소설, 비소설, 학술, 잡지 중에서 선택할 수 있다.\",\"등록된 도서는 초기 상태가 '대출가능'이며, 대출/반납/예약에 따라 상태가 자동 변경된다.\",\"도서가 훼손되거나 분실되면 '폐기' 처리되어 대출 기능에서 제외된다.\"]}],\"entities\":{\"Book\":{\"properties\":[{\"name\":\"bookTitle\",\"type\":\"String\",\"required\":true},{\"name\":\"ISBN\",\"type\":\"String\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"author\",\"type\":\"String\",\"required\":true},{\"name\":\"publisher\",\"type\":\"String\",\"required\":true},{\"name\":\"category\",\"type\":\"enum\",\"required\":true,\"values\":[\"소설\",\"비소설\",\"학술\",\"잡지\"]},{\"name\":\"status\",\"type\":\"enum\",\"required\":true,\"values\":[\"대출가능\",\"대출중\",\"예약중\",\"폐기\"]}]}},\"businessRules\":[{\"name\":\"ISBN 형식 검증\",\"description\":\"ISBN은 13자리 숫자로 구성되어야 하며, 입력된 ISBN은 기존 등록 도서와 중복되지 않아야 한다.\"},{\"name\":\"초기 대출 상태\",\"description\":\"신규 등록된 도서는 자동으로 '대출가능' 상태로 설정된다.\"},{\"name\":\"상태 전이 관리\",\"description\":\"대출, 반납, 예약, 훼손 또는 분실 이벤트 발생 시 도서의 상태는 각각 '대출중', '예약중', '폐기'로 자동 갱신된다.\"},{\"name\":\"폐기 처리\",\"description\":\"도서가 '폐기' 상태일 경우 더 이상 대출이 불가능하다.\"}],\"interfaces\":{\"BookManagement\":{\"sections\":[{\"name\":\"도서 등록\",\"type\":\"form\",\"fields\":[{\"name\":\"bookTitle\",\"type\":\"text\",\"required\":true},{\"name\":\"ISBN\",\"type\":\"text\",\"required\":true},{\"name\":\"author\",\"type\":\"text\",\"required\":true},{\"name\":\"publisher\",\"type\":\"text\",\"required\":true},{\"name\":\"category\",\"type\":\"select\",\"required\":true}],\"actions\":[\"Register Book\"],\"filters\":[],\"resultTable\":{\"columns\":[],\"actions\":[]}},{\"name\":\"도서 상태 관리\",\"type\":\"table\",\"fields\":[],\"actions\":[\"Modify Status\",\"Discard Book\"],\"filters\":[\"category\",\"status\"],\"resultTable\":{\"columns\":[\"ISBN\",\"bookTitle\",\"author\",\"publisher\",\"category\",\"status\"],\"actions\":[\"View Details\"]}}]}}}",
    "esValue": {
        "elements": {
            "0d4a84aa-370f-8c08-2617-ab46c3d4b90b": {
                "_type": "org.uengine.modeling.model.BoundedContext",
                "aggregates": [
                    {
                        "id": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1"
                    }
                ],
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "description": "[{\"type\":\"userStory\",\"text\":\"도서 관리 화면에서는 새로운 도서를 등록하고 현재 보유한 도서들의 상태를 관리할 수 있어야 해. 도서 등록 시에는 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받아야 해. ISBN은 13자리 숫자여야 하고 중복 확인이 필요해. 카테고리는 소설/비소설/학술/잡지 중에서 선택할 수 있어야 해. 등록된 도서는 처음에 '대출가능' 상태가 되고, 이후 대출/반납 상황에 따라 '대출중', '예약중' 상태로 자동으로 변경되어야 해. 도서가 훼손되거나 분실된 경우 '폐기' 처리가 가능해야 해며, 폐기된 도서는 더 이상 대출이 불가능해야 해.\"}]",
                "id": "0d4a84aa-370f-8c08-2617-ab46c3d4b90b",
                "elementView": {
                    "_type": "org.uengine.modeling.model.BoundedContext",
                    "height": 590,
                    "id": "0d4a84aa-370f-8c08-2617-ab46c3d4b90b",
                    "style": "{}",
                    "width": 560,
                    "x": 650,
                    "y": 450
                },
                "gitURL": None,
                "hexagonalView": {
                    "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
                    "height": 350,
                    "id": "0d4a84aa-370f-8c08-2617-ab46c3d4b90b",
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
                "definitionId": "163972132_es_e2b927f329062519cf6cda2285d0e30a"
            },
            "348ea9d9-ffb2-975a-b94b-9a37ab30eabb": {
                "_type": "org.uengine.modeling.model.BoundedContext",
                "aggregates": [
                    {
                        "id": "dffec6c1-e5eb-3488-cf5b-85ac8f3e1c55"
                    }
                ],
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "description": "[{\"type\":\"userStory\",\"text\":\"대출/반납 화면에서는 회원이 도서를 대출하고 반납하는 것을 관리할 수 있어야 해. 대출 신청 시에는 회원번호와 이름으로 회원을 확인하고, 대출할 도서를 선택해야 해. 도서는 도서명이나 ISBN으로 검색할 수 있어야 해. 대출 기간은 7일/14일/30일 중에서 선택할 수 있어. 만약 대출하려는 도서가 이미 대출 중이라면, 예약 신청이 가능해야 해. 대출이 완료되면 해당 도서의 상태는 자동으로 '대출중'으로 변경되어야 해.\"}]",
                "id": "348ea9d9-ffb2-975a-b94b-9a37ab30eabb",
                "elementView": {
                    "_type": "org.uengine.modeling.model.BoundedContext",
                    "height": 590,
                    "id": "348ea9d9-ffb2-975a-b94b-9a37ab30eabb",
                    "style": "{}",
                    "width": 560,
                    "x": 1235,
                    "y": 450
                },
                "gitURL": None,
                "hexagonalView": {
                    "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
                    "height": 350,
                    "id": "348ea9d9-ffb2-975a-b94b-9a37ab30eabb",
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
                "definitionId": "163972132_es_e2b927f329062519cf6cda2285d0e30a"
            },
            "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1": {
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
                            "f504e7a6-1dee-9475-efa8-1399561ac950": {
                                "_type": "org.uengine.uml.model.Class",
                                "id": "f504e7a6-1dee-9475-efa8-1399561ac950",
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
                                    "id": "f504e7a6-1dee-9475-efa8-1399561ac950",
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
                                "parentId": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1"
                            },
                            "a2e83a99-2a61-a1cb-cb8b-4afbc3cc1e0d": {
                                "_type": "org.uengine.uml.model.enum",
                                "id": "a2e83a99-2a61-a1cb-cb8b-4afbc3cc1e0d",
                                "name": "Category",
                                "displayName": "카테고리",
                                "nameCamelCase": "category",
                                "namePascalCase": "Category",
                                "namePlural": "categories",
                                "elementView": {
                                    "_type": "org.uengine.uml.model.enum",
                                    "id": "a2e83a99-2a61-a1cb-cb8b-4afbc3cc1e0d",
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
                            "9b1f89ac-6b6a-6f35-590a-e50c744d910f": {
                                "_type": "org.uengine.uml.model.enum",
                                "id": "9b1f89ac-6b6a-6f35-590a-e50c744d910f",
                                "name": "Status",
                                "displayName": "도서상태",
                                "nameCamelCase": "status",
                                "namePascalCase": "Status",
                                "namePlural": "statuses",
                                "elementView": {
                                    "_type": "org.uengine.uml.model.enum",
                                    "id": "9b1f89ac-6b6a-6f35-590a-e50c744d910f",
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
                    "name": "0d4a84aa-370f-8c08-2617-ab46c3d4b90b",
                    "id": "0d4a84aa-370f-8c08-2617-ab46c3d4b90b"
                },
                "commands": [],
                "description": None,
                "id": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1",
                "elementView": {
                    "_type": "org.uengine.modeling.model.Aggregate",
                    "id": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1",
                    "x": 650,
                    "y": 450,
                    "width": 130,
                    "height": 400
                },
                "events": [],
                "hexagonalView": {
                    "_type": "org.uengine.modeling.model.AggregateHexagonal",
                    "id": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1",
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
            "dffec6c1-e5eb-3488-cf5b-85ac8f3e1c55": {
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
                            "7933815c-6e59-c1c9-3182-5edfc3b4d48d": {
                                "_type": "org.uengine.uml.model.Class",
                                "id": "7933815c-6e59-c1c9-3182-5edfc3b4d48d",
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
                                    "id": "7933815c-6e59-c1c9-3182-5edfc3b4d48d",
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
                                "parentId": "dffec6c1-e5eb-3488-cf5b-85ac8f3e1c55"
                            },
                            "360a2c65-51d3-a718-db09-6879bb6f8328": {
                                "_type": "org.uengine.uml.model.enum",
                                "id": "360a2c65-51d3-a718-db09-6879bb6f8328",
                                "name": "TransactionType",
                                "displayName": "거래 유형",
                                "nameCamelCase": "transactionType",
                                "namePascalCase": "TransactionType",
                                "namePlural": "transactionTypes",
                                "elementView": {
                                    "_type": "org.uengine.uml.model.enum",
                                    "id": "360a2c65-51d3-a718-db09-6879bb6f8328",
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
                            "66cba710-ebb9-936c-fe9e-aec936313e0c": {
                                "_type": "org.uengine.uml.model.vo.Class",
                                "id": "66cba710-ebb9-936c-fe9e-aec936313e0c",
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
                                    "id": "66cba710-ebb9-936c-fe9e-aec936313e0c",
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
                    "name": "348ea9d9-ffb2-975a-b94b-9a37ab30eabb",
                    "id": "348ea9d9-ffb2-975a-b94b-9a37ab30eabb"
                },
                "commands": [],
                "description": None,
                "id": "dffec6c1-e5eb-3488-cf5b-85ac8f3e1c55",
                "elementView": {
                    "_type": "org.uengine.modeling.model.Aggregate",
                    "id": "dffec6c1-e5eb-3488-cf5b-85ac8f3e1c55",
                    "x": 1235,
                    "y": 450,
                    "width": 130,
                    "height": 400
                },
                "events": [],
                "hexagonalView": {
                    "_type": "org.uengine.modeling.model.AggregateHexagonal",
                    "id": "dffec6c1-e5eb-3488-cf5b-85ac8f3e1c55",
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
        "relations": {
            "6a0b75e3-1a12-8881-638a-a34e293b55ef": {
                "_type": "org.uengine.modeling.model.Relation",
                "name": "",
                "id": "6a0b75e3-1a12-8881-638a-a34e293b55ef",
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
                                "7933815c-6e59-c1c9-3182-5edfc3b4d48d": {
                                    "_type": "org.uengine.uml.model.Class",
                                    "id": "7933815c-6e59-c1c9-3182-5edfc3b4d48d",
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
                                        "id": "7933815c-6e59-c1c9-3182-5edfc3b4d48d",
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
                                    "parentId": "dffec6c1-e5eb-3488-cf5b-85ac8f3e1c55"
                                },
                                "360a2c65-51d3-a718-db09-6879bb6f8328": {
                                    "_type": "org.uengine.uml.model.enum",
                                    "id": "360a2c65-51d3-a718-db09-6879bb6f8328",
                                    "name": "TransactionType",
                                    "displayName": "거래 유형",
                                    "nameCamelCase": "transactionType",
                                    "namePascalCase": "TransactionType",
                                    "namePlural": "transactionTypes",
                                    "elementView": {
                                        "_type": "org.uengine.uml.model.enum",
                                        "id": "360a2c65-51d3-a718-db09-6879bb6f8328",
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
                        "name": "348ea9d9-ffb2-975a-b94b-9a37ab30eabb",
                        "id": "348ea9d9-ffb2-975a-b94b-9a37ab30eabb"
                    },
                    "commands": [],
                    "description": None,
                    "id": "dffec6c1-e5eb-3488-cf5b-85ac8f3e1c55",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Aggregate",
                        "id": "dffec6c1-e5eb-3488-cf5b-85ac8f3e1c55",
                        "x": 1235,
                        "y": 450,
                        "width": 130,
                        "height": 400
                    },
                    "events": [],
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.AggregateHexagonal",
                        "id": "dffec6c1-e5eb-3488-cf5b-85ac8f3e1c55",
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
                                "f504e7a6-1dee-9475-efa8-1399561ac950": {
                                    "_type": "org.uengine.uml.model.Class",
                                    "id": "f504e7a6-1dee-9475-efa8-1399561ac950",
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
                                        "id": "f504e7a6-1dee-9475-efa8-1399561ac950",
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
                                    "parentId": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1"
                                },
                                "a2e83a99-2a61-a1cb-cb8b-4afbc3cc1e0d": {
                                    "_type": "org.uengine.uml.model.enum",
                                    "id": "a2e83a99-2a61-a1cb-cb8b-4afbc3cc1e0d",
                                    "name": "Category",
                                    "displayName": "카테고리",
                                    "nameCamelCase": "category",
                                    "namePascalCase": "Category",
                                    "namePlural": "categories",
                                    "elementView": {
                                        "_type": "org.uengine.uml.model.enum",
                                        "id": "a2e83a99-2a61-a1cb-cb8b-4afbc3cc1e0d",
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
                                "9b1f89ac-6b6a-6f35-590a-e50c744d910f": {
                                    "_type": "org.uengine.uml.model.enum",
                                    "id": "9b1f89ac-6b6a-6f35-590a-e50c744d910f",
                                    "name": "Status",
                                    "displayName": "도서상태",
                                    "nameCamelCase": "status",
                                    "namePascalCase": "Status",
                                    "namePlural": "statuses",
                                    "elementView": {
                                        "_type": "org.uengine.uml.model.enum",
                                        "id": "9b1f89ac-6b6a-6f35-590a-e50c744d910f",
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
                        "name": "0d4a84aa-370f-8c08-2617-ab46c3d4b90b",
                        "id": "0d4a84aa-370f-8c08-2617-ab46c3d4b90b"
                    },
                    "commands": [],
                    "description": None,
                    "id": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Aggregate",
                        "id": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1",
                        "x": 650,
                        "y": 450,
                        "width": 130,
                        "height": 400
                    },
                    "events": [],
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.AggregateHexagonal",
                        "id": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1",
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
                "from": "dffec6c1-e5eb-3488-cf5b-85ac8f3e1c55",
                "to": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1",
                "relationView": {
                    "id": "6a0b75e3-1a12-8881-638a-a34e293b55ef",
                    "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                    "from": "dffec6c1-e5eb-3488-cf5b-85ac8f3e1c55",
                    "to": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1",
                    "needReconnect": True,
                    "value": "[[1170,456],[715,456]]"
                },
                "hexagonalView": {
                    "_type": "org.uengine.modeling.model.RelationHexagonal",
                    "from": "dffec6c1-e5eb-3488-cf5b-85ac8f3e1c55",
                    "id": "6a0b75e3-1a12-8881-638a-a34e293b55ef",
                    "needReconnect": True,
                    "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                    "to": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1",
                    "value": None
                },
                "sourceMultiplicity": "1",
                "targetMultiplicity": "1",
                "displayName": ""
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
    "aggregateDisplayName": "도서",
    "esAliasTransManager": {
        "esValue": {
            "elements": {
                "0d4a84aa-370f-8c08-2617-ab46c3d4b90b": {
                    "_type": "org.uengine.modeling.model.BoundedContext",
                    "aggregates": [
                        {
                            "id": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1"
                        }
                    ],
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "description": "[{\"type\":\"userStory\",\"text\":\"도서 관리 화면에서는 새로운 도서를 등록하고 현재 보유한 도서들의 상태를 관리할 수 있어야 해. 도서 등록 시에는 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받아야 해. ISBN은 13자리 숫자여야 하고 중복 확인이 필요해. 카테고리는 소설/비소설/학술/잡지 중에서 선택할 수 있어야 해. 등록된 도서는 처음에 '대출가능' 상태가 되고, 이후 대출/반납 상황에 따라 '대출중', '예약중' 상태로 자동으로 변경되어야 해. 도서가 훼손되거나 분실된 경우 '폐기' 처리가 가능해야 해며, 폐기된 도서는 더 이상 대출이 불가능해야 해.\"}]",
                    "id": "0d4a84aa-370f-8c08-2617-ab46c3d4b90b",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.BoundedContext",
                        "height": 590,
                        "id": "0d4a84aa-370f-8c08-2617-ab46c3d4b90b",
                        "style": "{}",
                        "width": 560,
                        "x": 650,
                        "y": 450
                    },
                    "gitURL": None,
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
                        "height": 350,
                        "id": "0d4a84aa-370f-8c08-2617-ab46c3d4b90b",
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
                    "definitionId": "163972132_es_e2b927f329062519cf6cda2285d0e30a"
                },
                "348ea9d9-ffb2-975a-b94b-9a37ab30eabb": {
                    "_type": "org.uengine.modeling.model.BoundedContext",
                    "aggregates": [
                        {
                            "id": "dffec6c1-e5eb-3488-cf5b-85ac8f3e1c55"
                        }
                    ],
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "description": "[{\"type\":\"userStory\",\"text\":\"대출/반납 화면에서는 회원이 도서를 대출하고 반납하는 것을 관리할 수 있어야 해. 대출 신청 시에는 회원번호와 이름으로 회원을 확인하고, 대출할 도서를 선택해야 해. 도서는 도서명이나 ISBN으로 검색할 수 있어야 해. 대출 기간은 7일/14일/30일 중에서 선택할 수 있어. 만약 대출하려는 도서가 이미 대출 중이라면, 예약 신청이 가능해야 해. 대출이 완료되면 해당 도서의 상태는 자동으로 '대출중'으로 변경되어야 해.\"}]",
                    "id": "348ea9d9-ffb2-975a-b94b-9a37ab30eabb",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.BoundedContext",
                        "height": 590,
                        "id": "348ea9d9-ffb2-975a-b94b-9a37ab30eabb",
                        "style": "{}",
                        "width": 560,
                        "x": 1235,
                        "y": 450
                    },
                    "gitURL": None,
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
                        "height": 350,
                        "id": "348ea9d9-ffb2-975a-b94b-9a37ab30eabb",
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
                    "definitionId": "163972132_es_e2b927f329062519cf6cda2285d0e30a"
                },
                "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1": {
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
                                "f504e7a6-1dee-9475-efa8-1399561ac950": {
                                    "_type": "org.uengine.uml.model.Class",
                                    "id": "f504e7a6-1dee-9475-efa8-1399561ac950",
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
                                        "id": "f504e7a6-1dee-9475-efa8-1399561ac950",
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
                                    "parentId": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1"
                                },
                                "a2e83a99-2a61-a1cb-cb8b-4afbc3cc1e0d": {
                                    "_type": "org.uengine.uml.model.enum",
                                    "id": "a2e83a99-2a61-a1cb-cb8b-4afbc3cc1e0d",
                                    "name": "Category",
                                    "displayName": "카테고리",
                                    "nameCamelCase": "category",
                                    "namePascalCase": "Category",
                                    "namePlural": "categories",
                                    "elementView": {
                                        "_type": "org.uengine.uml.model.enum",
                                        "id": "a2e83a99-2a61-a1cb-cb8b-4afbc3cc1e0d",
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
                                "9b1f89ac-6b6a-6f35-590a-e50c744d910f": {
                                    "_type": "org.uengine.uml.model.enum",
                                    "id": "9b1f89ac-6b6a-6f35-590a-e50c744d910f",
                                    "name": "Status",
                                    "displayName": "도서상태",
                                    "nameCamelCase": "status",
                                    "namePascalCase": "Status",
                                    "namePlural": "statuses",
                                    "elementView": {
                                        "_type": "org.uengine.uml.model.enum",
                                        "id": "9b1f89ac-6b6a-6f35-590a-e50c744d910f",
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
                        "name": "0d4a84aa-370f-8c08-2617-ab46c3d4b90b",
                        "id": "0d4a84aa-370f-8c08-2617-ab46c3d4b90b"
                    },
                    "commands": [],
                    "description": None,
                    "id": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Aggregate",
                        "id": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1",
                        "x": 650,
                        "y": 450,
                        "width": 130,
                        "height": 400
                    },
                    "events": [],
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.AggregateHexagonal",
                        "id": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1",
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
                "dffec6c1-e5eb-3488-cf5b-85ac8f3e1c55": {
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
                                "7933815c-6e59-c1c9-3182-5edfc3b4d48d": {
                                    "_type": "org.uengine.uml.model.Class",
                                    "id": "7933815c-6e59-c1c9-3182-5edfc3b4d48d",
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
                                        "id": "7933815c-6e59-c1c9-3182-5edfc3b4d48d",
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
                                    "parentId": "dffec6c1-e5eb-3488-cf5b-85ac8f3e1c55"
                                },
                                "360a2c65-51d3-a718-db09-6879bb6f8328": {
                                    "_type": "org.uengine.uml.model.enum",
                                    "id": "360a2c65-51d3-a718-db09-6879bb6f8328",
                                    "name": "TransactionType",
                                    "displayName": "거래 유형",
                                    "nameCamelCase": "transactionType",
                                    "namePascalCase": "TransactionType",
                                    "namePlural": "transactionTypes",
                                    "elementView": {
                                        "_type": "org.uengine.uml.model.enum",
                                        "id": "360a2c65-51d3-a718-db09-6879bb6f8328",
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
                                "66cba710-ebb9-936c-fe9e-aec936313e0c": {
                                    "_type": "org.uengine.uml.model.vo.Class",
                                    "id": "66cba710-ebb9-936c-fe9e-aec936313e0c",
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
                                        "id": "66cba710-ebb9-936c-fe9e-aec936313e0c",
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
                        "name": "348ea9d9-ffb2-975a-b94b-9a37ab30eabb",
                        "id": "348ea9d9-ffb2-975a-b94b-9a37ab30eabb"
                    },
                    "commands": [],
                    "description": None,
                    "id": "dffec6c1-e5eb-3488-cf5b-85ac8f3e1c55",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Aggregate",
                        "id": "dffec6c1-e5eb-3488-cf5b-85ac8f3e1c55",
                        "x": 1235,
                        "y": 450,
                        "width": 130,
                        "height": 400
                    },
                    "events": [],
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.AggregateHexagonal",
                        "id": "dffec6c1-e5eb-3488-cf5b-85ac8f3e1c55",
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
            "relations": {
                "6a0b75e3-1a12-8881-638a-a34e293b55ef": {
                    "_type": "org.uengine.modeling.model.Relation",
                    "name": "",
                    "id": "6a0b75e3-1a12-8881-638a-a34e293b55ef",
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
                                    "7933815c-6e59-c1c9-3182-5edfc3b4d48d": {
                                        "_type": "org.uengine.uml.model.Class",
                                        "id": "7933815c-6e59-c1c9-3182-5edfc3b4d48d",
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
                                            "id": "7933815c-6e59-c1c9-3182-5edfc3b4d48d",
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
                                        "parentId": "dffec6c1-e5eb-3488-cf5b-85ac8f3e1c55"
                                    },
                                    "360a2c65-51d3-a718-db09-6879bb6f8328": {
                                        "_type": "org.uengine.uml.model.enum",
                                        "id": "360a2c65-51d3-a718-db09-6879bb6f8328",
                                        "name": "TransactionType",
                                        "displayName": "거래 유형",
                                        "nameCamelCase": "transactionType",
                                        "namePascalCase": "TransactionType",
                                        "namePlural": "transactionTypes",
                                        "elementView": {
                                            "_type": "org.uengine.uml.model.enum",
                                            "id": "360a2c65-51d3-a718-db09-6879bb6f8328",
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
                            "name": "348ea9d9-ffb2-975a-b94b-9a37ab30eabb",
                            "id": "348ea9d9-ffb2-975a-b94b-9a37ab30eabb"
                        },
                        "commands": [],
                        "description": None,
                        "id": "dffec6c1-e5eb-3488-cf5b-85ac8f3e1c55",
                        "elementView": {
                            "_type": "org.uengine.modeling.model.Aggregate",
                            "id": "dffec6c1-e5eb-3488-cf5b-85ac8f3e1c55",
                            "x": 1235,
                            "y": 450,
                            "width": 130,
                            "height": 400
                        },
                        "events": [],
                        "hexagonalView": {
                            "_type": "org.uengine.modeling.model.AggregateHexagonal",
                            "id": "dffec6c1-e5eb-3488-cf5b-85ac8f3e1c55",
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
                                    "f504e7a6-1dee-9475-efa8-1399561ac950": {
                                        "_type": "org.uengine.uml.model.Class",
                                        "id": "f504e7a6-1dee-9475-efa8-1399561ac950",
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
                                            "id": "f504e7a6-1dee-9475-efa8-1399561ac950",
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
                                        "parentId": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1"
                                    },
                                    "a2e83a99-2a61-a1cb-cb8b-4afbc3cc1e0d": {
                                        "_type": "org.uengine.uml.model.enum",
                                        "id": "a2e83a99-2a61-a1cb-cb8b-4afbc3cc1e0d",
                                        "name": "Category",
                                        "displayName": "카테고리",
                                        "nameCamelCase": "category",
                                        "namePascalCase": "Category",
                                        "namePlural": "categories",
                                        "elementView": {
                                            "_type": "org.uengine.uml.model.enum",
                                            "id": "a2e83a99-2a61-a1cb-cb8b-4afbc3cc1e0d",
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
                                    "9b1f89ac-6b6a-6f35-590a-e50c744d910f": {
                                        "_type": "org.uengine.uml.model.enum",
                                        "id": "9b1f89ac-6b6a-6f35-590a-e50c744d910f",
                                        "name": "Status",
                                        "displayName": "도서상태",
                                        "nameCamelCase": "status",
                                        "namePascalCase": "Status",
                                        "namePlural": "statuses",
                                        "elementView": {
                                            "_type": "org.uengine.uml.model.enum",
                                            "id": "9b1f89ac-6b6a-6f35-590a-e50c744d910f",
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
                            "name": "0d4a84aa-370f-8c08-2617-ab46c3d4b90b",
                            "id": "0d4a84aa-370f-8c08-2617-ab46c3d4b90b"
                        },
                        "commands": [],
                        "description": None,
                        "id": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1",
                        "elementView": {
                            "_type": "org.uengine.modeling.model.Aggregate",
                            "id": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1",
                            "x": 650,
                            "y": 450,
                            "width": 130,
                            "height": 400
                        },
                        "events": [],
                        "hexagonalView": {
                            "_type": "org.uengine.modeling.model.AggregateHexagonal",
                            "id": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1",
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
                    "from": "dffec6c1-e5eb-3488-cf5b-85ac8f3e1c55",
                    "to": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1",
                    "relationView": {
                        "id": "6a0b75e3-1a12-8881-638a-a34e293b55ef",
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "from": "dffec6c1-e5eb-3488-cf5b-85ac8f3e1c55",
                        "to": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1",
                        "needReconnect": True,
                        "value": "[[1170,456],[715,456]]"
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.RelationHexagonal",
                        "from": "dffec6c1-e5eb-3488-cf5b-85ac8f3e1c55",
                        "id": "6a0b75e3-1a12-8881-638a-a34e293b55ef",
                        "needReconnect": True,
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "to": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1",
                        "value": None
                    },
                    "sourceMultiplicity": "1",
                    "targetMultiplicity": "1",
                    "displayName": ""
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
            "0d4a84aa-370f-8c08-2617-ab46c3d4b90b": "bc-bookManagement",
            "348ea9d9-ffb2-975a-b94b-9a37ab30eabb": "bc-loanManagement",
            "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1": "agg-book",
            "f504e7a6-1dee-9475-efa8-1399561ac950": "agg-root-book",
            "a2e83a99-2a61-a1cb-cb8b-4afbc3cc1e0d": "enum-category",
            "9b1f89ac-6b6a-6f35-590a-e50c744d910f": "enum-status",
            "dffec6c1-e5eb-3488-cf5b-85ac8f3e1c55": "agg-loanTransaction",
            "7933815c-6e59-c1c9-3182-5edfc3b4d48d": "agg-root-loanTransaction",
            "360a2c65-51d3-a718-db09-6879bb6f8328": "enum-transactionType",
            "66cba710-ebb9-936c-fe9e-aec936313e0c": "vo-bookId",
            "6a0b75e3-1a12-8881-638a-a34e293b55ef": "agg-loanTransaction-to-agg-book"
        },
        "aliasToUUIDDic": {
            "bc-bookManagement": "0d4a84aa-370f-8c08-2617-ab46c3d4b90b",
            "bc-loanManagement": "348ea9d9-ffb2-975a-b94b-9a37ab30eabb",
            "agg-book": "79c0439e-e253-01f5-7e8e-faf9ae2ef2e1",
            "agg-root-book": "f504e7a6-1dee-9475-efa8-1399561ac950",
            "enum-category": "a2e83a99-2a61-a1cb-cb8b-4afbc3cc1e0d",
            "enum-status": "9b1f89ac-6b6a-6f35-590a-e50c744d910f",
            "agg-loanTransaction": "dffec6c1-e5eb-3488-cf5b-85ac8f3e1c55",
            "agg-root-loanTransaction": "7933815c-6e59-c1c9-3182-5edfc3b4d48d",
            "enum-transactionType": "360a2c65-51d3-a718-db09-6879bb6f8328",
            "vo-bookId": "66cba710-ebb9-936c-fe9e-aec936313e0c",
            "agg-loanTransaction-to-agg-book": "6a0b75e3-1a12-8881-638a-a34e293b55ef"
        }
    },
    "summarizedESValue": {
        "deletedProperties": [],
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
                        "valueObjects": [],
                        "commands": [],
                        "events": [],
                        "readModels": []
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
                            },
                            {
                                "name": "bookId",
                                "type": "BookId"
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
                        "valueObjects": [
                            {
                                "id": "vo-bookId",
                                "name": "BookId",
                                "properties": [
                                    {
                                        "name": "ISBN",
                                        "isKey": True,
                                        "referencedAggregateName": "Book",
                                        "isForeignProperty": True
                                    }
                                ]
                            }
                        ],
                        "commands": [],
                        "events": [],
                        "readModels": []
                    }
                ]
            }
        ]
    },
    "subjectText": "Creating commands for 도서 Aggregate"
}