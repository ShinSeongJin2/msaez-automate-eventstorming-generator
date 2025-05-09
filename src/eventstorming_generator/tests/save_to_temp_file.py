from datetime import datetime
from typing import Any

def save_to_temp_file(data: Any, file_name: str) -> None:
    print(data.model_dump_json(indent=4))
    
    FILE_PATH = f".temp/{file_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(FILE_PATH, "w") as f:
        f.write(data.model_dump_json(indent=4))
    print(f"{FILE_PATH} 파일에 생성 결과 저장 완료")