import uuid
from typing import Dict, Any, List
from ..models import ActionModel
from .log_util import LogUtil
from .convert_case_util import CaseConvertUtil

class EsUtils:
    @staticmethod
    def get_uuid() -> str:
        """자바스크립트와 동일한 형식의 UUID 생성"""
        return str(uuid.uuid4())
    
    @staticmethod
    def add_line_numbers_to_description(description: str) -> str:
        """
        기능 요구사항 텍스트에 줄 번호를 추가하는 공통 메서드
        
        Args:
            description: 원본 기능 요구사항 텍스트
            
        Returns:
            줄 번호가 추가된 텍스트
        """
        if not description:
            return description
            
        lines = description.split('\n')
        line_numbered_description = '\n'.join([f"{i+1}: {line}" for i, line in enumerate(lines)])
        return line_numbered_description
    
    @staticmethod
    def convert_source_references(actions: List[ActionModel], original_description: str, state, log_prefix: str = "") -> None:
        """
        Action 목록의 모든 sourceReferences를 단어 조합에서 컬럼 위치로 변환하는 공통 메서드
        
        Args:
            actions: 변환할 액션 목록
            original_description: 원본 기능 요구사항 텍스트 (줄 번호 없는 버전)
            state: 로깅을 위한 State 객체
            log_prefix: 로그 메시지에 사용할 접두사
        """
        if not original_description:
            LogUtil.add_warning_log(state, f"{log_prefix} Original description is empty, skipping source reference conversion.")
            return

        lines = original_description.split('\n')

        for action in actions:
            args = action.args
            if not args:
                continue

            # Aggregate, ValueObject, Enumeration, Command, Event, ReadModel 자체의 sourceReferences 변환
            if args.get("sourceReferences"):
                is_processed = False
                for reference in args["sourceReferences"]:
                    for position_pair in reference:
                        if isinstance(position_pair, list) and all(isinstance(item, int) for item in position_pair):
                            continue
                        else:
                            args["sourceReferences"] = EsUtils._transform_reference(args["sourceReferences"], lines, state, log_prefix)
                            is_processed = True
                            break
                    if is_processed:
                        break

            # Properties 또는 queryParameters의 sourceReferences 변환
            properties_key = None
            if args.get("properties"):
                properties_key = "properties"
            elif args.get("queryParameters"):
                properties_key = "queryParameters"
                
            if properties_key and args.get(properties_key):
                for prop in args[properties_key]:
                    if isinstance(prop, dict) and prop.get("sourceReferences"):
                        is_processed = False
                        for reference in prop["sourceReferences"]:
                            for position_pair in reference:
                                if isinstance(position_pair, list) and all(isinstance(item, int) for item in position_pair):
                                    continue
                                else:
                                    prop["sourceReferences"] = EsUtils._transform_reference(prop["sourceReferences"], lines, state, log_prefix)
                                    is_processed = True
                                    break
                            if is_processed:
                                break

    @staticmethod
    def _transform_reference(reference: List[List[List[Any]]], lines: List[str], state, log_prefix: str) -> List[List[List[int]]]:
        """
        단일 sourceReferences 값을 변환합니다.
        
        Args:
            reference: 변환할 sourceReferences 값
            lines: 원본 텍스트의 줄 목록
            state: 로깅을 위한 State 객체
            log_prefix: 로그 메시지에 사용할 접두사
            
        Returns:
            변환된 sourceReferences 값
        """
        transformed_positions = []
        for position_pair in reference:
            try:
                if not position_pair:
                    continue

                start_pos = position_pair[0]
                end_pos = position_pair[1] if len(position_pair) > 1 else None

                start_line_num, start_words = start_pos
                start_line_num = int(start_line_num)

                start_col = EsUtils._find_column_for_words(lines, start_line_num, start_words)

                if end_pos:
                    end_line_num, end_words = end_pos
                    end_line_num = int(end_line_num)
                    end_col = EsUtils._find_column_for_words(lines, end_line_num, end_words, is_end=True)
                else:
                    end_line_num = start_line_num
                    end_words = ""
                    if 1 <= start_line_num <= len(lines):
                        line_content = lines[start_line_num - 1]
                        end_col = len(line_content)
                    else:
                        end_col = -1

                if start_col != -1 and end_col != -1:
                    transformed_positions.append([[start_line_num, start_col], [end_line_num, end_col]])
                else:
                    log_end_line = end_line_num if end_pos else start_line_num
                    log_end_words = f"'{end_words}'" if end_pos else "<end of line>"
                    LogUtil.add_warning_log(state, f"{log_prefix} Could not find words for reference. Start: L{start_line_num} '{start_words}', End: L{log_end_line} {log_end_words}. Skipping this reference.")

            except (ValueError, IndexError, TypeError) as e:
                LogUtil.add_warning_log(state, f"{log_prefix} Malformed sourceReferences item '{position_pair}'. Error: {e}. Skipping.")
                continue
        return transformed_positions

    @staticmethod
    def _find_column_for_words(lines: List[str], line_num: int, words: str, is_end: bool = False) -> int:
        """
        주어진 라인 번호와 단어 조합으로 컬럼 위치를 찾습니다.
        
        Args:
            lines: 텍스트의 줄 목록
            line_num: 라인 번호 (1-based)
            words: 찾을 단어 조합
            is_end: True이면 단어 조합의 끝 위치를 반환
            
        Returns:
            컬럼 위치 (1-based), 찾지 못하면 -1
        """
        if not (1 <= line_num <= len(lines)):
            return -1
        
        line_content = lines[line_num - 1]
        
        try:
            start_col = line_content.index(words)
            if is_end:
                return start_col + len(words)
            return start_col + 1  # 1-based index
        except ValueError:
            return len(line_content) if is_end else 0
    
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
    def get_aggregate_policies(es_value: Dict[str, Any], target_aggregate_id: str) -> List[Dict[str, Any]]:
        """특정 Aggregate에 속한 모든 Policy 가져오기"""
        return [
            element for element in es_value["elements"].values()
            if (element and
                element.get("_type") == "org.uengine.modeling.model.Policy" and
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
    def get_valid_position_for_left_side_element(es_value: Dict[str, Any], aggregate_id: str, 
                                                 element_object: Dict[str, Any]) -> Dict[str, int]:
        """Aggregate 좌측 요소(Command, ReadModel, Policy)의 유효한 위치를 계산합니다"""
        commands = EsUtils.get_aggregate_commands(es_value, aggregate_id)
        read_models = EsUtils.get_aggregate_read_models(es_value, aggregate_id)
        policies = EsUtils.get_aggregate_policies(es_value, aggregate_id)
        
        # 새롭게 추가되는 element_object는 아직 es_value에 없으므로, 중복 계산을 피하기 위해 리스트에서 제거
        all_models = [
            m for m in (commands + read_models + policies) 
            if m["id"] != element_object["id"]
        ]
        
        if len(all_models) <= 0:
            current_aggregate = es_value["elements"].get(aggregate_id, {})
            if not current_aggregate:
                return {"x": 0, "y": 0}
                
            return {
                "x": current_aggregate["elementView"]["x"] - int(current_aggregate["elementView"]["width"]/2) - 29,
                "y": current_aggregate["elementView"]["y"] - int(current_aggregate["elementView"]["height"]/2)
            }
        else:
            min_x = min(model["elementView"]["x"] for model in all_models)
            max_y = max(model["elementView"]["y"] for model in all_models)
            
            max_y_models = [model for model in all_models if model["elementView"]["y"] == max_y]
            if not max_y_models:
                return {"x": min_x, "y": max_y + 150}
                
            max_y_model = max_y_models[0]
            return {
                "x": min_x,
                "y": max_y + int(max_y_model["elementView"]["height"]/2) + int(element_object["elementView"]["height"]/2) + 14
            }
            
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
            "relationType": "Realization",
            "fromLabel": "",
            "toLabel": ""
        }

    @staticmethod
    def resize_aggregate_vertically(es_value: Dict[str, Any], agg_element_object: Dict[str, Any]) -> None:
        """Aggregate 크기를 수직으로 조정합니다"""
        RESIZE_HEIGHT = 115 + 14
        
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
            bc_object["elementView"]["height"] += RESIZE_HEIGHT
            bc_object["elementView"]["y"] += int(RESIZE_HEIGHT/2)
            es_value["elements"][bc_object["id"]] = bc_object.copy()

            # 아래 BoundedContext 위치 조정
            for bc_element in EsUtils.get_all_bc_below_bc(es_value, bc_object):
                bc_element["elementView"]["y"] += RESIZE_HEIGHT
                es_value["elements"][bc_element["id"]] = bc_element.copy()
                
                for element_in_bc in EsUtils.get_all_elements_in_bounded_context(es_value, bc_element["id"]):
                    element_in_bc["elementView"]["y"] += RESIZE_HEIGHT
                    es_value["elements"][element_in_bc["id"]] = element_in_bc.copy()
        
        # Aggregate 크기 조정
        agg_object["elementView"]["height"] += RESIZE_HEIGHT
        agg_object["elementView"]["y"] += int(RESIZE_HEIGHT/2)
        es_value["elements"][agg_object["id"]] = agg_object.copy()
    
    @staticmethod
    def get_all_bc_below_bc(es_value: Dict[str, Any], bc_object: Dict[str, Any]) -> List[Dict[str, Any]]:
        """지정된 BoundedContext 아래에 있으면서 직접적으로 인접한 모든 BoundedContext를 가져옵니다."""
        target_bc_id = bc_object.get("id")
        target_view = bc_object.get("elementView", {})
        if not target_view or not target_bc_id:
            return []

        target_y = target_view.get("y", 0)
        target_x = target_view.get("x", 0)
        target_width = target_view.get("width", 0)
        target_height = target_view.get("height", 0)
        target_left = target_x - (target_width // 2)
        target_right = target_x + (target_width // 2)
        target_bottom = target_y + (target_height // 2)

        bcs_below = []
        for element in es_value["elements"].values():
            if not element or element.get("_type") != "org.uengine.modeling.model.BoundedContext":
                continue
            
            element_id = element.get("id")
            element_view = element.get("elementView", {})
            if not element_id or not element_view or element_id == target_bc_id:
                continue

            element_y = element_view.get("y", 0)
            
            # 1. 수직 위치 확인: 대상 BC보다 아래에 있는지 확인 (y 좌표가 더 큰 경우)
            if element_y <= target_y:
                continue

            element_x = element_view.get("x", 0)
            element_width = element_view.get("width", 0)
            element_height = element_view.get("height", 0)
            element_left = element_x - (element_width // 2)
            element_right = element_x + (element_width // 2)
            element_bottom = element_y + (element_height // 2)
            
            # 2. 수평 위치 확인: 수평으로 겹치는지 확인
            # (element의 범위가 target의 범위와 하나라도 겹치면 True)
            is_horizontally_overlapping = (element_right >= target_left and element_left <= target_right)
            
            # 3. 수직 인접성 확인: 불필요한 공백을 방지하기 위해, 바로 아래에 위치하는지 검사합니다.
            is_vertically_adjacent = element_bottom >= target_bottom
            
            if is_horizontally_overlapping and is_vertically_adjacent:
                bcs_below.append(element)
                
        return bcs_below

    @staticmethod
    def create_field_descriptors(
        properties: List[Dict[str, Any]],
        options: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        속성 목록에서 필드 디스크립터 목록을 생성합니다.

        Args:
            properties: 필드 속성 목록.
            options (dict): 생성 옵션.
                'is_value_object' (bool): ValueObject 전용 `label` 필드를 추가합니다.
                'is_root_aggregate' (bool): AggregateRoot 전용 필드를 추가하고 displayName을 비웁니다.
                'include_ref_and_override' (bool): `referenceClass`와 `isOverrideField`를 포함합니다.
                'exclude_foreign' (bool): 'isForeignProperty'가 True인 속성을 제외합니다.
        """
        if options is None:
            options = {}

        descriptors = []
        
        props_to_process = properties
        if options.get("exclude_foreign"):
            props_to_process = [p for p in properties if not p.get("isForeignProperty")]

        for prop in props_to_process:
            name = prop.get("name", "")
            prop_type = prop.get("type") or "String"
            
            descriptor = {
                "className": prop_type,
                "isCopy": False,
                "isKey": prop.get("isKey") or False,
                "name": CaseConvertUtil.camel_case(name),
                "nameCamelCase": CaseConvertUtil.camel_case(name),
                "namePascalCase": CaseConvertUtil.pascal_case(name),
                "displayName": prop.get("displayName", ""),
                "_type": "org.uengine.model.FieldDescriptor",
                "isList": ("list" in prop_type.lower()) or ("collection" in prop_type.lower()),
                "sourceReferences": prop.get("sourceReferences", None)
            }

            if options.get("is_root_aggregate"):
                descriptor["displayName"] = ""
                descriptor["inputUI"] = None
                descriptor["options"] = None
            
            if options.get("include_ref_and_override"):
                descriptor["referenceClass"] = prop.get("referenceClass", None)
                descriptor["isOverrideField"] = prop.get("isOverrideField", False)
                
            if options.get("is_value_object"):
                descriptor["label"] = f"- {name}: {prop_type}"

            descriptors.append(descriptor)
            
        return descriptors
