from typing import Dict, Callable

RunableLogics = Dict[str, Callable]
RunableLogicsCategories = Dict[str, RunableLogics]

__all__ = [
    "RunableLogics",
    "RunableLogicsCategories"
]