import streamlit as st
import random

st.header("Step 3: Random Data Table")
num_rows = st.session_state.get('num_rows', 5)
num_cols = st.session_state.get('num_cols', 5)

data = []
for i in range(num_rows):
    row = []
    for j in range(num_cols):
        random_value = random.randint(0, 100)
        row.append(random_value)
    data.append(row)
st.dataframe(data)
