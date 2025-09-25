create_command_actions_by_function_inputs = {
    "summarizedESValue": {
        "deletedProperties": [],
        "boundedContexts": [
            {
                "id": "bc-bookManagement",
                "name": "BookManagement",
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
                                "name": "historyId",
                                "type": "Integer"
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
                                    "FICTION",
                                    "NON_FICTION",
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
            }
        ]
    },
    "description": "<1># Bounded Context Overview: BookManagement (도서 관리)</1>\n<2></2>\n<3>## Role</3>\n<4>도서 등록, 상태 관리, 폐기 처리를 담당하며 도서의 생애주기와 상태 변화를 관리한다.</4>\n<5></5>\n<6>## Key Events</6>\n<7>- BookRegistered</7>\n<8>- BookStatusChanged</8>\n<9>- BookDisposed</9>\n<10></10>\n<11># Requirements</11>\n<12></12>\n<13>## userStory</13>\n<14></14>\n<15>도서 관리' 화면에서는 새로운 도서를 등록하고 현재 보유한 도서들의 상태를 관리할 수 있어야 해. 도서 등록 시에는 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받아야 해. ISBN은 13자리 숫자여야 하고 중복 확인이 필요해. 카테고리는 소설/비소설/학술/잡지 중에서 선택할 수 있어야 해. 등록된 도서는 처음에 '대출가능' 상태가 되고, 이후 대출/반납 상황에 따라 '대출중', '예약중' 상태로 자동으로 변경되어야 해. 도서가 훼손되거나 분실된 경우 '폐기' 처리가 가능해야 하며, 폐기된 도서는 더 이상 대출이 불가능해야</15>\n<16></16>\n<17>도서별로 대출 이력과 상태 변경 이력을 조회할 수 있어야 하고, 이를 통해 도서의 대출 현황과 상태 변화를 추적할</17>\n<18></18>\n<19>## DDL</19>\n<20></20>\n<21>```sql</21>\n<22>도서 테이블</22>\n<23>CREATE TABLE books (</23>\n<24>    book_id INT AUTO_INCREMENT PRIMARY KEY,</24>\n<25>    title VARCHAR(500) NOT NULL,</25>\n<26>    isbn VARCHAR(13) UNIQUE NOT NULL,</26>\n<27>    author VARCHAR(200) NOT NULL,</27>\n<28>    publisher VARCHAR(200) NOT NULL,</28>\n<29>    category ENUM('소설', '비소설', '학술', '잡지') NOT NULL,</29>\n<30>    status ENUM('대출가능', '대출중', '예약중', '폐기') DEFAULT '대출가능',</30>\n<31>    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,</31>\n<32>    disposal_date DATETIME NULL,</32>\n<33>    disposal_reason TEXT NULL,</33>\n<34>    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,</34>\n<35>    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,</35>\n<36>    INDEX idx_title (title),</36>\n<37>    INDEX idx_isbn (isbn),</37>\n<38>    INDEX idx_status (status),</38>\n<39>    INDEX idx_category (category)</39>\n<40>);</40>\n<41>```</41>\n<42>```sql</42>\n<43>도서 상태 변경 이력 테이블</43>\n<44>CREATE TABLE book_status_history (</44>\n<45>    history_id INT AUTO_INCREMENT PRIMARY KEY,</45>\n<46>    book_id INT NOT NULL,</46>\n<47>    previous_status ENUM('대출가능', '대출중', '예약중', '폐기'),</47>\n<48>    new_status ENUM('대출가능', '대출중', '예약중', '폐기') NOT NULL,</48>\n<49>    change_reason VARCHAR(200),</49>\n<50>    changed_by VARCHAR(100),</50>\n<51>    change_date DATETIME DEFAULT CURRENT_TIMESTAMP,</51>\n<52>    FOREIGN KEY (book_id) REFERENCES books(book_id),</52>\n<53>    INDEX idx_book_id (book_id),</53>\n<54>    INDEX idx_change_date (change_date)</54>\n<55>);</55>\n<56>```</56>\n<57>## Event</57>\n<58></58>\n<59>```json</59>\n<60>{</60>\n<61>  \"name\": \"BookRegistered\",</61>\n<62>  \"displayName\": \"도서 등록됨\",</62>\n<63>  \"actor\": \"Librarian\",</63>\n<64>  \"level\": 1,</64>\n<65>  \"description\": \"사서가 새로운 도서를 등록하여 도서관 시스템에 추가하였음. 등록 시 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받고, ISBN 중복 및 유효성 검증이 완료됨.\",</65>\n<66>  \"inputs\": [</66>\n<67>    \"도서명\",</67>\n<68>    \"ISBN(13자리)\",</68>\n<69>    \"저자\",</69>\n<70>    \"출판사\",</70>\n<71>    \"카테고리(소설/비소설/학술/잡지)\"</71>\n<72>  ],</72>\n<73>  \"outputs\": [</73>\n<74>    \"신규 도서 정보\",</74>\n<75>    \"도서 상태: 대출가능\"</75>\n<76>  ],</76>\n<77>  \"nextEvents\": [</77>\n<78>    \"BookStatusChanged\"</78>\n<79>  ]</79>\n<80>}</80>\n<81>```</81>\n<82></82>\n<83>```json</83>\n<84>{</84>\n<85>  \"name\": \"BookStatusChanged\",</85>\n<86>  \"displayName\": \"도서 상태 변경됨\",</86>\n<87>  \"actor\": \"System\",</87>\n<88>  \"level\": 2,</88>\n<89>  \"description\": \"도서의 대출/반납/예약/폐기 등 상태 변화가 발생하여 도서 상태가 자동 또는 수동으로 변경됨.\",</89>\n<90>  \"inputs\": [</90>\n<91>    \"도서 상태 변경 트리거(대출, 반납, 예약, 폐기 등)\",</91>\n<92>    \"도서 식별자\"</92>\n<93>  ],</93>\n<94>  \"outputs\": [</94>\n<95>    \"변경된 도서 상태\"</95>\n<96>  ],</96>\n<97>  \"nextEvents\": [</97>\n<98>    \"BookDisposed\",</98>\n<99>    \"BookLoaned\",</99>\n<100>    \"BookReturned\",</100>\n<101>    \"BookReserved\"</101>\n<102>  ]</102>\n<103>}</103>\n<104>```</104>\n<105></105>\n<106>```json</106>\n<107>{</107>\n<108>  \"name\": \"BookDisposed\",</108>\n<109>  \"displayName\": \"도서 폐기됨\",</109>\n<110>  \"actor\": \"Librarian\",</110>\n<111>  \"level\": 3,</111>\n<112>  \"description\": \"도서가 훼손 또는 분실되어 사서에 의해 폐기 처리됨. 폐기된 도서는 더 이상 대출이 불가능함.\",</112>\n<113>  \"inputs\": [</113>\n<114>    \"도서 식별자\",</114>\n<115>    \"폐기 사유\"</115>\n<116>  ],</116>\n<117>  \"outputs\": [</117>\n<118>    \"도서 상태: 폐기\"</118>\n<119>  ],</119>\n<120>  \"nextEvents\": []</120>\n<121>}</121>\n<122>```</122>\n<123></123>\n<124>## Context Relations</124>\n<125></125>\n<126>### BookManagement-LoanAndReservation</126>\n<127>- **Type**: Pub/Sub</127>\n<128>- **Direction**: sends to 대출/반납 및 예약 (LoanAndReservation)</128>\n<129>- **Reason**: 도서 상태 변경(대출가능, 대출중, 예약중, 폐기 등)이 발생하면 대출/반납 및 예약 컨텍스트에서 이를 구독하여 대출/예약 프로세스에 반영한다.</129>\n<130>- **Interaction Pattern**: 도서 관리에서 도서 상태 변경 이벤트를 발행하면 대출/반납 및 예약 컨텍스트가 이를 구독하여 처리한다.</130>\n<131></131>\n<132>### BookManagement-LoanHistory</132>\n<133>- **Type**: Pub/Sub</133>\n<134>- **Direction**: sends to 이력 관리 (LoanHistory)</134>\n<135>- **Reason**: 도서 등록, 폐기 등 도서 상태 변화 이력도 이력 관리 컨텍스트에서 기록할 수 있도록 이벤트를 발행한다.</135>\n<136>- **Interaction Pattern**: 도서 관리에서 도서 등록, 폐기 등 상태 변화 이벤트를 발행하면 이력 관리 컨텍스트가 이를 구독하여 상태 변경 이력을 기록한다.</136>",
    "targetBoundedContextName": "BookManagement",
    "targetAggregateName": "Book",
    "eventNamesToGenerate": [
        "BookRegistered",
        "BookEdited",
        "BookStatusChanged",
        "BookDisposed"
    ],
    "commandNamesToGenerate": [
        "CreateBook",
        "EditBook",
        "UpdateBookStatus",
        "DisposeBook"
    ],
    "readModelNamesToGenerate": [
        "BookList",
        "BookStatusChangeHistory"
    ]
}