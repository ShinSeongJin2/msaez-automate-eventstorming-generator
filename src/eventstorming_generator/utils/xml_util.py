from .convert_case_util import CaseConvertUtil  

class XmlUtil:
    @staticmethod
    def from_dict(data: dict, is_use_escape_xml: bool = False, to_snake_case: bool = False) -> str:
        """
        딕셔너리를 XML 형식의 텍스트로 변환합니다.
        
        Args:
            data (dict): 변환할 딕셔너리 데이터
            is_use_escape_xml (bool): XML 특수문자 이스케이프 여부
            to_snake_case (bool): 키를 snake_case로 변환 여부
        Returns:
            str: XML 형식의 문자열
        """
        def _convert_value_to_xml(value, indent_level=1):
            """값을 XML 형식으로 변환하는 내부 함수"""
            indent = "  " * indent_level
            
            if isinstance(value, dict):
                # 딕셔너리인 경우 각 키-값 쌍을 태그로 변환
                result = []
                for key, val in value.items():
                    if to_snake_case:
                        key = CaseConvertUtil.snake_case(key)
                    
                    if isinstance(val, (list, dict)):
                        # 리스트나 딕셔너리인 경우 재귀적으로 처리
                        result.append(f"{indent}<{key}>")
                        result.append(_convert_value_to_xml(val, indent_level + 1))
                        result.append(f"{indent}</{key}>")
                    else:
                        # 일반 값인 경우
                        result.append(f"{indent}<{key}>{_escape_xml(val)}</{key}>")
                return "\n".join(result)
            
            elif isinstance(value, list):
                # 리스트인 경우 각 항목을 <item> 태그로 감쌈
                result = []
                for item in value:
                    result.append(f"{indent}<item>")
                    if isinstance(item, dict):
                        # 딕셔너리 항목인 경우 재귀적으로 처리
                        nested_result = _convert_value_to_xml(item, indent_level + 1)
                        # 인덴트 레벨을 조정해서 추가
                        nested_lines = nested_result.split('\n')
                        for line in nested_lines:
                            if line.strip():  # 빈 줄이 아닌 경우만
                                result.append(f"  {line}")
                        result.append(f"{indent}</item>")
                    elif isinstance(item, list):
                        # 리스트 항목인 경우 재귀적으로 처리
                        nested_result = _convert_value_to_xml(item, indent_level + 1)
                        nested_lines = nested_result.split('\n')
                        for line in nested_lines:
                            if line.strip():  # 빈 줄이 아닌 경우만
                                result.append(f"  {line}")
                        result.append(f"{indent}</item>")
                    else:
                        # 일반 값인 경우
                        result.append(f"{indent}  {_escape_xml(item)}")
                        result.append(f"{indent}</item>")
                return "\n".join(result)
            
            else:
                # 일반 값인 경우
                return f"{indent}{_escape_xml(value)}"
        
        def _escape_xml(value):
            """XML에서 특수문자를 이스케이프 처리"""
            if value is None:
                return ""
            
            # Boolean 값을 문자열로 변환
            if isinstance(value, bool):
                return str(value)
            
            # 문자열인 경우 XML 특수문자 이스케이프
            if isinstance(value, str):
                if is_use_escape_xml:
                    return (value.replace("&", "&amp;")
                            .replace("<", "&lt;")
                            .replace(">", "&gt;")
                            .replace('"', "&quot;")
                            .replace("'", "&#39;"))
                else:
                    return value
            
            return str(value)
        
        return _convert_value_to_xml(data)
  