from ..base import BaseModelWithItem

class TextChunkModel(BaseModelWithItem):
    text: str = ""
    start_line: int = 0