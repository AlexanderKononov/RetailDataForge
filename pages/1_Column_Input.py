import streamlit as st
from data_schema_config.column_schema import ColumnType, ColumnConfig
from data_schema_config.table_schema import TableSchema


st.title("Step 1: Define Columns")

# Initialize schema in session state if it doesn't exist
if "table_schema" not in st.session_state:
    st.session_state.table_schema = TableSchema()

table_schema: TableSchema = st.session_state.table_schema

with st.expander("➕ Add New Column", expanded=False):
    config = ColumnConfig.from_form()
    if config:
        try:
            table_schema.add_config(config)
            st.success(f"Added column: {config}")
        except ValueError as e:
            st.warning(str(e))

# Display existing columns
st.subheader("📋 Current Columns")

columns = table_schema.get_columns()

if columns:
    for idx, col in enumerate(columns, 1):
        st.markdown(f"**{idx}.** `{col.name}` – *{col.type.value}*")
else:
    st.info("No columns defined yet. Add some using the form above.")