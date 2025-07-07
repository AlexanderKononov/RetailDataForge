from typing import List
from column_schema import ColumnConfig

class TableSchema:
    def __init__(self):
        self.columns: List[ColumnConfig] = []

    def add_column(self, name: str, col_type: str):
        column = ColumnConfig(name=name, type=col_type)
        if any(c.name == column.name for c in self.columns):
            raise ValueError(f"Column '{column.name}' already exists.")
        self.columns.append(column)

    def remove_column(self, name: str):
        self.columns = [col for col in self.columns if col.name != name]

    def get_columns(self) -> List[ColumnConfig]:
        return self.columns

    def as_dict_list(self) -> List[dict]:
        return [col.dict() for col in self.columns]

    def clear(self):
        self.columns = []