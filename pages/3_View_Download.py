import streamlit as st
import pandas as pd
from data_schema_config.table_schema import TableSchema

st.title("Step 3: Generate & Preview Synthetic Data")

# Check session data
if "table_schema" not in st.session_state or not st.session_state.table_schema.get_columns():
    st.warning("No column schema found. Please define columns first.")
    st.stop()

table_schema: TableSchema = st.session_state.table_schema

# Button to generate
if st.button("🚀 Generate Synthetic Data"):
    df = table_schema.generate_dataframe()
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
