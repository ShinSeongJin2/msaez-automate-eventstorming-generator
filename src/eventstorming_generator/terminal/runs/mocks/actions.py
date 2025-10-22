from ....models import *

user_info = {"uid": "test_user"}
information = {"projectId": "test_project"}

bounded_context_id = '0faf38c9-6471-4a6e-b24a-d691ac7ab385'
aggregate_id = 'a932c245-ac83-4d8e-8fe3-eb787fe5943b'

actions_collection = [
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
            objectType="Command",
            type="create",
            ids={
                "boundedContextId": bounded_context_id,
                "aggregateId": aggregate_id,
                "commandId": "cmd-loanBook"
            },
            args={
                "commandName": "LoanBook",
                "commandAlias": "Loan Book",
                "api_verb": "POST",

                "properties": [
                    {
                        "name": "bookId",
                        "type": "Long",
                        "isKey": True
                    },
                    {
                        "name": "title",
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
                "boundedContextId": bounded_context_id,
                "aggregateId": aggregate_id,
                "eventId": "evt-bookLoaned"
            },
            args={
                "eventName": "BookLoaned",
                "eventAlias": "Book Loaned",

                "properties": [
                    {
                        "name": "bookId",
                        "type": "Long",
                        "isKey": True
                    },
                    {
                        "name": "title",
                        "type": "String"
                    }
                ]
            }
        ),

        ActionModel(
            objectType="ReadModel",
            type="create",
            ids={
                "boundedContextId": bounded_context_id,
                "aggregateId": aggregate_id,
                "readModelId": "read-book-details"
            },
            args={
                "readModelName": "BookDetails",
                "readModelAlias": "Book Details",
                "isMultipleResult": False,
                "queryParameters": [
                    {
                        "name": "bookId",
                        "type": "Long",
                        "isKey": True
                    }
                ],
                "actor": "User"
            }
        )
    ]
]

