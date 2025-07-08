from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional
import streamlit as st
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
    
    @classmethod
    def from_form(cls, form_key: str = "column_form") -> Optional["ColumnConfig"]:
        """
        Displays a form to collect column config, and returns a ColumnConfig if submitted.
        """
        with st.form(form_key, clear_on_submit=True, border=False):
            col_name = st.text_input("Column Name", key=f"{form_key}_name")
            col_type = st.selectbox("Data Type", [col.value for col in ColumnType], key=f"{form_key}_type")
            submit = st.form_submit_button("Add Column")

            if submit:
                try:
                    config = cls(name=col_name.strip(), type=ColumnType(col_type))
                    return config
                except ValidationError as ve:
                    st.warning("Invalid input: " + "; ".join(e["msg"] for e in ve.errors()))
                except Exception as e:
                    st.error(f"Unexpected error: {str(e)}")
        return None