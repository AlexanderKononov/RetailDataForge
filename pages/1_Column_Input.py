import streamlit as st
from data_schema_config.base_column_configs import (
    ColumnConfig, 
    ColumnType, 
    ColumnTypeGroup)
from data_schema_config.table_schema import TableSchema


st.title("Step 1: Define Columns")

# Initialize schema in session state if it doesn't exist
if "table_schema" not in st.session_state:
    st.session_state.table_schema = TableSchema()

table_schema: TableSchema = st.session_state.table_schema


with st.expander("➕ Add New Column", expanded=True):
    col_config = ColumnConfig.select_col_form()
    print("!!!!!!!!Column config selected:", col_config)
    print(f"Column config selected: {col_config}")
    if col_config:
        try:
            table_schema.add_col_config(col_config)
            st.success(f"Added column: {col_config}")
        except ValueError as e:
            st.warning(str(e))

# Display list of columns with delete buttons
st.subheader("📋 Current Columns")

columns = table_schema.get_columns()

if columns:
    for idx, col in enumerate(columns, 1):
        col_container = st.container()
        with col_container:
            col1, col2 = st.columns([6, 1])
            col1.markdown(f"**{idx}.** `{col.name}` – *{col.type.value}*")
            if col2.button("❌", key=f"delete_{col.name}"):
                table_schema.remove_column(col.name)
                st.rerun()