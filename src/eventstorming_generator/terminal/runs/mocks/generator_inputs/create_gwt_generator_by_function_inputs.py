create_gwt_generator_by_function_inputs = {
    "summarizedESValue": {
        "deletedProperties": [],
        "boundedContexts": [
            {
                "id": "bc-bookManagement",
                "name": "BookManagement",
                "actors": [
                    {
                        "id": "act-librarian",
                        "name": "Librarian"
                    }
                ],
                "aggregates": [
                    {
                        "id": "agg-book",
                        "name": "Book",
                        "properties": [
                            {
                                "name": "bookId",
                                "type": "Integer",
                                "isKey": True
                            },
                            {
                                "name": "title"
                            },
                            {
                                "name": "isbn"
                            },
                            {
                                "name": "author"
                            },
                            {
                                "name": "publisher"
                            },
                            {
                                "name": "category",
                                "type": "BookCategory"
                            },
                            {
                                "name": "status",
                                "type": "BookStatus"
                            },
                            {
                                "name": "registrationDate",
                                "type": "Date"
                            },
                            {
                                "name": "disposalDate",
                                "type": "Date"
                            },
                            {
                                "name": "disposalReason"
                            },
                            {
                                "name": "createdAt",
                                "type": "Date"
                            },
                            {
                                "name": "updatedAt",
                                "type": "Date"
                            },
                            {
                                "name": "statusHistories",
                                "type": "List<BookStatusHistory>"
                            }
                        ],
                        "entities": [],
                        "enumerations": [
                            {
                                "id": "enum-bookStatus",
                                "name": "BookStatus",
                                "items": [
                                    "AVAILABLE",
                                    "ON_LOAN",
                                    "RESERVED",
                                    "DISPOSED"
                                ]
                            },
                            {
                                "id": "enum-bookCategory",
                                "name": "BookCategory",
                                "items": [
                                    "NOVEL",
                                    "NONFICTION",
                                    "ACADEMIC",
                                    "MAGAZINE"
                                ]
                            }
                        ],
                        "valueObjects": [
                            {
                                "id": "vo-bookStatusHistory",
                                "name": "BookStatusHistory",
                                "properties": [
                                    {
                                        "name": "historyId",
                                        "type": "Integer",
                                        "isKey": True
                                    },
                                    {
                                        "name": "previousStatus",
                                        "type": "BookStatus"
                                    },
                                    {
                                        "name": "newStatus",
                                        "type": "BookStatus"
                                    },
                                    {
                                        "name": "changeReason"
                                    },
                                    {
                                        "name": "changedBy"
                                    },
                                    {
                                        "name": "changeDate",
                                        "type": "Date"
                                    }
                                ]
                            }
                        ],
                        "commands": [
                            {
                                "id": "cmd-createBook",
                                "name": "CreateBook",
                                "api_verb": "POST",
                                "isRestRepository": False,
                                "properties": [
                                    {
                                        "name": "title"
                                    },
                                    {
                                        "name": "isbn"
                                    },
                                    {
                                        "name": "author"
                                    },
                                    {
                                        "name": "publisher"
                                    },
                                    {
                                        "name": "category",
                                        "type": "BookCategory"
                                    }
                                ],
                                "outputEvents": [
                                    {
                                        "id": "evt-bookRegistered",
                                        "name": "BookRegistered"
                                    }
                                ]
                            },
                            {
                                "id": "cmd-editBook",
                                "name": "EditBook",
                                "api_verb": "PUT",
                                "isRestRepository": False,
                                "properties": [
                                    {
                                        "name": "bookId",
                                        "type": "Integer",
                                        "isKey": True
                                    },
                                    {
                                        "name": "title"
                                    },
                                    {
                                        "name": "author"
                                    },
                                    {
                                        "name": "publisher"
                                    },
                                    {
                                        "name": "category",
                                        "type": "BookCategory"
                                    }
                                ],
                                "outputEvents": [
                                    {
                                        "id": "evt-bookStatusChanged",
                                        "name": "BookStatusChanged"
                                    }
                                ]
                            },
                            {
                                "id": "cmd-disposeBook",
                                "name": "DisposeBook",
                                "api_verb": "DELETE",
                                "isRestRepository": False,
                                "properties": [
                                    {
                                        "name": "bookId",
                                        "type": "Integer",
                                        "isKey": True
                                    },
                                    {
                                        "name": "disposalReason"
                                    }
                                ],
                                "outputEvents": [
                                    {
                                        "id": "evt-bookDisposed",
                                        "name": "BookDisposed"
                                    }
                                ]
                            }
                        ],
                        "policies": [],
                        "events": [
                            {
                                "id": "evt-bookRegistered",
                                "name": "BookRegistered",
                                "properties": [
                                    {
                                        "name": "bookId",
                                        "type": "Integer",
                                        "isKey": True
                                    },
                                    {
                                        "name": "title"
                                    },
                                    {
                                        "name": "isbn"
                                    },
                                    {
                                        "name": "author"
                                    },
                                    {
                                        "name": "publisher"
                                    },
                                    {
                                        "name": "category",
                                        "type": "BookCategory"
                                    },
                                    {
                                        "name": "status",
                                        "type": "BookStatus"
                                    },
                                    {
                                        "name": "registrationDate",
                                        "type": "Date"
                                    }
                                ]
                            },
                            {
                                "id": "evt-bookStatusChanged",
                                "name": "BookStatusChanged",
                                "properties": [
                                    {
                                        "name": "bookId",
                                        "type": "Integer",
                                        "isKey": True
                                    },
                                    {
                                        "name": "previousStatus",
                                        "type": "BookStatus"
                                    },
                                    {
                                        "name": "newStatus",
                                        "type": "BookStatus"
                                    },
                                    {
                                        "name": "changeReason"
                                    },
                                    {
                                        "name": "changedBy"
                                    },
                                    {
                                        "name": "changeDate",
                                        "type": "Date"
                                    }
                                ]
                            },
                            {
                                "id": "evt-bookDisposed",
                                "name": "BookDisposed",
                                "properties": [
                                    {
                                        "name": "bookId",
                                        "type": "Integer",
                                        "isKey": True
                                    },
                                    {
                                        "name": "disposalReason"
                                    },
                                    {
                                        "name": "disposalDate",
                                        "type": "Date"
                                    },
                                    {
                                        "name": "status",
                                        "type": "BookStatus"
                                    }
                                ]
                            }
                        ],
                        "readModels": [
                            {
                                "id": "rm-bookList",
                                "name": "BookList",
                                "queryParameters": [
                                    {
                                        "name": "category",
                                        "type": "BookCategory"
                                    },
                                    {
                                        "name": "status",
                                        "type": "BookStatus"
                                    },
                                    {
                                        "name": "title"
                                    }
                                ],
                                "isMultipleResult": False
                            },
                            {
                                "id": "rm-bookStatusChangeHistory",
                                "name": "BookStatusChangeHistory",
                                "queryParameters": [
                                    {
                                        "name": "bookId",
                                        "type": "Integer",
                                        "isKey": True
                                    }
                                ],
                                "isMultipleResult": False
                            }
                        ]
                    }
                ]
            }
        ]
    },
    "description": "# Bounded Context Overview: BookManagement (도서 관리)\n\n## Role\n도서 등록, 상태 관리, 폐기 처리를 담당하며 도서의 생애주기와 상태 변화를 관리한다.\n\n## Key Events\n- BookRegistered\n- BookStatusChanged\n- BookDisposed\n\n# Requirements\n\n## userStory\n\n도서 관리' 화면에서는 새로운 도서를 등록하고 현재 보유한 도서들의 상태를 관리할 수 있어야 해. 도서 등록 시에는 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받아야 해. ISBN은 13자리 숫자여야 하고 중복 확인이 필요해. 카테고리는 소설/비소설/학술/잡지 중에서 선택할 수 있어야 해. 등록된 도서는 처음에 '대출가능' 상태가 되고, 이후 대출/반납 상황에 따라 '대출중', '예약중' 상태로 자동으로 변경되어야 해. 도서가 훼손되거나 분실된 경우 '폐기' 처리가 가능해야 하며, 폐기된 도서는 더 이상 대출이 불가능해야\n\n도서별로 대출 이력과 상태 변경 이력을 조회할 수 있어야 하고, 이를 통해 도서의 대출 현황과 상태 변화를 추적할\n\n## DDL\n\n```sql\n도서 테이블\nCREATE TABLE books (\n    book_id INT AUTO_INCREMENT PRIMARY KEY,\n    title VARCHAR(500) NOT NULL,\n    isbn VARCHAR(13) UNIQUE NOT NULL,\n    author VARCHAR(200) NOT NULL,\n    publisher VARCHAR(200) NOT NULL,\n    category ENUM('소설', '비소설', '학술', '잡지') NOT NULL,\n    status ENUM('대출가능', '대출중', '예약중', '폐기') DEFAULT '대출가능',\n    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    disposal_date DATETIME NULL,\n    disposal_reason TEXT NULL,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    INDEX idx_title (title),\n    INDEX idx_isbn (isbn),\n    INDEX idx_status (status),\n    INDEX idx_category (category)\n);\n```\n```sql\n도서 상태 변경 이력 테이블\nCREATE TABLE book_status_history (\n    history_id INT AUTO_INCREMENT PRIMARY KEY,\n    book_id INT NOT NULL,\n    previous_status ENUM('대출가능', '대출중', '예약중', '폐기'),\n    new_status ENUM('대출가능', '대출중', '예약중', '폐기') NOT NULL,\n    change_reason VARCHAR(200),\n    changed_by VARCHAR(100),\n    change_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    FOREIGN KEY (book_id) REFERENCES books(book_id),\n    INDEX idx_book_id (book_id),\n    INDEX idx_change_date (change_date)\n);\n```\n## Event\n\n```json\n{\n  \"name\": \"BookRegistered\",\n  \"displayName\": \"도서 등록됨\",\n  \"actor\": \"Librarian\",\n  \"level\": 1,\n  \"description\": \"사서가 새로운 도서를 등록하여 도서관 시스템에 추가하였음. 등록 시 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받고, ISBN 중복 및 유효성 검증이 완료됨.\",\n  \"inputs\": [\n    \"도서명\",\n    \"ISBN(13자리)\",\n    \"저자\",\n    \"출판사\",\n    \"카테고리(소설/비소설/학술/잡지)\"\n  ],\n  \"outputs\": [\n    \"신규 도서 정보\",\n    \"도서 상태: 대출가능\"\n  ],\n  \"nextEvents\": [\n    \"BookStatusChanged\"\n  ]\n}\n```\n\n```json\n{\n  \"name\": \"BookStatusChanged\",\n  \"displayName\": \"도서 상태 변경됨\",\n  \"actor\": \"System\",\n  \"level\": 2,\n  \"description\": \"도서의 대출/반납/예약/폐기 등 상태 변화가 발생하여 도서 상태가 자동 또는 수동으로 변경됨.\",\n  \"inputs\": [\n    \"도서 상태 변경 트리거(대출, 반납, 예약, 폐기 등)\",\n    \"도서 식별자\"\n  ],\n  \"outputs\": [\n    \"변경된 도서 상태\"\n  ],\n  \"nextEvents\": [\n    \"BookDisposed\",\n    \"BookLoaned\",\n    \"BookReturned\",\n    \"BookReserved\"\n  ]\n}\n```\n\n```json\n{\n  \"name\": \"BookDisposed\",\n  \"displayName\": \"도서 폐기됨\",\n  \"actor\": \"Librarian\",\n  \"level\": 3,\n  \"description\": \"도서가 훼손 또는 분실되어 사서에 의해 폐기 처리됨. 폐기된 도서는 더 이상 대출이 불가능함.\",\n  \"inputs\": [\n    \"도서 식별자\",\n    \"폐기 사유\"\n  ],\n  \"outputs\": [\n    \"도서 상태: 폐기\"\n  ],\n  \"nextEvents\": []\n}\n```\n\n## Context Relations\n\n### BookManagement-LoanAndReservation\n- **Type**: Pub/Sub\n- **Direction**: sends to 대출/반납 및 예약 (LoanAndReservation)\n- **Reason**: 도서 상태 변경(대출가능, 대출중, 예약중, 폐기 등)이 발생하면 대출/반납 및 예약 컨텍스트에서 이를 구독하여 대출/예약 프로세스에 반영한다.\n- **Interaction Pattern**: 도서 관리에서 도서 상태 변경 이벤트를 발행하면 대출/반납 및 예약 컨텍스트가 이를 구독하여 처리한다.\n\n### BookManagement-LoanHistory\n- **Type**: Pub/Sub\n- **Direction**: sends to 이력 관리 (LoanHistory)\n- **Reason**: 도서 등록, 폐기 등 도서 상태 변화 이력도 이력 관리 컨텍스트에서 기록할 수 있도록 이벤트를 발행한다.\n- **Interaction Pattern**: 도서 관리에서 도서 등록, 폐기 등 상태 변화 이벤트를 발행하면 이력 관리 컨텍스트가 이를 구독하여 상태 변경 이력을 기록한다.",
    "targetCommandAlias": "cmd-createBook"
}