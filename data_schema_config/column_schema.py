from pydantic import BaseModel, Field, ValidationError, conint, constr
from enum import Enum
from typing import Optional, Union
import streamlit as st

class ColumnType(str, Enum):
    INTEGER = "Integer"
    FLOAT = "Float"
    STRING = "String"
    BOOLEAN = "Boolean"


class BaseColumnConfig(BaseModel):
    name: str
    type: ColumnType

    @classmethod
    def select_and_configure_column(cls, key_prefix="add_column") -> Optional["BaseColumnConfig"]:
        col_type_str = st.selectbox(
            "Column Type", 
            [t.value for t in ColumnType], 
            key=f"{key_prefix}_type"
        )
        try:
            col_type = ColumnType(col_type_str)
        except ValueError:
            st.warning("Invalid column type.")
            return None

        config_cls = column_type_to_config_class.get(col_type)
        if not config_cls:
            st.warning(f"No configuration form for column type: {col_type}")
            return None

        return config_cls.from_form(key_prefix=f"{key_prefix}_{col_type.value.lower()}")
    

class IntegerColumnConfig(BaseColumnConfig):
    type: ColumnType = ColumnType.INTEGER
    min_value: int = 0
    max_value: int = 100

    @classmethod
    def from_form(cls, key_prefix="int_cfg") -> Optional["IntegerColumnConfig"]:
        with st.form(f"{key_prefix}_form", clear_on_submit=True, border=False):
            name = st.text_input("Column Name", key=f"{key_prefix}_name")
            min_val = st.number_input("Minimum Value", value=0, key=f"{key_prefix}_min")
            max_val = st.number_input("Maximum Value", value=100, key=f"{key_prefix}_max")
            submit = st.form_submit_button("Add Column")

            if submit and name.strip():
                return cls(name=name.strip(), min_value=min_val, max_value=max_val)
        return None


class StringColumnConfig(BaseColumnConfig):
    type: ColumnType = ColumnType.STRING
    max_length: int = 20

    @classmethod
    def from_form(cls, key_prefix="str_cfg") -> Optional["StringColumnConfig"]:
        with st.form(f"{key_prefix}_form", clear_on_submit=True, border=False):
            name = st.text_input("Column Name", key=f"{key_prefix}_name")
            max_len = st.number_input("Max String Length", value=20, min_value=1, key=f"{key_prefix}_max_len")
            submit = st.form_submit_button("Add Column")

            if submit and name.strip():
                return cls(name=name.strip(), max_length=max_len)
        return None
    
column_type_to_config_class = {
    ColumnType.INTEGER: IntegerColumnConfig,
    ColumnType.STRING: StringColumnConfig,
    # Add others...
}