assign_command_view_names_to_aggregate_draft_generator_inputs = {
    "aggregateDrafts": [
        {
            "name": "Loan",
            "alias": "대출"
        },
        {
            "name": "Reservation",
            "alias": "예약"
        }
    ],
    "siteMap": [
        {
            "boundedContext":"LoanProcess",
            "description":"도서 대출, 반납, 예약 및 연장 처리",
            "id":"loan-process",
            "title":"대출/반납"
        },
        {
            "boundedContext":"LoanProcess",
            "description":"회원 인증 및 도서 대출 신청",
            "id":"loan-application",
            "title":"대출 신청"
        },
        {
            "boundedContext":"LoanProcess",
            "description":"도서 반납 및 상태 변경",
            "id":"return-process",
            "title":"반납 처리"
        }
    ]
}