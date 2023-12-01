import streamlit as st
import pandas as pd
from products.product_controller import (
    get_categories,
    get_products,
    add_new_product,
    delete_product,
    update_product,
    add_new_category,
    edit_existing_category,
    delete_category,
    get_products_df,
)


def display_products():
    all_products, df_all_products = get_products_df()
    st.dataframe(df_all_products, use_container_width=True)
    return all_products


def edit_product_components():
    existing_products = get_products()

    df_existing_products = pd.DataFrame(existing_products)
    selected_product_name = st.selectbox(
        "Select a product:",
        [product["product_name"] for product in existing_products],
        key="select_product_edit",
    )
    selected_product_details = df_existing_products[
        df_existing_products["product_name"] == selected_product_name
    ]

    if not selected_product_details.empty:
        selected_product_details_display = selected_product_details.drop(
            columns=["_id"], errors="ignore"
        ).transpose()
        st.table(selected_product_details_display)

        # Input fields for editing
        category_options = get_categories()
        edited_product_name = st.text_input(
            "Edited Product Name:", selected_product_details["product_name"].iloc[0]
        )
        edited_category = st.selectbox(
            "Select Category:",
            category_options,
            index=category_options.index(selected_product_details["category"].iloc[0]),
            key="select_category_edit",
        )
        edited_barcode_data = st.text_input(
            "Edited Barcode Data:", selected_product_details["barcode_data"].iloc[0]
        )
        edited_price = st.text_input(
            "Edited Price Data:", selected_product_details["price"].iloc[0]
        )

        # Button to update the product
        if st.button("Update Product"):
            err = update_product(
                selected_product_details,
                edited_product_name,
                edited_category,
                edited_barcode_data,
                edited_price,
            )
            if err:
                st.warning(err)
            else:
                st.rerun()


def delete_product_components():
    existing_products = get_products()
    df_existing_products = pd.DataFrame(existing_products)
    selected_product_name_delete = st.selectbox(
        "Select a product:",
        [product["product_name"] for product in existing_products],
        key="select_product_delete",
    )
    selected_product_details_delete = df_existing_products[
        df_existing_products["product_name"] == selected_product_name_delete
    ]

    if not selected_product_details_delete.empty:
        selected_product_details_delete_display = selected_product_details_delete.drop(
            columns=["_id"], errors="ignore"
        ).transpose()
        st.table(selected_product_details_delete_display)

        # Button to delete the selected product
        if st.button("Delete Product"):
            delete_product(selected_product_details_delete)
            st.rerun()
    else:
        st.warning("No product details found for the selected product.")


def add_product_components():
    product_name = st.text_input("Product Name:")
    category_options = get_categories()
    category = st.selectbox("Select Category:", category_options)
    barcode_data = st.text_input("Barcode Data:")
    price = st.text_input("Price:")

    # Add product button
    if st.button("Add Product"):
        err = add_new_product(product_name, category, barcode_data, price)
        if err:
            st.warning(err)

        else:
            st.rerun()


def add_category_components():
    new_category_name = st.text_input("Category Name:")

    if st.button("Add Category"):
        err = add_new_category(new_category_name)
        if err:
            st.warning(err)
        else:
            st.rerun()


def edit_category_components():
    selected_category_name = st.selectbox(
        "Select a category:",
        get_categories(),
        key="select_category_edit_2",
    )

    new_category_name = st.text_input("Edit Category Name:", selected_category_name)
    # Add additional input fields for other category details if needed

    if st.button("Edit Category"):
        err = edit_existing_category(selected_category_name, new_category_name)
        if err:
            st.warning(err)
        else:
            st.rerun()


def delete_category_components():
    selected_category_name = st.selectbox(
        "Select a category to delete:",
        get_categories(),
        key="select_category_delete",
    )

    if st.button("Delete Category"):
        err = delete_category(selected_category_name)
        if err:
            st.warning(err)
        else:
            st.rerun()


def product_main():
    st.title("Product Management")
    products = display_products()
    categories = get_categories()
    product_col, category_col = st.columns(2)

    with product_col:
        with st.expander("Add Product"):
            add_product_components()

        if products:
            with st.expander("Edit Product"):
                edit_product_components()

            with st.expander("Delete Product"):
                delete_product_components()
        else:
            st.info("No products found")

    with category_col:
        with st.expander("Add Category"):
            add_category_components()

        if categories:
            with st.expander("Edit Category"):
                edit_category_components()

            with st.expander("Delete Category"):
                delete_category_components()
        else:
            st.info("No categories found")
