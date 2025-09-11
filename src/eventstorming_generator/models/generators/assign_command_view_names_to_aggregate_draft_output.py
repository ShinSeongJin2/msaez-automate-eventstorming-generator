from pydantic import Field
from typing import List
from ..base import BaseModelWithItem

class ExtractedCommand(BaseModelWithItem):
    """Represents an extracted command from site map"""
    referencedId: str = Field(description="ID of the site map element that this command is referenced from")
    aggregateName: str = Field(description="Name of the aggregate this command belongs to")
    commandName: str = Field(description="Name of the extracted command")

class ExtractedReadModel(BaseModelWithItem):
    """Represents an extracted read model from site map"""
    referencedId: str = Field(description="ID of the site map element that this read model is referenced from")
    aggregateName: str = Field(description="Name of the aggregate this read model belongs to")
    readModelName: str = Field(description="Name of the extracted read model")

class ExtractionResult(BaseModelWithItem):
    """Contains all extracted commands and read models"""
    extractedCommands: List[ExtractedCommand] = Field(description="List of commands extracted from site map")
    extractedReadModels: List[ExtractedReadModel] = Field(description="List of read models extracted from site map")

class AssignCommandViewNamesToAggregateDraftOutput(BaseModelWithItem):
    """Output model for assigning command and view names to aggregate drafts"""
    inference: str = Field(description="Detailed reasoning and analysis for the extracted commands and read models")
    result: ExtractionResult = Field(description="The extracted commands and read models from site map")