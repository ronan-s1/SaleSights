import streamlit as st
from pymongo import MongoClient
import pandas as pd

def product_main():
    # Connect to MongoDB
    client = MongoClient("localhost", 27017)
    db = client.salesights
    products_collection = db.products
    categories_collection = db.product_categories

    # Function to fetch products from MongoDB
    def fetch_products(include_id=False):
        # Include "_id" in the result if include_id is True
        projection = {"_id": 1, "product_name": 1, "category": 1, "barcode_data": 1} if include_id else {"_id": 0, "product_name": 1, "category": 1, "barcode_data": 1}
        return list(products_collection.find({}, projection))

    # Function to fetch categories from MongoDB
    def fetch_categories():
        return [category["category"] for category in categories_collection.find()]

    # Function to add a new product to MongoDB
    def add_product(product_name, category, barcode_data):
        new_product = {
            "product_name": product_name,
            "category": category,
            "barcode_data": barcode_data,
        }
        products_collection.insert_one(new_product)

    # Function to delete a product from MongoDB
    def delete_product(product_name):
        products_collection.delete_one({"product_name": product_name})
        st.success(f"Product '{product_name}' deleted successfully!")

    st.title("Product Management")

    all_products = fetch_products()
    if all_products:
        # Exclude "_id" when displaying products in the table
        df_all_products = pd.DataFrame(all_products, columns=["product_name", "category", "barcode_data"])
        st.table(df_all_products)
    else:
        st.info("No products found.")

    # Expander for fetching and displaying existing products in a table
    with st.expander("Manage Products"):
        existing_products = fetch_products(include_id=True)
        if existing_products:
            df_existing_products = pd.DataFrame(existing_products)

            # Selectbox to choose a product for deletion or editing
            selected_product_name = st.selectbox("Select a product:", [product["product_name"] for product in existing_products], key="select_product_manage")

            # Display the selected product's details
            selected_product_details = df_existing_products[df_existing_products["product_name"] == selected_product_name]
            if not selected_product_details.empty:
                st.table(selected_product_details)
            else:
                st.warning("No product details found for the selected product.")

            # Button to delete the selected product
            if st.button("Delete Product"):
                delete_product(selected_product_name)

            # Form fields for editing the selected product
            st.write("Edit Product")

            # Check if selected product details are available
            if not selected_product_details.empty:
                # Fetch category options
                category_options = fetch_categories()

                # Input fields for editing
                edited_product_name = st.text_input("Edited Product Name:", selected_product_details["product_name"].iloc[0])
                edited_category = st.selectbox("Select Category:", category_options, index=category_options.index(selected_product_details["category"].iloc[0]), key="select_category_edit")
                edited_barcode_data = st.text_input("Edited Barcode Data:", selected_product_details["barcode_data"].iloc[0])

                # Button to update the product
                if st.button("Update Product"):
                    if edited_product_name and edited_category and edited_barcode_data:
                        # Get the _id from the selected_product_details
                        selected_product_id = selected_product_details["_id"].iloc[0]

                        # Update the existing product
                        updated_product = {
                            "product_name": edited_product_name,
                            "category": edited_category,
                            "barcode_data": edited_barcode_data,
                        }

                        # Use the _id to identify the document for update
                        products_collection.update_one({"_id": selected_product_id}, {"$set": updated_product})

                        st.info(f"Updated product: {edited_product_name}")
                    else:
                        st.warning("Please fill in all the fields.")
            else:
                st.info("No product selected.")

        else:
            st.info("No existing products found.")

    # Expander for adding a new product form
    with st.expander("Add a New Product"):
        # Form fields
        product_name = st.text_input("Product Name:")
        category_options = fetch_categories()
        category = st.selectbox("Select Category:", category_options)
        barcode_data = st.text_input("Barcode Data:")

        # Add product button
        if st.button("Add Product"):
            if product_name and category and barcode_data:
                add_product(product_name, category, barcode_data)
                st.success(f"New Product '{product_name}' added!")
            else:
                st.warning("Please fill in all the fields.")
