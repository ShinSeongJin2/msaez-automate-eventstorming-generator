create_aggregate_actions_by_function_inputs = {
    "targetBoundedContext": {
        "name": "LoanAndReservation",
        "_type": "org.uengine.modeling.model.BoundedContext",
        "aggregates": [],
        "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
        "description": "# Bounded Context Overview: LoanAndReservation (대출/반납 및 예약)\n\n## Role\n회원의 도서 대출, 반납, 연장, 예약을 관리하고 도서 상태 변경을 트리거한다.\n\n## Key Events\n- BookLoaned\n- BookReserved\n- BookReturned\n- LoanExtended\n\n# Requirements\n\n## userStory\n\n대출/반납을 통합적으로 관리하는\n\n대출/반납' 화면에서는 회원이 도서를 대출하고 반납하는 것을 관리할 수 있어야 해. 대출 신청 시에는 회원번호와 이름으로 회원을 확인하고, 대출할\n\n예약\n\n대출 현황 화면에서는 현재 대출 중인 도서들의 목록을 볼 수 있어야 해. 각 대출 건에 대해 대출일, 반납\n\n연장\n\n대출 이력과 상태\n\n## DDL\n\n```sql\nCREATE TABLE loans (\n    loan_id INT AUTO_INCREMENT PRIMARY KEY,\n    member_id VARCHAR(20) NOT NULL,\n    book_id INT NOT NULL,\n    loan_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    due_date DATETIME NOT NULL,\n    return_date DATETIME NULL,\n    loan_period_days INT NOT NULL CHECK (loan_period_days IN (7, 14, 30)),\n    status ENUM('대출중', '연체', '반납완료', '연장') DEFAULT '대출중',\n    extension_count INT DEFAULT 0,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    FOREIGN KEY (member_id) REFERENCES members(member_id),\n    FOREIGN KEY (book_id) REFERENCES books(book_id),\n    INDEX idx_member_id (member_id),\n    INDEX idx_book_id (book_id),\n    INDEX idx_status (status),\n    INDEX idx_due_date (due_date)\n);\n```\n```sql\nCREATE TABLE reservations (\n    reservation_id INT AUTO_INCREMENT PRIMARY KEY,\n    member_id VARCHAR(20) NOT NULL,\n    book_id INT NOT NULL,\n    reservation_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    status ENUM('예약중', '예약완료', '예약취소', '예약만료') DEFAULT '예약중',\n    notification_sent BOOLEAN DEFAULT FALSE,\n    expiry_date DATETIME NULL,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    FOREIGN KEY (member_id) REFERENCES members(member_id),\n    FOREIGN KEY (book_id) REFERENCES books(book_id),\n    INDEX idx_member_id (member_id),\n    INDEX idx_book_id (book_id),\n    INDEX idx_status (status),\n    INDEX idx_reservation_date (reservation_date)\n);\n```\n```sql\nCREATE TABLE loan_history (\n    history_id INT AUTO_INCREMENT PRIMARY KEY,\n    loan_id INT NOT NULL,\n    action_type ENUM('대출', '반납', '연장', '연체알림', '분실신고') NOT NULL,\n    action_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    previous_due_date DATETIME NULL,\n    new_due_date DATETIME NULL,\n    notes TEXT,\n    processed_by VARCHAR(100),\n    FOREIGN KEY (loan_id) REFERENCES loans(loan_id),\n    INDEX idx_loan_id (loan_id),\n    INDEX idx_action_type (action_type),\n    INDEX idx_action_date (action_date)\n);\n```\n## Event\n\n```json\n{\n  \"name\": \"BookLoaned\",\n  \"displayName\": \"도서 대출됨\",\n  \"actor\": \"Member\",\n  \"level\": 4,\n  \"description\": \"회원이 도서 대출을 신청하고, 회원 인증 및 도서 상태 확인 후 대출이 승인됨. 대출 기간이 설정되고 도서 상태가 '대출중'으로 변경됨.\",\n  \"inputs\": [\n    \"회원번호\",\n    \"이름\",\n    \"도서 식별자\",\n    \"대출 기간(7/14/30일)\"\n  ],\n  \"outputs\": [\n    \"대출 정보\",\n    \"도서 상태: 대출중\"\n  ],\n  \"nextEvents\": [\n    \"BookStatusChanged\",\n    \"LoanHistoryRecorded\"\n  ]\n}\n```\n\n```json\n{\n  \"name\": \"BookReserved\",\n  \"displayName\": \"도서 예약됨\",\n  \"actor\": \"Member\",\n  \"level\": 5,\n  \"description\": \"회원이 대출 중인 도서에 대해 예약을 신청함. 예약이 완료되면 도서 상태가 '예약중'으로 변경됨.\",\n  \"inputs\": [\n    \"회원번호\",\n    \"도서 식별자\"\n  ],\n  \"outputs\": [\n    \"예약 정보\",\n    \"도서 상태: 예약중\"\n  ],\n  \"nextEvents\": [\n    \"BookStatusChanged\",\n    \"ReservationHistoryRecorded\"\n  ]\n}\n```\n\n```json\n{\n  \"name\": \"BookReturned\",\n  \"displayName\": \"도서 반납됨\",\n  \"actor\": \"Member\",\n  \"level\": 6,\n  \"description\": \"회원이 대출한 도서를 반납함. 반납 시 도서 상태가 '대출가능'으로 변경되고, 예약자가 있을 경우 '예약중'으로 변경됨.\",\n  \"inputs\": [\n    \"회원번호\",\n    \"도서 식별자\"\n  ],\n  \"outputs\": [\n    \"도서 상태: 대출가능 또는 예약중\",\n    \"반납 처리 정보\"\n  ],\n  \"nextEvents\": [\n    \"BookStatusChanged\",\n    \"LoanHistoryRecorded\"\n  ]\n}\n```\n\n```json\n{\n  \"name\": \"LoanExtended\",\n  \"displayName\": \"대출 연장됨\",\n  \"actor\": \"Member\",\n  \"level\": 7,\n  \"description\": \"회원이 대출 중인 도서의 대출 기간을 연장함. 연장 후 대출 정보와 반납 예정일이 갱신됨.\",\n  \"inputs\": [\n    \"회원번호\",\n    \"도서 식별자\",\n    \"연장 기간\"\n  ],\n  \"outputs\": [\n    \"갱신된 대출 정보\",\n    \"새 반납 예정일\"\n  ],\n  \"nextEvents\": [\n    \"LoanHistoryRecorded\"\n  ]\n}\n```\n\n## Context Relations\n\n### BookManagement-LoanAndReservation\n- **Type**: Pub/Sub\n- **Direction**: receives from 도서 관리 (BookManagement)\n- **Reason**: 도서 상태 변경(대출가능, 대출중, 예약중, 폐기 등)이 발생하면 대출/반납 및 예약 컨텍스트에서 이를 구독하여 대출/예약 프로세스에 반영한다.\n- **Interaction Pattern**: 도서 관리에서 도서 상태 변경 이벤트를 발행하면 대출/반납 및 예약 컨텍스트가 이를 구독하여 처리한다.\n\n### LoanAndReservation-LoanHistory\n- **Type**: Pub/Sub\n- **Direction**: sends to 이력 관리 (LoanHistory)\n- **Reason**: 대출, 반납, 연장, 예약 등 이벤트 발생 시 이력 관리 컨텍스트에서 해당 이벤트를 구독하여 이력을 기록한다.\n- **Interaction Pattern**: 대출/반납 및 예약에서 대출/반납/연장/예약 이벤트를 발행하면 이력 관리 컨텍스트가 이를 구독하여 이력 데이터를 생성한다.",
        "id": "a35f39e7-6201-441e-9b5b-931aeba36079",
        "elementView": {
            "_type": "org.uengine.modeling.model.BoundedContext",
            "height": 590,
            "id": "a35f39e7-6201-441e-9b5b-931aeba36079",
            "style": "{}",
            "width": 560,
            "x": 1185.0,
            "y": 450
        },
        "gitURL": None,
        "hexagonalView": {
            "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
            "height": 350,
            "id": "a35f39e7-6201-441e-9b5b-931aeba36079",
            "style": "{}",
            "width": 350,
            "x": 235,
            "y": 365
        },
        "members": [],
        "traceName": "LoanAndReservation",
        "displayName": "대출/반납 및 예약",
        "oldName": "",
        "policies": [],
        "portGenerated": 8081,
        "preferredPlatform": "template-spring-boot",
        "preferredPlatformConf": {},
        "rotateStatus": False,
        "tempId": "",
        "templatePerElements": {},
        "views": [],
        "definitionId": "163972132_es_a4afe53e52e57652bdbd6dac8e734470",
        "requirements": {
            "ddl": "CREATE TABLE loans (\n    loan_id INT AUTO_INCREMENT PRIMARY KEY,\n    member_id VARCHAR(20) NOT NULL,\n    book_id INT NOT NULL,\n    loan_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    due_date DATETIME NOT NULL,\n    return_date DATETIME NULL,\n    loan_period_days INT NOT NULL CHECK (loan_period_days IN (7, 14, 30)),\n    status ENUM('대출중', '연체', '반납완료', '연장') DEFAULT '대출중',\n    extension_count INT DEFAULT 0,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    FOREIGN KEY (member_id) REFERENCES members(member_id),\n    FOREIGN KEY (book_id) REFERENCES books(book_id),\n    INDEX idx_member_id (member_id),\n    INDEX idx_book_id (book_id),\n    INDEX idx_status (status),\n    INDEX idx_due_date (due_date)\n);\nCREATE TABLE reservations (\n    reservation_id INT AUTO_INCREMENT PRIMARY KEY,\n    member_id VARCHAR(20) NOT NULL,\n    book_id INT NOT NULL,\n    reservation_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    status ENUM('예약중', '예약완료', '예약취소', '예약만료') DEFAULT '예약중',\n    notification_sent BOOLEAN DEFAULT FALSE,\n    expiry_date DATETIME NULL,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    FOREIGN KEY (member_id) REFERENCES members(member_id),\n    FOREIGN KEY (book_id) REFERENCES books(book_id),\n    INDEX idx_member_id (member_id),\n    INDEX idx_book_id (book_id),\n    INDEX idx_status (status),\n    INDEX idx_reservation_date (reservation_date)\n);\nCREATE TABLE loan_history (\n    history_id INT AUTO_INCREMENT PRIMARY KEY,\n    loan_id INT NOT NULL,\n    action_type ENUM('대출', '반납', '연장', '연체알림', '분실신고') NOT NULL,\n    action_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    previous_due_date DATETIME NULL,\n    new_due_date DATETIME NULL,\n    notes TEXT,\n    processed_by VARCHAR(100),\n    FOREIGN KEY (loan_id) REFERENCES loans(loan_id),\n    INDEX idx_loan_id (loan_id),\n    INDEX idx_action_type (action_type),\n    INDEX idx_action_date (action_date)\n);",
            "ddlFields": [
                {
                    "fieldName": "loan_id",
                    "refs": [
                        [
                            [
                                46,
                                5
                            ],
                            [
                                46,
                                38
                            ]
                        ],
                        [
                            [
                                101,
                                5
                            ],
                            [
                                101,
                                24
                            ]
                        ]
                    ]
                },
                {
                    "fieldName": "member_id",
                    "refs": [
                        [
                            [
                                47,
                                5
                            ],
                            [
                                47,
                                34
                            ]
                        ],
                        [
                            [
                                68,
                                5
                            ],
                            [
                                68,
                                34
                            ]
                        ]
                    ]
                },
                {
                    "fieldName": "book_id",
                    "refs": [
                        [
                            [
                                48,
                                5
                            ],
                            [
                                48,
                                24
                            ]
                        ],
                        [
                            [
                                69,
                                5
                            ],
                            [
                                69,
                                24
                            ]
                        ]
                    ]
                },
                {
                    "fieldName": "loan_date",
                    "refs": [
                        [
                            [
                                49,
                                5
                            ],
                            [
                                49,
                                48
                            ]
                        ]
                    ]
                },
                {
                    "fieldName": "due_date",
                    "refs": [
                        [
                            [
                                50,
                                5
                            ],
                            [
                                50,
                                30
                            ]
                        ]
                    ]
                },
                {
                    "fieldName": "return_date",
                    "refs": [
                        [
                            [
                                51,
                                5
                            ],
                            [
                                51,
                                29
                            ]
                        ]
                    ]
                },
                {
                    "fieldName": "loan_period_days",
                    "refs": [
                        [
                            [
                                52,
                                5
                            ],
                            [
                                52,
                                39
                            ]
                        ]
                    ]
                },
                {
                    "fieldName": "status",
                    "refs": [
                        [
                            [
                                53,
                                5
                            ],
                            [
                                53,
                                50
                            ]
                        ],
                        [
                            [
                                71,
                                5
                            ],
                            [
                                71,
                                54
                            ]
                        ]
                    ]
                },
                {
                    "fieldName": "extension_count",
                    "refs": [
                        [
                            [
                                54,
                                5
                            ],
                            [
                                54,
                                31
                            ]
                        ]
                    ]
                },
                {
                    "fieldName": "created_at",
                    "refs": [
                        [
                            [
                                55,
                                5
                            ],
                            [
                                55,
                                49
                            ]
                        ],
                        [
                            [
                                74,
                                5
                            ],
                            [
                                74,
                                49
                            ]
                        ]
                    ]
                },
                {
                    "fieldName": "updated_at",
                    "refs": [
                        [
                            [
                                56,
                                5
                            ],
                            [
                                56,
                                77
                            ]
                        ],
                        [
                            [
                                75,
                                5
                            ],
                            [
                                75,
                                77
                            ]
                        ]
                    ]
                },
                {
                    "fieldName": "reservation_id",
                    "refs": [
                        [
                            [
                                67,
                                5
                            ],
                            [
                                67,
                                45
                            ]
                        ]
                    ]
                },
                {
                    "fieldName": "reservation_date",
                    "refs": [
                        [
                            [
                                70,
                                5
                            ],
                            [
                                70,
                                55
                            ]
                        ]
                    ]
                },
                {
                    "fieldName": "notification_sent",
                    "refs": [
                        [
                            [
                                72,
                                5
                            ],
                            [
                                72,
                                37
                            ]
                        ]
                    ]
                },
                {
                    "fieldName": "expiry_date",
                    "refs": [
                        [
                            [
                                73,
                                5
                            ],
                            [
                                73,
                                29
                            ]
                        ]
                    ]
                },
                {
                    "fieldName": "history_id",
                    "refs": [
                        [
                            [
                                100,
                                5
                            ],
                            [
                                100,
                                41
                            ]
                        ]
                    ]
                },
                {
                    "fieldName": "action_type",
                    "refs": [
                        [
                            [
                                102,
                                5
                            ],
                            [
                                102,
                                63
                            ]
                        ]
                    ]
                },
                {
                    "fieldName": "action_date",
                    "refs": [
                        [
                            [
                                103,
                                5
                            ],
                            [
                                103,
                                50
                            ]
                        ]
                    ]
                },
                {
                    "fieldName": "previous_due_date",
                    "refs": [
                        [
                            [
                                104,
                                5
                            ],
                            [
                                104,
                                35
                            ]
                        ]
                    ]
                },
                {
                    "fieldName": "new_due_date",
                    "refs": [
                        [
                            [
                                105,
                                5
                            ],
                            [
                                105,
                                30
                            ]
                        ]
                    ]
                },
                {
                    "fieldName": "notes",
                    "refs": [
                        [
                            [
                                106,
                                5
                            ],
                            [
                                106,
                                14
                            ]
                        ]
                    ]
                },
                {
                    "fieldName": "processed_by",
                    "refs": [
                        [
                            [
                                107,
                                5
                            ],
                            [
                                107,
                                29
                            ]
                        ]
                    ]
                }
            ],
            "description": "# Bounded Context Overview: LoanAndReservation (대출/반납 및 예약)\n\n## Role\n회원의 도서 대출, 반납, 연장, 예약을 관리하고 도서 상태 변경을 트리거한다.\n\n## Key Events\n- BookLoaned\n- BookReserved\n- BookReturned\n- LoanExtended\n\n# Requirements\n\n## userStory\n\n대출/반납을 통합적으로 관리하는\n\n대출/반납' 화면에서는 회원이 도서를 대출하고 반납하는 것을 관리할 수 있어야 해. 대출 신청 시에는 회원번호와 이름으로 회원을 확인하고, 대출할\n\n예약\n\n대출 현황 화면에서는 현재 대출 중인 도서들의 목록을 볼 수 있어야 해. 각 대출 건에 대해 대출일, 반납\n\n연장\n\n대출 이력과 상태\n\n## DDL\n\n```sql\nCREATE TABLE loans (\n    loan_id INT AUTO_INCREMENT PRIMARY KEY,\n    member_id VARCHAR(20) NOT NULL,\n    book_id INT NOT NULL,\n    loan_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    due_date DATETIME NOT NULL,\n    return_date DATETIME NULL,\n    loan_period_days INT NOT NULL CHECK (loan_period_days IN (7, 14, 30)),\n    status ENUM('대출중', '연체', '반납완료', '연장') DEFAULT '대출중',\n    extension_count INT DEFAULT 0,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    FOREIGN KEY (member_id) REFERENCES members(member_id),\n    FOREIGN KEY (book_id) REFERENCES books(book_id),\n    INDEX idx_member_id (member_id),\n    INDEX idx_book_id (book_id),\n    INDEX idx_status (status),\n    INDEX idx_due_date (due_date)\n);\n```\n```sql\nCREATE TABLE reservations (\n    reservation_id INT AUTO_INCREMENT PRIMARY KEY,\n    member_id VARCHAR(20) NOT NULL,\n    book_id INT NOT NULL,\n    reservation_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    status ENUM('예약중', '예약완료', '예약취소', '예약만료') DEFAULT '예약중',\n    notification_sent BOOLEAN DEFAULT FALSE,\n    expiry_date DATETIME NULL,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    FOREIGN KEY (member_id) REFERENCES members(member_id),\n    FOREIGN KEY (book_id) REFERENCES books(book_id),\n    INDEX idx_member_id (member_id),\n    INDEX idx_book_id (book_id),\n    INDEX idx_status (status),\n    INDEX idx_reservation_date (reservation_date)\n);\n```\n```sql\nCREATE TABLE loan_history (\n    history_id INT AUTO_INCREMENT PRIMARY KEY,\n    loan_id INT NOT NULL,\n    action_type ENUM('대출', '반납', '연장', '연체알림', '분실신고') NOT NULL,\n    action_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    previous_due_date DATETIME NULL,\n    new_due_date DATETIME NULL,\n    notes TEXT,\n    processed_by VARCHAR(100),\n    FOREIGN KEY (loan_id) REFERENCES loans(loan_id),\n    INDEX idx_loan_id (loan_id),\n    INDEX idx_action_type (action_type),\n    INDEX idx_action_date (action_date)\n);\n```\n## Event\n\n```json\n{\n  \"name\": \"BookLoaned\",\n  \"displayName\": \"도서 대출됨\",\n  \"actor\": \"Member\",\n  \"level\": 4,\n  \"description\": \"회원이 도서 대출을 신청하고, 회원 인증 및 도서 상태 확인 후 대출이 승인됨. 대출 기간이 설정되고 도서 상태가 '대출중'으로 변경됨.\",\n  \"inputs\": [\n    \"회원번호\",\n    \"이름\",\n    \"도서 식별자\",\n    \"대출 기간(7/14/30일)\"\n  ],\n  \"outputs\": [\n    \"대출 정보\",\n    \"도서 상태: 대출중\"\n  ],\n  \"nextEvents\": [\n    \"BookStatusChanged\",\n    \"LoanHistoryRecorded\"\n  ]\n}\n```\n\n```json\n{\n  \"name\": \"BookReserved\",\n  \"displayName\": \"도서 예약됨\",\n  \"actor\": \"Member\",\n  \"level\": 5,\n  \"description\": \"회원이 대출 중인 도서에 대해 예약을 신청함. 예약이 완료되면 도서 상태가 '예약중'으로 변경됨.\",\n  \"inputs\": [\n    \"회원번호\",\n    \"도서 식별자\"\n  ],\n  \"outputs\": [\n    \"예약 정보\",\n    \"도서 상태: 예약중\"\n  ],\n  \"nextEvents\": [\n    \"BookStatusChanged\",\n    \"ReservationHistoryRecorded\"\n  ]\n}\n```\n\n```json\n{\n  \"name\": \"BookReturned\",\n  \"displayName\": \"도서 반납됨\",\n  \"actor\": \"Member\",\n  \"level\": 6,\n  \"description\": \"회원이 대출한 도서를 반납함. 반납 시 도서 상태가 '대출가능'으로 변경되고, 예약자가 있을 경우 '예약중'으로 변경됨.\",\n  \"inputs\": [\n    \"회원번호\",\n    \"도서 식별자\"\n  ],\n  \"outputs\": [\n    \"도서 상태: 대출가능 또는 예약중\",\n    \"반납 처리 정보\"\n  ],\n  \"nextEvents\": [\n    \"BookStatusChanged\",\n    \"LoanHistoryRecorded\"\n  ]\n}\n```\n\n```json\n{\n  \"name\": \"LoanExtended\",\n  \"displayName\": \"대출 연장됨\",\n  \"actor\": \"Member\",\n  \"level\": 7,\n  \"description\": \"회원이 대출 중인 도서의 대출 기간을 연장함. 연장 후 대출 정보와 반납 예정일이 갱신됨.\",\n  \"inputs\": [\n    \"회원번호\",\n    \"도서 식별자\",\n    \"연장 기간\"\n  ],\n  \"outputs\": [\n    \"갱신된 대출 정보\",\n    \"새 반납 예정일\"\n  ],\n  \"nextEvents\": [\n    \"LoanHistoryRecorded\"\n  ]\n}\n```\n\n## Context Relations\n\n### BookManagement-LoanAndReservation\n- **Type**: Pub/Sub\n- **Direction**: receives from 도서 관리 (BookManagement)\n- **Reason**: 도서 상태 변경(대출가능, 대출중, 예약중, 폐기 등)이 발생하면 대출/반납 및 예약 컨텍스트에서 이를 구독하여 대출/예약 프로세스에 반영한다.\n- **Interaction Pattern**: 도서 관리에서 도서 상태 변경 이벤트를 발행하면 대출/반납 및 예약 컨텍스트가 이를 구독하여 처리한다.\n\n### LoanAndReservation-LoanHistory\n- **Type**: Pub/Sub\n- **Direction**: sends to 이력 관리 (LoanHistory)\n- **Reason**: 대출, 반납, 연장, 예약 등 이벤트 발생 시 이력 관리 컨텍스트에서 해당 이벤트를 구독하여 이력을 기록한다.\n- **Interaction Pattern**: 대출/반납 및 예약에서 대출/반납/연장/예약 이벤트를 발행하면 이력 관리 컨텍스트가 이를 구독하여 이력 데이터를 생성한다.",
            "event": "{\n  \"name\": \"BookLoaned\",\n  \"displayName\": \"도서 대출됨\",\n  \"actor\": \"Member\",\n  \"level\": 4,\n  \"description\": \"회원이 도서 대출을 신청하고, 회원 인증 및 도서 상태 확인 후 대출이 승인됨. 대출 기간이 설정되고 도서 상태가 '대출중'으로 변경됨.\",\n  \"inputs\": [\n    \"회원번호\",\n    \"이름\",\n    \"도서 식별자\",\n    \"대출 기간(7/14/30일)\"\n  ],\n  \"outputs\": [\n    \"대출 정보\",\n    \"도서 상태: 대출중\"\n  ],\n  \"nextEvents\": [\n    \"BookStatusChanged\",\n    \"LoanHistoryRecorded\"\n  ],\n  \"refs\": [\n    [\n      [\n        5,\n        49\n      ],\n      [\n        5,\n        91\n      ]\n    ],\n    [\n      [\n        5,\n        59\n      ],\n      [\n        5,\n        77\n      ]\n    ],\n    [\n      [\n        5,\n        43\n      ],\n      [\n        5,\n        126\n      ]\n    ],\n    [\n      [\n        5,\n        198\n      ],\n      [\n        5,\n        235\n      ]\n    ]\n  ]\n}\n{\n  \"name\": \"BookReserved\",\n  \"displayName\": \"도서 예약됨\",\n  \"actor\": \"Member\",\n  \"level\": 5,\n  \"description\": \"회원이 대출 중인 도서에 대해 예약을 신청함. 예약이 완료되면 도서 상태가 '예약중'으로 변경됨.\",\n  \"inputs\": [\n    \"회원번호\",\n    \"도서 식별자\"\n  ],\n  \"outputs\": [\n    \"예약 정보\",\n    \"도서 상태: 예약중\"\n  ],\n  \"nextEvents\": [\n    \"BookStatusChanged\",\n    \"ReservationHistoryRecorded\"\n  ],\n  \"refs\": [\n    [\n      [\n        5,\n        183\n      ],\n      [\n        5,\n        193\n      ]\n    ],\n    [\n      [\n        7,\n        167\n      ],\n      [\n        7,\n        175\n      ]\n    ]\n  ]\n}\n{\n  \"name\": \"BookReturned\",\n  \"displayName\": \"도서 반납됨\",\n  \"actor\": \"Member\",\n  \"level\": 6,\n  \"description\": \"회원이 대출한 도서를 반납함. 반납 시 도서 상태가 '대출가능'으로 변경되고, 예약자가 있을 경우 '예약중'으로 변경됨.\",\n  \"inputs\": [\n    \"회원번호\",\n    \"도서 식별자\"\n  ],\n  \"outputs\": [\n    \"도서 상태: 대출가능 또는 예약중\",\n    \"반납 처리 정보\"\n  ],\n  \"nextEvents\": [\n    \"BookStatusChanged\",\n    \"LoanHistoryRecorded\"\n  ],\n  \"refs\": [\n    [\n      [\n        7,\n        133\n      ],\n      [\n        7,\n        167\n      ]\n    ],\n    [\n      [\n        7,\n        167\n      ],\n      [\n        7,\n        175\n      ]\n    ]\n  ]\n}\n{\n  \"name\": \"LoanExtended\",\n  \"displayName\": \"대출 연장됨\",\n  \"actor\": \"Member\",\n  \"level\": 7,\n  \"description\": \"회원이 대출 중인 도서의 대출 기간을 연장함. 연장 후 대출 정보와 반납 예정일이 갱신됨.\",\n  \"inputs\": [\n    \"회원번호\",\n    \"도서 식별자\",\n    \"연장 기간\"\n  ],\n  \"outputs\": [\n    \"갱신된 대출 정보\",\n    \"새 반납 예정일\"\n  ],\n  \"nextEvents\": [\n    \"LoanHistoryRecorded\"\n  ],\n  \"refs\": [\n    [\n      [\n        7,\n        109\n      ],\n      [\n        7,\n        124\n      ]\n    ]\n  ]\n}",
            "eventNames": "BookLoaned, BookReserved, BookReturned, LoanExtended 이벤트가 발생할 수 있어.",
            "userStory": "대출/반납을 통합적으로 관리하는\n대출/반납' 화면에서는 회원이 도서를 대출하고 반납하는 것을 관리할 수 있어야 해. 대출 신청 시에는 회원번호와 이름으로 회원을 확인하고, 대출할\n예약\n대출 현황 화면에서는 현재 대출 중인 도서들의 목록을 볼 수 있어야 해. 각 대출 건에 대해 대출일, 반납\n연장\n대출 이력과 상태"
        }
    },
    "description": "<1># Bounded Context Overview: LoanAndReservation (대출/반납 및 예약)</1>\n<2></2>\n<3>## Role</3>\n<4>회원의 도서 대출, 반납, 연장, 예약을 관리하고 도서 상태 변경을 트리거한다.</4>\n<5></5>\n<6>## Key Events</6>\n<7>- BookLoaned</7>\n<8>- BookReserved</8>\n<9>- BookReturned</9>\n<10>- LoanExtended</10>\n<11></11>\n<12># Requirements</12>\n<13></13>\n<14>## userStory</14>\n<15></15>\n<16>대출/반납을 통합적으로 관리하는</16>\n<17></17>\n<18>대출/반납' 화면에서는 회원이 도서를 대출하고 반납하는 것을 관리할 수 있어야 해. 대출 신청 시에는 회원번호와 이름으로 회원을 확인하고, 대출할</18>\n<19></19>\n<20>예약</20>\n<21></21>\n<22>대출 현황 화면에서는 현재 대출 중인 도서들의 목록을 볼 수 있어야 해. 각 대출 건에 대해 대출일, 반납</22>\n<23></23>\n<24>연장</24>\n<25></25>\n<26>대출 이력과 상태</26>\n<27></27>\n<28>## DDL</28>\n<29></29>\n<30>```sql</30>\n<31>CREATE TABLE loans (</31>\n<32>    loan_id INT AUTO_INCREMENT PRIMARY KEY,</32>\n<33>    member_id VARCHAR(20) NOT NULL,</33>\n<34>    book_id INT NOT NULL,</34>\n<35>    loan_date DATETIME DEFAULT CURRENT_TIMESTAMP,</35>\n<36>    due_date DATETIME NOT NULL,</36>\n<37>    return_date DATETIME NULL,</37>\n<38>    loan_period_days INT NOT NULL CHECK (loan_period_days IN (7, 14, 30)),</38>\n<39>    status ENUM('대출중', '연체', '반납완료', '연장') DEFAULT '대출중',</39>\n<40>    extension_count INT DEFAULT 0,</40>\n<41>    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,</41>\n<42>    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,</42>\n<43>    FOREIGN KEY (member_id) REFERENCES members(member_id),</43>\n<44>    FOREIGN KEY (book_id) REFERENCES books(book_id),</44>\n<45>    INDEX idx_member_id (member_id),</45>\n<46>    INDEX idx_book_id (book_id),</46>\n<47>    INDEX idx_status (status),</47>\n<48>    INDEX idx_due_date (due_date)</48>\n<49>);</49>\n<50>```</50>\n<51>```sql</51>\n<52>CREATE TABLE reservations (</52>\n<53>    reservation_id INT AUTO_INCREMENT PRIMARY KEY,</53>\n<54>    member_id VARCHAR(20) NOT NULL,</54>\n<55>    book_id INT NOT NULL,</55>\n<56>    reservation_date DATETIME DEFAULT CURRENT_TIMESTAMP,</56>\n<57>    status ENUM('예약중', '예약완료', '예약취소', '예약만료') DEFAULT '예약중',</57>\n<58>    notification_sent BOOLEAN DEFAULT FALSE,</58>\n<59>    expiry_date DATETIME NULL,</59>\n<60>    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,</60>\n<61>    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,</61>\n<62>    FOREIGN KEY (member_id) REFERENCES members(member_id),</62>\n<63>    FOREIGN KEY (book_id) REFERENCES books(book_id),</63>\n<64>    INDEX idx_member_id (member_id),</64>\n<65>    INDEX idx_book_id (book_id),</65>\n<66>    INDEX idx_status (status),</66>\n<67>    INDEX idx_reservation_date (reservation_date)</67>\n<68>);</68>\n<69>```</69>\n<70>```sql</70>\n<71>CREATE TABLE loan_history (</71>\n<72>    history_id INT AUTO_INCREMENT PRIMARY KEY,</72>\n<73>    loan_id INT NOT NULL,</73>\n<74>    action_type ENUM('대출', '반납', '연장', '연체알림', '분실신고') NOT NULL,</74>\n<75>    action_date DATETIME DEFAULT CURRENT_TIMESTAMP,</75>\n<76>    previous_due_date DATETIME NULL,</76>\n<77>    new_due_date DATETIME NULL,</77>\n<78>    notes TEXT,</78>\n<79>    processed_by VARCHAR(100),</79>\n<80>    FOREIGN KEY (loan_id) REFERENCES loans(loan_id),</80>\n<81>    INDEX idx_loan_id (loan_id),</81>\n<82>    INDEX idx_action_type (action_type),</82>\n<83>    INDEX idx_action_date (action_date)</83>\n<84>);</84>\n<85>```</85>\n<86>## Event</86>\n<87></87>\n<88>```json</88>\n<89>{</89>\n<90>  \"name\": \"BookLoaned\",</90>\n<91>  \"displayName\": \"도서 대출됨\",</91>\n<92>  \"actor\": \"Member\",</92>\n<93>  \"level\": 4,</93>\n<94>  \"description\": \"회원이 도서 대출을 신청하고, 회원 인증 및 도서 상태 확인 후 대출이 승인됨. 대출 기간이 설정되고 도서 상태가 '대출중'으로 변경됨.\",</94>\n<95>  \"inputs\": [</95>\n<96>    \"회원번호\",</96>\n<97>    \"이름\",</97>\n<98>    \"도서 식별자\",</98>\n<99>    \"대출 기간(7/14/30일)\"</99>\n<100>  ],</100>\n<101>  \"outputs\": [</101>\n<102>    \"대출 정보\",</102>\n<103>    \"도서 상태: 대출중\"</103>\n<104>  ],</104>\n<105>  \"nextEvents\": [</105>\n<106>    \"BookStatusChanged\",</106>\n<107>    \"LoanHistoryRecorded\"</107>\n<108>  ]</108>\n<109>}</109>\n<110>```</110>\n<111></111>\n<112>```json</112>\n<113>{</113>\n<114>  \"name\": \"BookReserved\",</114>\n<115>  \"displayName\": \"도서 예약됨\",</115>\n<116>  \"actor\": \"Member\",</116>\n<117>  \"level\": 5,</117>\n<118>  \"description\": \"회원이 대출 중인 도서에 대해 예약을 신청함. 예약이 완료되면 도서 상태가 '예약중'으로 변경됨.\",</118>\n<119>  \"inputs\": [</119>\n<120>    \"회원번호\",</120>\n<121>    \"도서 식별자\"</121>\n<122>  ],</122>\n<123>  \"outputs\": [</123>\n<124>    \"예약 정보\",</124>\n<125>    \"도서 상태: 예약중\"</125>\n<126>  ],</126>\n<127>  \"nextEvents\": [</127>\n<128>    \"BookStatusChanged\",</128>\n<129>    \"ReservationHistoryRecorded\"</129>\n<130>  ]</130>\n<131>}</131>\n<132>```</132>\n<133></133>\n<134>```json</134>\n<135>{</135>\n<136>  \"name\": \"BookReturned\",</136>\n<137>  \"displayName\": \"도서 반납됨\",</137>\n<138>  \"actor\": \"Member\",</138>\n<139>  \"level\": 6,</139>\n<140>  \"description\": \"회원이 대출한 도서를 반납함. 반납 시 도서 상태가 '대출가능'으로 변경되고, 예약자가 있을 경우 '예약중'으로 변경됨.\",</140>\n<141>  \"inputs\": [</141>\n<142>    \"회원번호\",</142>\n<143>    \"도서 식별자\"</143>\n<144>  ],</144>\n<145>  \"outputs\": [</145>\n<146>    \"도서 상태: 대출가능 또는 예약중\",</146>\n<147>    \"반납 처리 정보\"</147>\n<148>  ],</148>\n<149>  \"nextEvents\": [</149>\n<150>    \"BookStatusChanged\",</150>\n<151>    \"LoanHistoryRecorded\"</151>\n<152>  ]</152>\n<153>}</153>\n<154>```</154>\n<155></155>\n<156>```json</156>\n<157>{</157>\n<158>  \"name\": \"LoanExtended\",</158>\n<159>  \"displayName\": \"대출 연장됨\",</159>\n<160>  \"actor\": \"Member\",</160>\n<161>  \"level\": 7,</161>\n<162>  \"description\": \"회원이 대출 중인 도서의 대출 기간을 연장함. 연장 후 대출 정보와 반납 예정일이 갱신됨.\",</162>\n<163>  \"inputs\": [</163>\n<164>    \"회원번호\",</164>\n<165>    \"도서 식별자\",</165>\n<166>    \"연장 기간\"</166>\n<167>  ],</167>\n<168>  \"outputs\": [</168>\n<169>    \"갱신된 대출 정보\",</169>\n<170>    \"새 반납 예정일\"</170>\n<171>  ],</171>\n<172>  \"nextEvents\": [</172>\n<173>    \"LoanHistoryRecorded\"</173>\n<174>  ]</174>\n<175>}</175>\n<176>```</176>\n<177></177>\n<178>## Context Relations</178>\n<179></179>\n<180>### BookManagement-LoanAndReservation</180>\n<181>- **Type**: Pub/Sub</181>\n<182>- **Direction**: receives from 도서 관리 (BookManagement)</182>\n<183>- **Reason**: 도서 상태 변경(대출가능, 대출중, 예약중, 폐기 등)이 발생하면 대출/반납 및 예약 컨텍스트에서 이를 구독하여 대출/예약 프로세스에 반영한다.</183>\n<184>- **Interaction Pattern**: 도서 관리에서 도서 상태 변경 이벤트를 발행하면 대출/반납 및 예약 컨텍스트가 이를 구독하여 처리한다.</184>\n<185></185>\n<186>### LoanAndReservation-LoanHistory</186>\n<187>- **Type**: Pub/Sub</187>\n<188>- **Direction**: sends to 이력 관리 (LoanHistory)</188>\n<189>- **Reason**: 대출, 반납, 연장, 예약 등 이벤트 발생 시 이력 관리 컨텍스트에서 해당 이벤트를 구독하여 이력을 기록한다.</189>\n<190>- **Interaction Pattern**: 대출/반납 및 예약에서 대출/반납/연장/예약 이벤트를 발행하면 이력 관리 컨텍스트가 이를 구독하여 이력 데이터를 생성한다.</190>",
    "draftOption": [
        {
            "aggregate": {
                "alias": "대출",
                "name": "Loan"
            },
            "enumerations": [
                {
                    "alias": "대출 상태",
                    "name": "LoanStatus"
                }
            ],
            "valueObjects": []
        }
    ],
    "targetAggregate": {
        "alias": "대출",
        "name": "Loan"
    },
    "extractedDdlFields": [
        "loanId",
        "memberId",
        "bookId",
        "loanDate",
        "dueDate",
        "returnDate",
        "loanPeriodDays",
        "status",
        "extensionCount",
        "createdAt",
        "updatedAt",
        "historyId",
        "actionType",
        "actionDate",
        "previousDueDate",
        "newDueDate",
        "notes",
        "processedBy"
    ]
}