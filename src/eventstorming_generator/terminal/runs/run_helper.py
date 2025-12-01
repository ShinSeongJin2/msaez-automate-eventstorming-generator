from typing import Any, List, Dict, Callable
import json

from ..terminal_helper import TerminalHelper
from ...config import Config
from ...systems import DatabaseFactory, MemoryDBSystem
from ...models import State
from ...utils import EsAliasTransManager, ESValueSummarizeWithFilter
from ...constants import RG

class RunHelper:
    @staticmethod
    def save_es_summarize_result_to_temp_file(es_value: Any, file_name: str, directory: str = ".temp") -> None:
        es_alias_trans_manager = EsAliasTransManager(es_value)
        summarized_es_value = ESValueSummarizeWithFilter.get_summarized_es_value(es_value, [], es_alias_trans_manager)
        TerminalHelper.save_dict_to_temp_file(
            summarized_es_value, f"{file_name}_es_value_summarized", directory
        ) 

    @staticmethod
    def check_error_logs_from_state(state: State, file_name: str, directory: str = ".temp") -> None:
        logs_to_check = state.outputs.logs

        error_logs = []
        for log in logs_to_check:
            if log.level == "error":
                error_logs.append(log)
        
        if len(error_logs) > 0:
            print(f"[!] Error logs found: {error_logs}")
            TerminalHelper.save_dict_to_temp_file(error_logs, f"{file_name}_error_logs", directory)
        else:
            print(f"[*] No error logs found")    

    @staticmethod
    def save_db_data_to_temp_file(file_name: str, directory: str = ".temp") -> None:
        if Config.get_db_type() == "memory":
            db_system: MemoryDBSystem = DatabaseFactory.get_db_system()
            db_data = db_system.get_all_data()
            TerminalHelper.save_dict_to_temp_file(db_data, file_name, directory)
    
    @staticmethod
    def save_state_by_after_stop_node(after_stop_node: str, state: State, run_name: str, directory: str = ".temp") -> None:
        RunHelper.check_error_logs_from_state(state, run_name, directory)

        if after_stop_node == RG.CREATE_BOUNDED_CONTEXTS:    
            TerminalHelper.save_dict_to_temp_file({
                "merged_bounded_contexts": [m.model_dump() for m in state.subgraphs.createBoundedContextByFunctionsModel.merged_bounded_contexts],
                "logs": state.outputs.logs,
                "totalSeconds": state.subgraphs.createBoundedContextByFunctionsModel.total_seconds
            }, run_name, directory)
        elif after_stop_node == RG.CREATE_CONTEXT_MAPPING:
            TerminalHelper.save_dict_to_temp_file({
                "boundedContextRequirements": state.inputs.draft.metadatas.boundedContextRequirements,
                "boundedContextRequirementIndexMapping": state.inputs.draft.metadatas.boundedContextRequirementIndexMapping,
                "logs": state.outputs.logs,
                "totalSeconds": state.subgraphs.createContextMappingModel.total_seconds
            }, run_name, directory)
        elif after_stop_node == RG.CREATE_DRAFT_BY_FUNCTION:
            TerminalHelper.save_dict_to_temp_file({
                "structures": state.inputs.draft.structures,
                "logs": state.outputs.logs,
                "totalSeconds": state.subgraphs.createDraftByFunctionModel.total_seconds
            }, run_name, directory)
        elif after_stop_node == RG.CREATE_AGGREGATES:
            TerminalHelper.save_dict_to_temp_file({
                "esValue": state.outputs.esValue,
                "logs": state.outputs.logs,
                "totalSeconds": state.subgraphs.createAggregateByFunctionsModel.total_seconds
            }, run_name, directory)
            RunHelper.save_es_summarize_result_to_temp_file(state.outputs.esValue, run_name, directory)
        elif after_stop_node == RG.CREATE_COMMAND_ACTIONS:
            TerminalHelper.save_dict_to_temp_file({
                "esValue": state.outputs.esValue,
                "logs": state.outputs.logs,
                "totalSeconds": state.subgraphs.createCommandActionsByFunctionModel.total_seconds
            }, run_name, directory)
            RunHelper.save_es_summarize_result_to_temp_file(state.outputs.esValue, run_name, directory)
        elif after_stop_node == RG.CREATE_POLICY_ACTIONS:
            TerminalHelper.save_dict_to_temp_file({
                "esValue": state.outputs.esValue,
                "logs": state.outputs.logs,
                "totalSeconds": state.subgraphs.createPolicyActionsByFunctionModel.total_seconds
            }, run_name, directory)
            RunHelper.save_es_summarize_result_to_temp_file(state.outputs.esValue, run_name, directory)
        elif after_stop_node == RG.COMPLETE:
            TerminalHelper.save_dict_to_temp_file({
                "esValue": state.outputs.esValue,
                "logs": state.outputs.logs
            }, run_name, directory)
            RunHelper.save_es_summarize_result_to_temp_file(state.outputs.esValue, run_name, directory)
        
        RunHelper.save_db_data_to_temp_file(f"{run_name}_db_data", directory)

    @staticmethod
    async def run_func_using_name(run_name_registry: Dict[str, Callable], result_handler: Callable):
        while True:
            print("--------------------------------")
            print("Available runs:")
            run_names = list(run_name_registry.keys())
            for idx, run_name in enumerate(run_names, start=1):
                print(f"{idx}. {run_name}")

            user_input = input("> Run name or number: ")
            if user_input == "exit":
                break

            # 번호로 입력된 경우 처리
            selected_run_name = None
            if user_input.isdigit():
                idx = int(user_input)
                if 1 <= idx <= len(run_names):
                    selected_run_name = run_names[idx - 1]
                else:
                    print(f"Invalid number: {user_input}. Please enter a number between 1 and {len(run_names)}")
                    continue
            # 이름으로 입력된 경우 처리
            elif user_input in run_name_registry:
                selected_run_name = user_input
            else:
                print(f"Run name: {user_input} not found")
                continue

            result = await run_name_registry[selected_run_name]()
            if result_handler:
                await result_handler(result, selected_run_name)
    
    @staticmethod
    def input_with_default(prompt: str, default: Any, type: str = "text") -> str:
        user_input = RunHelper.input_by_type(f"{prompt} [{default}]: ", type)
        if user_input == "":
            return default
        return user_input
    
    @staticmethod
    def input_by_type(prompt: str, type: str = "text") -> str:
        user_input = ""
        if type == "text":
            user_input = input(prompt).strip()
        elif type == "text_lines":
            print(prompt)
            user_input_lines: List[str] = []
            while True:
                line = input()
                if not line.strip():
                    break
                user_input_lines.append(line)
            user_input = "\n".join(user_input_lines).strip()
        elif type == "json":
            user_input = input(prompt).strip()
            if user_input:
                user_input = json.loads(user_input)
        else:
            raise ValueError(f"Invalid input type: {type}")
        return user_input