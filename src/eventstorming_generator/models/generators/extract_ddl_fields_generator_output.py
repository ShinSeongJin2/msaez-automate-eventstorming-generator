from pydantic import Field
from typing import List
from ..base import BaseModelWithItem

class DDLFieldResult(BaseModelWithItem):
    ddl_fields: List[str] = Field(default_factory=list, description="List of field names extracted from the DDL.")

class ExtractDDLFieldsGeneratorOutput(BaseModelWithItem):
    """Structured Output Model of the ExtractDDLFieldsGenerator"""
    inference: str = Field(..., description="Reasoning for the extracted fields.") 
    result: DDLFieldResult = Field(..., description="The extracted fields from the DDL.")