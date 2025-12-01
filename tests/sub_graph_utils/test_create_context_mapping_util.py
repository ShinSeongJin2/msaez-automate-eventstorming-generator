from eventstorming_generator.utils import CreateContextMappingUtil

class TestCreateContextMappingUtil:
    """CreateContextMappingUtil 클래스의 테스트"""
    
    def test_get_referenced_context_mappings_single_context_single_range(self):
        """단일 바운디드 컨텍스트, 단일 라인 범위 테스트"""
        # Given
        requirements = "Line 1\nLine 2\nLine 3\nLine 4\nLine 5"
        line_number_ranges = {
            "UserContext": [[2, 4]]
        }
        
        # When
        result = CreateContextMappingUtil.get_referenced_context_mappings(
            line_number_ranges, requirements
        )
        
        # Then
        assert len(result) == 1
        assert result[0].bounded_context_name == "UserContext"
        assert result[0].created_requirements == "Line 2\nLine 3\nLine 4"
        assert result[0].requirement_index_mapping == {1: 2, 2: 3, 3: 4}
    
    def test_get_referenced_context_mappings_single_context_multiple_ranges(self):
        """단일 바운디드 컨텍스트, 여러 라인 범위 테스트"""
        # Given
        requirements = "Line 1\nLine 2\nLine 3\nLine 4\nLine 5"
        line_number_ranges = {
            "OrderContext": [[1, 2], [4, 5]]
        }
        
        # When
        result = CreateContextMappingUtil.get_referenced_context_mappings(
            line_number_ranges, requirements
        )
        
        # Then
        assert len(result) == 1
        assert result[0].bounded_context_name == "OrderContext"
        assert result[0].created_requirements == "Line 1\nLine 2\nLine 4\nLine 5"
        assert result[0].requirement_index_mapping == {1: 1, 2: 2, 3: 4, 4: 5}
    
    def test_get_referenced_context_mappings_multiple_contexts(self):
        """여러 바운디드 컨텍스트 테스트"""
        # Given
        requirements = "Requirement A\nRequirement B\nRequirement C\nRequirement D"
        line_number_ranges = {
            "UserContext": [[1, 2]],
            "OrderContext": [[3, 4]]
        }
        
        # When
        result = CreateContextMappingUtil.get_referenced_context_mappings(
            line_number_ranges, requirements
        )
        
        # Then
        assert len(result) == 2
        
        # UserContext 검증
        user_context = next(r for r in result if r.bounded_context_name == "UserContext")
        assert user_context.created_requirements == "Requirement A\nRequirement B"
        assert user_context.requirement_index_mapping == {1: 1, 2: 2}
        
        # OrderContext 검증
        order_context = next(r for r in result if r.bounded_context_name == "OrderContext")
        assert order_context.created_requirements == "Requirement C\nRequirement D"
        assert order_context.requirement_index_mapping == {1: 3, 2: 4}
    
    def test_get_referenced_context_mappings_with_overlapping_ranges(self):
        """겹치는 라인 범위 테스트 (병합되어야 함)"""
        # Given
        requirements = "Line 1\nLine 2\nLine 3\nLine 4\nLine 5\nLine 6"
        line_number_ranges = {
            "ProductContext": [[1, 3], [2, 4], [5, 6]]
        }
        
        # When
        result = CreateContextMappingUtil.get_referenced_context_mappings(
            line_number_ranges, requirements
        )
        
        # Then
        assert len(result) == 1
        assert result[0].bounded_context_name == "ProductContext"
        # 범위 [1,3]과 [2,4]가 병합되어 [1,4], 그리고 [5,6]이 별도로 유지
        assert result[0].created_requirements == "Line 1\nLine 2\nLine 3\nLine 4\nLine 5\nLine 6"
        assert result[0].requirement_index_mapping == {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6}
    
    def test_get_referenced_context_mappings_with_adjacent_ranges(self):
        """인접한 라인 범위 테스트 (병합되어야 함)"""
        # Given
        requirements = "Line 1\nLine 2\nLine 3\nLine 4"
        line_number_ranges = {
            "PaymentContext": [[1, 2], [3, 4]]
        }
        
        # When
        result = CreateContextMappingUtil.get_referenced_context_mappings(
            line_number_ranges, requirements
        )
        
        # Then
        assert len(result) == 1
        assert result[0].bounded_context_name == "PaymentContext"
        # 인접한 범위가 병합되어 연속된 라인으로 추출
        assert result[0].created_requirements == "Line 1\nLine 2\nLine 3\nLine 4"
        assert result[0].requirement_index_mapping == {1: 1, 2: 2, 3: 3, 4: 4}
    
    def test_get_referenced_context_mappings_empty_ranges(self):
        """빈 라인 범위 테스트"""
        # Given
        requirements = "Line 1\nLine 2\nLine 3"
        line_number_ranges = {
            "EmptyContext": []
        }
        
        # When
        result = CreateContextMappingUtil.get_referenced_context_mappings(
            line_number_ranges, requirements
        )
        
        # Then
        assert len(result) == 1
        assert result[0].bounded_context_name == "EmptyContext"
        assert result[0].created_requirements == ""
        assert result[0].requirement_index_mapping == {}
    
    def test_get_referenced_context_mappings_out_of_bounds_range(self):
        """범위를 벗어난 라인 번호 테스트"""
        # Given
        requirements = "Line 1\nLine 2\nLine 3"
        line_number_ranges = {
            "ShippingContext": [[2, 5]]  # Line 4, 5는 존재하지 않음
        }
        
        # When
        result = CreateContextMappingUtil.get_referenced_context_mappings(
            line_number_ranges, requirements
        )
        
        # Then
        assert len(result) == 1
        assert result[0].bounded_context_name == "ShippingContext"
        # 존재하는 라인만 추출
        assert result[0].created_requirements == "Line 2\nLine 3"
        assert result[0].requirement_index_mapping == {1: 2, 2: 3}
    
    def test_get_referenced_context_mappings_single_line(self):
        """단일 라인만 참조하는 테스트"""
        # Given
        requirements = "First\nSecond\nThird"
        line_number_ranges = {
            "SingleLineContext": [[2, 2]]
        }
        
        # When
        result = CreateContextMappingUtil.get_referenced_context_mappings(
            line_number_ranges, requirements
        )
        
        # Then
        assert len(result) == 1
        assert result[0].bounded_context_name == "SingleLineContext"
        assert result[0].created_requirements == "Second"
        assert result[0].requirement_index_mapping == {1: 2}