from .....models import *

create_element_names_by_drafts_inputs = {
    "previousElementNames": {
        "BookManagement": {
            "Book": ExtractedElementNameDetail(
                command_names=[
                    "CreateBook",
                    "EditBook",
                    "UpdateBookStatus",
                    "DisposeBook",
                    "ValidateBookIsbn"
                ],
                event_names=[
                    "BookRegistered",
                    "BookEdited",
                    "BookStatusChanged",
                    "BookDisposed",
                    "BookIsbnValidated"
                ],
                read_model_names=[
                    "BookList",
                    "BookStatusChangeHistory"
                ]
            )
        }
    },
    "targetBoundedContextName": "LoanAndReservation",
    "aggregateDraft": [
        {
            "alias": "대출",
            "name": "Loan"
        },
        {
            "alias": "예약",
            "name": "Reservation"
        }
    ],
    "description": "# Bounded Context Overview: LoanAndReservation (대출/반납 및 예약)\n\n## Role\n회원의 도서 대출, 반납, 연장, 예약을 관리하고 도서 상태 변경을 트리거한다.\n\n## Key Events\n- BookLoaned\n- BookReserved\n- BookReturned\n- LoanExtended\n\n# Requirements\n\n## userStory\n\n대출/반납을 통합적으로 관리하는\n\n대출/반납' 화면에서는 회원이 도서를 대출하고 반납하는 것을 관리할 수 있어야 해. 대출 신청 시에는 회원번호와 이름으로 회원을 확인하고, 대출할\n\n예약\n\n대출 현황 화면에서는 현재 대출 중인 도서들의 목록을 볼 수 있어야 해. 각 대출 건에 대해 대출일, 반납\n\n연장\n\n대출 이력과 상태\n\n## DDL\n\n```sql\nCREATE TABLE loans (\n    loan_id INT AUTO_INCREMENT PRIMARY KEY,\n    member_id VARCHAR(20) NOT NULL,\n    book_id INT NOT NULL,\n    loan_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    due_date DATETIME NOT NULL,\n    return_date DATETIME NULL,\n    loan_period_days INT NOT NULL CHECK (loan_period_days IN (7, 14, 30)),\n    status ENUM('대출중', '연체', '반납완료', '연장') DEFAULT '대출중',\n    extension_count INT DEFAULT 0,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    FOREIGN KEY (member_id) REFERENCES members(member_id),\n    FOREIGN KEY (book_id) REFERENCES books(book_id),\n    INDEX idx_member_id (member_id),\n    INDEX idx_book_id (book_id),\n    INDEX idx_status (status),\n    INDEX idx_due_date (due_date)\n);\n```\n```sql\nCREATE TABLE reservations (\n    reservation_id INT AUTO_INCREMENT PRIMARY KEY,\n    member_id VARCHAR(20) NOT NULL,\n    book_id INT NOT NULL,\n    reservation_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    status ENUM('예약중', '예약완료', '예약취소', '예약만료') DEFAULT '예약중',\n    notification_sent BOOLEAN DEFAULT FALSE,\n    expiry_date DATETIME NULL,\n    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    FOREIGN KEY (member_id) REFERENCES members(member_id),\n    FOREIGN KEY (book_id) REFERENCES books(book_id),\n    INDEX idx_member_id (member_id),\n    INDEX idx_book_id (book_id),\n    INDEX idx_status (status),\n    INDEX idx_reservation_date (reservation_date)\n);\n```\n```sql\nCREATE TABLE loan_history (\n    history_id INT AUTO_INCREMENT PRIMARY KEY,\n    loan_id INT NOT NULL,\n    action_type ENUM('대출', '반납', '연장', '연체알림', '분실신고') NOT NULL,\n    action_date DATETIME DEFAULT CURRENT_TIMESTAMP,\n    previous_due_date DATETIME NULL,\n    new_due_date DATETIME NULL,\n    notes TEXT,\n    processed_by VARCHAR(100),\n    FOREIGN KEY (loan_id) REFERENCES loans(loan_id),\n    INDEX idx_loan_id (loan_id),\n    INDEX idx_action_type (action_type),\n    INDEX idx_action_date (action_date)\n);\n```\n## Event\n\n```json\n{\n  \"name\": \"BookLoaned\",\n  \"displayName\": \"도서 대출됨\",\n  \"actor\": \"Member\",\n  \"level\": 4,\n  \"description\": \"회원이 도서 대출을 신청하고, 회원 인증 및 도서 상태 확인 후 대출이 승인됨. 대출 기간이 설정되고 도서 상태가 '대출중'으로 변경됨.\",\n  \"inputs\": [\n    \"회원번호\",\n    \"이름\",\n    \"도서 식별자\",\n    \"대출 기간(7/14/30일)\"\n  ],\n  \"outputs\": [\n    \"대출 정보\",\n    \"도서 상태: 대출중\"\n  ],\n  \"nextEvents\": [\n    \"BookStatusChanged\",\n    \"LoanHistoryRecorded\"\n  ]\n}\n```\n\n```json\n{\n  \"name\": \"BookReserved\",\n  \"displayName\": \"도서 예약됨\",\n  \"actor\": \"Member\",\n  \"level\": 5,\n  \"description\": \"회원이 대출 중인 도서에 대해 예약을 신청함. 예약이 완료되면 도서 상태가 '예약중'으로 변경됨.\",\n  \"inputs\": [\n    \"회원번호\",\n    \"도서 식별자\"\n  ],\n  \"outputs\": [\n    \"예약 정보\",\n    \"도서 상태: 예약중\"\n  ],\n  \"nextEvents\": [\n    \"BookStatusChanged\",\n    \"ReservationHistoryRecorded\"\n  ]\n}\n```\n\n```json\n{\n  \"name\": \"BookReturned\",\n  \"displayName\": \"도서 반납됨\",\n  \"actor\": \"Member\",\n  \"level\": 6,\n  \"description\": \"회원이 대출한 도서를 반납함. 반납 시 도서 상태가 '대출가능'으로 변경되고, 예약자가 있을 경우 '예약중'으로 변경됨.\",\n  \"inputs\": [\n    \"회원번호\",\n    \"도서 식별자\"\n  ],\n  \"outputs\": [\n    \"도서 상태: 대출가능 또는 예약중\",\n    \"반납 처리 정보\"\n  ],\n  \"nextEvents\": [\n    \"BookStatusChanged\",\n    \"LoanHistoryRecorded\"\n  ]\n}\n```\n\n```json\n{\n  \"name\": \"LoanExtended\",\n  \"displayName\": \"대출 연장됨\",\n  \"actor\": \"Member\",\n  \"level\": 7,\n  \"description\": \"회원이 대출 중인 도서의 대출 기간을 연장함. 연장 후 대출 정보와 반납 예정일이 갱신됨.\",\n  \"inputs\": [\n    \"회원번호\",\n    \"도서 식별자\",\n    \"연장 기간\"\n  ],\n  \"outputs\": [\n    \"갱신된 대출 정보\",\n    \"새 반납 예정일\"\n  ],\n  \"nextEvents\": [\n    \"LoanHistoryRecorded\"\n  ]\n}\n```\n\n## Context Relations\n\n### BookManagement-LoanAndReservation\n- **Type**: Pub/Sub\n- **Direction**: receives from 도서 관리 (BookManagement)\n- **Reason**: 도서 상태 변경(대출가능, 대출중, 예약중, 폐기 등)이 발생하면 대출/반납 및 예약 컨텍스트에서 이를 구독하여 대출/예약 프로세스에 반영한다.\n- **Interaction Pattern**: 도서 관리에서 도서 상태 변경 이벤트를 발행하면 대출/반납 및 예약 컨텍스트가 이를 구독하여 처리한다.\n\n### LoanAndReservation-LoanHistory\n- **Type**: Pub/Sub\n- **Direction**: sends to 이력 관리 (LoanHistory)\n- **Reason**: 대출, 반납, 연장, 예약 등 이벤트 발생 시 이력 관리 컨텍스트에서 해당 이벤트를 구독하여 이력을 기록한다.\n- **Interaction Pattern**: 대출/반납 및 예약에서 대출/반납/연장/예약 이벤트를 발행하면 이력 관리 컨텍스트가 이를 구독하여 이력 데이터를 생성한다.",
    "siteMap": [],
    "requestedEventNames": [
        "BookLoaned",
        "BookReserved",
        "BookReturned",
        "LoanExtended"
    ],
    "requestedCommandNames": [],
    "requestedReadModelNames": []
}