total_actions = {
    "esValue": EsValueModel(elements={'a0f580e4-fc10-4d02-8a63-a81e7811e821': {'_type': 'org.uengine.modeling.model.BoundedContext', 'aggregates': [], 'author': 'EYCl46CwWAWvpz2E1BCUpVgPIpa2', 'description': '# Bounded Context Overview: BookManagement (도서 관리)\n\n## Role\n도서 등록, 상태 관리, 폐기 처리를 담당하며 도서의 생애주기와 상태 변화를 관리한다.\n\n## Key Events\n- BookRegistered\n- BookStatusChanged\n- BookDisposed\n\n# Requirements\n\n## userStory\n\n도서 관리\' 화면에서는 새로운 도서를 등록하고 현재 보유한 도서들의 상태를 관리할 수 있어야 해. 도서 등록 시에는 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받아야 해. ISBN은 13자리 숫자여야 하고 중복 확인이 필요해. 카테고리는 소설/비소설/학술/잡지 중에서 선택할 수 있어야 해. 등록된 도서는 처음에 \'대출가능\' 상태가 되고, 이후 대출/반납 상황에 따라 \'대출중\', \'예약중\' 상태로 자동으로 변경되어야 해. 도서가 훼손되거나 분실된 경우 \'폐기\' 처리가 가능해야 하며, 폐기된 도서는 더 이상 대출이 불가능해야\n\n도서별로 대출 이력과 상태 변경 이력을 조회할 수 있어야 하고, 이를 통해 도서의 대출 현황과 상태 변화를 추적할\n\n## DDL\n\n```sql\n도서 테이블\nCREATE TABLE books (\n    book_id INT AUTO_INCREMENT PRIMARY KEY,\n    title VARCHAR(500) NOT NULL,\n    isbn VARCHAR(13) UNIQUE NOT NULL,\n    author VARCHAR(200) NOT NULL,\n    publisher VARCHAR(200) NOT NULL,\n    category ENUM(\'소설\', \'비소설\', \'학술\', \'잡지\') NOT NULL,\n    status ENUM(\'대출가능\', \'대출중\', \'예약중\', \'폐기\') DEFAULT \'대출가능\',\n    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    disposal_date DATETIME NULL,\n    disposal_reason TEXT NULL,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    INDEX idx_title (title),\n    INDEX idx_isbn (isbn),\n    INDEX idx_status (status),\n    INDEX idx_category (category)\n);\n```\n```sql\n도서 상태 변경 이력 테이블\nCREATE TABLE book_status_history (\n    history_id INT AUTO_INCREMENT PRIMARY KEY,\n    book_id INT NOT NULL,\n    previous_status ENUM(\'대출가능\', \'대출중\', \'예약중\', \'폐기\'),\n    new_status ENUM(\'대출가능\', \'대출중\', \'예약중\', \'폐기\') NOT NULL,\n    change_reason VARCHAR(200),\n    changed_by VARCHAR(100),\n    change_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    FOREIGN KEY (book_id) REFERENCES books(book_id),\n    INDEX idx_book_id (book_id),\n    INDEX idx_change_date (change_date)\n);\n```\n## Event\n\n```json\n{\n  "name": "BookRegistered",\n  "displayName": "도서 등록됨",\n  "actor": "Librarian",\n  "level": 1,\n  "description": "사서가 새로운 도서를 등록하여 도서관 시스템에 추가하였음. 등록 시 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받고, ISBN 중복 및 유효성 검증이 완료됨.",\n  "inputs": [\n    "도서명",\n    "ISBN(13자리)",\n    "저자",\n    "출판사",\n    "카테고리(소설/비소설/학술/잡지)"\n  ],\n  "outputs": [\n    "신규 도서 정보",\n    "도서 상태: 대출가능"\n  ],\n  "nextEvents": [\n    "BookStatusChanged"\n  ]\n}\n```\n\n```json\n{\n  "name": "BookStatusChanged",\n  "displayName": "도서 상태 변경됨",\n  "actor": "System",\n  "level": 2,\n  "description": "도서의 대출/반납/예약/폐기 등 상태 변화가 발생하여 도서 상태가 자동 또는 수동으로 변경됨.",\n  "inputs": [\n    "도서 상태 변경 트리거(대출, 반납, 예약, 폐기 등)",\n    "도서 식별자"\n  ],\n  "outputs": [\n    "변경된 도서 상태"\n  ],\n  "nextEvents": [\n    "BookDisposed",\n    "BookLoaned",\n    "BookReturned",\n    "BookReserved"\n  ]\n}\n```\n\n```json\n{\n  "name": "BookDisposed",\n  "displayName": "도서 폐기됨",\n  "actor": "Librarian",\n  "level": 3,\n  "description": "도서가 훼손 또는 분실되어 사서에 의해 폐기 처리됨. 폐기된 도서는 더 이상 대출이 불가능함.",\n  "inputs": [\n    "도서 식별자",\n    "폐기 사유"\n  ],\n  "outputs": [\n    "도서 상태: 폐기"\n  ],\n  "nextEvents": []\n}\n```\n\n## Context Relations\n\n### BookManagement-LoanAndReservation\n- **Type**: Pub/Sub\n- **Direction**: sends to 대출/반납 및 예약 (LoanAndReservation)\n- **Reason**: 도서 상태 변경(대출가능, 대출중, 예약중, 폐기 등)이 발생하면 대출/반납 및 예약 컨텍스트에서 이를 구독하여 대출/예약 프로세스에 반영한다.\n- **Interaction Pattern**: 도서 관리에서 도서 상태 변경 이벤트를 발행하면 대출/반납 및 예약 컨텍스트가 이를 구독하여 처리한다.\n\n### BookManagement-LoanHistory\n- **Type**: Pub/Sub\n- **Direction**: sends to 이력 관리 (LoanHistory)\n- **Reason**: 도서 등록, 폐기 등 도서 상태 변화 이력도 이력 관리 컨텍스트에서 기록할 수 있도록 이벤트를 발행한다.\n- **Interaction Pattern**: 도서 관리에서 도서 등록, 폐기 등 상태 변화 이벤트를 발행하면 이력 관리 컨텍스트가 이를 구독하여 상태 변경 이력을 기록한다.', 'id': 'a0f580e4-fc10-4d02-8a63-a81e7811e821', 'elementView': {'_type': 'org.uengine.modeling.model.BoundedContext', 'height': 590, 'id': 'a0f580e4-fc10-4d02-8a63-a81e7811e821', 'style': '{}', 'width': 560, 'x': 600, 'y': 450}, 'gitURL': None, 'hexagonalView': {'_type': 'org.uengine.modeling.model.BoundedContextHexagonal', 'height': 350, 'id': 'a0f580e4-fc10-4d02-8a63-a81e7811e821', 'style': '{}', 'width': 350, 'x': 235, 'y': 365}, 'members': [], 'name': 'BookManagement', 'traceName': 'BookManagement', 'displayName': '도서 관리', 'oldName': '', 'policies': [], 'portGenerated': 8080, 'preferredPlatform': 'template-spring-boot', 'preferredPlatformConf': {}, 'rotateStatus': False, 'tempId': '', 'templatePerElements': {}, 'views': [], 'definitionId': '163972132_es_a4afe53e52e57652bdbd6dac8e734470', 'requirements': {'ddl': "도서 테이블\nCREATE TABLE books (\n    book_id INT AUTO_INCREMENT PRIMARY KEY,\n    title VARCHAR(500) NOT NULL,\n    isbn VARCHAR(13) UNIQUE NOT NULL,\n    author VARCHAR(200) NOT NULL,\n    publisher VARCHAR(200) NOT NULL,\n    category ENUM('소설', '비소설', '학술', '잡지') NOT NULL,\n    status ENUM('대출가능', '대출중', '예약중', '폐기') DEFAULT '대출가능',\n    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    disposal_date DATETIME NULL,\n    disposal_reason TEXT NULL,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    INDEX idx_title (title),\n    INDEX idx_isbn (isbn),\n    INDEX idx_status (status),\n    INDEX idx_category (category)\n);\n도서 상태 변경 이력 테이블\nCREATE TABLE book_status_history (\n    history_id INT AUTO_INCREMENT PRIMARY KEY,\n    book_id INT NOT NULL,\n    previous_status ENUM('대출가능', '대출중', '예약중', '폐기'),\n    new_status ENUM('대출가능', '대출중', '예약중', '폐기') NOT NULL,\n    change_reason VARCHAR(200),\n    changed_by VARCHAR(100),\n    change_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    FOREIGN KEY (book_id) REFERENCES books(book_id),\n    INDEX idx_book_id (book_id),\n    INDEX idx_change_date (change_date)\n);", 'ddlFields': [{'fieldName': 'book_id', 'refs': [[[26, 5], [26, 42]], [[87, 5], [87, 24]]]}, {'fieldName': 'title', 'refs': [[[27, 5], [27, 31]]]}, {'fieldName': 'isbn', 'refs': [[[28, 5], [28, 36]]]}, {'fieldName': 'author', 'refs': [[[29, 5], [29, 32]]]}, {'fieldName': 'publisher', 'refs': [[[30, 5], [30, 35]]]}, {'fieldName': 'category', 'refs': [[[31, 5], [31, 51]]]}, {'fieldName': 'status', 'refs': [[[32, 5], [32, 51]]]}, {'fieldName': 'registration_date', 'refs': [[[33, 5], [33, 56]]]}, {'fieldName': 'disposal_date', 'refs': [[[34, 5], [34, 31]]]}, {'fieldName': 'disposal_reason', 'refs': [[[35, 5], [35, 29]]]}, {'fieldName': 'created_at', 'refs': [[[36, 5], [36, 49]]]}, {'fieldName': 'updated_at', 'refs': [[[37, 5], [37, 77]]]}, {'fieldName': 'history_id', 'refs': [[[86, 5], [86, 45]]]}, {'fieldName': 'previous_status', 'refs': [[[88, 5], [88, 53]]]}, {'fieldName': 'new_status', 'refs': [[[89, 5], [89, 56]]]}, {'fieldName': 'change_reason', 'refs': [[[90, 5], [90, 30]]]}, {'fieldName': 'changed_by', 'refs': [[[91, 5], [91, 27]]]}, {'fieldName': 'change_date', 'refs': [[[92, 5], [92, 50]]]}], 'description': '# Bounded Context Overview: BookManagement (도서 관리)\n\n## Role\n도서 등록, 상태 관리, 폐기 처리를 담당하며 도서의 생애주기와 상태 변화를 관리한다.\n\n## Key Events\n- BookRegistered\n- BookStatusChanged\n- BookDisposed\n\n# Requirements\n\n## userStory\n\n도서 관리\' 화면에서는 새로운 도서를 등록하고 현재 보유한 도서들의 상태를 관리할 수 있어야 해. 도서 등록 시에는 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받아야 해. ISBN은 13자리 숫자여야 하고 중복 확인이 필요해. 카테고리는 소설/비소설/학술/잡지 중에서 선택할 수 있어야 해. 등록된 도서는 처음에 \'대출가능\' 상태가 되고, 이후 대출/반납 상황에 따라 \'대출중\', \'예약중\' 상태로 자동으로 변경되어야 해. 도서가 훼손되거나 분실된 경우 \'폐기\' 처리가 가능해야 하며, 폐기된 도서는 더 이상 대출이 불가능해야\n\n도서별로 대출 이력과 상태 변경 이력을 조회할 수 있어야 하고, 이를 통해 도서의 대출 현황과 상태 변화를 추적할\n\n## DDL\n\n```sql\n도서 테이블\nCREATE TABLE books (\n    book_id INT AUTO_INCREMENT PRIMARY KEY,\n    title VARCHAR(500) NOT NULL,\n    isbn VARCHAR(13) UNIQUE NOT NULL,\n    author VARCHAR(200) NOT NULL,\n    publisher VARCHAR(200) NOT NULL,\n    category ENUM(\'소설\', \'비소설\', \'학술\', \'잡지\') NOT NULL,\n    status ENUM(\'대출가능\', \'대출중\', \'예약중\', \'폐기\') DEFAULT \'대출가능\',\n    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    disposal_date DATETIME NULL,\n    disposal_reason TEXT NULL,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    INDEX idx_title (title),\n    INDEX idx_isbn (isbn),\n    INDEX idx_status (status),\n    INDEX idx_category (category)\n);\n```\n```sql\n도서 상태 변경 이력 테이블\nCREATE TABLE book_status_history (\n    history_id INT AUTO_INCREMENT PRIMARY KEY,\n    book_id INT NOT NULL,\n    previous_status ENUM(\'대출가능\', \'대출중\', \'예약중\', \'폐기\'),\n    new_status ENUM(\'대출가능\', \'대출중\', \'예약중\', \'폐기\') NOT NULL,\n    change_reason VARCHAR(200),\n    changed_by VARCHAR(100),\n    change_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    FOREIGN KEY (book_id) REFERENCES books(book_id),\n    INDEX idx_book_id (book_id),\n    INDEX idx_change_date (change_date)\n);\n```\n## Event\n\n```json\n{\n  "name": "BookRegistered",\n  "displayName": "도서 등록됨",\n  "actor": "Librarian",\n  "level": 1,\n  "description": "사서가 새로운 도서를 등록하여 도서관 시스템에 추가하였음. 등록 시 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받고, ISBN 중복 및 유효성 검증이 완료됨.",\n  "inputs": [\n    "도서명",\n    "ISBN(13자리)",\n    "저자",\n    "출판사",\n    "카테고리(소설/비소설/학술/잡지)"\n  ],\n  "outputs": [\n    "신규 도서 정보",\n    "도서 상태: 대출가능"\n  ],\n  "nextEvents": [\n    "BookStatusChanged"\n  ]\n}\n```\n\n```json\n{\n  "name": "BookStatusChanged",\n  "displayName": "도서 상태 변경됨",\n  "actor": "System",\n  "level": 2,\n  "description": "도서의 대출/반납/예약/폐기 등 상태 변화가 발생하여 도서 상태가 자동 또는 수동으로 변경됨.",\n  "inputs": [\n    "도서 상태 변경 트리거(대출, 반납, 예약, 폐기 등)",\n    "도서 식별자"\n  ],\n  "outputs": [\n    "변경된 도서 상태"\n  ],\n  "nextEvents": [\n    "BookDisposed",\n    "BookLoaned",\n    "BookReturned",\n    "BookReserved"\n  ]\n}\n```\n\n```json\n{\n  "name": "BookDisposed",\n  "displayName": "도서 폐기됨",\n  "actor": "Librarian",\n  "level": 3,\n  "description": "도서가 훼손 또는 분실되어 사서에 의해 폐기 처리됨. 폐기된 도서는 더 이상 대출이 불가능함.",\n  "inputs": [\n    "도서 식별자",\n    "폐기 사유"\n  ],\n  "outputs": [\n    "도서 상태: 폐기"\n  ],\n  "nextEvents": []\n}\n```\n\n## Context Relations\n\n### BookManagement-LoanAndReservation\n- **Type**: Pub/Sub\n- **Direction**: sends to 대출/반납 및 예약 (LoanAndReservation)\n- **Reason**: 도서 상태 변경(대출가능, 대출중, 예약중, 폐기 등)이 발생하면 대출/반납 및 예약 컨텍스트에서 이를 구독하여 대출/예약 프로세스에 반영한다.\n- **Interaction Pattern**: 도서 관리에서 도서 상태 변경 이벤트를 발행하면 대출/반납 및 예약 컨텍스트가 이를 구독하여 처리한다.\n\n### BookManagement-LoanHistory\n- **Type**: Pub/Sub\n- **Direction**: sends to 이력 관리 (LoanHistory)\n- **Reason**: 도서 등록, 폐기 등 도서 상태 변화 이력도 이력 관리 컨텍스트에서 기록할 수 있도록 이벤트를 발행한다.\n- **Interaction Pattern**: 도서 관리에서 도서 등록, 폐기 등 상태 변화 이벤트를 발행하면 이력 관리 컨텍스트가 이를 구독하여 상태 변경 이력을 기록한다.', 'event': '{\n  "name": "BookRegistered",\n  "displayName": "도서 등록됨",\n  "actor": "Librarian",\n  "level": 1,\n  "description": "사서가 새로운 도서를 등록하여 도서관 시스템에 추가하였음. 등록 시 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받고, ISBN 중복 및 유효성 검증이 완료됨.",\n  "inputs": [\n    "도서명",\n    "ISBN(13자리)",\n    "저자",\n    "출판사",\n    "카테고리(소설/비소설/학술/잡지)"\n  ],\n  "outputs": [\n    "신규 도서 정보",\n    "도서 상태: 대출가능"\n  ],\n  "nextEvents": [\n    "BookStatusChanged"\n  ],\n  "refs": [\n    [\n      [\n        3,\n        57\n      ],\n      [\n        3,\n        100\n      ]\n    ],\n    [\n      [\n        3,\n        105\n      ],\n      [\n        3,\n        128\n      ]\n    ],\n    [\n      [\n        3,\n        136\n      ],\n      [\n        3,\n        161\n      ]\n    ]\n  ]\n}\n{\n  "name": "BookStatusChanged",\n  "displayName": "도서 상태 변경됨",\n  "actor": "System",\n  "level": 2,\n  "description": "도서의 대출/반납/예약/폐기 등 상태 변화가 발생하여 도서 상태가 자동 또는 수동으로 변경됨.",\n  "inputs": [\n    "도서 상태 변경 트리거(대출, 반납, 예약, 폐기 등)",\n    "도서 식별자"\n  ],\n  "outputs": [\n    "변경된 도서 상태"\n  ],\n  "nextEvents": [\n    "BookDisposed",\n    "BookLoaned",\n    "BookReturned",\n    "BookReserved"\n  ],\n  "refs": [\n    [\n      [\n        3,\n        191\n      ],\n      [\n        3,\n        238\n      ]\n    ],\n    [\n      [\n        3,\n        264\n      ],\n      [\n        3,\n        302\n      ]\n    ],\n    [\n      [\n        7,\n        150\n      ],\n      [\n        7,\n        167\n      ]\n    ],\n    [\n      [\n        7,\n        167\n      ],\n      [\n        7,\n        175\n      ]\n    ]\n  ]\n}\n{\n  "name": "BookDisposed",\n  "displayName": "도서 폐기됨",\n  "actor": "Librarian",\n  "level": 3,\n  "description": "도서가 훼손 또는 분실되어 사서에 의해 폐기 처리됨. 폐기된 도서는 더 이상 대출이 불가능함.",\n  "inputs": [\n    "도서 식별자",\n    "폐기 사유"\n  ],\n  "outputs": [\n    "도서 상태: 폐기"\n  ],\n  "nextEvents": [],\n  "refs": [\n    [\n      [\n        3,\n        264\n      ],\n      [\n        3,\n        302\n      ]\n    ]\n  ]\n}', 'eventNames': 'BookRegistered, BookStatusChanged, BookDisposed 이벤트가 발생할 수 있어.', 'siteMap': [{'boundedContext': 'BookManagement', 'description': '현재 보유 도서의 목록과 상태를 조회', 'functionType': 'view', 'id': 'book-list-view', 'name': 'BookListView', 'title': '도서 목록 조회', 'uiRequirements': '도서명, ISBN, 저자, 출판사, 카테고리, 상태(대출가능/대출중/예약중/폐기) 필터 및 검색, 페이징 지원'}, {'boundedContext': 'BookManagement', 'description': '새로운 도서를 등록', 'functionType': 'command', 'id': 'book-create-command', 'name': 'BookCreateCommand', 'title': '도서 등록', 'uiRequirements': "도서명, ISBN(13자리, 중복확인), 저자, 출판사, 카테고리(소설/비소설/학술/잡지) 입력 폼, 등록 시 상태는 '대출가능'으로 설정"}, {'boundedContext': 'BookManagement', 'description': '기존 도서의 정보를 수정', 'functionType': 'command', 'id': 'book-edit-command', 'name': 'BookEditCommand', 'title': '도서 정보 수정', 'uiRequirements': '도서명, 저자, 출판사, 카테고리 등 수정, ISBN은 수정 불가, 상태 변경 불가'}, {'boundedContext': 'BookManagement', 'description': '훼손 또는 분실된 도서를 폐기 처리', 'functionType': 'command', 'id': 'book-dispose-command', 'name': 'BookDisposeCommand', 'title': '도서 폐기 처리', 'uiRequirements': "도서 목록에서 폐기 처리 버튼, 폐기 사유 입력, 폐기 시 상태를 '폐기'로 변경, 폐기 도서는 대출 불가"}, {'boundedContext': 'BookManagement', 'description': '도서별 상태 변경 이력을 조회', 'functionType': 'view', 'id': 'book-status-change-view', 'name': 'BookStatusChangeHistoryView', 'title': '도서 상태 변경 이력 조회', 'uiRequirements': '도서별 상태 변경(대출가능/대출중/예약중/폐기 등) 이력 리스트, 변경일시, 변경자, 변경 사유 표시'}], 'userStory': "도서 관리' 화면에서는 새로운 도서를 등록하고 현재 보유한 도서들의 상태를 관리할 수 있어야 해. 도서 등록 시에는 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받아야 해. ISBN은 13자리 숫자여야 하고 중복 확인이 필요해. 카테고리는 소설/비소설/학술/잡지 중에서 선택할 수 있어야 해. 등록된 도서는 처음에 '대출가능' 상태가 되고, 이후 대출/반납 상황에 따라 '대출중', '예약중' 상태로 자동으로 변경되어야 해. 도서가 훼손되거나 분실된 경우 '폐기' 처리가 가능해야 하며, 폐기된 도서는 더 이상 대출이 불가능해야\n도서별로 대출 이력과 상태 변경 이력을 조회할 수 있어야 하고, 이를 통해 도서의 대출 현황과 상태 변화를 추적할"}}, 'a35f39e7-6201-441e-9b5b-931aeba36079': {'_type': 'org.uengine.modeling.model.BoundedContext', 'aggregates': [], 'author': 'EYCl46CwWAWvpz2E1BCUpVgPIpa2', 'description': '# Bounded Context Overview: LoanAndReservation (대출/반납 및 예약)\n\n## Role\n회원의 도서 대출, 반납, 연장, 예약을 관리하고 도서 상태 변경을 트리거한다.\n\n## Key Events\n- BookLoaned\n- BookReserved\n- BookReturned\n- LoanExtended\n\n# Requirements\n\n## userStory\n\n대출/반납을 통합적으로 관리하는\n\n대출/반납\' 화면에서는 회원이 도서를 대출하고 반납하는 것을 관리할 수 있어야 해. 대출 신청 시에는 회원번호와 이름으로 회원을 확인하고, 대출할\n\n예약\n\n대출 현황 화면에서는 현재 대출 중인 도서들의 목록을 볼 수 있어야 해. 각 대출 건에 대해 대출일, 반납\n\n연장\n\n대출 이력과 상태\n\n## DDL\n\n```sql\nCREATE TABLE loans (\n    loan_id INT AUTO_INCREMENT PRIMARY KEY,\n    member_id VARCHAR(20) NOT NULL,\n    book_id INT NOT NULL,\n    loan_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    due_date DATETIME NOT NULL,\n    return_date DATETIME NULL,\n    loan_period_days INT NOT NULL CHECK (loan_period_days IN (7, 14, 30)),\n    status ENUM(\'대출중\', \'연체\', \'반납완료\', \'연장\') DEFAULT \'대출중\',\n    extension_count INT DEFAULT 0,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    FOREIGN KEY (member_id) REFERENCES members(member_id),\n    FOREIGN KEY (book_id) REFERENCES books(book_id),\n    INDEX idx_member_id (member_id),\n    INDEX idx_book_id (book_id),\n    INDEX idx_status (status),\n    INDEX idx_due_date (due_date)\n);\n```\n```sql\nCREATE TABLE reservations (\n    reservation_id INT AUTO_INCREMENT PRIMARY KEY,\n    member_id VARCHAR(20) NOT NULL,\n    book_id INT NOT NULL,\n    reservation_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    status ENUM(\'예약중\', \'예약완료\', \'예약취소\', \'예약만료\') DEFAULT \'예약중\',\n    notification_sent BOOLEAN DEFAULT FALSE,\n    expiry_date DATETIME NULL,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    FOREIGN KEY (member_id) REFERENCES members(member_id),\n    FOREIGN KEY (book_id) REFERENCES books(book_id),\n    INDEX idx_member_id (member_id),\n    INDEX idx_book_id (book_id),\n    INDEX idx_status (status),\n    INDEX idx_reservation_date (reservation_date)\n);\n```\n```sql\nCREATE TABLE loan_history (\n    history_id INT AUTO_INCREMENT PRIMARY KEY,\n    loan_id INT NOT NULL,\n    action_type ENUM(\'대출\', \'반납\', \'연장\', \'연체알림\', \'분실신고\') NOT NULL,\n    action_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    previous_due_date DATETIME NULL,\n    new_due_date DATETIME NULL,\n    notes TEXT,\n    processed_by VARCHAR(100),\n    FOREIGN KEY (loan_id) REFERENCES loans(loan_id),\n    INDEX idx_loan_id (loan_id),\n    INDEX idx_action_type (action_type),\n    INDEX idx_action_date (action_date)\n);\n```\n## Event\n\n```json\n{\n  "name": "BookLoaned",\n  "displayName": "도서 대출됨",\n  "actor": "Member",\n  "level": 4,\n  "description": "회원이 도서 대출을 신청하고, 회원 인증 및 도서 상태 확인 후 대출이 승인됨. 대출 기간이 설정되고 도서 상태가 \'대출중\'으로 변경됨.",\n  "inputs": [\n    "회원번호",\n    "이름",\n    "도서 식별자",\n    "대출 기간(7/14/30일)"\n  ],\n  "outputs": [\n    "대출 정보",\n    "도서 상태: 대출중"\n  ],\n  "nextEvents": [\n    "BookStatusChanged",\n    "LoanHistoryRecorded"\n  ]\n}\n```\n\n```json\n{\n  "name": "BookReserved",\n  "displayName": "도서 예약됨",\n  "actor": "Member",\n  "level": 5,\n  "description": "회원이 대출 중인 도서에 대해 예약을 신청함. 예약이 완료되면 도서 상태가 \'예약중\'으로 변경됨.",\n  "inputs": [\n    "회원번호",\n    "도서 식별자"\n  ],\n  "outputs": [\n    "예약 정보",\n    "도서 상태: 예약중"\n  ],\n  "nextEvents": [\n    "BookStatusChanged",\n    "ReservationHistoryRecorded"\n  ]\n}\n```\n\n```json\n{\n  "name": "BookReturned",\n  "displayName": "도서 반납됨",\n  "actor": "Member",\n  "level": 6,\n  "description": "회원이 대출한 도서를 반납함. 반납 시 도서 상태가 \'대출가능\'으로 변경되고, 예약자가 있을 경우 \'예약중\'으로 변경됨.",\n  "inputs": [\n    "회원번호",\n    "도서 식별자"\n  ],\n  "outputs": [\n    "도서 상태: 대출가능 또는 예약중",\n    "반납 처리 정보"\n  ],\n  "nextEvents": [\n    "BookStatusChanged",\n    "LoanHistoryRecorded"\n  ]\n}\n```\n\n```json\n{\n  "name": "LoanExtended",\n  "displayName": "대출 연장됨",\n  "actor": "Member",\n  "level": 7,\n  "description": "회원이 대출 중인 도서의 대출 기간을 연장함. 연장 후 대출 정보와 반납 예정일이 갱신됨.",\n  "inputs": [\n    "회원번호",\n    "도서 식별자",\n    "연장 기간"\n  ],\n  "outputs": [\n    "갱신된 대출 정보",\n    "새 반납 예정일"\n  ],\n  "nextEvents": [\n    "LoanHistoryRecorded"\n  ]\n}\n```\n\n## Context Relations\n\n### BookManagement-LoanAndReservation\n- **Type**: Pub/Sub\n- **Direction**: receives from 도서 관리 (BookManagement)\n- **Reason**: 도서 상태 변경(대출가능, 대출중, 예약중, 폐기 등)이 발생하면 대출/반납 및 예약 컨텍스트에서 이를 구독하여 대출/예약 프로세스에 반영한다.\n- **Interaction Pattern**: 도서 관리에서 도서 상태 변경 이벤트를 발행하면 대출/반납 및 예약 컨텍스트가 이를 구독하여 처리한다.\n\n### LoanAndReservation-LoanHistory\n- **Type**: Pub/Sub\n- **Direction**: sends to 이력 관리 (LoanHistory)\n- **Reason**: 대출, 반납, 연장, 예약 등 이벤트 발생 시 이력 관리 컨텍스트에서 해당 이벤트를 구독하여 이력을 기록한다.\n- **Interaction Pattern**: 대출/반납 및 예약에서 대출/반납/연장/예약 이벤트를 발행하면 이력 관리 컨텍스트가 이를 구독하여 이력 데이터를 생성한다.', 'id': 'a35f39e7-6201-441e-9b5b-931aeba36079', 'elementView': {'_type': 'org.uengine.modeling.model.BoundedContext', 'height': 590, 'id': 'a35f39e7-6201-441e-9b5b-931aeba36079', 'style': '{}', 'width': 560, 'x': 1185.0, 'y': 450}, 'gitURL': None, 'hexagonalView': {'_type': 'org.uengine.modeling.model.BoundedContextHexagonal', 'height': 350, 'id': 'a35f39e7-6201-441e-9b5b-931aeba36079', 'style': '{}', 'width': 350, 'x': 235, 'y': 365}, 'members': [], 'name': 'LoanAndReservation', 'traceName': 'LoanAndReservation', 'displayName': '대출/반납 및 예약', 'oldName': '', 'policies': [], 'portGenerated': 8081, 'preferredPlatform': 'template-spring-boot', 'preferredPlatformConf': {}, 'rotateStatus': False, 'tempId': '', 'templatePerElements': {}, 'views': [], 'definitionId': '163972132_es_a4afe53e52e57652bdbd6dac8e734470', 'requirements': {'ddl': "CREATE TABLE loans (\n    loan_id INT AUTO_INCREMENT PRIMARY KEY,\n    member_id VARCHAR(20) NOT NULL,\n    book_id INT NOT NULL,\n    loan_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    due_date DATETIME NOT NULL,\n    return_date DATETIME NULL,\n    loan_period_days INT NOT NULL CHECK (loan_period_days IN (7, 14, 30)),\n    status ENUM('대출중', '연체', '반납완료', '연장') DEFAULT '대출중',\n    extension_count INT DEFAULT 0,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    FOREIGN KEY (member_id) REFERENCES members(member_id),\n    FOREIGN KEY (book_id) REFERENCES books(book_id),\n    INDEX idx_member_id (member_id),\n    INDEX idx_book_id (book_id),\n    INDEX idx_status (status),\n    INDEX idx_due_date (due_date)\n);\nCREATE TABLE reservations (\n    reservation_id INT AUTO_INCREMENT PRIMARY KEY,\n    member_id VARCHAR(20) NOT NULL,\n    book_id INT NOT NULL,\n    reservation_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    status ENUM('예약중', '예약완료', '예약취소', '예약만료') DEFAULT '예약중',\n    notification_sent BOOLEAN DEFAULT FALSE,\n    expiry_date DATETIME NULL,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    FOREIGN KEY (member_id) REFERENCES members(member_id),\n    FOREIGN KEY (book_id) REFERENCES books(book_id),\n    INDEX idx_member_id (member_id),\n    INDEX idx_book_id (book_id),\n    INDEX idx_status (status),\n    INDEX idx_reservation_date (reservation_date)\n);\nCREATE TABLE loan_history (\n    history_id INT AUTO_INCREMENT PRIMARY KEY,\n    loan_id INT NOT NULL,\n    action_type ENUM('대출', '반납', '연장', '연체알림', '분실신고') NOT NULL,\n    action_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    previous_due_date DATETIME NULL,\n    new_due_date DATETIME NULL,\n    notes TEXT,\n    processed_by VARCHAR(100),\n    FOREIGN KEY (loan_id) REFERENCES loans(loan_id),\n    INDEX idx_loan_id (loan_id),\n    INDEX idx_action_type (action_type),\n    INDEX idx_action_date (action_date)\n);", 'ddlFields': [{'fieldName': 'loan_id', 'refs': [[[46, 5], [46, 38]], [[101, 5], [101, 24]]]}, {'fieldName': 'member_id', 'refs': [[[47, 5], [47, 34]], [[68, 5], [68, 34]]]}, {'fieldName': 'book_id', 'refs': [[[48, 5], [48, 24]], [[69, 5], [69, 24]]]}, {'fieldName': 'loan_date', 'refs': [[[49, 5], [49, 48]]]}, {'fieldName': 'due_date', 'refs': [[[50, 5], [50, 30]]]}, {'fieldName': 'return_date', 'refs': [[[51, 5], [51, 29]]]}, {'fieldName': 'loan_period_days', 'refs': [[[52, 5], [52, 39]]]}, {'fieldName': 'status', 'refs': [[[53, 5], [53, 50]], [[71, 5], [71, 54]]]}, {'fieldName': 'extension_count', 'refs': [[[54, 5], [54, 31]]]}, {'fieldName': 'created_at', 'refs': [[[55, 5], [55, 49]], [[74, 5], [74, 49]]]}, {'fieldName': 'updated_at', 'refs': [[[56, 5], [56, 77]], [[75, 5], [75, 77]]]}, {'fieldName': 'reservation_id', 'refs': [[[67, 5], [67, 45]]]}, {'fieldName': 'reservation_date', 'refs': [[[70, 5], [70, 55]]]}, {'fieldName': 'notification_sent', 'refs': [[[72, 5], [72, 37]]]}, {'fieldName': 'expiry_date', 'refs': [[[73, 5], [73, 29]]]}, {'fieldName': 'history_id', 'refs': [[[100, 5], [100, 41]]]}, {'fieldName': 'action_type', 'refs': [[[102, 5], [102, 63]]]}, {'fieldName': 'action_date', 'refs': [[[103, 5], [103, 50]]]}, {'fieldName': 'previous_due_date', 'refs': [[[104, 5], [104, 35]]]}, {'fieldName': 'new_due_date', 'refs': [[[105, 5], [105, 30]]]}, {'fieldName': 'notes', 'refs': [[[106, 5], [106, 14]]]}, {'fieldName': 'processed_by', 'refs': [[[107, 5], [107, 29]]]}], 'description': '# Bounded Context Overview: LoanAndReservation (대출/반납 및 예약)\n\n## Role\n회원의 도서 대출, 반납, 연장, 예약을 관리하고 도서 상태 변경을 트리거한다.\n\n## Key Events\n- BookLoaned\n- BookReserved\n- BookReturned\n- LoanExtended\n\n# Requirements\n\n## userStory\n\n대출/반납을 통합적으로 관리하는\n\n대출/반납\' 화면에서는 회원이 도서를 대출하고 반납하는 것을 관리할 수 있어야 해. 대출 신청 시에는 회원번호와 이름으로 회원을 확인하고, 대출할\n\n예약\n\n대출 현황 화면에서는 현재 대출 중인 도서들의 목록을 볼 수 있어야 해. 각 대출 건에 대해 대출일, 반납\n\n연장\n\n대출 이력과 상태\n\n## DDL\n\n```sql\nCREATE TABLE loans (\n    loan_id INT AUTO_INCREMENT PRIMARY KEY,\n    member_id VARCHAR(20) NOT NULL,\n    book_id INT NOT NULL,\n    loan_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    due_date DATETIME NOT NULL,\n    return_date DATETIME NULL,\n    loan_period_days INT NOT NULL CHECK (loan_period_days IN (7, 14, 30)),\n    status ENUM(\'대출중\', \'연체\', \'반납완료\', \'연장\') DEFAULT \'대출중\',\n    extension_count INT DEFAULT 0,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    FOREIGN KEY (member_id) REFERENCES members(member_id),\n    FOREIGN KEY (book_id) REFERENCES books(book_id),\n    INDEX idx_member_id (member_id),\n    INDEX idx_book_id (book_id),\n    INDEX idx_status (status),\n    INDEX idx_due_date (due_date)\n);\n```\n```sql\nCREATE TABLE reservations (\n    reservation_id INT AUTO_INCREMENT PRIMARY KEY,\n    member_id VARCHAR(20) NOT NULL,\n    book_id INT NOT NULL,\n    reservation_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    status ENUM(\'예약중\', \'예약완료\', \'예약취소\', \'예약만료\') DEFAULT \'예약중\',\n    notification_sent BOOLEAN DEFAULT FALSE,\n    expiry_date DATETIME NULL,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    FOREIGN KEY (member_id) REFERENCES members(member_id),\n    FOREIGN KEY (book_id) REFERENCES books(book_id),\n    INDEX idx_member_id (member_id),\n    INDEX idx_book_id (book_id),\n    INDEX idx_status (status),\n    INDEX idx_reservation_date (reservation_date)\n);\n```\n```sql\nCREATE TABLE loan_history (\n    history_id INT AUTO_INCREMENT PRIMARY KEY,\n    loan_id INT NOT NULL,\n    action_type ENUM(\'대출\', \'반납\', \'연장\', \'연체알림\', \'분실신고\') NOT NULL,\n    action_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    previous_due_date DATETIME NULL,\n    new_due_date DATETIME NULL,\n    notes TEXT,\n    processed_by VARCHAR(100),\n    FOREIGN KEY (loan_id) REFERENCES loans(loan_id),\n    INDEX idx_loan_id (loan_id),\n    INDEX idx_action_type (action_type),\n    INDEX idx_action_date (action_date)\n);\n```\n## Event\n\n```json\n{\n  "name": "BookLoaned",\n  "displayName": "도서 대출됨",\n  "actor": "Member",\n  "level": 4,\n  "description": "회원이 도서 대출을 신청하고, 회원 인증 및 도서 상태 확인 후 대출이 승인됨. 대출 기간이 설정되고 도서 상태가 \'대출중\'으로 변경됨.",\n  "inputs": [\n    "회원번호",\n    "이름",\n    "도서 식별자",\n    "대출 기간(7/14/30일)"\n  ],\n  "outputs": [\n    "대출 정보",\n    "도서 상태: 대출중"\n  ],\n  "nextEvents": [\n    "BookStatusChanged",\n    "LoanHistoryRecorded"\n  ]\n}\n```\n\n```json\n{\n  "name": "BookReserved",\n  "displayName": "도서 예약됨",\n  "actor": "Member",\n  "level": 5,\n  "description": "회원이 대출 중인 도서에 대해 예약을 신청함. 예약이 완료되면 도서 상태가 \'예약중\'으로 변경됨.",\n  "inputs": [\n    "회원번호",\n    "도서 식별자"\n  ],\n  "outputs": [\n    "예약 정보",\n    "도서 상태: 예약중"\n  ],\n  "nextEvents": [\n    "BookStatusChanged",\n    "ReservationHistoryRecorded"\n  ]\n}\n```\n\n```json\n{\n  "name": "BookReturned",\n  "displayName": "도서 반납됨",\n  "actor": "Member",\n  "level": 6,\n  "description": "회원이 대출한 도서를 반납함. 반납 시 도서 상태가 \'대출가능\'으로 변경되고, 예약자가 있을 경우 \'예약중\'으로 변경됨.",\n  "inputs": [\n    "회원번호",\n    "도서 식별자"\n  ],\n  "outputs": [\n    "도서 상태: 대출가능 또는 예약중",\n    "반납 처리 정보"\n  ],\n  "nextEvents": [\n    "BookStatusChanged",\n    "LoanHistoryRecorded"\n  ]\n}\n```\n\n```json\n{\n  "name": "LoanExtended",\n  "displayName": "대출 연장됨",\n  "actor": "Member",\n  "level": 7,\n  "description": "회원이 대출 중인 도서의 대출 기간을 연장함. 연장 후 대출 정보와 반납 예정일이 갱신됨.",\n  "inputs": [\n    "회원번호",\n    "도서 식별자",\n    "연장 기간"\n  ],\n  "outputs": [\n    "갱신된 대출 정보",\n    "새 반납 예정일"\n  ],\n  "nextEvents": [\n    "LoanHistoryRecorded"\n  ]\n}\n```\n\n## Context Relations\n\n### BookManagement-LoanAndReservation\n- **Type**: Pub/Sub\n- **Direction**: receives from 도서 관리 (BookManagement)\n- **Reason**: 도서 상태 변경(대출가능, 대출중, 예약중, 폐기 등)이 발생하면 대출/반납 및 예약 컨텍스트에서 이를 구독하여 대출/예약 프로세스에 반영한다.\n- **Interaction Pattern**: 도서 관리에서 도서 상태 변경 이벤트를 발행하면 대출/반납 및 예약 컨텍스트가 이를 구독하여 처리한다.\n\n### LoanAndReservation-LoanHistory\n- **Type**: Pub/Sub\n- **Direction**: sends to 이력 관리 (LoanHistory)\n- **Reason**: 대출, 반납, 연장, 예약 등 이벤트 발생 시 이력 관리 컨텍스트에서 해당 이벤트를 구독하여 이력을 기록한다.\n- **Interaction Pattern**: 대출/반납 및 예약에서 대출/반납/연장/예약 이벤트를 발행하면 이력 관리 컨텍스트가 이를 구독하여 이력 데이터를 생성한다.', 'event': '{\n  "name": "BookLoaned",\n  "displayName": "도서 대출됨",\n  "actor": "Member",\n  "level": 4,\n  "description": "회원이 도서 대출을 신청하고, 회원 인증 및 도서 상태 확인 후 대출이 승인됨. 대출 기간이 설정되고 도서 상태가 \'대출중\'으로 변경됨.",\n  "inputs": [\n    "회원번호",\n    "이름",\n    "도서 식별자",\n    "대출 기간(7/14/30일)"\n  ],\n  "outputs": [\n    "대출 정보",\n    "도서 상태: 대출중"\n  ],\n  "nextEvents": [\n    "BookStatusChanged",\n    "LoanHistoryRecorded"\n  ],\n  "refs": [\n    [\n      [\n        5,\n        49\n      ],\n      [\n        5,\n        91\n      ]\n    ],\n    [\n      [\n        5,\n        59\n      ],\n      [\n        5,\n        77\n      ]\n    ],\n    [\n      [\n        5,\n        43\n      ],\n      [\n        5,\n        126\n      ]\n    ],\n    [\n      [\n        5,\n        198\n      ],\n      [\n        5,\n        235\n      ]\n    ]\n  ]\n}\n{\n  "name": "BookReserved",\n  "displayName": "도서 예약됨",\n  "actor": "Member",\n  "level": 5,\n  "description": "회원이 대출 중인 도서에 대해 예약을 신청함. 예약이 완료되면 도서 상태가 \'예약중\'으로 변경됨.",\n  "inputs": [\n    "회원번호",\n    "도서 식별자"\n  ],\n  "outputs": [\n    "예약 정보",\n    "도서 상태: 예약중"\n  ],\n  "nextEvents": [\n    "BookStatusChanged",\n    "ReservationHistoryRecorded"\n  ],\n  "refs": [\n    [\n      [\n        5,\n        183\n      ],\n      [\n        5,\n        193\n      ]\n    ],\n    [\n      [\n        7,\n        167\n      ],\n      [\n        7,\n        175\n      ]\n    ]\n  ]\n}\n{\n  "name": "BookReturned",\n  "displayName": "도서 반납됨",\n  "actor": "Member",\n  "level": 6,\n  "description": "회원이 대출한 도서를 반납함. 반납 시 도서 상태가 \'대출가능\'으로 변경되고, 예약자가 있을 경우 \'예약중\'으로 변경됨.",\n  "inputs": [\n    "회원번호",\n    "도서 식별자"\n  ],\n  "outputs": [\n    "도서 상태: 대출가능 또는 예약중",\n    "반납 처리 정보"\n  ],\n  "nextEvents": [\n    "BookStatusChanged",\n    "LoanHistoryRecorded"\n  ],\n  "refs": [\n    [\n      [\n        7,\n        133\n      ],\n      [\n        7,\n        167\n      ]\n    ],\n    [\n      [\n        7,\n        167\n      ],\n      [\n        7,\n        175\n      ]\n    ]\n  ]\n}\n{\n  "name": "LoanExtended",\n  "displayName": "대출 연장됨",\n  "actor": "Member",\n  "level": 7,\n  "description": "회원이 대출 중인 도서의 대출 기간을 연장함. 연장 후 대출 정보와 반납 예정일이 갱신됨.",\n  "inputs": [\n    "회원번호",\n    "도서 식별자",\n    "연장 기간"\n  ],\n  "outputs": [\n    "갱신된 대출 정보",\n    "새 반납 예정일"\n  ],\n  "nextEvents": [\n    "LoanHistoryRecorded"\n  ],\n  "refs": [\n    [\n      [\n        7,\n        109\n      ],\n      [\n        7,\n        124\n      ]\n    ]\n  ]\n}', 'eventNames': 'BookLoaned, BookReserved, BookReturned, LoanExtended 이벤트가 발생할 수 있어.', 'userStory': "대출/반납을 통합적으로 관리하는\n대출/반납' 화면에서는 회원이 도서를 대출하고 반납하는 것을 관리할 수 있어야 해. 대출 신청 시에는 회원번호와 이름으로 회원을 확인하고, 대출할\n예약\n대출 현황 화면에서는 현재 대출 중인 도서들의 목록을 볼 수 있어야 해. 각 대출 건에 대해 대출일, 반납\n연장\n대출 이력과 상태"}}}, relations={}),
    "actions": [
        ActionModel(
            objectType= "Aggregate",
            type= "create",
            ids= {
                "boundedContextId": "a35f39e7-6201-441e-9b5b-931aeba36079",
                "aggregateId": "6a58ccad-7551-445d-a4ba-3f2128d26bd4"
            },
            args= {
                "aggregateName": "Loan",
                "aggregateAlias": "대출",
                "properties": [
                    {
                        "name": "loanId",
                        "type": "Integer",
                        "isKey": True,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    32,
                                    5
                                ],
                                [
                                    32,
                                    42
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "memberId",
                        "type": "String",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    33,
                                    5
                                ],
                                [
                                    33,
                                    34
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "bookId",
                        "type": "Integer",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    34,
                                    5
                                ],
                                [
                                    34,
                                    24
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "loanDate",
                        "type": "Date",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    35,
                                    5
                                ],
                                [
                                    35,
                                    48
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "dueDate",
                        "type": "Date",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    36,
                                    5
                                ],
                                [
                                    36,
                                    30
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "returnDate",
                        "type": "Date",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    37,
                                    5
                                ],
                                [
                                    37,
                                    29
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "loanPeriodDays",
                        "type": "Integer",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    38,
                                    5
                                ],
                                [
                                    38,
                                    39
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "status",
                        "type": "LoanStatus",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    39,
                                    5
                                ],
                                [
                                    39,
                                    50
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "extensionCount",
                        "type": "Integer",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    40,
                                    5
                                ],
                                [
                                    40,
                                    31
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "createdAt",
                        "type": "Date",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    41,
                                    5
                                ],
                                [
                                    41,
                                    31
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "updatedAt",
                        "type": "Date",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    42,
                                    5
                                ],
                                [
                                    42,
                                    31
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "historyId",
                        "type": "Integer",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    72,
                                    5
                                ],
                                [
                                    72,
                                    45
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "actionType",
                        "type": "LoanActionType",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    74,
                                    5
                                ],
                                [
                                    74,
                                    63
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "actionDate",
                        "type": "Date",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    75,
                                    5
                                ],
                                [
                                    75,
                                    32
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "previousDueDate",
                        "type": "Date",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    76,
                                    5
                                ],
                                [
                                    76,
                                    35
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "newDueDate",
                        "type": "Date",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    77,
                                    5
                                ],
                                [
                                    77,
                                    30
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "notes",
                        "type": "String",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    78,
                                    5
                                ],
                                [
                                    78,
                                    14
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "processedBy",
                        "type": "String",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    79,
                                    5
                                ],
                                [
                                    79,
                                    29
                                ]
                            ]
                        ]
                    }
                ],
                "refs": [
                    [
                        [
                            31,
                            1
                        ],
                        [
                            49,
                            2
                        ]
                    ]
                ],
                "description": "* Inference(When generating the aggregate)\n주어진 요구사항과 DDL을 분석한 결과, Loan Aggregate는 도서 대출과 관련된 모든 필수 필드를 포함해야 하며, 대출 상태를 나타내는 LoanStatus 열거형을 사용하여 상태 관리가 명확히 이루어지도록 설계한다. 또한, 대출 이력 관련 필드(historyId, actionType, actionDate, previousDueDate, newDueDate, notes, processedBy)를 Loan Aggregate 내에 직접 포함시켜 별도의 Aggregate 생성 없이 요구사항을 충족한다. 모든 필드는 DDL과 이벤트 설명에 근거하여 정확히 매핑되었으며, 상태 필드는 한글 상태명을 영어로 변환하여 열거형 멤버로 정의하였다.\n"
            },
            actionName= "CreateLoanAggregate"
        ),
        ActionModel(
            objectType= "Enumeration",
            type= "create",
            ids= {
                "boundedContextId": "a35f39e7-6201-441e-9b5b-931aeba36079",
                "aggregateId": "6a58ccad-7551-445d-a4ba-3f2128d26bd4",
                "enumerationId": "10469fdf-3cbb-452b-92c9-add711dd259f"
            },
            args= {
                "enumerationName": "LoanStatus",
                "enumerationAlias": "대출 상태",
                "properties": [
                    {
                        "name": "ON_LOAN",
                        "refs": [
                            [
                                [
                                    39,
                                    18
                                ],
                                [
                                    39,
                                    20
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "OVERDUE",
                        "refs": [
                            [
                                [
                                    39,
                                    25
                                ],
                                [
                                    39,
                                    26
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "RETURNED",
                        "refs": [
                            [
                                [
                                    39,
                                    31
                                ],
                                [
                                    39,
                                    34
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "EXTENDED",
                        "refs": [
                            [
                                [
                                    39,
                                    39
                                ],
                                [
                                    39,
                                    40
                                ]
                            ]
                        ]
                    }
                ],
                "refs": [
                    [
                        [
                            39,
                            5
                        ],
                        [
                            39,
                            50
                        ]
                    ]
                ]
            },
            actionName= "CreateLoanStatusEnum"
        ),
        ActionModel(
            objectType= "Enumeration",
            type= "create",
            ids= {
                "boundedContextId": "a35f39e7-6201-441e-9b5b-931aeba36079",
                "aggregateId": "6a58ccad-7551-445d-a4ba-3f2128d26bd4",
                "enumerationId": "3b8e440f-cabe-453c-a256-2e71c39201f5"
            },
            args= {
                "enumerationName": "LoanActionType",
                "enumerationAlias": "대출 이력 액션 타입",
                "properties": [
                    {
                        "name": "LOAN",
                        "refs": [
                            [
                                [
                                    74,
                                    23
                                ],
                                [
                                    74,
                                    24
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "RETURN",
                        "refs": [
                            [
                                [
                                    74,
                                    29
                                ],
                                [
                                    74,
                                    30
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "EXTENSION",
                        "refs": [
                            [
                                [
                                    74,
                                    35
                                ],
                                [
                                    74,
                                    36
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "OVERDUE_NOTICE",
                        "refs": [
                            [
                                [
                                    74,
                                    41
                                ],
                                [
                                    74,
                                    44
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "LOSS_REPORT",
                        "refs": [
                            [
                                [
                                    74,
                                    49
                                ],
                                [
                                    74,
                                    52
                                ]
                            ]
                        ]
                    }
                ],
                "refs": [
                    [
                        [
                            74,
                            5
                        ],
                        [
                            74,
                            63
                        ]
                    ]
                ]
            },
            actionName= "CreateLoanActionTypeEnum"
        ),
        ActionModel(
            objectType= "Aggregate",
            type= "create",
            ids= {
                "boundedContextId": "a35f39e7-6201-441e-9b5b-931aeba36079",
                "aggregateId": "deee744d-983e-47f5-be6b-16b72fa1b300"
            },
            args= {
                "aggregateName": "Reservation",
                "aggregateAlias": "예약",
                "properties": [
                    {
                        "name": "reservationId",
                        "type": "Integer",
                        "isKey": True,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    53,
                                    5
                                ],
                                [
                                    53,
                                    49
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "memberId",
                        "type": "String",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    54,
                                    5
                                ],
                                [
                                    54,
                                    34
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "bookId",
                        "type": "Integer",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    55,
                                    5
                                ],
                                [
                                    55,
                                    24
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "reservationDate",
                        "type": "Date",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    56,
                                    5
                                ],
                                [
                                    56,
                                    55
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "status",
                        "type": "ReservationStatus",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    57,
                                    5
                                ],
                                [
                                    57,
                                    60
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "notificationSent",
                        "type": "Boolean",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    58,
                                    5
                                ],
                                [
                                    58,
                                    43
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "expiryDate",
                        "type": "Date",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    59,
                                    5
                                ],
                                [
                                    59,
                                    29
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "createdAt",
                        "type": "Date",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    60,
                                    5
                                ],
                                [
                                    60,
                                    49
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "updatedAt",
                        "type": "Date",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    61,
                                    5
                                ],
                                [
                                    61,
                                    77
                                ]
                            ]
                        ]
                    }
                ],
                "refs": [
                    [
                        [
                            52,
                            2
                        ],
                        [
                            68,
                            2
                        ]
                    ]
                ],
                "description": "* Inference(When generating the aggregate)\nReservation Aggregate는 회원의 도서 예약 정보를 관리하는 핵심 도메인 객체입니다. DDL과 요구사항에 따라 예약 ID, 회원 ID, 도서 ID, 예약일, 상태, 알림 발송 여부, 만료일, 생성 및 수정 일자를 포함하여 예약 관련 모든 필드를 포함합니다. ReservationStatus 열거형은 예약 상태를 명확히 표현하며, 예약 상태의 다양한 값을 영어로 변환하여 사용합니다. 모든 필드는 Reservation Aggregate 내에 포함되어 있으며, 별도의 ValueObject는 필요하지 않아 단순하고 명확한 모델을 유지합니다.\n"
            },
            actionName= "CreateReservationAggregate"
        ),
        ActionModel(
            objectType= "Enumeration",
            type= "create",
            ids= {
                "boundedContextId": "a35f39e7-6201-441e-9b5b-931aeba36079",
                "aggregateId": "deee744d-983e-47f5-be6b-16b72fa1b300",
                "enumerationId": "68bae2d0-8e22-4741-91fa-9587c1f5065b"
            },
            args= {
                "enumerationName": "ReservationStatus",
                "enumerationAlias": "예약 상태",
                "properties": [
                    {
                        "name": "RESERVATION_PENDING",
                        "refs": [
                            [
                                [
                                    57,
                                    17
                                ],
                                [
                                    57,
                                    54
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "RESERVATION_COMPLETED",
                        "refs": [
                            [
                                [
                                    57,
                                    24
                                ],
                                [
                                    57,
                                    54
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "RESERVATION_CANCELLED",
                        "refs": [
                            [
                                [
                                    57,
                                    32
                                ],
                                [
                                    57,
                                    54
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "RESERVATION_EXPIRED",
                        "refs": [
                            [
                                [
                                    57,
                                    40
                                ],
                                [
                                    57,
                                    54
                                ]
                            ]
                        ]
                    }
                ],
                "refs": [
                    [
                        [
                            57,
                            5
                        ],
                        [
                            57,
                            60
                        ]
                    ]
                ]
            },
            actionName= "CreateReservationStatusEnum"
        ),
        ActionModel(
            objectType= "Aggregate",
            type= "create",
            ids= {
                "boundedContextId": "a0f580e4-fc10-4d02-8a63-a81e7811e821",
                "aggregateId": "a08b8110-d0b9-434f-b93a-744108e91bf6"
            },
            args= {
                "aggregateName": "Book",
                "aggregateAlias": "도서",
                "properties": [
                    {
                        "name": "bookId",
                        "type": "Integer",
                        "isKey": True,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    24,
                                    5
                                ],
                                [
                                    24,
                                    42
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "title",
                        "type": "String",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    15,
                                    66
                                ],
                                [
                                    15,
                                    74
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "isbn",
                        "type": "String",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    15,
                                    8
                                ],
                                [
                                    26,
                                    37
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "author",
                        "type": "String",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    15,
                                    10
                                ],
                                [
                                    27,
                                    33
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "publisher",
                        "type": "String",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    15,
                                    13
                                ],
                                [
                                    28,
                                    36
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "category",
                        "type": "BookCategory",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    15,
                                    12
                                ],
                                [
                                    29,
                                    52
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "status",
                        "type": "BookStatus",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    15,
                                    10
                                ],
                                [
                                    30,
                                    59
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "registrationDate",
                        "type": "Date",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    31,
                                    5
                                ],
                                [
                                    31,
                                    38
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "disposalDate",
                        "type": "Date",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    32,
                                    5
                                ],
                                [
                                    32,
                                    31
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "disposalReason",
                        "type": "String",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    33,
                                    5
                                ],
                                [
                                    33,
                                    29
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "createdAt",
                        "type": "Date",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    34,
                                    5
                                ],
                                [
                                    34,
                                    31
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "updatedAt",
                        "type": "Date",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    35,
                                    5
                                ],
                                [
                                    35,
                                    31
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "historyId",
                        "type": "Integer",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    45,
                                    5
                                ],
                                [
                                    45,
                                    45
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "previousStatus",
                        "type": "BookStatus",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    47,
                                    5
                                ],
                                [
                                    47,
                                    24
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "newStatus",
                        "type": "BookStatus",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    48,
                                    5
                                ],
                                [
                                    48,
                                    56
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "changeReason",
                        "type": "String",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    49,
                                    5
                                ],
                                [
                                    49,
                                    25
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "changedBy",
                        "type": "String",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    50,
                                    5
                                ],
                                [
                                    50,
                                    22
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "changeDate",
                        "type": "Date",
                        "isKey": None,
                        "isForeignProperty": None,
                        "refs": [
                            [
                                [
                                    51,
                                    5
                                ],
                                [
                                    51,
                                    32
                                ]
                            ]
                        ]
                    }
                ],
                "refs": [
                    [
                        [
                            4,
                            1
                        ],
                        [
                            4,
                            12
                        ]
                    ]
                ],
                "description": "* Inference(When generating the aggregate)\nBookManagement 도메인은 도서의 등록, 상태 관리, 폐기 처리 및 상태 변경 이력 관리를 포함합니다. Book Aggregate는 도서의 핵심 속성을 포함하며, BookStatus와 BookCategory 두 개의 Enumeration을 통해 도서 상태와 카테고리를 명확히 구분합니다. 도서 상태 변경 이력 관련 필드(historyId, previousStatus, newStatus, changeReason, changedBy, changeDate)는 도서 상태 변경 이력 관리가 Book Aggregate 내에서 관리되도록 포함시켰습니다. 모든 필드는 DDL과 요구사항에 따라 적절히 매핑되었으며, 도서 상태 및 카테고리 필드는 Enumeration으로 처리하여 도메인 규칙을 엄격히 반영했습니다.\n"
            },
            actionName= "CreateBookAggregate"
        ),
        ActionModel(
            objectType= "Enumeration",
            type= "create",
            ids= {
                "boundedContextId": "a0f580e4-fc10-4d02-8a63-a81e7811e821",
                "aggregateId": "a08b8110-d0b9-434f-b93a-744108e91bf6",
                "enumerationId": "e337e326-e737-40a8-8a8a-248f539c35f5"
            },
            args= {
                "enumerationName": "BookStatus",
                "enumerationAlias": "도서 상태",
                "properties": [
                    {
                        "name": "AVAILABLE",
                        "refs": [
                            [
                                [
                                    15,
                                    10
                                ],
                                [
                                    30,
                                    59
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "ON_LOAN",
                        "refs": [
                            [
                                [
                                    15,
                                    10
                                ],
                                [
                                    30,
                                    59
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "RESERVED",
                        "refs": [
                            [
                                [
                                    15,
                                    10
                                ],
                                [
                                    30,
                                    59
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "DISPOSED",
                        "refs": [
                            [
                                [
                                    15,
                                    10
                                ],
                                [
                                    30,
                                    59
                                ]
                            ]
                        ]
                    }
                ],
                "refs": [
                    [
                        [
                            15,
                            10
                        ],
                        [
                            30,
                            59
                        ]
                    ]
                ]
            },
            actionName= "CreateBookStatusEnum"
        ),
        ActionModel(
            objectType= "Enumeration",
            type= "create",
            ids= {
                "boundedContextId": "a0f580e4-fc10-4d02-8a63-a81e7811e821",
                "aggregateId": "a08b8110-d0b9-434f-b93a-744108e91bf6",
                "enumerationId": "37fec9a5-6c67-49dc-bb4c-2306c45b48b9"
            },
            args= {
                "enumerationName": "BookCategory",
                "enumerationAlias": "도서 카테고리",
                "properties": [
                    {
                        "name": "FICTION",
                        "refs": [
                            [
                                [
                                    15,
                                    12
                                ],
                                [
                                    29,
                                    52
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "NON_FICTION",
                        "refs": [
                            [
                                [
                                    15,
                                    12
                                ],
                                [
                                    29,
                                    52
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "ACADEMIC",
                        "refs": [
                            [
                                [
                                    15,
                                    12
                                ],
                                [
                                    29,
                                    52
                                ]
                            ]
                        ]
                    },
                    {
                        "name": "MAGAZINE",
                        "refs": [
                            [
                                [
                                    15,
                                    12
                                ],
                                [
                                    29,
                                    52
                                ]
                            ]
                        ]
                    }
                ],
                "refs": [
                    [
                        [
                            15,
                            12
                        ],
                        [
                            29,
                            52
                        ]
                    ]
                ]
            },
            actionName= "CreateBookCategoryEnum"
        )
    ]
}