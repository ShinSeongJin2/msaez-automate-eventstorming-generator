merge_draft_generator_inputs = {
  "targetDrafts": {
    "EnrollmentManagement": {
      "aggregates": [
        {
          "aggregateName": "Enrollment",
          "aggregateAlias": "수강 신청",
          "enumerations": [
            {
              "name": "EnrollmentStatus",
              "alias": "수강 상태"
            }
          ],
          "valueObjects": [
            {
              "name": "EnrollmentDate",
              "alias": "수강 신청 날짜"
            },
            {
              "name": "Progress",
              "alias": "진행률"
            }
          ]
        }
      ]
    },
    "AssessmentManagement": {
      "aggregates": [
        {
          "aggregateName": "Assessment",
          "aggregateAlias": "평가",
          "enumerations": [
            {
              "name": "AssessmentType",
              "alias": "평가 유형"
            }
          ],
          "valueObjects": [
            {
              "name": "Score",
              "alias": "점수"
            },
            {
              "name": "Feedback",
              "alias": "피드백"
            }
          ]
        }
      ]
    }
  },
  "accumulatedDrafts": {
    "UserManagement": {
      "aggregates": [
        {
          "aggregateName": "User",
          "aggregateAlias": "사용자",
          "enumerations": [
            {
              "name": "UserRole",
              "alias": "사용자 역할"
            }
          ],
          "valueObjects": [
            {
              "name": "Profile",
              "alias": "프로필"
            },
            {
              "name": "Email",
              "alias": "이메일"
            }
          ],
          "IDValueObjects": []
        }
      ]
    },
    "CourseManagement": {
      "aggregates": [
        {
          "aggregateName": "Course",
          "aggregateAlias": "강좌",
          "enumerations": [
            {
              "name": "CourseLevel",
              "alias": "강좌 난이도"
            }
          ],
          "valueObjects": [
            {
              "name": "CourseContent",
              "alias": "강좌 내용"
            },
            {
              "name": "Duration",
              "alias": "수강 기간"
            }
          ],
          "IDValueObjects": []
        }
      ]
    }
  },
  "targetBoundedContextNames": ["EnrollmentManagement"]
}