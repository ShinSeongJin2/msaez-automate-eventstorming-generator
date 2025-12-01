from eventstorming_generator.utils import XmlUtil

class TestXmlUtil:
    """XmlUtil 클래스의 테스트"""
    
    def test_from_dict_simple_dict(self):
        """간단한 딕셔너리 변환 테스트"""
        data = {"name": "John", "age": 30}
        result = XmlUtil.from_dict(data)
        
        assert "<name>John</name>" in result
        assert "<age>30</age>" in result
    
    def test_from_dict_nested_dict(self):
        """중첩된 딕셔너리 변환 테스트"""
        data = {
            "user": {
                "name": "John",
                "email": "john@example.com"
            }
        }
        result = XmlUtil.from_dict(data)
        
        assert "<user>" in result
        assert "</user>" in result
        assert "<name>John</name>" in result
        assert "<email>john@example.com</email>" in result
    
    def test_from_dict_with_list(self):
        """리스트가 포함된 딕셔너리 변환 테스트"""
        data = {
            "users": ["Alice", "Bob", "Charlie"]
        }
        result = XmlUtil.from_dict(data)
        
        assert "<users>" in result
        assert "</users>" in result
        assert "<item>" in result
        assert "</item>" in result
        assert "Alice" in result
        assert "Bob" in result
        assert "Charlie" in result
    
    def test_from_dict_with_list_of_dicts(self):
        """딕셔너리 리스트 변환 테스트"""
        data = {
            "users": [
                {"name": "Alice", "age": 25},
                {"name": "Bob", "age": 30}
            ]
        }
        result = XmlUtil.from_dict(data)
        
        assert "<users>" in result
        assert "</users>" in result
        assert "<item>" in result
        assert "<name>Alice</name>" in result
        assert "<age>25</age>" in result
        assert "<name>Bob</name>" in result
        assert "<age>30</age>" in result
    
    def test_from_dict_with_escape_xml(self):
        """XML 특수문자 이스케이프 테스트"""
        data = {
            "content": "<script>alert('XSS')</script>",
            "quote": 'He said "Hello"'
        }
        result = XmlUtil.from_dict(data, is_use_escape_xml=True)
        
        assert "&lt;script&gt;" in result
        assert "&lt;/script&gt;" in result
        assert "&quot;Hello&quot;" in result
        assert "&#39;" in result
    
    def test_from_dict_without_escape_xml(self):
        """XML 이스케이프 미사용 테스트"""
        data = {
            "content": "<div>Hello</div>"
        }
        result = XmlUtil.from_dict(data, is_use_escape_xml=False)
        
        assert "<div>Hello</div>" in result
    
    def test_from_dict_with_snake_case_conversion(self):
        """snake_case 변환 테스트"""
        data = {
            "userName": "John",
            "userEmail": "john@example.com"
        }
        result = XmlUtil.from_dict(data, to_snake_case=True)
        
        assert "<user_name>John</user_name>" in result
        assert "<user_email>john@example.com</user_email>" in result
    
    def test_from_dict_with_none_value(self):
        """None 값 처리 테스트"""
        data = {
            "name": "John",
            "email": None
        }
        result = XmlUtil.from_dict(data)
        
        assert "<name>John</name>" in result
        assert "<email></email>" in result
    
    def test_from_dict_with_boolean_value(self):
        """Boolean 값 처리 테스트"""
        data = {
            "active": True,
            "deleted": False
        }
        result = XmlUtil.from_dict(data)
        
        assert "<active>True</active>" in result
        assert "<deleted>False</deleted>" in result
    
    def test_from_dict_with_empty_dict(self):
        """빈 딕셔너리 테스트"""
        data = {
            "empty": {}
        }
        result = XmlUtil.from_dict(data)
        
        assert "<empty>" in result
        assert "</empty>" in result
    
    def test_from_dict_with_empty_list(self):
        """빈 리스트 테스트"""
        data = {
            "items": []
        }
        result = XmlUtil.from_dict(data)
        
        assert "<items>" in result
        assert "</items>" in result
    
    def test_from_dict_complex_nested_structure(self):
        """복잡한 중첩 구조 테스트"""
        data = {
            "company": {
                "name": "Tech Corp",
                "departments": [
                    {
                        "name": "Engineering",
                        "employees": ["Alice", "Bob"]
                    },
                    {
                        "name": "Marketing",
                        "employees": ["Charlie"]
                    }
                ]
            }
        }
        result = XmlUtil.from_dict(data)
        
        assert "<company>" in result
        assert "</company>" in result
        assert "<name>Tech Corp</name>" in result
        assert "<departments>" in result
        assert "</departments>" in result
        assert "<item>" in result
        assert "<name>Engineering</name>" in result
        assert "<employees>" in result
        assert "Alice" in result
        assert "Bob" in result
        assert "Charlie" in result
    
    def test_from_dict_with_numeric_values(self):
        """숫자 값 처리 테스트"""
        data = {
            "integer": 42,
            "float": 3.14,
            "negative": -10
        }
        result = XmlUtil.from_dict(data)
        
        assert "<integer>42</integer>" in result
        assert "<float>3.14</float>" in result
        assert "<negative>-10</negative>" in result
    
    def test_from_dict_indentation(self):
        """들여쓰기 확인 테스트"""
        data = {
            "parent": {
                "child": "value"
            }
        }
        result = XmlUtil.from_dict(data)
        
        lines = result.split('\n')
        # 첫 번째 레벨은 2칸 들여쓰기
        assert lines[0].startswith("  <parent>")
        # 두 번째 레벨은 4칸 들여쓰기
        assert any(line.startswith("    <child>") for line in lines)