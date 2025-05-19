from ....models import State, InputsModel, OutputsModel, UserInfoModel, InformationModel, EsValueModel, SubgraphsModel, CreateAggregateByFunctionsModel, CreateAggregateClassIdByDraftsModel, CreateCommandActionsByFunctionModel, CreatePolicyActionsByFunctionModel

create_policy_actions_by_function_sub_graph_inputs = State(
    inputs=InputsModel(
        selectedDraftOptions={
            "LibraryBookLoan": {
                "structure": [
                    {
                        "aggregate": {
                            "name": "Book",
                            "alias": "도서"
                        },
                        "enumerations": [
                            {
                                "name": "BookStatus",
                                "alias": "도서상태"
                            },
                            {
                                "name": "BookCategory",
                                "alias": "도서카테고리"
                            }
                        ],
                        "valueObjects": [
                            {
                                "name": "LoanHistoryReference",
                                "alias": "대출이력참조",
                                "referencedAggregate": {
                                    "name": "LoanHistory",
                                    "alias": "대출이력"
                                }
                            },
                            {
                                "name": "BookStatusHistoryReference",
                                "alias": "상태변경이력참조",
                                "referencedAggregate": {
                                    "name": "BookStatusHistory",
                                    "alias": "도서상태변경이력"
                                }
                            }
                        ]
                    }
                ],
                "pros": {
                    "cohesion": "도서에 관한 모든 속성과 상태 및 이력 관리까지 Book Aggregate에 통합되어, 도서 관점의 모든 비즈니스 규칙을 한 곳에서 강하게 보장할 수 있습니다.",
                    "coupling": "외부 참조가 최소화되어, 도서 단위의 변경이 타 도메인에 미치는 영향이 매우 적고, 도서 관련 변경이 Aggregate 내부에서만 일어납니다.",
                    "consistency": "도서 상태, 등록, 폐기, 대출 가능 여부 등 모든 도메인 불변성이 한 트랜잭션 내에서 완벽하게 보장됩니다.",
                    "encapsulation": "도서 상태 변경, 이력 기록 등 모든 도메인 규칙이 외부에서 직접 접근 불가하며, Aggregate 내부에서만 조작됩니다.",
                    "complexity": "단일 Aggregate이므로 이해와 접근이 직관적이며, 복잡한 관계를 신경 쓸 필요 없이 도서 중심으로 개발이 가능합니다.",
                    "independence": "도서 단위로 독립적인 확장과 유지보수가 가능해, 시스템 진화에 매우 유리합니다.",
                    "performance": "도서 기준의 조회 및 관리에 있어 쿼리 효율성이 극대화되어, 다수의 도서 정보를 빠르게 처리할 수 있습니다."
                },
                "cons": {
                    "cohesion": "대출, 예약 등 도서 외 세부 행위까지 Book Aggregate에 모두 통합하면, 점차 책임 범위가 확장되어 SRP(단일 책임 원칙)가 약화될 수 있습니다.",
                    "coupling": "대출, 예약 등 타 도메인 비즈니스 변화가 도서 Aggregate 구조에 직접적인 영향을 미쳐 Aggregate 크기가 커질 위험이 있습니다.",
                    "consistency": "다수 사용자의 대출, 예약 등 도서 관련 이벤트가 몰릴 경우 동시성 문제나 잠금 이슈가 발생할 수 있습니다.",
                    "encapsulation": "비즈니스가 발전하면서 도서와 관련 없는 세부 규칙까지 이 Aggregate에서 관리하게 되면, 도메인 캡슐화가 흐려질 수 있습니다.",
                    "complexity": "도서 Aggregate 내부에 너무 많은 도메인 규칙이 쏠리면 복잡도가 상승하여 유지보수 비용이 커질 수 있습니다.",
                    "independence": "Book이 모든 책임을 가지면 도서의 변경이 전체 시스템에 ripple effect를 줄 수 있습니다.",
                    "performance": "대규모 대출/예약/상태 변경이 한 Aggregate에 집중되면, 처리 성능 저하 및 병목이 발생할 수 있습니다."
                },
                "isAIRecommended": False,
                "boundedContext": {
                    "_type": "org.uengine.modeling.model.BoundedContext",
                    "aggregates": [
                        {
                            "id": "8e794426-f189-4559-8e36-0a8b457c3db9"
                        }
                    ],
                    "author": "My-UID",
                    "description": "# Requirements\n\n## userStory\n\n도서관의 도서 관리와 대출/반납을 통합적으로 관리하는 화면을 만들려고 해.\n\n## userStory\n\n'도서 관리' 화면에서는 새로운 도서를 등록하고 현재 보유한 도서들의 상태를 관리할 수 있어야 해. 도서 등록 시에는 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받아야 해. ISBN은 13자리 숫자여야 하고 중복 확인이 필요해. 카테고리는 소설/비소설/학술/잡지 중에서 선택할 수 있어야 해. 등록된 도서는 처음에 '대출가능' 상태가 되고, 이후 대출/반납 상황에 따라 '대출중', '예약중' 상태로 자동으로 변경되어야 해. 도서가 훼손되거나 분실된 경우 '폐기' 처리가 가능해야 하며, 폐기된 도서는 더 이상 대출이 불가능해야 해.\n\n## userStory\n\n'대출/반납' 화면에서는 회원이 도서를 대출하고 반납하는 것을 관리할 수 있어야 해. 대출 신청 시에는 회원번호와 이름으로 회원을 확인하고, 대출할 도서를 선택해야 해. 도서는 도서명이나 ISBN으로 검색할 수 있어야 해. 대출 기간은 7일/14일/30일 중에서 선택할 수 있어. 만약 대출하려는 도서가 이미 대출 중이라면, 예약 신청이 가능해야 해. 대출이 완료되면 해당 도서의 상태는 자동으로 '대출중'으로 변경되어야 해.\n\n## userStory\n\n대출 현황 화면에서는 현재 대출 중인 도서들의 목록을 볼 수 있어야 해. 각 대출 건에 대해 대출일, 반납예정일, 현재 상태(대출중/연체/반납완료)를 확인할 수 있어야 하고, 대출 중인 도서는 연장이나 반납 처리가 가능해야 해. 도서가 반납되면 자동으로 해당 도서의 상태가 '대출가능'으로 변경되어야 해. 만약 예약자가 있는 도서가 반납되면, 해당 도서는 '예약중' 상태로 변경되어야 해.\n\n## userStory\n\n각 도서별로 대출 이력과 상태 변경 이력을 조회할 수 있어야 하고, 이를 통해 도서의 대출 현황과 상태 변화를 추적할 수 있어야 해.\n\n## Event\n\n{\"name\":\"BookRegistered\",\"displayName\":\"도서가 등록됨\",\"actor\":\"Librarian\",\"level\":1,\"description\":\"사서가 도서명, ISBN, 저자, 출판사, 카테고리를 입력하여 신규 도서를 등록함. ISBN 중복 및 형식(13자리 숫자) 검증을 거침.\",\"inputs\":[\"도서명\",\"ISBN(13자리)\",\"저자\",\"출판사\",\"카테고리(소설/비소설/학술/잡지)\",\"ISBN 중복 아님\",\"ISBN 형식 유효\"],\"outputs\":[\"신규 도서 등록\",\"도서 상태: 대출가능\"],\"nextEvents\":[\"BookStateChanged\"]}\n\n## Event\n\n{\"name\":\"BookRegistrationFailedDueToDuplicateISBN\",\"displayName\":\"ISBN 중복으로 도서 등록 실패함\",\"actor\":\"Librarian\",\"level\":1,\"description\":\"도서 등록 시 입력한 ISBN이 기존에 이미 존재할 경우, 도서 등록이 실패함.\",\"inputs\":[\"ISBN(13자리)\",\"기존 도서에 동일 ISBN 존재\"],\"outputs\":[\"도서 등록 실패 알림\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookRegistrationFailedDueToInvalidISBNFormat\",\"displayName\":\"ISBN 형식 오류로 도서 등록 실패함\",\"actor\":\"Librarian\",\"level\":1,\"description\":\"도서 등록 시 입력한 ISBN이 13자리 숫자 형식이 아닐 경우, 도서 등록이 실패함.\",\"inputs\":[\"ISBN(13자리 아님)\"],\"outputs\":[\"도서 등록 실패 알림\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookStateChanged\",\"displayName\":\"도서 상태가 변경됨\",\"actor\":\"System\",\"level\":2,\"description\":\"도서의 상태가 비즈니스 프로세스(등록, 대출, 반납, 예약, 폐기)에 따라 변경됨.\",\"inputs\":[\"도서 ID\",\"변경 사유(등록, 대출, 반납, 예약, 폐기 등)\"],\"outputs\":[\"도서 상태 변경(대출가능/대출중/예약중/폐기)\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookDisposed\",\"displayName\":\"도서가 폐기됨\",\"actor\":\"Librarian\",\"level\":3,\"description\":\"사서가 도서가 훼손되거나 분실되었음을 확인하고 해당 도서를 폐기 처리함.\",\"inputs\":[\"도서 ID\",\"폐기 사유(훼손, 분실 등)\"],\"outputs\":[\"도서 상태: 폐기\",\"해당 도서 대출 불가\"],\"nextEvents\":[\"BookStateChanged\"]}\n\n## Event\n\n{\"name\":\"BookBorrowed\",\"displayName\":\"도서가 대출됨\",\"actor\":\"Member\",\"level\":4,\"description\":\"회원이 회원번호와 이름으로 인증 후 도서명 또는 ISBN으로 도서를 검색하여 대출 기간을 선택하고 대출 신청을 완료함.\",\"inputs\":[\"회원번호\",\"회원명\",\"도서 ID\",\"대출 기간(7/14/30일)\",\"도서 상태: 대출가능\"],\"outputs\":[\"도서 대출 기록 생성\",\"도서 상태: 대출중\"],\"nextEvents\":[\"BookStateChanged\",\"LoanHistoryRecorded\"]}\n\n## Event\n\n{\"name\":\"BookBorrowFailedDueToUnavailableBook\",\"displayName\":\"도서 대출 불가로 대출 실패함\",\"actor\":\"Member\",\"level\":4,\"description\":\"회원이 대출을 시도했으나 해당 도서가 이미 대출 중이어서 대출이 실패함.\",\"inputs\":[\"도서 ID\",\"도서 상태: 대출중/폐기\"],\"outputs\":[\"도서 대출 실패 알림\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookReserved\",\"displayName\":\"도서가 예약됨\",\"actor\":\"Member\",\"level\":5,\"description\":\"회원이 대출 중인 도서를 예약함. 예약자 정보와 예약 일시가 저장됨.\",\"inputs\":[\"회원번호\",\"회원명\",\"도서 ID\",\"도서 상태: 대출중\"],\"outputs\":[\"도서 예약 기록 생성\",\"도서 상태: 예약중(반납 시 자동 전환)\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookReturned\",\"displayName\":\"도서가 반납됨\",\"actor\":\"Member\",\"level\":6,\"description\":\"회원이 대출 중이던 도서를 반납함. 반납일이 기록되고 도서의 상태가 변경됨.\",\"inputs\":[\"회원번호\",\"도서 ID\",\"대출 기록\"],\"outputs\":[\"반납일 기록\",\"도서 상태: 대출가능(예약자 없을 시) 또는 예약중(예약자 있을 시)\"],\"nextEvents\":[\"BookStateChanged\",\"LoanHistoryRecorded\"]}\n\n## Event\n\n{\"name\":\"BookReturnOverdue\",\"displayName\":\"도서가 연체되어 반납됨\",\"actor\":\"Member\",\"level\":7,\"description\":\"회원이 반납 예정일을 초과하여 도서를 반납함. 연체 이력이 기록됨.\",\"inputs\":[\"회원번호\",\"도서 ID\",\"반납일 > 반납예정일\"],\"outputs\":[\"연체 기록\",\"도서 상태 변경\"],\"nextEvents\":[\"BookReturned\"]}\n\n## Event\n\n{\"name\":\"LoanExtended\",\"displayName\":\"대출이 연장됨\",\"actor\":\"Member\",\"level\":8,\"description\":\"회원이 현재 대출 중인 도서에 대해 연장 신청하여 반납 예정일이 연장됨.\",\"inputs\":[\"회원번호\",\"도서 ID\",\"대출 기록\",\"연장 조건 충족\"],\"outputs\":[\"반납 예정일 연장\",\"연장 이력 기록\"],\"nextEvents\":[\"LoanHistoryRecorded\"]}\n\n## Event\n\n{\"name\":\"LoanHistoryRecorded\",\"displayName\":\"대출 이력이 기록됨\",\"actor\":\"System\",\"level\":9,\"description\":\"도서별로 대출, 반납, 연장 등의 이력이 기록되어 도서의 대출 현황과 상태 변화 추적이 가능해짐.\",\"inputs\":[\"도서 ID\",\"이벤트 정보(대출/반납/연장/연체 등)\"],\"outputs\":[\"대출/반납/연장/연체 이력 데이터\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookStatusHistoryRecorded\",\"displayName\":\"도서 상태 변경 이력이 기록됨\",\"actor\":\"System\",\"level\":10,\"description\":\"도서의 상태(대출가능/대출중/예약중/폐기 등) 변경 이력이 별도로 기록되어 관리자가 이력 조회 가능.\",\"inputs\":[\"도서 ID\",\"이전 상태\",\"변경된 상태\",\"변경 일시\",\"변경 사유\"],\"outputs\":[\"도서 상태 변경 이력\"],\"nextEvents\":[]}",
                    "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.BoundedContext",
                        "height": 590,
                        "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e",
                        "style": "{}",
                        "width": 560,
                        "x": 650,
                        "y": 450
                    },
                    "gitURL": None,
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
                        "height": 350,
                        "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e",
                        "style": "{}",
                        "width": 350,
                        "x": 235,
                        "y": 365
                    },
                    "members": [],
                    "name": "LibraryBookLoan",
                    "displayName": "도서관 도서대출",
                    "oldName": "",
                    "policies": [],
                    "portGenerated": 8080,
                    "preferredPlatform": "template-spring-boot",
                    "preferredPlatformConf": {},
                    "rotateStatus": False,
                    "tempId": "",
                    "templatePerElements": {},
                    "views": [],
                    "definitionId": "My-Project-ID"
                },
                "description": "{\"userStories\":[{\"title\":\"도서 등록 및 관리\",\"description\":\"사서로서 새로운 도서를 등록하고, 등록된 도서의 상태(대출가능, 대출중, 예약중, 폐기)를 관리할 수 있다.\",\"acceptance\":[\"도서명, ISBN, 저자, 출판사, 카테고리 입력 필수.\",\"ISBN은 13자리 숫자만 허용, 중복 불가.\",\"도서 등록 시 상태는 '대출가능'으로 설정.\",\"도서 상태 변경(대출, 반납, 예약, 폐기) 이력 추적 가능.\",\"도서가 폐기되면 대출 및 예약 불가.\"]},{\"title\":\"도서 대출 및 반납 처리\",\"description\":\"회원이 도서 대출/반납을 신청하고, 시스템은 대출 가능 여부를 판단하며 대출, 예약, 연체, 반납 등의 상태를 관리한다.\",\"acceptance\":[\"회원번호와 이름으로 회원 확인 필수.\",\"도서명 또는 ISBN으로 도서 검색 가능.\",\"대출 기간 7/14/30일 중 선택 가능.\",\"대출 중 도서는 예약 가능.\",\"대출 시 도서 상태는 자동으로 '대출중'으로 변경.\",\"반납 시 예약자가 있으면 '예약중', 없으면 '대출가능'으로 자동 전환.\",\"대출 연체 시 연체 이력 기록.\"]},{\"title\":\"대출 현황 및 연장/반납 처리\",\"description\":\"관리자는 현재 대출 중인 도서 현황을 확인하고, 각 건별로 연장 또는 반납 처리를 할 수 있다.\",\"acceptance\":[\"대출 중인 도서 목록, 대출일, 반납예정일, 상태(대출중/연체/반납완료) 표시.\",\"각 대출 건별 연장 또는 반납 버튼 제공.\",\"연장 시 반납예정일이 변경되고, 연장 이력이 기록됨.\",\"반납 시 도서 상태가 자동 변경됨.\"]},{\"title\":\"도서별 대출 및 상태 변경 이력 조회\",\"description\":\"관리자는 특정 도서의 대출 이력 및 상태 변경 이력을 조회하여 추적할 수 있다.\",\"acceptance\":[\"도서별 대출/반납/연장/연체 등 이력 리스트 제공.\",\"도서별 상태 변경 이력(변경일시, 변경 전/후 상태, 변경 사유) 제공.\"]}],\"entities\":{\"Book\":{\"properties\":[{\"name\":\"bookId\",\"type\":\"Long\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"title\",\"type\":\"String\",\"required\":true},{\"name\":\"isbn\",\"type\":\"String\",\"required\":true},{\"name\":\"author\",\"type\":\"String\",\"required\":true},{\"name\":\"publisher\",\"type\":\"String\",\"required\":true},{\"name\":\"category\",\"type\":\"enum\",\"required\":true,\"values\":[\"소설\",\"비소설\",\"학술\",\"잡지\"]},{\"name\":\"status\",\"type\":\"enum\",\"required\":true,\"values\":[\"대출가능\",\"대출중\",\"예약중\",\"폐기\"]}]},\"Member\":{\"properties\":[{\"name\":\"memberId\",\"type\":\"String\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"name\",\"type\":\"String\",\"required\":true}]},\"Loan\":{\"properties\":[{\"name\":\"loanId\",\"type\":\"Long\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"bookId\",\"type\":\"Long\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Book\"},{\"name\":\"memberId\",\"type\":\"String\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Member\"},{\"name\":\"loanDate\",\"type\":\"Date\",\"required\":true},{\"name\":\"dueDate\",\"type\":\"Date\",\"required\":true},{\"name\":\"returnDate\",\"type\":\"Date\"},{\"name\":\"status\",\"type\":\"enum\",\"required\":true,\"values\":[\"대출중\",\"연체\",\"반납완료\"]}]},\"Reservation\":{\"properties\":[{\"name\":\"reservationId\",\"type\":\"Long\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"bookId\",\"type\":\"Long\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Book\"},{\"name\":\"memberId\",\"type\":\"String\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Member\"},{\"name\":\"reservationDate\",\"type\":\"Date\",\"required\":true}]},\"BookStatusHistory\":{\"properties\":[{\"name\":\"historyId\",\"type\":\"Long\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"bookId\",\"type\":\"Long\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Book\"},{\"name\":\"previousStatus\",\"type\":\"String\",\"required\":true},{\"name\":\"currentStatus\",\"type\":\"String\",\"required\":true},{\"name\":\"changedAt\",\"type\":\"Date\",\"required\":true},{\"name\":\"reason\",\"type\":\"String\",\"required\":true}]},\"LoanHistory\":{\"properties\":[{\"name\":\"historyId\",\"type\":\"Long\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"bookId\",\"type\":\"Long\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Book\"},{\"name\":\"eventType\",\"type\":\"enum\",\"required\":true,\"values\":[\"대출\",\"반납\",\"연장\",\"연체\"]},{\"name\":\"eventDate\",\"type\":\"Date\",\"required\":true},{\"name\":\"memberId\",\"type\":\"String\",\"isForeignKey\":true,\"foreignEntity\":\"Member\"}]}},\"businessRules\":[{\"name\":\"ISBN 13자리 유효성 및 중복 검사\",\"description\":\"도서 등록 시 ISBN은 13자리 숫자이며, 기존 도서와 중복되어서는 안된다.\"},{\"name\":\"도서 상태 자동 전환\",\"description\":\"대출, 반납, 예약, 폐기 등 주요 이벤트 발생 시 도서 상태를 자동 변경한다.\"},{\"name\":\"폐기 도서 대출/예약 금지\",\"description\":\"도서 상태가 '폐기'일 경우, 대출 또는 예약 처리가 불가하다.\"},{\"name\":\"예약 우선 반영\",\"description\":\"반납 시 예약자가 있으면 도서 상태를 '예약중'으로 변경하며, 예약자에게 우선 대출이 가능하다.\"},{\"name\":\"대출 연장 조건\",\"description\":\"대출 중인 도서는 연장 가능하며, 연장 시 반납 예정일이 변경되고 연장 이력이 기록된다.\"}],\"interfaces\":{\"BookManagement\":{\"sections\":[{\"name\":\"도서 등록\",\"type\":\"form\",\"fields\":[{\"name\":\"title\",\"type\":\"text\",\"required\":true},{\"name\":\"isbn\",\"type\":\"text\",\"required\":true},{\"name\":\"author\",\"type\":\"text\",\"required\":true},{\"name\":\"publisher\",\"type\":\"text\",\"required\":true},{\"name\":\"category\",\"type\":\"select\",\"required\":true}],\"actions\":[\"도서 등록\"],\"filters\":[],\"resultTable\":{\"columns\":[],\"actions\":[]}},{\"name\":\"도서 현황\",\"type\":\"table\",\"fields\":[],\"actions\":[\"상태 변경\",\"폐기 처리\"],\"filters\":[\"카테고리\",\"상태\"],\"resultTable\":{\"columns\":[\"bookId\",\"title\",\"isbn\",\"author\",\"publisher\",\"category\",\"status\"],\"actions\":[\"상태 변경\",\"이력 조회\"]}}]},\"LoanAndReturn\":{\"sections\":[{\"name\":\"대출/반납 처리\",\"type\":\"form\",\"fields\":[{\"name\":\"memberId\",\"type\":\"text\",\"required\":true},{\"name\":\"name\",\"type\":\"text\",\"required\":true},{\"name\":\"bookSearch\",\"type\":\"search\",\"required\":true},{\"name\":\"loanPeriod\",\"type\":\"select\",\"required\":true}],\"actions\":[\"대출 신청\",\"반납 처리\",\"예약 신청\"],\"filters\":[],\"resultTable\":{\"columns\":[],\"actions\":[]}}]},\"LoanStatus\":{\"sections\":[{\"name\":\"대출 현황\",\"type\":\"table\",\"fields\":[],\"actions\":[\"연장\",\"반납\"],\"filters\":[\"대출상태\"],\"resultTable\":{\"columns\":[\"loanId\",\"bookId\",\"title\",\"memberId\",\"loanDate\",\"dueDate\",\"returnDate\",\"status\"],\"actions\":[\"연장\",\"반납\"]}}]},\"BookHistory\":{\"sections\":[{\"name\":\"대출 이력 조회\",\"type\":\"table\",\"fields\":[],\"actions\":[],\"filters\":[\"도서ID\"],\"resultTable\":{\"columns\":[\"historyId\",\"eventType\",\"eventDate\",\"memberId\"],\"actions\":[]}},{\"name\":\"상태 변경 이력 조회\",\"type\":\"table\",\"fields\":[],\"actions\":[],\"filters\":[\"도서ID\"],\"resultTable\":{\"columns\":[\"historyId\",\"previousStatus\",\"currentStatus\",\"changedAt\",\"reason\"],\"actions\":[]}}]}},\"events\":[{\"name\":\"BookRegistered\",\"description\":\"사서가 도서명, ISBN, 저자, 출판사, 카테고리를 입력하여 신규 도서를 등록함. ISBN 중복 및 형식(13자리 숫자) 검증을 거침.\",\"displayName\":\"도서가 등록됨\"},{\"name\":\"BookRegistrationFailedDueToDuplicateISBN\",\"description\":\"도서 등록 시 입력한 ISBN이 기존에 이미 존재할 경우, 도서 등록이 실패함.\",\"displayName\":\"ISBN 중복으로 도서 등록 실패함\"},{\"name\":\"BookRegistrationFailedDueToInvalidISBNFormat\",\"description\":\"도서 등록 시 입력한 ISBN이 13자리 숫자 형식이 아닐 경우, 도서 등록이 실패함.\",\"displayName\":\"ISBN 형식 오류로 도서 등록 실패함\"},{\"name\":\"BookStateChanged\",\"description\":\"도서의 상태가 비즈니스 프로세스(등록, 대출, 반납, 예약, 폐기)에 따라 변경됨.\",\"displayName\":\"도서 상태가 변경됨\"},{\"name\":\"BookDisposed\",\"description\":\"사서가 도서가 훼손되거나 분실되었음을 확인하고 해당 도서를 폐기 처리함.\",\"displayName\":\"도서가 폐기됨\"},{\"name\":\"BookBorrowed\",\"description\":\"회원이 회원번호와 이름으로 인증 후 도서명 또는 ISBN으로 도서를 검색하여 대출 기간을 선택하고 대출 신청을 완료함.\",\"displayName\":\"도서가 대출됨\"},{\"name\":\"BookBorrowFailedDueToUnavailableBook\",\"description\":\"회원이 대출을 시도했으나 해당 도서가 이미 대출 중이어서 대출이 실패함.\",\"displayName\":\"도서 대출 불가로 대출 실패함\"},{\"name\":\"BookReserved\",\"description\":\"회원이 대출 중인 도서를 예약함. 예약자 정보와 예약 일시가 저장됨.\",\"displayName\":\"도서가 예약됨\"},{\"name\":\"BookReturned\",\"description\":\"회원이 대출 중이던 도서를 반납함. 반납일이 기록되고 도서의 상태가 변경됨.\",\"displayName\":\"도서가 반납됨\"},{\"name\":\"BookReturnOverdue\",\"description\":\"회원이 반납 예정일을 초과하여 도서를 반납함. 연체 이력이 기록됨.\",\"displayName\":\"도서가 연체되어 반납됨\"},{\"name\":\"LoanExtended\",\"description\":\"회원이 현재 대출 중인 도서에 대해 연장 신청하여 반납 예정일이 연장됨.\",\"displayName\":\"대출이 연장됨\"},{\"name\":\"LoanHistoryRecorded\",\"description\":\"도서별로 대출, 반납, 연장 등의 이력이 기록되어 도서의 대출 현황과 상태 변화 추적이 가능해짐.\",\"displayName\":\"대출 이력이 기록됨\"},{\"name\":\"BookStatusHistoryRecorded\",\"description\":\"도서의 상태(대출가능/대출중/예약중/폐기 등) 변경 이력이 별도로 기록되어 관리자가 이력 조회 가능.\",\"displayName\":\"도서 상태 변경 이력이 기록됨\"}]}"
            },
            "LoanHistory": {
                "structure": [
                    {
                        "aggregate": {
                            "name": "LoanHistory",
                            "alias": "대출이력"
                        },
                        "enumerations": [
                            {
                                "name": "LoanType",
                                "alias": "대출이력타입"
                            }
                        ],
                        "valueObjects": [
                            {
                                "name": "BookReference",
                                "alias": "도서참조",
                                "referencedAggregate": {
                                    "name": "Book",
                                    "alias": "도서"
                                }
                            },
                            {
                                "name": "Member",
                                "alias": "회원"
                            }
                        ]
                    },
                    {
                        "aggregate": {
                            "name": "BookStatusHistory",
                            "alias": "도서상태변경이력"
                        },
                        "enumerations": [
                            {
                                "name": "BookStatus",
                                "alias": "도서상태"
                            }
                        ],
                        "valueObjects": [
                            {
                                "name": "BookReference",
                                "alias": "도서참조",
                                "referencedAggregate": {
                                    "name": "Book",
                                    "alias": "도서"
                                }
                            }
                        ]
                    }
                ],
                "pros": {
                    "cohesion": "대출이력과 상태변경이력 각각 도메인별 책임이 명확하게 분리되어, 각 Aggregate가 자신의 업무 규칙과 트랜잭션 일관성을 독립적으로 유지합니다.",
                    "coupling": "Book, Loan 등 외부 Aggregate는 참조 ValueObject로만 연결되어 직접 의존성이 낮아 전체 시스템 유연성이 높아집니다.",
                    "consistency": "각 이력별로 필수 불변조건(대출 이벤트, 상태 변경 이벤트)을 Aggregate 내부에서 원자적으로 보장할 수 있습니다.",
                    "encapsulation": "각각의 도메인 규칙이 별도 Aggregate 내부에 은닉되어 변경 영향이 최소화됩니다.",
                    "complexity": "업무별 Aggregate로 구조가 단순하며, 한 Aggregate만 파악해도 주요 로직을 이해할 수 있습니다.",
                    "independence": "이력 유형별 확장 및 변경이 독립적으로 가능하며, 운영 중에도 각 Aggregate의 독립 배포가 용이합니다.",
                    "performance": "이력 테이블이 분리되어 대량 데이터가 발생해도 각 쿼리 및 인덱스 설계가 최적화 가능합니다."
                },
                "cons": {
                    "cohesion": "도서별 전체 이력(대출+상태변경) 조회 시 두 Aggregate를 모두 질의해야 하므로 업무 관점의 완전한 단일성을 제공하지 않습니다.",
                    "coupling": "조회나 통계 등 복합 정보가 필요한 경우 두 Aggregate 간 데이터를 조합하는 추가 로직이 필요합니다.",
                    "consistency": "도서 대출 이벤트와 상태 변경이력이 동시에 발생하는 경우 트랜잭션 일관성 보장이 Aggregate 단위로 분리되어 있습니다.",
                    "encapsulation": "비즈니스 규칙이 분산되므로, 전체 이력 처리 로직을 한곳에서 변경하거나 관리하려면 여러 Aggregate를 모두 파악해야 합니다.",
                    "complexity": "대출과 상태변경 이벤트가 동시에 발생할 때 외부 오케스트레이션이 필요합니다.",
                    "independence": "이력 간 통합적 변경 요구가 생길 경우, 구조 재설계가 필요할 수 있습니다.",
                    "performance": "복합 이력 조회 쿼리는 다중 Aggregate 접근으로 인한 약간의 쿼리 비용 상승이 있을 수 있습니다."
                },
                "isAIRecommended": False,
                "boundedContext": {
                    "_type": "org.uengine.modeling.model.BoundedContext",
                    "aggregates": [
                        {
                            "id": "b352b64a-a49d-4704-b27f-e532280568d8"
                        },
                        {
                            "id": "4d3ad69a-26a0-4339-b557-dcd54213c61f"
                        }
                    ],
                    "author": "My-UID",
                    "description": "# Requirements\n\n## userStory\n\n각 도서별로 대출 이력과 상태 변경 이력을 조회할 수 있어야 하고, 이를 통해 도서의 대출 현황과 상태 변화를 추적할 수 있어야 해.\n\n## Event\n\n{\"name\":\"BookBorrowed\",\"displayName\":\"도서가 대출됨\",\"actor\":\"Member\",\"level\":4,\"description\":\"회원이 회원번호와 이름으로 인증 후 도서명 또는 ISBN으로 도서를 검색하여 대출 기간을 선택하고 대출 신청을 완료함.\",\"inputs\":[\"회원번호\",\"회원명\",\"도서 ID\",\"대출 기간(7/14/30일)\",\"도서 상태: 대출가능\"],\"outputs\":[\"도서 대출 기록 생성\",\"도서 상태: 대출중\"],\"nextEvents\":[\"BookStateChanged\",\"LoanHistoryRecorded\"]}\n\n## Event\n\n{\"name\":\"BookReturned\",\"displayName\":\"도서가 반납됨\",\"actor\":\"Member\",\"level\":6,\"description\":\"회원이 대출 중이던 도서를 반납함. 반납일이 기록되고 도서의 상태가 변경됨.\",\"inputs\":[\"회원번호\",\"도서 ID\",\"대출 기록\"],\"outputs\":[\"반납일 기록\",\"도서 상태: 대출가능(예약자 없을 시) 또는 예약중(예약자 있을 시)\"],\"nextEvents\":[\"BookStateChanged\",\"LoanHistoryRecorded\"]}\n\n## Event\n\n{\"name\":\"BookReturnOverdue\",\"displayName\":\"도서가 연체되어 반납됨\",\"actor\":\"Member\",\"level\":7,\"description\":\"회원이 반납 예정일을 초과하여 도서를 반납함. 연체 이력이 기록됨.\",\"inputs\":[\"회원번호\",\"도서 ID\",\"반납일 > 반납예정일\"],\"outputs\":[\"연체 기록\",\"도서 상태 변경\"],\"nextEvents\":[\"BookReturned\"]}\n\n## Event\n\n{\"name\":\"LoanExtended\",\"displayName\":\"대출이 연장됨\",\"actor\":\"Member\",\"level\":8,\"description\":\"회원이 현재 대출 중인 도서에 대해 연장 신청하여 반납 예정일이 연장됨.\",\"inputs\":[\"회원번호\",\"도서 ID\",\"대출 기록\",\"연장 조건 충족\"],\"outputs\":[\"반납 예정일 연장\",\"연장 이력 기록\"],\"nextEvents\":[\"LoanHistoryRecorded\"]}\n\n## Event\n\n{\"name\":\"LoanHistoryRecorded\",\"displayName\":\"대출 이력이 기록됨\",\"actor\":\"System\",\"level\":9,\"description\":\"도서별로 대출, 반납, 연장 등의 이력이 기록되어 도서의 대출 현황과 상태 변화 추적이 가능해짐.\",\"inputs\":[\"도서 ID\",\"이벤트 정보(대출/반납/연장/연체 등)\"],\"outputs\":[\"대출/반납/연장/연체 이력 데이터\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookStatusHistoryRecorded\",\"displayName\":\"도서 상태 변경 이력이 기록됨\",\"actor\":\"System\",\"level\":10,\"description\":\"도서의 상태(대출가능/대출중/예약중/폐기 등) 변경 이력이 별도로 기록되어 관리자가 이력 조회 가능.\",\"inputs\":[\"도서 ID\",\"이전 상태\",\"변경된 상태\",\"변경 일시\",\"변경 사유\"],\"outputs\":[\"도서 상태 변경 이력\"],\"nextEvents\":[]}",
                    "id": "c517babe-52fb-48ba-8920-60df60b3da1e",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.BoundedContext",
                        "height": 590,
                        "id": "c517babe-52fb-48ba-8920-60df60b3da1e",
                        "style": "{}",
                        "width": 1010,
                        "x": 1460.0,
                        "y": 450
                    },
                    "gitURL": None,
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
                        "height": 350,
                        "id": "c517babe-52fb-48ba-8920-60df60b3da1e",
                        "style": "{}",
                        "width": 350,
                        "x": 235,
                        "y": 365
                    },
                    "members": [],
                    "name": "LoanHistory",
                    "displayName": "대출이력",
                    "oldName": "",
                    "policies": [],
                    "portGenerated": 8081,
                    "preferredPlatform": "template-spring-boot",
                    "preferredPlatformConf": {},
                    "rotateStatus": False,
                    "tempId": "",
                    "templatePerElements": {},
                    "views": [],
                    "definitionId": "My-Project-ID"
                },
                "description": "{\"userStories\":[{\"title\":\"도서별 대출 및 상태 변경 이력 조회\",\"description\":\"관리자 또는 이용자는 특정 도서의 대출 이력과 상태 변경 이력을 조회하여 도서의 대출 현황과 상태 변화를 한눈에 파악할 수 있다.\",\"acceptance\":[\"도서 ID로 대출 이력 및 상태 변경 이력을 모두 조회할 수 있다.\",\"대출, 반납, 연장, 연체 등 모든 대출 관련 이력이 포함된다.\",\"상태 변경 이력에는 변경 전/후 상태, 변경 일시, 사유가 명확히 표시된다.\",\"이력 데이터는 정렬/필터링이 가능하다.\"]}],\"entities\":{\"Book\":{\"properties\":[{\"name\":\"bookId\",\"type\":\"String\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"title\",\"type\":\"String\",\"required\":true},{\"name\":\"isbn\",\"type\":\"String\"},{\"name\":\"status\",\"type\":\"enum\",\"required\":true,\"values\":[\"AVAILABLE\",\"BORROWED\",\"RESERVED\",\"DISCARDED\"]}]},\"LoanHistory\":{\"properties\":[{\"name\":\"loanHistoryId\",\"type\":\"Long\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"bookId\",\"type\":\"String\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Book\"},{\"name\":\"memberId\",\"type\":\"String\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Member\"},{\"name\":\"loanType\",\"type\":\"enum\",\"required\":true,\"values\":[\"BORROW\",\"RETURN\",\"EXTEND\",\"OVERDUE\"]},{\"name\":\"loanStartDate\",\"type\":\"Date\"},{\"name\":\"loanDueDate\",\"type\":\"Date\"},{\"name\":\"returnDate\",\"type\":\"Date\"},{\"name\":\"overdueDays\",\"type\":\"Integer\"},{\"name\":\"createdAt\",\"type\":\"Date\",\"required\":true}]},\"BookStatusHistory\":{\"properties\":[{\"name\":\"statusHistoryId\",\"type\":\"Long\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"bookId\",\"type\":\"String\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Book\"},{\"name\":\"previousStatus\",\"type\":\"enum\",\"required\":true,\"values\":[\"AVAILABLE\",\"BORROWED\",\"RESERVED\",\"DISCARDED\"]},{\"name\":\"currentStatus\",\"type\":\"enum\",\"required\":true,\"values\":[\"AVAILABLE\",\"BORROWED\",\"RESERVED\",\"DISCARDED\"]},{\"name\":\"changedAt\",\"type\":\"Date\",\"required\":true},{\"name\":\"reason\",\"type\":\"String\"}]},\"Member\":{\"properties\":[{\"name\":\"memberId\",\"type\":\"String\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"memberName\",\"type\":\"String\",\"required\":true}]}},\"businessRules\":[{\"name\":\"대출 이력 기록\",\"description\":\"모든 도서 대출, 반납, 연장, 연체 발생 시 LoanHistory에 이력이 자동으로 기록된다.\"},{\"name\":\"상태 변경 이력 기록\",\"description\":\"도서 상태(AVAILABLE, BORROWED, RESERVED, DISCARDED)가 변경될 때마다 BookStatusHistory에 이전 상태, 변경된 상태, 일시, 사유가 저장된다.\"}],\"interfaces\":{\"BookHistoryLookup\":{\"sections\":[{\"name\":\"도서 이력 조회\",\"type\":\"form\",\"fields\":[{\"name\":\"bookId\",\"type\":\"text\",\"required\":true}],\"actions\":[\"이력 조회\"],\"filters\":[],\"resultTable\":{\"columns\":[],\"actions\":[]}},{\"name\":\"대출 이력 테이블\",\"type\":\"table\",\"fields\":[],\"actions\":[],\"filters\":[\"기간\",\"이력 타입(BORROW, RETURN, EXTEND, OVERDUE)\"],\"resultTable\":{\"columns\":[\"loanType\",\"memberId\",\"loanStartDate\",\"loanDueDate\",\"returnDate\",\"overdueDays\",\"createdAt\"],\"actions\":[]}},{\"name\":\"상태 변경 이력 테이블\",\"type\":\"table\",\"fields\":[],\"actions\":[],\"filters\":[\"기간\",\"상태\"],\"resultTable\":{\"columns\":[\"previousStatus\",\"currentStatus\",\"changedAt\",\"reason\"],\"actions\":[]}}]}},\"events\":[{\"name\":\"BookBorrowed\",\"description\":\"회원이 회원번호와 이름으로 인증 후 도서명 또는 ISBN으로 도서를 검색하여 대출 기간을 선택하고 대출 신청을 완료함.\",\"displayName\":\"도서가 대출됨\"},{\"name\":\"BookReturned\",\"description\":\"회원이 대출 중이던 도서를 반납함. 반납일이 기록되고 도서의 상태가 변경됨.\",\"displayName\":\"도서가 반납됨\"},{\"name\":\"BookReturnOverdue\",\"description\":\"회원이 반납 예정일을 초과하여 도서를 반납함. 연체 이력이 기록됨.\",\"displayName\":\"도서가 연체되어 반납됨\"},{\"name\":\"LoanExtended\",\"description\":\"회원이 현재 대출 중인 도서에 대해 연장 신청하여 반납 예정일이 연장됨.\",\"displayName\":\"대출이 연장됨\"},{\"name\":\"LoanHistoryRecorded\",\"description\":\"도서별로 대출, 반납, 연장 등의 이력이 기록되어 도서의 대출 현황과 상태 변화 추적이 가능해짐.\",\"displayName\":\"대출 이력이 기록됨\"},{\"name\":\"BookStatusHistoryRecorded\",\"description\":\"도서의 상태(대출가능/대출중/예약중/폐기 등) 변경 이력이 별도로 기록되어 관리자가 이력 조회 가능.\",\"displayName\":\"도서 상태 변경 이력이 기록됨\"}]}"
            }
        },
        userInfo=UserInfoModel(
            uid="My-UID"
        ),
        information=InformationModel(
            projectId="My-Project-ID",
        )
    ),
    subgraphs=SubgraphsModel(
        createAggregateByFunctionsModel=CreateAggregateByFunctionsModel(
            draft_options={
                "LibraryBookLoan": {
                    "structure": [
                        {
                            "aggregate": {
                                "name": "Book",
                                "alias": "도서"
                            },
                            "enumerations": [
                                {
                                    "name": "BookStatus",
                                    "alias": "도서상태"
                                },
                                {
                                    "name": "BookCategory",
                                    "alias": "도서카테고리"
                                }
                            ],
                            "valueObjects": [
                                {
                                    "name": "LoanHistoryReference",
                                    "alias": "대출이력참조",
                                    "referencedAggregate": {
                                        "name": "LoanHistory",
                                        "alias": "대출이력"
                                    }
                                },
                                {
                                    "name": "BookStatusHistoryReference",
                                    "alias": "상태변경이력참조",
                                    "referencedAggregate": {
                                        "name": "BookStatusHistory",
                                        "alias": "도서상태변경이력"
                                    }
                                }
                            ]
                        }
                    ],
                    "pros": {
                        "cohesion": "도서에 관한 모든 속성과 상태 및 이력 관리까지 Book Aggregate에 통합되어, 도서 관점의 모든 비즈니스 규칙을 한 곳에서 강하게 보장할 수 있습니다.",
                        "coupling": "외부 참조가 최소화되어, 도서 단위의 변경이 타 도메인에 미치는 영향이 매우 적고, 도서 관련 변경이 Aggregate 내부에서만 일어납니다.",
                        "consistency": "도서 상태, 등록, 폐기, 대출 가능 여부 등 모든 도메인 불변성이 한 트랜잭션 내에서 완벽하게 보장됩니다.",
                        "encapsulation": "도서 상태 변경, 이력 기록 등 모든 도메인 규칙이 외부에서 직접 접근 불가하며, Aggregate 내부에서만 조작됩니다.",
                        "complexity": "단일 Aggregate이므로 이해와 접근이 직관적이며, 복잡한 관계를 신경 쓸 필요 없이 도서 중심으로 개발이 가능합니다.",
                        "independence": "도서 단위로 독립적인 확장과 유지보수가 가능해, 시스템 진화에 매우 유리합니다.",
                        "performance": "도서 기준의 조회 및 관리에 있어 쿼리 효율성이 극대화되어, 다수의 도서 정보를 빠르게 처리할 수 있습니다."
                    },
                    "cons": {
                        "cohesion": "대출, 예약 등 도서 외 세부 행위까지 Book Aggregate에 모두 통합하면, 점차 책임 범위가 확장되어 SRP(단일 책임 원칙)가 약화될 수 있습니다.",
                        "coupling": "대출, 예약 등 타 도메인 비즈니스 변화가 도서 Aggregate 구조에 직접적인 영향을 미쳐 Aggregate 크기가 커질 위험이 있습니다.",
                        "consistency": "다수 사용자의 대출, 예약 등 도서 관련 이벤트가 몰릴 경우 동시성 문제나 잠금 이슈가 발생할 수 있습니다.",
                        "encapsulation": "비즈니스가 발전하면서 도서와 관련 없는 세부 규칙까지 이 Aggregate에서 관리하게 되면, 도메인 캡슐화가 흐려질 수 있습니다.",
                        "complexity": "도서 Aggregate 내부에 너무 많은 도메인 규칙이 쏠리면 복잡도가 상승하여 유지보수 비용이 커질 수 있습니다.",
                        "independence": "Book이 모든 책임을 가지면 도서의 변경이 전체 시스템에 ripple effect를 줄 수 있습니다.",
                        "performance": "대규모 대출/예약/상태 변경이 한 Aggregate에 집중되면, 처리 성능 저하 및 병목이 발생할 수 있습니다."
                    },
                    "isAIRecommended": False,
                    "boundedContext": {
                        "_type": "org.uengine.modeling.model.BoundedContext",
                        "aggregates": [],
                        "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                        "description": "# Requirements\n\n## userStory\n\n도서관의 도서 관리와 대출/반납을 통합적으로 관리하는 화면을 만들려고 해.\n\n## userStory\n\n'도서 관리' 화면에서는 새로운 도서를 등록하고 현재 보유한 도서들의 상태를 관리할 수 있어야 해. 도서 등록 시에는 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받아야 해. ISBN은 13자리 숫자여야 하고 중복 확인이 필요해. 카테고리는 소설/비소설/학술/잡지 중에서 선택할 수 있어야 해. 등록된 도서는 처음에 '대출가능' 상태가 되고, 이후 대출/반납 상황에 따라 '대출중', '예약중' 상태로 자동으로 변경되어야 해. 도서가 훼손되거나 분실된 경우 '폐기' 처리가 가능해야 하며, 폐기된 도서는 더 이상 대출이 불가능해야 해.\n\n## userStory\n\n'대출/반납' 화면에서는 회원이 도서를 대출하고 반납하는 것을 관리할 수 있어야 해. 대출 신청 시에는 회원번호와 이름으로 회원을 확인하고, 대출할 도서를 선택해야 해. 도서는 도서명이나 ISBN으로 검색할 수 있어야 해. 대출 기간은 7일/14일/30일 중에서 선택할 수 있어. 만약 대출하려는 도서가 이미 대출 중이라면, 예약 신청이 가능해야 해. 대출이 완료되면 해당 도서의 상태는 자동으로 '대출중'으로 변경되어야 해.\n\n## userStory\n\n대출 현황 화면에서는 현재 대출 중인 도서들의 목록을 볼 수 있어야 해. 각 대출 건에 대해 대출일, 반납예정일, 현재 상태(대출중/연체/반납완료)를 확인할 수 있어야 하고, 대출 중인 도서는 연장이나 반납 처리가 가능해야 해. 도서가 반납되면 자동으로 해당 도서의 상태가 '대출가능'으로 변경되어야 해. 만약 예약자가 있는 도서가 반납되면, 해당 도서는 '예약중' 상태로 변경되어야 해.\n\n## userStory\n\n각 도서별로 대출 이력과 상태 변경 이력을 조회할 수 있어야 하고, 이를 통해 도서의 대출 현황과 상태 변화를 추적할 수 있어야 해.\n\n## Event\n\n{\"name\":\"BookRegistered\",\"displayName\":\"도서가 등록됨\",\"actor\":\"Librarian\",\"level\":1,\"description\":\"사서가 도서명, ISBN, 저자, 출판사, 카테고리를 입력하여 신규 도서를 등록함. ISBN 중복 및 형식(13자리 숫자) 검증을 거침.\",\"inputs\":[\"도서명\",\"ISBN(13자리)\",\"저자\",\"출판사\",\"카테고리(소설/비소설/학술/잡지)\",\"ISBN 중복 아님\",\"ISBN 형식 유효\"],\"outputs\":[\"신규 도서 등록\",\"도서 상태: 대출가능\"],\"nextEvents\":[\"BookStateChanged\"]}\n\n## Event\n\n{\"name\":\"BookRegistrationFailedDueToDuplicateISBN\",\"displayName\":\"ISBN 중복으로 도서 등록 실패함\",\"actor\":\"Librarian\",\"level\":1,\"description\":\"도서 등록 시 입력한 ISBN이 기존에 이미 존재할 경우, 도서 등록이 실패함.\",\"inputs\":[\"ISBN(13자리)\",\"기존 도서에 동일 ISBN 존재\"],\"outputs\":[\"도서 등록 실패 알림\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookRegistrationFailedDueToInvalidISBNFormat\",\"displayName\":\"ISBN 형식 오류로 도서 등록 실패함\",\"actor\":\"Librarian\",\"level\":1,\"description\":\"도서 등록 시 입력한 ISBN이 13자리 숫자 형식이 아닐 경우, 도서 등록이 실패함.\",\"inputs\":[\"ISBN(13자리 아님)\"],\"outputs\":[\"도서 등록 실패 알림\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookStateChanged\",\"displayName\":\"도서 상태가 변경됨\",\"actor\":\"System\",\"level\":2,\"description\":\"도서의 상태가 비즈니스 프로세스(등록, 대출, 반납, 예약, 폐기)에 따라 변경됨.\",\"inputs\":[\"도서 ID\",\"변경 사유(등록, 대출, 반납, 예약, 폐기 등)\"],\"outputs\":[\"도서 상태 변경(대출가능/대출중/예약중/폐기)\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookDisposed\",\"displayName\":\"도서가 폐기됨\",\"actor\":\"Librarian\",\"level\":3,\"description\":\"사서가 도서가 훼손되거나 분실되었음을 확인하고 해당 도서를 폐기 처리함.\",\"inputs\":[\"도서 ID\",\"폐기 사유(훼손, 분실 등)\"],\"outputs\":[\"도서 상태: 폐기\",\"해당 도서 대출 불가\"],\"nextEvents\":[\"BookStateChanged\"]}\n\n## Event\n\n{\"name\":\"BookBorrowed\",\"displayName\":\"도서가 대출됨\",\"actor\":\"Member\",\"level\":4,\"description\":\"회원이 회원번호와 이름으로 인증 후 도서명 또는 ISBN으로 도서를 검색하여 대출 기간을 선택하고 대출 신청을 완료함.\",\"inputs\":[\"회원번호\",\"회원명\",\"도서 ID\",\"대출 기간(7/14/30일)\",\"도서 상태: 대출가능\"],\"outputs\":[\"도서 대출 기록 생성\",\"도서 상태: 대출중\"],\"nextEvents\":[\"BookStateChanged\",\"LoanHistoryRecorded\"]}\n\n## Event\n\n{\"name\":\"BookBorrowFailedDueToUnavailableBook\",\"displayName\":\"도서 대출 불가로 대출 실패함\",\"actor\":\"Member\",\"level\":4,\"description\":\"회원이 대출을 시도했으나 해당 도서가 이미 대출 중이어서 대출이 실패함.\",\"inputs\":[\"도서 ID\",\"도서 상태: 대출중/폐기\"],\"outputs\":[\"도서 대출 실패 알림\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookReserved\",\"displayName\":\"도서가 예약됨\",\"actor\":\"Member\",\"level\":5,\"description\":\"회원이 대출 중인 도서를 예약함. 예약자 정보와 예약 일시가 저장됨.\",\"inputs\":[\"회원번호\",\"회원명\",\"도서 ID\",\"도서 상태: 대출중\"],\"outputs\":[\"도서 예약 기록 생성\",\"도서 상태: 예약중(반납 시 자동 전환)\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookReturned\",\"displayName\":\"도서가 반납됨\",\"actor\":\"Member\",\"level\":6,\"description\":\"회원이 대출 중이던 도서를 반납함. 반납일이 기록되고 도서의 상태가 변경됨.\",\"inputs\":[\"회원번호\",\"도서 ID\",\"대출 기록\"],\"outputs\":[\"반납일 기록\",\"도서 상태: 대출가능(예약자 없을 시) 또는 예약중(예약자 있을 시)\"],\"nextEvents\":[\"BookStateChanged\",\"LoanHistoryRecorded\"]}\n\n## Event\n\n{\"name\":\"BookReturnOverdue\",\"displayName\":\"도서가 연체되어 반납됨\",\"actor\":\"Member\",\"level\":7,\"description\":\"회원이 반납 예정일을 초과하여 도서를 반납함. 연체 이력이 기록됨.\",\"inputs\":[\"회원번호\",\"도서 ID\",\"반납일 > 반납예정일\"],\"outputs\":[\"연체 기록\",\"도서 상태 변경\"],\"nextEvents\":[\"BookReturned\"]}\n\n## Event\n\n{\"name\":\"LoanExtended\",\"displayName\":\"대출이 연장됨\",\"actor\":\"Member\",\"level\":8,\"description\":\"회원이 현재 대출 중인 도서에 대해 연장 신청하여 반납 예정일이 연장됨.\",\"inputs\":[\"회원번호\",\"도서 ID\",\"대출 기록\",\"연장 조건 충족\"],\"outputs\":[\"반납 예정일 연장\",\"연장 이력 기록\"],\"nextEvents\":[\"LoanHistoryRecorded\"]}\n\n## Event\n\n{\"name\":\"LoanHistoryRecorded\",\"displayName\":\"대출 이력이 기록됨\",\"actor\":\"System\",\"level\":9,\"description\":\"도서별로 대출, 반납, 연장 등의 이력이 기록되어 도서의 대출 현황과 상태 변화 추적이 가능해짐.\",\"inputs\":[\"도서 ID\",\"이벤트 정보(대출/반납/연장/연체 등)\"],\"outputs\":[\"대출/반납/연장/연체 이력 데이터\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookStatusHistoryRecorded\",\"displayName\":\"도서 상태 변경 이력이 기록됨\",\"actor\":\"System\",\"level\":10,\"description\":\"도서의 상태(대출가능/대출중/예약중/폐기 등) 변경 이력이 별도로 기록되어 관리자가 이력 조회 가능.\",\"inputs\":[\"도서 ID\",\"이전 상태\",\"변경된 상태\",\"변경 일시\",\"변경 사유\"],\"outputs\":[\"도서 상태 변경 이력\"],\"nextEvents\":[]}",
                        "id": "6e671f4b-e55f-92b2-746d-4451c7d007cb",
                        "elementView": {
                            "_type": "org.uengine.modeling.model.BoundedContext",
                            "height": 590,
                            "id": "6e671f4b-e55f-92b2-746d-4451c7d007cb",
                            "style": "{}",
                            "width": 560,
                            "x": 650,
                            "y": 450
                        },
                        "gitURL": None,
                        "hexagonalView": {
                            "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
                            "height": 350,
                            "id": "6e671f4b-e55f-92b2-746d-4451c7d007cb",
                            "style": "{}",
                            "width": 350,
                            "x": 235,
                            "y": 365
                        },
                        "members": [],
                        "name": "LibraryBookLoan",
                        "displayName": "도서관 도서대출",
                        "oldName": "",
                        "policies": [],
                        "portGenerated": None,
                        "preferredPlatform": "template-spring-boot",
                        "preferredPlatformConf": {},
                        "rotateStatus": False,
                        "tempId": "",
                        "templatePerElements": {},
                        "views": [],
                        "definitionId": "22901979210f3e4d4078ed657eee2155"
                    },
                    "description": "{\"userStories\":[{\"title\":\"도서 등록 및 관리\",\"description\":\"사서로서 새로운 도서를 등록하고, 등록된 도서의 상태(대출가능, 대출중, 예약중, 폐기)를 관리할 수 있다.\",\"acceptance\":[\"도서명, ISBN, 저자, 출판사, 카테고리 입력 필수.\",\"ISBN은 13자리 숫자만 허용, 중복 불가.\",\"도서 등록 시 상태는 '대출가능'으로 설정.\",\"도서 상태 변경(대출, 반납, 예약, 폐기) 이력 추적 가능.\",\"도서가 폐기되면 대출 및 예약 불가.\"]},{\"title\":\"도서 대출 및 반납 처리\",\"description\":\"회원이 도서 대출/반납을 신청하고, 시스템은 대출 가능 여부를 판단하며 대출, 예약, 연체, 반납 등의 상태를 관리한다.\",\"acceptance\":[\"회원번호와 이름으로 회원 확인 필수.\",\"도서명 또는 ISBN으로 도서 검색 가능.\",\"대출 기간 7/14/30일 중 선택 가능.\",\"대출 중 도서는 예약 가능.\",\"대출 시 도서 상태는 자동으로 '대출중'으로 변경.\",\"반납 시 예약자가 있으면 '예약중', 없으면 '대출가능'으로 자동 전환.\",\"대출 연체 시 연체 이력 기록.\"]},{\"title\":\"대출 현황 및 연장/반납 처리\",\"description\":\"관리자는 현재 대출 중인 도서 현황을 확인하고, 각 건별로 연장 또는 반납 처리를 할 수 있다.\",\"acceptance\":[\"대출 중인 도서 목록, 대출일, 반납예정일, 상태(대출중/연체/반납완료) 표시.\",\"각 대출 건별 연장 또는 반납 버튼 제공.\",\"연장 시 반납예정일이 변경되고, 연장 이력이 기록됨.\",\"반납 시 도서 상태가 자동 변경됨.\"]},{\"title\":\"도서별 대출 및 상태 변경 이력 조회\",\"description\":\"관리자는 특정 도서의 대출 이력 및 상태 변경 이력을 조회하여 추적할 수 있다.\",\"acceptance\":[\"도서별 대출/반납/연장/연체 등 이력 리스트 제공.\",\"도서별 상태 변경 이력(변경일시, 변경 전/후 상태, 변경 사유) 제공.\"]}],\"entities\":{\"Book\":{\"properties\":[{\"name\":\"bookId\",\"type\":\"Long\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"title\",\"type\":\"String\",\"required\":true},{\"name\":\"isbn\",\"type\":\"String\",\"required\":true},{\"name\":\"author\",\"type\":\"String\",\"required\":true},{\"name\":\"publisher\",\"type\":\"String\",\"required\":true},{\"name\":\"category\",\"type\":\"enum\",\"required\":true,\"values\":[\"소설\",\"비소설\",\"학술\",\"잡지\"]},{\"name\":\"status\",\"type\":\"enum\",\"required\":true,\"values\":[\"대출가능\",\"대출중\",\"예약중\",\"폐기\"]}]},\"Member\":{\"properties\":[{\"name\":\"memberId\",\"type\":\"String\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"name\",\"type\":\"String\",\"required\":true}]},\"Loan\":{\"properties\":[{\"name\":\"loanId\",\"type\":\"Long\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"bookId\",\"type\":\"Long\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Book\"},{\"name\":\"memberId\",\"type\":\"String\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Member\"},{\"name\":\"loanDate\",\"type\":\"Date\",\"required\":true},{\"name\":\"dueDate\",\"type\":\"Date\",\"required\":true},{\"name\":\"returnDate\",\"type\":\"Date\"},{\"name\":\"status\",\"type\":\"enum\",\"required\":true,\"values\":[\"대출중\",\"연체\",\"반납완료\"]}]},\"Reservation\":{\"properties\":[{\"name\":\"reservationId\",\"type\":\"Long\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"bookId\",\"type\":\"Long\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Book\"},{\"name\":\"memberId\",\"type\":\"String\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Member\"},{\"name\":\"reservationDate\",\"type\":\"Date\",\"required\":true}]},\"BookStatusHistory\":{\"properties\":[{\"name\":\"historyId\",\"type\":\"Long\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"bookId\",\"type\":\"Long\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Book\"},{\"name\":\"previousStatus\",\"type\":\"String\",\"required\":true},{\"name\":\"currentStatus\",\"type\":\"String\",\"required\":true},{\"name\":\"changedAt\",\"type\":\"Date\",\"required\":true},{\"name\":\"reason\",\"type\":\"String\",\"required\":true}]},\"LoanHistory\":{\"properties\":[{\"name\":\"historyId\",\"type\":\"Long\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"bookId\",\"type\":\"Long\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Book\"},{\"name\":\"eventType\",\"type\":\"enum\",\"required\":true,\"values\":[\"대출\",\"반납\",\"연장\",\"연체\"]},{\"name\":\"eventDate\",\"type\":\"Date\",\"required\":true},{\"name\":\"memberId\",\"type\":\"String\",\"isForeignKey\":true,\"foreignEntity\":\"Member\"}]}},\"businessRules\":[{\"name\":\"ISBN 13자리 유효성 및 중복 검사\",\"description\":\"도서 등록 시 ISBN은 13자리 숫자이며, 기존 도서와 중복되어서는 안된다.\"},{\"name\":\"도서 상태 자동 전환\",\"description\":\"대출, 반납, 예약, 폐기 등 주요 이벤트 발생 시 도서 상태를 자동 변경한다.\"},{\"name\":\"폐기 도서 대출/예약 금지\",\"description\":\"도서 상태가 '폐기'일 경우, 대출 또는 예약 처리가 불가하다.\"},{\"name\":\"예약 우선 반영\",\"description\":\"반납 시 예약자가 있으면 도서 상태를 '예약중'으로 변경하며, 예약자에게 우선 대출이 가능하다.\"},{\"name\":\"대출 연장 조건\",\"description\":\"대출 중인 도서는 연장 가능하며, 연장 시 반납 예정일이 변경되고 연장 이력이 기록된다.\"}],\"interfaces\":{\"BookManagement\":{\"sections\":[{\"name\":\"도서 등록\",\"type\":\"form\",\"fields\":[{\"name\":\"title\",\"type\":\"text\",\"required\":true},{\"name\":\"isbn\",\"type\":\"text\",\"required\":true},{\"name\":\"author\",\"type\":\"text\",\"required\":true},{\"name\":\"publisher\",\"type\":\"text\",\"required\":true},{\"name\":\"category\",\"type\":\"select\",\"required\":true}],\"actions\":[\"도서 등록\"],\"filters\":[],\"resultTable\":{\"columns\":[],\"actions\":[]}},{\"name\":\"도서 현황\",\"type\":\"table\",\"fields\":[],\"actions\":[\"상태 변경\",\"폐기 처리\"],\"filters\":[\"카테고리\",\"상태\"],\"resultTable\":{\"columns\":[\"bookId\",\"title\",\"isbn\",\"author\",\"publisher\",\"category\",\"status\"],\"actions\":[\"상태 변경\",\"이력 조회\"]}}]},\"LoanAndReturn\":{\"sections\":[{\"name\":\"대출/반납 처리\",\"type\":\"form\",\"fields\":[{\"name\":\"memberId\",\"type\":\"text\",\"required\":true},{\"name\":\"name\",\"type\":\"text\",\"required\":true},{\"name\":\"bookSearch\",\"type\":\"search\",\"required\":true},{\"name\":\"loanPeriod\",\"type\":\"select\",\"required\":true}],\"actions\":[\"대출 신청\",\"반납 처리\",\"예약 신청\"],\"filters\":[],\"resultTable\":{\"columns\":[],\"actions\":[]}}]},\"LoanStatus\":{\"sections\":[{\"name\":\"대출 현황\",\"type\":\"table\",\"fields\":[],\"actions\":[\"연장\",\"반납\"],\"filters\":[\"대출상태\"],\"resultTable\":{\"columns\":[\"loanId\",\"bookId\",\"title\",\"memberId\",\"loanDate\",\"dueDate\",\"returnDate\",\"status\"],\"actions\":[\"연장\",\"반납\"]}}]},\"BookHistory\":{\"sections\":[{\"name\":\"대출 이력 조회\",\"type\":\"table\",\"fields\":[],\"actions\":[],\"filters\":[\"도서ID\"],\"resultTable\":{\"columns\":[\"historyId\",\"eventType\",\"eventDate\",\"memberId\"],\"actions\":[]}},{\"name\":\"상태 변경 이력 조회\",\"type\":\"table\",\"fields\":[],\"actions\":[],\"filters\":[\"도서ID\"],\"resultTable\":{\"columns\":[\"historyId\",\"previousStatus\",\"currentStatus\",\"changedAt\",\"reason\"],\"actions\":[]}}]}},\"events\":[{\"name\":\"BookRegistered\",\"description\":\"사서가 도서명, ISBN, 저자, 출판사, 카테고리를 입력하여 신규 도서를 등록함. ISBN 중복 및 형식(13자리 숫자) 검증을 거침.\",\"displayName\":\"도서가 등록됨\"},{\"name\":\"BookRegistrationFailedDueToDuplicateISBN\",\"description\":\"도서 등록 시 입력한 ISBN이 기존에 이미 존재할 경우, 도서 등록이 실패함.\",\"displayName\":\"ISBN 중복으로 도서 등록 실패함\"},{\"name\":\"BookRegistrationFailedDueToInvalidISBNFormat\",\"description\":\"도서 등록 시 입력한 ISBN이 13자리 숫자 형식이 아닐 경우, 도서 등록이 실패함.\",\"displayName\":\"ISBN 형식 오류로 도서 등록 실패함\"},{\"name\":\"BookStateChanged\",\"description\":\"도서의 상태가 비즈니스 프로세스(등록, 대출, 반납, 예약, 폐기)에 따라 변경됨.\",\"displayName\":\"도서 상태가 변경됨\"},{\"name\":\"BookDisposed\",\"description\":\"사서가 도서가 훼손되거나 분실되었음을 확인하고 해당 도서를 폐기 처리함.\",\"displayName\":\"도서가 폐기됨\"},{\"name\":\"BookBorrowed\",\"description\":\"회원이 회원번호와 이름으로 인증 후 도서명 또는 ISBN으로 도서를 검색하여 대출 기간을 선택하고 대출 신청을 완료함.\",\"displayName\":\"도서가 대출됨\"},{\"name\":\"BookBorrowFailedDueToUnavailableBook\",\"description\":\"회원이 대출을 시도했으나 해당 도서가 이미 대출 중이어서 대출이 실패함.\",\"displayName\":\"도서 대출 불가로 대출 실패함\"},{\"name\":\"BookReserved\",\"description\":\"회원이 대출 중인 도서를 예약함. 예약자 정보와 예약 일시가 저장됨.\",\"displayName\":\"도서가 예약됨\"},{\"name\":\"BookReturned\",\"description\":\"회원이 대출 중이던 도서를 반납함. 반납일이 기록되고 도서의 상태가 변경됨.\",\"displayName\":\"도서가 반납됨\"},{\"name\":\"BookReturnOverdue\",\"description\":\"회원이 반납 예정일을 초과하여 도서를 반납함. 연체 이력이 기록됨.\",\"displayName\":\"도서가 연체되어 반납됨\"},{\"name\":\"LoanExtended\",\"description\":\"회원이 현재 대출 중인 도서에 대해 연장 신청하여 반납 예정일이 연장됨.\",\"displayName\":\"대출이 연장됨\"},{\"name\":\"LoanHistoryRecorded\",\"description\":\"도서별로 대출, 반납, 연장 등의 이력이 기록되어 도서의 대출 현황과 상태 변화 추적이 가능해짐.\",\"displayName\":\"대출 이력이 기록됨\"},{\"name\":\"BookStatusHistoryRecorded\",\"description\":\"도서의 상태(대출가능/대출중/예약중/폐기 등) 변경 이력이 별도로 기록되어 관리자가 이력 조회 가능.\",\"displayName\":\"도서 상태 변경 이력이 기록됨\"}]}"
                },
                "LoanHistory": {
                    "structure": [
                        {
                            "aggregate": {
                                "name": "LoanHistory",
                                "alias": "대출이력"
                            },
                            "enumerations": [
                                {
                                    "name": "LoanType",
                                    "alias": "대출이력타입"
                                }
                            ],
                            "valueObjects": [
                                {
                                    "name": "BookReference",
                                    "alias": "도서참조",
                                    "referencedAggregate": {
                                        "name": "Book",
                                        "alias": "도서"
                                    }
                                },
                                {
                                    "name": "Member",
                                    "alias": "회원"
                                }
                            ]
                        },
                        {
                            "aggregate": {
                                "name": "BookStatusHistory",
                                "alias": "도서상태변경이력"
                            },
                            "enumerations": [
                                {
                                    "name": "BookStatus",
                                    "alias": "도서상태"
                                }
                            ],
                            "valueObjects": [
                                {
                                    "name": "BookReference",
                                    "alias": "도서참조",
                                    "referencedAggregate": {
                                        "name": "Book",
                                        "alias": "도서"
                                    }
                                }
                            ]
                        }
                    ],
                    "pros": {
                        "cohesion": "대출이력과 상태변경이력 각각 도메인별 책임이 명확하게 분리되어, 각 Aggregate가 자신의 업무 규칙과 트랜잭션 일관성을 독립적으로 유지합니다.",
                        "coupling": "Book, Loan 등 외부 Aggregate는 참조 ValueObject로만 연결되어 직접 의존성이 낮아 전체 시스템 유연성이 높아집니다.",
                        "consistency": "각 이력별로 필수 불변조건(대출 이벤트, 상태 변경 이벤트)을 Aggregate 내부에서 원자적으로 보장할 수 있습니다.",
                        "encapsulation": "각각의 도메인 규칙이 별도 Aggregate 내부에 은닉되어 변경 영향이 최소화됩니다.",
                        "complexity": "업무별 Aggregate로 구조가 단순하며, 한 Aggregate만 파악해도 주요 로직을 이해할 수 있습니다.",
                        "independence": "이력 유형별 확장 및 변경이 독립적으로 가능하며, 운영 중에도 각 Aggregate의 독립 배포가 용이합니다.",
                        "performance": "이력 테이블이 분리되어 대량 데이터가 발생해도 각 쿼리 및 인덱스 설계가 최적화 가능합니다."
                    },
                    "cons": {
                        "cohesion": "도서별 전체 이력(대출+상태변경) 조회 시 두 Aggregate를 모두 질의해야 하므로 업무 관점의 완전한 단일성을 제공하지 않습니다.",
                        "coupling": "조회나 통계 등 복합 정보가 필요한 경우 두 Aggregate 간 데이터를 조합하는 추가 로직이 필요합니다.",
                        "consistency": "도서 대출 이벤트와 상태 변경이력이 동시에 발생하는 경우 트랜잭션 일관성 보장이 Aggregate 단위로 분리되어 있습니다.",
                        "encapsulation": "비즈니스 규칙이 분산되므로, 전체 이력 처리 로직을 한곳에서 변경하거나 관리하려면 여러 Aggregate를 모두 파악해야 합니다.",
                        "complexity": "대출과 상태변경 이벤트가 동시에 발생할 때 외부 오케스트레이션이 필요합니다.",
                        "independence": "이력 간 통합적 변경 요구가 생길 경우, 구조 재설계가 필요할 수 있습니다.",
                        "performance": "복합 이력 조회 쿼리는 다중 Aggregate 접근으로 인한 약간의 쿼리 비용 상승이 있을 수 있습니다."
                    },
                    "isAIRecommended": False,
                    "boundedContext": {
                        "_type": "org.uengine.modeling.model.BoundedContext",
                        "aggregates": [],
                        "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                        "description": "# Requirements\n\n## userStory\n\n각 도서별로 대출 이력과 상태 변경 이력을 조회할 수 있어야 하고, 이를 통해 도서의 대출 현황과 상태 변화를 추적할 수 있어야 해.\n\n## Event\n\n{\"name\":\"BookBorrowed\",\"displayName\":\"도서가 대출됨\",\"actor\":\"Member\",\"level\":4,\"description\":\"회원이 회원번호와 이름으로 인증 후 도서명 또는 ISBN으로 도서를 검색하여 대출 기간을 선택하고 대출 신청을 완료함.\",\"inputs\":[\"회원번호\",\"회원명\",\"도서 ID\",\"대출 기간(7/14/30일)\",\"도서 상태: 대출가능\"],\"outputs\":[\"도서 대출 기록 생성\",\"도서 상태: 대출중\"],\"nextEvents\":[\"BookStateChanged\",\"LoanHistoryRecorded\"]}\n\n## Event\n\n{\"name\":\"BookReturned\",\"displayName\":\"도서가 반납됨\",\"actor\":\"Member\",\"level\":6,\"description\":\"회원이 대출 중이던 도서를 반납함. 반납일이 기록되고 도서의 상태가 변경됨.\",\"inputs\":[\"회원번호\",\"도서 ID\",\"대출 기록\"],\"outputs\":[\"반납일 기록\",\"도서 상태: 대출가능(예약자 없을 시) 또는 예약중(예약자 있을 시)\"],\"nextEvents\":[\"BookStateChanged\",\"LoanHistoryRecorded\"]}\n\n## Event\n\n{\"name\":\"BookReturnOverdue\",\"displayName\":\"도서가 연체되어 반납됨\",\"actor\":\"Member\",\"level\":7,\"description\":\"회원이 반납 예정일을 초과하여 도서를 반납함. 연체 이력이 기록됨.\",\"inputs\":[\"회원번호\",\"도서 ID\",\"반납일 > 반납예정일\"],\"outputs\":[\"연체 기록\",\"도서 상태 변경\"],\"nextEvents\":[\"BookReturned\"]}\n\n## Event\n\n{\"name\":\"LoanExtended\",\"displayName\":\"대출이 연장됨\",\"actor\":\"Member\",\"level\":8,\"description\":\"회원이 현재 대출 중인 도서에 대해 연장 신청하여 반납 예정일이 연장됨.\",\"inputs\":[\"회원번호\",\"도서 ID\",\"대출 기록\",\"연장 조건 충족\"],\"outputs\":[\"반납 예정일 연장\",\"연장 이력 기록\"],\"nextEvents\":[\"LoanHistoryRecorded\"]}\n\n## Event\n\n{\"name\":\"LoanHistoryRecorded\",\"displayName\":\"대출 이력이 기록됨\",\"actor\":\"System\",\"level\":9,\"description\":\"도서별로 대출, 반납, 연장 등의 이력이 기록되어 도서의 대출 현황과 상태 변화 추적이 가능해짐.\",\"inputs\":[\"도서 ID\",\"이벤트 정보(대출/반납/연장/연체 등)\"],\"outputs\":[\"대출/반납/연장/연체 이력 데이터\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookStatusHistoryRecorded\",\"displayName\":\"도서 상태 변경 이력이 기록됨\",\"actor\":\"System\",\"level\":10,\"description\":\"도서의 상태(대출가능/대출중/예약중/폐기 등) 변경 이력이 별도로 기록되어 관리자가 이력 조회 가능.\",\"inputs\":[\"도서 ID\",\"이전 상태\",\"변경된 상태\",\"변경 일시\",\"변경 사유\"],\"outputs\":[\"도서 상태 변경 이력\"],\"nextEvents\":[]}",
                        "id": "dd3e4d7d-ed26-c3c3-670e-541e8723c9a1",
                        "elementView": {
                            "_type": "org.uengine.modeling.model.BoundedContext",
                            "height": 590,
                            "id": "dd3e4d7d-ed26-c3c3-670e-541e8723c9a1",
                            "style": "{}",
                            "width": 560,
                            "x": 1235,
                            "y": 450
                        },
                        "gitURL": None,
                        "hexagonalView": {
                            "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
                            "height": 350,
                            "id": "dd3e4d7d-ed26-c3c3-670e-541e8723c9a1",
                            "style": "{}",
                            "width": 350,
                            "x": 235,
                            "y": 365
                        },
                        "members": [],
                        "name": "LoanHistory",
                        "displayName": "대출이력",
                        "oldName": "",
                        "policies": [],
                        "portGenerated": 8080,
                        "preferredPlatform": "template-spring-boot",
                        "preferredPlatformConf": {},
                        "rotateStatus": False,
                        "tempId": "",
                        "templatePerElements": {},
                        "views": [],
                        "definitionId": "22901979210f3e4d4078ed657eee2155"
                    },
                    "description": "{\"userStories\":[{\"title\":\"도서별 대출 및 상태 변경 이력 조회\",\"description\":\"관리자 또는 이용자는 특정 도서의 대출 이력과 상태 변경 이력을 조회하여 도서의 대출 현황과 상태 변화를 한눈에 파악할 수 있다.\",\"acceptance\":[\"도서 ID로 대출 이력 및 상태 변경 이력을 모두 조회할 수 있다.\",\"대출, 반납, 연장, 연체 등 모든 대출 관련 이력이 포함된다.\",\"상태 변경 이력에는 변경 전/후 상태, 변경 일시, 사유가 명확히 표시된다.\",\"이력 데이터는 정렬/필터링이 가능하다.\"]}],\"entities\":{\"Book\":{\"properties\":[{\"name\":\"bookId\",\"type\":\"String\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"title\",\"type\":\"String\",\"required\":true},{\"name\":\"isbn\",\"type\":\"String\"},{\"name\":\"status\",\"type\":\"enum\",\"required\":true,\"values\":[\"AVAILABLE\",\"BORROWED\",\"RESERVED\",\"DISCARDED\"]}]},\"LoanHistory\":{\"properties\":[{\"name\":\"loanHistoryId\",\"type\":\"Long\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"bookId\",\"type\":\"String\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Book\"},{\"name\":\"memberId\",\"type\":\"String\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Member\"},{\"name\":\"loanType\",\"type\":\"enum\",\"required\":true,\"values\":[\"BORROW\",\"RETURN\",\"EXTEND\",\"OVERDUE\"]},{\"name\":\"loanStartDate\",\"type\":\"Date\"},{\"name\":\"loanDueDate\",\"type\":\"Date\"},{\"name\":\"returnDate\",\"type\":\"Date\"},{\"name\":\"overdueDays\",\"type\":\"Integer\"},{\"name\":\"createdAt\",\"type\":\"Date\",\"required\":true}]},\"BookStatusHistory\":{\"properties\":[{\"name\":\"statusHistoryId\",\"type\":\"Long\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"bookId\",\"type\":\"String\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Book\"},{\"name\":\"previousStatus\",\"type\":\"enum\",\"required\":true,\"values\":[\"AVAILABLE\",\"BORROWED\",\"RESERVED\",\"DISCARDED\"]},{\"name\":\"currentStatus\",\"type\":\"enum\",\"required\":true,\"values\":[\"AVAILABLE\",\"BORROWED\",\"RESERVED\",\"DISCARDED\"]},{\"name\":\"changedAt\",\"type\":\"Date\",\"required\":true},{\"name\":\"reason\",\"type\":\"String\"}]},\"Member\":{\"properties\":[{\"name\":\"memberId\",\"type\":\"String\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"memberName\",\"type\":\"String\",\"required\":true}]}},\"businessRules\":[{\"name\":\"대출 이력 기록\",\"description\":\"모든 도서 대출, 반납, 연장, 연체 발생 시 LoanHistory에 이력이 자동으로 기록된다.\"},{\"name\":\"상태 변경 이력 기록\",\"description\":\"도서 상태(AVAILABLE, BORROWED, RESERVED, DISCARDED)가 변경될 때마다 BookStatusHistory에 이전 상태, 변경된 상태, 일시, 사유가 저장된다.\"}],\"interfaces\":{\"BookHistoryLookup\":{\"sections\":[{\"name\":\"도서 이력 조회\",\"type\":\"form\",\"fields\":[{\"name\":\"bookId\",\"type\":\"text\",\"required\":true}],\"actions\":[\"이력 조회\"],\"filters\":[],\"resultTable\":{\"columns\":[],\"actions\":[]}},{\"name\":\"대출 이력 테이블\",\"type\":\"table\",\"fields\":[],\"actions\":[],\"filters\":[\"기간\",\"이력 타입(BORROW, RETURN, EXTEND, OVERDUE)\"],\"resultTable\":{\"columns\":[\"loanType\",\"memberId\",\"loanStartDate\",\"loanDueDate\",\"returnDate\",\"overdueDays\",\"createdAt\"],\"actions\":[]}},{\"name\":\"상태 변경 이력 테이블\",\"type\":\"table\",\"fields\":[],\"actions\":[],\"filters\":[\"기간\",\"상태\"],\"resultTable\":{\"columns\":[\"previousStatus\",\"currentStatus\",\"changedAt\",\"reason\"],\"actions\":[]}}]}},\"events\":[{\"name\":\"BookBorrowed\",\"description\":\"회원이 회원번호와 이름으로 인증 후 도서명 또는 ISBN으로 도서를 검색하여 대출 기간을 선택하고 대출 신청을 완료함.\",\"displayName\":\"도서가 대출됨\"},{\"name\":\"BookReturned\",\"description\":\"회원이 대출 중이던 도서를 반납함. 반납일이 기록되고 도서의 상태가 변경됨.\",\"displayName\":\"도서가 반납됨\"},{\"name\":\"BookReturnOverdue\",\"description\":\"회원이 반납 예정일을 초과하여 도서를 반납함. 연체 이력이 기록됨.\",\"displayName\":\"도서가 연체되어 반납됨\"},{\"name\":\"LoanExtended\",\"description\":\"회원이 현재 대출 중인 도서에 대해 연장 신청하여 반납 예정일이 연장됨.\",\"displayName\":\"대출이 연장됨\"},{\"name\":\"LoanHistoryRecorded\",\"description\":\"도서별로 대출, 반납, 연장 등의 이력이 기록되어 도서의 대출 현황과 상태 변화 추적이 가능해짐.\",\"displayName\":\"대출 이력이 기록됨\"},{\"name\":\"BookStatusHistoryRecorded\",\"description\":\"도서의 상태(대출가능/대출중/예약중/폐기 등) 변경 이력이 별도로 기록되어 관리자가 이력 조회 가능.\",\"displayName\":\"도서 상태 변경 이력이 기록됨\"}]}"
                }
            },
            current_generation=None,
            completed_generations=[
                {
                    "target_bounded_context": {
                        "name": "LibraryBookLoan",
                        "_type": "org.uengine.modeling.model.BoundedContext",
                        "aggregates": [],
                        "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                        "description": "# Requirements\n\n## userStory\n\n도서관의 도서 관리와 대출/반납을 통합적으로 관리하는 화면을 만들려고 해.\n\n## userStory\n\n'도서 관리' 화면에서는 새로운 도서를 등록하고 현재 보유한 도서들의 상태를 관리할 수 있어야 해. 도서 등록 시에는 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받아야 해. ISBN은 13자리 숫자여야 하고 중복 확인이 필요해. 카테고리는 소설/비소설/학술/잡지 중에서 선택할 수 있어야 해. 등록된 도서는 처음에 '대출가능' 상태가 되고, 이후 대출/반납 상황에 따라 '대출중', '예약중' 상태로 자동으로 변경되어야 해. 도서가 훼손되거나 분실된 경우 '폐기' 처리가 가능해야 하며, 폐기된 도서는 더 이상 대출이 불가능해야 해.\n\n## userStory\n\n'대출/반납' 화면에서는 회원이 도서를 대출하고 반납하는 것을 관리할 수 있어야 해. 대출 신청 시에는 회원번호와 이름으로 회원을 확인하고, 대출할 도서를 선택해야 해. 도서는 도서명이나 ISBN으로 검색할 수 있어야 해. 대출 기간은 7일/14일/30일 중에서 선택할 수 있어. 만약 대출하려는 도서가 이미 대출 중이라면, 예약 신청이 가능해야 해. 대출이 완료되면 해당 도서의 상태는 자동으로 '대출중'으로 변경되어야 해.\n\n## userStory\n\n대출 현황 화면에서는 현재 대출 중인 도서들의 목록을 볼 수 있어야 해. 각 대출 건에 대해 대출일, 반납예정일, 현재 상태(대출중/연체/반납완료)를 확인할 수 있어야 하고, 대출 중인 도서는 연장이나 반납 처리가 가능해야 해. 도서가 반납되면 자동으로 해당 도서의 상태가 '대출가능'으로 변경되어야 해. 만약 예약자가 있는 도서가 반납되면, 해당 도서는 '예약중' 상태로 변경되어야 해.\n\n## userStory\n\n각 도서별로 대출 이력과 상태 변경 이력을 조회할 수 있어야 하고, 이를 통해 도서의 대출 현황과 상태 변화를 추적할 수 있어야 해.\n\n## Event\n\n{\"name\":\"BookRegistered\",\"displayName\":\"도서가 등록됨\",\"actor\":\"Librarian\",\"level\":1,\"description\":\"사서가 도서명, ISBN, 저자, 출판사, 카테고리를 입력하여 신규 도서를 등록함. ISBN 중복 및 형식(13자리 숫자) 검증을 거침.\",\"inputs\":[\"도서명\",\"ISBN(13자리)\",\"저자\",\"출판사\",\"카테고리(소설/비소설/학술/잡지)\",\"ISBN 중복 아님\",\"ISBN 형식 유효\"],\"outputs\":[\"신규 도서 등록\",\"도서 상태: 대출가능\"],\"nextEvents\":[\"BookStateChanged\"]}\n\n## Event\n\n{\"name\":\"BookRegistrationFailedDueToDuplicateISBN\",\"displayName\":\"ISBN 중복으로 도서 등록 실패함\",\"actor\":\"Librarian\",\"level\":1,\"description\":\"도서 등록 시 입력한 ISBN이 기존에 이미 존재할 경우, 도서 등록이 실패함.\",\"inputs\":[\"ISBN(13자리)\",\"기존 도서에 동일 ISBN 존재\"],\"outputs\":[\"도서 등록 실패 알림\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookRegistrationFailedDueToInvalidISBNFormat\",\"displayName\":\"ISBN 형식 오류로 도서 등록 실패함\",\"actor\":\"Librarian\",\"level\":1,\"description\":\"도서 등록 시 입력한 ISBN이 13자리 숫자 형식이 아닐 경우, 도서 등록이 실패함.\",\"inputs\":[\"ISBN(13자리 아님)\"],\"outputs\":[\"도서 등록 실패 알림\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookStateChanged\",\"displayName\":\"도서 상태가 변경됨\",\"actor\":\"System\",\"level\":2,\"description\":\"도서의 상태가 비즈니스 프로세스(등록, 대출, 반납, 예약, 폐기)에 따라 변경됨.\",\"inputs\":[\"도서 ID\",\"변경 사유(등록, 대출, 반납, 예약, 폐기 등)\"],\"outputs\":[\"도서 상태 변경(대출가능/대출중/예약중/폐기)\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookDisposed\",\"displayName\":\"도서가 폐기됨\",\"actor\":\"Librarian\",\"level\":3,\"description\":\"사서가 도서가 훼손되거나 분실되었음을 확인하고 해당 도서를 폐기 처리함.\",\"inputs\":[\"도서 ID\",\"폐기 사유(훼손, 분실 등)\"],\"outputs\":[\"도서 상태: 폐기\",\"해당 도서 대출 불가\"],\"nextEvents\":[\"BookStateChanged\"]}\n\n## Event\n\n{\"name\":\"BookBorrowed\",\"displayName\":\"도서가 대출됨\",\"actor\":\"Member\",\"level\":4,\"description\":\"회원이 회원번호와 이름으로 인증 후 도서명 또는 ISBN으로 도서를 검색하여 대출 기간을 선택하고 대출 신청을 완료함.\",\"inputs\":[\"회원번호\",\"회원명\",\"도서 ID\",\"대출 기간(7/14/30일)\",\"도서 상태: 대출가능\"],\"outputs\":[\"도서 대출 기록 생성\",\"도서 상태: 대출중\"],\"nextEvents\":[\"BookStateChanged\",\"LoanHistoryRecorded\"]}\n\n## Event\n\n{\"name\":\"BookBorrowFailedDueToUnavailableBook\",\"displayName\":\"도서 대출 불가로 대출 실패함\",\"actor\":\"Member\",\"level\":4,\"description\":\"회원이 대출을 시도했으나 해당 도서가 이미 대출 중이어서 대출이 실패함.\",\"inputs\":[\"도서 ID\",\"도서 상태: 대출중/폐기\"],\"outputs\":[\"도서 대출 실패 알림\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookReserved\",\"displayName\":\"도서가 예약됨\",\"actor\":\"Member\",\"level\":5,\"description\":\"회원이 대출 중인 도서를 예약함. 예약자 정보와 예약 일시가 저장됨.\",\"inputs\":[\"회원번호\",\"회원명\",\"도서 ID\",\"도서 상태: 대출중\"],\"outputs\":[\"도서 예약 기록 생성\",\"도서 상태: 예약중(반납 시 자동 전환)\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookReturned\",\"displayName\":\"도서가 반납됨\",\"actor\":\"Member\",\"level\":6,\"description\":\"회원이 대출 중이던 도서를 반납함. 반납일이 기록되고 도서의 상태가 변경됨.\",\"inputs\":[\"회원번호\",\"도서 ID\",\"대출 기록\"],\"outputs\":[\"반납일 기록\",\"도서 상태: 대출가능(예약자 없을 시) 또는 예약중(예약자 있을 시)\"],\"nextEvents\":[\"BookStateChanged\",\"LoanHistoryRecorded\"]}\n\n## Event\n\n{\"name\":\"BookReturnOverdue\",\"displayName\":\"도서가 연체되어 반납됨\",\"actor\":\"Member\",\"level\":7,\"description\":\"회원이 반납 예정일을 초과하여 도서를 반납함. 연체 이력이 기록됨.\",\"inputs\":[\"회원번호\",\"도서 ID\",\"반납일 > 반납예정일\"],\"outputs\":[\"연체 기록\",\"도서 상태 변경\"],\"nextEvents\":[\"BookReturned\"]}\n\n## Event\n\n{\"name\":\"LoanExtended\",\"displayName\":\"대출이 연장됨\",\"actor\":\"Member\",\"level\":8,\"description\":\"회원이 현재 대출 중인 도서에 대해 연장 신청하여 반납 예정일이 연장됨.\",\"inputs\":[\"회원번호\",\"도서 ID\",\"대출 기록\",\"연장 조건 충족\"],\"outputs\":[\"반납 예정일 연장\",\"연장 이력 기록\"],\"nextEvents\":[\"LoanHistoryRecorded\"]}\n\n## Event\n\n{\"name\":\"LoanHistoryRecorded\",\"displayName\":\"대출 이력이 기록됨\",\"actor\":\"System\",\"level\":9,\"description\":\"도서별로 대출, 반납, 연장 등의 이력이 기록되어 도서의 대출 현황과 상태 변화 추적이 가능해짐.\",\"inputs\":[\"도서 ID\",\"이벤트 정보(대출/반납/연장/연체 등)\"],\"outputs\":[\"대출/반납/연장/연체 이력 데이터\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookStatusHistoryRecorded\",\"displayName\":\"도서 상태 변경 이력이 기록됨\",\"actor\":\"System\",\"level\":10,\"description\":\"도서의 상태(대출가능/대출중/예약중/폐기 등) 변경 이력이 별도로 기록되어 관리자가 이력 조회 가능.\",\"inputs\":[\"도서 ID\",\"이전 상태\",\"변경된 상태\",\"변경 일시\",\"변경 사유\"],\"outputs\":[\"도서 상태 변경 이력\"],\"nextEvents\":[]}",
                        "id": "6e671f4b-e55f-92b2-746d-4451c7d007cb",
                        "elementView": {
                            "_type": "org.uengine.modeling.model.BoundedContext",
                            "height": 590,
                            "id": "6e671f4b-e55f-92b2-746d-4451c7d007cb",
                            "style": "{}",
                            "width": 560,
                            "x": 650,
                            "y": 450
                        },
                        "gitURL": None,
                        "hexagonalView": {
                            "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
                            "height": 350,
                            "id": "6e671f4b-e55f-92b2-746d-4451c7d007cb",
                            "style": "{}",
                            "width": 350,
                            "x": 235,
                            "y": 365
                        },
                        "members": [],
                        "displayName": "도서관 도서대출",
                        "oldName": "",
                        "policies": [],
                        "portGenerated": None,
                        "preferredPlatform": "template-spring-boot",
                        "preferredPlatformConf": {},
                        "rotateStatus": False,
                        "tempId": "",
                        "templatePerElements": {},
                        "views": [],
                        "definitionId": "22901979210f3e4d4078ed657eee2155"
                    },
                    "target_aggregate": {
                        "name": "Book",
                        "alias": "도서"
                    },
                    "description": "{\"userStories\":[{\"title\":\"도서 등록 및 관리\",\"description\":\"사서로서 새로운 도서를 등록하고, 등록된 도서의 상태(대출가능, 대출중, 예약중, 폐기)를 관리할 수 있다.\",\"acceptance\":[\"도서명, ISBN, 저자, 출판사, 카테고리 입력 필수.\",\"ISBN은 13자리 숫자만 허용, 중복 불가.\",\"도서 등록 시 상태는 '대출가능'으로 설정.\",\"도서 상태 변경(대출, 반납, 예약, 폐기) 이력 추적 가능.\",\"도서가 폐기되면 대출 및 예약 불가.\"]},{\"title\":\"도서 대출 및 반납 처리\",\"description\":\"회원이 도서 대출/반납을 신청하고, 시스템은 대출 가능 여부를 판단하며 대출, 예약, 연체, 반납 등의 상태를 관리한다.\",\"acceptance\":[\"회원번호와 이름으로 회원 확인 필수.\",\"도서명 또는 ISBN으로 도서 검색 가능.\",\"대출 기간 7/14/30일 중 선택 가능.\",\"대출 중 도서는 예약 가능.\",\"대출 시 도서 상태는 자동으로 '대출중'으로 변경.\",\"반납 시 예약자가 있으면 '예약중', 없으면 '대출가능'으로 자동 전환.\",\"대출 연체 시 연체 이력 기록.\"]},{\"title\":\"대출 현황 및 연장/반납 처리\",\"description\":\"관리자는 현재 대출 중인 도서 현황을 확인하고, 각 건별로 연장 또는 반납 처리를 할 수 있다.\",\"acceptance\":[\"대출 중인 도서 목록, 대출일, 반납예정일, 상태(대출중/연체/반납완료) 표시.\",\"각 대출 건별 연장 또는 반납 버튼 제공.\",\"연장 시 반납예정일이 변경되고, 연장 이력이 기록됨.\",\"반납 시 도서 상태가 자동 변경됨.\"]},{\"title\":\"도서별 대출 및 상태 변경 이력 조회\",\"description\":\"관리자는 특정 도서의 대출 이력 및 상태 변경 이력을 조회하여 추적할 수 있다.\",\"acceptance\":[\"도서별 대출/반납/연장/연체 등 이력 리스트 제공.\",\"도서별 상태 변경 이력(변경일시, 변경 전/후 상태, 변경 사유) 제공.\"]}],\"entities\":{\"Book\":{\"properties\":[{\"name\":\"bookId\",\"type\":\"Long\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"title\",\"type\":\"String\",\"required\":true},{\"name\":\"isbn\",\"type\":\"String\",\"required\":true},{\"name\":\"author\",\"type\":\"String\",\"required\":true},{\"name\":\"publisher\",\"type\":\"String\",\"required\":true},{\"name\":\"category\",\"type\":\"enum\",\"required\":true,\"values\":[\"소설\",\"비소설\",\"학술\",\"잡지\"]},{\"name\":\"status\",\"type\":\"enum\",\"required\":true,\"values\":[\"대출가능\",\"대출중\",\"예약중\",\"폐기\"]}]},\"Member\":{\"properties\":[{\"name\":\"memberId\",\"type\":\"String\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"name\",\"type\":\"String\",\"required\":true}]},\"Loan\":{\"properties\":[{\"name\":\"loanId\",\"type\":\"Long\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"bookId\",\"type\":\"Long\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Book\"},{\"name\":\"memberId\",\"type\":\"String\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Member\"},{\"name\":\"loanDate\",\"type\":\"Date\",\"required\":true},{\"name\":\"dueDate\",\"type\":\"Date\",\"required\":true},{\"name\":\"returnDate\",\"type\":\"Date\"},{\"name\":\"status\",\"type\":\"enum\",\"required\":true,\"values\":[\"대출중\",\"연체\",\"반납완료\"]}]},\"Reservation\":{\"properties\":[{\"name\":\"reservationId\",\"type\":\"Long\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"bookId\",\"type\":\"Long\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Book\"},{\"name\":\"memberId\",\"type\":\"String\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Member\"},{\"name\":\"reservationDate\",\"type\":\"Date\",\"required\":true}]},\"BookStatusHistory\":{\"properties\":[{\"name\":\"historyId\",\"type\":\"Long\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"bookId\",\"type\":\"Long\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Book\"},{\"name\":\"previousStatus\",\"type\":\"String\",\"required\":true},{\"name\":\"currentStatus\",\"type\":\"String\",\"required\":true},{\"name\":\"changedAt\",\"type\":\"Date\",\"required\":true},{\"name\":\"reason\",\"type\":\"String\",\"required\":true}]},\"LoanHistory\":{\"properties\":[{\"name\":\"historyId\",\"type\":\"Long\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"bookId\",\"type\":\"Long\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Book\"},{\"name\":\"eventType\",\"type\":\"enum\",\"required\":true,\"values\":[\"대출\",\"반납\",\"연장\",\"연체\"]},{\"name\":\"eventDate\",\"type\":\"Date\",\"required\":true},{\"name\":\"memberId\",\"type\":\"String\",\"isForeignKey\":true,\"foreignEntity\":\"Member\"}]}},\"businessRules\":[{\"name\":\"ISBN 13자리 유효성 및 중복 검사\",\"description\":\"도서 등록 시 ISBN은 13자리 숫자이며, 기존 도서와 중복되어서는 안된다.\"},{\"name\":\"도서 상태 자동 전환\",\"description\":\"대출, 반납, 예약, 폐기 등 주요 이벤트 발생 시 도서 상태를 자동 변경한다.\"},{\"name\":\"폐기 도서 대출/예약 금지\",\"description\":\"도서 상태가 '폐기'일 경우, 대출 또는 예약 처리가 불가하다.\"},{\"name\":\"예약 우선 반영\",\"description\":\"반납 시 예약자가 있으면 도서 상태를 '예약중'으로 변경하며, 예약자에게 우선 대출이 가능하다.\"},{\"name\":\"대출 연장 조건\",\"description\":\"대출 중인 도서는 연장 가능하며, 연장 시 반납 예정일이 변경되고 연장 이력이 기록된다.\"}],\"interfaces\":{\"BookManagement\":{\"sections\":[{\"name\":\"도서 등록\",\"type\":\"form\",\"fields\":[{\"name\":\"title\",\"type\":\"text\",\"required\":true},{\"name\":\"isbn\",\"type\":\"text\",\"required\":true},{\"name\":\"author\",\"type\":\"text\",\"required\":true},{\"name\":\"publisher\",\"type\":\"text\",\"required\":true},{\"name\":\"category\",\"type\":\"select\",\"required\":true}],\"actions\":[\"도서 등록\"],\"filters\":[],\"resultTable\":{\"columns\":[],\"actions\":[]}},{\"name\":\"도서 현황\",\"type\":\"table\",\"fields\":[],\"actions\":[\"상태 변경\",\"폐기 처리\"],\"filters\":[\"카테고리\",\"상태\"],\"resultTable\":{\"columns\":[\"bookId\",\"title\",\"isbn\",\"author\",\"publisher\",\"category\",\"status\"],\"actions\":[\"상태 변경\",\"이력 조회\"]}}]},\"LoanAndReturn\":{\"sections\":[{\"name\":\"대출/반납 처리\",\"type\":\"form\",\"fields\":[{\"name\":\"memberId\",\"type\":\"text\",\"required\":true},{\"name\":\"name\",\"type\":\"text\",\"required\":true},{\"name\":\"bookSearch\",\"type\":\"search\",\"required\":true},{\"name\":\"loanPeriod\",\"type\":\"select\",\"required\":true}],\"actions\":[\"대출 신청\",\"반납 처리\",\"예약 신청\"],\"filters\":[],\"resultTable\":{\"columns\":[],\"actions\":[]}}]},\"LoanStatus\":{\"sections\":[{\"name\":\"대출 현황\",\"type\":\"table\",\"fields\":[],\"actions\":[\"연장\",\"반납\"],\"filters\":[\"대출상태\"],\"resultTable\":{\"columns\":[\"loanId\",\"bookId\",\"title\",\"memberId\",\"loanDate\",\"dueDate\",\"returnDate\",\"status\"],\"actions\":[\"연장\",\"반납\"]}}]},\"BookHistory\":{\"sections\":[{\"name\":\"대출 이력 조회\",\"type\":\"table\",\"fields\":[],\"actions\":[],\"filters\":[\"도서ID\"],\"resultTable\":{\"columns\":[\"historyId\",\"eventType\",\"eventDate\",\"memberId\"],\"actions\":[]}},{\"name\":\"상태 변경 이력 조회\",\"type\":\"table\",\"fields\":[],\"actions\":[],\"filters\":[\"도서ID\"],\"resultTable\":{\"columns\":[\"historyId\",\"previousStatus\",\"currentStatus\",\"changedAt\",\"reason\"],\"actions\":[]}}]}},\"events\":[{\"name\":\"BookRegistered\",\"description\":\"사서가 도서명, ISBN, 저자, 출판사, 카테고리를 입력하여 신규 도서를 등록함. ISBN 중복 및 형식(13자리 숫자) 검증을 거침.\",\"displayName\":\"도서가 등록됨\"},{\"name\":\"BookRegistrationFailedDueToDuplicateISBN\",\"description\":\"도서 등록 시 입력한 ISBN이 기존에 이미 존재할 경우, 도서 등록이 실패함.\",\"displayName\":\"ISBN 중복으로 도서 등록 실패함\"},{\"name\":\"BookRegistrationFailedDueToInvalidISBNFormat\",\"description\":\"도서 등록 시 입력한 ISBN이 13자리 숫자 형식이 아닐 경우, 도서 등록이 실패함.\",\"displayName\":\"ISBN 형식 오류로 도서 등록 실패함\"},{\"name\":\"BookStateChanged\",\"description\":\"도서의 상태가 비즈니스 프로세스(등록, 대출, 반납, 예약, 폐기)에 따라 변경됨.\",\"displayName\":\"도서 상태가 변경됨\"},{\"name\":\"BookDisposed\",\"description\":\"사서가 도서가 훼손되거나 분실되었음을 확인하고 해당 도서를 폐기 처리함.\",\"displayName\":\"도서가 폐기됨\"},{\"name\":\"BookBorrowed\",\"description\":\"회원이 회원번호와 이름으로 인증 후 도서명 또는 ISBN으로 도서를 검색하여 대출 기간을 선택하고 대출 신청을 완료함.\",\"displayName\":\"도서가 대출됨\"},{\"name\":\"BookBorrowFailedDueToUnavailableBook\",\"description\":\"회원이 대출을 시도했으나 해당 도서가 이미 대출 중이어서 대출이 실패함.\",\"displayName\":\"도서 대출 불가로 대출 실패함\"},{\"name\":\"BookReserved\",\"description\":\"회원이 대출 중인 도서를 예약함. 예약자 정보와 예약 일시가 저장됨.\",\"displayName\":\"도서가 예약됨\"},{\"name\":\"BookReturned\",\"description\":\"회원이 대출 중이던 도서를 반납함. 반납일이 기록되고 도서의 상태가 변경됨.\",\"displayName\":\"도서가 반납됨\"},{\"name\":\"BookReturnOverdue\",\"description\":\"회원이 반납 예정일을 초과하여 도서를 반납함. 연체 이력이 기록됨.\",\"displayName\":\"도서가 연체되어 반납됨\"},{\"name\":\"LoanExtended\",\"description\":\"회원이 현재 대출 중인 도서에 대해 연장 신청하여 반납 예정일이 연장됨.\",\"displayName\":\"대출이 연장됨\"},{\"name\":\"LoanHistoryRecorded\",\"description\":\"도서별로 대출, 반납, 연장 등의 이력이 기록되어 도서의 대출 현황과 상태 변화 추적이 가능해짐.\",\"displayName\":\"대출 이력이 기록됨\"},{\"name\":\"BookStatusHistoryRecorded\",\"description\":\"도서의 상태(대출가능/대출중/예약중/폐기 등) 변경 이력이 별도로 기록되어 관리자가 이력 조회 가능.\",\"displayName\":\"도서 상태 변경 이력이 기록됨\"}]}",
                    "draft_option": [
                        {
                            "aggregate": {
                                "name": "Book",
                                "alias": "도서"
                            },
                            "enumerations": [
                                {
                                    "name": "BookStatus",
                                    "alias": "도서상태"
                                },
                                {
                                    "name": "BookCategory",
                                    "alias": "도서카테고리"
                                }
                            ],
                            "valueObjects": []
                        }
                    ],
                    "summarized_es_value": {
                        "deletedProperties": [
                            "aggregate.commands",
                            "aggregate.events",
                            "aggregate.readModels"
                        ],
                        "boundedContexts": [
                            {
                                "id": "bc-libraryBookLoan",
                                "name": "LibraryBookLoan",
                                "actors": [],
                                "aggregates": []
                            },
                            {
                                "id": "bc-loanHistory",
                                "name": "LoanHistory",
                                "actors": [],
                                "aggregates": []
                            }
                        ]
                    },
                    "is_accumulated": False,
                    "retry_count": 0,
                    "created_actions": [
                        {
                            "objectType": "Aggregate",
                            "type": "create",
                            "ids": {
                                "boundedContextId": "6b5d96ec-a502-4242-a6d4-890ec1b2104e",
                                "aggregateId": "8e794426-f189-4559-8e36-0a8b457c3db9"
                            },
                            "args": {
                                "aggregateName": "Book",
                                "aggregateAlias": "도서",
                                "properties": [
                                    {
                                        "name": "bookId",
                                        "type": "Long",
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
                                    }
                                ]
                            },
                            "actionName": "CreateBookAggregate"
                        },
                        {
                            "objectType": "Enumeration",
                            "type": "create",
                            "ids": {
                                "boundedContextId": "6b5d96ec-a502-4242-a6d4-890ec1b2104e",
                                "aggregateId": "8e794426-f189-4559-8e36-0a8b457c3db9",
                                "enumerationId": "80a5e04e-bd4d-4387-b5dc-25b6d79a5089"
                            },
                            "args": {
                                "enumerationName": "BookStatus",
                                "enumerationAlias": "도서상태",
                                "properties": [
                                    {
                                        "name": "AVAILABLE"
                                    },
                                    {
                                        "name": "BORROWED"
                                    },
                                    {
                                        "name": "RESERVED"
                                    },
                                    {
                                        "name": "DISPOSED"
                                    }
                                ]
                            },
                            "actionName": "CreateBookStatusEnum"
                        },
                        {
                            "objectType": "Enumeration",
                            "type": "create",
                            "ids": {
                                "boundedContextId": "6b5d96ec-a502-4242-a6d4-890ec1b2104e",
                                "aggregateId": "8e794426-f189-4559-8e36-0a8b457c3db9",
                                "enumerationId": "a50b5105-1d52-4925-bcb2-f4899b109978"
                            },
                            "args": {
                                "enumerationName": "BookCategory",
                                "enumerationAlias": "도서카테고리",
                                "properties": [
                                    {
                                        "name": "NOVEL"
                                    },
                                    {
                                        "name": "NONFICTION"
                                    },
                                    {
                                        "name": "ACADEMIC"
                                    },
                                    {
                                        "name": "MAGAZINE"
                                    }
                                ]
                            },
                            "actionName": "CreateBookCategoryEnum"
                        }
                    ],
                    "generation_complete": True
                },
                {
                    "target_bounded_context": {
                        "name": "LoanHistory",
                        "_type": "org.uengine.modeling.model.BoundedContext",
                        "aggregates": [],
                        "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                        "description": "# Requirements\n\n## userStory\n\n각 도서별로 대출 이력과 상태 변경 이력을 조회할 수 있어야 하고, 이를 통해 도서의 대출 현황과 상태 변화를 추적할 수 있어야 해.\n\n## Event\n\n{\"name\":\"BookBorrowed\",\"displayName\":\"도서가 대출됨\",\"actor\":\"Member\",\"level\":4,\"description\":\"회원이 회원번호와 이름으로 인증 후 도서명 또는 ISBN으로 도서를 검색하여 대출 기간을 선택하고 대출 신청을 완료함.\",\"inputs\":[\"회원번호\",\"회원명\",\"도서 ID\",\"대출 기간(7/14/30일)\",\"도서 상태: 대출가능\"],\"outputs\":[\"도서 대출 기록 생성\",\"도서 상태: 대출중\"],\"nextEvents\":[\"BookStateChanged\",\"LoanHistoryRecorded\"]}\n\n## Event\n\n{\"name\":\"BookReturned\",\"displayName\":\"도서가 반납됨\",\"actor\":\"Member\",\"level\":6,\"description\":\"회원이 대출 중이던 도서를 반납함. 반납일이 기록되고 도서의 상태가 변경됨.\",\"inputs\":[\"회원번호\",\"도서 ID\",\"대출 기록\"],\"outputs\":[\"반납일 기록\",\"도서 상태: 대출가능(예약자 없을 시) 또는 예약중(예약자 있을 시)\"],\"nextEvents\":[\"BookStateChanged\",\"LoanHistoryRecorded\"]}\n\n## Event\n\n{\"name\":\"BookReturnOverdue\",\"displayName\":\"도서가 연체되어 반납됨\",\"actor\":\"Member\",\"level\":7,\"description\":\"회원이 반납 예정일을 초과하여 도서를 반납함. 연체 이력이 기록됨.\",\"inputs\":[\"회원번호\",\"도서 ID\",\"반납일 > 반납예정일\"],\"outputs\":[\"연체 기록\",\"도서 상태 변경\"],\"nextEvents\":[\"BookReturned\"]}\n\n## Event\n\n{\"name\":\"LoanExtended\",\"displayName\":\"대출이 연장됨\",\"actor\":\"Member\",\"level\":8,\"description\":\"회원이 현재 대출 중인 도서에 대해 연장 신청하여 반납 예정일이 연장됨.\",\"inputs\":[\"회원번호\",\"도서 ID\",\"대출 기록\",\"연장 조건 충족\"],\"outputs\":[\"반납 예정일 연장\",\"연장 이력 기록\"],\"nextEvents\":[\"LoanHistoryRecorded\"]}\n\n## Event\n\n{\"name\":\"LoanHistoryRecorded\",\"displayName\":\"대출 이력이 기록됨\",\"actor\":\"System\",\"level\":9,\"description\":\"도서별로 대출, 반납, 연장 등의 이력이 기록되어 도서의 대출 현황과 상태 변화 추적이 가능해짐.\",\"inputs\":[\"도서 ID\",\"이벤트 정보(대출/반납/연장/연체 등)\"],\"outputs\":[\"대출/반납/연장/연체 이력 데이터\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookStatusHistoryRecorded\",\"displayName\":\"도서 상태 변경 이력이 기록됨\",\"actor\":\"System\",\"level\":10,\"description\":\"도서의 상태(대출가능/대출중/예약중/폐기 등) 변경 이력이 별도로 기록되어 관리자가 이력 조회 가능.\",\"inputs\":[\"도서 ID\",\"이전 상태\",\"변경된 상태\",\"변경 일시\",\"변경 사유\"],\"outputs\":[\"도서 상태 변경 이력\"],\"nextEvents\":[]}",
                        "id": "dd3e4d7d-ed26-c3c3-670e-541e8723c9a1",
                        "elementView": {
                            "_type": "org.uengine.modeling.model.BoundedContext",
                            "height": 590,
                            "id": "dd3e4d7d-ed26-c3c3-670e-541e8723c9a1",
                            "style": "{}",
                            "width": 560,
                            "x": 1235,
                            "y": 450
                        },
                        "gitURL": None,
                        "hexagonalView": {
                            "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
                            "height": 350,
                            "id": "dd3e4d7d-ed26-c3c3-670e-541e8723c9a1",
                            "style": "{}",
                            "width": 350,
                            "x": 235,
                            "y": 365
                        },
                        "members": [],
                        "displayName": "대출이력",
                        "oldName": "",
                        "policies": [],
                        "portGenerated": 8080,
                        "preferredPlatform": "template-spring-boot",
                        "preferredPlatformConf": {},
                        "rotateStatus": False,
                        "tempId": "",
                        "templatePerElements": {},
                        "views": [],
                        "definitionId": "22901979210f3e4d4078ed657eee2155"
                    },
                    "target_aggregate": {
                        "name": "LoanHistory",
                        "alias": "대출이력"
                    },
                    "description": "{\"userStories\":[{\"title\":\"도서별 대출 및 상태 변경 이력 조회\",\"description\":\"관리자 또는 이용자는 특정 도서의 대출 이력과 상태 변경 이력을 조회하여 도서의 대출 현황과 상태 변화를 한눈에 파악할 수 있다.\",\"acceptance\":[\"도서 ID로 대출 이력 및 상태 변경 이력을 모두 조회할 수 있다.\",\"대출, 반납, 연장, 연체 등 모든 대출 관련 이력이 포함된다.\",\"상태 변경 이력에는 변경 전/후 상태, 변경 일시, 사유가 명확히 표시된다.\",\"이력 데이터는 정렬/필터링이 가능하다.\"]}],\"entities\":{\"Book\":{\"properties\":[{\"name\":\"bookId\",\"type\":\"String\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"title\",\"type\":\"String\",\"required\":true},{\"name\":\"isbn\",\"type\":\"String\"},{\"name\":\"status\",\"type\":\"enum\",\"required\":true,\"values\":[\"AVAILABLE\",\"BORROWED\",\"RESERVED\",\"DISCARDED\"]}]},\"LoanHistory\":{\"properties\":[{\"name\":\"loanHistoryId\",\"type\":\"Long\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"bookId\",\"type\":\"String\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Book\"},{\"name\":\"memberId\",\"type\":\"String\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Member\"},{\"name\":\"loanType\",\"type\":\"enum\",\"required\":true,\"values\":[\"BORROW\",\"RETURN\",\"EXTEND\",\"OVERDUE\"]},{\"name\":\"loanStartDate\",\"type\":\"Date\"},{\"name\":\"loanDueDate\",\"type\":\"Date\"},{\"name\":\"returnDate\",\"type\":\"Date\"},{\"name\":\"overdueDays\",\"type\":\"Integer\"},{\"name\":\"createdAt\",\"type\":\"Date\",\"required\":true}]},\"BookStatusHistory\":{\"properties\":[{\"name\":\"statusHistoryId\",\"type\":\"Long\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"bookId\",\"type\":\"String\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Book\"},{\"name\":\"previousStatus\",\"type\":\"enum\",\"required\":true,\"values\":[\"AVAILABLE\",\"BORROWED\",\"RESERVED\",\"DISCARDED\"]},{\"name\":\"currentStatus\",\"type\":\"enum\",\"required\":true,\"values\":[\"AVAILABLE\",\"BORROWED\",\"RESERVED\",\"DISCARDED\"]},{\"name\":\"changedAt\",\"type\":\"Date\",\"required\":true},{\"name\":\"reason\",\"type\":\"String\"}]},\"Member\":{\"properties\":[{\"name\":\"memberId\",\"type\":\"String\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"memberName\",\"type\":\"String\",\"required\":true}]}},\"businessRules\":[{\"name\":\"대출 이력 기록\",\"description\":\"모든 도서 대출, 반납, 연장, 연체 발생 시 LoanHistory에 이력이 자동으로 기록된다.\"},{\"name\":\"상태 변경 이력 기록\",\"description\":\"도서 상태(AVAILABLE, BORROWED, RESERVED, DISCARDED)가 변경될 때마다 BookStatusHistory에 이전 상태, 변경된 상태, 일시, 사유가 저장된다.\"}],\"interfaces\":{\"BookHistoryLookup\":{\"sections\":[{\"name\":\"도서 이력 조회\",\"type\":\"form\",\"fields\":[{\"name\":\"bookId\",\"type\":\"text\",\"required\":true}],\"actions\":[\"이력 조회\"],\"filters\":[],\"resultTable\":{\"columns\":[],\"actions\":[]}},{\"name\":\"대출 이력 테이블\",\"type\":\"table\",\"fields\":[],\"actions\":[],\"filters\":[\"기간\",\"이력 타입(BORROW, RETURN, EXTEND, OVERDUE)\"],\"resultTable\":{\"columns\":[\"loanType\",\"memberId\",\"loanStartDate\",\"loanDueDate\",\"returnDate\",\"overdueDays\",\"createdAt\"],\"actions\":[]}},{\"name\":\"상태 변경 이력 테이블\",\"type\":\"table\",\"fields\":[],\"actions\":[],\"filters\":[\"기간\",\"상태\"],\"resultTable\":{\"columns\":[\"previousStatus\",\"currentStatus\",\"changedAt\",\"reason\"],\"actions\":[]}}]}},\"events\":[{\"name\":\"BookBorrowed\",\"description\":\"회원이 회원번호와 이름으로 인증 후 도서명 또는 ISBN으로 도서를 검색하여 대출 기간을 선택하고 대출 신청을 완료함.\",\"displayName\":\"도서가 대출됨\"},{\"name\":\"BookReturned\",\"description\":\"회원이 대출 중이던 도서를 반납함. 반납일이 기록되고 도서의 상태가 변경됨.\",\"displayName\":\"도서가 반납됨\"},{\"name\":\"BookReturnOverdue\",\"description\":\"회원이 반납 예정일을 초과하여 도서를 반납함. 연체 이력이 기록됨.\",\"displayName\":\"도서가 연체되어 반납됨\"},{\"name\":\"LoanExtended\",\"description\":\"회원이 현재 대출 중인 도서에 대해 연장 신청하여 반납 예정일이 연장됨.\",\"displayName\":\"대출이 연장됨\"},{\"name\":\"LoanHistoryRecorded\",\"description\":\"도서별로 대출, 반납, 연장 등의 이력이 기록되어 도서의 대출 현황과 상태 변화 추적이 가능해짐.\",\"displayName\":\"대출 이력이 기록됨\"},{\"name\":\"BookStatusHistoryRecorded\",\"description\":\"도서의 상태(대출가능/대출중/예약중/폐기 등) 변경 이력이 별도로 기록되어 관리자가 이력 조회 가능.\",\"displayName\":\"도서 상태 변경 이력이 기록됨\"}]}",
                    "draft_option": [
                        {
                            "aggregate": {
                                "name": "LoanHistory",
                                "alias": "대출이력"
                            },
                            "enumerations": [
                                {
                                    "name": "LoanType",
                                    "alias": "대출이력타입"
                                }
                            ],
                            "valueObjects": [
                                {
                                    "name": "Member",
                                    "alias": "회원"
                                }
                            ]
                        }
                    ],
                    "summarized_es_value": {
                        "deletedProperties": [
                            "aggregate.commands",
                            "aggregate.events",
                            "aggregate.readModels"
                        ],
                        "boundedContexts": [
                            {
                                "id": "bc-libraryBookLoan",
                                "name": "LibraryBookLoan",
                                "actors": [],
                                "aggregates": [
                                    {
                                        "id": "agg-book",
                                        "name": "Book",
                                        "properties": [
                                            {
                                                "name": "bookId",
                                                "type": "Long",
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
                                            }
                                        ],
                                        "entities": [],
                                        "enumerations": [
                                            {
                                                "id": "enum-bookStatus",
                                                "name": "BookStatus",
                                                "items": [
                                                    "AVAILABLE",
                                                    "BORROWED",
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
                                        "valueObjects": []
                                    }
                                ]
                            },
                            {
                                "id": "bc-loanHistory",
                                "name": "LoanHistory",
                                "actors": [],
                                "aggregates": []
                            }
                        ]
                    },
                    "is_accumulated": False,
                    "retry_count": 0,
                    "created_actions": [
                        {
                            "objectType": "Aggregate",
                            "type": "create",
                            "ids": {
                                "boundedContextId": "c517babe-52fb-48ba-8920-60df60b3da1e",
                                "aggregateId": "b352b64a-a49d-4704-b27f-e532280568d8"
                            },
                            "args": {
                                "aggregateName": "LoanHistory",
                                "aggregateAlias": "대출이력",
                                "properties": [
                                    {
                                        "name": "loanHistoryId",
                                        "type": "Long",
                                        "isKey": True
                                    },
                                    {
                                        "name": "bookId"
                                    },
                                    {
                                        "name": "member",
                                        "type": "Member"
                                    },
                                    {
                                        "name": "loanType",
                                        "type": "LoanType"
                                    },
                                    {
                                        "name": "loanStartDate",
                                        "type": "Date"
                                    },
                                    {
                                        "name": "loanDueDate",
                                        "type": "Date"
                                    },
                                    {
                                        "name": "returnDate",
                                        "type": "Date"
                                    },
                                    {
                                        "name": "overdueDays",
                                        "type": "Integer"
                                    },
                                    {
                                        "name": "createdAt",
                                        "type": "Date"
                                    }
                                ]
                            },
                            "actionName": "CreateLoanHistoryAggregate"
                        },
                        {
                            "objectType": "ValueObject",
                            "type": "create",
                            "ids": {
                                "boundedContextId": "c517babe-52fb-48ba-8920-60df60b3da1e",
                                "aggregateId": "b352b64a-a49d-4704-b27f-e532280568d8",
                                "valueObjectId": "8e253425-bdeb-4a21-8277-57ef1e071f75"
                            },
                            "args": {
                                "valueObjectName": "Member",
                                "valueObjectAlias": "회원",
                                "properties": [
                                    {
                                        "name": "memberId"
                                    },
                                    {
                                        "name": "memberName"
                                    }
                                ]
                            },
                            "actionName": "CreateMemberVO"
                        },
                        {
                            "objectType": "Enumeration",
                            "type": "create",
                            "ids": {
                                "boundedContextId": "c517babe-52fb-48ba-8920-60df60b3da1e",
                                "aggregateId": "b352b64a-a49d-4704-b27f-e532280568d8",
                                "enumerationId": "cdeaf14e-572c-4e47-a997-6a831bbae718"
                            },
                            "args": {
                                "enumerationName": "LoanType",
                                "enumerationAlias": "대출이력타입",
                                "properties": [
                                    {
                                        "name": "BORROW"
                                    },
                                    {
                                        "name": "RETURN"
                                    },
                                    {
                                        "name": "EXTEND"
                                    },
                                    {
                                        "name": "OVERDUE"
                                    }
                                ]
                            },
                            "actionName": "CreateLoanTypeEnum"
                        }
                    ],
                    "generation_complete": True
                },
                {
                    "target_bounded_context": {
                        "name": "LoanHistory",
                        "_type": "org.uengine.modeling.model.BoundedContext",
                        "aggregates": [],
                        "author": "EYCl46CwWAWvpz2E1BCUpVgPIpa2",
                        "description": "# Requirements\n\n## userStory\n\n각 도서별로 대출 이력과 상태 변경 이력을 조회할 수 있어야 하고, 이를 통해 도서의 대출 현황과 상태 변화를 추적할 수 있어야 해.\n\n## Event\n\n{\"name\":\"BookBorrowed\",\"displayName\":\"도서가 대출됨\",\"actor\":\"Member\",\"level\":4,\"description\":\"회원이 회원번호와 이름으로 인증 후 도서명 또는 ISBN으로 도서를 검색하여 대출 기간을 선택하고 대출 신청을 완료함.\",\"inputs\":[\"회원번호\",\"회원명\",\"도서 ID\",\"대출 기간(7/14/30일)\",\"도서 상태: 대출가능\"],\"outputs\":[\"도서 대출 기록 생성\",\"도서 상태: 대출중\"],\"nextEvents\":[\"BookStateChanged\",\"LoanHistoryRecorded\"]}\n\n## Event\n\n{\"name\":\"BookReturned\",\"displayName\":\"도서가 반납됨\",\"actor\":\"Member\",\"level\":6,\"description\":\"회원이 대출 중이던 도서를 반납함. 반납일이 기록되고 도서의 상태가 변경됨.\",\"inputs\":[\"회원번호\",\"도서 ID\",\"대출 기록\"],\"outputs\":[\"반납일 기록\",\"도서 상태: 대출가능(예약자 없을 시) 또는 예약중(예약자 있을 시)\"],\"nextEvents\":[\"BookStateChanged\",\"LoanHistoryRecorded\"]}\n\n## Event\n\n{\"name\":\"BookReturnOverdue\",\"displayName\":\"도서가 연체되어 반납됨\",\"actor\":\"Member\",\"level\":7,\"description\":\"회원이 반납 예정일을 초과하여 도서를 반납함. 연체 이력이 기록됨.\",\"inputs\":[\"회원번호\",\"도서 ID\",\"반납일 > 반납예정일\"],\"outputs\":[\"연체 기록\",\"도서 상태 변경\"],\"nextEvents\":[\"BookReturned\"]}\n\n## Event\n\n{\"name\":\"LoanExtended\",\"displayName\":\"대출이 연장됨\",\"actor\":\"Member\",\"level\":8,\"description\":\"회원이 현재 대출 중인 도서에 대해 연장 신청하여 반납 예정일이 연장됨.\",\"inputs\":[\"회원번호\",\"도서 ID\",\"대출 기록\",\"연장 조건 충족\"],\"outputs\":[\"반납 예정일 연장\",\"연장 이력 기록\"],\"nextEvents\":[\"LoanHistoryRecorded\"]}\n\n## Event\n\n{\"name\":\"LoanHistoryRecorded\",\"displayName\":\"대출 이력이 기록됨\",\"actor\":\"System\",\"level\":9,\"description\":\"도서별로 대출, 반납, 연장 등의 이력이 기록되어 도서의 대출 현황과 상태 변화 추적이 가능해짐.\",\"inputs\":[\"도서 ID\",\"이벤트 정보(대출/반납/연장/연체 등)\"],\"outputs\":[\"대출/반납/연장/연체 이력 데이터\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookStatusHistoryRecorded\",\"displayName\":\"도서 상태 변경 이력이 기록됨\",\"actor\":\"System\",\"level\":10,\"description\":\"도서의 상태(대출가능/대출중/예약중/폐기 등) 변경 이력이 별도로 기록되어 관리자가 이력 조회 가능.\",\"inputs\":[\"도서 ID\",\"이전 상태\",\"변경된 상태\",\"변경 일시\",\"변경 사유\"],\"outputs\":[\"도서 상태 변경 이력\"],\"nextEvents\":[]}",
                        "id": "dd3e4d7d-ed26-c3c3-670e-541e8723c9a1",
                        "elementView": {
                            "_type": "org.uengine.modeling.model.BoundedContext",
                            "height": 590,
                            "id": "dd3e4d7d-ed26-c3c3-670e-541e8723c9a1",
                            "style": "{}",
                            "width": 560,
                            "x": 1235,
                            "y": 450
                        },
                        "gitURL": None,
                        "hexagonalView": {
                            "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
                            "height": 350,
                            "id": "dd3e4d7d-ed26-c3c3-670e-541e8723c9a1",
                            "style": "{}",
                            "width": 350,
                            "x": 235,
                            "y": 365
                        },
                        "members": [],
                        "displayName": "대출이력",
                        "oldName": "",
                        "policies": [],
                        "portGenerated": 8080,
                        "preferredPlatform": "template-spring-boot",
                        "preferredPlatformConf": {},
                        "rotateStatus": False,
                        "tempId": "",
                        "templatePerElements": {},
                        "views": [],
                        "definitionId": "22901979210f3e4d4078ed657eee2155"
                    },
                    "target_aggregate": {
                        "name": "BookStatusHistory",
                        "alias": "도서상태변경이력"
                    },
                    "description": "{\"userStories\":[{\"title\":\"도서별 대출 및 상태 변경 이력 조회\",\"description\":\"관리자 또는 이용자는 특정 도서의 대출 이력과 상태 변경 이력을 조회하여 도서의 대출 현황과 상태 변화를 한눈에 파악할 수 있다.\",\"acceptance\":[\"도서 ID로 대출 이력 및 상태 변경 이력을 모두 조회할 수 있다.\",\"대출, 반납, 연장, 연체 등 모든 대출 관련 이력이 포함된다.\",\"상태 변경 이력에는 변경 전/후 상태, 변경 일시, 사유가 명확히 표시된다.\",\"이력 데이터는 정렬/필터링이 가능하다.\"]}],\"entities\":{\"Book\":{\"properties\":[{\"name\":\"bookId\",\"type\":\"String\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"title\",\"type\":\"String\",\"required\":true},{\"name\":\"isbn\",\"type\":\"String\"},{\"name\":\"status\",\"type\":\"enum\",\"required\":true,\"values\":[\"AVAILABLE\",\"BORROWED\",\"RESERVED\",\"DISCARDED\"]}]},\"LoanHistory\":{\"properties\":[{\"name\":\"loanHistoryId\",\"type\":\"Long\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"bookId\",\"type\":\"String\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Book\"},{\"name\":\"memberId\",\"type\":\"String\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Member\"},{\"name\":\"loanType\",\"type\":\"enum\",\"required\":true,\"values\":[\"BORROW\",\"RETURN\",\"EXTEND\",\"OVERDUE\"]},{\"name\":\"loanStartDate\",\"type\":\"Date\"},{\"name\":\"loanDueDate\",\"type\":\"Date\"},{\"name\":\"returnDate\",\"type\":\"Date\"},{\"name\":\"overdueDays\",\"type\":\"Integer\"},{\"name\":\"createdAt\",\"type\":\"Date\",\"required\":true}]},\"BookStatusHistory\":{\"properties\":[{\"name\":\"statusHistoryId\",\"type\":\"Long\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"bookId\",\"type\":\"String\",\"required\":true,\"isForeignKey\":true,\"foreignEntity\":\"Book\"},{\"name\":\"previousStatus\",\"type\":\"enum\",\"required\":true,\"values\":[\"AVAILABLE\",\"BORROWED\",\"RESERVED\",\"DISCARDED\"]},{\"name\":\"currentStatus\",\"type\":\"enum\",\"required\":true,\"values\":[\"AVAILABLE\",\"BORROWED\",\"RESERVED\",\"DISCARDED\"]},{\"name\":\"changedAt\",\"type\":\"Date\",\"required\":true},{\"name\":\"reason\",\"type\":\"String\"}]},\"Member\":{\"properties\":[{\"name\":\"memberId\",\"type\":\"String\",\"required\":true,\"isPrimaryKey\":true},{\"name\":\"memberName\",\"type\":\"String\",\"required\":true}]}},\"businessRules\":[{\"name\":\"대출 이력 기록\",\"description\":\"모든 도서 대출, 반납, 연장, 연체 발생 시 LoanHistory에 이력이 자동으로 기록된다.\"},{\"name\":\"상태 변경 이력 기록\",\"description\":\"도서 상태(AVAILABLE, BORROWED, RESERVED, DISCARDED)가 변경될 때마다 BookStatusHistory에 이전 상태, 변경된 상태, 일시, 사유가 저장된다.\"}],\"interfaces\":{\"BookHistoryLookup\":{\"sections\":[{\"name\":\"도서 이력 조회\",\"type\":\"form\",\"fields\":[{\"name\":\"bookId\",\"type\":\"text\",\"required\":true}],\"actions\":[\"이력 조회\"],\"filters\":[],\"resultTable\":{\"columns\":[],\"actions\":[]}},{\"name\":\"대출 이력 테이블\",\"type\":\"table\",\"fields\":[],\"actions\":[],\"filters\":[\"기간\",\"이력 타입(BORROW, RETURN, EXTEND, OVERDUE)\"],\"resultTable\":{\"columns\":[\"loanType\",\"memberId\",\"loanStartDate\",\"loanDueDate\",\"returnDate\",\"overdueDays\",\"createdAt\"],\"actions\":[]}},{\"name\":\"상태 변경 이력 테이블\",\"type\":\"table\",\"fields\":[],\"actions\":[],\"filters\":[\"기간\",\"상태\"],\"resultTable\":{\"columns\":[\"previousStatus\",\"currentStatus\",\"changedAt\",\"reason\"],\"actions\":[]}}]}},\"events\":[{\"name\":\"BookBorrowed\",\"description\":\"회원이 회원번호와 이름으로 인증 후 도서명 또는 ISBN으로 도서를 검색하여 대출 기간을 선택하고 대출 신청을 완료함.\",\"displayName\":\"도서가 대출됨\"},{\"name\":\"BookReturned\",\"description\":\"회원이 대출 중이던 도서를 반납함. 반납일이 기록되고 도서의 상태가 변경됨.\",\"displayName\":\"도서가 반납됨\"},{\"name\":\"BookReturnOverdue\",\"description\":\"회원이 반납 예정일을 초과하여 도서를 반납함. 연체 이력이 기록됨.\",\"displayName\":\"도서가 연체되어 반납됨\"},{\"name\":\"LoanExtended\",\"description\":\"회원이 현재 대출 중인 도서에 대해 연장 신청하여 반납 예정일이 연장됨.\",\"displayName\":\"대출이 연장됨\"},{\"name\":\"LoanHistoryRecorded\",\"description\":\"도서별로 대출, 반납, 연장 등의 이력이 기록되어 도서의 대출 현황과 상태 변화 추적이 가능해짐.\",\"displayName\":\"대출 이력이 기록됨\"},{\"name\":\"BookStatusHistoryRecorded\",\"description\":\"도서의 상태(대출가능/대출중/예약중/폐기 등) 변경 이력이 별도로 기록되어 관리자가 이력 조회 가능.\",\"displayName\":\"도서 상태 변경 이력이 기록됨\"}]}",
                    "draft_option": [
                        {
                            "aggregate": {
                                "name": "BookStatusHistory",
                                "alias": "도서상태변경이력"
                            },
                            "enumerations": [
                                {
                                    "name": "BookStatus",
                                    "alias": "도서상태"
                                }
                            ],
                            "valueObjects": []
                        }
                    ],
                    "summarized_es_value": {
                        "deletedProperties": [
                            "aggregate.commands",
                            "aggregate.events",
                            "aggregate.readModels"
                        ],
                        "boundedContexts": [
                            {
                                "id": "bc-libraryBookLoan",
                                "name": "LibraryBookLoan",
                                "actors": [],
                                "aggregates": [
                                    {
                                        "id": "agg-book",
                                        "name": "Book",
                                        "properties": [
                                            {
                                                "name": "bookId",
                                                "type": "Long",
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
                                            }
                                        ],
                                        "entities": [],
                                        "enumerations": [
                                            {
                                                "id": "enum-bookStatus",
                                                "name": "BookStatus",
                                                "items": [
                                                    "AVAILABLE",
                                                    "BORROWED",
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
                                        "valueObjects": []
                                    }
                                ]
                            },
                            {
                                "id": "bc-loanHistory",
                                "name": "LoanHistory",
                                "actors": [],
                                "aggregates": [
                                    {
                                        "id": "agg-loanHistory",
                                        "name": "LoanHistory",
                                        "properties": [
                                            {
                                                "name": "loanHistoryId",
                                                "type": "Long",
                                                "isKey": True
                                            },
                                            {
                                                "name": "bookId"
                                            },
                                            {
                                                "name": "member",
                                                "type": "Member"
                                            },
                                            {
                                                "name": "loanType",
                                                "type": "LoanType"
                                            },
                                            {
                                                "name": "loanStartDate",
                                                "type": "Date"
                                            },
                                            {
                                                "name": "loanDueDate",
                                                "type": "Date"
                                            },
                                            {
                                                "name": "returnDate",
                                                "type": "Date"
                                            },
                                            {
                                                "name": "overdueDays",
                                                "type": "Integer"
                                            },
                                            {
                                                "name": "createdAt",
                                                "type": "Date"
                                            }
                                        ],
                                        "entities": [],
                                        "enumerations": [
                                            {
                                                "id": "enum-loanType",
                                                "name": "LoanType",
                                                "items": [
                                                    "BORROW",
                                                    "RETURN",
                                                    "EXTEND",
                                                    "OVERDUE"
                                                ]
                                            }
                                        ],
                                        "valueObjects": [
                                            {
                                                "id": "vo-member",
                                                "name": "Member",
                                                "properties": [
                                                    {
                                                        "name": "memberId"
                                                    },
                                                    {
                                                        "name": "memberName"
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    "is_accumulated": True,
                    "retry_count": 0,
                    "created_actions": [
                        {
                            "objectType": "Aggregate",
                            "type": "create",
                            "ids": {
                                "boundedContextId": "c517babe-52fb-48ba-8920-60df60b3da1e",
                                "aggregateId": "4d3ad69a-26a0-4339-b557-dcd54213c61f"
                            },
                            "args": {
                                "aggregateName": "BookStatusHistory",
                                "aggregateAlias": "도서상태변경이력",
                                "properties": [
                                    {
                                        "name": "statusHistoryId",
                                        "type": "Long",
                                        "isKey": True
                                    },
                                    {
                                        "name": "bookId"
                                    },
                                    {
                                        "name": "previousStatus",
                                        "type": "BookStatus"
                                    },
                                    {
                                        "name": "currentStatus",
                                        "type": "BookStatus"
                                    },
                                    {
                                        "name": "changedAt",
                                        "type": "Date"
                                    },
                                    {
                                        "name": "reason"
                                    }
                                ]
                            },
                            "actionName": "CreateBookStatusHistoryAggregate"
                        },
                        {
                            "objectType": "Enumeration",
                            "type": "create",
                            "ids": {
                                "boundedContextId": "c517babe-52fb-48ba-8920-60df60b3da1e",
                                "aggregateId": "4d3ad69a-26a0-4339-b557-dcd54213c61f",
                                "enumerationId": "410591e3-b3a0-418e-b36c-f398e0d1a0ab"
                            },
                            "args": {
                                "enumerationName": "BookStatus",
                                "enumerationAlias": "도서상태",
                                "properties": [
                                    {
                                        "name": "AVAILABLE"
                                    },
                                    {
                                        "name": "BORROWED"
                                    },
                                    {
                                        "name": "RESERVED"
                                    },
                                    {
                                        "name": "DISCARDED"
                                    }
                                ]
                            },
                            "actionName": "CreateBookStatusEnum"
                        }
                    ],
                    "generation_complete": True
                }
            ],
            pending_generations=[],
            is_processing=False,
            all_complete=True,
            max_retry_count=3,
            is_failed=False
        ),
        createAggregateClassIdByDraftsModel=CreateAggregateClassIdByDraftsModel(),
        createCommandActionsByFunctionModel=CreateCommandActionsByFunctionModel(),
        createPolicyActionsByFunctionModel=CreatePolicyActionsByFunctionModel()
    ),
    outputs=OutputsModel(
        esValue=EsValueModel(
            elements={
                "6b5d96ec-a502-4242-a6d4-890ec1b2104e": {
                    "_type": "org.uengine.modeling.model.BoundedContext",
                    "aggregates": [
                        {
                            "id": "8e794426-f189-4559-8e36-0a8b457c3db9"
                        }
                    ],
                    "author": "My-UID",
                    "description": "# Requirements\n\n## userStory\n\n도서관의 도서 관리와 대출/반납을 통합적으로 관리하는 화면을 만들려고 해.\n\n## userStory\n\n'도서 관리' 화면에서는 새로운 도서를 등록하고 현재 보유한 도서들의 상태를 관리할 수 있어야 해. 도서 등록 시에는 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받아야 해. ISBN은 13자리 숫자여야 하고 중복 확인이 필요해. 카테고리는 소설/비소설/학술/잡지 중에서 선택할 수 있어야 해. 등록된 도서는 처음에 '대출가능' 상태가 되고, 이후 대출/반납 상황에 따라 '대출중', '예약중' 상태로 자동으로 변경되어야 해. 도서가 훼손되거나 분실된 경우 '폐기' 처리가 가능해야 하며, 폐기된 도서는 더 이상 대출이 불가능해야 해.\n\n## userStory\n\n'대출/반납' 화면에서는 회원이 도서를 대출하고 반납하는 것을 관리할 수 있어야 해. 대출 신청 시에는 회원번호와 이름으로 회원을 확인하고, 대출할 도서를 선택해야 해. 도서는 도서명이나 ISBN으로 검색할 수 있어야 해. 대출 기간은 7일/14일/30일 중에서 선택할 수 있어. 만약 대출하려는 도서가 이미 대출 중이라면, 예약 신청이 가능해야 해. 대출이 완료되면 해당 도서의 상태는 자동으로 '대출중'으로 변경되어야 해.\n\n## userStory\n\n대출 현황 화면에서는 현재 대출 중인 도서들의 목록을 볼 수 있어야 해. 각 대출 건에 대해 대출일, 반납예정일, 현재 상태(대출중/연체/반납완료)를 확인할 수 있어야 하고, 대출 중인 도서는 연장이나 반납 처리가 가능해야 해. 도서가 반납되면 자동으로 해당 도서의 상태가 '대출가능'으로 변경되어야 해. 만약 예약자가 있는 도서가 반납되면, 해당 도서는 '예약중' 상태로 변경되어야 해.\n\n## userStory\n\n각 도서별로 대출 이력과 상태 변경 이력을 조회할 수 있어야 하고, 이를 통해 도서의 대출 현황과 상태 변화를 추적할 수 있어야 해.\n\n## Event\n\n{\"name\":\"BookRegistered\",\"displayName\":\"도서가 등록됨\",\"actor\":\"Librarian\",\"level\":1,\"description\":\"사서가 도서명, ISBN, 저자, 출판사, 카테고리를 입력하여 신규 도서를 등록함. ISBN 중복 및 형식(13자리 숫자) 검증을 거침.\",\"inputs\":[\"도서명\",\"ISBN(13자리)\",\"저자\",\"출판사\",\"카테고리(소설/비소설/학술/잡지)\",\"ISBN 중복 아님\",\"ISBN 형식 유효\"],\"outputs\":[\"신규 도서 등록\",\"도서 상태: 대출가능\"],\"nextEvents\":[\"BookStateChanged\"]}\n\n## Event\n\n{\"name\":\"BookRegistrationFailedDueToDuplicateISBN\",\"displayName\":\"ISBN 중복으로 도서 등록 실패함\",\"actor\":\"Librarian\",\"level\":1,\"description\":\"도서 등록 시 입력한 ISBN이 기존에 이미 존재할 경우, 도서 등록이 실패함.\",\"inputs\":[\"ISBN(13자리)\",\"기존 도서에 동일 ISBN 존재\"],\"outputs\":[\"도서 등록 실패 알림\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookRegistrationFailedDueToInvalidISBNFormat\",\"displayName\":\"ISBN 형식 오류로 도서 등록 실패함\",\"actor\":\"Librarian\",\"level\":1,\"description\":\"도서 등록 시 입력한 ISBN이 13자리 숫자 형식이 아닐 경우, 도서 등록이 실패함.\",\"inputs\":[\"ISBN(13자리 아님)\"],\"outputs\":[\"도서 등록 실패 알림\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookStateChanged\",\"displayName\":\"도서 상태가 변경됨\",\"actor\":\"System\",\"level\":2,\"description\":\"도서의 상태가 비즈니스 프로세스(등록, 대출, 반납, 예약, 폐기)에 따라 변경됨.\",\"inputs\":[\"도서 ID\",\"변경 사유(등록, 대출, 반납, 예약, 폐기 등)\"],\"outputs\":[\"도서 상태 변경(대출가능/대출중/예약중/폐기)\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookDisposed\",\"displayName\":\"도서가 폐기됨\",\"actor\":\"Librarian\",\"level\":3,\"description\":\"사서가 도서가 훼손되거나 분실되었음을 확인하고 해당 도서를 폐기 처리함.\",\"inputs\":[\"도서 ID\",\"폐기 사유(훼손, 분실 등)\"],\"outputs\":[\"도서 상태: 폐기\",\"해당 도서 대출 불가\"],\"nextEvents\":[\"BookStateChanged\"]}\n\n## Event\n\n{\"name\":\"BookBorrowed\",\"displayName\":\"도서가 대출됨\",\"actor\":\"Member\",\"level\":4,\"description\":\"회원이 회원번호와 이름으로 인증 후 도서명 또는 ISBN으로 도서를 검색하여 대출 기간을 선택하고 대출 신청을 완료함.\",\"inputs\":[\"회원번호\",\"회원명\",\"도서 ID\",\"대출 기간(7/14/30일)\",\"도서 상태: 대출가능\"],\"outputs\":[\"도서 대출 기록 생성\",\"도서 상태: 대출중\"],\"nextEvents\":[\"BookStateChanged\",\"LoanHistoryRecorded\"]}\n\n## Event\n\n{\"name\":\"BookBorrowFailedDueToUnavailableBook\",\"displayName\":\"도서 대출 불가로 대출 실패함\",\"actor\":\"Member\",\"level\":4,\"description\":\"회원이 대출을 시도했으나 해당 도서가 이미 대출 중이어서 대출이 실패함.\",\"inputs\":[\"도서 ID\",\"도서 상태: 대출중/폐기\"],\"outputs\":[\"도서 대출 실패 알림\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookReserved\",\"displayName\":\"도서가 예약됨\",\"actor\":\"Member\",\"level\":5,\"description\":\"회원이 대출 중인 도서를 예약함. 예약자 정보와 예약 일시가 저장됨.\",\"inputs\":[\"회원번호\",\"회원명\",\"도서 ID\",\"도서 상태: 대출중\"],\"outputs\":[\"도서 예약 기록 생성\",\"도서 상태: 예약중(반납 시 자동 전환)\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookReturned\",\"displayName\":\"도서가 반납됨\",\"actor\":\"Member\",\"level\":6,\"description\":\"회원이 대출 중이던 도서를 반납함. 반납일이 기록되고 도서의 상태가 변경됨.\",\"inputs\":[\"회원번호\",\"도서 ID\",\"대출 기록\"],\"outputs\":[\"반납일 기록\",\"도서 상태: 대출가능(예약자 없을 시) 또는 예약중(예약자 있을 시)\"],\"nextEvents\":[\"BookStateChanged\",\"LoanHistoryRecorded\"]}\n\n## Event\n\n{\"name\":\"BookReturnOverdue\",\"displayName\":\"도서가 연체되어 반납됨\",\"actor\":\"Member\",\"level\":7,\"description\":\"회원이 반납 예정일을 초과하여 도서를 반납함. 연체 이력이 기록됨.\",\"inputs\":[\"회원번호\",\"도서 ID\",\"반납일 > 반납예정일\"],\"outputs\":[\"연체 기록\",\"도서 상태 변경\"],\"nextEvents\":[\"BookReturned\"]}\n\n## Event\n\n{\"name\":\"LoanExtended\",\"displayName\":\"대출이 연장됨\",\"actor\":\"Member\",\"level\":8,\"description\":\"회원이 현재 대출 중인 도서에 대해 연장 신청하여 반납 예정일이 연장됨.\",\"inputs\":[\"회원번호\",\"도서 ID\",\"대출 기록\",\"연장 조건 충족\"],\"outputs\":[\"반납 예정일 연장\",\"연장 이력 기록\"],\"nextEvents\":[\"LoanHistoryRecorded\"]}\n\n## Event\n\n{\"name\":\"LoanHistoryRecorded\",\"displayName\":\"대출 이력이 기록됨\",\"actor\":\"System\",\"level\":9,\"description\":\"도서별로 대출, 반납, 연장 등의 이력이 기록되어 도서의 대출 현황과 상태 변화 추적이 가능해짐.\",\"inputs\":[\"도서 ID\",\"이벤트 정보(대출/반납/연장/연체 등)\"],\"outputs\":[\"대출/반납/연장/연체 이력 데이터\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookStatusHistoryRecorded\",\"displayName\":\"도서 상태 변경 이력이 기록됨\",\"actor\":\"System\",\"level\":10,\"description\":\"도서의 상태(대출가능/대출중/예약중/폐기 등) 변경 이력이 별도로 기록되어 관리자가 이력 조회 가능.\",\"inputs\":[\"도서 ID\",\"이전 상태\",\"변경된 상태\",\"변경 일시\",\"변경 사유\"],\"outputs\":[\"도서 상태 변경 이력\"],\"nextEvents\":[]}",
                    "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.BoundedContext",
                        "height": 860,
                        "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e",
                        "style": "{}",
                        "width": 560,
                        "x": 650,
                        "y": 584
                    },
                    "gitURL": None,
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
                        "height": 350,
                        "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e",
                        "style": "{}",
                        "width": 350,
                        "x": 235,
                        "y": 365
                    },
                    "members": [],
                    "name": "LibraryBookLoan",
                    "displayName": "도서관 도서대출",
                    "oldName": "",
                    "policies": [],
                    "portGenerated": 8080,
                    "preferredPlatform": "template-spring-boot",
                    "preferredPlatformConf": {},
                    "rotateStatus": False,
                    "tempId": "",
                    "templatePerElements": {},
                    "views": [],
                    "definitionId": "My-Project-ID"
                },
                "c517babe-52fb-48ba-8920-60df60b3da1e": {
                    "_type": "org.uengine.modeling.model.BoundedContext",
                    "aggregates": [
                        {
                            "id": "b352b64a-a49d-4704-b27f-e532280568d8"
                        },
                        {
                            "id": "4d3ad69a-26a0-4339-b557-dcd54213c61f"
                        }
                    ],
                    "author": "My-UID",
                    "description": "# Requirements\n\n## userStory\n\n각 도서별로 대출 이력과 상태 변경 이력을 조회할 수 있어야 하고, 이를 통해 도서의 대출 현황과 상태 변화를 추적할 수 있어야 해.\n\n## Event\n\n{\"name\":\"BookBorrowed\",\"displayName\":\"도서가 대출됨\",\"actor\":\"Member\",\"level\":4,\"description\":\"회원이 회원번호와 이름으로 인증 후 도서명 또는 ISBN으로 도서를 검색하여 대출 기간을 선택하고 대출 신청을 완료함.\",\"inputs\":[\"회원번호\",\"회원명\",\"도서 ID\",\"대출 기간(7/14/30일)\",\"도서 상태: 대출가능\"],\"outputs\":[\"도서 대출 기록 생성\",\"도서 상태: 대출중\"],\"nextEvents\":[\"BookStateChanged\",\"LoanHistoryRecorded\"]}\n\n## Event\n\n{\"name\":\"BookReturned\",\"displayName\":\"도서가 반납됨\",\"actor\":\"Member\",\"level\":6,\"description\":\"회원이 대출 중이던 도서를 반납함. 반납일이 기록되고 도서의 상태가 변경됨.\",\"inputs\":[\"회원번호\",\"도서 ID\",\"대출 기록\"],\"outputs\":[\"반납일 기록\",\"도서 상태: 대출가능(예약자 없을 시) 또는 예약중(예약자 있을 시)\"],\"nextEvents\":[\"BookStateChanged\",\"LoanHistoryRecorded\"]}\n\n## Event\n\n{\"name\":\"BookReturnOverdue\",\"displayName\":\"도서가 연체되어 반납됨\",\"actor\":\"Member\",\"level\":7,\"description\":\"회원이 반납 예정일을 초과하여 도서를 반납함. 연체 이력이 기록됨.\",\"inputs\":[\"회원번호\",\"도서 ID\",\"반납일 > 반납예정일\"],\"outputs\":[\"연체 기록\",\"도서 상태 변경\"],\"nextEvents\":[\"BookReturned\"]}\n\n## Event\n\n{\"name\":\"LoanExtended\",\"displayName\":\"대출이 연장됨\",\"actor\":\"Member\",\"level\":8,\"description\":\"회원이 현재 대출 중인 도서에 대해 연장 신청하여 반납 예정일이 연장됨.\",\"inputs\":[\"회원번호\",\"도서 ID\",\"대출 기록\",\"연장 조건 충족\"],\"outputs\":[\"반납 예정일 연장\",\"연장 이력 기록\"],\"nextEvents\":[\"LoanHistoryRecorded\"]}\n\n## Event\n\n{\"name\":\"LoanHistoryRecorded\",\"displayName\":\"대출 이력이 기록됨\",\"actor\":\"System\",\"level\":9,\"description\":\"도서별로 대출, 반납, 연장 등의 이력이 기록되어 도서의 대출 현황과 상태 변화 추적이 가능해짐.\",\"inputs\":[\"도서 ID\",\"이벤트 정보(대출/반납/연장/연체 등)\"],\"outputs\":[\"대출/반납/연장/연체 이력 데이터\"],\"nextEvents\":[]}\n\n## Event\n\n{\"name\":\"BookStatusHistoryRecorded\",\"displayName\":\"도서 상태 변경 이력이 기록됨\",\"actor\":\"System\",\"level\":10,\"description\":\"도서의 상태(대출가능/대출중/예약중/폐기 등) 변경 이력이 별도로 기록되어 관리자가 이력 조회 가능.\",\"inputs\":[\"도서 ID\",\"이전 상태\",\"변경된 상태\",\"변경 일시\",\"변경 사유\"],\"outputs\":[\"도서 상태 변경 이력\"],\"nextEvents\":[]}",
                    "id": "c517babe-52fb-48ba-8920-60df60b3da1e",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.BoundedContext",
                        "height": 590,
                        "id": "c517babe-52fb-48ba-8920-60df60b3da1e",
                        "style": "{}",
                        "width": 1010,
                        "x": 1460.0,
                        "y": 450
                    },
                    "gitURL": None,
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
                        "height": 350,
                        "id": "c517babe-52fb-48ba-8920-60df60b3da1e",
                        "style": "{}",
                        "width": 350,
                        "x": 235,
                        "y": 365
                    },
                    "members": [],
                    "name": "LoanHistory",
                    "displayName": "대출이력",
                    "oldName": "",
                    "policies": [],
                    "portGenerated": 8081,
                    "preferredPlatform": "template-spring-boot",
                    "preferredPlatformConf": {},
                    "rotateStatus": False,
                    "tempId": "",
                    "templatePerElements": {},
                    "views": [],
                    "definitionId": "My-Project-ID"
                },
                "8e794426-f189-4559-8e36-0a8b457c3db9": {
                    "aggregateRoot": {
                        "_type": "org.uengine.modeling.model.AggregateRoot",
                        "fieldDescriptors": [
                            {
                                "className": "Long",
                                "isCopy": False,
                                "isKey": True,
                                "name": "bookId",
                                "nameCamelCase": "bookId",
                                "namePascalCase": "BookId",
                                "displayName": "",
                                "referenceClass": None,
                                "isOverrideField": False,
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": False,
                                "name": "title",
                                "nameCamelCase": "title",
                                "namePascalCase": "Title",
                                "displayName": "",
                                "referenceClass": None,
                                "isOverrideField": False,
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": False,
                                "name": "isbn",
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
                                "className": "BookCategory",
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
                                "className": "BookStatus",
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
                                "4541e3cb-de79-4e55-a238-4b5c158d2c5f": {
                                    "_type": "org.uengine.uml.model.Class",
                                    "id": "4541e3cb-de79-4e55-a238-4b5c158d2c5f",
                                    "name": "Book",
                                    "namePascalCase": "Book",
                                    "nameCamelCase": "book",
                                    "namePlural": "books",
                                    "fieldDescriptors": [
                                        {
                                            "className": "Long",
                                            "isCopy": False,
                                            "isKey": True,
                                            "name": "bookId",
                                            "displayName": "",
                                            "nameCamelCase": "bookId",
                                            "namePascalCase": "BookId",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None
                                        },
                                        {
                                            "className": "String",
                                            "isCopy": False,
                                            "isKey": False,
                                            "name": "title",
                                            "displayName": "",
                                            "nameCamelCase": "title",
                                            "namePascalCase": "Title",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None
                                        },
                                        {
                                            "className": "String",
                                            "isCopy": False,
                                            "isKey": False,
                                            "name": "isbn",
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
                                            "className": "BookCategory",
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
                                            "className": "BookStatus",
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
                                        "id": "4541e3cb-de79-4e55-a238-4b5c158d2c5f",
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
                                    "parentId": "8e794426-f189-4559-8e36-0a8b457c3db9"
                                },
                                "80a5e04e-bd4d-4387-b5dc-25b6d79a5089": {
                                    "_type": "org.uengine.uml.model.enum",
                                    "id": "80a5e04e-bd4d-4387-b5dc-25b6d79a5089",
                                    "name": "BookStatus",
                                    "displayName": "도서상태",
                                    "nameCamelCase": "bookStatus",
                                    "namePascalCase": "BookStatus",
                                    "namePlural": "bookStatuses",
                                    "elementView": {
                                        "_type": "org.uengine.uml.model.enum",
                                        "id": "80a5e04e-bd4d-4387-b5dc-25b6d79a5089",
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
                                            "value": "AVAILABLE"
                                        },
                                        {
                                            "value": "BORROWED"
                                        },
                                        {
                                            "value": "RESERVED"
                                        },
                                        {
                                            "value": "DISPOSED"
                                        }
                                    ],
                                    "useKeyValue": False,
                                    "relations": []
                                },
                                "a50b5105-1d52-4925-bcb2-f4899b109978": {
                                    "_type": "org.uengine.uml.model.enum",
                                    "id": "a50b5105-1d52-4925-bcb2-f4899b109978",
                                    "name": "BookCategory",
                                    "displayName": "도서카테고리",
                                    "nameCamelCase": "bookCategory",
                                    "namePascalCase": "BookCategory",
                                    "namePlural": "bookCategories",
                                    "elementView": {
                                        "_type": "org.uengine.uml.model.enum",
                                        "id": "a50b5105-1d52-4925-bcb2-f4899b109978",
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
                                }
                            },
                            "relations": {}
                        },
                        "operations": []
                    },
                    "author": "My-UID",
                    "boundedContext": {
                        "name": "6b5d96ec-a502-4242-a6d4-890ec1b2104e",
                        "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
                    },
                    "commands": [],
                    "description": None,
                    "id": "8e794426-f189-4559-8e36-0a8b457c3db9",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Aggregate",
                        "id": "8e794426-f189-4559-8e36-0a8b457c3db9",
                        "x": 650,
                        "y": 600,
                        "width": 130,
                        "height": 700
                    },
                    "events": [],
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.AggregateHexagonal",
                        "id": "8e794426-f189-4559-8e36-0a8b457c3db9",
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
                "b352b64a-a49d-4704-b27f-e532280568d8": {
                    "aggregateRoot": {
                        "_type": "org.uengine.modeling.model.AggregateRoot",
                        "fieldDescriptors": [
                            {
                                "className": "Long",
                                "isCopy": False,
                                "isKey": True,
                                "name": "loanHistoryId",
                                "nameCamelCase": "loanHistoryId",
                                "namePascalCase": "LoanHistoryId",
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
                            },
                            {
                                "className": "Member",
                                "isCopy": False,
                                "isKey": False,
                                "name": "member",
                                "nameCamelCase": "member",
                                "namePascalCase": "Member",
                                "displayName": "",
                                "referenceClass": None,
                                "isOverrideField": False,
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "LoanType",
                                "isCopy": False,
                                "isKey": False,
                                "name": "loanType",
                                "nameCamelCase": "loanType",
                                "namePascalCase": "LoanType",
                                "displayName": "",
                                "referenceClass": None,
                                "isOverrideField": False,
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Date",
                                "isCopy": False,
                                "isKey": False,
                                "name": "loanStartDate",
                                "nameCamelCase": "loanStartDate",
                                "namePascalCase": "LoanStartDate",
                                "displayName": "",
                                "referenceClass": None,
                                "isOverrideField": False,
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Date",
                                "isCopy": False,
                                "isKey": False,
                                "name": "loanDueDate",
                                "nameCamelCase": "loanDueDate",
                                "namePascalCase": "LoanDueDate",
                                "displayName": "",
                                "referenceClass": None,
                                "isOverrideField": False,
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Date",
                                "isCopy": False,
                                "isKey": False,
                                "name": "returnDate",
                                "nameCamelCase": "returnDate",
                                "namePascalCase": "ReturnDate",
                                "displayName": "",
                                "referenceClass": None,
                                "isOverrideField": False,
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Integer",
                                "isCopy": False,
                                "isKey": False,
                                "name": "overdueDays",
                                "nameCamelCase": "overdueDays",
                                "namePascalCase": "OverdueDays",
                                "displayName": "",
                                "referenceClass": None,
                                "isOverrideField": False,
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Date",
                                "isCopy": False,
                                "isKey": False,
                                "name": "createdAt",
                                "nameCamelCase": "createdAt",
                                "namePascalCase": "CreatedAt",
                                "displayName": "",
                                "referenceClass": None,
                                "isOverrideField": False,
                                "_type": "org.uengine.model.FieldDescriptor"
                            }
                        ],
                        "entities": {
                            "elements": {
                                "ce774860-ebf5-4d55-9c0f-ce47f6466f5b": {
                                    "_type": "org.uengine.uml.model.Class",
                                    "id": "ce774860-ebf5-4d55-9c0f-ce47f6466f5b",
                                    "name": "LoanHistory",
                                    "namePascalCase": "LoanHistory",
                                    "nameCamelCase": "loanHistory",
                                    "namePlural": "loanHistories",
                                    "fieldDescriptors": [
                                        {
                                            "className": "Long",
                                            "isCopy": False,
                                            "isKey": True,
                                            "name": "loanHistoryId",
                                            "displayName": "",
                                            "nameCamelCase": "loanHistoryId",
                                            "namePascalCase": "LoanHistoryId",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None
                                        },
                                        {
                                            "className": "BookId",
                                            "isCopy": False,
                                            "isKey": False,
                                            "name": "bookId",
                                            "displayName": "",
                                            "nameCamelCase": "bookId",
                                            "namePascalCase": "BookId",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None,
                                            "referenceClass": "Book",
                                            "isOverrideField": True
                                        },
                                        {
                                            "className": "Member",
                                            "isCopy": False,
                                            "isKey": False,
                                            "name": "member",
                                            "displayName": "",
                                            "nameCamelCase": "member",
                                            "namePascalCase": "Member",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None
                                        },
                                        {
                                            "className": "LoanType",
                                            "isCopy": False,
                                            "isKey": False,
                                            "name": "loanType",
                                            "displayName": "",
                                            "nameCamelCase": "loanType",
                                            "namePascalCase": "LoanType",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None
                                        },
                                        {
                                            "className": "Date",
                                            "isCopy": False,
                                            "isKey": False,
                                            "name": "loanStartDate",
                                            "displayName": "",
                                            "nameCamelCase": "loanStartDate",
                                            "namePascalCase": "LoanStartDate",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None
                                        },
                                        {
                                            "className": "Date",
                                            "isCopy": False,
                                            "isKey": False,
                                            "name": "loanDueDate",
                                            "displayName": "",
                                            "nameCamelCase": "loanDueDate",
                                            "namePascalCase": "LoanDueDate",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None
                                        },
                                        {
                                            "className": "Date",
                                            "isCopy": False,
                                            "isKey": False,
                                            "name": "returnDate",
                                            "displayName": "",
                                            "nameCamelCase": "returnDate",
                                            "namePascalCase": "ReturnDate",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None
                                        },
                                        {
                                            "className": "Integer",
                                            "isCopy": False,
                                            "isKey": False,
                                            "name": "overdueDays",
                                            "displayName": "",
                                            "nameCamelCase": "overdueDays",
                                            "namePascalCase": "OverdueDays",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None
                                        },
                                        {
                                            "className": "Date",
                                            "isCopy": False,
                                            "isKey": False,
                                            "name": "createdAt",
                                            "displayName": "",
                                            "nameCamelCase": "createdAt",
                                            "namePascalCase": "CreatedAt",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None
                                        }
                                    ],
                                    "operations": [],
                                    "elementView": {
                                        "_type": "org.uengine.uml.model.Class",
                                        "id": "ce774860-ebf5-4d55-9c0f-ce47f6466f5b",
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
                                    "parentId": "b352b64a-a49d-4704-b27f-e532280568d8"
                                },
                                "8e253425-bdeb-4a21-8277-57ef1e071f75": {
                                    "_type": "org.uengine.uml.model.vo.Class",
                                    "id": "8e253425-bdeb-4a21-8277-57ef1e071f75",
                                    "name": "Member",
                                    "displayName": "회원",
                                    "namePascalCase": "Member",
                                    "nameCamelCase": "member",
                                    "namePlural": "members",
                                    "fieldDescriptors": [
                                        {
                                            "className": "String",
                                            "isCopy": False,
                                            "isKey": False,
                                            "label": "- memberId: String",
                                            "name": "memberId",
                                            "nameCamelCase": "memberId",
                                            "namePascalCase": "MemberId",
                                            "displayName": "",
                                            "referenceClass": None,
                                            "isOverrideField": False,
                                            "_type": "org.uengine.model.FieldDescriptor"
                                        },
                                        {
                                            "className": "String",
                                            "isCopy": False,
                                            "isKey": False,
                                            "label": "- memberName: String",
                                            "name": "memberName",
                                            "nameCamelCase": "memberName",
                                            "namePascalCase": "MemberName",
                                            "displayName": "",
                                            "referenceClass": None,
                                            "isOverrideField": False,
                                            "_type": "org.uengine.model.FieldDescriptor"
                                        }
                                    ],
                                    "operations": [],
                                    "elementView": {
                                        "_type": "org.uengine.uml.model.vo.address.Class",
                                        "id": "8e253425-bdeb-4a21-8277-57ef1e071f75",
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
                                    "isAbstract": False,
                                    "isInterface": False
                                },
                                "cdeaf14e-572c-4e47-a997-6a831bbae718": {
                                    "_type": "org.uengine.uml.model.enum",
                                    "id": "cdeaf14e-572c-4e47-a997-6a831bbae718",
                                    "name": "LoanType",
                                    "displayName": "대출이력타입",
                                    "nameCamelCase": "loanType",
                                    "namePascalCase": "LoanType",
                                    "namePlural": "loanTypes",
                                    "elementView": {
                                        "_type": "org.uengine.uml.model.enum",
                                        "id": "cdeaf14e-572c-4e47-a997-6a831bbae718",
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
                                            "value": "BORROW"
                                        },
                                        {
                                            "value": "RETURN"
                                        },
                                        {
                                            "value": "EXTEND"
                                        },
                                        {
                                            "value": "OVERDUE"
                                        }
                                    ],
                                    "useKeyValue": False,
                                    "relations": []
                                },
                                "f8d37084-ab73-4827-9ba4-3e5c91af13d6": {
                                    "_type": "org.uengine.uml.model.vo.Class",
                                    "id": "f8d37084-ab73-4827-9ba4-3e5c91af13d6",
                                    "name": "BookId",
                                    "displayName": "",
                                    "namePascalCase": "BookId",
                                    "nameCamelCase": "bookId",
                                    "namePlural": "bookIds",
                                    "fieldDescriptors": [
                                        {
                                            "className": "Long",
                                            "isCopy": False,
                                            "isKey": True,
                                            "label": "- bookId: Long",
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
                                        "_type": "org.uengine.uml.model.vo.address.Class",
                                        "id": "f8d37084-ab73-4827-9ba4-3e5c91af13d6",
                                        "x": 1200,
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
                                    "isAbstract": False,
                                    "isInterface": False
                                }
                            },
                            "relations": {}
                        },
                        "operations": []
                    },
                    "author": "My-UID",
                    "boundedContext": {
                        "name": "c517babe-52fb-48ba-8920-60df60b3da1e",
                        "id": "c517babe-52fb-48ba-8920-60df60b3da1e"
                    },
                    "commands": [],
                    "description": None,
                    "id": "b352b64a-a49d-4704-b27f-e532280568d8",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Aggregate",
                        "id": "b352b64a-a49d-4704-b27f-e532280568d8",
                        "x": 1235.0,
                        "y": 450,
                        "width": 130,
                        "height": 400
                    },
                    "events": [],
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.AggregateHexagonal",
                        "id": "b352b64a-a49d-4704-b27f-e532280568d8",
                        "x": 0,
                        "y": 0,
                        "subWidth": 0,
                        "width": 0
                    },
                    "name": "LoanHistory",
                    "displayName": "대출이력",
                    "nameCamelCase": "loanHistory",
                    "namePascalCase": "LoanHistory",
                    "namePlural": "loanHistories",
                    "rotateStatus": False,
                    "selected": False,
                    "_type": "org.uengine.modeling.model.Aggregate"
                },
                "4d3ad69a-26a0-4339-b557-dcd54213c61f": {
                    "aggregateRoot": {
                        "_type": "org.uengine.modeling.model.AggregateRoot",
                        "fieldDescriptors": [
                            {
                                "className": "Long",
                                "isCopy": False,
                                "isKey": True,
                                "name": "statusHistoryId",
                                "nameCamelCase": "statusHistoryId",
                                "namePascalCase": "StatusHistoryId",
                                "displayName": "",
                                "referenceClass": None,
                                "isOverrideField": False,
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": False,
                                "name": "bookId",
                                "nameCamelCase": "bookId",
                                "namePascalCase": "BookId",
                                "displayName": "",
                                "referenceClass": None,
                                "isOverrideField": False,
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "BookStatus",
                                "isCopy": False,
                                "isKey": False,
                                "name": "previousStatus",
                                "nameCamelCase": "previousStatus",
                                "namePascalCase": "PreviousStatus",
                                "displayName": "",
                                "referenceClass": None,
                                "isOverrideField": False,
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "BookStatus",
                                "isCopy": False,
                                "isKey": False,
                                "name": "currentStatus",
                                "nameCamelCase": "currentStatus",
                                "namePascalCase": "CurrentStatus",
                                "displayName": "",
                                "referenceClass": None,
                                "isOverrideField": False,
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
                                "referenceClass": None,
                                "isOverrideField": False,
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
                                "referenceClass": None,
                                "isOverrideField": False,
                                "_type": "org.uengine.model.FieldDescriptor"
                            }
                        ],
                        "entities": {
                            "elements": {
                                "778e59f9-ce03-4a44-a426-47bd75ce31e9": {
                                    "_type": "org.uengine.uml.model.Class",
                                    "id": "778e59f9-ce03-4a44-a426-47bd75ce31e9",
                                    "name": "BookStatusHistory",
                                    "namePascalCase": "BookStatusHistory",
                                    "nameCamelCase": "bookStatusHistory",
                                    "namePlural": "bookStatusHistories",
                                    "fieldDescriptors": [
                                        {
                                            "className": "Long",
                                            "isCopy": False,
                                            "isKey": True,
                                            "name": "statusHistoryId",
                                            "displayName": "",
                                            "nameCamelCase": "statusHistoryId",
                                            "namePascalCase": "StatusHistoryId",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None
                                        },
                                        {
                                            "className": "String",
                                            "isCopy": False,
                                            "isKey": False,
                                            "name": "bookId",
                                            "displayName": "",
                                            "nameCamelCase": "bookId",
                                            "namePascalCase": "BookId",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None
                                        },
                                        {
                                            "className": "BookStatus",
                                            "isCopy": False,
                                            "isKey": False,
                                            "name": "previousStatus",
                                            "displayName": "",
                                            "nameCamelCase": "previousStatus",
                                            "namePascalCase": "PreviousStatus",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None
                                        },
                                        {
                                            "className": "BookStatus",
                                            "isCopy": False,
                                            "isKey": False,
                                            "name": "currentStatus",
                                            "displayName": "",
                                            "nameCamelCase": "currentStatus",
                                            "namePascalCase": "CurrentStatus",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None
                                        },
                                        {
                                            "className": "Date",
                                            "isCopy": False,
                                            "isKey": False,
                                            "name": "changedAt",
                                            "displayName": "",
                                            "nameCamelCase": "changedAt",
                                            "namePascalCase": "ChangedAt",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None
                                        },
                                        {
                                            "className": "String",
                                            "isCopy": False,
                                            "isKey": False,
                                            "name": "reason",
                                            "displayName": "",
                                            "nameCamelCase": "reason",
                                            "namePascalCase": "Reason",
                                            "_type": "org.uengine.model.FieldDescriptor",
                                            "inputUI": None,
                                            "options": None
                                        }
                                    ],
                                    "operations": [],
                                    "elementView": {
                                        "_type": "org.uengine.uml.model.Class",
                                        "id": "778e59f9-ce03-4a44-a426-47bd75ce31e9",
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
                                    "parentId": "4d3ad69a-26a0-4339-b557-dcd54213c61f"
                                },
                                "410591e3-b3a0-418e-b36c-f398e0d1a0ab": {
                                    "_type": "org.uengine.uml.model.enum",
                                    "id": "410591e3-b3a0-418e-b36c-f398e0d1a0ab",
                                    "name": "BookStatus",
                                    "displayName": "도서상태",
                                    "nameCamelCase": "bookStatus",
                                    "namePascalCase": "BookStatus",
                                    "namePlural": "bookStatuses",
                                    "elementView": {
                                        "_type": "org.uengine.uml.model.enum",
                                        "id": "410591e3-b3a0-418e-b36c-f398e0d1a0ab",
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
                    "author": "My-UID",
                    "boundedContext": {
                        "name": "c517babe-52fb-48ba-8920-60df60b3da1e",
                        "id": "c517babe-52fb-48ba-8920-60df60b3da1e"
                    },
                    "commands": [],
                    "description": None,
                    "id": "4d3ad69a-26a0-4339-b557-dcd54213c61f",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Aggregate",
                        "id": "4d3ad69a-26a0-4339-b557-dcd54213c61f",
                        "x": 1665.0,
                        "y": 450,
                        "width": 130,
                        "height": 400
                    },
                    "events": [],
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.AggregateHexagonal",
                        "id": "4d3ad69a-26a0-4339-b557-dcd54213c61f",
                        "x": 0,
                        "y": 0,
                        "subWidth": 0,
                        "width": 0
                    },
                    "name": "BookStatusHistory",
                    "displayName": "도서상태변경이력",
                    "nameCamelCase": "bookStatusHistory",
                    "namePascalCase": "BookStatusHistory",
                    "namePlural": "bookStatusHistories",
                    "rotateStatus": False,
                    "selected": False,
                    "_type": "org.uengine.modeling.model.Aggregate"
                },
                "19b5f83b-aea7-4f19-bb09-c43ac32e4bd9": {
                    "alertURL": "/static/image/symbol/alert-icon.png",
                    "author": "My-UID",
                    "checkAlert": True,
                    "description": None,
                    "id": "19b5f83b-aea7-4f19-bb09-c43ac32e4bd9",
                    "elementView": {
                        "angle": 0,
                        "height": 115,
                        "id": "19b5f83b-aea7-4f19-bb09-c43ac32e4bd9",
                        "style": "{}",
                        "width": 100,
                        "x": 744,
                        "y": 250,
                        "_type": "org.uengine.modeling.model.Event"
                    },
                    "fieldDescriptors": [
                        {
                            "className": "Long",
                            "isCopy": False,
                            "isKey": True,
                            "name": "bookId",
                            "nameCamelCase": "bookId",
                            "namePascalCase": "BookId",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": False,
                            "name": "title",
                            "nameCamelCase": "title",
                            "namePascalCase": "Title",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": False,
                            "name": "isbn",
                            "nameCamelCase": "isbn",
                            "namePascalCase": "Isbn",
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
                            "className": "BookCategory",
                            "isCopy": False,
                            "isKey": False,
                            "name": "category",
                            "nameCamelCase": "category",
                            "namePascalCase": "Category",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "BookStatus",
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
                        "id": "19b5f83b-aea7-4f19-bb09-c43ac32e4bd9",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0,
                        "_type": "org.uengine.modeling.model.EventHexagonal"
                    },
                    "name": "BookRegistered",
                    "displayName": "도서가 등록됨",
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
                        "id": "8e794426-f189-4559-8e36-0a8b457c3db9"
                    },
                    "boundedContext": {
                        "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
                    }
                },
                "dbd2d70b-ec51-4385-b811-31f3c9ef15e1": {
                    "alertURL": "/static/image/symbol/alert-icon.png",
                    "author": "My-UID",
                    "checkAlert": True,
                    "description": None,
                    "id": "dbd2d70b-ec51-4385-b811-31f3c9ef15e1",
                    "elementView": {
                        "angle": 0,
                        "height": 115,
                        "id": "dbd2d70b-ec51-4385-b811-31f3c9ef15e1",
                        "style": "{}",
                        "width": 100,
                        "x": 744,
                        "y": 378,
                        "_type": "org.uengine.modeling.model.Event"
                    },
                    "fieldDescriptors": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": False,
                            "name": "isbn",
                            "nameCamelCase": "isbn",
                            "namePascalCase": "Isbn",
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
                        "id": "dbd2d70b-ec51-4385-b811-31f3c9ef15e1",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0,
                        "_type": "org.uengine.modeling.model.EventHexagonal"
                    },
                    "name": "BookRegistrationFailedDueToDuplicateISBN",
                    "displayName": "ISBN 중복으로 도서 등록 실패함",
                    "nameCamelCase": "bookregistrationfailedduetoduplicateisbn",
                    "namePascalCase": "Bookregistrationfailedduetoduplicateisbn",
                    "namePlural": "",
                    "relationCommandInfo": [],
                    "relationPolicyInfo": [],
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PostPersist",
                    "_type": "org.uengine.modeling.model.Event",
                    "aggregate": {
                        "id": "8e794426-f189-4559-8e36-0a8b457c3db9"
                    },
                    "boundedContext": {
                        "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
                    }
                },
                "1c18e36c-49a8-49d3-9f07-5b68cc386450": {
                    "alertURL": "/static/image/symbol/alert-icon.png",
                    "author": "My-UID",
                    "checkAlert": True,
                    "description": None,
                    "id": "1c18e36c-49a8-49d3-9f07-5b68cc386450",
                    "elementView": {
                        "angle": 0,
                        "height": 115,
                        "id": "1c18e36c-49a8-49d3-9f07-5b68cc386450",
                        "style": "{}",
                        "width": 100,
                        "x": 744,
                        "y": 506,
                        "_type": "org.uengine.modeling.model.Event"
                    },
                    "fieldDescriptors": [
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": False,
                            "name": "isbn",
                            "nameCamelCase": "isbn",
                            "namePascalCase": "Isbn",
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
                        "id": "1c18e36c-49a8-49d3-9f07-5b68cc386450",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0,
                        "_type": "org.uengine.modeling.model.EventHexagonal"
                    },
                    "name": "BookRegistrationFailedDueToInvalidISBNFormat",
                    "displayName": "ISBN 형식 오류로 도서 등록 실패함",
                    "nameCamelCase": "bookregistrationfailedduetoinvalidisbnformat",
                    "namePascalCase": "Bookregistrationfailedduetoinvalidisbnformat",
                    "namePlural": "",
                    "relationCommandInfo": [],
                    "relationPolicyInfo": [],
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PostPersist",
                    "_type": "org.uengine.modeling.model.Event",
                    "aggregate": {
                        "id": "8e794426-f189-4559-8e36-0a8b457c3db9"
                    },
                    "boundedContext": {
                        "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
                    }
                },
                "dce353ac-1c01-437d-846a-e541170d2317": {
                    "alertURL": "/static/image/symbol/alert-icon.png",
                    "author": "My-UID",
                    "checkAlert": True,
                    "description": None,
                    "id": "dce353ac-1c01-437d-846a-e541170d2317",
                    "elementView": {
                        "angle": 0,
                        "height": 115,
                        "id": "dce353ac-1c01-437d-846a-e541170d2317",
                        "style": "{}",
                        "width": 100,
                        "x": 744,
                        "y": 634,
                        "_type": "org.uengine.modeling.model.Event"
                    },
                    "fieldDescriptors": [
                        {
                            "className": "Long",
                            "isCopy": False,
                            "isKey": True,
                            "name": "bookId",
                            "nameCamelCase": "bookId",
                            "namePascalCase": "BookId",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "BookStatus",
                            "isCopy": False,
                            "isKey": False,
                            "name": "previousStatus",
                            "nameCamelCase": "previousStatus",
                            "namePascalCase": "PreviousStatus",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "BookStatus",
                            "isCopy": False,
                            "isKey": False,
                            "name": "currentStatus",
                            "nameCamelCase": "currentStatus",
                            "namePascalCase": "CurrentStatus",
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
                        "id": "dce353ac-1c01-437d-846a-e541170d2317",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0,
                        "_type": "org.uengine.modeling.model.EventHexagonal"
                    },
                    "name": "BookStateChanged",
                    "displayName": "도서 상태가 변경됨",
                    "nameCamelCase": "bookStateChanged",
                    "namePascalCase": "BookStateChanged",
                    "namePlural": "",
                    "relationCommandInfo": [],
                    "relationPolicyInfo": [],
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PostPersist",
                    "_type": "org.uengine.modeling.model.Event",
                    "aggregate": {
                        "id": "8e794426-f189-4559-8e36-0a8b457c3db9"
                    },
                    "boundedContext": {
                        "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
                    }
                },
                "73448c06-5848-4a92-90f9-6fd5a7a5f7f5": {
                    "alertURL": "/static/image/symbol/alert-icon.png",
                    "author": "My-UID",
                    "checkAlert": True,
                    "description": None,
                    "id": "73448c06-5848-4a92-90f9-6fd5a7a5f7f5",
                    "elementView": {
                        "angle": 0,
                        "height": 115,
                        "id": "73448c06-5848-4a92-90f9-6fd5a7a5f7f5",
                        "style": "{}",
                        "width": 100,
                        "x": 744,
                        "y": 762,
                        "_type": "org.uengine.modeling.model.Event"
                    },
                    "fieldDescriptors": [
                        {
                            "className": "Long",
                            "isCopy": False,
                            "isKey": True,
                            "name": "bookId",
                            "nameCamelCase": "bookId",
                            "namePascalCase": "BookId",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Date",
                            "isCopy": False,
                            "isKey": False,
                            "name": "disposedAt",
                            "nameCamelCase": "disposedAt",
                            "namePascalCase": "DisposedAt",
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
                        "id": "73448c06-5848-4a92-90f9-6fd5a7a5f7f5",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0,
                        "_type": "org.uengine.modeling.model.EventHexagonal"
                    },
                    "name": "BookDisposed",
                    "displayName": "도서가 폐기됨",
                    "nameCamelCase": "bookDisposed",
                    "namePascalCase": "BookDisposed",
                    "namePlural": "",
                    "relationCommandInfo": [],
                    "relationPolicyInfo": [],
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PostPersist",
                    "_type": "org.uengine.modeling.model.Event",
                    "aggregate": {
                        "id": "8e794426-f189-4559-8e36-0a8b457c3db9"
                    },
                    "boundedContext": {
                        "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
                    }
                },
                "ab8d9f62-bc9f-4dda-bfa6-ee5becc12bf7": {
                    "alertURL": "/static/image/symbol/alert-icon.png",
                    "author": "My-UID",
                    "checkAlert": True,
                    "description": None,
                    "id": "ab8d9f62-bc9f-4dda-bfa6-ee5becc12bf7",
                    "elementView": {
                        "angle": 0,
                        "height": 115,
                        "id": "ab8d9f62-bc9f-4dda-bfa6-ee5becc12bf7",
                        "style": "{}",
                        "width": 100,
                        "x": 744,
                        "y": 890,
                        "_type": "org.uengine.modeling.model.Event"
                    },
                    "fieldDescriptors": [
                        {
                            "className": "Long",
                            "isCopy": False,
                            "isKey": True,
                            "name": "bookId",
                            "nameCamelCase": "bookId",
                            "namePascalCase": "BookId",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Date",
                            "isCopy": False,
                            "isKey": False,
                            "name": "blockedAt",
                            "nameCamelCase": "blockedAt",
                            "namePascalCase": "BlockedAt",
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
                        "id": "ab8d9f62-bc9f-4dda-bfa6-ee5becc12bf7",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0,
                        "_type": "org.uengine.modeling.model.EventHexagonal"
                    },
                    "name": "BookLoanReservationBlocked",
                    "displayName": "폐기 도서 대출/예약 차단됨",
                    "nameCamelCase": "bookLoanReservationBlocked",
                    "namePascalCase": "BookLoanReservationBlocked",
                    "namePlural": "",
                    "relationCommandInfo": [],
                    "relationPolicyInfo": [],
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PostPersist",
                    "_type": "org.uengine.modeling.model.Event",
                    "aggregate": {
                        "id": "8e794426-f189-4559-8e36-0a8b457c3db9"
                    },
                    "boundedContext": {
                        "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
                    }
                },
                "9cb00a7a-b78a-4d60-82ac-5c1d582692d3": {
                    "_type": "org.uengine.modeling.model.Command",
                    "outputEvents": [
                        "BookRegistered",
                        "BookRegistrationFailedDueToDuplicateISBN",
                        "BookRegistrationFailedDueToInvalidISBNFormat"
                    ],
                    "aggregate": {
                        "id": "8e794426-f189-4559-8e36-0a8b457c3db9"
                    },
                    "author": "My-UID",
                    "boundedContext": {
                        "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
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
                            "isKey": False,
                            "name": "title",
                            "nameCamelCase": "title",
                            "namePascalCase": "Title",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": False,
                            "name": "isbn",
                            "nameCamelCase": "isbn",
                            "namePascalCase": "Isbn",
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
                            "className": "BookCategory",
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
                    "id": "9cb00a7a-b78a-4d60-82ac-5c1d582692d3",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Command",
                        "height": 115,
                        "id": "9cb00a7a-b78a-4d60-82ac-5c1d582692d3",
                        "style": "{}",
                        "width": 100,
                        "x": 556,
                        "y": 250,
                        "z-index": 999
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.CommandHexagonal",
                        "height": 0,
                        "id": "9cb00a7a-b78a-4d60-82ac-5c1d582692d3",
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
                "f7614022-234a-4a55-bf35-703f02f90595": {
                    "_type": "org.uengine.modeling.model.Command",
                    "outputEvents": [
                        "BookStateChanged"
                    ],
                    "aggregate": {
                        "id": "8e794426-f189-4559-8e36-0a8b457c3db9"
                    },
                    "author": "My-UID",
                    "boundedContext": {
                        "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
                    },
                    "controllerInfo": {
                        "apiPath": "changebookstatus",
                        "method": "PATCH",
                        "fullApiPath": ""
                    },
                    "fieldDescriptors": [
                        {
                            "className": "Long",
                            "isCopy": False,
                            "isKey": True,
                            "name": "bookId",
                            "nameCamelCase": "bookId",
                            "namePascalCase": "BookId",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "BookStatus",
                            "isCopy": False,
                            "isKey": False,
                            "name": "newStatus",
                            "nameCamelCase": "newStatus",
                            "namePascalCase": "NewStatus",
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
                    "id": "f7614022-234a-4a55-bf35-703f02f90595",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Command",
                        "height": 115,
                        "id": "f7614022-234a-4a55-bf35-703f02f90595",
                        "style": "{}",
                        "width": 100,
                        "x": 556,
                        "y": 378,
                        "z-index": 999
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.CommandHexagonal",
                        "height": 0,
                        "id": "f7614022-234a-4a55-bf35-703f02f90595",
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
                        "method": "PATCH"
                    },
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PrePersist"
                },
                "139ce9e9-06f5-4a7f-8e4b-76b138c297ef": {
                    "_type": "org.uengine.modeling.model.Command",
                    "outputEvents": [
                        "BookDisposed"
                    ],
                    "aggregate": {
                        "id": "8e794426-f189-4559-8e36-0a8b457c3db9"
                    },
                    "author": "My-UID",
                    "boundedContext": {
                        "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
                    },
                    "controllerInfo": {
                        "apiPath": "disposebook",
                        "method": "PATCH",
                        "fullApiPath": ""
                    },
                    "fieldDescriptors": [
                        {
                            "className": "Long",
                            "isCopy": False,
                            "isKey": True,
                            "name": "bookId",
                            "nameCamelCase": "bookId",
                            "namePascalCase": "BookId",
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
                    "id": "139ce9e9-06f5-4a7f-8e4b-76b138c297ef",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Command",
                        "height": 115,
                        "id": "139ce9e9-06f5-4a7f-8e4b-76b138c297ef",
                        "style": "{}",
                        "width": 100,
                        "x": 556,
                        "y": 506,
                        "z-index": 999
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.CommandHexagonal",
                        "height": 0,
                        "id": "139ce9e9-06f5-4a7f-8e4b-76b138c297ef",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0
                    },
                    "isRestRepository": False,
                    "name": "DisposeBook",
                    "displayName": "도서 폐기 처리",
                    "nameCamelCase": "disposeBook",
                    "namePascalCase": "DisposeBook",
                    "namePlural": "disposeBooks",
                    "relationCommandInfo": [],
                    "relationEventInfo": [],
                    "restRepositoryInfo": {
                        "method": "PATCH"
                    },
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PrePersist"
                },
                "615bf707-e57b-437a-98af-29694c0ea7b2": {
                    "_type": "org.uengine.modeling.model.Command",
                    "outputEvents": [
                        "BookLoanReservationBlocked"
                    ],
                    "aggregate": {
                        "id": "8e794426-f189-4559-8e36-0a8b457c3db9"
                    },
                    "author": "My-UID",
                    "boundedContext": {
                        "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
                    },
                    "controllerInfo": {
                        "apiPath": "blockloanorreservationfordisposedbook",
                        "method": "POST",
                        "fullApiPath": ""
                    },
                    "fieldDescriptors": [
                        {
                            "className": "Long",
                            "isCopy": False,
                            "isKey": True,
                            "name": "bookId",
                            "nameCamelCase": "bookId",
                            "namePascalCase": "BookId",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "description": None,
                    "id": "615bf707-e57b-437a-98af-29694c0ea7b2",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Command",
                        "height": 115,
                        "id": "615bf707-e57b-437a-98af-29694c0ea7b2",
                        "style": "{}",
                        "width": 100,
                        "x": 556,
                        "y": 634,
                        "z-index": 999
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.CommandHexagonal",
                        "height": 0,
                        "id": "615bf707-e57b-437a-98af-29694c0ea7b2",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0
                    },
                    "isRestRepository": False,
                    "name": "BlockLoanOrReservationForDisposedBook",
                    "displayName": "폐기 도서 대출/예약 차단",
                    "nameCamelCase": "blockLoanOrReservationForDisposedBook",
                    "namePascalCase": "BlockLoanOrReservationForDisposedBook",
                    "namePlural": "blockLoanOrReservationForDisposedBooks",
                    "relationCommandInfo": [],
                    "relationEventInfo": [],
                    "restRepositoryInfo": {
                        "method": "POST"
                    },
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PrePersist"
                },
                "ec4c13c7-a449-4aa0-8583-cbe75732107b": {
                    "_type": "org.uengine.modeling.model.View",
                    "id": "ec4c13c7-a449-4aa0-8583-cbe75732107b",
                    "visibility": "public",
                    "name": "BookStatusList",
                    "oldName": "",
                    "displayName": "도서 현황 목록",
                    "namePascalCase": "BookStatusList",
                    "namePlural": "bookStatusLists",
                    "aggregate": {
                        "id": "8e794426-f189-4559-8e36-0a8b457c3db9"
                    },
                    "description": None,
                    "author": "My-UID",
                    "boundedContext": {
                        "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
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
                            "className": "BookCategory",
                            "isCopy": False,
                            "isKey": False,
                            "name": "category",
                            "nameCamelCase": "category",
                            "namePascalCase": "Category",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "BookStatus",
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
                            "name": "title",
                            "nameCamelCase": "title",
                            "namePascalCase": "Title",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "String",
                            "isCopy": False,
                            "isKey": False,
                            "name": "isbn",
                            "nameCamelCase": "isbn",
                            "namePascalCase": "Isbn",
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
                        "id": "ec4c13c7-a449-4aa0-8583-cbe75732107b",
                        "x": 556,
                        "y": 762,
                        "width": 100,
                        "height": 115,
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
                "d5081cd0-e352-42ae-a5ad-9578a8f32eed": {
                    "_type": "org.uengine.modeling.model.View",
                    "id": "d5081cd0-e352-42ae-a5ad-9578a8f32eed",
                    "visibility": "public",
                    "name": "BookDetails",
                    "oldName": "",
                    "displayName": "도서 상세 정보",
                    "namePascalCase": "BookDetails",
                    "namePlural": "bookDetails",
                    "aggregate": {
                        "id": "8e794426-f189-4559-8e36-0a8b457c3db9"
                    },
                    "description": None,
                    "author": "My-UID",
                    "boundedContext": {
                        "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
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
                            "className": "Long",
                            "isCopy": False,
                            "isKey": True,
                            "name": "bookId",
                            "nameCamelCase": "bookId",
                            "namePascalCase": "BookId",
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
                        "id": "d5081cd0-e352-42ae-a5ad-9578a8f32eed",
                        "x": 556,
                        "y": 890,
                        "width": 100,
                        "height": 115,
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
                "906e1adc-f1c9-4530-8f1c-38cbe843192c": {
                    "_type": "org.uengine.modeling.model.Actor",
                    "author": "My-UID",
                    "boundedContext": {
                        "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
                    },
                    "description": None,
                    "id": "906e1adc-f1c9-4530-8f1c-38cbe843192c",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Actor",
                        "height": 100,
                        "id": "906e1adc-f1c9-4530-8f1c-38cbe843192c",
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
                    "name": "Librarian",
                    "oldName": "",
                    "rotateStatus": False
                },
                "59bd38e1-e5a0-45f0-b74b-47d839e61645": {
                    "_type": "org.uengine.modeling.model.Actor",
                    "author": "My-UID",
                    "boundedContext": {
                        "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
                    },
                    "description": None,
                    "id": "59bd38e1-e5a0-45f0-b74b-47d839e61645",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Actor",
                        "height": 100,
                        "id": "59bd38e1-e5a0-45f0-b74b-47d839e61645",
                        "style": "{}",
                        "width": 100,
                        "x": 475,
                        "y": 378
                    },
                    "innerAggregate": {
                        "command": [],
                        "event": [],
                        "external": [],
                        "policy": [],
                        "view": []
                    },
                    "name": "Librarian",
                    "oldName": "",
                    "rotateStatus": False
                },
                "aadf1313-9ba2-4573-a990-8eba427719f8": {
                    "_type": "org.uengine.modeling.model.Actor",
                    "author": "My-UID",
                    "boundedContext": {
                        "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
                    },
                    "description": None,
                    "id": "aadf1313-9ba2-4573-a990-8eba427719f8",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Actor",
                        "height": 100,
                        "id": "aadf1313-9ba2-4573-a990-8eba427719f8",
                        "style": "{}",
                        "width": 100,
                        "x": 475,
                        "y": 506
                    },
                    "innerAggregate": {
                        "command": [],
                        "event": [],
                        "external": [],
                        "policy": [],
                        "view": []
                    },
                    "name": "Librarian",
                    "oldName": "",
                    "rotateStatus": False
                },
                "7a320e5b-3910-447c-b6f8-0335b1ccd8c7": {
                    "_type": "org.uengine.modeling.model.Actor",
                    "author": "My-UID",
                    "boundedContext": {
                        "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
                    },
                    "description": None,
                    "id": "7a320e5b-3910-447c-b6f8-0335b1ccd8c7",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Actor",
                        "height": 100,
                        "id": "7a320e5b-3910-447c-b6f8-0335b1ccd8c7",
                        "style": "{}",
                        "width": 100,
                        "x": 475,
                        "y": 762
                    },
                    "innerAggregate": {
                        "command": [],
                        "event": [],
                        "external": [],
                        "policy": [],
                        "view": []
                    },
                    "name": "Librarian",
                    "oldName": "",
                    "rotateStatus": False
                },
                "e74d639c-45b0-426d-ba7e-699f3cbf4d55": {
                    "_type": "org.uengine.modeling.model.Actor",
                    "author": "My-UID",
                    "boundedContext": {
                        "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
                    },
                    "description": None,
                    "id": "e74d639c-45b0-426d-ba7e-699f3cbf4d55",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Actor",
                        "height": 100,
                        "id": "e74d639c-45b0-426d-ba7e-699f3cbf4d55",
                        "style": "{}",
                        "width": 100,
                        "x": 475,
                        "y": 890
                    },
                    "innerAggregate": {
                        "command": [],
                        "event": [],
                        "external": [],
                        "policy": [],
                        "view": []
                    },
                    "name": "Librarian",
                    "oldName": "",
                    "rotateStatus": False
                },
                "8b664b48-2e29-48f8-8908-7555193344ee": {
                    "alertURL": "/static/image/symbol/alert-icon.png",
                    "author": "My-UID",
                    "checkAlert": True,
                    "description": None,
                    "id": "8b664b48-2e29-48f8-8908-7555193344ee",
                    "elementView": {
                        "angle": 0,
                        "height": 115,
                        "id": "8b664b48-2e29-48f8-8908-7555193344ee",
                        "style": "{}",
                        "width": 100,
                        "x": 1329.0,
                        "y": 250,
                        "_type": "org.uengine.modeling.model.Event"
                    },
                    "fieldDescriptors": [
                        {
                            "className": "Long",
                            "isCopy": False,
                            "isKey": True,
                            "name": "loanHistoryId",
                            "nameCamelCase": "loanHistoryId",
                            "namePascalCase": "LoanHistoryId",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Long",
                            "isCopy": False,
                            "isKey": False,
                            "name": "bookId",
                            "nameCamelCase": "bookId",
                            "namePascalCase": "BookId",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Member",
                            "isCopy": False,
                            "isKey": False,
                            "name": "member",
                            "nameCamelCase": "member",
                            "namePascalCase": "Member",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "LoanType",
                            "isCopy": False,
                            "isKey": False,
                            "name": "loanType",
                            "nameCamelCase": "loanType",
                            "namePascalCase": "LoanType",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Date",
                            "isCopy": False,
                            "isKey": False,
                            "name": "loanStartDate",
                            "nameCamelCase": "loanStartDate",
                            "namePascalCase": "LoanStartDate",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Date",
                            "isCopy": False,
                            "isKey": False,
                            "name": "loanDueDate",
                            "nameCamelCase": "loanDueDate",
                            "namePascalCase": "LoanDueDate",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Date",
                            "isCopy": False,
                            "isKey": False,
                            "name": "returnDate",
                            "nameCamelCase": "returnDate",
                            "namePascalCase": "ReturnDate",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Integer",
                            "isCopy": False,
                            "isKey": False,
                            "name": "overdueDays",
                            "nameCamelCase": "overdueDays",
                            "namePascalCase": "OverdueDays",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Date",
                            "isCopy": False,
                            "isKey": False,
                            "name": "createdAt",
                            "nameCamelCase": "createdAt",
                            "namePascalCase": "CreatedAt",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "hexagonalView": {
                        "height": 0,
                        "id": "8b664b48-2e29-48f8-8908-7555193344ee",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0,
                        "_type": "org.uengine.modeling.model.EventHexagonal"
                    },
                    "name": "LoanHistoryRecorded",
                    "displayName": "대출 이력이 기록됨",
                    "nameCamelCase": "loanHistoryRecorded",
                    "namePascalCase": "LoanHistoryRecorded",
                    "namePlural": "",
                    "relationCommandInfo": [],
                    "relationPolicyInfo": [],
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PostPersist",
                    "_type": "org.uengine.modeling.model.Event",
                    "aggregate": {
                        "id": "b352b64a-a49d-4704-b27f-e532280568d8"
                    },
                    "boundedContext": {
                        "id": "c517babe-52fb-48ba-8920-60df60b3da1e"
                    }
                },
                "3b804b8b-3b73-46b6-b8d0-a8892db6c0f2": {
                    "_type": "org.uengine.modeling.model.Command",
                    "outputEvents": [
                        "LoanHistoryRecorded"
                    ],
                    "aggregate": {
                        "id": "b352b64a-a49d-4704-b27f-e532280568d8"
                    },
                    "author": "My-UID",
                    "boundedContext": {
                        "id": "c517babe-52fb-48ba-8920-60df60b3da1e"
                    },
                    "controllerInfo": {
                        "apiPath": "recordloanhistory",
                        "method": "POST",
                        "fullApiPath": ""
                    },
                    "fieldDescriptors": [
                        {
                            "className": "Long",
                            "isCopy": False,
                            "isKey": False,
                            "name": "bookId",
                            "nameCamelCase": "bookId",
                            "namePascalCase": "BookId",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Member",
                            "isCopy": False,
                            "isKey": False,
                            "name": "member",
                            "nameCamelCase": "member",
                            "namePascalCase": "Member",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "LoanType",
                            "isCopy": False,
                            "isKey": False,
                            "name": "loanType",
                            "nameCamelCase": "loanType",
                            "namePascalCase": "LoanType",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Date",
                            "isCopy": False,
                            "isKey": False,
                            "name": "loanStartDate",
                            "nameCamelCase": "loanStartDate",
                            "namePascalCase": "LoanStartDate",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Date",
                            "isCopy": False,
                            "isKey": False,
                            "name": "loanDueDate",
                            "nameCamelCase": "loanDueDate",
                            "namePascalCase": "LoanDueDate",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Date",
                            "isCopy": False,
                            "isKey": False,
                            "name": "returnDate",
                            "nameCamelCase": "returnDate",
                            "namePascalCase": "ReturnDate",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Integer",
                            "isCopy": False,
                            "isKey": False,
                            "name": "overdueDays",
                            "nameCamelCase": "overdueDays",
                            "namePascalCase": "OverdueDays",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Date",
                            "isCopy": False,
                            "isKey": False,
                            "name": "createdAt",
                            "nameCamelCase": "createdAt",
                            "namePascalCase": "CreatedAt",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        }
                    ],
                    "description": None,
                    "id": "3b804b8b-3b73-46b6-b8d0-a8892db6c0f2",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Command",
                        "height": 115,
                        "id": "3b804b8b-3b73-46b6-b8d0-a8892db6c0f2",
                        "style": "{}",
                        "width": 100,
                        "x": 1141.0,
                        "y": 250,
                        "z-index": 999
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.CommandHexagonal",
                        "height": 0,
                        "id": "3b804b8b-3b73-46b6-b8d0-a8892db6c0f2",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0
                    },
                    "isRestRepository": False,
                    "name": "RecordLoanHistory",
                    "displayName": "대출 이력 기록",
                    "nameCamelCase": "recordLoanHistory",
                    "namePascalCase": "RecordLoanHistory",
                    "namePlural": "recordLoanHistories",
                    "relationCommandInfo": [],
                    "relationEventInfo": [],
                    "restRepositoryInfo": {
                        "method": "POST"
                    },
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PrePersist"
                },
                "874cf10b-09f4-4728-833d-ed6878f4d974": {
                    "_type": "org.uengine.modeling.model.View",
                    "id": "874cf10b-09f4-4728-833d-ed6878f4d974",
                    "visibility": "public",
                    "name": "LoanHistoryByBook",
                    "oldName": "",
                    "displayName": "도서별 대출 이력 목록",
                    "namePascalCase": "LoanHistoryByBook",
                    "namePlural": "loanHistoryByBooks",
                    "aggregate": {
                        "id": "b352b64a-a49d-4704-b27f-e532280568d8"
                    },
                    "description": None,
                    "author": "My-UID",
                    "boundedContext": {
                        "id": "c517babe-52fb-48ba-8920-60df60b3da1e"
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
                            "className": "Long",
                            "isCopy": False,
                            "isKey": False,
                            "name": "bookId",
                            "nameCamelCase": "bookId",
                            "namePascalCase": "BookId",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "LoanType",
                            "isCopy": False,
                            "isKey": False,
                            "name": "loanType",
                            "nameCamelCase": "loanType",
                            "namePascalCase": "LoanType",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Date",
                            "isCopy": False,
                            "isKey": False,
                            "name": "startDate",
                            "nameCamelCase": "startDate",
                            "namePascalCase": "StartDate",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Date",
                            "isCopy": False,
                            "isKey": False,
                            "name": "endDate",
                            "nameCamelCase": "endDate",
                            "namePascalCase": "EndDate",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Integer",
                            "isCopy": False,
                            "isKey": False,
                            "name": "page",
                            "nameCamelCase": "page",
                            "namePascalCase": "Page",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Integer",
                            "isCopy": False,
                            "isKey": False,
                            "name": "size",
                            "nameCamelCase": "size",
                            "namePascalCase": "Size",
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
                        "id": "874cf10b-09f4-4728-833d-ed6878f4d974",
                        "x": 1141.0,
                        "y": 378,
                        "width": 100,
                        "height": 115,
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
                "f1135820-4474-41cb-a838-ab5b8ee69e46": {
                    "_type": "org.uengine.modeling.model.View",
                    "id": "f1135820-4474-41cb-a838-ab5b8ee69e46",
                    "visibility": "public",
                    "name": "BookStatusHistoryByBook",
                    "oldName": "",
                    "displayName": "도서별 상태 변경 이력 목록",
                    "namePascalCase": "BookStatusHistoryByBook",
                    "namePlural": "bookStatusHistoryByBooks",
                    "aggregate": {
                        "id": "4d3ad69a-26a0-4339-b557-dcd54213c61f"
                    },
                    "description": None,
                    "author": "My-UID",
                    "boundedContext": {
                        "id": "c517babe-52fb-48ba-8920-60df60b3da1e"
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
                            "className": "Long",
                            "isCopy": False,
                            "isKey": False,
                            "name": "bookId",
                            "nameCamelCase": "bookId",
                            "namePascalCase": "BookId",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "BookStatus",
                            "isCopy": False,
                            "isKey": False,
                            "name": "previousStatus",
                            "nameCamelCase": "previousStatus",
                            "namePascalCase": "PreviousStatus",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "BookStatus",
                            "isCopy": False,
                            "isKey": False,
                            "name": "currentStatus",
                            "nameCamelCase": "currentStatus",
                            "namePascalCase": "CurrentStatus",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Date",
                            "isCopy": False,
                            "isKey": False,
                            "name": "startDate",
                            "nameCamelCase": "startDate",
                            "namePascalCase": "StartDate",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Date",
                            "isCopy": False,
                            "isKey": False,
                            "name": "endDate",
                            "nameCamelCase": "endDate",
                            "namePascalCase": "EndDate",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Integer",
                            "isCopy": False,
                            "isKey": False,
                            "name": "page",
                            "nameCamelCase": "page",
                            "namePascalCase": "Page",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Integer",
                            "isCopy": False,
                            "isKey": False,
                            "name": "size",
                            "nameCamelCase": "size",
                            "namePascalCase": "Size",
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
                        "id": "f1135820-4474-41cb-a838-ab5b8ee69e46",
                        "x": 1571.0,
                        "y": 250,
                        "width": 100,
                        "height": 115,
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
                "381250a0-4d9c-47fd-bbbc-256f72d6cbaa": {
                    "_type": "org.uengine.modeling.model.Actor",
                    "author": "My-UID",
                    "boundedContext": {
                        "id": "c517babe-52fb-48ba-8920-60df60b3da1e"
                    },
                    "description": None,
                    "id": "381250a0-4d9c-47fd-bbbc-256f72d6cbaa",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Actor",
                        "height": 100,
                        "id": "381250a0-4d9c-47fd-bbbc-256f72d6cbaa",
                        "style": "{}",
                        "width": 100,
                        "x": 1060.0,
                        "y": 378
                    },
                    "innerAggregate": {
                        "command": [],
                        "event": [],
                        "external": [],
                        "policy": [],
                        "view": []
                    },
                    "name": "Librarian",
                    "oldName": "",
                    "rotateStatus": False
                },
                "bca2b9fa-23f4-48cb-81ec-7756345dee9b": {
                    "_type": "org.uengine.modeling.model.Actor",
                    "author": "My-UID",
                    "boundedContext": {
                        "id": "c517babe-52fb-48ba-8920-60df60b3da1e"
                    },
                    "description": None,
                    "id": "bca2b9fa-23f4-48cb-81ec-7756345dee9b",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Actor",
                        "height": 100,
                        "id": "bca2b9fa-23f4-48cb-81ec-7756345dee9b",
                        "style": "{}",
                        "width": 100,
                        "x": 1490.0,
                        "y": 250
                    },
                    "innerAggregate": {
                        "command": [],
                        "event": [],
                        "external": [],
                        "policy": [],
                        "view": []
                    },
                    "name": "Librarian",
                    "oldName": "",
                    "rotateStatus": False
                },
                "ddefa445-30ae-4e41-8729-3b9ee661de39": {
                    "alertURL": "/static/image/symbol/alert-icon.png",
                    "author": "My-UID",
                    "checkAlert": True,
                    "description": None,
                    "id": "ddefa445-30ae-4e41-8729-3b9ee661de39",
                    "elementView": {
                        "angle": 0,
                        "height": 115,
                        "id": "ddefa445-30ae-4e41-8729-3b9ee661de39",
                        "style": "{}",
                        "width": 100,
                        "x": 1759.0,
                        "y": 250,
                        "_type": "org.uengine.modeling.model.Event"
                    },
                    "fieldDescriptors": [
                        {
                            "className": "Long",
                            "isCopy": False,
                            "isKey": True,
                            "name": "statusHistoryId",
                            "nameCamelCase": "statusHistoryId",
                            "namePascalCase": "StatusHistoryId",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "Long",
                            "isCopy": False,
                            "isKey": False,
                            "name": "bookId",
                            "nameCamelCase": "bookId",
                            "namePascalCase": "BookId",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "BookStatus",
                            "isCopy": False,
                            "isKey": False,
                            "name": "previousStatus",
                            "nameCamelCase": "previousStatus",
                            "namePascalCase": "PreviousStatus",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "BookStatus",
                            "isCopy": False,
                            "isKey": False,
                            "name": "currentStatus",
                            "nameCamelCase": "currentStatus",
                            "namePascalCase": "CurrentStatus",
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
                        "id": "ddefa445-30ae-4e41-8729-3b9ee661de39",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0,
                        "_type": "org.uengine.modeling.model.EventHexagonal"
                    },
                    "name": "BookStatusHistoryRecorded",
                    "displayName": "도서 상태 변경 이력이 기록됨",
                    "nameCamelCase": "bookStatusHistoryRecorded",
                    "namePascalCase": "BookStatusHistoryRecorded",
                    "namePlural": "",
                    "relationCommandInfo": [],
                    "relationPolicyInfo": [],
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PostPersist",
                    "_type": "org.uengine.modeling.model.Event",
                    "aggregate": {
                        "id": "4d3ad69a-26a0-4339-b557-dcd54213c61f"
                    },
                    "boundedContext": {
                        "id": "c517babe-52fb-48ba-8920-60df60b3da1e"
                    }
                },
                "00dbfc77-0e4a-4dc9-b132-23d4b5f5767c": {
                    "_type": "org.uengine.modeling.model.Command",
                    "outputEvents": [
                        "BookStatusHistoryRecorded"
                    ],
                    "aggregate": {
                        "id": "4d3ad69a-26a0-4339-b557-dcd54213c61f"
                    },
                    "author": "My-UID",
                    "boundedContext": {
                        "id": "c517babe-52fb-48ba-8920-60df60b3da1e"
                    },
                    "controllerInfo": {
                        "apiPath": "recordbookstatushistory",
                        "method": "POST",
                        "fullApiPath": ""
                    },
                    "fieldDescriptors": [
                        {
                            "className": "Long",
                            "isCopy": False,
                            "isKey": False,
                            "name": "bookId",
                            "nameCamelCase": "bookId",
                            "namePascalCase": "BookId",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "BookStatus",
                            "isCopy": False,
                            "isKey": False,
                            "name": "previousStatus",
                            "nameCamelCase": "previousStatus",
                            "namePascalCase": "PreviousStatus",
                            "displayName": "",
                            "_type": "org.uengine.model.FieldDescriptor"
                        },
                        {
                            "className": "BookStatus",
                            "isCopy": False,
                            "isKey": False,
                            "name": "currentStatus",
                            "nameCamelCase": "currentStatus",
                            "namePascalCase": "CurrentStatus",
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
                    "description": None,
                    "id": "00dbfc77-0e4a-4dc9-b132-23d4b5f5767c",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Command",
                        "height": 115,
                        "id": "00dbfc77-0e4a-4dc9-b132-23d4b5f5767c",
                        "style": "{}",
                        "width": 100,
                        "x": 1571.0,
                        "y": 378,
                        "z-index": 999
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.CommandHexagonal",
                        "height": 0,
                        "id": "00dbfc77-0e4a-4dc9-b132-23d4b5f5767c",
                        "style": "{}",
                        "width": 0,
                        "x": 0,
                        "y": 0
                    },
                    "isRestRepository": False,
                    "name": "RecordBookStatusHistory",
                    "displayName": "도서 상태 변경 이력 기록",
                    "nameCamelCase": "recordBookStatusHistory",
                    "namePascalCase": "RecordBookStatusHistory",
                    "namePlural": "recordBookStatusHistories",
                    "relationCommandInfo": [],
                    "relationEventInfo": [],
                    "restRepositoryInfo": {
                        "method": "POST"
                    },
                    "rotateStatus": False,
                    "selected": False,
                    "trigger": "@PrePersist"
                },
                "d02eb932-1d56-4d13-ac30-70db644de276": {
                    "_type": "org.uengine.modeling.model.Actor",
                    "author": "My-UID",
                    "boundedContext": {
                        "id": "c517babe-52fb-48ba-8920-60df60b3da1e"
                    },
                    "description": None,
                    "id": "d02eb932-1d56-4d13-ac30-70db644de276",
                    "elementView": {
                        "_type": "org.uengine.modeling.model.Actor",
                        "height": 100,
                        "id": "d02eb932-1d56-4d13-ac30-70db644de276",
                        "style": "{}",
                        "width": 100,
                        "x": 1490.0,
                        "y": 378
                    },
                    "innerAggregate": {
                        "command": [],
                        "event": [],
                        "external": [],
                        "policy": [],
                        "view": []
                    },
                    "name": "Librarian",
                    "oldName": "",
                    "rotateStatus": False
                }
            },
            relations={
                "f3dc3e3f-b5b6-475f-8c4f-3ded1e4e2d59": {
                    "_type": "org.uengine.modeling.model.Relation",
                    "name": "",
                    "id": "f3dc3e3f-b5b6-475f-8c4f-3ded1e4e2d59",
                    "sourceElement": {
                        "aggregateRoot": {
                            "_type": "org.uengine.modeling.model.AggregateRoot",
                            "fieldDescriptors": [
                                {
                                    "className": "Long",
                                    "isCopy": False,
                                    "isKey": True,
                                    "name": "loanHistoryId",
                                    "nameCamelCase": "loanHistoryId",
                                    "namePascalCase": "LoanHistoryId",
                                    "displayName": "",
                                    "referenceClass": None,
                                    "isOverrideField": False,
                                    "_type": "org.uengine.model.FieldDescriptor"
                                },
                                {
                                    "className": "String",
                                    "isCopy": False,
                                    "isKey": False,
                                    "name": "bookId",
                                    "nameCamelCase": "bookId",
                                    "namePascalCase": "BookId",
                                    "displayName": "",
                                    "referenceClass": None,
                                    "isOverrideField": False,
                                    "_type": "org.uengine.model.FieldDescriptor"
                                },
                                {
                                    "className": "Member",
                                    "isCopy": False,
                                    "isKey": False,
                                    "name": "member",
                                    "nameCamelCase": "member",
                                    "namePascalCase": "Member",
                                    "displayName": "",
                                    "referenceClass": None,
                                    "isOverrideField": False,
                                    "_type": "org.uengine.model.FieldDescriptor"
                                },
                                {
                                    "className": "LoanType",
                                    "isCopy": False,
                                    "isKey": False,
                                    "name": "loanType",
                                    "nameCamelCase": "loanType",
                                    "namePascalCase": "LoanType",
                                    "displayName": "",
                                    "referenceClass": None,
                                    "isOverrideField": False,
                                    "_type": "org.uengine.model.FieldDescriptor"
                                },
                                {
                                    "className": "Date",
                                    "isCopy": False,
                                    "isKey": False,
                                    "name": "loanStartDate",
                                    "nameCamelCase": "loanStartDate",
                                    "namePascalCase": "LoanStartDate",
                                    "displayName": "",
                                    "referenceClass": None,
                                    "isOverrideField": False,
                                    "_type": "org.uengine.model.FieldDescriptor"
                                },
                                {
                                    "className": "Date",
                                    "isCopy": False,
                                    "isKey": False,
                                    "name": "loanDueDate",
                                    "nameCamelCase": "loanDueDate",
                                    "namePascalCase": "LoanDueDate",
                                    "displayName": "",
                                    "referenceClass": None,
                                    "isOverrideField": False,
                                    "_type": "org.uengine.model.FieldDescriptor"
                                },
                                {
                                    "className": "Date",
                                    "isCopy": False,
                                    "isKey": False,
                                    "name": "returnDate",
                                    "nameCamelCase": "returnDate",
                                    "namePascalCase": "ReturnDate",
                                    "displayName": "",
                                    "referenceClass": None,
                                    "isOverrideField": False,
                                    "_type": "org.uengine.model.FieldDescriptor"
                                },
                                {
                                    "className": "Integer",
                                    "isCopy": False,
                                    "isKey": False,
                                    "name": "overdueDays",
                                    "nameCamelCase": "overdueDays",
                                    "namePascalCase": "OverdueDays",
                                    "displayName": "",
                                    "referenceClass": None,
                                    "isOverrideField": False,
                                    "_type": "org.uengine.model.FieldDescriptor"
                                },
                                {
                                    "className": "Date",
                                    "isCopy": False,
                                    "isKey": False,
                                    "name": "createdAt",
                                    "nameCamelCase": "createdAt",
                                    "namePascalCase": "CreatedAt",
                                    "displayName": "",
                                    "referenceClass": None,
                                    "isOverrideField": False,
                                    "_type": "org.uengine.model.FieldDescriptor"
                                }
                            ],
                            "entities": {
                                "elements": {
                                    "ce774860-ebf5-4d55-9c0f-ce47f6466f5b": {
                                        "_type": "org.uengine.uml.model.Class",
                                        "id": "ce774860-ebf5-4d55-9c0f-ce47f6466f5b",
                                        "name": "LoanHistory",
                                        "namePascalCase": "LoanHistory",
                                        "nameCamelCase": "loanHistory",
                                        "namePlural": "loanHistories",
                                        "fieldDescriptors": [
                                            {
                                                "className": "Long",
                                                "isCopy": False,
                                                "isKey": True,
                                                "name": "loanHistoryId",
                                                "displayName": "",
                                                "nameCamelCase": "loanHistoryId",
                                                "namePascalCase": "LoanHistoryId",
                                                "_type": "org.uengine.model.FieldDescriptor",
                                                "inputUI": None,
                                                "options": None
                                            },
                                            {
                                                "className": "String",
                                                "isCopy": False,
                                                "isKey": False,
                                                "name": "bookId",
                                                "displayName": "",
                                                "nameCamelCase": "bookId",
                                                "namePascalCase": "BookId",
                                                "_type": "org.uengine.model.FieldDescriptor",
                                                "inputUI": None,
                                                "options": None
                                            },
                                            {
                                                "className": "Member",
                                                "isCopy": False,
                                                "isKey": False,
                                                "name": "member",
                                                "displayName": "",
                                                "nameCamelCase": "member",
                                                "namePascalCase": "Member",
                                                "_type": "org.uengine.model.FieldDescriptor",
                                                "inputUI": None,
                                                "options": None
                                            },
                                            {
                                                "className": "LoanType",
                                                "isCopy": False,
                                                "isKey": False,
                                                "name": "loanType",
                                                "displayName": "",
                                                "nameCamelCase": "loanType",
                                                "namePascalCase": "LoanType",
                                                "_type": "org.uengine.model.FieldDescriptor",
                                                "inputUI": None,
                                                "options": None
                                            },
                                            {
                                                "className": "Date",
                                                "isCopy": False,
                                                "isKey": False,
                                                "name": "loanStartDate",
                                                "displayName": "",
                                                "nameCamelCase": "loanStartDate",
                                                "namePascalCase": "LoanStartDate",
                                                "_type": "org.uengine.model.FieldDescriptor",
                                                "inputUI": None,
                                                "options": None
                                            },
                                            {
                                                "className": "Date",
                                                "isCopy": False,
                                                "isKey": False,
                                                "name": "loanDueDate",
                                                "displayName": "",
                                                "nameCamelCase": "loanDueDate",
                                                "namePascalCase": "LoanDueDate",
                                                "_type": "org.uengine.model.FieldDescriptor",
                                                "inputUI": None,
                                                "options": None
                                            },
                                            {
                                                "className": "Date",
                                                "isCopy": False,
                                                "isKey": False,
                                                "name": "returnDate",
                                                "displayName": "",
                                                "nameCamelCase": "returnDate",
                                                "namePascalCase": "ReturnDate",
                                                "_type": "org.uengine.model.FieldDescriptor",
                                                "inputUI": None,
                                                "options": None
                                            },
                                            {
                                                "className": "Integer",
                                                "isCopy": False,
                                                "isKey": False,
                                                "name": "overdueDays",
                                                "displayName": "",
                                                "nameCamelCase": "overdueDays",
                                                "namePascalCase": "OverdueDays",
                                                "_type": "org.uengine.model.FieldDescriptor",
                                                "inputUI": None,
                                                "options": None
                                            },
                                            {
                                                "className": "Date",
                                                "isCopy": False,
                                                "isKey": False,
                                                "name": "createdAt",
                                                "displayName": "",
                                                "nameCamelCase": "createdAt",
                                                "namePascalCase": "CreatedAt",
                                                "_type": "org.uengine.model.FieldDescriptor",
                                                "inputUI": None,
                                                "options": None
                                            }
                                        ],
                                        "operations": [],
                                        "elementView": {
                                            "_type": "org.uengine.uml.model.Class",
                                            "id": "ce774860-ebf5-4d55-9c0f-ce47f6466f5b",
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
                                        "parentId": "b352b64a-a49d-4704-b27f-e532280568d8"
                                    },
                                    "8e253425-bdeb-4a21-8277-57ef1e071f75": {
                                        "_type": "org.uengine.uml.model.vo.Class",
                                        "id": "8e253425-bdeb-4a21-8277-57ef1e071f75",
                                        "name": "Member",
                                        "displayName": "회원",
                                        "namePascalCase": "Member",
                                        "nameCamelCase": "member",
                                        "namePlural": "members",
                                        "fieldDescriptors": [
                                            {
                                                "className": "String",
                                                "isCopy": False,
                                                "isKey": False,
                                                "label": "- memberId: String",
                                                "name": "memberId",
                                                "nameCamelCase": "memberId",
                                                "namePascalCase": "MemberId",
                                                "displayName": "",
                                                "referenceClass": None,
                                                "isOverrideField": False,
                                                "_type": "org.uengine.model.FieldDescriptor"
                                            },
                                            {
                                                "className": "String",
                                                "isCopy": False,
                                                "isKey": False,
                                                "label": "- memberName: String",
                                                "name": "memberName",
                                                "nameCamelCase": "memberName",
                                                "namePascalCase": "MemberName",
                                                "displayName": "",
                                                "referenceClass": None,
                                                "isOverrideField": False,
                                                "_type": "org.uengine.model.FieldDescriptor"
                                            }
                                        ],
                                        "operations": [],
                                        "elementView": {
                                            "_type": "org.uengine.uml.model.vo.address.Class",
                                            "id": "8e253425-bdeb-4a21-8277-57ef1e071f75",
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
                                        "isAbstract": False,
                                        "isInterface": False
                                    },
                                    "cdeaf14e-572c-4e47-a997-6a831bbae718": {
                                        "_type": "org.uengine.uml.model.enum",
                                        "id": "cdeaf14e-572c-4e47-a997-6a831bbae718",
                                        "name": "LoanType",
                                        "displayName": "대출이력타입",
                                        "nameCamelCase": "loanType",
                                        "namePascalCase": "LoanType",
                                        "namePlural": "loanTypes",
                                        "elementView": {
                                            "_type": "org.uengine.uml.model.enum",
                                            "id": "cdeaf14e-572c-4e47-a997-6a831bbae718",
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
                                                "value": "BORROW"
                                            },
                                            {
                                                "value": "RETURN"
                                            },
                                            {
                                                "value": "EXTEND"
                                            },
                                            {
                                                "value": "OVERDUE"
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
                        "author": "My-UID",
                        "boundedContext": {
                            "name": "c517babe-52fb-48ba-8920-60df60b3da1e",
                            "id": "c517babe-52fb-48ba-8920-60df60b3da1e"
                        },
                        "commands": [],
                        "description": None,
                        "id": "b352b64a-a49d-4704-b27f-e532280568d8",
                        "elementView": {
                            "_type": "org.uengine.modeling.model.Aggregate",
                            "id": "b352b64a-a49d-4704-b27f-e532280568d8",
                            "x": 1235.0,
                            "y": 450,
                            "width": 130,
                            "height": 400
                        },
                        "events": [],
                        "hexagonalView": {
                            "_type": "org.uengine.modeling.model.AggregateHexagonal",
                            "id": "b352b64a-a49d-4704-b27f-e532280568d8",
                            "x": 0,
                            "y": 0,
                            "subWidth": 0,
                            "width": 0
                        },
                        "name": "LoanHistory",
                        "displayName": "대출이력",
                        "nameCamelCase": "loanHistory",
                        "namePascalCase": "LoanHistory",
                        "namePlural": "loanHistories",
                        "rotateStatus": False,
                        "selected": False,
                        "_type": "org.uengine.modeling.model.Aggregate"
                    },
                    "targetElement": {
                        "aggregateRoot": {
                            "_type": "org.uengine.modeling.model.AggregateRoot",
                            "fieldDescriptors": [
                                {
                                    "className": "Long",
                                    "isCopy": False,
                                    "isKey": True,
                                    "name": "bookId",
                                    "nameCamelCase": "bookId",
                                    "namePascalCase": "BookId",
                                    "displayName": "",
                                    "referenceClass": None,
                                    "isOverrideField": False,
                                    "_type": "org.uengine.model.FieldDescriptor"
                                },
                                {
                                    "className": "String",
                                    "isCopy": False,
                                    "isKey": False,
                                    "name": "title",
                                    "nameCamelCase": "title",
                                    "namePascalCase": "Title",
                                    "displayName": "",
                                    "referenceClass": None,
                                    "isOverrideField": False,
                                    "_type": "org.uengine.model.FieldDescriptor"
                                },
                                {
                                    "className": "String",
                                    "isCopy": False,
                                    "isKey": False,
                                    "name": "isbn",
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
                                    "className": "BookCategory",
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
                                    "className": "BookStatus",
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
                                    "4541e3cb-de79-4e55-a238-4b5c158d2c5f": {
                                        "_type": "org.uengine.uml.model.Class",
                                        "id": "4541e3cb-de79-4e55-a238-4b5c158d2c5f",
                                        "name": "Book",
                                        "namePascalCase": "Book",
                                        "nameCamelCase": "book",
                                        "namePlural": "books",
                                        "fieldDescriptors": [
                                            {
                                                "className": "Long",
                                                "isCopy": False,
                                                "isKey": True,
                                                "name": "bookId",
                                                "displayName": "",
                                                "nameCamelCase": "bookId",
                                                "namePascalCase": "BookId",
                                                "_type": "org.uengine.model.FieldDescriptor",
                                                "inputUI": None,
                                                "options": None
                                            },
                                            {
                                                "className": "String",
                                                "isCopy": False,
                                                "isKey": False,
                                                "name": "title",
                                                "displayName": "",
                                                "nameCamelCase": "title",
                                                "namePascalCase": "Title",
                                                "_type": "org.uengine.model.FieldDescriptor",
                                                "inputUI": None,
                                                "options": None
                                            },
                                            {
                                                "className": "String",
                                                "isCopy": False,
                                                "isKey": False,
                                                "name": "isbn",
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
                                                "className": "BookCategory",
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
                                                "className": "BookStatus",
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
                                            "id": "4541e3cb-de79-4e55-a238-4b5c158d2c5f",
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
                                        "parentId": "8e794426-f189-4559-8e36-0a8b457c3db9"
                                    },
                                    "80a5e04e-bd4d-4387-b5dc-25b6d79a5089": {
                                        "_type": "org.uengine.uml.model.enum",
                                        "id": "80a5e04e-bd4d-4387-b5dc-25b6d79a5089",
                                        "name": "BookStatus",
                                        "displayName": "도서상태",
                                        "nameCamelCase": "bookStatus",
                                        "namePascalCase": "BookStatus",
                                        "namePlural": "bookStatuses",
                                        "elementView": {
                                            "_type": "org.uengine.uml.model.enum",
                                            "id": "80a5e04e-bd4d-4387-b5dc-25b6d79a5089",
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
                                                "value": "AVAILABLE"
                                            },
                                            {
                                                "value": "BORROWED"
                                            },
                                            {
                                                "value": "RESERVED"
                                            },
                                            {
                                                "value": "DISPOSED"
                                            }
                                        ],
                                        "useKeyValue": False,
                                        "relations": []
                                    },
                                    "a50b5105-1d52-4925-bcb2-f4899b109978": {
                                        "_type": "org.uengine.uml.model.enum",
                                        "id": "a50b5105-1d52-4925-bcb2-f4899b109978",
                                        "name": "BookCategory",
                                        "displayName": "도서카테고리",
                                        "nameCamelCase": "bookCategory",
                                        "namePascalCase": "BookCategory",
                                        "namePlural": "bookCategories",
                                        "elementView": {
                                            "_type": "org.uengine.uml.model.enum",
                                            "id": "a50b5105-1d52-4925-bcb2-f4899b109978",
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
                                    }
                                },
                                "relations": {}
                            },
                            "operations": []
                        },
                        "author": "My-UID",
                        "boundedContext": {
                            "name": "6b5d96ec-a502-4242-a6d4-890ec1b2104e",
                            "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
                        },
                        "commands": [],
                        "description": None,
                        "id": "8e794426-f189-4559-8e36-0a8b457c3db9",
                        "elementView": {
                            "_type": "org.uengine.modeling.model.Aggregate",
                            "id": "8e794426-f189-4559-8e36-0a8b457c3db9",
                            "x": 650,
                            "y": 450,
                            "width": 130,
                            "height": 400
                        },
                        "events": [],
                        "hexagonalView": {
                            "_type": "org.uengine.modeling.model.AggregateHexagonal",
                            "id": "8e794426-f189-4559-8e36-0a8b457c3db9",
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
                    "from": "b352b64a-a49d-4704-b27f-e532280568d8",
                    "to": "8e794426-f189-4559-8e36-0a8b457c3db9",
                    "relationView": {
                        "id": "f3dc3e3f-b5b6-475f-8c4f-3ded1e4e2d59",
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "from": "b352b64a-a49d-4704-b27f-e532280568d8",
                        "to": "8e794426-f189-4559-8e36-0a8b457c3db9",
                        "needReconnect": True,
                        "value": "[]"
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.RelationHexagonal",
                        "from": "b352b64a-a49d-4704-b27f-e532280568d8",
                        "id": "f3dc3e3f-b5b6-475f-8c4f-3ded1e4e2d59",
                        "needReconnect": True,
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "to": "8e794426-f189-4559-8e36-0a8b457c3db9",
                        "value": None
                    },
                    "sourceMultiplicity": "1",
                    "targetMultiplicity": "1"
                },
                "e9bbe97a-2758-4393-9c28-1e23d0b298ef": {
                    "_type": "org.uengine.modeling.model.Relation",
                    "name": "",
                    "id": "e9bbe97a-2758-4393-9c28-1e23d0b298ef",
                    "sourceElement": {
                        "_type": "org.uengine.modeling.model.Command",
                        "outputEvents": [
                            "BookRegistered",
                            "BookRegistrationFailedDueToDuplicateISBN",
                            "BookRegistrationFailedDueToInvalidISBNFormat"
                        ],
                        "aggregate": {
                            "id": "8e794426-f189-4559-8e36-0a8b457c3db9"
                        },
                        "author": "My-UID",
                        "boundedContext": {
                            "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
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
                                "isKey": False,
                                "name": "title",
                                "nameCamelCase": "title",
                                "namePascalCase": "Title",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": False,
                                "name": "isbn",
                                "nameCamelCase": "isbn",
                                "namePascalCase": "Isbn",
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
                                "className": "BookCategory",
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
                        "id": "9cb00a7a-b78a-4d60-82ac-5c1d582692d3",
                        "elementView": {
                            "_type": "org.uengine.modeling.model.Command",
                            "height": 115,
                            "id": "9cb00a7a-b78a-4d60-82ac-5c1d582692d3",
                            "style": "{}",
                            "width": 100,
                            "x": 556,
                            "y": 250,
                            "z-index": 999
                        },
                        "hexagonalView": {
                            "_type": "org.uengine.modeling.model.CommandHexagonal",
                            "height": 0,
                            "id": "9cb00a7a-b78a-4d60-82ac-5c1d582692d3",
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
                        "author": "My-UID",
                        "checkAlert": True,
                        "description": None,
                        "id": "19b5f83b-aea7-4f19-bb09-c43ac32e4bd9",
                        "elementView": {
                            "angle": 0,
                            "height": 115,
                            "id": "19b5f83b-aea7-4f19-bb09-c43ac32e4bd9",
                            "style": "{}",
                            "width": 100,
                            "x": 744,
                            "y": 250,
                            "_type": "org.uengine.modeling.model.Event"
                        },
                        "fieldDescriptors": [
                            {
                                "className": "Long",
                                "isCopy": False,
                                "isKey": True,
                                "name": "bookId",
                                "nameCamelCase": "bookId",
                                "namePascalCase": "BookId",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": False,
                                "name": "title",
                                "nameCamelCase": "title",
                                "namePascalCase": "Title",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": False,
                                "name": "isbn",
                                "nameCamelCase": "isbn",
                                "namePascalCase": "Isbn",
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
                                "className": "BookCategory",
                                "isCopy": False,
                                "isKey": False,
                                "name": "category",
                                "nameCamelCase": "category",
                                "namePascalCase": "Category",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "BookStatus",
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
                            "id": "19b5f83b-aea7-4f19-bb09-c43ac32e4bd9",
                            "style": "{}",
                            "width": 0,
                            "x": 0,
                            "y": 0,
                            "_type": "org.uengine.modeling.model.EventHexagonal"
                        },
                        "name": "BookRegistered",
                        "displayName": "도서가 등록됨",
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
                            "id": "8e794426-f189-4559-8e36-0a8b457c3db9"
                        },
                        "boundedContext": {
                            "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
                        }
                    },
                    "from": "9cb00a7a-b78a-4d60-82ac-5c1d582692d3",
                    "to": "19b5f83b-aea7-4f19-bb09-c43ac32e4bd9",
                    "relationView": {
                        "id": "e9bbe97a-2758-4393-9c28-1e23d0b298ef",
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "from": "9cb00a7a-b78a-4d60-82ac-5c1d582692d3",
                        "to": "19b5f83b-aea7-4f19-bb09-c43ac32e4bd9",
                        "needReconnect": True,
                        "value": "[]"
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.RelationHexagonal",
                        "from": "9cb00a7a-b78a-4d60-82ac-5c1d582692d3",
                        "id": "e9bbe97a-2758-4393-9c28-1e23d0b298ef",
                        "needReconnect": True,
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "to": "19b5f83b-aea7-4f19-bb09-c43ac32e4bd9",
                        "value": None
                    },
                    "sourceMultiplicity": "1",
                    "targetMultiplicity": "1"
                },
                "3b931ed0-d343-48e0-aa14-df8cfdd28493": {
                    "_type": "org.uengine.modeling.model.Relation",
                    "name": "",
                    "id": "3b931ed0-d343-48e0-aa14-df8cfdd28493",
                    "sourceElement": {
                        "_type": "org.uengine.modeling.model.Command",
                        "outputEvents": [
                            "BookRegistered",
                            "BookRegistrationFailedDueToDuplicateISBN",
                            "BookRegistrationFailedDueToInvalidISBNFormat"
                        ],
                        "aggregate": {
                            "id": "8e794426-f189-4559-8e36-0a8b457c3db9"
                        },
                        "author": "My-UID",
                        "boundedContext": {
                            "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
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
                                "isKey": False,
                                "name": "title",
                                "nameCamelCase": "title",
                                "namePascalCase": "Title",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": False,
                                "name": "isbn",
                                "nameCamelCase": "isbn",
                                "namePascalCase": "Isbn",
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
                                "className": "BookCategory",
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
                        "id": "9cb00a7a-b78a-4d60-82ac-5c1d582692d3",
                        "elementView": {
                            "_type": "org.uengine.modeling.model.Command",
                            "height": 115,
                            "id": "9cb00a7a-b78a-4d60-82ac-5c1d582692d3",
                            "style": "{}",
                            "width": 100,
                            "x": 556,
                            "y": 250,
                            "z-index": 999
                        },
                        "hexagonalView": {
                            "_type": "org.uengine.modeling.model.CommandHexagonal",
                            "height": 0,
                            "id": "9cb00a7a-b78a-4d60-82ac-5c1d582692d3",
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
                        "author": "My-UID",
                        "checkAlert": True,
                        "description": None,
                        "id": "dbd2d70b-ec51-4385-b811-31f3c9ef15e1",
                        "elementView": {
                            "angle": 0,
                            "height": 115,
                            "id": "dbd2d70b-ec51-4385-b811-31f3c9ef15e1",
                            "style": "{}",
                            "width": 100,
                            "x": 744,
                            "y": 378,
                            "_type": "org.uengine.modeling.model.Event"
                        },
                        "fieldDescriptors": [
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": False,
                                "name": "isbn",
                                "nameCamelCase": "isbn",
                                "namePascalCase": "Isbn",
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
                            "id": "dbd2d70b-ec51-4385-b811-31f3c9ef15e1",
                            "style": "{}",
                            "width": 0,
                            "x": 0,
                            "y": 0,
                            "_type": "org.uengine.modeling.model.EventHexagonal"
                        },
                        "name": "BookRegistrationFailedDueToDuplicateISBN",
                        "displayName": "ISBN 중복으로 도서 등록 실패함",
                        "nameCamelCase": "bookregistrationfailedduetoduplicateisbn",
                        "namePascalCase": "Bookregistrationfailedduetoduplicateisbn",
                        "namePlural": "",
                        "relationCommandInfo": [],
                        "relationPolicyInfo": [],
                        "rotateStatus": False,
                        "selected": False,
                        "trigger": "@PostPersist",
                        "_type": "org.uengine.modeling.model.Event",
                        "aggregate": {
                            "id": "8e794426-f189-4559-8e36-0a8b457c3db9"
                        },
                        "boundedContext": {
                            "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
                        }
                    },
                    "from": "9cb00a7a-b78a-4d60-82ac-5c1d582692d3",
                    "to": "dbd2d70b-ec51-4385-b811-31f3c9ef15e1",
                    "relationView": {
                        "id": "3b931ed0-d343-48e0-aa14-df8cfdd28493",
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "from": "9cb00a7a-b78a-4d60-82ac-5c1d582692d3",
                        "to": "dbd2d70b-ec51-4385-b811-31f3c9ef15e1",
                        "needReconnect": True,
                        "value": "[]"
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.RelationHexagonal",
                        "from": "9cb00a7a-b78a-4d60-82ac-5c1d582692d3",
                        "id": "3b931ed0-d343-48e0-aa14-df8cfdd28493",
                        "needReconnect": True,
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "to": "dbd2d70b-ec51-4385-b811-31f3c9ef15e1",
                        "value": None
                    },
                    "sourceMultiplicity": "1",
                    "targetMultiplicity": "1"
                },
                "d69e09e9-e92e-4baa-a7f2-52ba0ea639df": {
                    "_type": "org.uengine.modeling.model.Relation",
                    "name": "",
                    "id": "d69e09e9-e92e-4baa-a7f2-52ba0ea639df",
                    "sourceElement": {
                        "_type": "org.uengine.modeling.model.Command",
                        "outputEvents": [
                            "BookRegistered",
                            "BookRegistrationFailedDueToDuplicateISBN",
                            "BookRegistrationFailedDueToInvalidISBNFormat"
                        ],
                        "aggregate": {
                            "id": "8e794426-f189-4559-8e36-0a8b457c3db9"
                        },
                        "author": "My-UID",
                        "boundedContext": {
                            "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
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
                                "isKey": False,
                                "name": "title",
                                "nameCamelCase": "title",
                                "namePascalCase": "Title",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": False,
                                "name": "isbn",
                                "nameCamelCase": "isbn",
                                "namePascalCase": "Isbn",
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
                                "className": "BookCategory",
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
                        "id": "9cb00a7a-b78a-4d60-82ac-5c1d582692d3",
                        "elementView": {
                            "_type": "org.uengine.modeling.model.Command",
                            "height": 115,
                            "id": "9cb00a7a-b78a-4d60-82ac-5c1d582692d3",
                            "style": "{}",
                            "width": 100,
                            "x": 556,
                            "y": 250,
                            "z-index": 999
                        },
                        "hexagonalView": {
                            "_type": "org.uengine.modeling.model.CommandHexagonal",
                            "height": 0,
                            "id": "9cb00a7a-b78a-4d60-82ac-5c1d582692d3",
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
                        "author": "My-UID",
                        "checkAlert": True,
                        "description": None,
                        "id": "1c18e36c-49a8-49d3-9f07-5b68cc386450",
                        "elementView": {
                            "angle": 0,
                            "height": 115,
                            "id": "1c18e36c-49a8-49d3-9f07-5b68cc386450",
                            "style": "{}",
                            "width": 100,
                            "x": 744,
                            "y": 506,
                            "_type": "org.uengine.modeling.model.Event"
                        },
                        "fieldDescriptors": [
                            {
                                "className": "String",
                                "isCopy": False,
                                "isKey": False,
                                "name": "isbn",
                                "nameCamelCase": "isbn",
                                "namePascalCase": "Isbn",
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
                            "id": "1c18e36c-49a8-49d3-9f07-5b68cc386450",
                            "style": "{}",
                            "width": 0,
                            "x": 0,
                            "y": 0,
                            "_type": "org.uengine.modeling.model.EventHexagonal"
                        },
                        "name": "BookRegistrationFailedDueToInvalidISBNFormat",
                        "displayName": "ISBN 형식 오류로 도서 등록 실패함",
                        "nameCamelCase": "bookregistrationfailedduetoinvalidisbnformat",
                        "namePascalCase": "Bookregistrationfailedduetoinvalidisbnformat",
                        "namePlural": "",
                        "relationCommandInfo": [],
                        "relationPolicyInfo": [],
                        "rotateStatus": False,
                        "selected": False,
                        "trigger": "@PostPersist",
                        "_type": "org.uengine.modeling.model.Event",
                        "aggregate": {
                            "id": "8e794426-f189-4559-8e36-0a8b457c3db9"
                        },
                        "boundedContext": {
                            "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
                        }
                    },
                    "from": "9cb00a7a-b78a-4d60-82ac-5c1d582692d3",
                    "to": "1c18e36c-49a8-49d3-9f07-5b68cc386450",
                    "relationView": {
                        "id": "d69e09e9-e92e-4baa-a7f2-52ba0ea639df",
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "from": "9cb00a7a-b78a-4d60-82ac-5c1d582692d3",
                        "to": "1c18e36c-49a8-49d3-9f07-5b68cc386450",
                        "needReconnect": True,
                        "value": "[]"
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.RelationHexagonal",
                        "from": "9cb00a7a-b78a-4d60-82ac-5c1d582692d3",
                        "id": "d69e09e9-e92e-4baa-a7f2-52ba0ea639df",
                        "needReconnect": True,
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "to": "1c18e36c-49a8-49d3-9f07-5b68cc386450",
                        "value": None
                    },
                    "sourceMultiplicity": "1",
                    "targetMultiplicity": "1"
                },
                "2a224a23-5bb2-4a72-aeb0-ee1c1636bc76": {
                    "_type": "org.uengine.modeling.model.Relation",
                    "name": "",
                    "id": "2a224a23-5bb2-4a72-aeb0-ee1c1636bc76",
                    "sourceElement": {
                        "_type": "org.uengine.modeling.model.Command",
                        "outputEvents": [
                            "BookStateChanged"
                        ],
                        "aggregate": {
                            "id": "8e794426-f189-4559-8e36-0a8b457c3db9"
                        },
                        "author": "My-UID",
                        "boundedContext": {
                            "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
                        },
                        "controllerInfo": {
                            "apiPath": "changebookstatus",
                            "method": "PATCH",
                            "fullApiPath": ""
                        },
                        "fieldDescriptors": [
                            {
                                "className": "Long",
                                "isCopy": False,
                                "isKey": True,
                                "name": "bookId",
                                "nameCamelCase": "bookId",
                                "namePascalCase": "BookId",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "BookStatus",
                                "isCopy": False,
                                "isKey": False,
                                "name": "newStatus",
                                "nameCamelCase": "newStatus",
                                "namePascalCase": "NewStatus",
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
                        "id": "f7614022-234a-4a55-bf35-703f02f90595",
                        "elementView": {
                            "_type": "org.uengine.modeling.model.Command",
                            "height": 115,
                            "id": "f7614022-234a-4a55-bf35-703f02f90595",
                            "style": "{}",
                            "width": 100,
                            "x": 556,
                            "y": 378,
                            "z-index": 999
                        },
                        "hexagonalView": {
                            "_type": "org.uengine.modeling.model.CommandHexagonal",
                            "height": 0,
                            "id": "f7614022-234a-4a55-bf35-703f02f90595",
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
                            "method": "PATCH"
                        },
                        "rotateStatus": False,
                        "selected": False,
                        "trigger": "@PrePersist"
                    },
                    "targetElement": {
                        "alertURL": "/static/image/symbol/alert-icon.png",
                        "author": "My-UID",
                        "checkAlert": True,
                        "description": None,
                        "id": "dce353ac-1c01-437d-846a-e541170d2317",
                        "elementView": {
                            "angle": 0,
                            "height": 115,
                            "id": "dce353ac-1c01-437d-846a-e541170d2317",
                            "style": "{}",
                            "width": 100,
                            "x": 744,
                            "y": 634,
                            "_type": "org.uengine.modeling.model.Event"
                        },
                        "fieldDescriptors": [
                            {
                                "className": "Long",
                                "isCopy": False,
                                "isKey": True,
                                "name": "bookId",
                                "nameCamelCase": "bookId",
                                "namePascalCase": "BookId",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "BookStatus",
                                "isCopy": False,
                                "isKey": False,
                                "name": "previousStatus",
                                "nameCamelCase": "previousStatus",
                                "namePascalCase": "PreviousStatus",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "BookStatus",
                                "isCopy": False,
                                "isKey": False,
                                "name": "currentStatus",
                                "nameCamelCase": "currentStatus",
                                "namePascalCase": "CurrentStatus",
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
                            "id": "dce353ac-1c01-437d-846a-e541170d2317",
                            "style": "{}",
                            "width": 0,
                            "x": 0,
                            "y": 0,
                            "_type": "org.uengine.modeling.model.EventHexagonal"
                        },
                        "name": "BookStateChanged",
                        "displayName": "도서 상태가 변경됨",
                        "nameCamelCase": "bookStateChanged",
                        "namePascalCase": "BookStateChanged",
                        "namePlural": "",
                        "relationCommandInfo": [],
                        "relationPolicyInfo": [],
                        "rotateStatus": False,
                        "selected": False,
                        "trigger": "@PostPersist",
                        "_type": "org.uengine.modeling.model.Event",
                        "aggregate": {
                            "id": "8e794426-f189-4559-8e36-0a8b457c3db9"
                        },
                        "boundedContext": {
                            "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
                        }
                    },
                    "from": "f7614022-234a-4a55-bf35-703f02f90595",
                    "to": "dce353ac-1c01-437d-846a-e541170d2317",
                    "relationView": {
                        "id": "2a224a23-5bb2-4a72-aeb0-ee1c1636bc76",
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "from": "f7614022-234a-4a55-bf35-703f02f90595",
                        "to": "dce353ac-1c01-437d-846a-e541170d2317",
                        "needReconnect": True,
                        "value": "[]"
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.RelationHexagonal",
                        "from": "f7614022-234a-4a55-bf35-703f02f90595",
                        "id": "2a224a23-5bb2-4a72-aeb0-ee1c1636bc76",
                        "needReconnect": True,
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "to": "dce353ac-1c01-437d-846a-e541170d2317",
                        "value": None
                    },
                    "sourceMultiplicity": "1",
                    "targetMultiplicity": "1"
                },
                "d91a9a9a-d63e-420d-8130-abf0296a54fe": {
                    "_type": "org.uengine.modeling.model.Relation",
                    "name": "",
                    "id": "d91a9a9a-d63e-420d-8130-abf0296a54fe",
                    "sourceElement": {
                        "_type": "org.uengine.modeling.model.Command",
                        "outputEvents": [
                            "BookDisposed"
                        ],
                        "aggregate": {
                            "id": "8e794426-f189-4559-8e36-0a8b457c3db9"
                        },
                        "author": "My-UID",
                        "boundedContext": {
                            "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
                        },
                        "controllerInfo": {
                            "apiPath": "disposebook",
                            "method": "PATCH",
                            "fullApiPath": ""
                        },
                        "fieldDescriptors": [
                            {
                                "className": "Long",
                                "isCopy": False,
                                "isKey": True,
                                "name": "bookId",
                                "nameCamelCase": "bookId",
                                "namePascalCase": "BookId",
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
                        "id": "139ce9e9-06f5-4a7f-8e4b-76b138c297ef",
                        "elementView": {
                            "_type": "org.uengine.modeling.model.Command",
                            "height": 115,
                            "id": "139ce9e9-06f5-4a7f-8e4b-76b138c297ef",
                            "style": "{}",
                            "width": 100,
                            "x": 556,
                            "y": 506,
                            "z-index": 999
                        },
                        "hexagonalView": {
                            "_type": "org.uengine.modeling.model.CommandHexagonal",
                            "height": 0,
                            "id": "139ce9e9-06f5-4a7f-8e4b-76b138c297ef",
                            "style": "{}",
                            "width": 0,
                            "x": 0,
                            "y": 0
                        },
                        "isRestRepository": False,
                        "name": "DisposeBook",
                        "displayName": "도서 폐기 처리",
                        "nameCamelCase": "disposeBook",
                        "namePascalCase": "DisposeBook",
                        "namePlural": "disposeBooks",
                        "relationCommandInfo": [],
                        "relationEventInfo": [],
                        "restRepositoryInfo": {
                            "method": "PATCH"
                        },
                        "rotateStatus": False,
                        "selected": False,
                        "trigger": "@PrePersist"
                    },
                    "targetElement": {
                        "alertURL": "/static/image/symbol/alert-icon.png",
                        "author": "My-UID",
                        "checkAlert": True,
                        "description": None,
                        "id": "73448c06-5848-4a92-90f9-6fd5a7a5f7f5",
                        "elementView": {
                            "angle": 0,
                            "height": 115,
                            "id": "73448c06-5848-4a92-90f9-6fd5a7a5f7f5",
                            "style": "{}",
                            "width": 100,
                            "x": 744,
                            "y": 762,
                            "_type": "org.uengine.modeling.model.Event"
                        },
                        "fieldDescriptors": [
                            {
                                "className": "Long",
                                "isCopy": False,
                                "isKey": True,
                                "name": "bookId",
                                "nameCamelCase": "bookId",
                                "namePascalCase": "BookId",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Date",
                                "isCopy": False,
                                "isKey": False,
                                "name": "disposedAt",
                                "nameCamelCase": "disposedAt",
                                "namePascalCase": "DisposedAt",
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
                            "id": "73448c06-5848-4a92-90f9-6fd5a7a5f7f5",
                            "style": "{}",
                            "width": 0,
                            "x": 0,
                            "y": 0,
                            "_type": "org.uengine.modeling.model.EventHexagonal"
                        },
                        "name": "BookDisposed",
                        "displayName": "도서가 폐기됨",
                        "nameCamelCase": "bookDisposed",
                        "namePascalCase": "BookDisposed",
                        "namePlural": "",
                        "relationCommandInfo": [],
                        "relationPolicyInfo": [],
                        "rotateStatus": False,
                        "selected": False,
                        "trigger": "@PostPersist",
                        "_type": "org.uengine.modeling.model.Event",
                        "aggregate": {
                            "id": "8e794426-f189-4559-8e36-0a8b457c3db9"
                        },
                        "boundedContext": {
                            "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
                        }
                    },
                    "from": "139ce9e9-06f5-4a7f-8e4b-76b138c297ef",
                    "to": "73448c06-5848-4a92-90f9-6fd5a7a5f7f5",
                    "relationView": {
                        "id": "d91a9a9a-d63e-420d-8130-abf0296a54fe",
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "from": "139ce9e9-06f5-4a7f-8e4b-76b138c297ef",
                        "to": "73448c06-5848-4a92-90f9-6fd5a7a5f7f5",
                        "needReconnect": True,
                        "value": "[]"
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.RelationHexagonal",
                        "from": "139ce9e9-06f5-4a7f-8e4b-76b138c297ef",
                        "id": "d91a9a9a-d63e-420d-8130-abf0296a54fe",
                        "needReconnect": True,
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "to": "73448c06-5848-4a92-90f9-6fd5a7a5f7f5",
                        "value": None
                    },
                    "sourceMultiplicity": "1",
                    "targetMultiplicity": "1"
                },
                "7642a6d4-7b5b-4b1b-8bb5-5cfb5d2c36c0": {
                    "_type": "org.uengine.modeling.model.Relation",
                    "name": "",
                    "id": "7642a6d4-7b5b-4b1b-8bb5-5cfb5d2c36c0",
                    "sourceElement": {
                        "_type": "org.uengine.modeling.model.Command",
                        "outputEvents": [
                            "BookLoanReservationBlocked"
                        ],
                        "aggregate": {
                            "id": "8e794426-f189-4559-8e36-0a8b457c3db9"
                        },
                        "author": "My-UID",
                        "boundedContext": {
                            "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
                        },
                        "controllerInfo": {
                            "apiPath": "blockloanorreservationfordisposedbook",
                            "method": "POST",
                            "fullApiPath": ""
                        },
                        "fieldDescriptors": [
                            {
                                "className": "Long",
                                "isCopy": False,
                                "isKey": True,
                                "name": "bookId",
                                "nameCamelCase": "bookId",
                                "namePascalCase": "BookId",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            }
                        ],
                        "description": None,
                        "id": "615bf707-e57b-437a-98af-29694c0ea7b2",
                        "elementView": {
                            "_type": "org.uengine.modeling.model.Command",
                            "height": 115,
                            "id": "615bf707-e57b-437a-98af-29694c0ea7b2",
                            "style": "{}",
                            "width": 100,
                            "x": 556,
                            "y": 634,
                            "z-index": 999
                        },
                        "hexagonalView": {
                            "_type": "org.uengine.modeling.model.CommandHexagonal",
                            "height": 0,
                            "id": "615bf707-e57b-437a-98af-29694c0ea7b2",
                            "style": "{}",
                            "width": 0,
                            "x": 0,
                            "y": 0
                        },
                        "isRestRepository": False,
                        "name": "BlockLoanOrReservationForDisposedBook",
                        "displayName": "폐기 도서 대출/예약 차단",
                        "nameCamelCase": "blockLoanOrReservationForDisposedBook",
                        "namePascalCase": "BlockLoanOrReservationForDisposedBook",
                        "namePlural": "blockLoanOrReservationForDisposedBooks",
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
                        "author": "My-UID",
                        "checkAlert": True,
                        "description": None,
                        "id": "ab8d9f62-bc9f-4dda-bfa6-ee5becc12bf7",
                        "elementView": {
                            "angle": 0,
                            "height": 115,
                            "id": "ab8d9f62-bc9f-4dda-bfa6-ee5becc12bf7",
                            "style": "{}",
                            "width": 100,
                            "x": 744,
                            "y": 890,
                            "_type": "org.uengine.modeling.model.Event"
                        },
                        "fieldDescriptors": [
                            {
                                "className": "Long",
                                "isCopy": False,
                                "isKey": True,
                                "name": "bookId",
                                "nameCamelCase": "bookId",
                                "namePascalCase": "BookId",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Date",
                                "isCopy": False,
                                "isKey": False,
                                "name": "blockedAt",
                                "nameCamelCase": "blockedAt",
                                "namePascalCase": "BlockedAt",
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
                            "id": "ab8d9f62-bc9f-4dda-bfa6-ee5becc12bf7",
                            "style": "{}",
                            "width": 0,
                            "x": 0,
                            "y": 0,
                            "_type": "org.uengine.modeling.model.EventHexagonal"
                        },
                        "name": "BookLoanReservationBlocked",
                        "displayName": "폐기 도서 대출/예약 차단됨",
                        "nameCamelCase": "bookLoanReservationBlocked",
                        "namePascalCase": "BookLoanReservationBlocked",
                        "namePlural": "",
                        "relationCommandInfo": [],
                        "relationPolicyInfo": [],
                        "rotateStatus": False,
                        "selected": False,
                        "trigger": "@PostPersist",
                        "_type": "org.uengine.modeling.model.Event",
                        "aggregate": {
                            "id": "8e794426-f189-4559-8e36-0a8b457c3db9"
                        },
                        "boundedContext": {
                            "id": "6b5d96ec-a502-4242-a6d4-890ec1b2104e"
                        }
                    },
                    "from": "615bf707-e57b-437a-98af-29694c0ea7b2",
                    "to": "ab8d9f62-bc9f-4dda-bfa6-ee5becc12bf7",
                    "relationView": {
                        "id": "7642a6d4-7b5b-4b1b-8bb5-5cfb5d2c36c0",
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "from": "615bf707-e57b-437a-98af-29694c0ea7b2",
                        "to": "ab8d9f62-bc9f-4dda-bfa6-ee5becc12bf7",
                        "needReconnect": True,
                        "value": "[]"
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.RelationHexagonal",
                        "from": "615bf707-e57b-437a-98af-29694c0ea7b2",
                        "id": "7642a6d4-7b5b-4b1b-8bb5-5cfb5d2c36c0",
                        "needReconnect": True,
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "to": "ab8d9f62-bc9f-4dda-bfa6-ee5becc12bf7",
                        "value": None
                    },
                    "sourceMultiplicity": "1",
                    "targetMultiplicity": "1"
                },
                "30f53302-8bdc-4d09-a199-9a60d924486b": {
                    "_type": "org.uengine.modeling.model.Relation",
                    "name": "",
                    "id": "30f53302-8bdc-4d09-a199-9a60d924486b",
                    "sourceElement": {
                        "_type": "org.uengine.modeling.model.Command",
                        "outputEvents": [
                            "LoanHistoryRecorded"
                        ],
                        "aggregate": {
                            "id": "b352b64a-a49d-4704-b27f-e532280568d8"
                        },
                        "author": "My-UID",
                        "boundedContext": {
                            "id": "c517babe-52fb-48ba-8920-60df60b3da1e"
                        },
                        "controllerInfo": {
                            "apiPath": "recordloanhistory",
                            "method": "POST",
                            "fullApiPath": ""
                        },
                        "fieldDescriptors": [
                            {
                                "className": "Long",
                                "isCopy": False,
                                "isKey": False,
                                "name": "bookId",
                                "nameCamelCase": "bookId",
                                "namePascalCase": "BookId",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Member",
                                "isCopy": False,
                                "isKey": False,
                                "name": "member",
                                "nameCamelCase": "member",
                                "namePascalCase": "Member",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "LoanType",
                                "isCopy": False,
                                "isKey": False,
                                "name": "loanType",
                                "nameCamelCase": "loanType",
                                "namePascalCase": "LoanType",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Date",
                                "isCopy": False,
                                "isKey": False,
                                "name": "loanStartDate",
                                "nameCamelCase": "loanStartDate",
                                "namePascalCase": "LoanStartDate",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Date",
                                "isCopy": False,
                                "isKey": False,
                                "name": "loanDueDate",
                                "nameCamelCase": "loanDueDate",
                                "namePascalCase": "LoanDueDate",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Date",
                                "isCopy": False,
                                "isKey": False,
                                "name": "returnDate",
                                "nameCamelCase": "returnDate",
                                "namePascalCase": "ReturnDate",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Integer",
                                "isCopy": False,
                                "isKey": False,
                                "name": "overdueDays",
                                "nameCamelCase": "overdueDays",
                                "namePascalCase": "OverdueDays",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Date",
                                "isCopy": False,
                                "isKey": False,
                                "name": "createdAt",
                                "nameCamelCase": "createdAt",
                                "namePascalCase": "CreatedAt",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            }
                        ],
                        "description": None,
                        "id": "3b804b8b-3b73-46b6-b8d0-a8892db6c0f2",
                        "elementView": {
                            "_type": "org.uengine.modeling.model.Command",
                            "height": 115,
                            "id": "3b804b8b-3b73-46b6-b8d0-a8892db6c0f2",
                            "style": "{}",
                            "width": 100,
                            "x": 1141.0,
                            "y": 250,
                            "z-index": 999
                        },
                        "hexagonalView": {
                            "_type": "org.uengine.modeling.model.CommandHexagonal",
                            "height": 0,
                            "id": "3b804b8b-3b73-46b6-b8d0-a8892db6c0f2",
                            "style": "{}",
                            "width": 0,
                            "x": 0,
                            "y": 0
                        },
                        "isRestRepository": False,
                        "name": "RecordLoanHistory",
                        "displayName": "대출 이력 기록",
                        "nameCamelCase": "recordLoanHistory",
                        "namePascalCase": "RecordLoanHistory",
                        "namePlural": "recordLoanHistories",
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
                        "author": "My-UID",
                        "checkAlert": True,
                        "description": None,
                        "id": "8b664b48-2e29-48f8-8908-7555193344ee",
                        "elementView": {
                            "angle": 0,
                            "height": 115,
                            "id": "8b664b48-2e29-48f8-8908-7555193344ee",
                            "style": "{}",
                            "width": 100,
                            "x": 1329.0,
                            "y": 250,
                            "_type": "org.uengine.modeling.model.Event"
                        },
                        "fieldDescriptors": [
                            {
                                "className": "Long",
                                "isCopy": False,
                                "isKey": True,
                                "name": "loanHistoryId",
                                "nameCamelCase": "loanHistoryId",
                                "namePascalCase": "LoanHistoryId",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Long",
                                "isCopy": False,
                                "isKey": False,
                                "name": "bookId",
                                "nameCamelCase": "bookId",
                                "namePascalCase": "BookId",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Member",
                                "isCopy": False,
                                "isKey": False,
                                "name": "member",
                                "nameCamelCase": "member",
                                "namePascalCase": "Member",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "LoanType",
                                "isCopy": False,
                                "isKey": False,
                                "name": "loanType",
                                "nameCamelCase": "loanType",
                                "namePascalCase": "LoanType",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Date",
                                "isCopy": False,
                                "isKey": False,
                                "name": "loanStartDate",
                                "nameCamelCase": "loanStartDate",
                                "namePascalCase": "LoanStartDate",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Date",
                                "isCopy": False,
                                "isKey": False,
                                "name": "loanDueDate",
                                "nameCamelCase": "loanDueDate",
                                "namePascalCase": "LoanDueDate",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Date",
                                "isCopy": False,
                                "isKey": False,
                                "name": "returnDate",
                                "nameCamelCase": "returnDate",
                                "namePascalCase": "ReturnDate",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Integer",
                                "isCopy": False,
                                "isKey": False,
                                "name": "overdueDays",
                                "nameCamelCase": "overdueDays",
                                "namePascalCase": "OverdueDays",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Date",
                                "isCopy": False,
                                "isKey": False,
                                "name": "createdAt",
                                "nameCamelCase": "createdAt",
                                "namePascalCase": "CreatedAt",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            }
                        ],
                        "hexagonalView": {
                            "height": 0,
                            "id": "8b664b48-2e29-48f8-8908-7555193344ee",
                            "style": "{}",
                            "width": 0,
                            "x": 0,
                            "y": 0,
                            "_type": "org.uengine.modeling.model.EventHexagonal"
                        },
                        "name": "LoanHistoryRecorded",
                        "displayName": "대출 이력이 기록됨",
                        "nameCamelCase": "loanHistoryRecorded",
                        "namePascalCase": "LoanHistoryRecorded",
                        "namePlural": "",
                        "relationCommandInfo": [],
                        "relationPolicyInfo": [],
                        "rotateStatus": False,
                        "selected": False,
                        "trigger": "@PostPersist",
                        "_type": "org.uengine.modeling.model.Event",
                        "aggregate": {
                            "id": "b352b64a-a49d-4704-b27f-e532280568d8"
                        },
                        "boundedContext": {
                            "id": "c517babe-52fb-48ba-8920-60df60b3da1e"
                        }
                    },
                    "from": "3b804b8b-3b73-46b6-b8d0-a8892db6c0f2",
                    "to": "8b664b48-2e29-48f8-8908-7555193344ee",
                    "relationView": {
                        "id": "30f53302-8bdc-4d09-a199-9a60d924486b",
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "from": "3b804b8b-3b73-46b6-b8d0-a8892db6c0f2",
                        "to": "8b664b48-2e29-48f8-8908-7555193344ee",
                        "needReconnect": True,
                        "value": "[]"
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.RelationHexagonal",
                        "from": "3b804b8b-3b73-46b6-b8d0-a8892db6c0f2",
                        "id": "30f53302-8bdc-4d09-a199-9a60d924486b",
                        "needReconnect": True,
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "to": "8b664b48-2e29-48f8-8908-7555193344ee",
                        "value": None
                    },
                    "sourceMultiplicity": "1",
                    "targetMultiplicity": "1"
                },
                "522b9ec0-f0a1-4680-93c8-4c3e9f1e4c09": {
                    "_type": "org.uengine.modeling.model.Relation",
                    "name": "",
                    "id": "522b9ec0-f0a1-4680-93c8-4c3e9f1e4c09",
                    "sourceElement": {
                        "_type": "org.uengine.modeling.model.Command",
                        "outputEvents": [
                            "BookStatusHistoryRecorded"
                        ],
                        "aggregate": {
                            "id": "4d3ad69a-26a0-4339-b557-dcd54213c61f"
                        },
                        "author": "My-UID",
                        "boundedContext": {
                            "id": "c517babe-52fb-48ba-8920-60df60b3da1e"
                        },
                        "controllerInfo": {
                            "apiPath": "recordbookstatushistory",
                            "method": "POST",
                            "fullApiPath": ""
                        },
                        "fieldDescriptors": [
                            {
                                "className": "Long",
                                "isCopy": False,
                                "isKey": False,
                                "name": "bookId",
                                "nameCamelCase": "bookId",
                                "namePascalCase": "BookId",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "BookStatus",
                                "isCopy": False,
                                "isKey": False,
                                "name": "previousStatus",
                                "nameCamelCase": "previousStatus",
                                "namePascalCase": "PreviousStatus",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "BookStatus",
                                "isCopy": False,
                                "isKey": False,
                                "name": "currentStatus",
                                "nameCamelCase": "currentStatus",
                                "namePascalCase": "CurrentStatus",
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
                        "description": None,
                        "id": "00dbfc77-0e4a-4dc9-b132-23d4b5f5767c",
                        "elementView": {
                            "_type": "org.uengine.modeling.model.Command",
                            "height": 115,
                            "id": "00dbfc77-0e4a-4dc9-b132-23d4b5f5767c",
                            "style": "{}",
                            "width": 100,
                            "x": 1571.0,
                            "y": 378,
                            "z-index": 999
                        },
                        "hexagonalView": {
                            "_type": "org.uengine.modeling.model.CommandHexagonal",
                            "height": 0,
                            "id": "00dbfc77-0e4a-4dc9-b132-23d4b5f5767c",
                            "style": "{}",
                            "width": 0,
                            "x": 0,
                            "y": 0
                        },
                        "isRestRepository": False,
                        "name": "RecordBookStatusHistory",
                        "displayName": "도서 상태 변경 이력 기록",
                        "nameCamelCase": "recordBookStatusHistory",
                        "namePascalCase": "RecordBookStatusHistory",
                        "namePlural": "recordBookStatusHistories",
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
                        "author": "My-UID",
                        "checkAlert": True,
                        "description": None,
                        "id": "ddefa445-30ae-4e41-8729-3b9ee661de39",
                        "elementView": {
                            "angle": 0,
                            "height": 115,
                            "id": "ddefa445-30ae-4e41-8729-3b9ee661de39",
                            "style": "{}",
                            "width": 100,
                            "x": 1759.0,
                            "y": 250,
                            "_type": "org.uengine.modeling.model.Event"
                        },
                        "fieldDescriptors": [
                            {
                                "className": "Long",
                                "isCopy": False,
                                "isKey": True,
                                "name": "statusHistoryId",
                                "nameCamelCase": "statusHistoryId",
                                "namePascalCase": "StatusHistoryId",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "Long",
                                "isCopy": False,
                                "isKey": False,
                                "name": "bookId",
                                "nameCamelCase": "bookId",
                                "namePascalCase": "BookId",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "BookStatus",
                                "isCopy": False,
                                "isKey": False,
                                "name": "previousStatus",
                                "nameCamelCase": "previousStatus",
                                "namePascalCase": "PreviousStatus",
                                "displayName": "",
                                "_type": "org.uengine.model.FieldDescriptor"
                            },
                            {
                                "className": "BookStatus",
                                "isCopy": False,
                                "isKey": False,
                                "name": "currentStatus",
                                "nameCamelCase": "currentStatus",
                                "namePascalCase": "CurrentStatus",
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
                            "id": "ddefa445-30ae-4e41-8729-3b9ee661de39",
                            "style": "{}",
                            "width": 0,
                            "x": 0,
                            "y": 0,
                            "_type": "org.uengine.modeling.model.EventHexagonal"
                        },
                        "name": "BookStatusHistoryRecorded",
                        "displayName": "도서 상태 변경 이력이 기록됨",
                        "nameCamelCase": "bookStatusHistoryRecorded",
                        "namePascalCase": "BookStatusHistoryRecorded",
                        "namePlural": "",
                        "relationCommandInfo": [],
                        "relationPolicyInfo": [],
                        "rotateStatus": False,
                        "selected": False,
                        "trigger": "@PostPersist",
                        "_type": "org.uengine.modeling.model.Event",
                        "aggregate": {
                            "id": "4d3ad69a-26a0-4339-b557-dcd54213c61f"
                        },
                        "boundedContext": {
                            "id": "c517babe-52fb-48ba-8920-60df60b3da1e"
                        }
                    },
                    "from": "00dbfc77-0e4a-4dc9-b132-23d4b5f5767c",
                    "to": "ddefa445-30ae-4e41-8729-3b9ee661de39",
                    "relationView": {
                        "id": "522b9ec0-f0a1-4680-93c8-4c3e9f1e4c09",
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "from": "00dbfc77-0e4a-4dc9-b132-23d4b5f5767c",
                        "to": "ddefa445-30ae-4e41-8729-3b9ee661de39",
                        "needReconnect": True,
                        "value": "[]"
                    },
                    "hexagonalView": {
                        "_type": "org.uengine.modeling.model.RelationHexagonal",
                        "from": "00dbfc77-0e4a-4dc9-b132-23d4b5f5767c",
                        "id": "522b9ec0-f0a1-4680-93c8-4c3e9f1e4c09",
                        "needReconnect": True,
                        "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                        "to": "ddefa445-30ae-4e41-8729-3b9ee661de39",
                        "value": None
                    },
                    "sourceMultiplicity": "1",
                    "targetMultiplicity": "1"
                }
            }
        )
    )
)

