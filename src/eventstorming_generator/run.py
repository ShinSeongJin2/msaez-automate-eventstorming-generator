

import os

from eventstorming_generator.runs import runable_logics_categories
from eventstorming_generator.types import RunableLogicsCategories, RunableLogics

def run():
    """
    특정한 Mock 데이터를 활용해서 일부 로직을 부분적으로 실행
    """
    try:
        if not os.path.exists(".temp"):
            os.makedirs(".temp")

        selected_category = _select_category(runable_logics_categories)
        selected_function = _select_function(runable_logics_categories[selected_category], selected_category)
        
        print(f"\n'{selected_category}' > '{selected_function}' 로직을 실행합니다...\n")
        runable_logics_categories[selected_category][selected_function]()
    
    except Exception as e:
        print(f"로직 실행 중 오류 발생: {e}")

def _select_category(runable_logics_categories: RunableLogicsCategories) -> str:
    """
    1차 선택: 카테고리 선택
    """
    print("### 카테고리 선택 ###")
    categories = list(runable_logics_categories.keys())
    
    for idx, category in enumerate(categories, 1):
        print(f"{idx}. {category}")
    
    while True:
        user_input = input("> 카테고리 이름 또는 번호를 입력하세요: ")
        
        if user_input.isdigit():
            idx = int(user_input)
            if 1 <= idx <= len(categories):
                return categories[idx-1]
            else:
                print(f"오류: {idx}번 카테고리가 존재하지 않습니다. 다시 입력해주세요.")
        else:
            if user_input in categories:
                return user_input
            else:
                print(f"오류: '{user_input}' 카테고리가 존재하지 않습니다. 다시 입력해주세요.")

def _select_function(runable_logics: RunableLogics, category_name: str) -> str:
    """
    2차 선택: 구체적인 함수 선택
    """
    print(f"\n### '{category_name}' 카테고리 내 함수 선택 ###")
    function_names = list(runable_logics.keys())
    
    for idx, func_name in enumerate(function_names, 1):
        print(f"{idx}. {func_name}")
    
    while True:
        user_input = input("> 함수 이름 또는 번호를 입력하세요: ")
        
        if user_input.isdigit():
            idx = int(user_input)
            if 1 <= idx <= len(function_names):
                return function_names[idx-1]
            else:
                print(f"오류: {idx}번 함수가 존재하지 않습니다. 다시 입력해주세요.")
        else:
            if user_input in function_names:
                return user_input
            else:
                print(f"오류: '{user_input}' 함수가 존재하지 않습니다. 다시 입력해주세요.")

if __name__ == "__main__":
    run()