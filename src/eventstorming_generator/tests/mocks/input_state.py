from ...graph import State
from ...models import InputsModel, UserInfoModel, InformationModel

input_state = State(
    inputs=InputsModel(
        selectedDraftOptions={
          "BookManagement": {
            "boundedContext": {
              "aggregates": [
                {
                  "alias": "도서",
                  "name": "Book"
                }
              ],
              "alias": "도서 관리",
              "description": "# Bounded Context Overview: BookManagement (도서 관리)\n\n## Role\n도서 관리에서는 새로운 도서의 등록, 상태 관리(대출가능, 대출중, 예약중, 폐기), ISBN 중복 및 형식 검증, 도서 정보 갱신, 폐기 및 도서 상태 변경 이력 관리를 수행한다. 도서별 상태 및 변동 내역을 추적하며, 대출/반납/예약 등 도서 상태 변화 이벤트를 수신하거나 발행한다.\n\n## Key Events\n- BookRegistered\n- BookDiscarded\n- BookStateChanged\n- BookStatusHistoryUpdated\n\n# Requirements\n\n## userStory\n\n'도서 관리' 화면에서는 새로운 도서를 등록하고 현재 보유한 도서들의 상태를 관리할 수 있어야 해. 도서 등록 시에는 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받아야 해. ISBN은 13자리 숫자여야 하고 중복 확인이 필요해. 카테고리는 소설/비소설/학술/잡지 중에서 선택할 수 있어야 해. 등록된 도서는 처음에 '대출가능' 상태가 되고, 이후 대출/반납 상황에 따라 '대출중', '예약중' 상태로 자동으로 변경되어야 해. 도서가 훼손되거나 분실된 경우 '폐기' 처리가 가능해야 하며, 폐기된 도서는 더 이상 대출이 불가능해야 해.\n\n각 도서별로 대출 이력과 상태 변경 이력을 조회할 수 있어야 하고, 이를 통해 도서의 대출 현황과 상태 변화를 추적할 수 있어야 해.\n\n## Event\n\n```json\n{\n  \"name\": \"BookRegistered\",\n  \"displayName\": \"도서가 등록됨\",\n  \"actor\": \"사서\",\n  \"level\": 1,\n  \"description\": \"사서가 도서 정보를 입력하여 새로운 도서를 등록하였음. 이때 ISBN 중복 및 13자리 숫자 형식이 검증됨.\",\n  \"inputs\": [\n    \"도서명\",\n    \"ISBN\",\n    \"저자\",\n    \"출판사\",\n    \"카테고리(소설/비소설/학술/잡지)\",\n    \"ISBN 중복 불가\",\n    \"ISBN 13자리\"\n  ],\n  \"outputs\": [\n    \"도서가 시스템에 등록됨\",\n    \"도서 상태가 '대출가능'으로 설정됨\"\n  ],\n  \"nextEvents\": [\n    \"BookStateChanged\"\n  ]\n}\n```\n\n```json\n{\n  \"name\": \"BookStateChanged\",\n  \"displayName\": \"도서 상태가 변경됨\",\n  \"actor\": \"도서관리시스템\",\n  \"level\": 2,\n  \"description\": \"도서의 대출, 반납, 예약, 폐기 등 상태 변화에 따라 도서 상태가 자동으로 변경됨.\",\n  \"inputs\": [\n    \"대출/반납/예약/폐기 트리거\",\n    \"이전 도서 상태\"\n  ],\n  \"outputs\": [\n    \"도서 상태가 변경됨\"\n  ],\n  \"nextEvents\": []\n}\n```\n\n```json\n{\n  \"name\": \"BookDiscarded\",\n  \"displayName\": \"도서가 폐기됨\",\n  \"actor\": \"사서\",\n  \"level\": 3,\n  \"description\": \"사서가 도서의 훼손 또는 분실을 확인하고 해당 도서를 폐기 처리함.\",\n  \"inputs\": [\n    \"도서 선택\",\n    \"폐기 사유\"\n  ],\n  \"outputs\": [\n    \"도서 상태가 '폐기'로 변경됨\",\n    \"도서 대출 불가\"\n  ],\n  \"nextEvents\": [\n    \"BookStateChanged\"\n  ]\n}\n```\n\n```json\n{\n  \"name\": \"BookStatusHistoryUpdated\",\n  \"displayName\": \"도서 상태 이력이 갱신됨\",\n  \"actor\": \"도서관리시스템\",\n  \"level\": 13,\n  \"description\": \"도서의 상태가 변경될 때마다 상태 변경 이력이 기록됨.\",\n  \"inputs\": [\n    \"도서 상태 변경 이벤트\"\n  ],\n  \"outputs\": [\n    \"상태 이력 저장/추가\"\n  ],\n  \"nextEvents\": []\n}\n```\n\n## DDL\n\n```sql\n-- 도서 테이블\nCREATE TABLE books (\n    book_id INT AUTO_INCREMENT PRIMARY KEY,\n    title VARCHAR(500) NOT NULL,\n    isbn VARCHAR(13) UNIQUE NOT NULL,\n    author VARCHAR(200) NOT NULL,\n    publisher VARCHAR(200) NOT NULL,\n    category ENUM('소설', '비소설', '학술', '잡지') NOT NULL,\n    status ENUM('대출가능', '대출중', '예약중', '폐기') DEFAULT '대출가능',\n    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    disposal_date DATETIME NULL,\n    disposal_reason TEXT NULL,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    INDEX idx_title (title),\n    INDEX idx_isbn (isbn),\n    INDEX idx_status (status),\n    INDEX idx_category (category)\n);\n```\n\n```sql\n-- 도서 상태 변경 이력 테이블\nCREATE TABLE book_status_history (\n    history_id INT AUTO_INCREMENT PRIMARY KEY,\n    book_id INT NOT NULL,\n    previous_status ENUM('대출가능', '대출중', '예약중', '폐기'),\n    new_status ENUM('대출가능', '대출중', '예약중', '폐기') NOT NULL,\n    change_reason VARCHAR(200),\n    changed_by VARCHAR(100),\n    change_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    FOREIGN KEY (book_id) REFERENCES books(book_id),\n    INDEX idx_book_id (book_id),\n    INDEX idx_change_date (change_date)\n);\n```\n\n\n## Context Relations\n\n### BookStateSync\n- **Type**: Pub/Sub\n- **Direction**: receives from 대출/반납 프로세스 (LoanProcess)\n- **Reason**: 대출/반납/예약 등 주요 도서 상태 변경은 프로세스 도메인에서 발생하고, 도서 관리 도메인은 해당 이벤트를 구독하여 도서 상태 일관성을 유지한다.\n- **Interaction Pattern**: 대출/반납 프로세스에서 BookStateChanged 등 이벤트를 발행하면, 도서 관리가 이를 구독하여 도서 상태를 업데이트함.\n\n### LoanStatusBookUpdate\n- **Type**: Pub/Sub\n- **Direction**: sends to 대출/반납 프로세스 (LoanProcess)\n- **Reason**: 대출/반납/예약 등 주요 도서 상태 변경은 프로세스 도메인에서 발생하고, 도서 관리 도메인은 해당 이벤트를 구독하여 도서 상태 일관성을 유지한다.\n- **Interaction Pattern**: 대출/반납 프로세스에서 BookStateChanged 등 이벤트를 발행하면, 도서 관리가 이를 구독하여 도서 상태를 업데이트함.",
              "displayName": "도서 관리",
              "name": "BookManagement",
              "requirements": {
                "ddl": "-- 도서 테이블\nCREATE TABLE books (\n    book_id INT AUTO_INCREMENT PRIMARY KEY,\n    title VARCHAR(500) NOT NULL,\n    isbn VARCHAR(13) UNIQUE NOT NULL,\n    author VARCHAR(200) NOT NULL,\n    publisher VARCHAR(200) NOT NULL,\n    category ENUM('소설', '비소설', '학술', '잡지') NOT NULL,\n    status ENUM('대출가능', '대출중', '예약중', '폐기') DEFAULT '대출가능',\n    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    disposal_date DATETIME NULL,\n    disposal_reason TEXT NULL,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    INDEX idx_title (title),\n    INDEX idx_isbn (isbn),\n    INDEX idx_status (status),\n    INDEX idx_category (category)\n);\n-- 도서 상태 변경 이력 테이블\nCREATE TABLE book_status_history (\n    history_id INT AUTO_INCREMENT PRIMARY KEY,\n    book_id INT NOT NULL,\n    previous_status ENUM('대출가능', '대출중', '예약중', '폐기'),\n    new_status ENUM('대출가능', '대출중', '예약중', '폐기') NOT NULL,\n    change_reason VARCHAR(200),\n    changed_by VARCHAR(100),\n    change_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    FOREIGN KEY (book_id) REFERENCES books(book_id),\n    INDEX idx_book_id (book_id),\n    INDEX idx_change_date (change_date)\n);",
                "ddlFields": [
                  "book_id",
                  "title",
                  "isbn",
                  "author",
                  "publisher",
                  "category",
                  "status",
                  "registration_date",
                  "disposal_date",
                  "disposal_reason",
                  "created_at",
                  "updated_at",
                  "history_id",
                  "previous_status",
                  "new_status",
                  "change_reason",
                  "changed_by",
                  "change_date"
                ],
                "event": "{\"name\":\"BookRegistered\",\"displayName\":\"도서가 등록됨\",\"actor\":\"사서\",\"level\":1,\"description\":\"사서가 도서 정보를 입력하여 새로운 도서를 등록하였음. 이때 ISBN 중복 및 13자리 숫자 형식이 검증됨.\",\"inputs\":[\"도서명\",\"ISBN\",\"저자\",\"출판사\",\"카테고리(소설/비소설/학술/잡지)\",\"ISBN 중복 불가\",\"ISBN 13자리\"],\"outputs\":[\"도서가 시스템에 등록됨\",\"도서 상태가 '대출가능'으로 설정됨\"],\"nextEvents\":[\"BookStateChanged\"]}\n{\"name\":\"BookStateChanged\",\"displayName\":\"도서 상태가 변경됨\",\"actor\":\"도서관리시스템\",\"level\":2,\"description\":\"도서의 대출, 반납, 예약, 폐기 등 상태 변화에 따라 도서 상태가 자동으로 변경됨.\",\"inputs\":[\"대출/반납/예약/폐기 트리거\",\"이전 도서 상태\"],\"outputs\":[\"도서 상태가 변경됨\"],\"nextEvents\":[]}\n{\"name\":\"BookDiscarded\",\"displayName\":\"도서가 폐기됨\",\"actor\":\"사서\",\"level\":3,\"description\":\"사서가 도서의 훼손 또는 분실을 확인하고 해당 도서를 폐기 처리함.\",\"inputs\":[\"도서 선택\",\"폐기 사유\"],\"outputs\":[\"도서 상태가 '폐기'로 변경됨\",\"도서 대출 불가\"],\"nextEvents\":[\"BookStateChanged\"]}\n{\"name\":\"BookStatusHistoryUpdated\",\"displayName\":\"도서 상태 이력이 갱신됨\",\"actor\":\"도서관리시스템\",\"level\":13,\"description\":\"도서의 상태가 변경될 때마다 상태 변경 이력이 기록됨.\",\"inputs\":[\"도서 상태 변경 이벤트\"],\"outputs\":[\"상태 이력 저장/추가\"],\"nextEvents\":[]}",
                "eventNames": "BookRegistered, BookDiscarded, BookStateChanged, BookStatusHistoryUpdated 이벤트가 발생할 수 있어.",
                "userStory": "'도서 관리' 화면에서는 새로운 도서를 등록하고 현재 보유한 도서들의 상태를 관리할 수 있어야 해. 도서 등록 시에는 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받아야 해. ISBN은 13자리 숫자여야 하고 중복 확인이 필요해. 카테고리는 소설/비소설/학술/잡지 중에서 선택할 수 있어야 해. 등록된 도서는 처음에 '대출가능' 상태가 되고, 이후 대출/반납 상황에 따라 '대출중', '예약중' 상태로 자동으로 변경되어야 해. 도서가 훼손되거나 분실된 경우 '폐기' 처리가 가능해야 하며, 폐기된 도서는 더 이상 대출이 불가능해야 해.\n각 도서별로 대출 이력과 상태 변경 이력을 조회할 수 있어야 하고, 이를 통해 도서의 대출 현황과 상태 변화를 추적할 수 있어야 해."
              }
            },
            "cons": {
              "cohesion": "상태 변경 시 Book과 BookStatusHistory 간의 동기화·오케스트레이션 로직이 필요합니다.",
              "complexity": "이력 동기화 등 추가 서비스 계층에서 관리할 논리가 필요합니다.",
              "consistency": "상태 변경과 이력 기록이 별도 트랜잭션으로 처리되어 짧은 기간 일관성이 잠시 깨질 수 있습니다.",
              "coupling": "이력 조회 시 Book과 BookStatusHistory 두 Aggregate를 함께 조회해야 하여 쿼리 복잡성이 증가합니다.",
              "encapsulation": "상태와 이력 사이의 비즈니스 규칙이 Aggregate 경계를 넘어 분산될 수 있습니다.",
              "independence": "도서 삭제 등 특수 상황에서 이력 데이터와의 정합성 관리 추가 로직이 필요합니다.",
              "performance": "상태변경 이벤트 발생 시 두 Aggregate에 대한 트랜잭션 관리 비용이 발생할 수 있습니다."
            },
            "description": "# Bounded Context Overview: BookManagement (도서 관리)\n\n## Role\n도서 관리에서는 새로운 도서의 등록, 상태 관리(대출가능, 대출중, 예약중, 폐기), ISBN 중복 및 형식 검증, 도서 정보 갱신, 폐기 및 도서 상태 변경 이력 관리를 수행한다. 도서별 상태 및 변동 내역을 추적하며, 대출/반납/예약 등 도서 상태 변화 이벤트를 수신하거나 발행한다.\n\n## Key Events\n- BookRegistered\n- BookDiscarded\n- BookStateChanged\n- BookStatusHistoryUpdated\n\n# Requirements\n\n## userStory\n\n'도서 관리' 화면에서는 새로운 도서를 등록하고 현재 보유한 도서들의 상태를 관리할 수 있어야 해. 도서 등록 시에는 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받아야 해. ISBN은 13자리 숫자여야 하고 중복 확인이 필요해. 카테고리는 소설/비소설/학술/잡지 중에서 선택할 수 있어야 해. 등록된 도서는 처음에 '대출가능' 상태가 되고, 이후 대출/반납 상황에 따라 '대출중', '예약중' 상태로 자동으로 변경되어야 해. 도서가 훼손되거나 분실된 경우 '폐기' 처리가 가능해야 하며, 폐기된 도서는 더 이상 대출이 불가능해야 해.\n\n각 도서별로 대출 이력과 상태 변경 이력을 조회할 수 있어야 하고, 이를 통해 도서의 대출 현황과 상태 변화를 추적할 수 있어야 해.\n\n## Event\n\n```json\n{\n  \"name\": \"BookRegistered\",\n  \"displayName\": \"도서가 등록됨\",\n  \"actor\": \"사서\",\n  \"level\": 1,\n  \"description\": \"사서가 도서 정보를 입력하여 새로운 도서를 등록하였음. 이때 ISBN 중복 및 13자리 숫자 형식이 검증됨.\",\n  \"inputs\": [\n    \"도서명\",\n    \"ISBN\",\n    \"저자\",\n    \"출판사\",\n    \"카테고리(소설/비소설/학술/잡지)\",\n    \"ISBN 중복 불가\",\n    \"ISBN 13자리\"\n  ],\n  \"outputs\": [\n    \"도서가 시스템에 등록됨\",\n    \"도서 상태가 '대출가능'으로 설정됨\"\n  ],\n  \"nextEvents\": [\n    \"BookStateChanged\"\n  ]\n}\n```\n\n```json\n{\n  \"name\": \"BookStateChanged\",\n  \"displayName\": \"도서 상태가 변경됨\",\n  \"actor\": \"도서관리시스템\",\n  \"level\": 2,\n  \"description\": \"도서의 대출, 반납, 예약, 폐기 등 상태 변화에 따라 도서 상태가 자동으로 변경됨.\",\n  \"inputs\": [\n    \"대출/반납/예약/폐기 트리거\",\n    \"이전 도서 상태\"\n  ],\n  \"outputs\": [\n    \"도서 상태가 변경됨\"\n  ],\n  \"nextEvents\": []\n}\n```\n\n```json\n{\n  \"name\": \"BookDiscarded\",\n  \"displayName\": \"도서가 폐기됨\",\n  \"actor\": \"사서\",\n  \"level\": 3,\n  \"description\": \"사서가 도서의 훼손 또는 분실을 확인하고 해당 도서를 폐기 처리함.\",\n  \"inputs\": [\n    \"도서 선택\",\n    \"폐기 사유\"\n  ],\n  \"outputs\": [\n    \"도서 상태가 '폐기'로 변경됨\",\n    \"도서 대출 불가\"\n  ],\n  \"nextEvents\": [\n    \"BookStateChanged\"\n  ]\n}\n```\n\n```json\n{\n  \"name\": \"BookStatusHistoryUpdated\",\n  \"displayName\": \"도서 상태 이력이 갱신됨\",\n  \"actor\": \"도서관리시스템\",\n  \"level\": 13,\n  \"description\": \"도서의 상태가 변경될 때마다 상태 변경 이력이 기록됨.\",\n  \"inputs\": [\n    \"도서 상태 변경 이벤트\"\n  ],\n  \"outputs\": [\n    \"상태 이력 저장/추가\"\n  ],\n  \"nextEvents\": []\n}\n```\n\n## DDL\n\n```sql\n-- 도서 테이블\nCREATE TABLE books (\n    book_id INT AUTO_INCREMENT PRIMARY KEY,\n    title VARCHAR(500) NOT NULL,\n    isbn VARCHAR(13) UNIQUE NOT NULL,\n    author VARCHAR(200) NOT NULL,\n    publisher VARCHAR(200) NOT NULL,\n    category ENUM('소설', '비소설', '학술', '잡지') NOT NULL,\n    status ENUM('대출가능', '대출중', '예약중', '폐기') DEFAULT '대출가능',\n    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    disposal_date DATETIME NULL,\n    disposal_reason TEXT NULL,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    INDEX idx_title (title),\n    INDEX idx_isbn (isbn),\n    INDEX idx_status (status),\n    INDEX idx_category (category)\n);\n```\n\n```sql\n-- 도서 상태 변경 이력 테이블\nCREATE TABLE book_status_history (\n    history_id INT AUTO_INCREMENT PRIMARY KEY,\n    book_id INT NOT NULL,\n    previous_status ENUM('대출가능', '대출중', '예약중', '폐기'),\n    new_status ENUM('대출가능', '대출중', '예약중', '폐기') NOT NULL,\n    change_reason VARCHAR(200),\n    changed_by VARCHAR(100),\n    change_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    FOREIGN KEY (book_id) REFERENCES books(book_id),\n    INDEX idx_book_id (book_id),\n    INDEX idx_change_date (change_date)\n);\n```\n\n\n## Context Relations\n\n### BookStateSync\n- **Type**: Pub/Sub\n- **Direction**: receives from 대출/반납 프로세스 (LoanProcess)\n- **Reason**: 대출/반납/예약 등 주요 도서 상태 변경은 프로세스 도메인에서 발생하고, 도서 관리 도메인은 해당 이벤트를 구독하여 도서 상태 일관성을 유지한다.\n- **Interaction Pattern**: 대출/반납 프로세스에서 BookStateChanged 등 이벤트를 발행하면, 도서 관리가 이를 구독하여 도서 상태를 업데이트함.\n\n### LoanStatusBookUpdate\n- **Type**: Pub/Sub\n- **Direction**: sends to 대출/반납 프로세스 (LoanProcess)\n- **Reason**: 대출/반납/예약 등 주요 도서 상태 변경은 프로세스 도메인에서 발생하고, 도서 관리 도메인은 해당 이벤트를 구독하여 도서 상태 일관성을 유지한다.\n- **Interaction Pattern**: 대출/반납 프로세스에서 BookStateChanged 등 이벤트를 발행하면, 도서 관리가 이를 구독하여 도서 상태를 업데이트함.",
            "isAIRecommended": True,
            "pros": {
              "cohesion": "도서 정보와 상태 이력이 각자의 Aggregate로 분리되어 각자의 책임에 집중합니다.",
              "complexity": "각 Aggregate가 단순해져 도메인 설계, 구현, 확장 및 유지보수가 용이합니다.",
              "consistency": "상태 변경, 이력 관리 등 각 기능이 별도 트랜잭션으로 처리되어 이력 저장에 따른 성능 영향이 적습니다.",
              "coupling": "Book과 BookStatusHistory가 ValueObject 참조로 연결되어 느슨한 결합이 유지됩니다.",
              "encapsulation": "상태이력 관리 방식 및 구조 변경이 BookStatusHistory Aggregate 단위로 독립적 변경이 가능합니다.",
              "independence": "도서 관리와 이력 관리를 각각 독립적으로 배포 및 확장할 수 있습니다.",
              "performance": "대규모 이력 데이터에 대한 저장·조회 성능을 별도 Aggregate 차원에서 최적화할 수 있습니다."
            },
            "structure": [
              {
                "aggregate": {
                  "alias": "도서",
                  "name": "Book"
                },
                "enumerations": [
                  {
                    "alias": "도서상태",
                    "name": "BookStatus"
                  },
                  {
                    "alias": "도서카테고리",
                    "name": "BookCategory"
                  }
                ],
                "previewAttributes": [
                  "book_id",
                  "title",
                  "isbn",
                  "author",
                  "publisher",
                  "category",
                  "status",
                  "registration_date",
                  "disposal_date",
                  "disposal_reason",
                  "created_at",
                  "updated_at"
                ],
                "valueObjects": [
                  {
                    "alias": "도서기본정보",
                    "name": "BookInfo"
                  },
                  {
                    "alias": "대출참조",
                    "name": "LoanReference",
                    "referencedAggregate": {
                      "alias": "대출",
                      "name": "Loan"
                    }
                  },
                  {
                    "alias": "예약참조",
                    "name": "ReservationReference",
                    "referencedAggregate": {
                      "alias": "예약",
                      "name": "Reservation"
                    }
                  }
                ]
              },
              {
                "aggregate": {
                  "alias": "도서상태이력",
                  "name": "BookStatusHistory"
                },
                "enumerations": [
                  {
                    "alias": "도서상태",
                    "name": "BookStatus"
                  }
                ],
                "previewAttributes": [
                  "history_id",
                  "book_id",
                  "previous_status",
                  "new_status",
                  "change_reason",
                  "changed_by",
                  "change_date"
                ],
                "valueObjects": [
                  {
                    "alias": "상태변경이력항목",
                    "name": "BookStatusHistoryItem"
                  },
                  {
                    "alias": "도서참조",
                    "name": "BookReference",
                    "referencedAggregate": {
                      "alias": "도서",
                      "name": "Book"
                    }
                  }
                ]
              }
            ]
          },
          "LoanProcess": {
            "boundedContext": {
              "aggregates": [
                {
                  "alias": "대출",
                  "name": "Loan"
                },
                {
                  "alias": "예약",
                  "name": "Reservation"
                }
              ],
              "alias": "대출/반납 프로세스",
              "description": "# Bounded Context Overview: LoanProcess (대출/반납 프로세스)\n\n## Role\n대출/반납 프로세스에서는 회원 인증, 도서 대출/반납/연장, 도서 예약, 대출 상태(대출중, 연체, 반납완료) 변경, 대출 이력 갱신, 예약 활성화 및 알림 트리거 역할을 담당한다. 프로세스의 흐름에 따라 도서 상태 변경 이벤트를 발생시키거나 구독한다.\n\n## Key Events\n- LoanRequested\n- LoanRejected\n- LoanApproved\n- ReservationRequested\n- LoanExtended\n- LoanReturned\n- LoanOverdue\n- ReservationActivated\n- LoanHistoryUpdated\n\n# Requirements\n\n## userStory\n\n'대출/반납' 화면에서는 회원이 도서를 대출하고 반납하는 것을 관리할 수 있어야 해. 대출 신청 시에는 회원번호와 이름으로 회원을 확인하고, 대출할 도서를 선택해야 해. 도서는 도서명이나 ISBN으로 검색할 수 있어야 해. 대출 기간은 7일/14일/30일 중에서 선택할 수 있어. 만약 대출하려는 도서가 이미 대출 중이라면, 예약 신청이 가능해야 해. 대출이 완료되면 해당 도서의 상태는 자동으로 '대출중'으로 변경되어야 해.\n\n대출 현황 화면에서는 현재 대출 중인 도서들의 목록을 볼 수 있어야 해. 각 대출 건에 대해 대출일, 반납예정일, 현재 상태(대출중/연체/반납완료)를 확인할 수 있어야 하고, 대출 중인 도서는 연장이나 반납 처리가 가능해야 해. 도서가 반납되면 자동으로 해당 도서의 상태가 '대출가능'으로 변경되어야 해. 만약 예약자가 있는 도서가 반납되면, 해당 도서는 '예약중' 상태로 변경되어야 해.\n\n각 도서별로 대출 이력과 상태 변경 이력을 조회할 수 있어야 하고, 이를 통해 도서의 대출 현황과 상태 변화를 추적할 수 있어야 해.\n\n## Event\n\n```json\n{\n  \"name\": \"LoanRequested\",\n  \"displayName\": \"대출이 신청됨\",\n  \"actor\": \"회원\",\n  \"level\": 4,\n  \"description\": \"회원이 도서 대출을 신청하고 대출 기간(7/14/30일)을 선택함. 회원번호와 이름으로 회원 인증이 선행됨.\",\n  \"inputs\": [\n    \"회원번호\",\n    \"이름\",\n    \"대출 도서\",\n    \"대출 기간\",\n    \"도서 상태=대출가능\"\n  ],\n  \"outputs\": [\n    \"대출 요청 생성\"\n  ],\n  \"nextEvents\": [\n    \"LoanApproved\",\n    \"LoanRejected\"\n  ]\n}\n```\n\n```json\n{\n  \"name\": \"LoanRejected\",\n  \"displayName\": \"대출이 거절됨\",\n  \"actor\": \"도서관리시스템\",\n  \"level\": 5,\n  \"description\": \"대출 신청 시 도서가 이미 대출 중이거나 폐기 상태일 경우 대출이 거절됨.\",\n  \"inputs\": [\n    \"대출 도서 상태=대출중/폐기\"\n  ],\n  \"outputs\": [\n    \"대출 요청 거절 안내\"\n  ],\n  \"nextEvents\": [\n    \"ReservationRequested\"\n  ]\n}\n```\n\n```json\n{\n  \"name\": \"LoanApproved\",\n  \"displayName\": \"대출이 승인됨\",\n  \"actor\": \"도서관리시스템\",\n  \"level\": 6,\n  \"description\": \"도서가 대출가능 상태여서 대출이 승인되고, 도서 상태가 '대출중'으로 변경됨.\",\n  \"inputs\": [\n    \"대출 요청\",\n    \"도서 상태=대출가능\"\n  ],\n  \"outputs\": [\n    \"대출 정보 생성\",\n    \"도서 상태 '대출중'\"\n  ],\n  \"nextEvents\": [\n    \"BookStateChanged\"\n  ]\n}\n```\n\n```json\n{\n  \"name\": \"ReservationRequested\",\n  \"displayName\": \"예약이 신청됨\",\n  \"actor\": \"회원\",\n  \"level\": 7,\n  \"description\": \"회원이 대출 중인 도서에 대해 예약을 신청함.\",\n  \"inputs\": [\n    \"회원번호\",\n    \"도서\",\n    \"도서 상태=대출중\"\n  ],\n  \"outputs\": [\n    \"예약 정보 생성\"\n  ],\n  \"nextEvents\": [\n    \"BookStateChanged\"\n  ]\n}\n```\n\n```json\n{\n  \"name\": \"LoanExtended\",\n  \"displayName\": \"대출이 연장됨\",\n  \"actor\": \"회원\",\n  \"level\": 8,\n  \"description\": \"회원이 대출 중인 도서에 대해 대출 연장을 요청하여 연장됨.\",\n  \"inputs\": [\n    \"회원번호\",\n    \"대출 정보\",\n    \"연장 조건 만족\"\n  ],\n  \"outputs\": [\n    \"반납예정일 변경\"\n  ],\n  \"nextEvents\": []\n}\n```\n\n```json\n{\n  \"name\": \"LoanReturned\",\n  \"displayName\": \"도서가 반납됨\",\n  \"actor\": \"회원\",\n  \"level\": 9,\n  \"description\": \"회원이 대출 중이던 도서를 반납함.\",\n  \"inputs\": [\n    \"회원번호\",\n    \"대출 정보\",\n    \"반납 처리\"\n  ],\n  \"outputs\": [\n    \"도서 상태 변경\",\n    \"대출 상태 변경(반납완료)\"\n  ],\n  \"nextEvents\": [\n    \"BookStateChanged\",\n    \"ReservationActivated\"\n  ]\n}\n```\n\n```json\n{\n  \"name\": \"LoanOverdue\",\n  \"displayName\": \"대출이 연체됨\",\n  \"actor\": \"도서관리시스템\",\n  \"level\": 10,\n  \"description\": \"반납예정일이 지나도록 반납되지 않은 대출건이 연체 상태로 변경됨.\",\n  \"inputs\": [\n    \"현재일자\",\n    \"반납예정일\",\n    \"미반납\"\n  ],\n  \"outputs\": [\n    \"대출 상태가 '연체'로 변경됨\"\n  ],\n  \"nextEvents\": []\n}\n```\n\n```json\n{\n  \"name\": \"ReservationActivated\",\n  \"displayName\": \"예약이 활성화됨\",\n  \"actor\": \"도서관리시스템\",\n  \"level\": 11,\n  \"description\": \"예약자가 존재하는 도서가 반납되면 도서 상태가 '예약중'으로 변경되고 예약자가 알림을 받음.\",\n  \"inputs\": [\n    \"도서 반납\",\n    \"예약 존재\"\n  ],\n  \"outputs\": [\n    \"도서 상태 '예약중'\",\n    \"예약자 알림\"\n  ],\n  \"nextEvents\": [\n    \"BookStateChanged\"\n  ]\n}\n```\n\n```json\n{\n  \"name\": \"LoanHistoryUpdated\",\n  \"displayName\": \"대출 이력이 갱신됨\",\n  \"actor\": \"도서관리시스템\",\n  \"level\": 12,\n  \"description\": \"모든 대출/반납/연장/연체 등 대출 관련 상태 변화 시 대출 이력이 갱신됨.\",\n  \"inputs\": [\n    \"대출/반납/연장/연체 이벤트\"\n  ],\n  \"outputs\": [\n    \"대출 이력 저장/추가\"\n  ],\n  \"nextEvents\": []\n}\n```\n\n## DDL\n\n```sql\n-- 대출 테이블\nCREATE TABLE loans (\n    loan_id INT AUTO_INCREMENT PRIMARY KEY,\n    member_id VARCHAR(20) NOT NULL,\n    book_id INT NOT NULL,\n    loan_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    due_date DATETIME NOT NULL,\n    return_date DATETIME NULL,\n    loan_period_days INT NOT NULL CHECK (loan_period_days IN (7, 14, 30)),\n    status ENUM('대출중', '연체', '반납완료', '연장') DEFAULT '대출중',\n    extension_count INT DEFAULT 0,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    FOREIGN KEY (member_id) REFERENCES members(member_id),\n    FOREIGN KEY (book_id) REFERENCES books(book_id),\n    INDEX idx_member_id (member_id),\n    INDEX idx_book_id (book_id),\n    INDEX idx_status (status),\n    INDEX idx_due_date (due_date)\n);\n```\n\n```sql\n-- 예약 테이블\nCREATE TABLE reservations (\n    reservation_id INT AUTO_INCREMENT PRIMARY KEY,\n    member_id VARCHAR(20) NOT NULL,\n    book_id INT NOT NULL,\n    reservation_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    status ENUM('예약중', '예약완료', '예약취소', '예약만료') DEFAULT '예약중',\n    notification_sent BOOLEAN DEFAULT FALSE,\n    expiry_date DATETIME NULL,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    FOREIGN KEY (member_id) REFERENCES members(member_id),\n    FOREIGN KEY (book_id) REFERENCES books(book_id),\n    INDEX idx_member_id (member_id),\n    INDEX idx_book_id (book_id),\n    INDEX idx_status (status),\n    INDEX idx_reservation_date (reservation_date)\n);\n```\n\n```sql\n-- 대출 이력 테이블 (모든 대출 활동의 상세 로그)\nCREATE TABLE loan_history (\n    history_id INT AUTO_INCREMENT PRIMARY KEY,\n    loan_id INT NOT NULL,\n    action_type ENUM('대출', '반납', '연장', '연체알림', '분실신고') NOT NULL,\n    action_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    previous_due_date DATETIME NULL,\n    new_due_date DATETIME NULL,\n    notes TEXT,\n    processed_by VARCHAR(100),\n    FOREIGN KEY (loan_id) REFERENCES loans(loan_id),\n    INDEX idx_loan_id (loan_id),\n    INDEX idx_action_type (action_type),\n    INDEX idx_action_date (action_date)\n);\n```\n\n```sql\n-- 연체 관리 테이블\nCREATE TABLE overdue_records (\n    overdue_id INT AUTO_INCREMENT PRIMARY KEY,\n    loan_id INT NOT NULL,\n    overdue_days INT NOT NULL,\n    fine_amount DECIMAL(10,2) DEFAULT 0.00,\n    fine_paid BOOLEAN DEFAULT FALSE,\n    notification_count INT DEFAULT 0,\n    last_notification_date DATETIME NULL,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    FOREIGN KEY (loan_id) REFERENCES loans(loan_id),\n    INDEX idx_loan_id (loan_id),\n    INDEX idx_overdue_days (overdue_days)\n);\n```\n\n\n## Context Relations\n\n### BookStateSync\n- **Type**: Pub/Sub\n- **Direction**: sends to 도서 관리 (BookManagement)\n- **Reason**: 대출/반납/예약 등 주요 도서 상태 변경은 프로세스 도메인에서 발생하고, 도서 관리 도메인은 해당 이벤트를 구독하여 도서 상태 일관성을 유지한다.\n- **Interaction Pattern**: 대출/반납 프로세스에서 BookStateChanged 등 이벤트를 발행하면, 도서 관리가 이를 구독하여 도서 상태를 업데이트함.\n\n### LoanStatusBookUpdate\n- **Type**: Pub/Sub\n- **Direction**: receives from 도서 관리 (BookManagement)\n- **Reason**: 대출/반납/예약 등 주요 도서 상태 변경은 프로세스 도메인에서 발생하고, 도서 관리 도메인은 해당 이벤트를 구독하여 도서 상태 일관성을 유지한다.\n- **Interaction Pattern**: 대출/반납 프로세스에서 BookStateChanged 등 이벤트를 발행하면, 도서 관리가 이를 구독하여 도서 상태를 업데이트함.\n\n### ReservationNotificationIntegration\n- **Type**: Request/Response\n- **Direction**: sends to 예약 & 알림 서비스 (reservation-notification)\n- **Reason**: 알림 서비스는 사전 구축된 PBC를 활용하며, 예약 활성화 시점에만 직접적으로 호출되기 때문에 Request/Response가 적합하다.\n- **Interaction Pattern**: 예약 활성화 이벤트 발생 시 대출/반납 프로세스가 예약 & 알림 서비스 PBC를 호출하여 알림을 전송함.",
              "displayName": "대출/반납 프로세스",
              "name": "LoanProcess",
              "requirements": {
                "ddl": "-- 대출 테이블\nCREATE TABLE loans (\n    loan_id INT AUTO_INCREMENT PRIMARY KEY,\n    member_id VARCHAR(20) NOT NULL,\n    book_id INT NOT NULL,\n    loan_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    due_date DATETIME NOT NULL,\n    return_date DATETIME NULL,\n    loan_period_days INT NOT NULL CHECK (loan_period_days IN (7, 14, 30)),\n    status ENUM('대출중', '연체', '반납완료', '연장') DEFAULT '대출중',\n    extension_count INT DEFAULT 0,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    FOREIGN KEY (member_id) REFERENCES members(member_id),\n    FOREIGN KEY (book_id) REFERENCES books(book_id),\n    INDEX idx_member_id (member_id),\n    INDEX idx_book_id (book_id),\n    INDEX idx_status (status),\n    INDEX idx_due_date (due_date)\n);\n-- 예약 테이블\nCREATE TABLE reservations (\n    reservation_id INT AUTO_INCREMENT PRIMARY KEY,\n    member_id VARCHAR(20) NOT NULL,\n    book_id INT NOT NULL,\n    reservation_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    status ENUM('예약중', '예약완료', '예약취소', '예약만료') DEFAULT '예약중',\n    notification_sent BOOLEAN DEFAULT FALSE,\n    expiry_date DATETIME NULL,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    FOREIGN KEY (member_id) REFERENCES members(member_id),\n    FOREIGN KEY (book_id) REFERENCES books(book_id),\n    INDEX idx_member_id (member_id),\n    INDEX idx_book_id (book_id),\n    INDEX idx_status (status),\n    INDEX idx_reservation_date (reservation_date)\n);\n-- 대출 이력 테이블 (모든 대출 활동의 상세 로그)\nCREATE TABLE loan_history (\n    history_id INT AUTO_INCREMENT PRIMARY KEY,\n    loan_id INT NOT NULL,\n    action_type ENUM('대출', '반납', '연장', '연체알림', '분실신고') NOT NULL,\n    action_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    previous_due_date DATETIME NULL,\n    new_due_date DATETIME NULL,\n    notes TEXT,\n    processed_by VARCHAR(100),\n    FOREIGN KEY (loan_id) REFERENCES loans(loan_id),\n    INDEX idx_loan_id (loan_id),\n    INDEX idx_action_type (action_type),\n    INDEX idx_action_date (action_date)\n);\n-- 연체 관리 테이블\nCREATE TABLE overdue_records (\n    overdue_id INT AUTO_INCREMENT PRIMARY KEY,\n    loan_id INT NOT NULL,\n    overdue_days INT NOT NULL,\n    fine_amount DECIMAL(10,2) DEFAULT 0.00,\n    fine_paid BOOLEAN DEFAULT FALSE,\n    notification_count INT DEFAULT 0,\n    last_notification_date DATETIME NULL,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    FOREIGN KEY (loan_id) REFERENCES loans(loan_id),\n    INDEX idx_loan_id (loan_id),\n    INDEX idx_overdue_days (overdue_days)\n);",
                "ddlFields": [
                  "loan_id",
                  "member_id",
                  "book_id",
                  "loan_date",
                  "due_date",
                  "return_date",
                  "loan_period_days",
                  "status",
                  "extension_count",
                  "created_at",
                  "updated_at",
                  "reservation_id",
                  "reservation_date",
                  "notification_sent",
                  "expiry_date",
                  "history_id",
                  "action_type",
                  "action_date",
                  "previous_due_date",
                  "new_due_date",
                  "notes",
                  "processed_by",
                  "overdue_id",
                  "overdue_days",
                  "fine_amount",
                  "fine_paid",
                  "notification_count",
                  "last_notification_date"
                ],
                "event": "{\"name\":\"LoanRequested\",\"displayName\":\"대출이 신청됨\",\"actor\":\"회원\",\"level\":4,\"description\":\"회원이 도서 대출을 신청하고 대출 기간(7/14/30일)을 선택함. 회원번호와 이름으로 회원 인증이 선행됨.\",\"inputs\":[\"회원번호\",\"이름\",\"대출 도서\",\"대출 기간\",\"도서 상태=대출가능\"],\"outputs\":[\"대출 요청 생성\"],\"nextEvents\":[\"LoanApproved\",\"LoanRejected\"]}\n{\"name\":\"LoanRejected\",\"displayName\":\"대출이 거절됨\",\"actor\":\"도서관리시스템\",\"level\":5,\"description\":\"대출 신청 시 도서가 이미 대출 중이거나 폐기 상태일 경우 대출이 거절됨.\",\"inputs\":[\"대출 도서 상태=대출중/폐기\"],\"outputs\":[\"대출 요청 거절 안내\"],\"nextEvents\":[\"ReservationRequested\"]}\n{\"name\":\"LoanApproved\",\"displayName\":\"대출이 승인됨\",\"actor\":\"도서관리시스템\",\"level\":6,\"description\":\"도서가 대출가능 상태여서 대출이 승인되고, 도서 상태가 '대출중'으로 변경됨.\",\"inputs\":[\"대출 요청\",\"도서 상태=대출가능\"],\"outputs\":[\"대출 정보 생성\",\"도서 상태 '대출중'\"],\"nextEvents\":[\"BookStateChanged\"]}\n{\"name\":\"ReservationRequested\",\"displayName\":\"예약이 신청됨\",\"actor\":\"회원\",\"level\":7,\"description\":\"회원이 대출 중인 도서에 대해 예약을 신청함.\",\"inputs\":[\"회원번호\",\"도서\",\"도서 상태=대출중\"],\"outputs\":[\"예약 정보 생성\"],\"nextEvents\":[\"BookStateChanged\"]}\n{\"name\":\"LoanExtended\",\"displayName\":\"대출이 연장됨\",\"actor\":\"회원\",\"level\":8,\"description\":\"회원이 대출 중인 도서에 대해 대출 연장을 요청하여 연장됨.\",\"inputs\":[\"회원번호\",\"대출 정보\",\"연장 조건 만족\"],\"outputs\":[\"반납예정일 변경\"],\"nextEvents\":[]}\n{\"name\":\"LoanReturned\",\"displayName\":\"도서가 반납됨\",\"actor\":\"회원\",\"level\":9,\"description\":\"회원이 대출 중이던 도서를 반납함.\",\"inputs\":[\"회원번호\",\"대출 정보\",\"반납 처리\"],\"outputs\":[\"도서 상태 변경\",\"대출 상태 변경(반납완료)\"],\"nextEvents\":[\"BookStateChanged\",\"ReservationActivated\"]}\n{\"name\":\"LoanOverdue\",\"displayName\":\"대출이 연체됨\",\"actor\":\"도서관리시스템\",\"level\":10,\"description\":\"반납예정일이 지나도록 반납되지 않은 대출건이 연체 상태로 변경됨.\",\"inputs\":[\"현재일자\",\"반납예정일\",\"미반납\"],\"outputs\":[\"대출 상태가 '연체'로 변경됨\"],\"nextEvents\":[]}\n{\"name\":\"ReservationActivated\",\"displayName\":\"예약이 활성화됨\",\"actor\":\"도서관리시스템\",\"level\":11,\"description\":\"예약자가 존재하는 도서가 반납되면 도서 상태가 '예약중'으로 변경되고 예약자가 알림을 받음.\",\"inputs\":[\"도서 반납\",\"예약 존재\"],\"outputs\":[\"도서 상태 '예약중'\",\"예약자 알림\"],\"nextEvents\":[\"BookStateChanged\"]}\n{\"name\":\"LoanHistoryUpdated\",\"displayName\":\"대출 이력이 갱신됨\",\"actor\":\"도서관리시스템\",\"level\":12,\"description\":\"모든 대출/반납/연장/연체 등 대출 관련 상태 변화 시 대출 이력이 갱신됨.\",\"inputs\":[\"대출/반납/연장/연체 이벤트\"],\"outputs\":[\"대출 이력 저장/추가\"],\"nextEvents\":[]}",
                "eventNames": "LoanRequested, LoanRejected, LoanApproved, ReservationRequested, LoanExtended, LoanReturned, LoanOverdue, ReservationActivated, LoanHistoryUpdated 이벤트가 발생할 수 있어.",
                "userStory": "'대출/반납' 화면에서는 회원이 도서를 대출하고 반납하는 것을 관리할 수 있어야 해. 대출 신청 시에는 회원번호와 이름으로 회원을 확인하고, 대출할 도서를 선택해야 해. 도서는 도서명이나 ISBN으로 검색할 수 있어야 해. 대출 기간은 7일/14일/30일 중에서 선택할 수 있어. 만약 대출하려는 도서가 이미 대출 중이라면, 예약 신청이 가능해야 해. 대출이 완료되면 해당 도서의 상태는 자동으로 '대출중'으로 변경되어야 해.\n대출 현황 화면에서는 현재 대출 중인 도서들의 목록을 볼 수 있어야 해. 각 대출 건에 대해 대출일, 반납예정일, 현재 상태(대출중/연체/반납완료)를 확인할 수 있어야 하고, 대출 중인 도서는 연장이나 반납 처리가 가능해야 해. 도서가 반납되면 자동으로 해당 도서의 상태가 '대출가능'으로 변경되어야 해. 만약 예약자가 있는 도서가 반납되면, 해당 도서는 '예약중' 상태로 변경되어야 해.\n각 도서별로 대출 이력과 상태 변경 이력을 조회할 수 있어야 하고, 이를 통해 도서의 대출 현황과 상태 변화를 추적할 수 있어야 해."
              }
            },
            "cons": {
              "cohesion": "연체 처리 과정에서 Loan과 OverdueRecord 간 데이터 일관성을 보장하려면 응용서비스 또는 이벤트 연동이 필수적이다.",
              "complexity": "오케스트레이션 및 이벤트 기반 연동 로직이 추가되어 전체 시스템 복잡도가 다소 증가한다.",
              "consistency": "연체 발생과 대출 상태 변경이 분리 트랜잭션이므로 순간적인 데이터 불일치(이벤트처리 지연 등)가 발생할 수 있다.",
              "coupling": "대출 연체 등 상태 변화가 Aggregate 간 동기화돼야 하므로 오케스트레이션 로직이 증가한다.",
              "encapsulation": "업무 흐름이 여러 Aggregate에 걸쳐 있으므로, 전반적 도메인 흐름 파악에 추가 학습이 필요하다.",
              "independence": "트랜잭션 처리 경계가 분리되어 일부 단일 뷰(예: 대출+연체 상세 조회)는 별도 조인이 필요하다.",
              "performance": "대출 상태와 연체 정보를 동시에 자주 조회하는 화면에서는 성능 저하가 일부 발생할 수 있다."
            },
            "description": "# Bounded Context Overview: LoanProcess (대출/반납 프로세스)\n\n## Role\n대출/반납 프로세스에서는 회원 인증, 도서 대출/반납/연장, 도서 예약, 대출 상태(대출중, 연체, 반납완료) 변경, 대출 이력 갱신, 예약 활성화 및 알림 트리거 역할을 담당한다. 프로세스의 흐름에 따라 도서 상태 변경 이벤트를 발생시키거나 구독한다.\n\n## Key Events\n- LoanRequested\n- LoanRejected\n- LoanApproved\n- ReservationRequested\n- LoanExtended\n- LoanReturned\n- LoanOverdue\n- ReservationActivated\n- LoanHistoryUpdated\n\n# Requirements\n\n## userStory\n\n'대출/반납' 화면에서는 회원이 도서를 대출하고 반납하는 것을 관리할 수 있어야 해. 대출 신청 시에는 회원번호와 이름으로 회원을 확인하고, 대출할 도서를 선택해야 해. 도서는 도서명이나 ISBN으로 검색할 수 있어야 해. 대출 기간은 7일/14일/30일 중에서 선택할 수 있어. 만약 대출하려는 도서가 이미 대출 중이라면, 예약 신청이 가능해야 해. 대출이 완료되면 해당 도서의 상태는 자동으로 '대출중'으로 변경되어야 해.\n\n대출 현황 화면에서는 현재 대출 중인 도서들의 목록을 볼 수 있어야 해. 각 대출 건에 대해 대출일, 반납예정일, 현재 상태(대출중/연체/반납완료)를 확인할 수 있어야 하고, 대출 중인 도서는 연장이나 반납 처리가 가능해야 해. 도서가 반납되면 자동으로 해당 도서의 상태가 '대출가능'으로 변경되어야 해. 만약 예약자가 있는 도서가 반납되면, 해당 도서는 '예약중' 상태로 변경되어야 해.\n\n각 도서별로 대출 이력과 상태 변경 이력을 조회할 수 있어야 하고, 이를 통해 도서의 대출 현황과 상태 변화를 추적할 수 있어야 해.\n\n## Event\n\n```json\n{\n  \"name\": \"LoanRequested\",\n  \"displayName\": \"대출이 신청됨\",\n  \"actor\": \"회원\",\n  \"level\": 4,\n  \"description\": \"회원이 도서 대출을 신청하고 대출 기간(7/14/30일)을 선택함. 회원번호와 이름으로 회원 인증이 선행됨.\",\n  \"inputs\": [\n    \"회원번호\",\n    \"이름\",\n    \"대출 도서\",\n    \"대출 기간\",\n    \"도서 상태=대출가능\"\n  ],\n  \"outputs\": [\n    \"대출 요청 생성\"\n  ],\n  \"nextEvents\": [\n    \"LoanApproved\",\n    \"LoanRejected\"\n  ]\n}\n```\n\n```json\n{\n  \"name\": \"LoanRejected\",\n  \"displayName\": \"대출이 거절됨\",\n  \"actor\": \"도서관리시스템\",\n  \"level\": 5,\n  \"description\": \"대출 신청 시 도서가 이미 대출 중이거나 폐기 상태일 경우 대출이 거절됨.\",\n  \"inputs\": [\n    \"대출 도서 상태=대출중/폐기\"\n  ],\n  \"outputs\": [\n    \"대출 요청 거절 안내\"\n  ],\n  \"nextEvents\": [\n    \"ReservationRequested\"\n  ]\n}\n```\n\n```json\n{\n  \"name\": \"LoanApproved\",\n  \"displayName\": \"대출이 승인됨\",\n  \"actor\": \"도서관리시스템\",\n  \"level\": 6,\n  \"description\": \"도서가 대출가능 상태여서 대출이 승인되고, 도서 상태가 '대출중'으로 변경됨.\",\n  \"inputs\": [\n    \"대출 요청\",\n    \"도서 상태=대출가능\"\n  ],\n  \"outputs\": [\n    \"대출 정보 생성\",\n    \"도서 상태 '대출중'\"\n  ],\n  \"nextEvents\": [\n    \"BookStateChanged\"\n  ]\n}\n```\n\n```json\n{\n  \"name\": \"ReservationRequested\",\n  \"displayName\": \"예약이 신청됨\",\n  \"actor\": \"회원\",\n  \"level\": 7,\n  \"description\": \"회원이 대출 중인 도서에 대해 예약을 신청함.\",\n  \"inputs\": [\n    \"회원번호\",\n    \"도서\",\n    \"도서 상태=대출중\"\n  ],\n  \"outputs\": [\n    \"예약 정보 생성\"\n  ],\n  \"nextEvents\": [\n    \"BookStateChanged\"\n  ]\n}\n```\n\n```json\n{\n  \"name\": \"LoanExtended\",\n  \"displayName\": \"대출이 연장됨\",\n  \"actor\": \"회원\",\n  \"level\": 8,\n  \"description\": \"회원이 대출 중인 도서에 대해 대출 연장을 요청하여 연장됨.\",\n  \"inputs\": [\n    \"회원번호\",\n    \"대출 정보\",\n    \"연장 조건 만족\"\n  ],\n  \"outputs\": [\n    \"반납예정일 변경\"\n  ],\n  \"nextEvents\": []\n}\n```\n\n```json\n{\n  \"name\": \"LoanReturned\",\n  \"displayName\": \"도서가 반납됨\",\n  \"actor\": \"회원\",\n  \"level\": 9,\n  \"description\": \"회원이 대출 중이던 도서를 반납함.\",\n  \"inputs\": [\n    \"회원번호\",\n    \"대출 정보\",\n    \"반납 처리\"\n  ],\n  \"outputs\": [\n    \"도서 상태 변경\",\n    \"대출 상태 변경(반납완료)\"\n  ],\n  \"nextEvents\": [\n    \"BookStateChanged\",\n    \"ReservationActivated\"\n  ]\n}\n```\n\n```json\n{\n  \"name\": \"LoanOverdue\",\n  \"displayName\": \"대출이 연체됨\",\n  \"actor\": \"도서관리시스템\",\n  \"level\": 10,\n  \"description\": \"반납예정일이 지나도록 반납되지 않은 대출건이 연체 상태로 변경됨.\",\n  \"inputs\": [\n    \"현재일자\",\n    \"반납예정일\",\n    \"미반납\"\n  ],\n  \"outputs\": [\n    \"대출 상태가 '연체'로 변경됨\"\n  ],\n  \"nextEvents\": []\n}\n```\n\n```json\n{\n  \"name\": \"ReservationActivated\",\n  \"displayName\": \"예약이 활성화됨\",\n  \"actor\": \"도서관리시스템\",\n  \"level\": 11,\n  \"description\": \"예약자가 존재하는 도서가 반납되면 도서 상태가 '예약중'으로 변경되고 예약자가 알림을 받음.\",\n  \"inputs\": [\n    \"도서 반납\",\n    \"예약 존재\"\n  ],\n  \"outputs\": [\n    \"도서 상태 '예약중'\",\n    \"예약자 알림\"\n  ],\n  \"nextEvents\": [\n    \"BookStateChanged\"\n  ]\n}\n```\n\n```json\n{\n  \"name\": \"LoanHistoryUpdated\",\n  \"displayName\": \"대출 이력이 갱신됨\",\n  \"actor\": \"도서관리시스템\",\n  \"level\": 12,\n  \"description\": \"모든 대출/반납/연장/연체 등 대출 관련 상태 변화 시 대출 이력이 갱신됨.\",\n  \"inputs\": [\n    \"대출/반납/연장/연체 이벤트\"\n  ],\n  \"outputs\": [\n    \"대출 이력 저장/추가\"\n  ],\n  \"nextEvents\": []\n}\n```\n\n## DDL\n\n```sql\n-- 대출 테이블\nCREATE TABLE loans (\n    loan_id INT AUTO_INCREMENT PRIMARY KEY,\n    member_id VARCHAR(20) NOT NULL,\n    book_id INT NOT NULL,\n    loan_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    due_date DATETIME NOT NULL,\n    return_date DATETIME NULL,\n    loan_period_days INT NOT NULL CHECK (loan_period_days IN (7, 14, 30)),\n    status ENUM('대출중', '연체', '반납완료', '연장') DEFAULT '대출중',\n    extension_count INT DEFAULT 0,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    FOREIGN KEY (member_id) REFERENCES members(member_id),\n    FOREIGN KEY (book_id) REFERENCES books(book_id),\n    INDEX idx_member_id (member_id),\n    INDEX idx_book_id (book_id),\n    INDEX idx_status (status),\n    INDEX idx_due_date (due_date)\n);\n```\n\n```sql\n-- 예약 테이블\nCREATE TABLE reservations (\n    reservation_id INT AUTO_INCREMENT PRIMARY KEY,\n    member_id VARCHAR(20) NOT NULL,\n    book_id INT NOT NULL,\n    reservation_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    status ENUM('예약중', '예약완료', '예약취소', '예약만료') DEFAULT '예약중',\n    notification_sent BOOLEAN DEFAULT FALSE,\n    expiry_date DATETIME NULL,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    FOREIGN KEY (member_id) REFERENCES members(member_id),\n    FOREIGN KEY (book_id) REFERENCES books(book_id),\n    INDEX idx_member_id (member_id),\n    INDEX idx_book_id (book_id),\n    INDEX idx_status (status),\n    INDEX idx_reservation_date (reservation_date)\n);\n```\n\n```sql\n-- 대출 이력 테이블 (모든 대출 활동의 상세 로그)\nCREATE TABLE loan_history (\n    history_id INT AUTO_INCREMENT PRIMARY KEY,\n    loan_id INT NOT NULL,\n    action_type ENUM('대출', '반납', '연장', '연체알림', '분실신고') NOT NULL,\n    action_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    previous_due_date DATETIME NULL,\n    new_due_date DATETIME NULL,\n    notes TEXT,\n    processed_by VARCHAR(100),\n    FOREIGN KEY (loan_id) REFERENCES loans(loan_id),\n    INDEX idx_loan_id (loan_id),\n    INDEX idx_action_type (action_type),\n    INDEX idx_action_date (action_date)\n);\n```\n\n```sql\n-- 연체 관리 테이블\nCREATE TABLE overdue_records (\n    overdue_id INT AUTO_INCREMENT PRIMARY KEY,\n    loan_id INT NOT NULL,\n    overdue_days INT NOT NULL,\n    fine_amount DECIMAL(10,2) DEFAULT 0.00,\n    fine_paid BOOLEAN DEFAULT FALSE,\n    notification_count INT DEFAULT 0,\n    last_notification_date DATETIME NULL,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    FOREIGN KEY (loan_id) REFERENCES loans(loan_id),\n    INDEX idx_loan_id (loan_id),\n    INDEX idx_overdue_days (overdue_days)\n);\n```\n\n\n## Context Relations\n\n### BookStateSync\n- **Type**: Pub/Sub\n- **Direction**: sends to 도서 관리 (BookManagement)\n- **Reason**: 대출/반납/예약 등 주요 도서 상태 변경은 프로세스 도메인에서 발생하고, 도서 관리 도메인은 해당 이벤트를 구독하여 도서 상태 일관성을 유지한다.\n- **Interaction Pattern**: 대출/반납 프로세스에서 BookStateChanged 등 이벤트를 발행하면, 도서 관리가 이를 구독하여 도서 상태를 업데이트함.\n\n### LoanStatusBookUpdate\n- **Type**: Pub/Sub\n- **Direction**: receives from 도서 관리 (BookManagement)\n- **Reason**: 대출/반납/예약 등 주요 도서 상태 변경은 프로세스 도메인에서 발생하고, 도서 관리 도메인은 해당 이벤트를 구독하여 도서 상태 일관성을 유지한다.\n- **Interaction Pattern**: 대출/반납 프로세스에서 BookStateChanged 등 이벤트를 발행하면, 도서 관리가 이를 구독하여 도서 상태를 업데이트함.\n\n### ReservationNotificationIntegration\n- **Type**: Request/Response\n- **Direction**: sends to 예약 & 알림 서비스 (reservation-notification)\n- **Reason**: 알림 서비스는 사전 구축된 PBC를 활용하며, 예약 활성화 시점에만 직접적으로 호출되기 때문에 Request/Response가 적합하다.\n- **Interaction Pattern**: 예약 활성화 이벤트 발생 시 대출/반납 프로세스가 예약 & 알림 서비스 PBC를 호출하여 알림을 전송함.",
            "isAIRecommended": True,
            "pros": {
              "cohesion": "Loan, Reservation, OverdueRecord 각각이 본연의 책임과 라이프사이클에 집중할 수 있어 역할이 명확하다.",
              "complexity": "복잡도가 적정하게 분산되어 코드 관리 및 테스트가 용이하다.",
              "consistency": "연체 정보는 별도 Aggregate로 관리되어 대출 갱신과 연체 기록이 독립적으로 트랜잭션 경계를 가진다.",
              "coupling": "연체 처리, 대출/반납, 예약 관리 등 도메인 책임이 분리되어 정책 변화 시 각 Aggregate만 수정하면 된다.",
              "encapsulation": "각 도메인 룰과 부가정보는 개별 Aggregate 내에서 은닉, 각 파트 담당자가 자신의 업무 규칙에 집중할 수 있다.",
              "independence": "연체 정책·예약 정책 변화가 Loan에 영향을 주지 않고 독립적으로 반영 가능하다.",
              "performance": "Loan과 OverdueRecord가 독립되어 처리량이 분산되고, 대출/연체 건수에 따라 각각 최적화된 스케일아웃이 가능하다."
            },
            "structure": [
              {
                "aggregate": {
                  "alias": "대출",
                  "name": "Loan"
                },
                "enumerations": [
                  {
                    "alias": "대출상태",
                    "name": "LoanStatus"
                  },
                  {
                    "alias": "대출이력액션유형",
                    "name": "LoanActionType"
                  }
                ],
                "previewAttributes": [
                  "loan_id",
                  "member_id",
                  "book_id",
                  "loan_date",
                  "due_date",
                  "return_date",
                  "loan_period_days",
                  "status",
                  "extension_count",
                  "created_at",
                  "updated_at",
                  "history_id",
                  "action_type",
                  "action_date",
                  "previous_due_date",
                  "new_due_date",
                  "notes",
                  "processed_by"
                ],
                "valueObjects": [
                  {
                    "alias": "도서참조",
                    "name": "BookReference",
                    "referencedAggregate": {
                      "alias": "도서",
                      "name": "Book"
                    }
                  },
                  {
                    "alias": "대출기간정보",
                    "name": "LoanPeriod",
                    "referencedAggregateName": ""
                  }
                ]
              },
              {
                "aggregate": {
                  "alias": "예약",
                  "name": "Reservation"
                },
                "enumerations": [
                  {
                    "alias": "예약상태",
                    "name": "ReservationStatus"
                  }
                ],
                "previewAttributes": [
                  "reservation_id",
                  "member_id",
                  "book_id",
                  "reservation_date",
                  "status",
                  "notification_sent",
                  "expiry_date",
                  "created_at",
                  "updated_at"
                ],
                "valueObjects": [
                  {
                    "alias": "도서참조",
                    "name": "BookReference",
                    "referencedAggregate": {
                      "alias": "도서",
                      "name": "Book"
                    }
                  }
                ]
              },
              {
                "aggregate": {
                  "alias": "연체기록",
                  "name": "OverdueRecord"
                },
                "previewAttributes": [
                  "overdue_id",
                  "loan_id",
                  "overdue_days",
                  "fine_amount",
                  "fine_paid",
                  "notification_count",
                  "last_notification_date",
                  "created_at",
                  "updated_at"
                ],
                "valueObjects": [
                  {
                    "alias": "대출참조",
                    "name": "LoanReference",
                    "referencedAggregate": {
                      "alias": "대출",
                      "name": "Loan"
                    }
                  }
                ]
              }
            ]
          }
        },
        userInfo=UserInfoModel(
            uid="My-UID"
        ),
        information=InformationModel(
            projectId="My-Project-ID",
        ),
        preferedLanguage="Korean",
        jobId="04d17f9e-bd7e-ec2e-4e3a-77a9c6973c6b"
    )
)

