import streamlit as st

st.title("Step 2: Specify Number of Rows")

if "num_rows" not in st.session_state:
    st.session_state.num_rows = 10

num = st.number_input("Enter number of rows to generate", min_value=1, value=st.session_state.num_rows)

if st.button("Set Number of Rows"):
    st.session_state.num_rows = num
    st.success(f"Number of rows set to {num}")
