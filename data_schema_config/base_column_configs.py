from enum import Enum
from pydantic import BaseModel
from typing import List, Optional
import streamlit as st

COLUMN_TYPE_REGISTRY = {}

def register_column_config(column_type):
    def decorator(cls):
        COLUMN_TYPE_REGISTRY[column_type] = cls
        return cls
    return decorator

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
    PRICE = "Price"
    CUSTOM_ID = "Custom ID"

    @property
    def format(self) -> str:
        mapping = {
            self.INTEGER: "Numeric",
            self.FLOAT: "Numeric",
            self.PRICE: "Numeric",
            self.STRING: "Text",
            self.CUSTOM_ID: "Text",
            self.BOOLEAN: "Categorical",
            self.PERSON_NAME: "Text",
            self.FIRST_NAME: "Text",
            self.LAST_NAME: "Text",
            self.EMAIL: "Text",
            self.PHONE_NUMBER: "Text",
            self.COUNTRY: "Categorical",
            self.CITY: "Categorical",
            self.ADDRESS: "Text",
        }
        return mapping[self]


class ColumnTypeGroup(str, Enum):
    BASIC = "Basic"
    PERSONAL = "Personal Info"
    LOCATION = "Location"
    COMMERCE = "Commerce"
    CONTACTS = "Contacts"
    ALL = "All Types"

    def group_types(self) -> List[ColumnType]:
        mapping = {
            self.BASIC: [
                ColumnType.INTEGER,
                ColumnType.FLOAT,
                ColumnType.STRING,
                ColumnType.BOOLEAN
            ],
            self.PERSONAL: [
                ColumnType.PERSON_NAME,
                ColumnType.FIRST_NAME,
                ColumnType.LAST_NAME,
                ColumnType.EMAIL,
                ColumnType.PHONE_NUMBER
            ],
            self.LOCATION: [
                ColumnType.COUNTRY,
                ColumnType.CITY,
                ColumnType.ADDRESS
            ],
            self.COMMERCE: [
                ColumnType.PRICE,
                ColumnType.CUSTOM_ID
            ],
            self.CONTACTS: [
                ColumnType.EMAIL,
                ColumnType.PHONE_NUMBER
            ],
            self.ALL: list(ColumnType)  # ALL = all available types
        }
        return mapping[self]

class ColumnConfig(BaseModel):
    name: str
    type: ColumnType
    format: str

    @classmethod
    def select_col_form(cls, key_prefix="add_column"):
        # Type_group → Type → type-specific form logic.
        type_group_choice_str = st.selectbox("Column type groups",
                                             [t.value for t in ColumnTypeGroup], 
                                             key=f"{key_prefix}_group")
        print(f"Selected type group: {type_group_choice_str}")
        col_type = st.selectbox("Column Type",
                                            [t.value for t in ColumnTypeGroup(type_group_choice_str).group_types()],
                                            key=f"{key_prefix}_type")
        
        print(f"Selected column type: {col_type}")
        try:
            col_conf = col_confing_mapping[ColumnType(col_type)]        
        except ValueError:
            st.warning("Invalid column type.")
            return None
        
        print("================================")
        print(f"Parsed column conf: {col_conf}")


        if not col_conf:
            st.warning(f"No configuration form for column type: {col_type}")
            return None
        
        a = col_conf.from_form(key_prefix=f"{key_prefix}_{col_type.lower()}")
        print(f"Column config from form: {a}")

        return a
    
    @classmethod
    def generate_data(cls, config: "ColumnConfig", n_rows: int) -> List:
        return [None] * n_rows  # Default fallback
        # Dispatch to correct subclass:
        config_cls = column_type_to_config_class.get(ColumnType(type_choice))
        return config_cls.from_form(key_prefix=key_prefix)


    def generate_data(self, n_rows: int):  # default fallback
        return [None] * n_rows

class Config:
    validate_assignment = True  # strict validation



###################
### Categorical Column Configs
###################
from faker import Faker
from typing import List, Optional

fake = Faker()

class BooleanColumnConfig(ColumnConfig):
    type: ColumnType = ColumnType.BOOLEAN
    format: str = "Categorical"

    true_probability: float = 0.5  # Probability of generating True

    @classmethod
    def from_form(cls, key_prefix="bool_cfg"):
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
    def from_form(cls, key_prefix="country_cfg"):
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
    def from_form(cls, key_prefix="city_cfg"):
        with st.form(f"{key_prefix}_form", clear_on_submit=True, border=False):
            name = st.text_input("Column Name (e.g., 'City')", key=f"{key_prefix}_name")
            submit = st.form_submit_button("Add Column")
            if submit and name.strip():
                return cls(name=name.strip())
        return None

    @classmethod
    def generate_data(cls, config: "CityColumnConfig", n_rows: int) -> List[str]:
        return [fake.city() for _ in range(n_rows)]



