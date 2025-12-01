from .....models import *

merge_draft_generator_util_inputs = [
    BoundedContextStructureModel(
        boundedContextName="PatientManagement",
        boundedContextAlias="환자 관리",
        aggregates=[
            AggregateInfoModel(
                aggregateName="Patient",
                aggregateAlias="환자",
                enumerations=[
                    EnumerationInfoModel(name="Gender", alias="성별"),
                    EnumerationInfoModel(name="BloodType", alias="혈액형")
                ],
                valueObjects=[
                    ValueObjectInfoModel(name="PersonalInfo", alias="개인 정보"),
                    ValueObjectInfoModel(name="ContactInfo", alias="연락처 정보"),
                    ValueObjectInfoModel(name="EmergencyContact", alias="긴급 연락처"),
                    ValueObjectInfoModel(name="InsuranceInfo", alias="보험 정보")
                ]
            )
        ]
    ),
    BoundedContextStructureModel(
        boundedContextName="AppointmentManagement",
        boundedContextAlias="예약 관리",
        aggregates=[
            AggregateInfoModel(
                aggregateName="Appointment",
                aggregateAlias="예약",
                enumerations=[
                    EnumerationInfoModel(name="AppointmentStatus", alias="예약 상태"),
                    EnumerationInfoModel(name="AppointmentType", alias="예약 유형")
                ],
                valueObjects=[
                    ValueObjectInfoModel(name="TimeSlot", alias="시간대"),
                    ValueObjectInfoModel(name="AppointmentDetails", alias="예약 세부사항")
                ]
            )
        ]
    ),
    BoundedContextStructureModel(
        boundedContextName="MedicalRecordManagement",
        boundedContextAlias="진료 기록 관리",
        aggregates=[
            AggregateInfoModel(
                aggregateName="MedicalRecord",
                aggregateAlias="진료 기록",
                enumerations=[
                    EnumerationInfoModel(name="RecordType", alias="기록 유형"),
                    EnumerationInfoModel(name="Severity", alias="중증도")
                ],
                valueObjects=[
                    ValueObjectInfoModel(name="Diagnosis", alias="진단"),
                    ValueObjectInfoModel(name="Treatment", alias="치료"),
                    ValueObjectInfoModel(name="VitalSigns", alias="활력 징후"),
                    ValueObjectInfoModel(name="Prescription", alias="처방전")
                ]
            )
        ]
    ),
    BoundedContextStructureModel(
        boundedContextName="BillingManagement",
        boundedContextAlias="청구 관리",
        aggregates=[
            AggregateInfoModel(
                aggregateName="Bill",
                aggregateAlias="청구서",
                enumerations=[
                    EnumerationInfoModel(name="BillStatus", alias="청구 상태"),
                    EnumerationInfoModel(name="PaymentMethod", alias="결제 방법")
                ],
                valueObjects=[
                    ValueObjectInfoModel(name="BillingItem", alias="청구 항목"),
                    ValueObjectInfoModel(name="PaymentInfo", alias="결제 정보"),
                    ValueObjectInfoModel(name="InsuranceClaim", alias="보험 청구")
                ]
            )
        ]
    ),
    BoundedContextStructureModel(
        boundedContextName="PharmacyManagement",
        boundedContextAlias="약국 관리",
        aggregates=[
            AggregateInfoModel(
                aggregateName="Medication",
                aggregateAlias="의약품",
                enumerations=[
                    EnumerationInfoModel(name="MedicationType", alias="의약품 유형"),
                    EnumerationInfoModel(name="DosageForm", alias="제형")
                ],
                valueObjects=[
                    ValueObjectInfoModel(name="MedicationInfo", alias="의약품 정보"),
                    ValueObjectInfoModel(name="Dosage", alias="용량"),
                    ValueObjectInfoModel(name="SideEffects", alias="부작용")
                ]
            ),
            AggregateInfoModel(
                aggregateName="PrescriptionOrder",
                aggregateAlias="처방 주문",
                enumerations=[
                    EnumerationInfoModel(name="OrderStatus", alias="주문 상태")
                ],
                valueObjects=[
                    ValueObjectInfoModel(name="OrderItem", alias="주문 항목"),
                    ValueObjectInfoModel(name="DispenseInfo", alias="조제 정보")
                ]
            )
        ]
    ),
    BoundedContextStructureModel(
        boundedContextName="DoctorManagement",
        boundedContextAlias="의사 관리",
        aggregates=[
            AggregateInfoModel(
                aggregateName="Doctor",
                aggregateAlias="의사",
                enumerations=[
                    EnumerationInfoModel(name="Specialty", alias="전문 분야"),
                    EnumerationInfoModel(name="EmploymentStatus", alias="고용 상태")
                ],
                valueObjects=[
                    ValueObjectInfoModel(name="DoctorProfile", alias="의사 프로필"),
                    ValueObjectInfoModel(name="Qualification", alias="자격증"),
                    ValueObjectInfoModel(name="Schedule", alias="근무 일정")
                ]
            )
        ]
    )
]