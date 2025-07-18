from pydantic import BaseModel, Field, ValidationError, conint, constr
from enum import Enum
import numpy as np
from typing import Optional, List, Union
import streamlit as st
from faker import Faker
from data_schema_config.base_column_configs import (
    ColumnType, 
    ColumnConfig, 
    ColumnTypeGroup
)

fake = Faker()

class BooleanColumnConfig(ColumnConfig):
    type: ColumnType = ColumnType.BOOLEAN
    format: str = "Categorical"

    true_probability: float = 0.5  # Probability of generating True

    @classmethod
    def from_form(cls, key_prefix="bool_cfg") -> Optional["BooleanColumnConfig"]:
        with st.form(f"{key_prefix}_form", clear_on_submit=True, border=False):
            name = st.text_input("Column Name", key=f"{key_prefix}_name")
            probability = st.slider(
                "Probability of True", min_value=0.0, max_value=1.0, value=0.5, step=0.01, key=f"{key_prefix}_prob"
            )
            submit = st.form_submit_button("Add Column")

            if submit and name.strip():
                return cls(name=name.strip(), true_probability=probability)
        return None

    @classmethod
    def generate_data(cls, config: "BooleanColumnConfig", n_rows: int) -> List[bool]:
        return np.random.choice(
            [True, False], size=n_rows, p=[config.true_probability, 1 - config.true_probability]
        ).tolist()
    

class CountryColumnConfig(ColumnConfig):
    type: ColumnType = ColumnType.COUNTRY
    format: str = "Categorical"

    @classmethod
    def from_form(cls, key_prefix="country_cfg") -> Optional["CountryColumnConfig"]:
        with st.form(f"{key_prefix}_form", clear_on_submit=True, border=False):
            name = st.text_input("Column Name (e.g., 'Country')", key=f"{key_prefix}_name")
            submit = st.form_submit_button("Add Column")
            if submit and name.strip():
                return cls(name=name.strip())
        return None

    @classmethod
    def generate_data(cls, config: "CountryColumnConfig", n_rows: int) -> List[str]:
        return [fake.country() for _ in range(n_rows)]

class CityColumnConfig(ColumnConfig):
    type: ColumnType = ColumnType.CITY
    format: str = "Categorical"

    @classmethod
    def from_form(cls, key_prefix="city_cfg") -> Optional["CityColumnConfig"]:
        with st.form(f"{key_prefix}_form", clear_on_submit=True, border=False):
            name = st.text_input("Column Name (e.g., 'City')", key=f"{key_prefix}_name")
            submit = st.form_submit_button("Add Column")
            if submit and name.strip():
                return cls(name=name.strip())
        return None

    @classmethod
    def generate_data(cls, config: "CityColumnConfig", n_rows: int) -> List[str]:
        return [fake.city() for _ in range(n_rows)]

