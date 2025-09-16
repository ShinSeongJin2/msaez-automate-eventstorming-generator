import base64
from eventstorming_generator.models import State, LogModel
import traceback

class LogUtil:
    @staticmethod
    def add_log(state: State, message: str, level: str = "info"):
        if len(state.outputs.logs) >= 500:
            state.outputs.logs.pop(0)
        state.outputs.logs.append(LogModel(message=message, level=level))

    @staticmethod
    def add_info_log(state: State, message: str):
        LogUtil.add_log(state, message, "info")

    @staticmethod
    def add_error_log(state: State, message: str):
        LogUtil.add_log(state, message, "error")
    
    @staticmethod
    def add_exception_object_log(state: State, message: str, exception: Exception):
        base64_traceback = base64.b64encode(traceback.format_exc().encode()).decode()
        LogUtil.add_log(state, f"{message}: {exception}\nTraceback Code: {base64_traceback}", "error")

    @staticmethod
    def add_warning_log(state: State, message: str):
        LogUtil.add_log(state, message, "warning")