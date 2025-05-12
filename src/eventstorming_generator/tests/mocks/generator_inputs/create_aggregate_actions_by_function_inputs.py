create_aggregate_actions_by_function_inputs = {
    "targetBoundedContext": {
        "_type": "org.uengine.modeling.model.BoundedContext",
        "aggregates": [],
        "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
        "description": "[{\"type\":\"userStory\",\"text\":\"도서 관리 화면에서는 새로운 도서를 등록하고 현재 보유한 도서들의 상태를 관리할 수 있어야 해. 도서 등록 시에는 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받아야 해. ISBN은 13자리 숫자여야 하고 중복 확인이 필요해. 카테고리는 소설/비소설/학술/잡지 중에서 선택할 수 있어야 해. 등록된 도서는 처음에 '대출가능' 상태가 되고, 이후 대출/반납 상황에 따라 '대출중', '예약중' 상태로 자동으로 변경되어야 해. 도서가 훼손되거나 분실된 경우 '폐기' 처리가 가능해야 해며, 폐기된 도서는 더 이상 대출이 불가능해야 해.\"}]",
        "id": "854a2992-fc9c-69d4-26ff-0f8bbf6a6ec1",
        "elementView": {
            "_type": "org.uengine.modeling.model.BoundedContext",
            "height": 590,
            "id": "854a2992-fc9c-69d4-26ff-0f8bbf6a6ec1",
            "style": "{}",
            "width": 560,
            "x": 650,
            "y": 450
        },
        "gitURL": None,
        "hexagonalView": {
            "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
            "height": 350,
            "id": "854a2992-fc9c-69d4-26ff-0f8bbf6a6ec1",
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
        "definitionId": "163972132_es_05d136ce0010c9a1f5e2fde77b3fa549"
    },
    "description": "{\"userStories\":[{\"title\":\"도서 등록 및 관리\",\"description\":\"사용자는 도서 관리 화면에서 새로운 도서를 등록하고, 등록된 도서의 대출 상태를 관리할 수 있다. 신규 등록 시 도서명, ISBN, 저자, 출판사, 카테고리 정보를 필수 입력 받고, ISBN은 13자리 숫자이며 중복 체크가 수행된다. 등록 후 도서는 초기 '대출가능' 상태로 표시되며, 대출, 반납, 예약 등의 이벤트에 따라 상태가 자동 갱신된다. 또한, 도서가 훼손되거나 분실된 경우, '폐기' 처리를 통해 대출 기능에서 제외된다.\",\"acceptance\":[\"도서 등록 시 도서명, ISBN, 저자, 출판사, 카테고리 정보를 반드시 입력해야 한다.\",\"ISBN은 13자리 숫자여야 하며, 중복 체크 로직이 구현되어 있다.\",\"카테고리는 소설, 비소설, 학술, 잡지 중에서 선택할 수 있다.\",\"등록된 도서는 초기 상태가 '대출가능'이며, 대출/반납/예약에 따라 상태가 자동 변경된다.\",\"도서가 훼손되거나 분실되면 '폐기' 처리되어 대출 기능에서 제외된다.\"]}],\"entities\":{\"Book\":{\"properties\":[{\"name\":\"bookTitle\",\"type\":\"String\",\"required\":true},{\"name\":\"ISBN\",\"type\":\"String\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"author\",\"type\":\"String\",\"required\":true},{\"name\":\"publisher\",\"type\":\"String\",\"required\":true},{\"name\":\"category\",\"type\":\"enum\",\"required\":true,\"values\":[\"소설\",\"비소설\",\"학술\",\"잡지\"]},{\"name\":\"status\",\"type\":\"enum\",\"required\":true,\"values\":[\"대출가능\",\"대출중\",\"예약중\",\"폐기\"]}]}},\"businessRules\":[{\"name\":\"ISBN 형식 검증\",\"description\":\"ISBN은 13자리 숫자로 구성되어야 하며, 입력된 ISBN은 기존 등록 도서와 중복되지 않아야 한다.\"},{\"name\":\"초기 대출 상태\",\"description\":\"신규 등록된 도서는 자동으로 '대출가능' 상태로 설정된다.\"},{\"name\":\"상태 전이 관리\",\"description\":\"대출, 반납, 예약, 훼손 또는 분실 이벤트 발생 시 도서의 상태는 각각 '대출중', '예약중', '폐기'로 자동 갱신된다.\"},{\"name\":\"폐기 처리\",\"description\":\"도서가 '폐기' 상태일 경우 더 이상 대출이 불가능하다.\"}],\"interfaces\":{\"BookManagement\":{\"sections\":[{\"name\":\"도서 등록\",\"type\":\"form\",\"fields\":[{\"name\":\"bookTitle\",\"type\":\"text\",\"required\":true},{\"name\":\"ISBN\",\"type\":\"text\",\"required\":true},{\"name\":\"author\",\"type\":\"text\",\"required\":true},{\"name\":\"publisher\",\"type\":\"text\",\"required\":true},{\"name\":\"category\",\"type\":\"select\",\"required\":true}],\"actions\":[\"Register Book\"],\"filters\":[],\"resultTable\":{\"columns\":[],\"actions\":[]}},{\"name\":\"도서 상태 관리\",\"type\":\"table\",\"fields\":[],\"actions\":[\"Modify Status\",\"Discard Book\"],\"filters\":[\"category\",\"status\"],\"resultTable\":{\"columns\":[\"ISBN\",\"bookTitle\",\"author\",\"publisher\",\"category\",\"status\"],\"actions\":[\"View Details\"]}}]}}}",
    "draftOption": [
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
    "esValue": {
        "elements": {
            "854a2992-fc9c-69d4-26ff-0f8bbf6a6ec1": {
                "_type": "org.uengine.modeling.model.BoundedContext",
                "aggregates": [],
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "description": "[{\"type\":\"userStory\",\"text\":\"도서 관리 화면에서는 새로운 도서를 등록하고 현재 보유한 도서들의 상태를 관리할 수 있어야 해. 도서 등록 시에는 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받아야 해. ISBN은 13자리 숫자여야 하고 중복 확인이 필요해. 카테고리는 소설/비소설/학술/잡지 중에서 선택할 수 있어야 해. 등록된 도서는 처음에 '대출가능' 상태가 되고, 이후 대출/반납 상황에 따라 '대출중', '예약중' 상태로 자동으로 변경되어야 해. 도서가 훼손되거나 분실된 경우 '폐기' 처리가 가능해야 해며, 폐기된 도서는 더 이상 대출이 불가능해야 해.\"}]",
                "id": "854a2992-fc9c-69d4-26ff-0f8bbf6a6ec1",
                "elementView": {
                    "_type": "org.uengine.modeling.model.BoundedContext",
                    "height": 590,
                    "id": "854a2992-fc9c-69d4-26ff-0f8bbf6a6ec1",
                    "style": "{}",
                    "width": 560,
                    "x": 650,
                    "y": 450
                },
                "gitURL": None,
                "hexagonalView": {
                    "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
                    "height": 350,
                    "id": "854a2992-fc9c-69d4-26ff-0f8bbf6a6ec1",
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
                "definitionId": "163972132_es_05d136ce0010c9a1f5e2fde77b3fa549"
            },
            "9ef357e7-6141-eaa9-f96d-227f7070ac93": {
                "_type": "org.uengine.modeling.model.BoundedContext",
                "aggregates": [],
                "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                "description": "[{\"type\":\"userStory\",\"text\":\"대출/반납 화면에서는 회원이 도서를 대출하고 반납하는 것을 관리할 수 있어야 해. 대출 신청 시에는 회원번호와 이름으로 회원을 확인하고, 대출할 도서를 선택해야 해. 도서는 도서명이나 ISBN으로 검색할 수 있어야 해. 대출 기간은 7일/14일/30일 중에서 선택할 수 있어. 만약 대출하려는 도서가 이미 대출 중이라면, 예약 신청이 가능해야 해. 대출이 완료되면 해당 도서의 상태는 자동으로 '대출중'으로 변경되어야 해.\"}]",
                "id": "9ef357e7-6141-eaa9-f96d-227f7070ac93",
                "elementView": {
                    "_type": "org.uengine.modeling.model.BoundedContext",
                    "height": 590,
                    "id": "9ef357e7-6141-eaa9-f96d-227f7070ac93",
                    "style": "{}",
                    "width": 560,
                    "x": 1235,
                    "y": 450
                },
                "gitURL": None,
                "hexagonalView": {
                    "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
                    "height": 350,
                    "id": "9ef357e7-6141-eaa9-f96d-227f7070ac93",
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
                "definitionId": "163972132_es_05d136ce0010c9a1f5e2fde77b3fa549"
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
    "isAccumulated": False,
    "targetAggregate": {
        "name": "Book",
        "alias": "도서"
    },
    "aggregateDisplayName": "도서",
    "esAliasTransManager": {
        "esValue": {
            "elements": {
                "854a2992-fc9c-69d4-26ff-0f8bbf6a6ec1": {
                    "_type": "org.uengine.modeling.model.BoundedContext",
                    "aggregates": [],
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "description": "[{\"type\":\"userStory\",\"text\":\"도서 관리 화면에서는 새로운 도서를 등록하고 현재 보유한 도서들의 상태를 관리할 수 있어야 해. 도서 등록 시에는 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받아야 해. ISBN은 13자리 숫자여야 하고 중복 확인이 필요해. 카테고리는 소설/비소설/학술/잡지 중에서 선택할 수 있어야 해. 등록된 도서는 처음에 '대출가능' 상태가 되고, 이후 대출/반납 상황에 따라 '대출중', '예약중' 상태로 자동으로 변경되어야 해. 도서가 훼손되거나 분실된 경우 '폐기' 처리가 가능해야 해며, 폐기된 도서는 더 이상 대출이 불가능해야 해.\"}]",
                    "id": "854a2992-fc9c-69d4-26ff-0f8bbf6a6ec1",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.BoundedContext",
                        "height": 590,
                        "id": "854a2992-fc9c-69d4-26ff-0f8bbf6a6ec1",
                        "style": "{}",
                        "width": 560,
                        "x": 650,
                        "y": 450
                    },
                    "gitURL": None,
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
                        "height": 350,
                        "id": "854a2992-fc9c-69d4-26ff-0f8bbf6a6ec1",
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
                    "definitionId": "163972132_es_05d136ce0010c9a1f5e2fde77b3fa549"
                },
                "9ef357e7-6141-eaa9-f96d-227f7070ac93": {
                    "_type": "org.uengine.modeling.model.BoundedContext",
                    "aggregates": [],
                    "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                    "description": "[{\"type\":\"userStory\",\"text\":\"대출/반납 화면에서는 회원이 도서를 대출하고 반납하는 것을 관리할 수 있어야 해. 대출 신청 시에는 회원번호와 이름으로 회원을 확인하고, 대출할 도서를 선택해야 해. 도서는 도서명이나 ISBN으로 검색할 수 있어야 해. 대출 기간은 7일/14일/30일 중에서 선택할 수 있어. 만약 대출하려는 도서가 이미 대출 중이라면, 예약 신청이 가능해야 해. 대출이 완료되면 해당 도서의 상태는 자동으로 '대출중'으로 변경되어야 해.\"}]",
                    "id": "9ef357e7-6141-eaa9-f96d-227f7070ac93",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.BoundedContext",
                        "height": 590,
                        "id": "9ef357e7-6141-eaa9-f96d-227f7070ac93",
                        "style": "{}",
                        "width": 560,
                        "x": 1235,
                        "y": 450
                    },
                    "gitURL": None,
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
                        "height": 350,
                        "id": "9ef357e7-6141-eaa9-f96d-227f7070ac93",
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
                    "definitionId": "163972132_es_05d136ce0010c9a1f5e2fde77b3fa549"
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
            "854a2992-fc9c-69d4-26ff-0f8bbf6a6ec1": "bc-bookManagement",
            "9ef357e7-6141-eaa9-f96d-227f7070ac93": "bc-loanManagement"
        },
        "aliasToUUIDDic": {
            "bc-bookManagement": "854a2992-fc9c-69d4-26ff-0f8bbf6a6ec1",
            "bc-loanManagement": "9ef357e7-6141-eaa9-f96d-227f7070ac93"
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
                "aggregates": []
            },
            {
                "id": "bc-loanManagement",
                "name": "LoanManagement",
                "actors": [],
                "aggregates": []
            }
        ]
    },
    "subjectText": "Creating 도서 Aggregate"
}