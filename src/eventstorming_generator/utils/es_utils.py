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
    def get_element_ids_in_bounded_context(es_value: Dict[str, Any], bounded_context_id: str) -> List[str]:
        """특정 BoundedContext에 속한 모든 요소의 ID 가져오기"""
        return [element["id"] for element in EsUtils.get_all_elements_in_bounded_context(es_value, bounded_context_id)]
    
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

    @staticmethod
    def get_entities_for_aggregate(es_value: Dict[str, Any], aggregate_id: str) -> Dict[str, Any]:
        """Aggregate의 entities 객체를 가져옵니다. 없으면 초기화합니다."""
        aggregate = es_value["elements"].get(aggregate_id, {})
        
        if not aggregate.get("aggregateRoot"):
            aggregate["aggregateRoot"] = {}
            
        if not aggregate["aggregateRoot"].get("entities"):
            aggregate["aggregateRoot"]["entities"] = {}
            
        entities = aggregate["aggregateRoot"]["entities"]
        
        if not entities.get("elements"):
            entities["elements"] = {}
            
        if not entities.get("relations"):
            entities["relations"] = {}
            
        return entities
    
    @staticmethod
    def get_aggregate_commands(es_value: Dict[str, Any], target_aggregate_id: str) -> List[Dict[str, Any]]:
        """특정 Aggregate에 속한 모든 Command 가져오기"""
        return [
            element for element in es_value["elements"].values()
            if (element and
                element.get("_type") == "org.uengine.modeling.model.Command" and
                element.get("aggregate", {}).get("id") == target_aggregate_id)
        ]
    
    @staticmethod
    def get_aggregate_read_models(es_value: Dict[str, Any], target_aggregate_id: str) -> List[Dict[str, Any]]:
        """특정 Aggregate에 속한 모든 View(ReadModel) 가져오기"""
        return [
            element for element in es_value["elements"].values()
            if (element and
                element.get("_type") == "org.uengine.modeling.model.View" and
                element.get("aggregate", {}).get("id") == target_aggregate_id)
        ]
    
    @staticmethod
    def get_aggregate_events(es_value: Dict[str, Any], target_aggregate_id: str) -> List[Dict[str, Any]]:
        """특정 Aggregate에 속한 모든 Event 가져오기"""
        return [
            element for element in es_value["elements"].values()
            if (element and
                element.get("_type") == "org.uengine.modeling.model.Event" and
                element.get("aggregate", {}).get("id") == target_aggregate_id)
        ]
    
    @staticmethod
    def get_related_value_objects(es_value: Dict[str, Any], aggregate_id: str) -> List[Dict[str, Any]]:
        """특정 Aggregate에 속한 모든 ValueObject 가져오기"""
        entities = EsUtils.get_entities_for_aggregate(es_value, aggregate_id)
        return [
            element for element in entities["elements"].values()
            if element and element.get("_type") == "org.uengine.uml.model.vo.Class"
        ]
    
    @staticmethod
    def get_related_enumerations(es_value: Dict[str, Any], aggregate_id: str) -> List[Dict[str, Any]]:
        """특정 Aggregate에 속한 모든 Enumeration 가져오기"""
        entities = EsUtils.get_entities_for_aggregate(es_value, aggregate_id)
        return [
            element for element in entities["elements"].values()
            if element and element.get("_type") == "org.uengine.uml.model.enum"
        ]
    
    @staticmethod
    def get_related_general_classes(es_value: Dict[str, Any], aggregate_id: str) -> List[Dict[str, Any]]:
        """특정 Aggregate에 속한 일반 클래스(AggregateRoot가 아닌 Class) 가져오기"""
        entities = EsUtils.get_entities_for_aggregate(es_value, aggregate_id)
        return [
            element for element in entities["elements"].values()
            if (element and 
                not element.get("isAggregateRoot") and 
                element.get("_type") == "org.uengine.uml.model.Class")
        ]
    
    @staticmethod
    def is_related_by_delete_command(es_value: Dict[str, Any], event: Dict[str, Any]) -> bool:
        """이벤트가 DELETE Command와 연결되어 있는지 확인"""
        return any(
            relation for relation in es_value["relations"].values()
            if (relation and
                relation.get("_type") == "org.uengine.modeling.model.Relation" and
                relation.get("sourceElement", {}).get("_type") == "org.uengine.modeling.model.Command" and
                relation["sourceElement"].get("isRestRepository") and
                relation["sourceElement"].get("controllerInfo", {}).get("method") == "DELETE" and
                relation.get("targetElement", {}).get("id") == event["id"])
        )
    
    @staticmethod
    def is_related_by_post_command(es_value: Dict[str, Any], event: Dict[str, Any]) -> bool:
        """이벤트가 POST Command와 연결되어 있는지 확인"""
        return any(
            relation for relation in es_value["relations"].values()
            if (relation and
                relation.get("_type") == "org.uengine.modeling.model.Relation" and
                relation.get("sourceElement", {}).get("_type") == "org.uengine.modeling.model.Command" and
                relation["sourceElement"].get("isRestRepository") and
                relation["sourceElement"].get("controllerInfo", {}).get("method") == "POST" and
                relation.get("targetElement", {}).get("id") == event["id"])
        )

    @staticmethod
    def getEventStormingRelationObjectBase(fromObject: Dict[str, Any], toObject: Dict[str, Any]) -> Dict[str, Any]:
        """이벤트스토밍 관계 객체 생성"""
        elementUUIDtoUse = EsUtils.get_uuid()
        FROM_OBJECT_ID = fromObject.get("id") or fromObject["elementView"]["id"]
        TO_OBJECT_ID = toObject.get("id") or toObject["elementView"]["id"]

        return {
            "_type": "org.uengine.modeling.model.Relation",
            "name": "",
            "id": elementUUIDtoUse,
            "sourceElement": fromObject,
            "targetElement": toObject,
            "from": FROM_OBJECT_ID,
            "to": TO_OBJECT_ID,
            "relationView": {
                "id": elementUUIDtoUse,
                "style": '{"arrow-start":"none","arrow-end":"none"}',
                "from": FROM_OBJECT_ID,
                "to": TO_OBJECT_ID,
                "needReconnect": True,
                "value": "[]"
            },
            "hexagonalView": {
                "_type": "org.uengine.modeling.model.RelationHexagonal",
                "from": FROM_OBJECT_ID,
                "id": elementUUIDtoUse,
                "needReconnect": True,
                "style": '{"arrow-start":"none","arrow-end":"none"}',
                "to": TO_OBJECT_ID,
                "value": None
            },
            "sourceMultiplicity": "1",
            "targetMultiplicity": "1",
        }
    
    @staticmethod
    def getDDLRelationObjectBase(fromObject: Dict[str, Any], toObject: Dict[str, Any]) -> Dict[str, Any]:
        """DDL 관계 객체 생성"""
        elementUUIDtoUse = EsUtils.get_uuid()
        FROM_OBJECT_ID = fromObject.get("id") or fromObject["elementView"]["id"]
        TO_OBJECT_ID = toObject.get("id") or toObject["elementView"]["id"]
        
        return {
            "name": toObject.get("name", ""),
            "id": elementUUIDtoUse,
            "_type": "org.uengine.uml.model.Relation",
            "sourceElement": fromObject,
            "targetElement": toObject,
            "from": FROM_OBJECT_ID,
            "to": TO_OBJECT_ID,
            "selected": False,
            "relationView": {
                "id": elementUUIDtoUse,
                "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                "from": FROM_OBJECT_ID,
                "to": TO_OBJECT_ID,
                "needReconnect": True
            },
            "sourceMultiplicity": "1",
            "targetMultiplicity": "1",
            "relationType": "Association",
            "fromLabel": "",
            "toLabel": ""
        }

    @staticmethod
    def resize_aggregate_vertically(es_value: Dict[str, Any], agg_element_object: Dict[str, Any]) -> None:
        """Aggregate 크기를 수직으로 조정합니다"""
        RESIZE_HEIGHT = 150
        
        bc_object = es_value["elements"].get(agg_element_object["boundedContext"]["id"], {})
        agg_object = es_value["elements"].get(agg_element_object["aggregate"]["id"], {})
        
        if not bc_object or not agg_object:
            return
            
        # 불필요한 리사이징 방지
        if agg_element_object["elementView"]["y"] <= agg_object["elementView"]["y"] + int(agg_object["elementView"]["height"]/2):
            return
        
        # BoundedContext 크기 조정
        if (agg_object["elementView"]["y"] + int(agg_object["elementView"]["height"]/2) + RESIZE_HEIGHT >
            bc_object["elementView"]["y"] + int(bc_object["elementView"]["height"]/2)):
            BC_RESIZE_HEIGHT = int(RESIZE_HEIGHT * 0.90)
            bc_object["elementView"]["height"] += BC_RESIZE_HEIGHT
            bc_object["elementView"]["y"] += int(BC_RESIZE_HEIGHT/2)
            es_value["elements"][bc_object["id"]] = bc_object.copy()
        
        # Aggregate 크기 조정
        agg_object["elementView"]["height"] += RESIZE_HEIGHT
        agg_object["elementView"]["y"] += int(RESIZE_HEIGHT/2)
        es_value["elements"][agg_object["id"]] = agg_object.copy()
        
        # 아래 BoundedContext 위치 조정
        for bc_element in EsUtils.get_all_bc_below_bc(es_value, bc_object):
            bc_element["elementView"]["y"] += RESIZE_HEIGHT
            es_value["elements"][bc_element["id"]] = bc_element.copy()
            
            for element_in_bc in EsUtils.get_all_elements_in_bounded_context(es_value, bc_element["id"]):
                element_in_bc["elementView"]["y"] += RESIZE_HEIGHT
                es_value["elements"][element_in_bc["id"]] = element_in_bc.copy()
    
    @staticmethod
    def get_all_bc_below_bc(es_value: Dict[str, Any], bc_object: Dict[str, Any]) -> List[Dict[str, Any]]:
        """지정된 BoundedContext 아래에 있는 모든 BoundedContext를 가져옵니다"""
        return [
            element for element in es_value["elements"].values()
            if (element and
                element.get("_type") == "org.uengine.modeling.model.BoundedContext" and
                element.get("id") != bc_object["id"] and
                element["elementView"]["y"] >= bc_object["elementView"]["y"] and
                element["elementView"]["x"] >= bc_object["elementView"]["x"] - int(bc_object["elementView"]["width"]/2) and
                element["elementView"]["x"] <= bc_object["elementView"]["x"] + int(bc_object["elementView"]["width"]/2))
        ]