####################
### Numeric Column Configs
####################

class IntegerColumnConfig(ColumnConfig):
    type: ColumnType = ColumnType.INTEGER
    format: str = "Numeric"
    min_value: int = 0
    max_value: int = 100

    @classmethod
    def from_form(cls, key_prefix="int_cfg"):
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
    def from_form(cls, key_prefix="float_cfg"):
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
    



#####################
### Text Column Configs
#####################
    
class StringColumnConfig(ColumnConfig):
    type: ColumnType = ColumnType.STRING
    format: str = "Text"
    max_length: int = 20

    @classmethod
    def from_form(cls, key_prefix="str_cfg"):
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
    

class PersonNameColumnConfig(ColumnConfig):
    type: ColumnType = ColumnType.PERSON_NAME
    format: str = "Text"

    @classmethod
    def from_form(cls, key_prefix="person_name_cfg"):
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
    
class FirstNameColumnConfig(ColumnConfig):
    type: ColumnType = ColumnType.FIRST_NAME
    format: str = "Text"

    @classmethod
    def from_form(cls, key_prefix="first_name_cfg"):
        with st.form(f"{key_prefix}_form", clear_on_submit=True, border=False):
            name = st.text_input("Column Name (e.g., 'First Name')", key=f"{key_prefix}_name")
            submit = st.form_submit_button("Add Column")
            if submit and name.strip():
                return cls(name=name.strip())
        return None

    @classmethod
    def generate_data(cls, config: "FirstNameColumnConfig", n_rows: int) -> List[str]:
        return [fake.first_name() for _ in range(n_rows)]
    
class LastNameColumnConfig(ColumnConfig):
    type: ColumnType = ColumnType.LAST_NAME
    format: str = "Text"

    @classmethod
    def from_form(cls, key_prefix="last_name_cfg"):
        with st.form(f"{key_prefix}_form", clear_on_submit=True, border=False):
            name = st.text_input("Column Name (e.g., 'Last Name')", key=f"{key_prefix}_name")
            submit = st.form_submit_button("Add Column")
            if submit and name.strip():
                return cls(name=name.strip())
        return None

    @classmethod
    def generate_data(cls, config: "LastNameColumnConfig", n_rows: int) -> List[str]:
        return [fake.last_name() for _ in range(n_rows)]
    
class EmailColumnConfig(ColumnConfig):
    type: ColumnType = ColumnType.EMAIL
    format: str = "Text"

    @classmethod
    def from_form(cls, key_prefix="email_cfg"):
        with st.form(f"{key_prefix}_form", clear_on_submit=True, border=False):
            name = st.text_input("Column Name (e.g., 'Email')", key=f"{key_prefix}_name")
            submit = st.form_submit_button("Add Column")
            if submit and name.strip():
                return cls(name=name.strip())
        return None

    @classmethod
    def generate_data(cls, config: "EmailColumnConfig", n_rows: int) -> List[str]:
        return [fake.email() for _ in range(n_rows)]

class PhoneNumberColumnConfig(ColumnConfig):
    type: ColumnType = ColumnType.PHONE_NUMBER
    format: str = "Text"

    @classmethod
    def from_form(cls, key_prefix="phone_cfg"):
        with st.form(f"{key_prefix}_form", clear_on_submit=True, border=False):
            name = st.text_input("Column Name (e.g., 'Phone')", key=f"{key_prefix}_name")
            submit = st.form_submit_button("Add Column")
            if submit and name.strip():
                return cls(name=name.strip())
        return None

    @classmethod
    def generate_data(cls, config: "PhoneNumberColumnConfig", n_rows: int) -> List[str]:
        return [fake.phone_number() for _ in range(n_rows)]


class AddressColumnConfig(ColumnConfig):
    type: ColumnType = ColumnType.ADDRESS
    format: str = "Text"

    @classmethod
    def from_form(cls, key_prefix="address_cfg"):
        with st.form(f"{key_prefix}_form", clear_on_submit=True, border=False):
            name = st.text_input("Column Name (e.g., 'Address')", key=f"{key_prefix}_name")
            submit = st.form_submit_button("Add Column")
            if submit and name.strip():
                return cls(name=name.strip())
        return None

    @classmethod
    def generate_data(cls, config: "AddressColumnConfig", n_rows: int) -> List[str]:
        return [fake.address().replace('\n', ', ') for _ in range(n_rows)]



col_confing_mapping = {
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
}