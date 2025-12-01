from ....utils import TextChunker
from ..mocks import common_requirements

def execute_text_chunker_util(requirements_type:str="it_system_requirements"):
    requirements = common_requirements.get(requirements_type)
    chunks = TextChunker.split_into_chunks_by_line(requirements, 25000, 2000)
    return chunks
