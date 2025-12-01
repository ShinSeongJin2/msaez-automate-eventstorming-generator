create_aggregate_actions_by_function_inputs = {
    "targetBoundedContextName": "BookManagement",
    "description": "<1># Bounded Context Overview: BookManagement (도서 관리)</1>\n<2></2>\n<3>## Role</3>\n<4>도서 등록, 폐기, 상태 변경 등 도서의 라이프사이클을 관리하며, ISBN 중복 및 유효성 검증, 카테고리 관리, 도서 상태 전환(대출가능/대출중/예약중/폐기)을 담당한다.</4>\n<5></5>\n<6>## Key Events</6>\n<7>- BookRegistered</7>\n<8>- BookDiscarded</8>\n<9>- BookStatusChanged</9>\n<10></10>\n<11># Requirements</11>\n<12></12>\n<13>## userStory</13>\n<14></14>\n<15>도서관의 도서 관리와 대출/반납을 통합적으로 관리하는</15>\n<16></16>\n<17>'도서 관리' 화면에서는 새로운 도서를 등록하고 현재 보유한 도서들의 상태를 관리할 수 있어야 해. 도서 등록 시에는 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받아야 해. ISBN은 13자리 숫자여야 하고 중복 확인이 필요해. 카테고리는 소설/비소설/학술/잡지 중에서 선택할 수 있어야 해. 등록된 도서는 처음에 '대출가능' 상태가 되고, 이후 대출/반납 상황에 따라 '대출중', '예약중' 상태로 자동으로 변경되어야 해. 도서가 훼손되거나 분실된 경우 '폐기' 처리가 가능해야 하며, 폐기된 도서는 더 이상 대출이 불가능해야</17>\n<18></18>\n<19>각 도서별로 대출 이력과 상태 변경 이력을 조회할 수 있어야 하고, 이를 통해 도서의 대출 현황과 상태 변화를 추적할</19>\n<20></20>\n<21>## DDL</21>\n<22></22>\n<23>```sql</23>\n<24>도서 테이블</24>\n<25>CREATE TABLE books (</25>\n<26>    book_id INT AUTO_INCREMENT PRIMARY KEY,</26>\n<27>    title VARCHAR(500) NOT NULL,</27>\n<28>    isbn VARCHAR(13) UNIQUE NOT NULL,</28>\n<29>    author VARCHAR(200) NOT NULL,</29>\n<30>    publisher VARCHAR(200) NOT NULL,</30>\n<31>    category ENUM('소설', '비소설', '학술', '잡지') NOT NULL,</31>\n<32>    status ENUM('대출가능', '대출중', '예약중', '폐기') DEFAULT '대출가능',</32>\n<33>    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,</33>\n<34>    disposal_date DATETIME NULL,</34>\n<35>    disposal_reason TEXT NULL,</35>\n<36>    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,</36>\n<37>    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,</37>\n<38>    INDEX idx_title (title),</38>\n<39>    INDEX idx_isbn (isbn),</39>\n<40>    INDEX idx_status (status),</40>\n<41>    INDEX idx_category (category)</41>\n<42>);</42>\n<43>```</43>\n<44>```sql</44>\n<45>도서 상태 변경 이력 테이블</45>\n<46>CREATE TABLE book_status_history (</46>\n<47>    history_id INT AUTO_INCREMENT PRIMARY KEY,</47>\n<48>    book_id INT NOT NULL,</48>\n<49>    previous_status ENUM('대출가능', '대출중', '예약중', '폐기'),</49>\n<50>    new_status ENUM('대출가능', '대출중', '예약중', '폐기') NOT NULL,</50>\n<51>    change_reason VARCHAR(200),</51>\n<52>    changed_by VARCHAR(100),</52>\n<53>    change_date DATETIME DEFAULT CURRENT_TIMESTAMP,</53>\n<54>    FOREIGN KEY (book_id) REFERENCES books(book_id),</54>\n<55>    INDEX idx_book_id (book_id),</55>\n<56>    INDEX idx_change_date (change_date)</56>\n<57>);</57>\n<58>```</58>\n<59>## Event</59>\n<60></60>\n<61>```json</61>\n<62>{</62>\n<63>  \"name\": \"BookRegistered\",</63>\n<64>  \"displayName\": \"도서 등록됨\",</64>\n<65>  \"actor\": \"Librarian\",</65>\n<66>  \"level\": 1,</66>\n<67>  \"description\": \"사서가 새로운 도서를 도서 관리 화면에서 등록함. 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받고, ISBN 중복 및 유효성 검증을 통과한 후 도서가 등록됨. 등록된 도서는 '대출가능' 상태가 됨.\",</67>\n<68>  \"inputs\": [</68>\n<69>    \"도서명\",</69>\n<70>    \"ISBN(13자리)\",</70>\n<71>    \"저자\",</71>\n<72>    \"출판사\",</72>\n<73>    \"카테고리(소설/비소설/학술/잡지)\"</73>\n<74>  ],</74>\n<75>  \"outputs\": [</75>\n<76>    \"신규 도서(대출가능 상태)\"</76>\n<77>  ],</77>\n<78>  \"nextEvents\": [</78>\n<79>    \"BookStatusChanged\"</79>\n<80>  ]</80>\n<81>}</81>\n<82>```</82>\n<83></83>\n<84>```json</84>\n<85>{</85>\n<86>  \"name\": \"BookStatusChanged\",</86>\n<87>  \"displayName\": \"도서 상태 변경됨\",</87>\n<88>  \"actor\": \"System\",</88>\n<89>  \"level\": 2,</89>\n<90>  \"description\": \"도서가 등록, 대출, 반납, 예약, 폐기 등 주요 이벤트 발생 시 상태가 자동으로 변경됨. 예: 등록 시 '대출가능', 대출 시 '대출중', 반납 시 '대출가능' 또는 '예약중', 폐기 시 '폐기' 등.\",</90>\n<91>  \"inputs\": [</91>\n<92>    \"도서 이벤트(등록/대출/반납/예약/폐기 등)\"</92>\n<93>  ],</93>\n<94>  \"outputs\": [</94>\n<95>    \"도서 상태 변경\"</95>\n<96>  ],</96>\n<97>  \"nextEvents\": [</97>\n<98>    \"BookLoaned\",</98>\n<99>    \"BookReturned\",</99>\n<100>    \"BookReserved\",</100>\n<101>    \"BookDiscarded\"</101>\n<102>  ]</102>\n<103>}</103>\n<104>```</104>\n<105></105>\n<106>```json</106>\n<107>{</107>\n<108>  \"name\": \"BookDiscarded\",</108>\n<109>  \"displayName\": \"도서 폐기됨\",</109>\n<110>  \"actor\": \"Librarian\",</110>\n<111>  \"level\": 7,</111>\n<112>  \"description\": \"사서가 훼손되거나 분실된 도서를 폐기 처리함. 폐기된 도서는 더 이상 대출이 불가능함.\",</112>\n<113>  \"inputs\": [</113>\n<114>    \"도서명 또는 ISBN\",</114>\n<115>    \"폐기 사유\"</115>\n<116>  ],</116>\n<117>  \"outputs\": [</117>\n<118>    \"도서 상태 '폐기'\"</118>\n<119>  ],</119>\n<120>  \"nextEvents\": []</120>\n<121>}</121>\n<122>```</122>\n<123></123>\n<124>## Context Relations</124>\n<125></125>\n<126>### BookManagement→LoanProcessing</126>\n<127>- **Type**: Pub/Sub</127>\n<128>- **Direction**: sends to 대출/반납 처리 (LoanProcessing)</128>\n<129>- **Reason**: 도서의 상태(대출가능/대출중/예약중/폐기 등) 변경 이벤트가 대출/반납 프로세스와 연동되어야 하므로 이벤트 기반의 느슨한 결합이 적합하다.</129>\n<130>- **Interaction Pattern**: 도서 상태 변경 이벤트(BookStatusChanged 등)를 발행하면 대출/반납 처리 컨텍스트가 이를 구독하여 상태에 따라 대출 가능 여부를 판단한다.</130>\n<131></131>\n<132>### BookManagement→HistoryTracking</132>\n<133>- **Type**: Pub/Sub</133>\n<134>- **Direction**: sends to 이력 관리 (HistoryTracking)</134>\n<135>- **Reason**: 도서 등록, 폐기, 상태 변경 등 이벤트 발생 시 이력 관리 컨텍스트가 이벤트를 구독하여 상태 변경 이력을 기록한다.</135>\n<136>- **Interaction Pattern**: 도서 관리 컨텍스트에서 상태 변경 이벤트를 발행하면 이력 관리 컨텍스트가 이를 구독하여 상태 변경 이력을 기록한다.</136>",
    "targetAggregateStructure": {
        "aggregateAlias": "도서",
        "aggregateName": "Book",
        "enumerations": [
            {
                "alias": "도서 상태",
                "name": "BookStatus"
            }
        ],
        "valueObjects": [
            {
                "alias": "ISBN",
                "name": "ISBN",
                "referencedAggregate": None
            }
        ]
    },
    "attributesToGenerate": [
        "bookId",
        "title",
        "isbn",
        "author",
        "publisher",
        "category",
        "status",
        "registrationDate",
        "disposalDate",
        "disposalReason",
        "createdAt",
        "updatedAt",
        "historyId",
        "previousStatus",
        "newStatus",
        "changeReason",
        "changedBy",
        "changeDate"
    ]
}