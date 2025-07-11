import streamlit as st

st.set_page_config(page_title="Synthetic Data Generator", layout="wide")
st.title("🧪 Synthetic Data Generator")

st.markdown("""
Welcome to the **Synthetic Data Generator** app!  
This tool helps you quickly create synthetic datasets for testing, prototyping, or development purposes.

### 🔧 How to Use:
1. Use the **sidebar** to navigate through the different steps:
   - **Define Columns**: Choose and configure the type of data you want in each column.
   - **Set Row Count**: Specify how many rows of data to generate.
   - **Preview & Download**: View the generated dataset and download it as a CSV file.

2. Each column type has configurable options (e.g., range for numbers, max length for strings).

3. You can mix and match multiple data types – from numbers to names, emails, and addresses.

---

📌 **Note**: All data is randomly generated using predefined rules and does not represent real individuals.

""")