import streamlit as st
from streamlit_searchbox import st_searchbox
import pickle
import pandas as pd

st.title("Check Point Product Search")

def load_data():
    with open("tables.pkl", "rb") as f:
        tables = pickle.load(f)
        
    all_first_column_values = []
    for table in tables:
        first_col = table.columns[0]
        all_values = table[first_col].astype(str).tolist()
        clean_values = [val for val in all_values if len(val) < 100 and "note" not in val.lower()]
        all_first_column_values.extend(clean_values)
        
    return all_first_column_values, tables

product_list,tables = load_data()

def suggest_products(input):
    term = input.strip().lower()
    return [p for p in product_list if term in p.lower()]

def get_product_details(product_code, tables):
    for table in tables:
        row = table[table.iloc[:,0] == product_code]
        if not row.empty:
            return row
    return None

selected_product = st_searchbox(suggest_products, placeholder="Type a product...")

if selected_product:
    product_details = get_product_details(selected_product,tables)
    
    if product_details is not None:
        st.subheader("Product Details")
        st.write("Here is the full information about the product you selected:")
        st.dataframe(product_details, use_container_width=True)
    else:
        st.error("No product available with this product code.")