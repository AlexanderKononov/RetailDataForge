from typing import List, Type
from data_schema_config.column_schema import BaseColumnConfig  # adjust import to your structure

class TableSchema:
    def __init__(self):
        self.columns: List[BaseColumnConfig] = []

    def add_col_config(self, config: BaseColumnConfig):
        if any(c.name == config.name for c in self.columns):
            raise ValueError(f"Column '{config.name}' already exists.")
        self.columns.append(config)

    def remove_column(self, name: str):
        self.columns = [col for col in self.columns if col.name != name]

    def get_columns(self) -> List[BaseColumnConfig]:
        return self.columns

    def as_dict_list(self) -> List[dict]:
        return [col.dict() for col in self.columns]

    def clear(self):
        self.columns = []

    def get_column_by_name(self, name: str) -> BaseColumnConfig | None:
        for col in self.columns:
            if col.name == name:
                return col
        return None