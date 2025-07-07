import streamlit as st
import pandas as pd
import numpy as np
import random
import string

st.title("Step 3: View and Download Data")

def generate_data(columns, num_rows):
    data = {}
    for col in columns:
        if col["type"] == "Integer":
            data[col["name"]] = np.random.randint(0, 100, size=num_rows)
        elif col["type"] == "Float":
            data[col["name"]] = np.random.rand(num_rows) * 100
        elif col["type"] == "String":
            data[col["name"]] = [''.join(random.choices(string.ascii_letters, k=5)) for _ in range(num_rows)]
        elif col["type"] == "Boolean":
            data[col["name"]] = np.random.choice([True, False], size=num_rows)
    return pd.DataFrame(data)

if "columns" in st.session_state and "num_rows" in st.session_state:
    df = generate_data(st.session_state.columns, st.session_state.num_rows)
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='synthetic_data.csv',
        mime='text/csv',
    )
else:
    st.warning("Please define columns and number of rows first.")
