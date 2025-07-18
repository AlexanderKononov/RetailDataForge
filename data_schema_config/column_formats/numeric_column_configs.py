from pydantic import BaseModel, Field, ValidationError, conint, constr
from enum import Enum
import numpy as np
from typing import Optional, List, Union
import streamlit as st
from faker import Faker
from data_schema_config.base_column_configs import (
    ColumnType, 
    ColumnConfig, 
    register_column_config)


@register_column_config(ColumnType.INTEGER)
class IntegerColumnConfig(ColumnConfig):
    type: ColumnType = ColumnType.INTEGER
    format: str = "Numeric"
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
    
    @classmethod
    def generate_data(cls, config: "IntegerColumnConfig", n_rows: int) -> List[int]:
        return np.random.randint(config.min_value, config.max_value + 1, size=n_rows).tolist()

    
class FloatColumnConfig(ColumnConfig):
    type: ColumnType = ColumnType.FLOAT
    format: str = "Numeric"
    min_value: float = 0.0
    max_value: float = 1.0
    precision: int = 2  # Number of decimal places

    @classmethod
    def from_form(cls, key_prefix="float_cfg") -> Optional["FloatColumnConfig"]:
        with st.form(f"{key_prefix}_form", clear_on_submit=True, border=False):
            name = st.text_input("Column Name", key=f"{key_prefix}_name")
            min_val = st.number_input("Minimum Value", value=0.0, key=f"{key_prefix}_min")
            max_val = st.number_input("Maximum Value", value=1.0, key=f"{key_prefix}_max")
            precision = st.number_input("Decimal Precision", value=2, min_value=0, max_value=10, key=f"{key_prefix}_precision")
            submit = st.form_submit_button("Add Column")

            if submit and name.strip():
                return cls(name=name.strip(), min_value=min_val, max_value=max_val, precision=precision)
        return None

    @classmethod
    def generate_data(cls, config: "FloatColumnConfig", n_rows: int) -> List[float]:
        raw = np.random.uniform(config.min_value, config.max_value, size=n_rows)
        return np.round(raw, decimals=config.precision).tolist()
    