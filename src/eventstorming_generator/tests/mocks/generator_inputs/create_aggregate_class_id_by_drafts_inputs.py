create_aggregate_class_id_by_drafts_inputs = {
    "summarizedESValue": {
        "deletedProperties": [
            "aggregate.commands",
            "aggregate.events",
            "aggregate.readModels",
            "aggregate.entities",
            "aggregate.enumerations",
            "aggregate.valueObjects"
        ],
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
                        "policies": []
                    }
                ]
            },
            {
                "id": "bc-loanAndReservation",
                "name": "LoanAndReservation",
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
                                "type": "Integer"
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
                            }
                        ],
                        "policies": []
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
                        "policies": []
                    }
                ]
            }
        ]
    },
    "draftOption": {
        "BookManagement": [
            {
                "aggregate": {
                    "alias": "도서",
                    "name": "Book"
                },
                "valueObjects": [
                    {
                        "alias": "대출 참조",
                        "name": "LoanReference",
                        "referencedAggregate": {
                            "alias": "대출",
                            "name": "Loan"
                        }
                    }
                ]
            }
        ],
        "LoanAndReservation": [
            {
                "aggregate": {
                    "alias": "대출",
                    "name": "Loan"
                },
                "valueObjects": [
                    {
                        "alias": "도서 참조",
                        "name": "BookReference",
                        "referencedAggregate": {
                            "alias": "도서",
                            "name": "Book"
                        }
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
                    }
                ]
            }
        ]
    },
    "targetReferences": [
        "LoanReference",
        "BookReference"
    ]
}