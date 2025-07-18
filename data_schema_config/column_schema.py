from pydantic import BaseModel, Field, ValidationError, conint, constr
from enum import Enum
import numpy as np
from typing import Optional, List, Union
import streamlit as st
from faker import Faker

fake = Faker()

class ColumnType(str, Enum):
    INTEGER = "Integer"
    FLOAT = "Float"
    STRING = "String"
    BOOLEAN = "Boolean"
    PERSON_NAME = "Person Name"
    FIRST_NAME = "First Name"
    LAST_NAME = "Last Name"
    EMAIL = "Email"
    PHONE_NUMBER = "Phone Number"
    COUNTRY = "Country"
    CITY = "City"
    ADDRESS = "Address"

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
        print(f"Selected column type: {col_type_str}")
        try:
            col_type = ColumnType(col_type_str)
            print(f"Parsed column type: {col_type}")
        except ValueError:
            st.warning("Invalid column type.")
            return None

        config_cls = column_type_to_config_class.get(col_type)
        if not config_cls:
            st.warning(f"No configuration form for column type: {col_type}")
            return None

        return config_cls.from_form(key_prefix=f"{key_prefix}_{col_type.value.lower()}")
    
    @classmethod
    def generate_data(cls, config: "BaseColumnConfig", n_rows: int) -> List:
        return [None] * n_rows  # Default fallback
    

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
    
    @classmethod
    def generate_data(cls, config: "IntegerColumnConfig", n_rows: int) -> List[int]:
        return np.random.randint(config.min_value, config.max_value + 1, size=n_rows).tolist()



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
    
    @classmethod
    def generate_data(cls, config: "StringColumnConfig", n_rows: int) -> List[str]:
        return [fake.word()[:config.max_length] for _ in range(n_rows)]
    
class FloatColumnConfig(BaseColumnConfig):
    type: ColumnType = ColumnType.FLOAT
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
    
class BooleanColumnConfig(BaseColumnConfig):
    type: ColumnType = ColumnType.BOOLEAN
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
    

class PersonNameColumnConfig(BaseColumnConfig):
    type: ColumnType = ColumnType.PERSON_NAME

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

class CountryColumnConfig(BaseColumnConfig):
    type: ColumnType = ColumnType.COUNTRY

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

class CityColumnConfig(BaseColumnConfig):
    type: ColumnType = ColumnType.CITY

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

class AddressColumnConfig(BaseColumnConfig):
    type: ColumnType = ColumnType.ADDRESS

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


column_type_to_config_class = {
    ColumnType.INTEGER: IntegerColumnConfig,
    ColumnType.STRING: StringColumnConfig,
    ColumnType.FLOAT: FloatColumnConfig,
    ColumnType.BOOLEAN: BooleanColumnConfig,
    ColumnType.PERSON_NAME: PersonNameColumnConfig,
    ColumnType.FIRST_NAME: FirstNameColumnConfig,
    ColumnType.LAST_NAME: LastNameColumnConfig,
    ColumnType.EMAIL: EmailColumnConfig,
    ColumnType.PHONE_NUMBER: PhoneNumberColumnConfig,
    ColumnType.COUNTRY: CountryColumnConfig,
    ColumnType.CITY: CityColumnConfig,
    ColumnType.ADDRESS: AddressColumnConfig,

    # Add others types as needed
}