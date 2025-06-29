import streamlit as st

st.header("Step 2: Select Number of Rows")
st.session_state['num_rows'] = st.number_input(
    "Enter the number of rows:", min_value=1, value=st.session_state.get('num_rows', 5), step=1
)
st.info("Go to the next page to view the table.")
