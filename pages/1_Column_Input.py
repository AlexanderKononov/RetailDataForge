import streamlit as st
from data_schema_config.column_schema import ColumnType
from data_schema_config.table_schema import TableSchema


st.title("Step 1: Define Columns")

# Initialize schema in session state if it doesn't exist
if "table_schema" not in st.session_state:
    st.session_state.table_schema = TableSchema()

table_schema: TableSchema = st.session_state.table_schema

with st.expander("➕ Add New Column", expanded=False):
    with st.form("column_form", clear_on_submit=True, border=False):
        col_name = st.text_input("Column Name")
        col_type = st.selectbox("Data Type", [col.value for col in ColumnType])
        submit = st.form_submit_button("Add Column")

        if submit:
            try:
                table_schema.add_column(name=col_name.strip(), col_type=col_type)
                st.success(f"Added column: {col_name} ({col_type})")
            except ValueError as e:
                st.warning(str(e))
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Display existing columns
st.subheader("📋 Current Columns")

columns = table_schema.get_columns()

if columns:
    for idx, col in enumerate(columns, 1):
        st.markdown(f"**{idx}.** `{col.name}` – *{col.type.value}*")
else:
    st.info("No columns defined yet. Add some using the form above.")