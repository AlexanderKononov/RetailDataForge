import streamlit as st
import random

def create_table_with_random_data(num_rows, num_cols):
    """Generates a table with random number data."""

    if num_rows <= 0 or num_cols <= 0:
        st.error("Number of rows and columns must be positive integers.")
        return

    data = []
    for i in range(num_rows):
        row = []
        for j in range(num_cols):
            # Generate a random integer between 0 and 100 (adjust range as needed)
            random_value = random.randint(0, 100)
            row.append(random_value)
        data.append(row)

    st.dataframe(data)

    # Get user input for the number of rows and columns
num_rows = st.number_input("Enter the number of rows:", min_value=1, value=5, step=1)
num_cols = st.number_input("Enter the number of columns:", min_value=1, value=5, step=1)

# Call the function to create the table
create_table_with_random_data(num_rows, num_cols)