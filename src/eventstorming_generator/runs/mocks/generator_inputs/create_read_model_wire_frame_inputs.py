create_read_model_wire_frame_inputs = {
    "viewName": "BookList",
    "viewDisplayName": "도서 목록 조회",
    "aggregateFields": [
        {
            "name": "bookId",
            "type": "Integer"
        },
        {
            "name": "title",
            "type": "String"
        },
        {
            "name": "isbn",
            "type": "String"
        },
        {
            "name": "author",
            "type": "String"
        },
        {
            "name": "publisher",
            "type": "String"
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
            "name": "disposalReason",
            "type": "String"
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
    "viewQueryParameters": [
        {
            "name": "category",
            "type": "BookCategory"
        },
        {
            "name": "status",
            "type": "BookStatus"
        },
        {
            "name": "title",
            "type": "String"
        }
    ],
    "additionalRequirements": "<request type=\"site_map_info\">\n<guide>This UI is included as part of the given sitemap. Please create the UI with these points in mind.</guide>\n<site_map_info>\n<bounded_context>BookManagement</bounded_context>\n<title>도서 목록 조회</title>\n<description>현재 보유 도서의 목록과 상태를 조회</description>\n</site_map_info>\n</request>\n<request type=\"user_requirements_for_site_map\">\n<guide>The following information details user requirements related to the provided Sitemap. Please proceed with UI generation, appropriately utilizing content related to the UI you intend to create.</guide>\n<user_requirements>도서명, ISBN, 저자, 출판사, 카테고리, 상태(대출가능/대출중/예약중/폐기) 필터 및 검색, 페이징 지원</user_requirements>\n</request>\n"
}