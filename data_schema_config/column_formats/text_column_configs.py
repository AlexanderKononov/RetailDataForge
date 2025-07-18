from pydantic import BaseModel, Field, ValidationError, conint, constr
from enum import Enum
import numpy as np
from typing import Optional, List, Union
import streamlit as st
from faker import Faker
from data_schema_config.base_column_configs import ColumnType, BaseColumnConfig, ColumnFormat

fake = Faker()

class StringColumnConfig(BaseColumnConfig):
    type: ColumnType = ColumnType.STRING
    format: ColumnFormat = ColumnFormat.STRING
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
    
    @classmethod
    def generate_data(cls, config: "StringColumnConfig", n_rows: int) -> List[str]:
        return [fake.word()[:config.max_length] for _ in range(n_rows)]
    

class PersonNameColumnConfig(BaseColumnConfig):
    type: ColumnType = ColumnType.PERSON_NAME
    format: ColumnFormat = ColumnFormat.STRING

    @classmethod
    def from_form(cls, key_prefix="person_name_cfg") -> Optional["PersonNameColumnConfig"]:
        with st.form(f"{key_prefix}_form", clear_on_submit=True, border=False):
            col_label = "Column Name (e.g., 'Full Name')"
            name = st.text_input(col_label, key=f"{key_prefix}_name")
            submit = st.form_submit_button("Add Column")

            if submit and name.strip():
                return cls(name=name.strip())
        return None

    @classmethod
    def generate_data(cls, config: "PersonNameColumnConfig", n_rows: int) -> List[str]:
        return [fake.name() for _ in range(n_rows)]
    
class FirstNameColumnConfig(BaseColumnConfig):
    type: ColumnType = ColumnType.FIRST_NAME
    format: ColumnFormat = ColumnFormat.STRING

    @classmethod
    def from_form(cls, key_prefix="first_name_cfg") -> Optional["FirstNameColumnConfig"]:
        with st.form(f"{key_prefix}_form", clear_on_submit=True, border=False):
            name = st.text_input("Column Name (e.g., 'First Name')", key=f"{key_prefix}_name")
            submit = st.form_submit_button("Add Column")
            if submit and name.strip():
                return cls(name=name.strip())
        return None

    @classmethod
    def generate_data(cls, config: "FirstNameColumnConfig", n_rows: int) -> List[str]:
        return [fake.first_name() for _ in range(n_rows)]
    
class LastNameColumnConfig(BaseColumnConfig):
    type: ColumnType = ColumnType.LAST_NAME
    format: ColumnFormat = ColumnFormat.STRING

    @classmethod
    def from_form(cls, key_prefix="last_name_cfg") -> Optional["LastNameColumnConfig"]:
        with st.form(f"{key_prefix}_form", clear_on_submit=True, border=False):
            name = st.text_input("Column Name (e.g., 'Last Name')", key=f"{key_prefix}_name")
            submit = st.form_submit_button("Add Column")
            if submit and name.strip():
                return cls(name=name.strip())
        return None

    @classmethod
    def generate_data(cls, config: "LastNameColumnConfig", n_rows: int) -> List[str]:
        return [fake.last_name() for _ in range(n_rows)]
    
class EmailColumnConfig(BaseColumnConfig):
    type: ColumnType = ColumnType.EMAIL
    format: ColumnFormat = ColumnFormat.STRING

    @classmethod
    def from_form(cls, key_prefix="email_cfg") -> Optional["EmailColumnConfig"]:
        with st.form(f"{key_prefix}_form", clear_on_submit=True, border=False):
            name = st.text_input("Column Name (e.g., 'Email')", key=f"{key_prefix}_name")
            submit = st.form_submit_button("Add Column")
            if submit and name.strip():
                return cls(name=name.strip())
        return None

    @classmethod
    def generate_data(cls, config: "EmailColumnConfig", n_rows: int) -> List[str]:
        return [fake.email() for _ in range(n_rows)]

class PhoneNumberColumnConfig(BaseColumnConfig):
    type: ColumnType = ColumnType.PHONE_NUMBER
    format: ColumnFormat = ColumnFormat.STRING

    @classmethod
    def from_form(cls, key_prefix="phone_cfg") -> Optional["PhoneNumberColumnConfig"]:
        with st.form(f"{key_prefix}_form", clear_on_submit=True, border=False):
            name = st.text_input("Column Name (e.g., 'Phone')", key=f"{key_prefix}_name")
            submit = st.form_submit_button("Add Column")
            if submit and name.strip():
                return cls(name=name.strip())
        return None

    @classmethod
    def generate_data(cls, config: "PhoneNumberColumnConfig", n_rows: int) -> List[str]:
        return [fake.phone_number() for _ in range(n_rows)]


class AddressColumnConfig(BaseColumnConfig):
    type: ColumnType = ColumnType.ADDRESS
    format: ColumnFormat = ColumnFormat.STRING

    @classmethod
    def from_form(cls, key_prefix="address_cfg") -> Optional["AddressColumnConfig"]:
        with st.form(f"{key_prefix}_form", clear_on_submit=True, border=False):
            name = st.text_input("Column Name (e.g., 'Address')", key=f"{key_prefix}_name")
            submit = st.form_submit_button("Add Column")
            if submit and name.strip():
                return cls(name=name.strip())
        return None

    @classmethod
    def generate_data(cls, config: "AddressColumnConfig", n_rows: int) -> List[str]:
        return [fake.address().replace('\n', ', ') for _ in range(n_rows)]
