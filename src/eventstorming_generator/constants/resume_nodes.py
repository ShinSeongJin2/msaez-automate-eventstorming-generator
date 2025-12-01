from dataclasses import dataclass

@dataclass(frozen=True)
class RootGraphNode:
    CREATE_BOUNDED_CONTEXTS: str = "create_bounded_contexts"
    CREATE_CONTEXT_MAPPING: str = "create_context_mapping"
    CREATE_DRAFT_BY_FUNCTION: str = "create_draft_by_function"
    CREATE_BOUNDED_CONTEXTS_TO_ES_VALUE: str = "create_bounded_contexts_to_es_value"
    CREATE_AGGREGATES: str = "create_aggregates"
    CREATE_CLASS_ID: str = "create_class_id"
    CREATE_ELEMENT_NAMES: str = "create_element_names"
    CREATE_COMMAND_ACTIONS: str = "create_command_actions"
    CREATE_POLICY_ACTIONS: str = "create_policy_actions"
    CREATE_GWT: str = "create_gwt"
    CREATE_UI_COMPONENTS: str = "create_ui_components"
    COMPLETE: str = "complete"

@dataclass(frozen=True)
class BatchProcessNodes:
    PREPARE: str = "prepare"
    SELECT_BATCH: str = "select_batch"
    EXECUTE_PARALLEL: str = "execute_parallel"
    COLLECT_RESULTS: str = "collect_results"
    MERGE: str = "merge"
    COMPLETE: str = "complete"

@dataclass(frozen=True)
class ElementNamesNodes:
    PREPARE: str = "prepare"
    SELECT_NEXT: str = "select_next"
    PREPROCESS: str = "preprocess"
    GENERATE: str = "generate"
    POSTPROCESS: str = "postprocess"
    VALIDATE: str = "validate"
    COMPLETE: str = "complete"

@dataclass(frozen=True)
class ResumeNodes:
    ROOT_GRAPH = RootGraphNode()
    CREATE_BOUNDED_CONTEXTS = BatchProcessNodes()
    CREATE_CONTEXT_MAPPING = BatchProcessNodes()
    CREATE_DRAFT_BY_FUNCTION = BatchProcessNodes()
    CREATE_AGGREGATES = BatchProcessNodes()
    CREATE_CLASS_ID = BatchProcessNodes()
    CREATE_ELEMENT_NAMES = ElementNamesNodes()
    CREATE_COMMAND_ACTIONS = BatchProcessNodes()
    CREATE_POLICY_ACTIONS = BatchProcessNodes()
    CREATE_GWT = BatchProcessNodes()
    CREATE_UI_COMPONENTS = BatchProcessNodes()

RESUME_NODES = ResumeNodes()