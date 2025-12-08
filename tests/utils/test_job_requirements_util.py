import pytest
from eventstorming_generator.utils.job_utils import JobRequirementsUtil


class TestJobRequirementsUtil:
    """JobRequirementsUtil.parse_requirements 테스트"""
    
    def test_simple_key_value(self):
        """단순 키-값 객체 변환 테스트"""
        requirements = '[INPUT_DATA]\n{"message": "Hello!\\nWorld!"}'
        
        result = JobRequirementsUtil.parse_requirements(requirements)
        
        assert "[INPUT_DATA]" in result
        assert "# message" in result
        assert "Hello!\nWorld!" in result
        assert "{" not in result
        assert "}" not in result
    
    def test_nested_object(self):
        """중첩 객체 변환 테스트 (헤더 레벨 증가)"""
        requirements = '''{
    "user": {
        "name": "John",
        "profile": {
            "age": 30
        }
    }
}'''
        
        result = JobRequirementsUtil.parse_requirements(requirements)
        
        assert "# user" in result
        assert "## name" in result
        assert "John" in result
        assert "## profile" in result
        assert "### age" in result
        assert "30" in result
    
    def test_list_items(self):
        """리스트 항목 변환 테스트"""
        requirements = '''{
    "items": ["apple", "banana", "cherry"]
}'''
        
        result = JobRequirementsUtil.parse_requirements(requirements)
        
        assert "# items" in result
        assert "- apple" in result
        assert "- banana" in result
        assert "- cherry" in result
    
    def test_complex_nested_structure(self):
        """복합 중첩 구조 변환 테스트"""
        requirements = '''{
    "project": {
        "name": "MyProject",
        "members": ["Alice", "Bob"],
        "config": {
            "debug": true,
            "version": 1.0
        }
    }
}'''
        
        result = JobRequirementsUtil.parse_requirements(requirements)
        
        assert "# project" in result
        assert "## name" in result
        assert "MyProject" in result
        assert "## members" in result
        assert "- Alice" in result
        assert "- Bob" in result
        assert "## config" in result
        assert "### debug" in result
        assert "true" in result
        assert "### version" in result
        assert "1.0" in result
    
    def test_invalid_json_returns_original(self):
        """JSON 파싱 실패 시 원본 반환 테스트"""
        requirements = '''{
    "invalid": json without quotes
}'''
        
        result = JobRequirementsUtil.parse_requirements(requirements)
        
        # 유효하지 않은 JSON은 변환하지 않고 원본 유지
        assert "invalid" in result
    
    def test_no_json_returns_original(self):
        """JSON이 없는 문자열 원본 반환 테스트"""
        requirements = "This is plain text without any JSON"
        
        result = JobRequirementsUtil.parse_requirements(requirements)
        
        assert result == requirements
    
    def test_multiple_json_blocks(self):
        """여러 JSON 블록이 있는 경우 모두 변환"""
        requirements = '''First block:
{"name": "First"}
Second block:
{"name": "Second"}'''
        
        result = JobRequirementsUtil.parse_requirements(requirements)
        
        assert "First block:" in result
        assert "# name" in result
        assert "First" in result
        assert "Second block:" in result
        assert "Second" in result
    
    def test_list_of_objects(self):
        """객체 리스트 변환 테스트"""
        requirements = '''{
    "users": [
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 30}
    ]
}'''
        
        result = JobRequirementsUtil.parse_requirements(requirements)
        
        assert "# users" in result
        assert "## name" in result
        assert "Alice" in result
        assert "## age" in result
        assert "25" in result
        assert "Bob" in result
        assert "30" in result
    
    def test_null_value(self):
        """null 값 처리 테스트"""
        requirements = '{"value": null}'
        
        result = JobRequirementsUtil.parse_requirements(requirements)
        
        assert "# value" in result
    
    def test_boolean_values(self):
        """boolean 값 처리 테스트"""
        requirements = '{"enabled": true, "disabled": false}'
        
        result = JobRequirementsUtil.parse_requirements(requirements)
        
        assert "# enabled" in result
        assert "true" in result
        assert "# disabled" in result
        assert "false" in result
    
    def test_numeric_values(self):
        """숫자 값 처리 테스트"""
        requirements = '{"count": 42, "price": 19.99}'
        
        result = JobRequirementsUtil.parse_requirements(requirements)
        
        assert "# count" in result
        assert "42" in result
        assert "# price" in result
        assert "19.99" in result
    
    def test_empty_object(self):
        """빈 객체 처리 테스트"""
        requirements = '{"data": {}}'
        
        result = JobRequirementsUtil.parse_requirements(requirements)
        
        assert "# data" in result
    
    def test_empty_list(self):
        """빈 리스트 처리 테스트"""
        requirements = '{"items": []}'
        
        result = JobRequirementsUtil.parse_requirements(requirements)
        
        assert "# items" in result
    
    def test_preserves_surrounding_text(self):
        """JSON 블록 주변 텍스트 보존 테스트"""
        requirements = '''Before the JSON
{"key": "value"}
After the JSON'''
        
        result = JobRequirementsUtil.parse_requirements(requirements)
        
        assert "Before the JSON" in result
        assert "After the JSON" in result
        assert "# key" in result
        assert "value" in result
