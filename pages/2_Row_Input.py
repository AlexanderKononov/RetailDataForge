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

# Use existing value or default
default_rows = table_schema.get_num_rows() if hasattr(table_schema, "get_num_rows") else 100

num = st.number_input(
    "How many rows of synthetic data would you like to generate?",
    min_value=1, max_value=100000, step=10, value=default_rows
)

# Update schema directly
table_schema.set_num_rows(num)

# Optional: Store back (not strictly necessary if object is mutable)
st.session_state.table_schema = table_schema

# Show summary
st.subheader("📋 Column Schema Preview")
for idx, col in enumerate(table_schema.get_columns(), 1):
    st.markdown(f"**{idx}.** `{col.name}` – *{col.type.value}*")

st.success(f"Number of rows set to: {table_schema.get_num_rows()}")
