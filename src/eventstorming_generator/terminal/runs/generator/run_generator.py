from .run_assign_fields_to_actions_generator import run_assign_fields_to_actions_generator
from .run_create_aggregate_actions_by_function import run_create_aggregate_actions_by_function
from .run_create_aggregate_class_id_by_drafts import run_create_aggregate_class_id_by_drafts
from .run_create_command_actions_by_function import run_create_command_actions_by_function
from .run_create_command_wire_frame import run_create_command_wire_frame
from .run_create_element_names_by_drafts import run_create_element_names_by_drafts
from .run_create_gwt_generator_by_function import run_create_gwt_generator_by_function
from .run_create_policy_actions_by_function import run_create_policy_actions_by_function
from .run_create_read_model_wire_frame import run_create_read_model_wire_frame
from .run_es_value_summary_generator import run_es_value_summary_generator

run_generator_registry = {
    "AssignFieldsToActionsGenerator": {
        "handler": run_assign_fields_to_actions_generator,
        "description": "AssignFieldsToActionsGenerator를 즉시 실행",
        "usage": "run runGenerator AssignFieldsToActionsGenerator"
    },
    "CreateAggregateActionsByFunction": {
        "handler": run_create_aggregate_actions_by_function,
        "description": "CreateAggregateActionsByFunction를 즉시 실행",
        "usage": "run runGenerator CreateAggregateActionsByFunction"
    },
    "CreateAggregateClassIdByDrafts": {
        "handler": run_create_aggregate_class_id_by_drafts,
        "description": "CreateAggregateClassIdByDrafts를 즉시 실행",
        "usage": "run runGenerator CreateAggregateClassIdByDrafts"
    },
    "CreateCommandActionsByFunction": {
        "handler": run_create_command_actions_by_function,
        "description": "CreateCommandActionsByFunction를 즉시 실행",
        "usage": "run runGenerator CreateCommandActionsByFunction"
    },
    "CreateCommandWireFrame": {
        "handler": run_create_command_wire_frame,
        "description": "CreateCommandWireFrame를 즉시 실행",
        "usage": "run runGenerator CreateCommandWireFrame"
    },
    "CreateElementNamesByDrafts": {
        "handler": run_create_element_names_by_drafts,
        "description": "CreateElementNamesByDrafts를 즉시 실행",
        "usage": "run runGenerator CreateElementNamesByDrafts"
    },
    "CreateGWTGeneratorByFunction": {
        "handler": run_create_gwt_generator_by_function,
        "description": "CreateGWTGeneratorByFunction를 즉시 실행",
        "usage": "run runGenerator CreateGWTGeneratorByFunction"
    },
    "CreatePolicyActionsByFunction": {
        "handler": run_create_policy_actions_by_function,
        "description": "CreatePolicyActionsByFunction를 즉시 실행",
        "usage": "run runGenerator CreatePolicyActionsByFunction"
    },
    "CreateReadModelWireFrame": {
        "handler": run_create_read_model_wire_frame,
        "description": "CreateReadModelWireFrame를 즉시 실행",
        "usage": "run runGenerator CreateReadModelWireFrame"
    },
    "ESValueSummaryGenerator": {
        "handler": run_es_value_summary_generator,
        "description": "ESValueSummaryGenerator를 즉시 실행",
        "usage": "run runGenerator ESValueSummaryGenerator"
    }
}

def run_generator(command_args):
    generator_name = command_args[0]

    generator = run_generator_registry.get(generator_name, None)
    if not generator:
        print(f"유효하지 않은 제너레이터 명령어입니다. {generator_name}")
        return False
    return generator["handler"](command_args)