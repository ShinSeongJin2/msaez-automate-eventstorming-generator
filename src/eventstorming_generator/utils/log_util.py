import traceback

from eventstorming_generator.models import State, LogModel

class LogUtil:
    @staticmethod
    def add_log(state: State, message: str, level: str = "info"):
        state.outputs.logs.append(LogModel(message=message, level=level))

    @staticmethod
    def add_info_log(state: State, message: str):
        LogUtil.add_log(state, message, "info")

    @staticmethod
    def add_error_log(state: State, message: str):
        LogUtil.add_log(state, message, "error")
    
    @staticmethod
    def add_exception_object_log(state: State, message: str, exception: Exception):
        LogUtil.add_log(state, f"{message}: {exception} {traceback.format_exc()}", "error")

    @staticmethod
    def add_warning_log(state: State, message: str):
        LogUtil.add_log(state, message, "warning")