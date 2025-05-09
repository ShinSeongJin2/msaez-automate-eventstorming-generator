import os
from eventstorming_generator.tests import test_commands

def run_test():
    """
    사용자로부터 테스트 문자열 또는 인덱스를 입력받아 해당 테스트를 실행합니다.
    """
    if not os.path.exists(".temp"):
        os.makedirs(".temp")


    print("실행 가능한 테스트 목록:")
    for idx, test_name in enumerate(test_commands.keys(), 1):
        print(f"{idx}. {test_name}")
    
    user_input = input("\n테스트 이름 또는 번호를 입력하세요: ")
    

    if user_input.isdigit():
        idx = int(user_input)
        if 1 <= idx <= len(test_commands):
            test_name = list(test_commands.keys())[idx-1]
            print(f"\n'{test_name}' 테스트를 실행합니다...\n")
            test_commands[test_name]()
        else:
            print(f"오류: {idx}번 테스트가 존재하지 않습니다.")
    else:
        if user_input in test_commands:
            print(f"\n'{user_input}' 테스트를 실행합니다...\n")
            test_commands[user_input]()
        else:
            print(f"오류: '{user_input}' 테스트가 존재하지 않습니다.")

if __name__ == "__main__":
    run_test()
