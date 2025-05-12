from typing import Dict, List, Any, Optional, Union
from abc import ABC, abstractmethod
from langchain.chat_models import init_chat_model
from langchain.schema import HumanMessage, SystemMessage, AIMessage, BaseMessage
from langchain_community.cache import SQLiteCache
from langchain_core.globals import set_llm_cache
import os


def init_cache():
    if not os.path.exists(".cache"):
        os.makedirs(".cache")

    set_llm_cache(SQLiteCache(database_path=".cache/llm_cache.db"))

init_cache()


class BaseGenerator(ABC):
    """
    프롬프트 구성 및 LLM 호출을 위한 기본 생성기 클래스
    
    이 클래스는 구조화된 프롬프트 생성 및 LangChain 모델과의 통합을 위한 인터페이스를 제공합니다.
    상속받는 클래스는 프롬프트 구성 요소들을 구현하고, 이 베이스 클래스는 이를 조합하여 
    일관된 프롬프트 형식을 제공합니다.
    """
    
    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        """
        BaseGenerator 초기화
        
        Args:
            model_name: 모델 이름
            model_kwargs: 모델 파라미터
            client: 클라이언트
        """
        if model_kwargs is None: model_kwargs = {}
        if model_kwargs.get("temperature") is None: model_kwargs["temperature"] = 0.2

        if client is None: client = {}
        if not client.get("inputs"): client["inputs"] = {}
        if not client.get("preferredLanguage"): client["preferredLanguage"] = "English"
        if not client.get("disableLanguageGuide"): client["disableLanguageGuide"] = False

        self.set_model(model_name, model_kwargs)
        self.client = client

    def assemble_prompt(self) -> Dict[str, Union[str, List[str]]]:
        """
        시스템, 유저, 어시스턴트 프롬프트를 조합하여 완전한 프롬프트 구조 반환
        
        Returns:
            Dict: 각 역할별 프롬프트가 포함된 딕셔너리
        """
        return {
            "system": self._build_system_prompt(),
            "user": self._build_user_prompt(),
            "assistant": self._build_assistant_prompt()
        }
    
    def _build_system_prompt(self) -> str:
        """시스템 프롬프트 빌드"""
        return self._build_agent_role_prompt()
    
    def _build_user_prompt(self) -> List[str]:
        """유저 프롬프트 빌드"""
        prompts = []
        
        guidelines = [
            self._build_task_guidelines_prompt(),
            self._build_inference_guidelines_prompt(),
            self._build_request_format_prompt(),
            self._build_response_format_prompt()
        ]
        
        # 빈 문자열 필터링
        guidelines = [p for p in guidelines if p]
        
        example_inputs = self._build_json_example_input_format()
        user_inputs = self._build_json_user_query_input_format()
        
        if example_inputs and user_inputs:
            prompts.append("\n\n".join(guidelines) + "\n\nThis is the entire guideline.\nWhen you're ready, please output 'Approved.' Then I will begin user input.")
            prompts.append(self._inputs_to_string(example_inputs))
            prompts.append(self._inputs_to_string(user_inputs))
        elif user_inputs:
            prompts.append("\n\n".join(guidelines) + "\n\nThis is the entire guideline.\nWhen you're ready, please output 'Approved.' Then I will begin user input.")
            prompts.append(self._inputs_to_string(user_inputs))
        
        return prompts
    
    def _build_assistant_prompt(self) -> List[str]:
        """어시스턴트 프롬프트 빌드"""
        example_outputs = self._build_json_example_output_format()
        if not example_outputs:
            return []
        
        import json
        return ["Approved.", f"```json\n{json.dumps(example_outputs, indent=2)}\n```"]
    
    def _inputs_to_string(self, inputs: Dict[str, Any]) -> str:
        """입력 파라미터를 문자열로 변환"""
        import json
        result = []
        
        for key, value in inputs.items():
            formatted_value = value if isinstance(value, str) else json.dumps(value)
            result.append(f"- {key.strip()}\n{formatted_value.strip()}")
            
        return "\n\n".join(result)
    
    def _build_response_format_prompt(self) -> str:
        """응답 형식 프롬프트 빌드"""
        json_format = self._build_json_response_format()
        after_json_format = self._build_after_json_response_format()
        
        if not json_format:
            return ""
            
        return f"""You should return a list containing pretty-printed JSON objects for performing specific actions.
The returned format should be as follows.
```json
{json_format.strip()}
```

{after_json_format.strip()}
"""
    
    def generate(self) -> Any:
        """
        LLM을 사용하여 생성 실행
        
        Args:
            inputs: 생성에 필요한 입력 파라미터 (선택사항)
            
        Returns:
            생성된 결과
        """
        if not self.model:
            raise ValueError("모델이 설정되지 않았습니다. 생성기를 초기화할 때 model 파라미터를 전달하거나 set_model()을 호출하세요.")
        
        messages = self._get_messages()
        ai_message = self.model.invoke(messages)
        if ai_message.response_metadata["finish_reason"] == "stop":
            return ai_message.content
        else:
            raise ValueError("예측하지 못한 Base Generator 종료 이유: " + ai_message.response_metadata["finish_reason"])

    def _get_messages(self) -> List[BaseMessage]:
        promptsToBuild = self._get_prompts_to_build()

        messages = []
        
        if promptsToBuild["system"]:
            messages.append(SystemMessage(content=promptsToBuild["system"]))

        for i in range(len(promptsToBuild["user"])):
            messages.append(HumanMessage(content=promptsToBuild["user"][i]))
            if(i < len(promptsToBuild["assistant"])):
                messages.append(AIMessage(content=promptsToBuild["assistant"][i]))
        
        return messages

    def _get_prompts_to_build(self) -> Dict[str, Union[str, List[str]]]:
        promptsToBuild = {
            "system": "",
            "user": [],
            "assistant": []
        }

        createPromptWithRoles = self.assemble_prompt()
        promptsToBuild["system"] = createPromptWithRoles["system"]
        promptsToBuild["user"] = createPromptWithRoles["user"]
        if(promptsToBuild["user"] and len(promptsToBuild["user"]) > 0 and not self.client.get("disableLanguageGuide")):
            promptsToBuild["user"][len(promptsToBuild["user"]) - 1] += "\n[Please generate the response in " + self.client.get("preferredLanguage") + " while ensuring that all code elements (e.g., variable names, function names) remain in English.]"
        
        promptsToBuild["assistant"] = createPromptWithRoles["assistant"]

        return promptsToBuild
    
    def set_model(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None) -> None:
        """
        LangChain 모델 설정
        
        Args:
            model_name: 모델 이름
            model_kwargs: 모델 파라미터
        """
        if model_kwargs is None: model_kwargs = {}
        self.model = init_chat_model(model_name, **model_kwargs)
    
    # 아래 메서드들은 상속 클래스에서 구현해야 함
    
    @abstractmethod
    def _build_agent_role_prompt(self) -> str:
        """
        AI 에이전트의 역할 및 전문 분야 정의
        
        Returns:
            str: 에이전트 역할 프롬프트
        """
        return ""
    
    @abstractmethod
    def _build_task_guidelines_prompt(self) -> str:
        """
        작업 수행을 위한 가이드라인 정의
        
        Returns:
            str: 작업 가이드라인 프롬프트
        """
        return ""
    
    def _build_inference_guidelines_prompt(self) -> str:
        """
        추론 모델을 위한 가이드라인 정의 (선택적 구현)
        
        Returns:
            str: 추론 가이드라인 프롬프트
        """
        return ""
    
    def _build_request_format_prompt(self) -> str:
        """
        요청 형식 정의 (선택적 구현)
        
        Returns:
            str: 요청 형식 프롬프트
        """
        return ""
    
    def _build_json_response_format(self) -> str:
        """
        JSON 응답 형식 정의 (선택적 구현)
        
        Returns:
            str: JSON 응답 형식
        """
        return ""
    
    def _build_after_json_response_format(self) -> str:
        """
        JSON 응답 이후 추가 안내 정의 (선택적 구현)
        
        Returns:
            str: JSON 응답 이후 안내 문구
        """
        return ""
    
    def _build_json_example_input_format(self) -> Optional[Dict[str, Any]]:
        """
        예제 입력 형식 정의 (선택적 구현)
        
        Returns:
            Optional[Dict]: 예제 입력 형식
        """
        return None
    
    def _build_json_user_query_input_format(self) -> Dict[str, Any]:
        """
        사용자 쿼리 입력 형식 정의 (선택적 구현)
        
        Returns:
            Dict: 사용자 쿼리 입력 형식
        """
        return {}
    
    def _build_json_example_output_format(self) -> Optional[Dict[str, Any]]:
        """
        예제 출력 형식 정의 (선택적 구현)
        
        Returns:
            Optional[Dict]: 예제 출력 형식
        """
        return None