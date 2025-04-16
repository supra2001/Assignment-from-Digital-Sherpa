import streamlit as st
from streamlit_searchbox import st_searchbox
import pickle
import pandas as pd

st.title("Product Search")

def load_data():
    with open("tables.pkl", "rb") as f:
        tables = pickle.load(f)
    
    all_first_column_values = []
    for table in tables:
        first_col = table.columns[0]
        all_first_column_values.extend(table[first_col].astype(str).tolist())
    
    return all_first_column_values, tables

def suggest_products(input):
    term = input.strip().lower()
    return [p for p in product_list if term in p.lower()]  # Case-insensitive search

def get_product_details(product_code, tables):
    for table in tables:
        row = table[table.iloc[:, 0] == product_code]
        if not row.empty:
            return row
    return None

product_list, tables = load_data()

selected_product = st_searchbox(suggest_products, placeholder="Type a product code...")

if selected_product:
    with st.spinner('Loading product details...'):
        product_details = get_product_details(selected_product, tables)
    
    if product_details is not None:
        st.subheader("Product Details")
        st.write("Here is the full information for the selected product:")
        st.write(product_details)
    else:
        st.error("No product found with the given code.")
