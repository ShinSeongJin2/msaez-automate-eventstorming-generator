from typing import List, Dict, Callable

RunableLogics = Dict[str, Callable]
RunableLogicsCategories = Dict[str, RunableLogics]

LineNumberRange = List[int]
RequirementIndexMapping = Dict[int, int]

__all__ = [
    "RunableLogics",
    "RunableLogicsCategories",
    "LineNumberRange",
    "RequirementIndexMapping"
]