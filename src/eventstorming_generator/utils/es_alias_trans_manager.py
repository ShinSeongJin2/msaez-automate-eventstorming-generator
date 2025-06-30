from typing import Dict, Any, List

from .es_utils import EsUtils
from .convert_case_util import CaseConvertUtil

class EsAliasTransManager:
    """
    주어진 엘리먼트 이름 정보를 토대로 기존의 UUID 이름을 의미가 있는 별칭으로 변환/역복원시켜서 LLM에게 더 의미있는 엘리먼트 이름을 제공하도록 도와줌
    """
    def __init__(self, es_value: Dict[str, Any]):
        self.es_value = es_value
        self.uuid_to_alias_dic: Dict[str, str] = {}
        self.alias_to_uuid_dic: Dict[str, str] = {}
        
        self._init_uuid_alias_for_elements()
        self._init_uuid_alias_for_relations()
    
    def _init_uuid_alias_for_elements(self):
        """요소들의 UUID와 별칭 초기화"""
        if not self.es_value.get("elements"):
            return
        
        for key, element in self.es_value["elements"].items():
            if not element:
                continue
                
            alias_to_use = self.__make_alias_to_use(element)
            self.uuid_to_alias_dic[key] = alias_to_use
            self.alias_to_uuid_dic[alias_to_use] = key
            
            # Aggregate 타입이 아니거나 하위 엔티티가 없는 경우 건너뜀
            if element.get("_type") != "org.uengine.modeling.model.Aggregate":
                continue
                
            if (not element.get("aggregateRoot") or 
                not element["aggregateRoot"].get("entities") or 
                not element["aggregateRoot"]["entities"].get("elements")):
                continue
                
            aggregate_elements = element["aggregateRoot"]["entities"]["elements"]
            
            for entity_key, entity in aggregate_elements.items():
                if not entity:
                    continue
                    
                entity_alias_to_use = self.__make_alias_to_use(entity)
                self.uuid_to_alias_dic[entity_key] = entity_alias_to_use
                self.alias_to_uuid_dic[entity_alias_to_use] = entity_key
    
    def _init_uuid_alias_for_relations(self):
        """관계들의 UUID와 별칭 초기화"""
        if not self.es_value.get("relations"):
            return
            
        for relation_key, relation in self.es_value["relations"].items():
            if not relation:
                continue
                
            relation_alias_to_use = self._get_alias_for_relation(relation)
            self.uuid_to_alias_dic[relation_key] = relation_alias_to_use
            self.alias_to_uuid_dic[relation_alias_to_use] = relation_key
    
    def _get_alias_for_relation(self, relation: Dict[str, Any]) -> str:
        """관계 객체의 별칭 생성"""
        source_alias = self.__make_alias_to_use(relation["sourceElement"])
        target_alias = self.__make_alias_to_use(relation["targetElement"])
        return f"{source_alias}-to-{target_alias}"
    
    def __make_alias_to_use(self, element: Dict[str, Any]) -> str:
        """
        각 엘리먼트 타입마다 충돌되지 않는 의미있는 별칭을 LLM에게 제공하기 위함
        """
        def get_front_id(element: Dict[str, Any]) -> str:
            element_type = element.get("_type", "").lower()
            
            if "org.uengine.modeling.model.boundedcontext" in element_type:
                return "bc"
            elif "org.uengine.modeling.model.aggregate" in element_type:
                return "agg"
            elif "org.uengine.modeling.model.command" in element_type:
                return "cmd"
            elif "org.uengine.modeling.model.event" in element_type:
                return "evt"
            elif "org.uengine.modeling.model.view" in element_type:
                return "rm"
            elif "org.uengine.modeling.model.actor" in element_type:
                return "act"
            elif "org.uengine.uml.model.class" in element_type:
                return "agg-root" if element.get("isAggregateRoot") else "ent"
            elif "org.uengine.uml.model.enum" in element_type:
                return "enum"
            elif "org.uengine.uml.model.vo.class" in element_type:
                return "vo"
            elif "org.uengine.modeling.model.policy" in element_type:
                return "pol"
            else:
                return "obj"
        
        if element.get("id") in self.uuid_to_alias_dic:
            return self.uuid_to_alias_dic[element["id"]]
        
        base_alias = f"{get_front_id(element)}-{CaseConvertUtil.camel_case(element.get('name', ''))}"
        alias_to_use = base_alias
        i = 2
        
        while alias_to_use in self.alias_to_uuid_dic:
            alias_to_use = f"{base_alias}-{i}"
            i += 1
            
        return alias_to_use
    
    def get_alias_safely(self, uuid_val: str) -> str:
        """UUID를 안전하게 별칭으로 변환"""
        return self.uuid_to_alias_dic.get(uuid_val, uuid_val)
    
    def get_element_alias_safely(self, element: Dict[str, Any]) -> str:
        """엘리먼트에서 ID를 추출하여 별칭으로 변환"""
        if element.get("id"):
            return self.get_alias_safely(element["id"])
        if element.get("elementView") and element["elementView"].get("id"):
            return self.get_alias_safely(element["elementView"]["id"])
        return element.get("id", "")
    
    def get_uuid_safely(self, alias: str) -> str:
        """별칭을 안전하게 UUID로 변환"""
        return self.alias_to_uuid_dic.get(alias, alias)
    
    def get_uuid_safely_with_new_uuid(self, alias: str) -> str:
        """별칭을 UUID로 변환하고 없다면 새 UUID 생성"""
        if alias in self.alias_to_uuid_dic:
            return self.alias_to_uuid_dic[alias]
        
        new_uuid = EsUtils.get_uuid()
        self.alias_to_uuid_dic[alias] = new_uuid
        self.uuid_to_alias_dic[new_uuid] = alias
        return new_uuid
    
    def trans_to_alias_in_actions(self, actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """액션 내의 ID들을 별칭으로 변환"""
        return self._trans_actions(actions, lambda uuid_val: self.get_alias_safely(uuid_val))
    
    def trans_to_uuid_in_actions(self, actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """액션 내의 별칭들을 UUID로 변환"""
        return self._trans_actions(actions, lambda alias: self.get_uuid_safely_with_new_uuid(alias))
    
    def _trans_actions(self, actions: List[Dict[str, Any]], trans_func) -> List[Dict[str, Any]]:
        """액션 내의 ID들을 변환 함수를 통해 처리"""
        for action in actions:
            if "ids" in action:
                for id_key in action["ids"]:
                    action["ids"][id_key] = trans_func(action["ids"][id_key])
            
            if action.get("objectType") == "Command" and action.get("args") and "outputEventIds" in action["args"]:
                action["args"]["outputEventIds"] = [trans_func(id_val) for id_val in action["args"]["outputEventIds"]]
            
            if action.get("objectType") == "Policy" and action.get("args") and "inputEventIds" in action["args"]:
                action["args"]["inputEventIds"] = [trans_func(id_val) for id_val in action["args"]["inputEventIds"]]

            if action.get("objectType") == "Policy" and action.get("args") and "outputEventIds" in action["args"]:
                action["args"]["outputEventIds"] = [trans_func(id_val) for id_val in action["args"]["outputEventIds"]]
        
        return actions
