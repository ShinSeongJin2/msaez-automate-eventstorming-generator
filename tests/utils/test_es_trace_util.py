from eventstorming_generator.utils import EsTraceUtil
from eventstorming_generator.models import ActionModel, State


class TestEsTraceUtil:
    """EsTraceUtil 클래스의 테스트"""
    
    def test_convert_refs_to_indexes_basic(self):
        """기본적인 refs 변환 테스트 (문자열 -> 인덱스)"""
        # Given: 원본 텍스트와 문자열 기반 refs를 가진 액션
        original_description = "사용자는 주문을 생성할 수 있다.\n주문에는 상품명과 수량이 포함된다.\n주문 후 재고가 감소한다."
        
        action = ActionModel(
            objectType="Event",
            args={
                "name": "OrderCreated",
                "refs": [
                    [[1, "주문을 생성"], [1, "생성할 수 있다"]]
                ]
            }
        )
        
        state = State()
        
        # When: refs 변환 수행
        EsTraceUtil.convert_refs_to_indexes([action], original_description, None, state)
        
        # Then: refs가 인덱스로 변환되어야 함
        refs = action.args["refs"]
        assert len(refs) == 1
        assert refs[0][0][0] == 1  # 시작 라인
        assert isinstance(refs[0][0][1], int)  # 시작 컬럼이 정수
        assert refs[0][1][0] == 1  # 끝 라인
        assert isinstance(refs[0][1][1], int)  # 끝 컬럼이 정수
    
    def test_convert_refs_to_indexes_with_properties(self):
        """properties의 refs 변환 테스트"""
        # Given: properties에 refs를 가진 Aggregate 액션
        original_description = "주문 집계에는 주문번호, 고객명, 총액이 있다.\n각 속성은 필수이다."
        
        action = ActionModel(
            objectType="Aggregate",
            args={
                "name": "Order",
                "properties": [
                    {
                        "name": "orderId",
                        "type": "String",
                        "refs": [[[1, "주문번호"], [1, "주문번호"]]]
                    },
                    {
                        "name": "customerName",
                        "type": "String",
                        "refs": [[[1, "고객명"], [1, "고객명"]]]
                    }
                ]
            }
        )
        
        state = State()
        
        # When: refs 변환 수행
        EsTraceUtil.convert_refs_to_indexes([action], original_description, None, state)
        
        # Then: 각 property의 refs가 변환되어야 함
        properties = action.args["properties"]
        for prop in properties:
            refs = prop["refs"]
            assert len(refs) > 0
            assert isinstance(refs[0][0][1], int)  # 시작 컬럼이 정수
            assert isinstance(refs[0][1][1], int)  # 끝 컬럼이 정수
    
    def test_convert_refs_to_indexes_with_query_parameters(self):
        """queryParameters의 refs 변환 테스트"""
        # Given: queryParameters에 refs를 가진 ReadModel 액션
        original_description = "주문 조회는 시작일자와 종료일자로 필터링한다."
        
        action = ActionModel(
            objectType="ReadModel",
            args={
                "name": "OrderList",
                "queryParameters": [
                    {
                        "name": "startDate",
                        "type": "Date",
                        "refs": [[[1, "시작일자"], [1, "시작일자"]]]
                    },
                    {
                        "name": "endDate",
                        "type": "Date",
                        "refs": [[[1, "종료일자"], [1, "종료일자"]]]
                    }
                ]
            }
        )
        
        state = State()
        
        # When: refs 변환 수행
        EsTraceUtil.convert_refs_to_indexes([action], original_description, None, state)
        
        # Then: 각 queryParameter의 refs가 변환되어야 함
        query_params = action.args["queryParameters"]
        for param in query_params:
            refs = param["refs"]
            assert len(refs) > 0
            assert isinstance(refs[0][0][1], int)
            assert isinstance(refs[0][1][1], int)
    
    def test_convert_refs_to_indexes_multiline(self):
        """여러 라인에 걸친 refs 변환 테스트"""
        # Given: 여러 라인에 걸친 refs
        original_description = "주문 생성 시\n다음 정보가 필요합니다:\n- 상품명\n- 수량\n- 가격"
        
        action = ActionModel(
            objectType="Command",
            args={
                "name": "CreateOrder",
                "refs": [
                    [[2, "다음 정보"], [4, "수량"]]
                ]
            }
        )
        
        state = State()
        
        # When: refs 변환 수행
        EsTraceUtil.convert_refs_to_indexes([action], original_description, None, state)
        
        # Then: 멀티라인 refs가 올바르게 변환되어야 함
        refs = action.args["refs"]
        assert len(refs) == 1
        assert refs[0][0][0] == 2  # 시작 라인
        assert refs[0][1][0] == 4  # 끝 라인
    
    def test_convert_refs_to_indexes_with_requirement_index_mapping(self):
        """requirement_index_mapping 적용 테스트"""
        # Given: requirement_index_mapping이 있는 경우
        original_description = "첫 번째 요구사항\n두 번째 요구사항\n세 번째 요구사항"
        
        action = ActionModel(
            objectType="Event",
            args={
                "name": "TestEvent",
                "refs": [
                    [[2, "두 번째"], [2, "요구사항"]]
                ]
            }
        )
        
        # 라인 2를 라인 5로 매핑
        requirement_index_mapping = {2: 5}
        state = State()
        
        # When: refs 변환 수행
        EsTraceUtil.convert_refs_to_indexes([action], original_description, requirement_index_mapping, state)
        
        # Then: 라인 번호가 매핑에 따라 변환되어야 함
        refs = action.args["refs"]
        assert refs[0][0][0] == 5  # 매핑된 라인 번호
        assert refs[0][1][0] == 5
    
    def test_convert_refs_to_indexes_already_converted(self):
        """이미 변환된 refs는 다시 변환하지 않음"""
        # Given: 이미 인덱스로 변환된 refs
        original_description = "테스트 요구사항입니다."
        
        action = ActionModel(
            objectType="Event",
            args={
                "name": "TestEvent",
                "refs": [
                    [[1, 1], [1, 10]]  # 이미 숫자로 변환됨
                ]
            }
        )
        
        state = State()
        original_refs = action.args["refs"][0].copy()
        
        # When: refs 변환 수행
        EsTraceUtil.convert_refs_to_indexes([action], original_description, None, state)
        
        # Then: refs가 변경되지 않아야 함 (이미 변환된 상태)
        refs = action.args["refs"]
        assert refs[0] == original_refs
    
    def test_convert_refs_to_indexes_empty_description(self):
        """빈 description 처리 테스트"""
        # Given: 빈 description
        original_description = ""
        
        action = ActionModel(
            objectType="Event",
            args={
                "name": "TestEvent",
                "refs": [
                    [[1, "테스트"], [1, "테스트"]]
                ]
            }
        )
        
        state = State()
        
        # When: refs 변환 수행
        EsTraceUtil.convert_refs_to_indexes([action], original_description, None, state)
        
        # Then: 경고 로그가 추가되어야 함
        assert len(state.outputs.logs) > 0
        assert "empty" in state.outputs.logs[0].message.lower()
    
    def test_convert_refs_to_indexes_multiple_actions(self):
        """여러 액션의 refs를 한번에 변환"""
        # Given: 여러 액션들
        original_description = "사용자는 상품을 주문할 수 있다.\n주문은 결제를 통해 완료된다."
        
        actions = [
            ActionModel(
                objectType="Event",
                args={
                    "name": "OrderPlaced",
                    "refs": [[[1, "상품을 주문"], [1, "주문할 수 있다"]]]
                }
            ),
            ActionModel(
                objectType="Event",
                args={
                    "name": "PaymentCompleted",
                    "refs": [[[2, "결제를 통해"], [2, "완료된다"]]]
                }
            )
        ]
        
        state = State()
        
        # When: 모든 액션의 refs 변환 수행
        EsTraceUtil.convert_refs_to_indexes(actions, original_description, None, state)
        
        # Then: 모든 액션의 refs가 변환되어야 함
        for action in actions:
            refs = action.args["refs"]
            assert len(refs) > 0
            assert isinstance(refs[0][0][1], int)
            assert isinstance(refs[0][1][1], int)
    
    def test_convert_refs_to_indexes_no_refs(self):
        """refs가 없는 액션 처리"""
        # Given: refs가 없는 액션
        original_description = "테스트 요구사항"
        
        action = ActionModel(
            objectType="Event",
            args={
                "name": "TestEvent"
                # refs 없음
            }
        )
        
        state = State()
        
        # When: refs 변환 수행
        EsTraceUtil.convert_refs_to_indexes([action], original_description, None, state)
        
        # Then: 에러 없이 처리되어야 함
        assert "refs" not in action.args or action.args.get("refs") is None
    
    def test_convert_refs_to_indexes_with_log_prefix(self):
        """log_prefix가 포함된 테스트"""
        # Given: 잘못된 refs와 log_prefix
        original_description = "테스트"
        
        action = ActionModel(
            objectType="Event",
            args={
                "name": "TestEvent",
                "refs": [
                    [[999, "존재하지 않는"], [999, "텍스트"]]
                ]
            }
        )
        
        state = State()
        log_prefix = "[TEST_PREFIX]"
        
        # When: refs 변환 수행
        EsTraceUtil.convert_refs_to_indexes([action], original_description, None, state, log_prefix)
        
        # Then: 로그에 prefix가 포함되어야 함
        if len(state.outputs.logs) > 0:
            assert any(log_prefix in log.message for log in state.outputs.logs)