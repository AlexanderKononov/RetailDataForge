from typing import List, Type
from pydantic import BaseModel, Field, ValidationError
from data_schema_config.column_schema import BaseColumnConfig  # adjust import to your structure

class TableSchema(BaseModel):
    columns: List[BaseColumnConfig] = Field(default_factory=list)
    num_rows: int = 100

    def add_col_config(self, config: BaseColumnConfig):
        if any(c.name == config.name for c in self.columns):
            raise ValueError(f"Column '{config.name}' already exists.")
        self.columns.append(config)

    def remove_column(self, name: str):
        self.columns = [col for col in self.columns if col.name != name]

    def get_columns(self) -> List[BaseColumnConfig]:
        return self.columns

    def clear(self):
        self.columns = []

    def get_column_by_name(self, name: str) -> BaseColumnConfig | None:
        for col in self.columns:
            if col.name == name:
                return col
        return None
    
    def set_num_rows(self, num: int):
        if num < 1:
            raise ValueError("Row count must be at least 1.")
        self.num_rows = num

    def get_num_rows(self) -> int:
        return self.num_rows