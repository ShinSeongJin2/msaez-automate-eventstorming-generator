import uuid
from typing import Dict, Any, List

class EsUtils:
    @staticmethod
    def get_uuid() -> str:
        """자바스크립트와 동일한 형식의 UUID 생성"""
        return str(uuid.uuid4())
    
    @staticmethod
    def get_all_bounded_contexts(es_value: Dict[str, Any]) -> List[Dict[str, Any]]:
        """es_value에서 모든 BoundedContext 요소 가져오기"""
        if not es_value.get("elements"):
            return []
        
        return [
            element for element in es_value["elements"].values()
            if element and element.get("_type") == "org.uengine.modeling.model.BoundedContext"
        ]
    
    @staticmethod
    def get_all_elements_in_bounded_context(es_value: Dict[str, Any], bounded_context_id: str) -> List[Dict[str, Any]]:
        """특정 BoundedContext에 속한 모든 요소 가져오기"""
        if not es_value.get("elements"):
            return []
        
        return [
            element for element in es_value["elements"].values()
            if element and element.get("boundedContext") and element["boundedContext"].get("id") == bounded_context_id
        ]
    
    @staticmethod
    def get_all_aggregates_in_bounded_context(es_value: Dict[str, Any], bounded_context_id: str) -> List[Dict[str, Any]]:
        """특정 BoundedContext에 속한 모든 Aggregate 요소 가져오기"""
        if not es_value.get("elements"):
            return []
        
        return [
            element for element in es_value["elements"].values()
            if (element and 
                element.get("_type") == "org.uengine.modeling.model.Aggregate" and 
                element.get("boundedContext", {}).get("id") == bounded_context_id)
        ]
    
    @staticmethod
    def get_aggregate_root_object(aggregate_object: Dict[str, Any]) -> Dict[str, Any]:
        """Aggregate Root 객체 가져오기"""
        if (not aggregate_object.get("aggregateRoot") or 
            not aggregate_object["aggregateRoot"].get("entities") or 
            not aggregate_object["aggregateRoot"]["entities"].get("elements")):
            return None
        
        for element in aggregate_object["aggregateRoot"]["entities"]["elements"].values():
            if element.get("isAggregateRoot"):
                return element
        
        return None 