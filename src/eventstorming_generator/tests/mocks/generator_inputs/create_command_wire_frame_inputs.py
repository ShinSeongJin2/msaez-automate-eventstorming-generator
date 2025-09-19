create_command_wire_frame_inputs = {
    "commandName": "CreateBook",
    "commandDisplayName": "도서 등록",
    "fields": [
        {
            "name": "title",
            "type": "String",
            "required": False
        },
        {
            "name": "isbn",
            "type": "String",
            "required": False
        },
        {
            "name": "author",
            "type": "String",
            "required": False
        },
        {
            "name": "publisher",
            "type": "String",
            "required": False
        },
        {
            "name": "category",
            "type": "BookCategory",
            "required": False
        }
    ],
    "api": "POST createbook",
    "additionalRequirements": "<request type=\"site_map_info\">\n<guide>This UI is included as part of the given sitemap. Please create the UI with these points in mind.</guide>\n<site_map_info>\n<bounded_context>BookManagement</bounded_context>\n<title>도서 등록</title>\n<description>새로운 도서를 등록</description>\n</site_map_info>\n</request>\n<request type=\"user_requirements_for_site_map\">\n<guide>The following information details user requirements related to the provided Sitemap. Please proceed with UI generation, appropriately utilizing content related to the UI you intend to create.</guide>\n<user_requirements>도서명, ISBN(13자리, 중복확인), 저자, 출판사, 카테고리(소설/비소설/학술/잡지) 입력 폼, 등록 시 상태는 '대출가능'으로 설정</user_requirements>\n</request>"
}