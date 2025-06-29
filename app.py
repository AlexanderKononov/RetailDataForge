import streamlit as st

st.title("Retail Data Forge")
st.markdown("""
Welcome to the Retail Data Forge multi-page app! Use the navigation menu to:
- Select the number of columns
- Select the number of rows
- View your generated table
""")

# Initialize session state for inputs
if 'num_cols' not in st.session_state:
    st.session_state['num_cols'] = 5
if 'num_rows' not in st.session_state:
    st.session_state['num_rows'] = 5

st.header("Step 1: Select Number of Columns")
st.session_state['num_cols'] = st.number_input(
    "Enter the number of columns:", min_value=1, value=st.session_state.get('num_cols', 5), step=1
)
st.info("Go to the next page to select number of rows.")