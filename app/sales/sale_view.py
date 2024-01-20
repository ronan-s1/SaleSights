import streamlit as st
from sales.sale_controller import (
    add_scanned_product_to_transaction,
    format_transaction_df,
    process_barcode,
    get_products,
    add_product_to_transaction,
    get_total_transaction,
    add_transaction,
    clear_transaction_data,
)
from streamlit_qrcode_scanner import qrcode_scanner
import pandas as pd


def scan_product():
    # create cam_on session if it doesn't exist
    if "cam_on" not in st.session_state:
        st.session_state.cam_on = False

    # Add a button to toggle the camera on and off
    if st.button("Toggle Camera"):
        st.session_state.cam_on = not st.session_state.cam_on

    # If the camera is on, capture and display video frames
    if st.session_state.cam_on:
        barcode = qrcode_scanner(key="scanner")
        if barcode:
            scanned_product = process_barcode(barcode)

            if scanned_product:
                add_scanned_product_to_transaction(scanned_product)

            return scanned_product


def add_product_manually():
    # create selected_products session if it doesn't exist
    if "selected_products" not in st.session_state:
        st.session_state.selected_products = []

    products = get_products()

    # Check if the selected product is not already in the list
    selected_product_name = st.selectbox(
        "Select a product:", [product["product_name"] for product in products]
    )

    quantity = st.number_input("Quantity", min_value=1, value=1)

    if st.button("Add", key="add_manually"):
        selected_product_names = [
            product["product_name"] for product in st.session_state.selected_products
        ]

        add_product_to_transaction(
            selected_product_name, selected_product_names, quantity, products
        )
    df_selected_products = pd.DataFrame(st.session_state.selected_products)

    return df_selected_products


def sale_main():
    st.title("Log Sale Transaction 🛒")
    with st.expander("Add Product"):
        df_selected_products = add_product_manually()

    with st.expander("Scan Product"):
        scan_product()

    # if a product has been added to the transaction
    if not df_selected_products.empty:
        df_selected_products_show = format_transaction_df(df_selected_products)
        st.table(df_selected_products_show)
        total = get_total_transaction(df_selected_products)
        st.write(total)

        # create two columns for buttons
        col1, col2 = st.columns([9, 1])

        # clicked when transaction is finished
        if col1.button("Finish"):
            retrun_val = add_transaction(df_selected_products)
            if "iframe" in retrun_val:
                st.markdown(retrun_val, unsafe_allow_html=True)
            else:
                st.error(retrun_val)

        # clear table
        if col2.button("Clear"):
            clear_transaction_data()
