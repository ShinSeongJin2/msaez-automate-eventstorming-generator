import json

class JsonUtil:
    @staticmethod
    def convert_to_json(data: any, indent: int = 4) -> str:
        # 데이터 변환 함수
        def convert_data(item):
            if hasattr(item, 'model_dump_json'):
                return json.loads(item.model_dump_json())
            elif isinstance(item, dict):
                return item
            else:
                return str(item)
        
        # 리스트인 경우 각 항목을 개별적으로 처리
        if isinstance(data, list):
            processed_data = [convert_data(item) for item in data]
            json_data = json.dumps(processed_data, indent=indent, ensure_ascii=False)
        # Pydantic BaseModel인 경우
        elif hasattr(data, 'model_dump_json'):
            json_data = data.model_dump_json(indent=indent)
        # 딕셔너리인 경우
        elif isinstance(data, dict):
            json_data = json.dumps(data, indent=indent, ensure_ascii=False)
        # 그 외의 경우
        else:
            json_data = str(data)

        return json_data

    @staticmethod
    def convert_to_dict(json_str: str) -> dict:
        return json.loads(json_str)

