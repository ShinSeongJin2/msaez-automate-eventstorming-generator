create_command_actions_by_function_inputs = {
    "extractedElementNames":[{'referencedId': 'book-registration', 'aggregateName': 'Book', 'commandName': 'RegisterBook'}, {'referencedId': 'book-status-management', 'aggregateName': 'Book', 'commandName': 'ChangeBookStatus'}, {'referencedId': 'book-status-management', 'aggregateName': 'Book', 'commandName': 'DiscardBook'}, {'referencedId': 'book-management', 'aggregateName': 'Book', 'readModelName': 'BookList'}, {'referencedId': 'book-management', 'aggregateName': 'Book', 'readModelName': 'BookDetails'}, {'referencedId': 'book-history', 'aggregateName': 'Book', 'readModelName': 'BookHistory'}],
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
                                "name": "changeDate",
                                "type": "Date"
                            },
                            {
                                "name": "changeReason"
                            },
                            {
                                "name": "changedBy"
                            },
                            {
                                "name": "historyId",
                                "type": "Integer"
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
                                    "DISCARDED"
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
                        "valueObjects": [],
                        "commands": [],
                        "policies": [],
                        "events": [],
                        "readModels": []
                    }
                ]
            },
            {
                "id": "bc-loanProcess",
                "name": "LoanProcess",
                "actors": [],
                "aggregates": [
                    {
                        "id": "agg-loan",
                        "name": "Loan",
                        "properties": [
                            {
                                "name": "loanId",
                                "type": "Integer",
                                "isKey": True
                            },
                            {
                                "name": "memberId"
                            },
                            {
                                "name": "bookId",
                                "type": "BookId"
                            },
                            {
                                "name": "loanDate",
                                "type": "Date"
                            },
                            {
                                "name": "dueDate",
                                "type": "Date"
                            },
                            {
                                "name": "returnDate",
                                "type": "Date"
                            },
                            {
                                "name": "loanPeriodDays",
                                "type": "Integer"
                            },
                            {
                                "name": "status",
                                "type": "LoanStatus"
                            },
                            {
                                "name": "extensionCount",
                                "type": "Integer"
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
                                "name": "historyId",
                                "type": "Integer"
                            },
                            {
                                "name": "actionType",
                                "type": "LoanActionType"
                            },
                            {
                                "name": "actionDate",
                                "type": "Date"
                            },
                            {
                                "name": "previousDueDate",
                                "type": "Date"
                            },
                            {
                                "name": "newDueDate",
                                "type": "Date"
                            },
                            {
                                "name": "notes"
                            },
                            {
                                "name": "processedBy"
                            },
                            {
                                "name": "reservationId",
                                "type": "ReservationId"
                            }
                        ],
                        "entities": [],
                        "enumerations": [
                            {
                                "id": "enum-loanStatus",
                                "name": "LoanStatus",
                                "items": [
                                    "ON_LOAN",
                                    "OVERDUE",
                                    "RETURNED",
                                    "EXTENDED"
                                ]
                            },
                            {
                                "id": "enum-loanActionType",
                                "name": "LoanActionType",
                                "items": [
                                    "LOAN",
                                    "RETURN",
                                    "EXTEND",
                                    "OVERDUE_NOTICE",
                                    "LOST_REPORT"
                                ]
                            }
                        ],
                        "valueObjects": [
                            {
                                "id": "vo-bookId",
                                "name": "BookId",
                                "properties": [
                                    {
                                        "name": "bookId",
                                        "type": "Integer",
                                        "isKey": True,
                                        "referencedAggregateName": "Book",
                                        "isForeignProperty": True
                                    }
                                ]
                            },
                            {
                                "id": "vo-reservationId",
                                "name": "ReservationId",
                                "properties": [
                                    {
                                        "name": "reservationId",
                                        "type": "Integer",
                                        "isKey": True,
                                        "referencedAggregateName": "Reservation",
                                        "isForeignProperty": True
                                    }
                                ]
                            }
                        ],
                        "commands": [],
                        "policies": [],
                        "events": [],
                        "readModels": []
                    },
                    {
                        "id": "agg-reservation",
                        "name": "Reservation",
                        "properties": [
                            {
                                "name": "reservationId",
                                "type": "Integer",
                                "isKey": True
                            },
                            {
                                "name": "memberId"
                            },
                            {
                                "name": "bookId",
                                "type": "Integer"
                            },
                            {
                                "name": "reservationDate",
                                "type": "Date"
                            },
                            {
                                "name": "status",
                                "type": "ReservationStatus"
                            },
                            {
                                "name": "notificationSent",
                                "type": "Boolean"
                            },
                            {
                                "name": "expiryDate",
                                "type": "Date"
                            },
                            {
                                "name": "createdAt",
                                "type": "Date"
                            },
                            {
                                "name": "updatedAt",
                                "type": "Date"
                            }
                        ],
                        "entities": [],
                        "enumerations": [
                            {
                                "id": "enum-reservationStatus",
                                "name": "ReservationStatus",
                                "items": [
                                    "RESERVING",
                                    "RESERVED",
                                    "CANCELLED",
                                    "EXPIRED"
                                ]
                            }
                        ],
                        "valueObjects": [],
                        "commands": [],
                        "policies": [],
                        "events": [],
                        "readModels": []
                    }
                ]
            }
        ]
    },
    "description": "1: # Bounded Context Overview: BookManagement (도서 관리)\n2: \n3: ## Role\n4: 도서의 등록, 상태 관리, 폐기, 상태 변경 및 도서별 이력 관리를 담당한다. 도서의 상태는 대출/반납/예약/폐기 등 이벤트에 따라 자동으로 변경되며, 도서별 대출 및 상태 변경 이력을 추적할 수 있다.\n5: \n6: ## Key Events\n7: - BookRegistered\n8: - BookDiscarded\n9: - BookStatusChanged\n10: \n11: # Requirements\n12: \n13: ## userStory\n14: \n15: 도서 관리' 화면에서는 새로운 도서를 등록하고 현재 보유한 도서들의 상태를 관리할 수 있어야 해. 도서 등록 시에는 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받아야 해. ISBN은 13자리 숫자여야 하고 중복 확인이 필요해. 카테고리는 소설/비소설/학술/잡지 중에서 선택할 수 있어야 해. 등록된 도서는 처음에 '대출가능' 상태가 되고, 이후 대출/반납 상황에 따라 '대출중', '예약중' 상태로 자동으로 변경되어야 해. 도서가 훼손되거나 분실된 경우 '폐기' 처리가 가능해야 하며, 폐기된 도서는 더 이상 대출이 불가능해야\n16: \n17: 도서별로 대출 이력과 상태 변경 이력을 조회할 수 있어야 하고, 이를 통해 도서의 대출 현황과 상태 변화를 추적할\n18: \n19: ## DDL\n20: \n21: ```sql\n22: CREATE TABLE books (\n23:     book_id INT AUTO_INCREMENT PRIMARY KEY,\n24:     title VARCHAR(500) NOT NULL,\n25:     isbn VARCHAR(13) UNIQUE NOT NULL,\n26:     author VARCHAR(200) NOT NULL,\n27:     publisher VARCHAR(200) NOT NULL,\n28:     category ENUM('소설', '비소설', '학술', '잡지') NOT NULL,\n29:     status ENUM('대출가능', '대출중', '예약중', '폐기') DEFAULT '대출가능',\n30:     registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n31:     disposal_date DATETIME NULL,\n32:     disposal_reason TEXT NULL,\n33:     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n34:     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n35:     INDEX idx_title (title),\n36:     INDEX idx_isbn (isbn),\n37:     INDEX idx_status (status),\n38:     INDEX idx_category (category)\n39: );\n40: ```\n41: ```sql\n42: CREATE TABLE book_status_history (\n43:     history_id INT AUTO_INCREMENT PRIMARY KEY,\n44:     book_id INT NOT NULL,\n45:     previous_status ENUM('대출가능', '대출중', '예약중', '폐기'),\n46:     new_status ENUM('대출가능', '대출중', '예약중', '폐기') NOT NULL,\n47:     change_reason VARCHAR(200),\n48:     changed_by VARCHAR(100),\n49:     change_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n50:     FOREIGN KEY (book_id) REFERENCES books(book_id),\n51:     INDEX idx_book_id (book_id),\n52:     INDEX idx_change_date (change_date)\n53: );\n54: ```\n55: ## Event\n56: \n57: ```json\n58: {\n59:   \"name\": \"BookRegistered\",\n60:   \"displayName\": \"도서 등록됨\",\n61:   \"actor\": \"Librarian\",\n62:   \"level\": 1,\n63:   \"description\": \"관리자가 새로운 도서를 도서관 시스템에 등록함. 등록 시 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받고, ISBN 중복 및 유효성 검증이 완료됨.\",\n64:   \"inputs\": [\n65:     \"도서명\",\n66:     \"ISBN(13자리)\",\n67:     \"저자\",\n68:     \"출판사\",\n69:     \"카테고리(소설/비소설/학술/잡지)\"\n70:   ],\n71:   \"outputs\": [\n72:     \"신규 도서 생성\",\n73:     \"도서 상태 '대출가능'으로 설정\"\n74:   ],\n75:   \"nextEvents\": [\n76:     \"BookStatusChanged\"\n77:   ]\n78: }\n79: ```\n80: \n81: ```json\n82: {\n83:   \"name\": \"BookStatusChanged\",\n84:   \"displayName\": \"도서 상태 변경됨\",\n85:   \"actor\": \"System\",\n86:   \"level\": 2,\n87:   \"description\": \"도서의 대출/반납/예약/폐기 등 상황에 따라 도서 상태가 자동으로 변경됨.\",\n88:   \"inputs\": [\n89:     \"도서 상태 변경 트리거(대출, 반납, 예약, 폐기 등)\"\n90:   ],\n91:   \"outputs\": [\n92:     \"도서 상태(대출가능, 대출중, 예약중, 폐기)\"\n93:   ],\n94:   \"nextEvents\": [\n95:     \"BookDiscarded\",\n96:     \"LoanRequested\",\n97:     \"BookReturned\",\n98:     \"BookReserved\"\n99:   ]\n100: }\n101: ```\n102: \n103: ```json\n104: {\n105:   \"name\": \"BookDiscarded\",\n106:   \"displayName\": \"도서 폐기됨\",\n107:   \"actor\": \"Librarian\",\n108:   \"level\": 3,\n109:   \"description\": \"도서가 훼손되거나 분실된 경우 관리자가 해당 도서를 폐기 처리함. 폐기된 도서는 더 이상 대출이 불가능함.\",\n110:   \"inputs\": [\n111:     \"도서 훼손/분실 사유\",\n112:     \"도서 식별자\"\n113:   ],\n114:   \"outputs\": [\n115:     \"도서 상태 '폐기'로 변경\"\n116:   ],\n117:   \"nextEvents\": []\n118: }\n119: ```\n120: \n121: ```json\n122: {\n123:   \"name\": \"BookHistoryChecked\",\n124:   \"displayName\": \"도서 이력 조회됨\",\n125:   \"actor\": \"Librarian\",\n126:   \"level\": 1,\n127:   \"description\": \"관리자가 도서별 대출 이력과 상태 변경 이력을 조회함.\",\n128:   \"inputs\": [\n129:     \"도서 식별자\"\n130:   ],\n131:   \"outputs\": [\n132:     \"대출 이력\",\n133:     \"상태 변경 이력\"\n134:   ],\n135:   \"nextEvents\": []\n136: }\n137: ```\n138: \n139: ## Context Relations\n140: \n141: ### BookManagement-LoanProcess\n142: - **Type**: Pub/Sub\n143: - **Direction**: sends to 대출/반납 프로세스 (LoanProcess)\n144: - **Reason**: 도서 상태 변경 등 이벤트가 발생하면 대출/반납 프로세스에서 이를 구독하여 처리할 수 있도록 느슨한 결합을 유지하기 위함.\n145: - **Interaction Pattern**: 도서 등록, 폐기, 상태 변경 이벤트가 발생하면 대출/반납 프로세스에서 해당 이벤트를 구독하여 대출 가능 여부 등을 판단한다.\n146: \n147: ### LoanProcess-BookManagement\n148: - **Type**: Pub/Sub\n149: - **Direction**: receives from 대출/반납 프로세스 (LoanProcess)\n150: - **Reason**: 도서 상태 변경 등 이벤트가 발생하면 대출/반납 프로세스에서 이를 구독하여 처리할 수 있도록 느슨한 결합을 유지하기 위함.\n151: - **Interaction Pattern**: 도서 등록, 폐기, 상태 변경 이벤트가 발생하면 대출/반납 프로세스에서 해당 이벤트를 구독하여 대출 가능 여부 등을 판단한다.\n152: \n153: ### BookManagement-LoanStatusInquiry\n154: - **Type**: Pub/Sub\n155: - **Direction**: sends to 대출 현황 및 이력 조회 (LoanStatusInquiry)\n156: - **Reason**: 도서의 상태 변경 및 이력 이벤트가 발생하면 현황 및 이력 조회 컨텍스트가 이를 구독하여 도서별 이력 정보를 제공한다.\n157: - **Interaction Pattern**: 도서 등록, 폐기, 상태 변경 이벤트가 발생할 때마다 현황 및 이력 조회 컨텍스트가 도서별 이력 정보를 갱신한다.",
    "targetAggregate": {
        "aggregateRoot": {
            "_type": "org.uengine.modeling.model.AggregateRoot",
            "fieldDescriptors": [
                {
                    "className": "Integer",
                    "isCopy": False,
                    "isKey": True,
                    "name": "bookId",
                    "traceName": "bookId",
                    "nameCamelCase": "bookId",
                    "namePascalCase": "BookId",
                    "displayName": "",
                    "_type": "org.uengine.model.FieldDescriptor",
                    "isList": False,
                    "refs": [
                        [
                            [
                                23,
                                5
                            ],
                            [
                                23,
                                38
                            ]
                        ]
                    ],
                    "referenceClass": None,
                    "isOverrideField": False
                },
                {
                    "className": "String",
                    "isCopy": False,
                    "isKey": False,
                    "name": "title",
                    "traceName": "title",
                    "nameCamelCase": "title",
                    "namePascalCase": "Title",
                    "displayName": "",
                    "_type": "org.uengine.model.FieldDescriptor",
                    "isList": False,
                    "refs": [
                        [
                            [
                                24,
                                5
                            ],
                            [
                                24,
                                26
                            ]
                        ],
                        [
                            [
                                65,
                                6
                            ],
                            [
                                65,
                                8
                            ]
                        ]
                    ],
                    "referenceClass": None,
                    "isOverrideField": False
                },
                {
                    "className": "String",
                    "isCopy": False,
                    "isKey": False,
                    "name": "isbn",
                    "traceName": "isbn",
                    "nameCamelCase": "isbn",
                    "namePascalCase": "Isbn",
                    "displayName": "",
                    "_type": "org.uengine.model.FieldDescriptor",
                    "isList": False,
                    "refs": [
                        [
                            [
                                25,
                                5
                            ],
                            [
                                25,
                                31
                            ]
                        ],
                        [
                            [
                                66,
                                6
                            ],
                            [
                                66,
                                9
                            ]
                        ]
                    ],
                    "referenceClass": None,
                    "isOverrideField": False
                },
                {
                    "className": "String",
                    "isCopy": False,
                    "isKey": False,
                    "name": "author",
                    "traceName": "author",
                    "nameCamelCase": "author",
                    "namePascalCase": "Author",
                    "displayName": "",
                    "_type": "org.uengine.model.FieldDescriptor",
                    "isList": False,
                    "refs": [
                        [
                            [
                                26,
                                5
                            ],
                            [
                                26,
                                27
                            ]
                        ],
                        [
                            [
                                67,
                                6
                            ],
                            [
                                67,
                                7
                            ]
                        ]
                    ],
                    "referenceClass": None,
                    "isOverrideField": False
                },
                {
                    "className": "String",
                    "isCopy": False,
                    "isKey": False,
                    "name": "publisher",
                    "traceName": "publisher",
                    "nameCamelCase": "publisher",
                    "namePascalCase": "Publisher",
                    "displayName": "",
                    "_type": "org.uengine.model.FieldDescriptor",
                    "isList": False,
                    "refs": [
                        [
                            [
                                27,
                                5
                            ],
                            [
                                27,
                                30
                            ]
                        ],
                        [
                            [
                                68,
                                6
                            ],
                            [
                                68,
                                8
                            ]
                        ]
                    ],
                    "referenceClass": None,
                    "isOverrideField": False
                },
                {
                    "className": "BookCategory",
                    "isCopy": False,
                    "isKey": False,
                    "name": "category",
                    "traceName": "category",
                    "nameCamelCase": "category",
                    "namePascalCase": "Category",
                    "displayName": "",
                    "_type": "org.uengine.model.FieldDescriptor",
                    "isList": False,
                    "refs": [
                        [
                            [
                                28,
                                5
                            ],
                            [
                                28,
                                46
                            ]
                        ],
                        [
                            [
                                69,
                                6
                            ],
                            [
                                69,
                                22
                            ]
                        ]
                    ],
                    "referenceClass": None,
                    "isOverrideField": False
                },
                {
                    "className": "BookStatus",
                    "isCopy": False,
                    "isKey": False,
                    "name": "status",
                    "traceName": "status",
                    "nameCamelCase": "status",
                    "namePascalCase": "Status",
                    "displayName": "",
                    "_type": "org.uengine.model.FieldDescriptor",
                    "isList": False,
                    "refs": [
                        [
                            [
                                29,
                                5
                            ],
                            [
                                29,
                                51
                            ]
                        ],
                        [
                            [
                                73,
                                6
                            ],
                            [
                                73,
                                22
                            ]
                        ]
                    ],
                    "referenceClass": None,
                    "isOverrideField": False
                },
                {
                    "className": "Date",
                    "isCopy": False,
                    "isKey": False,
                    "name": "registrationDate",
                    "traceName": "registrationDate",
                    "nameCamelCase": "registrationDate",
                    "namePascalCase": "RegistrationDate",
                    "displayName": "",
                    "_type": "org.uengine.model.FieldDescriptor",
                    "isList": False,
                    "refs": [
                        [
                            [
                                30,
                                5
                            ],
                            [
                                30,
                                56
                            ]
                        ]
                    ],
                    "referenceClass": None,
                    "isOverrideField": False
                },
                {
                    "className": "Date",
                    "isCopy": False,
                    "isKey": False,
                    "name": "disposalDate",
                    "traceName": "disposalDate",
                    "nameCamelCase": "disposalDate",
                    "namePascalCase": "DisposalDate",
                    "displayName": "",
                    "_type": "org.uengine.model.FieldDescriptor",
                    "isList": False,
                    "refs": [
                        [
                            [
                                31,
                                5
                            ],
                            [
                                31,
                                31
                            ]
                        ]
                    ],
                    "referenceClass": None,
                    "isOverrideField": False
                },
                {
                    "className": "String",
                    "isCopy": False,
                    "isKey": False,
                    "name": "disposalReason",
                    "traceName": "disposalReason",
                    "nameCamelCase": "disposalReason",
                    "namePascalCase": "DisposalReason",
                    "displayName": "",
                    "_type": "org.uengine.model.FieldDescriptor",
                    "isList": False,
                    "refs": [
                        [
                            [
                                32,
                                5
                            ],
                            [
                                32,
                                29
                            ]
                        ],
                        [
                            [
                                111,
                                9
                            ],
                            [
                                111,
                                16
                            ]
                        ]
                    ],
                    "referenceClass": None,
                    "isOverrideField": False
                },
                {
                    "className": "Date",
                    "isCopy": False,
                    "isKey": False,
                    "name": "createdAt",
                    "traceName": "createdAt",
                    "nameCamelCase": "createdAt",
                    "namePascalCase": "CreatedAt",
                    "displayName": "",
                    "_type": "org.uengine.model.FieldDescriptor",
                    "isList": False,
                    "refs": [
                        [
                            [
                                33,
                                5
                            ],
                            [
                                33,
                                49
                            ]
                        ]
                    ],
                    "referenceClass": None,
                    "isOverrideField": False
                },
                {
                    "className": "Date",
                    "isCopy": False,
                    "isKey": False,
                    "name": "updatedAt",
                    "traceName": "updatedAt",
                    "nameCamelCase": "updatedAt",
                    "namePascalCase": "UpdatedAt",
                    "displayName": "",
                    "_type": "org.uengine.model.FieldDescriptor",
                    "isList": False,
                    "refs": [
                        [
                            [
                                34,
                                5
                            ],
                            [
                                34,
                                49
                            ]
                        ]
                    ],
                    "referenceClass": None,
                    "isOverrideField": False
                },
                {
                    "className": "Date",
                    "isCopy": False,
                    "isKey": False,
                    "name": "changeDate",
                    "traceName": "changeDate",
                    "nameCamelCase": "changeDate",
                    "namePascalCase": "ChangeDate",
                    "displayName": "",
                    "_type": "org.uengine.model.FieldDescriptor",
                    "isList": False,
                    "refs": [
                        [
                            [
                                49,
                                5
                            ],
                            [
                                49,
                                50
                            ]
                        ]
                    ],
                    "referenceClass": None,
                    "isOverrideField": False
                },
                {
                    "className": "String",
                    "isCopy": False,
                    "isKey": False,
                    "name": "changeReason",
                    "traceName": "changeReason",
                    "nameCamelCase": "changeReason",
                    "namePascalCase": "ChangeReason",
                    "displayName": "",
                    "_type": "org.uengine.model.FieldDescriptor",
                    "isList": False,
                    "refs": [
                        [
                            [
                                47,
                                5
                            ],
                            [
                                47,
                                25
                            ]
                        ]
                    ],
                    "referenceClass": None,
                    "isOverrideField": False
                },
                {
                    "className": "String",
                    "isCopy": False,
                    "isKey": False,
                    "name": "changedBy",
                    "traceName": "changedBy",
                    "nameCamelCase": "changedBy",
                    "namePascalCase": "ChangedBy",
                    "displayName": "",
                    "_type": "org.uengine.model.FieldDescriptor",
                    "isList": False,
                    "refs": [
                        [
                            [
                                48,
                                5
                            ],
                            [
                                48,
                                22
                            ]
                        ]
                    ],
                    "referenceClass": None,
                    "isOverrideField": False
                },
                {
                    "className": "Integer",
                    "isCopy": False,
                    "isKey": False,
                    "name": "historyId",
                    "traceName": "historyId",
                    "nameCamelCase": "historyId",
                    "namePascalCase": "HistoryId",
                    "displayName": "",
                    "_type": "org.uengine.model.FieldDescriptor",
                    "isList": False,
                    "refs": [
                        [
                            [
                                43,
                                5
                            ],
                            [
                                43,
                                41
                            ]
                        ]
                    ],
                    "referenceClass": None,
                    "isOverrideField": False
                }
            ],
            "entities": {
                "elements": {
                    "1c0b547d-3b80-441c-b1d6-452c68dfe450": {
                        "_type": "org.uengine.uml.model.Class",
                        "id": "1c0b547d-3b80-441c-b1d6-452c68dfe450",
                        "name": "Book",
                        "traceName": "Book",
                        "namePascalCase": "Book",
                        "nameCamelCase": "book",
                        "namePlural": "books",
                        "fieldDescriptors": [
                            {
                                "className": "Integer",
                                "isCopy": False,
                                "isKey": True,
                                "name": "bookId",
                                "traceName": "bookId",
                                "nameCamelCase": "bookId",
                                "namePascalCase": "BookId",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor",
                                "isList": False,
                                "refs": [
                                    [
                                        [
                                            23,
                                            5
                                        ],
                                        [
                                            23,
                                            38
                                        ]
                                    ]
                                ],
                                "inputUI": None,
                                "options": None
                            },
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": False,
                                "name": "title",
                                "traceName": "title",
                                "nameCamelCase": "title",
                                "namePascalCase": "Title",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor",
                                "isList": False,
                                "refs": [
                                    [
                                        [
                                            24,
                                            5
                                        ],
                                        [
                                            24,
                                            26
                                        ]
                                    ],
                                    [
                                        [
                                            65,
                                            6
                                        ],
                                        [
                                            65,
                                            8
                                        ]
                                    ]
                                ],
                                "inputUI": None,
                                "options": None
                            },
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": False,
                                "name": "isbn",
                                "traceName": "isbn",
                                "nameCamelCase": "isbn",
                                "namePascalCase": "Isbn",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor",
                                "isList": False,
                                "refs": [
                                    [
                                        [
                                            25,
                                            5
                                        ],
                                        [
                                            25,
                                            31
                                        ]
                                    ],
                                    [
                                        [
                                            66,
                                            6
                                        ],
                                        [
                                            66,
                                            9
                                        ]
                                    ]
                                ],
                                "inputUI": None,
                                "options": None
                            },
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": False,
                                "name": "author",
                                "traceName": "author",
                                "nameCamelCase": "author",
                                "namePascalCase": "Author",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor",
                                "isList": False,
                                "refs": [
                                    [
                                        [
                                            26,
                                            5
                                        ],
                                        [
                                            26,
                                            27
                                        ]
                                    ],
                                    [
                                        [
                                            67,
                                            6
                                        ],
                                        [
                                            67,
                                            7
                                        ]
                                    ]
                                ],
                                "inputUI": None,
                                "options": None
                            },
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": False,
                                "name": "publisher",
                                "traceName": "publisher",
                                "nameCamelCase": "publisher",
                                "namePascalCase": "Publisher",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor",
                                "isList": False,
                                "refs": [
                                    [
                                        [
                                            27,
                                            5
                                        ],
                                        [
                                            27,
                                            30
                                        ]
                                    ],
                                    [
                                        [
                                            68,
                                            6
                                        ],
                                        [
                                            68,
                                            8
                                        ]
                                    ]
                                ],
                                "inputUI": None,
                                "options": None
                            },
                            {
                                "className": "BookCategory",
                                "isCopy": False,
                                "isKey": False,
                                "name": "category",
                                "traceName": "category",
                                "nameCamelCase": "category",
                                "namePascalCase": "Category",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor",
                                "isList": False,
                                "refs": [
                                    [
                                        [
                                            28,
                                            5
                                        ],
                                        [
                                            28,
                                            46
                                        ]
                                    ],
                                    [
                                        [
                                            69,
                                            6
                                        ],
                                        [
                                            69,
                                            22
                                        ]
                                    ]
                                ],
                                "inputUI": None,
                                "options": None
                            },
                            {
                                "className": "BookStatus",
                                "isCopy": False,
                                "isKey": False,
                                "name": "status",
                                "traceName": "status",
                                "nameCamelCase": "status",
                                "namePascalCase": "Status",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor",
                                "isList": False,
                                "refs": [
                                    [
                                        [
                                            29,
                                            5
                                        ],
                                        [
                                            29,
                                            51
                                        ]
                                    ],
                                    [
                                        [
                                            73,
                                            6
                                        ],
                                        [
                                            73,
                                            22
                                        ]
                                    ]
                                ],
                                "inputUI": None,
                                "options": None
                            },
                            {
                                "className": "Date",
                                "isCopy": False,
                                "isKey": False,
                                "name": "registrationDate",
                                "traceName": "registrationDate",
                                "nameCamelCase": "registrationDate",
                                "namePascalCase": "RegistrationDate",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor",
                                "isList": False,
                                "refs": [
                                    [
                                        [
                                            30,
                                            5
                                        ],
                                        [
                                            30,
                                            56
                                        ]
                                    ]
                                ],
                                "inputUI": None,
                                "options": None
                            },
                            {
                                "className": "Date",
                                "isCopy": False,
                                "isKey": False,
                                "name": "disposalDate",
                                "traceName": "disposalDate",
                                "nameCamelCase": "disposalDate",
                                "namePascalCase": "DisposalDate",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor",
                                "isList": False,
                                "refs": [
                                    [
                                        [
                                            31,
                                            5
                                        ],
                                        [
                                            31,
                                            31
                                        ]
                                    ]
                                ],
                                "inputUI": None,
                                "options": None
                            },
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": False,
                                "name": "disposalReason",
                                "traceName": "disposalReason",
                                "nameCamelCase": "disposalReason",
                                "namePascalCase": "DisposalReason",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor",
                                "isList": False,
                                "refs": [
                                    [
                                        [
                                            32,
                                            5
                                        ],
                                        [
                                            32,
                                            29
                                        ]
                                    ],
                                    [
                                        [
                                            111,
                                            9
                                        ],
                                        [
                                            111,
                                            16
                                        ]
                                    ]
                                ],
                                "inputUI": None,
                                "options": None
                            },
                            {
                                "className": "Date",
                                "isCopy": False,
                                "isKey": False,
                                "name": "createdAt",
                                "traceName": "createdAt",
                                "nameCamelCase": "createdAt",
                                "namePascalCase": "CreatedAt",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor",
                                "isList": False,
                                "refs": [
                                    [
                                        [
                                            33,
                                            5
                                        ],
                                        [
                                            33,
                                            49
                                        ]
                                    ]
                                ],
                                "inputUI": None,
                                "options": None
                            },
                            {
                                "className": "Date",
                                "isCopy": False,
                                "isKey": False,
                                "name": "updatedAt",
                                "traceName": "updatedAt",
                                "nameCamelCase": "updatedAt",
                                "namePascalCase": "UpdatedAt",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor",
                                "isList": False,
                                "refs": [
                                    [
                                        [
                                            34,
                                            5
                                        ],
                                        [
                                            34,
                                            49
                                        ]
                                    ]
                                ],
                                "inputUI": None,
                                "options": None
                            },
                            {
                                "className": "Date",
                                "isCopy": False,
                                "isKey": False,
                                "name": "changeDate",
                                "traceName": "changeDate",
                                "nameCamelCase": "changeDate",
                                "namePascalCase": "ChangeDate",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor",
                                "isList": False,
                                "refs": [
                                    [
                                        [
                                            49,
                                            5
                                        ],
                                        [
                                            49,
                                            50
                                        ]
                                    ]
                                ],
                                "inputUI": None,
                                "options": None
                            },
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": False,
                                "name": "changeReason",
                                "traceName": "changeReason",
                                "nameCamelCase": "changeReason",
                                "namePascalCase": "ChangeReason",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor",
                                "isList": False,
                                "refs": [
                                    [
                                        [
                                            47,
                                            5
                                        ],
                                        [
                                            47,
                                            25
                                        ]
                                    ]
                                ],
                                "inputUI": None,
                                "options": None
                            },
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": False,
                                "name": "changedBy",
                                "traceName": "changedBy",
                                "nameCamelCase": "changedBy",
                                "namePascalCase": "ChangedBy",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor",
                                "isList": False,
                                "refs": [
                                    [
                                        [
                                            48,
                                            5
                                        ],
                                        [
                                            48,
                                            22
                                        ]
                                    ]
                                ],
                                "inputUI": None,
                                "options": None
                            },
                            {
                                "className": "Integer",
                                "isCopy": False,
                                "isKey": False,
                                "name": "historyId",
                                "traceName": "historyId",
                                "nameCamelCase": "historyId",
                                "namePascalCase": "HistoryId",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor",
                                "isList": False,
                                "refs": [
                                    [
                                        [
                                            43,
                                            5
                                        ],
                                        [
                                            43,
                                            41
                                        ]
                                    ]
                                ],
                                "inputUI": None,
                                "options": None
                            }
                        ],
                        "operations": [],
                        "elementView": {
                            "_type": "org.uengine.uml.model.Class",
                            "id": "1c0b547d-3b80-441c-b1d6-452c68dfe450",
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
                        "parentId": "573b904c-8c34-47ab-8ac3-2cbd2c2ecf70",
                        "refs": [
                            [
                                [
                                    4,
                                    1
                                ],
                                [
                                    4,
                                    13
                                ]
                            ]
                        ]
                    },
                    "e0fc7abe-6217-49f0-a5df-01faaf85c40b": {
                        "_type": "org.uengine.uml.model.enum",
                        "id": "e0fc7abe-6217-49f0-a5df-01faaf85c40b",
                        "name": "BookStatus",
                        "traceName": "BookStatus",
                        "displayName": "도서 상태",
                        "nameCamelCase": "bookStatus",
                        "namePascalCase": "BookStatus",
                        "namePlural": "bookStatuses",
                        "elementView": {
                            "_type": "org.uengine.uml.model.enum",
                            "id": "e0fc7abe-6217-49f0-a5df-01faaf85c40b",
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
                                "value": "AVAILABLE",
                                "traceName": "AVAILABLE",
                                "refs": [
                                    [
                                        [
                                            29,
                                            18
                                        ],
                                        [
                                            29,
                                            21
                                        ]
                                    ]
                                ]
                            },
                            {
                                "value": "ON_LOAN",
                                "traceName": "ON_LOAN",
                                "refs": [
                                    [
                                        [
                                            29,
                                            26
                                        ],
                                        [
                                            29,
                                            28
                                        ]
                                    ]
                                ]
                            },
                            {
                                "value": "RESERVED",
                                "traceName": "RESERVED",
                                "refs": [
                                    [
                                        [
                                            29,
                                            33
                                        ],
                                        [
                                            29,
                                            35
                                        ]
                                    ]
                                ]
                            },
                            {
                                "value": "DISCARDED",
                                "traceName": "DISCARDED",
                                "refs": [
                                    [
                                        [
                                            29,
                                            40
                                        ],
                                        [
                                            29,
                                            41
                                        ]
                                    ]
                                ]
                            }
                        ],
                        "useKeyValue": False,
                        "relations": [],
                        "refs": [
                            [
                                [
                                    29,
                                    5
                                ],
                                [
                                    29,
                                    51
                                ]
                            ],
                            [
                                [
                                    92,
                                    6
                                ],
                                [
                                    92,
                                    29
                                ]
                            ]
                        ]
                    },
                    "e121e110-ce49-40eb-91c4-5a7a6890769f": {
                        "_type": "org.uengine.uml.model.enum",
                        "id": "e121e110-ce49-40eb-91c4-5a7a6890769f",
                        "name": "BookCategory",
                        "traceName": "BookCategory",
                        "displayName": "도서 카테고리",
                        "nameCamelCase": "bookCategory",
                        "namePascalCase": "BookCategory",
                        "namePlural": "bookCategories",
                        "elementView": {
                            "_type": "org.uengine.uml.model.enum",
                            "id": "e121e110-ce49-40eb-91c4-5a7a6890769f",
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
                                "value": "NOVEL",
                                "traceName": "NOVEL",
                                "refs": [
                                    [
                                        [
                                            28,
                                            20
                                        ],
                                        [
                                            28,
                                            21
                                        ]
                                    ]
                                ]
                            },
                            {
                                "value": "NONFICTION",
                                "traceName": "NONFICTION",
                                "refs": [
                                    [
                                        [
                                            28,
                                            26
                                        ],
                                        [
                                            28,
                                            28
                                        ]
                                    ]
                                ]
                            },
                            {
                                "value": "ACADEMIC",
                                "traceName": "ACADEMIC",
                                "refs": [
                                    [
                                        [
                                            28,
                                            33
                                        ],
                                        [
                                            28,
                                            34
                                        ]
                                    ]
                                ]
                            },
                            {
                                "value": "MAGAZINE",
                                "traceName": "MAGAZINE",
                                "refs": [
                                    [
                                        [
                                            28,
                                            39
                                        ],
                                        [
                                            28,
                                            40
                                        ]
                                    ]
                                ]
                            }
                        ],
                        "useKeyValue": False,
                        "relations": [],
                        "refs": [
                            [
                                [
                                    28,
                                    5
                                ],
                                [
                                    28,
                                    46
                                ]
                            ],
                            [
                                [
                                    69,
                                    6
                                ],
                                [
                                    69,
                                    22
                                ]
                            ]
                        ]
                    }
                },
                "relations": {}
            },
            "operations": []
        },
        "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
        "boundedContext": {
            "name": "8a9d2422-87e9-4aa9-9087-30e9ef26d202",
            "id": "8a9d2422-87e9-4aa9-9087-30e9ef26d202"
        },
        "commands": [],
        "description": "BookManagement 컨텍스트의 도메인 요구사항과 DDL, 이벤트, 컨텍스트 통합 패턴을 분석한 결과, Book 집계는 도서의 라이프사이클 전체(등록, 상태 관리, 폐기, 상태 변경, 이력 추적)를 책임진다. 상태와 카테고리는 각각 BookStatus, BookCategory 열거형으로 정의하여 도메인 불변식과 상태 전이를 명확히 한다. DDL의 모든 필수 필드는 Book 집계에 포함되며, 이력 관리(상태 변경, 폐기 등)는 외부 컨텍스트와의 Pub/Sub 연동을 고려해 상태 및 이력 관련 속성을 포함한다. ValueObject는 요구된 구조상 생성하지 않는다. 집계 내 속성들은 이벤트 소싱 및 외부 시스템 연동(이벤트 발행/구독)에 필요한 정보를 모두 포함한다.",
        "id": "573b904c-8c34-47ab-8ac3-2cbd2c2ecf70",
        "elementView": {
            "_type": "org.uengine.modeling.model.Aggregate",
            "id": "573b904c-8c34-47ab-8ac3-2cbd2c2ecf70",
            "x": 600,
            "y": 450,
            "width": 130,
            "height": 400
        },
        "events": [],
        "hexagonalView": {
            "_type": "org.uengine.modeling.model.AggregateHexagonal",
            "id": "573b904c-8c34-47ab-8ac3-2cbd2c2ecf70",
            "x": 0,
            "y": 0,
            "subWidth": 0,
            "width": 0
        },
        "name": "Book",
        "traceName": "Book",
        "displayName": "도서",
        "nameCamelCase": "book",
        "namePascalCase": "Book",
        "namePlural": "books",
        "rotateStatus": False,
        "selected": False,
        "_type": "org.uengine.modeling.model.Aggregate",
        "refs": [
            [
                [
                    4,
                    1
                ],
                [
                    4,
                    13
                ]
            ]
        ]
    },
    "requiredEventNames": [
        "BookRegistered",
        "BookStatusChanged",
        "BookDiscarded",
        "BookHistoryChecked"
    ]
}