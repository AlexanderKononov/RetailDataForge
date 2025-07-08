import streamlit as st
from data_schema_config.table_schema import TableSchema

st.title("Step 2: Choose Number of Rows")

# Check and fetch the table schema from session state
if "table_schema" not in st.session_state:
    st.warning("No column schema found. Please define columns first.")
    st.stop()

table_schema: TableSchema = st.session_state.table_schema

if not table_schema.get_columns():
    st.warning("No columns defined. Please go to Step 1 to add columns.")
    st.stop()

# Initialize num_rows in session state if missing
if "num_rows" not in st.session_state:
    st.session_state.num_rows = 100  # Default value

# Input number of rows
num = st.number_input("How many rows of synthetic data would you like to generate?",
                      min_value=1, max_value=100000, step=10,
                      value=st.session_state.num_rows)

# Save to session state
st.session_state.num_rows = num

# Display a summary of the selected columns
st.subheader("📋 Column Schema Preview")

for idx, col in enumerate(table_schema.get_columns(), 1):
    st.markdown(f"**{idx}.** `{col.name}` – *{col.type.value}*")

st.success(f"Number of rows set to: {st.session_state.num_rows}")
