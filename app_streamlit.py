import streamlit as st
from utils import epic_chance, text_to_markdown
from contextlib import redirect_stdout
import io
import re

# # 1. Your Backend Function
# def my_backend_function(val1, val2, val3):
#     # This is where your actual logic goes (e.g., querying a database, RAG, scraping)
#     # For now, it just returns a formatted string.
#     return f"Successfully processed: '{val1}', {val2}, and '{val3}'."

# 2. GUI Header and Print Statements
st.title("Data Processor")
st.write("Welcome to the app. Please provide the three required parameters below to execute the backend task.")

# 3. The Three Inputs
input_1 = st.number_input("Total pack size (remaining):", value=250, min_value=1, step=10)
input_2 = st.number_input("# of cards you like:", value=7, min_value=1, max_value=input_1)
input_3 = st.number_input("# of cards you'll draw:", value=10, min_value=1, max_value=input_1)

# 4. Execution Trigger
if st.button("Run Backend Function"):
    # Input validation
    if not input_1 or not input_2 or not input_3:
        st.warning("Please ensure parameters are filled before running.")
    else:
        # Print an intermediate status statement
        st.info("Executing backend function...")
        
        # Plug inputs into the backend
        f = io.StringIO()
        with redirect_stdout(f):
            result = epic_chance(input_1, input_2, input_3)
        f_prints = f.getvalue()     # Collected print strings
        f_prints_markdown = text_to_markdown(f_prints)  # Convert the newlines
        
        # Print the final result statement for the user to read
        # st.success(result)
        st.success(f_prints_markdown)
