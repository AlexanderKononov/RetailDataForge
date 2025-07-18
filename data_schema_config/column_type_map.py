from enum import Enum
from typing import List
import streamlit as st
from data_schema_config.column_formats import (
    categorical_column_configs, 
    numeric_column_configs, 
    text_column_configs
)

col_confing_mapping = {
    "INTEGER": numeric_column_configs.IntegerColumnConfig,
    "STRING": text_column_configs.StringColumnConfig,
    "FLOAT": numeric_column_configs.FloatColumnConfig,
    "BOOLEAN": categorical_column_configs.BooleanColumnConfig,
    "PERSON_NAME": text_column_configs.PersonNameColumnConfig,
    "FIRST_NAME": text_column_configs.FirstNameColumnConfig,
    "LAST_NAME": text_column_configs.LastNameColumnConfig,
    "EMAIL": text_column_configs.EmailColumnConfig,
    "PHONE_NUMBER": text_column_configs.PhoneNumberColumnConfig,
    "COUNTRY": categorical_column_configs.CountryColumnConfig,
    "CITY": categorical_column_configs.CityColumnConfig,
    "ADDRESS": text_column_configs.AddressColumnConfig,
}

type_groups_mapping = {
    "BASIC": [
        "INTEGER", "FLOAT", "STRING", "BOOLEAN"
    ],
    "PERSONAL": [
        "PERSON_NAME", "FIRST_NAME", "LAST_NAME", "EMAIL", "PHONE_NUMBER"
    ],
    "LOCATION": [
        "COUNTRY", "CITY", "ADDRESS"
    ],
    "COMMERCE": [
        "PRICE", "CUSTOM_ID"
    ],
    "CONTACTS": [
        "EMAIL", "PHONE_NUMBER"
    ],
    "ALL": [
        "INTEGER", "FLOAT", "STRING", "BOOLEAN",
        "PERSON_NAME", "FIRST_NAME", "LAST_NAME",
        "EMAIL", "PHONE_NUMBER", "COUNTRY", "CITY", "ADDRESS",
        "PRICE", "CUSTOM_ID"
    ]
}  
