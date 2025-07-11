from ...graph import State
from ...models import InputsModel, UserInfoModel, InformationModel

input_state = State(
    inputs=InputsModel(
        selectedDraftOptions={
            "BookLoanProcess": {
                "boundedContext": {
                "aggregates": [
                    {
                    "alias": "대출",
                    "name": "Loan"
                    },
                    {
                    "alias": "예약",
                    "name": "Reservation"
                    },
                    {
                    "alias": "회원",
                    "name": "Member"
                    }
                ],
                "alias": "도서 대출 프로세스",
                "description": "# Requirements\n\n## userStory\n\n'대출/반납' 화면에서는 회원이 도서를 대출하고 반납하는 것을 관리할 수 있어야 해. 대출 신청 시에는 회원번호와 이름으로 회원을 확인하고, 대출할 도서를 선택해야 해. 도서는 도서명이나 ISBN으로 검색할 수 있어야 해. 대출 기간은 7일/14일/30일 중에서 선택할 수 있어. 만약 대출하려는 도서가 이미 대출 중이라면, 예약 신청이 가능해야 해. 대출이 완료되면 해당 도서의 상태는 자동으로 '대출중'으로 변경되어야 해.\n\n## userStory\n\n대출 현황 화면에서는 현재 대출 중인 도서들의 목록을 볼 수 있어야 해. 각 대출 건에 대해 대출일, 반납예정일, 현재 상태(대출중/연체/반납완료)를 확인할 수 있어야 하고, 대출 중인 도서는 연장이나 반납 처리가 가능해야 해. 도서가 반납되면 자동으로 해당 도서의 상태가 '대출가능'으로 변경되어야 해. 만약 예약자가 있는 도서가 반납되면, 해당 도서는 '예약중' 상태로 변경되어야 해.\n\n## userStory\n\n각 도서별로 대출 이력과 상태 변경 이력을 조회할 수 있어야 하고, 이를 통해 도서의 대출 현황과 상태 변화를 추적할 수 있어야 해.\n\n## Event\n\n{\"name\":\"MemberVerified\",\"displayName\":\"회원이 확인됨\",\"actor\":\"회원\",\"level\":5,\"description\":\"회원번호와 이름으로 회원 정보가 확인됨.\",\"inputs\":[\"회원번호\",\"이름\"],\"outputs\":[\"회원 정보\"],\"nextEvents\":[\"BookLoanRequested\"]}\n\n## Event\n\n{\"name\":\"BookLoanRequested\",\"displayName\":\"도서 대출이 신청됨\",\"actor\":\"회원\",\"level\":6,\"description\":\"회원이 대출하고자 하는 도서와 대출 기간(7일/14일/30일)을 선택하여 대출을 신청함.\",\"inputs\":[\"회원 정보\",\"도서 식별자\",\"대출 기간\"],\"outputs\":[\"대출 신청 요청\"],\"nextEvents\":[\"BookLoanApproved\",\"BookLoanRejected\"]}\n\n## Event\n\n{\"name\":\"BookLoanRejected\",\"displayName\":\"도서 대출이 거부됨\",\"actor\":\"도서 대출 시스템\",\"level\":7,\"description\":\"도서가 폐기되었거나 대출 불가 상태인 경우 대출이 거부됨.\",\"inputs\":[\"도서 상태 '폐기' 또는 대출 불가\"],\"outputs\":[\"대출 거부 알림\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookLoanApproved\",\"displayName\":\"도서 대출이 승인됨\",\"actor\":\"도서 대출 시스템\",\"level\":8,\"description\":\"도서가 대출 가능 상태라면 대출이 승인되고 대출 정보가 생성됨. 도서 상태는 '대출중'으로 변경됨.\",\"inputs\":[\"도서 상태 '대출가능'\",\"대출 신청 정보\"],\"outputs\":[\"대출 정보 생성\",\"도서 상태 '대출중'으로 변경\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookReserved\",\"displayName\":\"도서가 예약됨\",\"actor\":\"회원\",\"level\":9,\"description\":\"대출하려는 도서가 이미 대출 중일 때 회원이 해당 도서의 예약을 신청하면 예약이 생성되고, 도서의 상태가 '예약중'으로 변경됨.\",\"inputs\":[\"회원 정보\",\"대출 중인 도서 식별자\"],\"outputs\":[\"예약 정보 생성\",\"도서 상태 '예약중'으로 변경\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookReturned\",\"displayName\":\"도서가 반납됨\",\"actor\":\"회원\",\"level\":10,\"description\":\"회원이 대출한 도서를 반납함. 도서에 예약자가 있으면 상태가 '예약중'으로, 없으면 '대출가능'으로 변경됨.\",\"inputs\":[\"반납 도서 식별자\"],\"outputs\":[\"반납 처리\",\"도서 상태 변경\"],\"nextEvents\":[\"BookAvailable\",\"BookReservedForNext\"]}\n\n## Event\n\n{\"name\":\"BookAvailable\",\"displayName\":\"도서가 대출 가능 상태로 변경됨\",\"actor\":\"도서 대출 시스템\",\"level\":11,\"description\":\"반납된 도서에 예약자가 없는 경우 도서 상태가 '대출가능'으로 변경됨.\",\"inputs\":[\"반납 도서 식별자\",\"예약자 없음\"],\"outputs\":[\"도서 상태 '대출가능'\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookReservedForNext\",\"displayName\":\"도서가 다음 예약자를 위해 예약중 상태로 변경됨\",\"actor\":\"도서 대출 시스템\",\"level\":12,\"description\":\"반납된 도서에 예약자가 있을 경우 도서 상태가 '예약중'으로 변경됨.\",\"inputs\":[\"반납 도서 식별자\",\"예약자 존재\"],\"outputs\":[\"도서 상태 '예약중'\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"LoanExtended\",\"displayName\":\"대출 기간이 연장됨\",\"actor\":\"회원\",\"level\":13,\"description\":\"회원이 대출 중인 도서의 대출 기간을 연장함. 연체 상태에서는 연장이 불가함.\",\"inputs\":[\"회원 정보\",\"대출 중인 도서 식별자\",\"연장 요청\"],\"outputs\":[\"대출 기간 연장\",\"새 반납 예정일\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"LoanOverdue\",\"displayName\":\"도서 대출이 연체됨\",\"actor\":\"도서 대출 시스템\",\"level\":14,\"description\":\"반납 예정일이 지나도 도서가 반납되지 않은 경우, 대출 건의 상태가 '연체'로 변경됨.\",\"inputs\":[\"반납 예정일 경과\",\"반납 미처리\"],\"outputs\":[\"대출 상태 '연체'로 변경\"],\"nextEvents\":[]}\n\n\n## Context Relations\n\n### BookManagementToBookLoanProcess\n- **Type**: Pub/Sub\n- **Direction**: receives from 도서 관리 (BookManagement)\n- **Reason**: 도서의 상태 변화, 신규 등록, 폐기 등 이벤트가 발생하면 이를 대출/예약/연체 프로세스에 전달해야 하며, 두 컨텍스트가 느슨하게 결합되고 데이터 소유권이 명확히 분리됨.\n- **Interaction Pattern**: 도서 상태 변경, 신규 등록, 폐기 등 이벤트를 Pub/Sub로 발행하며 대출 프로세스에서 구독하여 반영함. 예: 도서가 폐기되면 대출 프로세스에서 대출 거부 처리.",
                "displayName": "도서 대출 프로세스",
                "name": "BookLoanProcess"
                },
                "cons": {
                "cohesion": "이력 관리, 상세 현황 등 부가 업무가 서비스 계층에 집중되어 코드 분산이 발생한다.",
                "complexity": "확장 시 부가 업무(이력, 상태변경 등) 도입을 위해 구조 변경 필요성이 생긴다.",
                "consistency": "복합 시나리오(대출→이력 동시 기록 등)에서 강한 일관성 보장이 어렵다.",
                "coupling": "이력·상태 추적이 외부 집계(BookLoanHistory, BookStatusHistory)에 의존해야 한다.",
                "encapsulation": "이력 및 상태 변경 규칙이 Loan 외부에 위치해 도메인 규칙이 분산될 수 있다.",
                "independence": "외부 이력 집계와의 연동이 반드시 필요해 완전 독립 운영은 어렵다.",
                "performance": "대출 및 예약 현황, 이력 동시 조회 시 성능 저하가 발생할 수 있다."
                },
                "description": "{\"userStories\":[{\"title\":\"도서 대출 및 반납 관리\",\"description\":\"회원은 '대출/반납' 화면에서 회원 확인 후 도서를 대출하거나 반납할 수 있다. 대출 시 도서명 또는 ISBN으로 검색, 대출 기간 선택, 이미 대출 중인 경우 예약 신청이 가능하다. 반납 시 도서 상태 및 예약자 유무에 따라 자동 상태 변경이 이루어진다.\",\"acceptance\":[\"회원번호와 이름으로 회원이 확인되어야 한다.\",\"도서명 또는 ISBN으로 도서를 검색할 수 있어야 한다.\",\"대출 기간은 7일/14일/30일 중 선택할 수 있다.\",\"이미 대출 중인 도서는 예약 신청이 가능하다.\",\"대출 완료 시 도서 상태가 자동으로 '대출중'으로 변경된다.\",\"반납 완료 시 예약자 유무에 따라 도서 상태가 '예약중' 또는 '대출가능'으로 변경된다.\"]},{\"title\":\"대출 현황 및 처리\",\"description\":\"대출 현황 화면에서는 현재 대출 중인 도서들의 목록, 대출일, 반납예정일, 상태(대출중/연체/반납완료)를 확인하고, 대출 중인 도서에 대해 연장 및 반납 처리가 가능하다.\",\"acceptance\":[\"대출 건별로 대출일, 반납예정일, 현재 상태를 확인할 수 있다.\",\"대출 중인 도서에 대해 연장 및 반납 처리가 가능하다.\",\"연체 상태에서는 연장이 불가하다.\"]},{\"title\":\"도서별 이력 및 상태 변경 추적\",\"description\":\"관리자는 각 도서별 대출 이력과 상태 변경 이력을 조회할 수 있어야 하며, 이를 통해 도서의 대출 현황과 상태 변화를 추적할 수 있다.\",\"acceptance\":[\"도서별로 모든 대출 이력과 상태 변경 이력을 볼 수 있다.\"]}],\"entities\":{\"Member\":{\"properties\":[{\"name\":\"memberId\",\"type\":\"String\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"name\",\"type\":\"String\",\"required\":true}]},\"Book\":{\"properties\":[{\"name\":\"bookId\",\"type\":\"String\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"title\",\"type\":\"String\",\"required\":true},{\"name\":\"isbn\",\"type\":\"String\",\"required\":true},{\"name\":\"status\",\"type\":\"enum\",\"required\":true,\"values\":[\"AVAILABLE\",\"ON_LOAN\",\"RESERVED\",\"DISCARDED\"]}]},\"Loan\":{\"properties\":[{\"name\":\"loanId\",\"type\":\"String\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"memberId\",\"type\":\"String\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Member\"},{\"name\":\"bookId\",\"type\":\"String\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Book\"},{\"name\":\"loanDate\",\"type\":\"Date\",\"required\":true},{\"name\":\"dueDate\",\"type\":\"Date\",\"required\":true},{\"name\":\"returnDate\",\"type\":\"Date\"},{\"name\":\"status\",\"type\":\"enum\",\"required\":true,\"values\":[\"ON_LOAN\",\"OVERDUE\",\"RETURNED\"]}]},\"Reservation\":{\"properties\":[{\"name\":\"reservationId\",\"type\":\"String\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"memberId\",\"type\":\"String\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Member\"},{\"name\":\"bookId\",\"type\":\"String\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Book\"},{\"name\":\"reservationDate\",\"type\":\"Date\",\"required\":true}]},\"BookStatusHistory\":{\"properties\":[{\"name\":\"historyId\",\"type\":\"String\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"bookId\",\"type\":\"String\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Book\"},{\"name\":\"beforeStatus\",\"type\":\"enum\",\"required\":true,\"values\":[\"AVAILABLE\",\"ON_LOAN\",\"RESERVED\",\"DISCARDED\"]},{\"name\":\"afterStatus\",\"type\":\"enum\",\"required\":true,\"values\":[\"AVAILABLE\",\"ON_LOAN\",\"RESERVED\",\"DISCARDED\"]},{\"name\":\"changedAt\",\"type\":\"Date\",\"required\":true}]}},\"businessRules\":[{\"name\":\"대출 기간 선택 제한\",\"description\":\"대출 기간은 7일, 14일, 30일만 선택할 수 있다.\"},{\"name\":\"연체 도서 연장 불가\",\"description\":\"연체 상태(OVERDUE)인 대출 건은 연장이 불가하다.\"},{\"name\":\"대출 상태 자동 변경\",\"description\":\"도서 대출 시 상태는 'ON_LOAN', 반납 시 예약자 없으면 'AVAILABLE', 예약자 있으면 'RESERVED'로 자동 변경된다.\"},{\"name\":\"폐기/대출 불가 도서 대출 거부\",\"description\":\"도서 상태가 'DISCARDED' 또는 대출 불가 시 대출이 거부된다.\"}],\"interfaces\":{\"LoanAndReturn\":{\"sections\":[{\"name\":\"회원 확인\",\"type\":\"form\",\"fields\":[{\"name\":\"memberId\",\"type\":\"text\",\"required\":true},{\"name\":\"name\",\"type\":\"text\",\"required\":true}],\"actions\":[\"회원 확인\"],\"filters\":[],\"resultTable\":{\"columns\":[],\"actions\":[]}},{\"name\":\"도서 대출 신청\",\"type\":\"form\",\"fields\":[{\"name\":\"bookSearch\",\"type\":\"text\",\"required\":true},{\"name\":\"searchType\",\"type\":\"select\",\"required\":true},{\"name\":\"loanPeriod\",\"type\":\"select\",\"required\":true}],\"actions\":[\"대출 신청\",\"예약 신청\"],\"filters\":[],\"resultTable\":{\"columns\":[],\"actions\":[]}},{\"name\":\"도서 반납\",\"type\":\"form\",\"fields\":[{\"name\":\"loanId\",\"type\":\"text\",\"required\":true}],\"actions\":[\"반납 처리\"],\"filters\":[],\"resultTable\":{\"columns\":[],\"actions\":[]}}]},\"LoanStatus\":{\"sections\":[{\"name\":\"대출 현황 목록\",\"type\":\"table\",\"fields\":[],\"actions\":[\"연장\",\"반납\"],\"filters\":[\"대출 상태\",\"대출일\",\"반납예정일\"],\"resultTable\":{\"columns\":[\"loanId\",\"bookId\",\"title\",\"loanDate\",\"dueDate\",\"status\"],\"actions\":[\"연장\",\"반납\"]}}]},\"BookHistory\":{\"sections\":[{\"name\":\"도서별 이력 조회\",\"type\":\"table\",\"fields\":[{\"name\":\"bookId\",\"type\":\"text\",\"required\":true}],\"actions\":[\"대출 이력 조회\",\"상태 변경 이력 조회\"],\"filters\":[],\"resultTable\":{\"columns\":[\"loanId\",\"memberId\",\"loanDate\",\"dueDate\",\"returnDate\",\"status\"],\"actions\":[]}},{\"name\":\"도서 상태 변경 이력\",\"type\":\"table\",\"fields\":[],\"actions\":[],\"filters\":[],\"resultTable\":{\"columns\":[\"historyId\",\"beforeStatus\",\"afterStatus\",\"changedAt\"],\"actions\":[]}}]}},\"events\":[{\"name\":\"MemberVerified\",\"description\":\"회원번호와 이름으로 회원 정보가 확인됨.\",\"displayName\":\"회원이 확인됨\"},{\"name\":\"BookLoanRequested\",\"description\":\"회원이 대출하고자 하는 도서와 대출 기간(7일/14일/30일)을 선택하여 대출을 신청함.\",\"displayName\":\"도서 대출이 신청됨\"},{\"name\":\"BookLoanRejected\",\"description\":\"도서가 폐기되었거나 대출 불가 상태인 경우 대출이 거부됨.\",\"displayName\":\"도서 대출이 거부됨\"},{\"name\":\"BookLoanApproved\",\"description\":\"도서가 대출 가능 상태라면 대출이 승인되고 대출 정보가 생성됨. 도서 상태는 '대출중'으로 변경됨.\",\"displayName\":\"도서 대출이 승인됨\"},{\"name\":\"BookReserved\",\"description\":\"대출하려는 도서가 이미 대출 중일 때 회원이 해당 도서의 예약을 신청하면 예약이 생성되고, 도서의 상태가 '예약중'으로 변경됨.\",\"displayName\":\"도서가 예약됨\"},{\"name\":\"BookReturned\",\"description\":\"회원이 대출한 도서를 반납함. 도서에 예약자가 있으면 상태가 '예약중'으로, 없으면 '대출가능'으로 변경됨.\",\"displayName\":\"도서가 반납됨\"},{\"name\":\"BookAvailable\",\"description\":\"반납된 도서에 예약자가 없는 경우 도서 상태가 '대출가능'으로 변경됨.\",\"displayName\":\"도서가 대출 가능 상태로 변경됨\"},{\"name\":\"BookReservedForNext\",\"description\":\"반납된 도서에 예약자가 있을 경우 도서 상태가 '예약중'으로 변경됨.\",\"displayName\":\"도서가 다음 예약자를 위해 예약중 상태로 변경됨\"},{\"name\":\"LoanExtended\",\"description\":\"회원이 대출 중인 도서의 대출 기간을 연장함. 연체 상태에서는 연장이 불가함.\",\"displayName\":\"대출 기간이 연장됨\"},{\"name\":\"LoanOverdue\",\"description\":\"반납 예정일이 지나도 도서가 반납되지 않은 경우, 대출 건의 상태가 '연체'로 변경됨.\",\"displayName\":\"도서 대출이 연체됨\"}],\"contextRelations\":[{\"name\":\"BookManagementToBookLoanProcess\",\"type\":\"Pub/Sub\",\"direction\":\"receives from\",\"targetContext\":\"도서 관리 (BookManagement)\",\"reason\":\"도서의 상태 변화, 신규 등록, 폐기 등 이벤트가 발생하면 이를 대출/예약/연체 프로세스에 전달해야 하며, 두 컨텍스트가 느슨하게 결합되고 데이터 소유권이 명확히 분리됨.\",\"interactionPattern\":\"도서 상태 변경, 신규 등록, 폐기 등 이벤트를 Pub/Sub로 발행하며 대출 프로세스에서 구독하여 반영함. 예: 도서가 폐기되면 대출 프로세스에서 대출 거부 처리.\"}]}",
                "isAIRecommended": False,
                "pros": {
                "cohesion": "핵심 대출·예약 업무에만 집중하여 집계 경계가 단순하다.",
                "complexity": "집계 수가 적어 전체 시스템 구조가 단순하며 이해와 유지보수가 쉽다.",
                "consistency": "대출·예약 관련 상태 변경이 집계 내에서 일관성 있게 처리된다.",
                "coupling": "Book, Member 등 외부 엔티티와의 참조만 유지하며 내부 결합도가 낮다.",
                "encapsulation": "도서 상태 자동 변경, 연체 연장 불가 등 핵심 규칙이 Loan 집계에 명확히 캡슐화된다.",
                "independence": "Loan, Reservation은 별도로 발전 가능하며, 서비스 규모가 작을 때 최적화된 형태다.",
                "performance": "불필요한 조인과 복잡한 트랜잭션이 최소화되어 빠른 응답이 가능하다."
                },
                "structure": [
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
                    "valueObjects": [
                    {
                        "alias": "도서 참조",
                        "name": "BookReference",
                        "referencedAggregate": {
                        "alias": "도서",
                        "name": "Book"
                        }
                    },
                    {
                        "alias": "회원",
                        "name": "Member"
                    }
                    ]
                },
                {
                    "aggregate": {
                    "alias": "예약",
                    "name": "Reservation"
                    },
                    "valueObjects": [
                    {
                        "alias": "도서 참조",
                        "name": "BookReference",
                        "referencedAggregate": {
                        "alias": "도서",
                        "name": "Book"
                        }
                    },
                    {
                        "alias": "회원",
                        "name": "Member"
                    }
                    ]
                }
                ]
            },
            "BookManagement": {
                "boundedContext": {
                "aggregates": [
                    {
                    "alias": "도서",
                    "name": "Book"
                    }
                ],
                "alias": "도서 관리",
                "description": "# Requirements\n\n## userStory\n\n'도서 관리' 화면에서는 새로운 도서를 등록하고 현재 보유한 도서들의 상태를 관리할 수 있어야 해. 도서 등록 시에는 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받아야 해. ISBN은 13자리 숫자여야 하고 중복 확인이 필요해. 카테고리는 소설/비소설/학술/잡지 중에서 선택할 수 있어야 해. 등록된 도서는 처음에 '대출가능' 상태가 되고, 이후 대출/반납 상황에 따라 '대출중', '예약중' 상태로 자동으로 변경되어야 해. 도서가 훼손되거나 분실된 경우 '폐기' 처리가 가능해야 하며, 폐기된 도서는 더 이상 대출이 불가능해야 해.\n\n## userStory\n\n도서는 도서명이나 ISBN으로 검색할 수 있어야 해.\n\n## userStory\n\n도서가 반납되면 자동으로 해당 도서의 상태가 '대출가능'으로 변경되어야 해. 만약 예약자가 있는 도서가 반납되면, 해당 도서는 '예약중' 상태로 변경되어야 해.\n\n## userStory\n\n각 도서별로 대출 이력과 상태 변경 이력을 조회할 수 있어야 하고, 이를 통해 도서의 대출 현황과 상태 변화를 추적할 수 있어야 해.\n\n## Event\n\n{\"name\":\"BookRegistered\",\"displayName\":\"도서가 등록됨\",\"actor\":\"도서 관리자\",\"level\":1,\"description\":\"도서 관리자가 새로운 도서를 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력하여 도서를 등록함. 등록된 도서는 '대출가능' 상태가 됨.\",\"inputs\":[\"도서명\",\"ISBN(13자리)\",\"저자\",\"출판사\",\"카테고리\",\"ISBN 중복 아님\"],\"outputs\":[\"신규 도서 데이터\",\"'대출가능' 상태\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookRegistrationFailed\",\"displayName\":\"도서 등록 실패됨\",\"actor\":\"도서 관리자\",\"level\":2,\"description\":\"도서 등록 시 ISBN이 13자리가 아니거나 중복된 경우 등록이 거부됨.\",\"inputs\":[\"ISBN(중복 또는 13자리 아님)\"],\"outputs\":[\"에러 메시지\",\"등록 거부\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookDiscarded\",\"displayName\":\"도서가 폐기됨\",\"actor\":\"도서 관리자\",\"level\":3,\"description\":\"도서가 훼손되거나 분실된 경우 도서 관리자가 해당 도서를 폐기 처리함. 폐기된 도서는 더 이상 대출이 불가함.\",\"inputs\":[\"도서 식별자\",\"폐기 사유\"],\"outputs\":[\"도서 상태 '폐기'로 변경\",\"대출 불가\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookSearched\",\"displayName\":\"도서가 검색됨\",\"actor\":\"회원\",\"level\":4,\"description\":\"회원이 도서명이나 ISBN으로 도서를 검색함.\",\"inputs\":[\"검색어(도서명 또는 ISBN)\"],\"outputs\":[\"검색 결과 도서 목록\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookLoanHistoryViewed\",\"displayName\":\"도서의 대출 이력이 조회됨\",\"actor\":\"도서 관리자\",\"level\":15,\"description\":\"도서 관리자가 특정 도서의 대출 이력을 조회함.\",\"inputs\":[\"도서 식별자\"],\"outputs\":[\"대출 이력 목록\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookStatusHistoryViewed\",\"displayName\":\"도서의 상태 변경 이력이 조회됨\",\"actor\":\"도서 관리자\",\"level\":16,\"description\":\"도서 관리자가 특정 도서의 상태 변경 이력을 조회함.\",\"inputs\":[\"도서 식별자\"],\"outputs\":[\"상태 변경 이력 목록\"],\"nextEvents\":[]}\n\n\n## Context Relations\n\n### BookManagementToBookLoanProcess\n- **Type**: Pub/Sub\n- **Direction**: sends to 도서 대출 프로세스 (BookLoanProcess)\n- **Reason**: 도서의 상태 변화, 신규 등록, 폐기 등 이벤트가 발생하면 이를 대출/예약/연체 프로세스에 전달해야 하며, 두 컨텍스트가 느슨하게 결합되고 데이터 소유권이 명확히 분리됨.\n- **Interaction Pattern**: 도서 상태 변경, 신규 등록, 폐기 등 이벤트를 Pub/Sub로 발행하며 대출 프로세스에서 구독하여 반영함. 예: 도서가 폐기되면 대출 프로세스에서 대출 거부 처리.",
                "displayName": "도서 관리",
                "name": "BookManagement"
                },
                "cons": {
                "cohesion": "이력 데이터가 계속 누적되면 Aggregate가 비대해져 단일 책임 원칙이 약화될 수 있다.",
                "complexity": "이력 데이터, 상태 등 다양한 관심사가 한 객체에 집중되어 복잡도가 누적된다.",
                "consistency": "대량 이력 데이터로 인한 트랜잭션 부하 및 충돌 가능성이 증가한다.",
                "coupling": "이력 데이터의 구조 변경이 Book 전체에 영향을 줄 수 있어 변화에 취약해진다.",
                "encapsulation": "외부 시스템에서 이력 정보만 분리 활용 시 도서 전체 구조를 알아야 한다.",
                "independence": "이력 처리, 조회만 확장하려면 Book 전체 구조를 함께 고려해야 한다.",
                "performance": "이력 데이터 증가 시 단일 Aggregate 조회/저장 성능 저하 우려가 있다."
                },
                "description": "{\"userStories\":[{\"title\":\"도서 등록 및 상태 관리\",\"description\":\"도서 관리자로서 새로운 도서를 등록하고, 보유 도서들의 상태(대출가능/대출중/예약중/폐기)를 관리할 수 있다.\",\"acceptance\":[\"도서명, ISBN(13자리), 저자, 출판사, 카테고리 입력이 필수이며, ISBN 중복 검사가 반드시 수행된다.\",\"도서 등록 시 상태는 '대출가능'이 기본값으로 설정된다.\",\"도서 상태는 대출/반납/예약/폐기 처리에 따라 자동으로 변경된다.\",\"폐기된 도서는 더 이상 대출이 불가하다.\"]},{\"title\":\"도서 검색\",\"description\":\"사용자로서 도서명이나 ISBN으로 도서를 검색할 수 있다.\",\"acceptance\":[\"검색어로 도서명 또는 ISBN 입력 시 관련 도서 목록이 출력된다.\"]},{\"title\":\"도서 반납 및 상태 전이\",\"description\":\"도서가 반납되면 해당 도서의 상태가 '대출가능' 또는 '예약중'으로 자동 전환된다.\",\"acceptance\":[\"예약자가 없으면 '대출가능', 예약자가 있으면 '예약중'으로 상태가 자동 변경된다.\"]},{\"title\":\"도서별 이력 조회\",\"description\":\"도서 관리자로서 각 도서별 대출 이력과 상태 변경 이력을 조회할 수 있다.\",\"acceptance\":[\"대출 이력과 상태 변경 이력이 조회 화면에 표시된다.\",\"이력에는 시점, 변경자, 변경 사유 등이 포함된다.\"]}],\"entities\":{\"Book\":{\"properties\":[{\"name\":\"bookId\",\"type\":\"Long\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"title\",\"type\":\"String\",\"required\":true},{\"name\":\"ISBN\",\"type\":\"String\",\"required\":true},{\"name\":\"author\",\"type\":\"String\",\"required\":true},{\"name\":\"publisher\",\"type\":\"String\",\"required\":true},{\"name\":\"category\",\"type\":\"enum\",\"required\":true,\"values\":[\"소설\",\"비소설\",\"학술\",\"잡지\"]},{\"name\":\"status\",\"type\":\"enum\",\"required\":true,\"values\":[\"대출가능\",\"대출중\",\"예약중\",\"폐기\"]}]},\"BookLoanHistory\":{\"properties\":[{\"name\":\"historyId\",\"type\":\"Long\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"bookId\",\"type\":\"Long\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Book\"},{\"name\":\"loanedBy\",\"type\":\"String\",\"required\":true},{\"name\":\"loanDate\",\"type\":\"Date\",\"required\":true},{\"name\":\"returnDate\",\"type\":\"Date\"}]},\"BookStatusHistory\":{\"properties\":[{\"name\":\"statusHistoryId\",\"type\":\"Long\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"bookId\",\"type\":\"Long\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Book\"},{\"name\":\"status\",\"type\":\"enum\",\"required\":true,\"values\":[\"대출가능\",\"대출중\",\"예약중\",\"폐기\"]},{\"name\":\"changedAt\",\"type\":\"Date\",\"required\":true},{\"name\":\"changedBy\",\"type\":\"String\",\"required\":true},{\"name\":\"reason\",\"type\":\"String\"}]}},\"businessRules\":[{\"name\":\"ISBN_Validation\",\"description\":\"ISBN은 반드시 13자리의 숫자여야 하며, 시스템 내에서 유일해야 한다.\"},{\"name\":\"BookStatus_AutoTransition\",\"description\":\"도서는 등록 시 '대출가능' 상태로 시작하며, 대출/반납/예약/폐기 상황에 따라 상태가 자동으로 변경된다.\"},{\"name\":\"BookDiscard_Restriction\",\"description\":\"폐기된 도서는 더 이상 대출이 불가하다.\"},{\"name\":\"ReturnStatusTransition\",\"description\":\"도서 반납 시 예약자가 없으면 '대출가능', 예약자가 있으면 '예약중' 상태로 자동 변경된다.\"}],\"interfaces\":{\"BookManagement\":{\"sections\":[{\"name\":\"도서 등록\",\"type\":\"form\",\"fields\":[{\"name\":\"title\",\"type\":\"text\",\"required\":true},{\"name\":\"ISBN\",\"type\":\"text\",\"required\":true},{\"name\":\"author\",\"type\":\"text\",\"required\":true},{\"name\":\"publisher\",\"type\":\"text\",\"required\":true},{\"name\":\"category\",\"type\":\"select\",\"required\":true}],\"actions\":[\"등록\",\"중복확인\"],\"filters\":[],\"resultTable\":{\"columns\":[],\"actions\":[]}},{\"name\":\"도서 목록\",\"type\":\"table\",\"fields\":[],\"actions\":[\"상세보기\",\"폐기처리\"],\"filters\":[\"title\",\"ISBN\",\"category\",\"status\"],\"resultTable\":{\"columns\":[\"bookId\",\"title\",\"ISBN\",\"author\",\"publisher\",\"category\",\"status\"],\"actions\":[\"상세보기\",\"폐기처리\"]}}]},\"BookDetail\":{\"sections\":[{\"name\":\"대출 이력\",\"type\":\"table\",\"fields\":[],\"actions\":[],\"filters\":[],\"resultTable\":{\"columns\":[\"loanedBy\",\"loanDate\",\"returnDate\"],\"actions\":[]}},{\"name\":\"상태 변경 이력\",\"type\":\"table\",\"fields\":[],\"actions\":[],\"filters\":[],\"resultTable\":{\"columns\":[\"status\",\"changedAt\",\"changedBy\",\"reason\"],\"actions\":[]}}]}},\"events\":[{\"name\":\"BookRegistered\",\"description\":\"도서 관리자가 새로운 도서를 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력하여 도서를 등록함. 등록된 도서는 '대출가능' 상태가 됨.\",\"displayName\":\"도서가 등록됨\"},{\"name\":\"BookRegistrationFailed\",\"description\":\"도서 등록 시 ISBN이 13자리가 아니거나 중복된 경우 등록이 거부됨.\",\"displayName\":\"도서 등록 실패됨\"},{\"name\":\"BookDiscarded\",\"description\":\"도서가 훼손되거나 분실된 경우 도서 관리자가 해당 도서를 폐기 처리함. 폐기된 도서는 더 이상 대출이 불가함.\",\"displayName\":\"도서가 폐기됨\"},{\"name\":\"BookSearched\",\"description\":\"회원이 도서명이나 ISBN으로 도서를 검색함.\",\"displayName\":\"도서가 검색됨\"},{\"name\":\"BookLoanHistoryViewed\",\"description\":\"도서 관리자가 특정 도서의 대출 이력을 조회함.\",\"displayName\":\"도서의 대출 이력이 조회됨\"},{\"name\":\"BookStatusHistoryViewed\",\"description\":\"도서 관리자가 특정 도서의 상태 변경 이력을 조회함.\",\"displayName\":\"도서의 상태 변경 이력이 조회됨\"}],\"contextRelations\":[{\"name\":\"BookManagementToBookLoanProcess\",\"type\":\"Pub/Sub\",\"direction\":\"sends to\",\"targetContext\":\"BookLoanProcess\",\"reason\":\"도서의 상태 변화, 신규 등록, 폐기 등 이벤트가 발생하면 이를 대출/예약/연체 프로세스에 전달해야 하며, 두 컨텍스트가 느슨하게 결합되고 데이터 소유권이 명확히 분리됨.\",\"interactionPattern\":\"도서 상태 변경, 신규 등록, 폐기 등 이벤트를 Pub/Sub로 발행하며 대출 프로세스에서 구독하여 반영함. 예: 도서가 폐기되면 대출 프로세스에서 대출 거부 처리.\"}]}",
                "isAIRecommended": False,
                "pros": {
                "cohesion": "도서의 핵심 정보와 이력 데이터, 상태 전이를 한 Aggregate 내에서 일관성 있게 관리하여 비즈니스 규칙을 강하게 보장한다.",
                "complexity": "이력까지 모두 한 곳에서 관리되어 구현 및 유지보수가 직관적이다.",
                "consistency": "ISBN 유일성, 상태 전이 등 도서 중심의 모든 비즈니스 불변성이 단일 트랜잭션에서 강하게 보장된다.",
                "coupling": "도서 관련 작업이 한 Aggregate 내에서 해결되므로 외부 참조와 Aggregate 간 결합이 최소화된다.",
                "encapsulation": "도서의 등록, 폐기, 상태 전이, 이력 관리까지 내부에서 처리되어 외부에 복잡성을 노출하지 않는다.",
                "independence": "Book Aggregate만으로 도서 업무의 대부분이 독립적으로 처리된다.",
                "performance": "도서와 연관된 이력/상태 조회가 단일 Aggregate 조회로 효율적이다."
                },
                "structure": [
                {
                    "aggregate": {
                    "alias": "도서",
                    "name": "Book"
                    },
                    "enumerations": [
                    {
                        "alias": "도서 카테고리",
                        "name": "BookCategory"
                    },
                    {
                        "alias": "도서 상태",
                        "name": "BookStatus"
                    }
                    ],
                    "valueObjects": [
                    {
                        "alias": "도서 대출 이력 정보",
                        "name": "BookLoanHistoryInfo",
                        "referencedAggregate": {
                        "alias": "대출",
                        "name": "Loan"
                        }
                    },
                    {
                        "alias": "도서 상태 변경 이력 정보",
                        "name": "BookStatusHistoryInfo"
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
        jobId="ce37f9ce-8f9d-4c6f-33a6-71b9dbe7c6bb"
    )
)

