from typing import Dict, Any, List, Callable, Optional

from .es_alias_trans_manager import EsAliasTransManager

class ESValueSummarizeWithFilter:
    """
    이벤트 스토밍 모델(es_value)을 요약된 형태로 변환하는 클래스입니다.
    특정 속성들을 제외하고 싶을 때 keys_to_exclude_filter를 사용하여 필터링할 수 있으며,
    ID 변환이 필요한 경우 es_alias_trans_manager를 통해 처리할 수 있습니다.
    """
    
    # 필터 템플릿 정의
    KEY_FILTER_TEMPLATES = {
        "aggregateOuterStickers": ["aggregate.commands", "aggregate.events", "aggregate.readModels"],
        "aggregateInnerStickers": ["aggregate.entities", "aggregate.enumerations", "aggregate.valueObjects"],
        "detailedProperties": ["properties", "items"]
    }
    
    @staticmethod
    def get_guide_prompt() -> str:
        """
        LLM에 전달할 가이드 프롬프트를 반환합니다.
        """
        return """You will receive a JSON object containing summarized information about the event storming model on which you will perform your task. Not all guided properties may be passed, and properties that are unnecessary for the task may be excluded.
The approximate structure is as follows.
{
    // Properties that have been deleted because they are not needed for the given task.
    "deletedProperties": ["<deletedPropertyPath>"],

    "boundedContexts": [
        "id": "<boundedContextId>",
        "name": "<boundedContextName>",
        "actors": [
            {
                "id": "<actorId>",
                "name": "<actorName>"
            }
        ],
        "aggregates": [
            {
                "id": "<aggregateId>",
                "name": "<aggregateName>",
                "properties": [
                    {
                        "name": "<propertyName>",

                        // "<propertyType>" must belong to one of the following three categories:
                        // 1. Well-known Java class names. In this case, write only the class name without the full package path. (e.g., java.lang.String > String)
                        // 2. If there's a name defined in Enumerations or ValueObjects or Entities, It can be used as the property type.
                        // If the type is String, do not specify the type.
                        ["type": "<propertyType>"],

                        // Only one of the properties should have isKey set to true.
                        // If it needs a composite key, it will reference a ValueObject with those properties.
                        ["isKey": true]
                    }
                ],

                "entities": [
                    {
                        "id": "<entityId>",
                        "name": "<entityName>",
                        "properties": [
                            {
                                "name": "<propertyName>",
                                ["type": "<propertyType>"], 
                                ["isKey": true],

                                // If this property references a property in another table, this value should be set to true.
                                ["isForeignProperty": true]
                            }
                        ]
                    }
                ],

                "enumerations": [
                    {
                        "id": "<enumerationId>",
                        "name": "<enumerationName>",
                        "items": ["<itemName1>"]
                    }
                ],

                "valueObjects": [
                    {
                        "id": "<valueObjectId>",
                        "name": "<valueObjectName>",
                        "properties": [
                            {
                                "name": "<propertyName>",
                                ["type": "<propertyType>"],
                                ["isKey": true],
                                ["isForeignProperty": true],

                                // If the property is used as a foreign key to reference another Aggregate, write the name of that Aggregate.
                                ["referencedAggregateName": "<referencedAggregateName>"]
                            }
                        ]
                    }
                ],

                "commands": [
                    {
                        "id": "<commandId>",
                        "name": "<commandName>",
                        "api_verb":  <"POST" | "PUT" | "PATCH" | "DELETE">,

                        // Determines the API endpoint structure:
                        // true: Uses standard REST endpoints with HTTP verbs only (e.g., POST /book)
                        // false: Uses custom endpoints with command names for complex operations (e.g., POST /book/updateStatus)
                        "isRestRepository": <true | false>, 
                        "properties": [
                            {
                                "name": "<propertyName>",
                                ["type": "<propertyType>"],
                                ["isKey": true]
                            }
                        ],

                        // A list of cascading events that occur when a command is executed.
                        "outputEvents": [
                            {
                                "id": "<eventId>",
                                "name": "<eventName>"
                            }
                        ]
                    }
                ],

                "events": [
                    {
                        "id": "<eventId>",
                        "name": "<eventName>",
                        "properties": [
                            {
                                "name": "<propertyName>",
                                ["type": "<propertyType>"],
                                ["isKey": true]
                            }
                        ],

                        // A list of cascading commands that occur when an event is executed.
                        "outputCommands": [
                            {
                                "id": "<commandId>",
                                "name": "<commandName>",
                                "policyId": "<policyId>",
                                "policyName": "<policyName>"
                            }
                        ]
                    }
                ],

                "readModels": [
                    {
                        "id": "<readModelId>",
                        "name": "<readModelName>",
                        "queryParameters": [
                            {
                                "name": "<propertyName>",
                                ["type": "<propertyType>"],
                                ["isKey": true]
                            }
                        ],
                        "isMultipleResult": <true | false>
                    }
                ]
            }
        ]
    ]
}"""
    
    @staticmethod
    def get_summarized_es_value(es_value: Dict[str, Any], keys_to_exclude_filter: List[str] = None, es_alias_trans_manager: Optional[EsAliasTransManager] = None) -> Dict[str, Any]:
        """
        이벤트 스토밍 모델(es_value)을 요약된 형태로 변환하는 메소드입니다.
        특정 속성들을 제외하고 싶을 때 keys_to_exclude_filter를 사용하여 필터링할 수 있으며,
        ID 변환이 필요한 경우 es_alias_trans_manager를 통해 처리할 수 있습니다.
        
        Args:
            es_value: 이벤트 스토밍 모델 객체
            keys_to_exclude_filter: 제외할 속성 키 배열
            es_alias_trans_manager: ID 변환을 위한 매니저 객체
        
        Returns:
            요약된 이벤트 스토밍 모델 정보
        """
        if keys_to_exclude_filter is None:
            keys_to_exclude_filter = []
        
        bounded_contexts = [
            element for element in es_value.get("elements", {}).values()
            if element and element.get("_type") == 'org.uengine.modeling.model.BoundedContext'
        ]
        
        summarized_bounded_contexts = [
            ESValueSummarizeWithFilter.get_summarized_bounded_context_value(
                es_value, bounded_context, keys_to_exclude_filter, es_alias_trans_manager
            )
            for bounded_context in bounded_contexts
        ]
        
        return {
            "deletedProperties": keys_to_exclude_filter,
            "boundedContexts": summarized_bounded_contexts
        }
    
    @staticmethod
    def get_summarized_bounded_context_value(es_value: Dict[str, Any], bounded_context: Dict[str, Any], 
                                           keys_to_exclude_filter: List[str] = None, 
                                           es_alias_trans_manager: Optional[EsAliasTransManager] = None) -> Dict[str, Any]:
        """
        Bounded Context에 대한 요약된 정보를 반환합니다.
        
        Args:
            es_value: 이벤트 스토밍 모델 객체
            bounded_context: Bounded Context 객체
            keys_to_exclude_filter: 제외할 속성 키 배열
            es_alias_trans_manager: ID 변환을 위한 매니저 객체
            
        Returns:
            요약된 Bounded Context 정보
        """
        if keys_to_exclude_filter is None:
            keys_to_exclude_filter = []
        
        def get_conditional_value(keys, value):
            return value if not ESValueSummarizeWithFilter._check_key_filters(keys_to_exclude_filter, keys) else {}
        
        ESValueSummarizeWithFilter._restore_bounded_context_aggregates_properties(es_value, bounded_context)
        
        result = {}
        result.update(get_conditional_value(
            ["id", "boundedContext.id"], 
            {"id": ESValueSummarizeWithFilter._get_element_id_safely(bounded_context, es_alias_trans_manager)}
        ))
        
        result.update(get_conditional_value(
            ["name", "boundedContext.name"], 
            {"name": bounded_context.get("name", "")}
        ))
        
        result.update(get_conditional_value(
            ["actors", "boundedContext.actors"], 
            {"actors": ESValueSummarizeWithFilter.get_summarized_actor_value(
                es_value, bounded_context, keys_to_exclude_filter, es_alias_trans_manager
            )}
        ))
        
        aggregates = []
        for agg_ref in bounded_context.get("aggregates", []):
            agg_id = agg_ref.get("id")
            if agg_id and agg_id in es_value.get("elements", {}):
                aggregate = es_value["elements"][agg_id]
                aggregates.append(
                    ESValueSummarizeWithFilter.get_summarized_aggregate_value(
                        es_value, bounded_context, aggregate, keys_to_exclude_filter, es_alias_trans_manager
                    )
                )
        
        result.update(get_conditional_value(
            ["aggregates", "boundedContext.aggregates"], 
            {"aggregates": aggregates}
        ))
        
        return result
    
    @staticmethod
    def get_summarized_actor_value(es_value: Dict[str, Any], bounded_context: Dict[str, Any], 
                                 keys_to_exclude_filter: List[str] = None, 
                                 es_alias_trans_manager: Optional[EsAliasTransManager] = None) -> List[Dict[str, Any]]:
        """
        Actor에 대한 요약된 정보를 반환합니다.
        
        Args:
            es_value: 이벤트 스토밍 모델 객체
            bounded_context: Bounded Context 객체
            keys_to_exclude_filter: 제외할 속성 키 배열
            es_alias_trans_manager: ID 변환을 위한 매니저 객체
            
        Returns:
            요약된 Actor 정보 리스트
        """
        if keys_to_exclude_filter is None:
            keys_to_exclude_filter = []
        
        def get_conditional_value(keys, value):
            return value if not ESValueSummarizeWithFilter._check_key_filters(keys_to_exclude_filter, keys) else {}
        
        def get_unique_actors(actors, property_name):
            unique_actors = []
            for actor in actors:
                if not any(a.get(property_name) == actor.get(property_name) for a in unique_actors):
                    unique_actors.append(actor)
            return unique_actors
        
        actors = []
        for element in es_value.get("elements", {}).values():
            if (element and element.get("_type") == 'org.uengine.modeling.model.Actor' and
                element.get("boundedContext", {}).get("id") == bounded_context.get("id")):
                
                actor = {}
                actor.update(get_conditional_value(
                    ["id", "actors.id"], 
                    {"id": ESValueSummarizeWithFilter._get_element_id_safely(element, es_alias_trans_manager)}
                ))
                
                actor.update(get_conditional_value(
                    ["name", "actors.name"], 
                    {"name": element.get("name", "")}
                ))
                
                actors.append(actor)
        
        if not ESValueSummarizeWithFilter._check_key_filters(keys_to_exclude_filter, ["name", "actors.name"]):
            return get_unique_actors(actors, "name")
        
        if not ESValueSummarizeWithFilter._check_key_filters(keys_to_exclude_filter, ["id", "actors.id"]):
            return get_unique_actors(actors, "id")
        
        return actors
    
    @staticmethod
    def get_summarized_aggregate_value(es_value: Dict[str, Any], bounded_context: Dict[str, Any], 
                                     aggregate: Dict[str, Any], keys_to_exclude_filter: List[str] = None, 
                                     es_alias_trans_manager: Optional[EsAliasTransManager] = None) -> Dict[str, Any]:
        """
        Aggregate에 대한 요약된 정보를 반환합니다.
        
        Args:
            es_value: 이벤트 스토밍 모델 객체
            bounded_context: Bounded Context 객체
            aggregate: Aggregate 객체
            keys_to_exclude_filter: 제외할 속성 키 배열
            es_alias_trans_manager: ID 변환을 위한 매니저 객체
            
        Returns:
            요약된 Aggregate 정보
        """
        if keys_to_exclude_filter is None:
            keys_to_exclude_filter = []
        
        def get_conditional_value(keys, value):
            return value if not ESValueSummarizeWithFilter._check_key_filters(keys_to_exclude_filter, keys) else {}
        
        result = {}
        result.update(get_conditional_value(
            ["id", "aggregate.id"],
            {"id": ESValueSummarizeWithFilter._get_element_id_safely(aggregate, es_alias_trans_manager)}
        ))
        
        result.update(get_conditional_value(
            ["name", "aggregate.name"],
            {"name": aggregate.get("name", "")}
        ))
        
        if aggregate.get("aggregateRoot") and aggregate["aggregateRoot"].get("fieldDescriptors"):
            result.update(get_conditional_value(
                ["properties", "aggregate.properties"],
                {"properties": ESValueSummarizeWithFilter._get_summarized_field_descriptors(
                    aggregate["aggregateRoot"]["fieldDescriptors"]
                )}
            ))
        
        result.update(get_conditional_value(
            ["entities", "aggregate.entities"],
            {"entities": ESValueSummarizeWithFilter.get_summarized_entity_value(
                aggregate, keys_to_exclude_filter, es_alias_trans_manager
            )}
        ))
        
        result.update(get_conditional_value(
            ["enumerations", "aggregate.enumerations"],
            {"enumerations": ESValueSummarizeWithFilter.get_summarized_enumeration_value(
                aggregate, keys_to_exclude_filter, es_alias_trans_manager
            )}
        ))
        
        result.update(get_conditional_value(
            ["valueObjects", "aggregate.valueObjects"],
            {"valueObjects": ESValueSummarizeWithFilter.get_summarized_value_object_value(
                aggregate, keys_to_exclude_filter, es_alias_trans_manager
            )}
        ))
        
        result.update(get_conditional_value(
            ["commands", "aggregate.commands"],
            {"commands": ESValueSummarizeWithFilter.get_summarized_command_value(
                es_value, bounded_context, aggregate, keys_to_exclude_filter, es_alias_trans_manager
            )}
        ))
        
        result.update(get_conditional_value(
            ["events", "aggregate.events"],
            {"events": ESValueSummarizeWithFilter.get_summarized_event_value(
                es_value, bounded_context, aggregate, keys_to_exclude_filter, es_alias_trans_manager
            )}
        ))
        
        result.update(get_conditional_value(
            ["readModels", "aggregate.readModels"],
            {"readModels": ESValueSummarizeWithFilter.get_summarized_read_model_value(
                es_value, bounded_context, aggregate, keys_to_exclude_filter, es_alias_trans_manager
            )}
        ))
        
        return result
    
    @staticmethod
    def get_summarized_entity_value(aggregate: Dict[str, Any], keys_to_exclude_filter: List[str] = None, 
                                  es_alias_trans_manager: Optional[EsAliasTransManager] = None) -> List[Dict[str, Any]]:
        """
        Entity에 대한 요약된 정보를 반환합니다.
        
        Args:
            aggregate: Aggregate 객체
            keys_to_exclude_filter: 제외할 속성 키 배열
            es_alias_trans_manager: ID 변환을 위한 매니저 객체
            
        Returns:
            요약된 Entity 정보 리스트
        """
        if keys_to_exclude_filter is None:
            keys_to_exclude_filter = []
        
        def get_conditional_value(keys, value):
            return value if not ESValueSummarizeWithFilter._check_key_filters(keys_to_exclude_filter, keys) else {}
        
        if not ESValueSummarizeWithFilter._is_aggregate_have_elements(aggregate):
            return []
        
        summarized_entity_value = []
        for element in aggregate["aggregateRoot"]["entities"]["elements"].values():
            if (element and not element.get("isAggregateRoot") and
                element.get("_type") == 'org.uengine.uml.model.Class'):
                
                entity = {}
                entity.update(get_conditional_value(
                    ["id", "entities.id"],
                    {"id": ESValueSummarizeWithFilter._get_element_id_safely(element, es_alias_trans_manager)}
                ))
                
                entity.update(get_conditional_value(
                    ["name", "entities.name"],
                    {"name": element.get("name", "")}
                ))
                
                if element.get("fieldDescriptors"):
                    entity.update(get_conditional_value(
                        ["properties", "entities.properties"],
                        {"properties": ESValueSummarizeWithFilter._get_summarized_field_descriptors(
                            element["fieldDescriptors"],
                            lambda property_dict, field_descriptor: ESValueSummarizeWithFilter._set_foreign_property(
                                property_dict, field_descriptor, aggregate
                            )
                        )}
                    ))
                
                summarized_entity_value.append(entity)
        
        return summarized_entity_value
    
    @staticmethod
    def get_summarized_enumeration_value(aggregate: Dict[str, Any], keys_to_exclude_filter: List[str] = None, 
                                       es_alias_trans_manager: Optional[EsAliasTransManager] = None) -> List[Dict[str, Any]]:
        """
        Enumeration에 대한 요약된 정보를 반환합니다.
        
        Args:
            aggregate: Aggregate 객체
            keys_to_exclude_filter: 제외할 속성 키 배열
            es_alias_trans_manager: ID 변환을 위한 매니저 객체
            
        Returns:
            요약된 Enumeration 정보 리스트
        """
        if keys_to_exclude_filter is None:
            keys_to_exclude_filter = []
        
        def get_conditional_value(keys, value):
            return value if not ESValueSummarizeWithFilter._check_key_filters(keys_to_exclude_filter, keys) else {}
        
        if not ESValueSummarizeWithFilter._is_aggregate_have_elements(aggregate):
            return []
        
        summarized_enumeration_value = []
        for element in aggregate["aggregateRoot"]["entities"]["elements"].values():
            if element and element.get("_type") == 'org.uengine.uml.model.enum':
                enum = {}
                enum.update(get_conditional_value(
                    ["id", "enumerations.id"],
                    {"id": ESValueSummarizeWithFilter._get_element_id_safely(element, es_alias_trans_manager)}
                ))
                
                enum.update(get_conditional_value(
                    ["name", "enumerations.name"],
                    {"name": element.get("name", "")}
                ))
                
                if element.get("items"):
                    enum.update(get_conditional_value(
                        ["items", "enumerations.items"],
                        {"items": [item.get("value") for item in element["items"]]}
                    ))
                
                summarized_enumeration_value.append(enum)
        
        return summarized_enumeration_value
    
    @staticmethod
    def get_summarized_value_object_value(aggregate: Dict[str, Any], keys_to_exclude_filter: List[str] = None, 
                                        es_alias_trans_manager: Optional[EsAliasTransManager] = None) -> List[Dict[str, Any]]:
        """
        Value Object에 대한 요약된 정보를 반환합니다.
        
        Args:
            aggregate: Aggregate 객체
            keys_to_exclude_filter: 제외할 속성 키 배열
            es_alias_trans_manager: ID 변환을 위한 매니저 객체
            
        Returns:
            요약된 Value Object 정보 리스트
        """
        if keys_to_exclude_filter is None:
            keys_to_exclude_filter = []
        
        def get_conditional_value(keys, value):
            return value if not ESValueSummarizeWithFilter._check_key_filters(keys_to_exclude_filter, keys) else {}
        
        if not ESValueSummarizeWithFilter._is_aggregate_have_elements(aggregate):
            return []
        
        summarized_value_object_value = []
        for element in aggregate["aggregateRoot"]["entities"]["elements"].values():
            if element and element.get("_type") == 'org.uengine.uml.model.vo.Class':
                vo = {}
                vo.update(get_conditional_value(
                    ["id", "valueObjects.id"],
                    {"id": ESValueSummarizeWithFilter._get_element_id_safely(element, es_alias_trans_manager)}
                ))
                
                vo.update(get_conditional_value(
                    ["name", "valueObjects.name"],
                    {"name": element.get("name", "")}
                ))
                
                if element.get("fieldDescriptors"):
                    vo.update(get_conditional_value(
                        ["properties", "valueObjects.properties"],
                        {"properties": ESValueSummarizeWithFilter._get_summarized_field_descriptors(
                            element["fieldDescriptors"],
                            lambda property_dict, field_descriptor: ESValueSummarizeWithFilter._set_vo_foreign_property(
                                property_dict, field_descriptor, aggregate
                            )
                        )}
                    ))
                
                summarized_value_object_value.append(vo)
        
        return summarized_value_object_value
    
    @staticmethod
    def get_summarized_command_value(es_value: Dict[str, Any], bounded_context: Dict[str, Any], 
                                   aggregate: Dict[str, Any], keys_to_exclude_filter: List[str] = None, 
                                   es_alias_trans_manager: Optional[EsAliasTransManager] = None) -> List[Dict[str, Any]]:
        """
        Command에 대한 요약된 정보를 반환합니다.
        
        Args:
            es_value: 이벤트 스토밍 모델 객체
            bounded_context: Bounded Context 객체
            aggregate: Aggregate 객체
            keys_to_exclude_filter: 제외할 속성 키 배열
            es_alias_trans_manager: ID 변환을 위한 매니저 객체
            
        Returns:
            요약된 Command 정보 리스트
        """
        if keys_to_exclude_filter is None:
            keys_to_exclude_filter = []
        
        def get_conditional_value(keys, value):
            return value if not ESValueSummarizeWithFilter._check_key_filters(keys_to_exclude_filter, keys) else {}
        
        def get_output_events(element):
            events = []
            for relation in es_value.get("relations", {}).values():
                if (relation and relation.get("sourceElement", {}).get("id") == element.get("id") and 
                    relation.get("targetElement", {}).get("_type") == 'org.uengine.modeling.model.Event'):
                    
                    event = {}
                    event.update(get_conditional_value(
                        ["id", "commands.outputEvents.id"],
                        {"id": ESValueSummarizeWithFilter._get_element_id_safely(relation["targetElement"], es_alias_trans_manager)}
                    ))
                    
                    event.update(get_conditional_value(
                        ["name", "commands.outputEvents.name"],
                        {"name": relation["targetElement"].get("name", "")}
                    ))
                    
                    events.append(event)
            
            return events
        
        summarized_command_value = []
        for element in es_value.get("elements", {}).values():
            if (element and element.get("_type") == 'org.uengine.modeling.model.Command' and
                element.get("boundedContext", {}).get("id") == bounded_context.get("id") and
                element.get("aggregate", {}).get("id") == aggregate.get("id")):
                
                command = {}
                command.update(get_conditional_value(
                    ["id", "commands.id"],
                    {"id": ESValueSummarizeWithFilter._get_element_id_safely(element, es_alias_trans_manager)}
                ))
                
                command.update(get_conditional_value(
                    ["name", "commands.name"],
                    {"name": element.get("name", "")}
                ))
                
                api_verb = "POST"
                if element.get("restRepositoryInfo") and element["restRepositoryInfo"].get("method"):
                    api_verb = element["restRepositoryInfo"]["method"]
                
                command.update(get_conditional_value(
                    ["api_verb", "commands.api_verb"],
                    {"api_verb": api_verb}
                ))
                
                command.update(get_conditional_value(
                    ["isRestRepository", "commands.isRestRepository"],
                    {"isRestRepository": True if element.get("isRestRepository") else False}
                ))
                
                if element.get("fieldDescriptors"):
                    command.update(get_conditional_value(
                        ["properties", "commands.properties"],
                        {"properties": ESValueSummarizeWithFilter._get_summarized_field_descriptors(element["fieldDescriptors"])}
                    ))
                else:
                    command.update(get_conditional_value(
                        ["properties", "commands.properties"],
                        {"properties": []}
                    ))
                
                command.update(get_conditional_value(
                    ["outputEvents", "commands.outputEvents"],
                    {"outputEvents": get_output_events(element)}
                ))
                
                summarized_command_value.append(command)
        
        return summarized_command_value
    
    @staticmethod
    def get_summarized_event_value(es_value: Dict[str, Any], bounded_context: Dict[str, Any], 
                                 aggregate: Dict[str, Any], keys_to_exclude_filter: List[str] = None, 
                                 es_alias_trans_manager: Optional[EsAliasTransManager] = None) -> List[Dict[str, Any]]:
        """
        Event에 대한 요약된 정보를 반환합니다.
        
        Args:
            es_value: 이벤트 스토밍 모델 객체
            bounded_context: Bounded Context 객체
            aggregate: Aggregate 객체
            keys_to_exclude_filter: 제외할 속성 키 배열
            es_alias_trans_manager: ID 변환을 위한 매니저 객체
            
        Returns:
            요약된 Event 정보 리스트
        """
        if keys_to_exclude_filter is None:
            keys_to_exclude_filter = []
        
        def get_conditional_value(keys, value):
            return value if not ESValueSummarizeWithFilter._check_key_filters(keys_to_exclude_filter, keys) else {}
        
        def get_relations_for_type(source_element, target_type):
            return [
                relation for relation in es_value.get("relations", {}).values()
                if relation and relation.get("sourceElement", {}).get("id") == source_element.get("id") and 
                   relation.get("targetElement", {}).get("_type") == target_type
            ]
        
        def get_output_commands(element):
            commands = []
            for policy_relation in get_relations_for_type(element, "org.uengine.modeling.model.Policy"):
                policy_id = policy_relation.get("targetElement", {}).get("id")
                if not policy_id or policy_id not in es_value.get("elements", {}):
                    continue
                
                target_policy = es_value["elements"][policy_id]
                
                for command_relation in get_relations_for_type(target_policy, "org.uengine.modeling.model.Command"):
                    command = {}
                    command.update(get_conditional_value(
                        ["id", "events.outputCommands.id"],
                        {"id": ESValueSummarizeWithFilter._get_element_id_safely(command_relation["targetElement"], es_alias_trans_manager)}
                    ))
                    
                    command.update(get_conditional_value(
                        ["name", "events.outputCommands.name"],
                        {"name": command_relation["targetElement"].get("name", "")}
                    ))
                    
                    command.update(get_conditional_value(
                        ["id", "events.outputCommands.policyId"],
                        {"policyId": ESValueSummarizeWithFilter._get_element_id_safely(target_policy, es_alias_trans_manager)}
                    ))
                    
                    command.update(get_conditional_value(
                        ["name", "events.outputCommands.policyName"],
                        {"policyName": target_policy.get("name", "")}
                    ))
                    
                    commands.append(command)
            
            return commands
        
        summarized_event_value = []
        for element in es_value.get("elements", {}).values():
            if (element and element.get("_type") == 'org.uengine.modeling.model.Event' and
                element.get("boundedContext", {}).get("id") == bounded_context.get("id") and
                element.get("aggregate", {}).get("id") == aggregate.get("id")):
                
                event = {}
                event.update(get_conditional_value(
                    ["id", "events.id"],
                    {"id": ESValueSummarizeWithFilter._get_element_id_safely(element, es_alias_trans_manager)}
                ))
                
                event.update(get_conditional_value(
                    ["name", "events.name"],
                    {"name": element.get("name", "")}
                ))
                
                if element.get("fieldDescriptors"):
                    event.update(get_conditional_value(
                        ["properties", "events.properties"],
                        {"properties": ESValueSummarizeWithFilter._get_summarized_field_descriptors(element["fieldDescriptors"])}
                    ))
                else:
                    event.update(get_conditional_value(
                        ["properties", "events.properties"],
                        {"properties": []}
                    ))
                
                event.update(get_conditional_value(
                    ["outputCommands", "events.outputCommands"],
                    {"outputCommands": get_output_commands(element)}
                ))
                
                summarized_event_value.append(event)
        
        return summarized_event_value
    
    @staticmethod
    def get_summarized_read_model_value(es_value: Dict[str, Any], bounded_context: Dict[str, Any], 
                                      aggregate: Dict[str, Any], keys_to_exclude_filter: List[str] = None, 
                                      es_alias_trans_manager: Optional[EsAliasTransManager] = None) -> List[Dict[str, Any]]:
        """
        Read Model에 대한 요약된 정보를 반환합니다.
        
        Args:
            es_value: 이벤트 스토밍 모델 객체
            bounded_context: Bounded Context 객체
            aggregate: Aggregate 객체
            keys_to_exclude_filter: 제외할 속성 키 배열
            es_alias_trans_manager: ID 변환을 위한 매니저 객체
            
        Returns:
            요약된 Read Model 정보 리스트
        """
        if keys_to_exclude_filter is None:
            keys_to_exclude_filter = []
        
        def get_conditional_value(keys, value):
            return value if not ESValueSummarizeWithFilter._check_key_filters(keys_to_exclude_filter, keys) else {}
        
        summarized_read_model_value = []
        for element in es_value.get("elements", {}).values():
            if (element and element.get("_type") == "org.uengine.modeling.model.View" and
                element.get("boundedContext", {}).get("id") == bounded_context.get("id") and
                element.get("aggregate", {}).get("id") == aggregate.get("id")):
                
                read_model = {}
                read_model.update(get_conditional_value(
                    ["id", "readModels.id"],
                    {"id": ESValueSummarizeWithFilter._get_element_id_safely(element, es_alias_trans_manager)}
                ))
                
                read_model.update(get_conditional_value(
                    ["name", "readModels.name"],
                    {"name": element.get("name", "")}
                ))
                
                if element.get("queryParameters"):
                    read_model.update(get_conditional_value(
                        ["properties", "readModels.properties"],
                        {"queryParameters": ESValueSummarizeWithFilter._get_summarized_field_descriptors(element["queryParameters"])}
                    ))
                else:
                    read_model.update(get_conditional_value(
                        ["properties", "readModels.properties"],
                        {"queryParameters": []}
                    ))
                
                read_model.update(get_conditional_value(
                    ["isMultipleResult", "readModels.isMultipleResult"],
                    {"isMultipleResult": True if element.get("isMultipleResult") else False}
                ))
                
                summarized_read_model_value.append(read_model)
        
        return summarized_read_model_value
    
    @staticmethod
    def _restore_bounded_context_aggregates_properties(es_value: Dict[str, Any], bounded_context: Dict[str, Any]) -> None:
        """
        주어진 BoundedContext에서 agggregates 속성이 없을 경우를 대비해서, 주어진 이벤트스토밍 값을 통해서 복원
        
        Args:
            es_value: 이벤트 스토밍 모델 객체
            bounded_context: Bounded Context 객체
        """
        bounded_context["aggregates"] = []
        
        for element in es_value.get("elements", {}).values():
            if (element and element.get("_type") == "org.uengine.modeling.model.Aggregate" and
                element.get("boundedContext") and element["boundedContext"].get("id") == bounded_context.get("id")):
                bounded_context["aggregates"].append({"id": element.get("id")})
    
    @staticmethod
    def _get_summarized_field_descriptors(field_descriptors: List[Dict[str, Any]], on_after_create_property: Callable = None) -> List[Dict[str, Any]]:
        """
        필드 설명자에 대한 요약된 정보를 반환합니다.
        
        Args:
            field_descriptors: 필드 설명자 리스트
            on_after_create_property: 속성 생성 후 호출될 콜백 함수
            
        Returns:
            요약된 필드 설명자 정보 리스트
        """
        properties = []
        
        for field_descriptor in field_descriptors:
            property_dict = {
                "name": field_descriptor.get("name", "")
            }
            
            class_name = field_descriptor.get("className", "").lower()
            if not class_name.endswith("string"):
                property_dict["type"] = field_descriptor.get("className", "")
            
            if field_descriptor.get("isKey"):
                property_dict["isKey"] = True
            
            if on_after_create_property:
                on_after_create_property(property_dict, field_descriptor)
            
            properties.append(property_dict)
        
        return properties
    
    @staticmethod
    def _set_foreign_property(property_dict: Dict[str, Any], field_descriptor: Dict[str, Any], aggregate: Dict[str, Any]) -> None:
        """
        Entity의 외래 속성 설정
        
        Args:
            property_dict: 속성 사전
            field_descriptor: 필드 설명자
            aggregate: Aggregate 객체
        """
        if field_descriptor.get("className", "").lower() == aggregate.get("name", "").lower():
            property_dict["isForeignProperty"] = True
    
    @staticmethod
    def _set_vo_foreign_property(property_dict: Dict[str, Any], field_descriptor: Dict[str, Any], aggregate: Dict[str, Any]) -> None:
        """
        Value Object의 외래 속성 설정
        
        Args:
            property_dict: 속성 사전
            field_descriptor: 필드 설명자
            aggregate: Aggregate 객체
        """
        if field_descriptor.get("className", "").lower() == aggregate.get("name", "").lower():
            property_dict["isForeignProperty"] = True
        
        if field_descriptor.get("referenceClass"):
            property_dict["referencedAggregateName"] = field_descriptor.get("referenceClass")
            property_dict["isForeignProperty"] = True
    
    @staticmethod
    def _check_key_filters(keys_to_exclude_filter: List[str], values_to_check: List[str]) -> bool:
        """
        주어진 키들이 필터에 포함되어 있는지 확인합니다.
        
        Args:
            keys_to_exclude_filter: 제외할 속성 키 배열
            values_to_check: 확인할 값 배열
            
        Returns:
            필터에 포함되어 있으면 True, 아니면 False
        """
        for key in keys_to_exclude_filter:
            if key in values_to_check:
                return True
        
        return False
    
    @staticmethod
    def _get_element_id_safely(element: Dict[str, Any], es_alias_trans_manager: Optional[EsAliasTransManager] = None) -> str:
        """
        엘리먼트의 ID를 안전하게 가져옵니다.
        
        Args:
            element: 엘리먼트 객체
            es_alias_trans_manager: ID 변환을 위한 매니저 객체
            
        Returns:
            엘리먼트 ID
        """
        if es_alias_trans_manager:
            return es_alias_trans_manager.get_element_alias_safely(element)
        
        if element.get("id"):
            return element["id"]
        
        if element.get("elementView") and element["elementView"].get("id"):
            return element["elementView"]["id"]
        
        return element.get("id", "")
    
    @staticmethod
    def _is_aggregate_have_elements(aggregate: Dict[str, Any]) -> bool:
        """
        Aggregate가 하위 엘리먼트를 가지고 있는지 확인합니다.
        
        Args:
            aggregate: Aggregate 객체
            
        Returns:
            하위 엘리먼트가 있으면 True, 없으면 False
        """
        return (aggregate.get("aggregateRoot") and 
                aggregate["aggregateRoot"].get("entities") and 
                aggregate["aggregateRoot"]["entities"].get("elements"))
