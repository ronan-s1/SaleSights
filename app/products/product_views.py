import streamlit as st
import pandas as pd
from products.product_controller import get_categories, get_products, add_new_product, delete_product, update_product


def edit_components():
    existing_products = get_products()
    
    if not existing_products:
        return

    df_existing_products = pd.DataFrame(existing_products)
    selected_product_name = st.selectbox("Select a product:", [product["product_name"] for product in existing_products], key="select_product_edit")
    selected_product_details = df_existing_products[df_existing_products["product_name"] == selected_product_name]

    if not selected_product_details.empty:
        st.table(selected_product_details)

        category_options = get_categories()

        # Input fields for editing
        edited_product_name = st.text_input("Edited Product Name:", selected_product_details["product_name"].iloc[0])
        edited_category = st.selectbox("Select Category:", category_options, index=category_options.index(selected_product_details["category"].iloc[0]), key="select_category_edit")
        edited_barcode_data = st.text_input("Edited Barcode Data:", selected_product_details["barcode_data"].iloc[0])

        # Button to update the product
        if st.button("Update Product"):
            if edited_product_name and edited_category and edited_barcode_data:  
                update_product(selected_product_details, edited_product_name, edited_category, edited_barcode_data)
                st.info(f"Updated product: {edited_product_name}")
            else:
                st.warning("Please fill in all the fields")
    else:
        st.warning("No product details found for the selected product.")


def delete_components():
    existing_products = get_products()
    
    if existing_products:
        df_existing_products = pd.DataFrame(existing_products)
        selected_product_name_delete = st.selectbox("Select a product:", [product["product_name"] for product in existing_products], key="select_product_delete")
        selected_product_details_delete = df_existing_products[df_existing_products["product_name"] == selected_product_name_delete]

        if not selected_product_details_delete.empty:
            st.table(selected_product_details_delete)
            
            # Button to delete the selected product
            if st.button("Delete Product"):
                delete_product(selected_product_details_delete)
                st.info(f"Deleted product: {selected_product_name_delete}")
        else:
            st.warning("No product details found for the selected product.")


def add_components():
    product_name = st.text_input("Product Name:")
    category_options = get_categories()
    category = st.selectbox("Select Category:", category_options)
    barcode_data = st.text_input("Barcode Data:")

    # Add product button
    if st.button("Add Product"):
        if product_name and category and barcode_data:
            add_new_product(product_name, category, barcode_data)
            st.success(f"New Product '{product_name}' added!")
        else:
            st.warning("Please fill in all the fields.")


def product_main():
    st.title("Product Management")
    
    all_products = get_products()
    if all_products:
        df_all_products = pd.DataFrame(all_products, columns=["product_name", "category", "barcode_data"])
        st.table(df_all_products)
    else:
        st.info("No products found.")
        
    
    if df_all_products:
        with st.expander("Edit Product"):
            edit_components()


        with st.expander("Delete Product"):
            delete_components()


    with st.expander("Add Product"):
        add_components()
