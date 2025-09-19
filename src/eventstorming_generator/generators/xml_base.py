import os
from typing import Dict, List, Any, Optional, Union, Type
from abc import ABC, abstractmethod
from langchain.chat_models import init_chat_model
from langchain.schema import HumanMessage, SystemMessage, AIMessage, BaseMessage
from langchain_community.cache import SQLiteCache
from langchain_core.globals import set_llm_cache

from ..models import BaseModelWithItem
from ..utils import JsonUtil
from ..config import Config


def init_cache():
    if not os.path.exists(".cache"):
        os.makedirs(".cache")

    set_llm_cache(SQLiteCache(database_path=".cache/llm_cache.db"))

if Config.is_local_run():
    init_cache()


class XmlBaseGenerator(ABC):
    """
    프롬프트 구성 및 LLM 호출을 위한 기본 생성기 클래스
    
    이 클래스는 구조화된 프롬프트 생성 및 LangChain 모델과의 통합을 위한 인터페이스를 제공합니다.
    상속받는 클래스는 프롬프트 구성 요소들을 구현하고, 이 베이스 클래스는 이를 조합하여 
    일관된 프롬프트 형식을 제공합니다.
    """
    
    def __init__(self, model_name: str, structured_output_class: Type, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        """
        XmlBaseGenerator 초기화
        
        Args:
            model_name: 모델 이름
            model_kwargs: 모델 파라미터
            client: 클라이언트
            structured_output_class: 구조화된 출력을 위한 Pydantic 모델 클래스
        """
        if not model_name or not structured_output_class:
            raise ValueError("model_name and structured_output_class are required")
        
        if model_kwargs is None: model_kwargs = {}
        if model_kwargs.get("temperature") is None: 
            if "gpt-4.1" in model_name:
                model_kwargs["temperature"] = 0.2

        if client is None: client = {}
        if not client.get("inputs"): client["inputs"] = {}
        if not client.get("preferredLanguage"): client["preferredLanguage"] = "English"
        if not client.get("disableLanguageGuide"): client["disableLanguageGuide"] = False

        if self.inputs_types_to_check:
            for input_type in self.inputs_types_to_check:
                if client.get("inputs").get(input_type) == None:
                    raise ValueError(f"{input_type} is required")

        self.structured_output_class = structured_output_class
        self.client = client
        self.set_model(model_name, model_kwargs)

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
        persona_info = self._build_persona_info()
        if persona_info["persona"] and persona_info["goal"] and persona_info["backstory"]:
            return f"""<persona_and_role>
    <persona>{persona_info["persona"]}</persona>
    <goal>{persona_info["goal"]}</goal>
    <backstory>{persona_info["backstory"]}</backstory>
</persona_and_role>"""
        else:
            return ""
    
    def _build_user_prompt(self) -> List[str]:
        """유저 프롬프트 빌드"""
        prompts = []
        
        instruction_prompt = self._build_task_instruction_prompt()
        example_inputs = self._build_json_example_input_format()
        user_inputs = self._build_json_user_query_input_format()
        
        approve_request = "<request>This is the entire guideline. When you're ready, please output 'Approved.' Then I will begin user input.</request>"
        if example_inputs and user_inputs:
            prompts.append(instruction_prompt + "\n\n" + approve_request)
            prompts.append(self._inputs_to_string(example_inputs))
            prompts.append(self._inputs_to_string(user_inputs))
        elif user_inputs:
            prompts.append(instruction_prompt + "\n\n" + approve_request)
            prompts.append(self._inputs_to_string(user_inputs))
        
        return prompts
    
    def _build_assistant_prompt(self) -> List[str]:
        """어시스턴트 프롬프트 빌드"""
        example_outputs = self._build_json_example_output_format()
        if not example_outputs:
            return []
        
        return ["Approved.", JsonUtil.convert_to_json(example_outputs, 4)]
    
    def _inputs_to_string(self, inputs: Dict[str, Any]) -> str:
        """입력 파라미터를 문자열로 변환"""
        result = []
        
        for key, value in inputs.items():
            formatted_value = value if isinstance(value, str) else JsonUtil.convert_to_json(value, 0)
            result.append(f"<{key.strip()}>{formatted_value.strip()}</{key.strip()}>")
            
        return "<inputs>\n" + "\n".join(result) + "\n</inputs>"
    
    def generate(self, bypass_cache: bool = False, retry_count: int = 0) -> Any:
        """
        LLM을 사용하여 생성 실행
        
        Args:
            bypass_cache: 캐시 우회 여부
            
        Returns:
            생성된 결과 (구조화된 출력이 설정된 경우 해당 클래스의 인스턴스)
        """
        if not self.model:
            raise ValueError("모델이 설정되지 않았습니다. 생성기를 초기화할 때 model 파라미터를 전달하거나 set_model()을 호출하세요.")
        if not Config.is_local_run():
            bypass_cache = False

        messages = self._get_messages(bypass_cache, retry_count)
        structured_model = self.model.with_structured_output(
            self.structured_output_class,
            method="function_calling"
        )
        result = structured_model.invoke(messages)
        result = self._post_process_to_structured_output(result)

        if isinstance(result, BaseModelWithItem):
            return result.model_dump()
        else:
            return result

    def _post_process_to_structured_output(self, structured_output: BaseModelWithItem) -> BaseModelWithItem:
        return structured_output

    def _get_messages(self, bypass_cache: bool = False, retry_count: int = 0) -> List[BaseMessage]:
        promptsToBuild = self._get_prompts_to_build()

        messages = []
        
        if promptsToBuild["system"]:
            system_content = promptsToBuild["system"]
            if bypass_cache:
                system_content += f"<cache_bypass retry_count=\"{retry_count}\"/>"
            messages.append(SystemMessage(content=system_content))

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
            promptsToBuild["user"][len(promptsToBuild["user"]) - 1] += "\n<language_guide>Please generate the response in " + self.client.get("preferredLanguage") + " while ensuring that all code elements (e.g., variable names, function names) remain in English.</language_guide>"
        
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
    
    def get_token_count(self) -> int:
        """
        현재 구축된 메세지들의 전체 토큰 수 반환
        """
        messages = self._get_messages()

        total_contents = ""
        for message in messages:
            total_contents += message.content
        
        return self.model.get_num_tokens(total_contents)
    
    def get_entire_prompt(self) -> str:
        """
        현재 구축된 메세지들의 전체 프롬프트 반환
        """
        messages = self._get_messages()
        return "\n---------\n".join([message.content for message in messages])
    
    # 아래 메서드들은 상속 클래스에서 구현해야 함
    
    @abstractmethod
    def _build_persona_info(self) -> Dict[str, str]:
        """
        AI 에이전트의 역할 및 전문 분야 정의
        
        Returns:
            str: 에이전트 역할 프롬프트
        """
        return {
            "persona": "",
            "goal": "",
            "backstory": ""
        }
    
    @abstractmethod
    def _build_task_instruction_prompt(self) -> str:
        """
        작업 수행을 위한 가이드라인 정의
        
        Returns:
            str: 작업 가이드라인 프롬프트
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