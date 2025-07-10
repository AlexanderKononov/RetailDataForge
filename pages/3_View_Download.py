import streamlit as st
import pandas as pd
import numpy as np
from faker import Faker
from data_schema_config.table_schema import TableSchema
from data_schema_config.column_schema import ColumnType

fake = Faker()

st.title("Step 3: Generate & Preview Synthetic Data")

# Check session data
if "table_schema" not in st.session_state or not st.session_state.table_schema.get_columns():
    st.warning("No column schema found. Please define columns first.")
    st.stop()

table_schema: TableSchema = st.session_state.table_schema

# Function to generate fake data
def generate_data(schema: TableSchema, n_rows: int) -> pd.DataFrame:
    data = {}

    for col in schema.get_columns():
        if col.type == ColumnType.INTEGER:
            data[col.name] = np.random.randint(0, 100, size=n_rows)
        elif col.type == ColumnType.FLOAT:
            data[col.name] = np.round(np.random.uniform(0.0, 100.0, size=n_rows), 2)
        elif col.type == ColumnType.STRING:
            data[col.name] = [fake.word() for _ in range(n_rows)]
        elif col.type == ColumnType.BOOLEAN:
            data[col.name] = np.random.choice([True, False], size=n_rows)
        else:
            data[col.name] = [None] * n_rows

    return pd.DataFrame(data)

# Button to generate
if st.button("🚀 Generate Synthetic Data"):
    df = generate_data(table_schema, table_schema.get_num_rows())
    st.session_state.generated_data = df
    st.success("Synthetic data generated successfully!")

# Download button
if "generated_data" in st.session_state:
    csv = st.session_state.generated_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='synthetic_data.csv',
        mime='text/csv',
        key='download-csv'
    )

# Display table
if "generated_data" in st.session_state:
    st.subheader("📊 Preview of Generated Data")
    st.dataframe(st.session_state.generated_data.head(), use_container_width=True)


