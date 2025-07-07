from pydantic import BaseModel, Field
from enum import Enum

class ColumnType(str, Enum):
    INTEGER = "Integer"
    FLOAT = "Float"
    STRING = "String"
    BOOLEAN = "Boolean"


class ColumnConfig(BaseModel):
    name: str = Field(..., min_length=1, description="Name of the column")
    type: ColumnType

    def __str__(self):
        return f"{self.name} ({self.type})"