from datetime import datetime as dt
import streamlit as st
import pandas as pd
from fpdf import FPDF
from PIL import Image
import io
from barcode import Code128
from barcode.writer import ImageWriter

from sale.sale_data import (
    fetch_products,
    get_product_by_barcode,
    insert_transaction_into_db,
)


def get_products():
    products = fetch_products()
    return list(products)


def process_barcode(barcode_data):
    product = get_product_by_barcode(barcode_data)

    if product:
        return product

    return f"No product with scanned barcode: {barcode_data}."


def add_product_to_transaction(
    selected_product_name, selected_product_names, quantity, products
):
    if selected_product_name in selected_product_names:
        # Update the quantity for the existing product
        for product in st.session_state.selected_products:
            if product["product_name"] == selected_product_name:
                product["quantity"] = quantity
    else:
        # Add a new entry to the list
        selected_product = [
            product
            for product in products
            if product["product_name"] == selected_product_name
        ]
        if selected_product:
            selected_product[0]["quantity"] = quantity
            st.session_state.selected_products.append(selected_product[0])


def format_transaction_df(df_selected_products):
    df_selected_products_show = df_selected_products.drop(
        columns=["_id", "barcode_data"], errors="ignore"
    )

    df_selected_products_show = df_selected_products_show.rename(
        columns={
            "product_name": "Product",
            "category": "Category",
            "price": "Price",
            "quantity": "Quantity",
        }
    )

    df_selected_products_show = df_selected_products_show.style.format(
        {"Price": "{:.2f}".format}
    )

    return df_selected_products_show


def get_total_transaction(df_selected_products):
    # total = product price * quantity
    total = (df_selected_products["price"] * df_selected_products["quantity"]).sum()
    return f"Total: {total:.2f}"


def add_scanned_product_to_transaction(scanned_product):
    if "selected_products" not in st.session_state:
        st.session_state.selected_products = []

    selected_product_names = [
        product["product_name"] for product in st.session_state.selected_products
    ]

    # Check if the scanned product is already in the list
    if not scanned_product["product_name"] in selected_product_names:
        scanned_product["quantity"] = 1
        st.session_state.selected_products.append(scanned_product)
        st.rerun()


def add_transaction(df_selected_products):
    st.session_state.cam_on = False
    if df_selected_products.empty:
        return "Cannot finish an empty transaction"

    # Create a transaction document
    transaction_data = {
        "timestamp": dt.utcnow(),
        "total": get_total_transaction(df_selected_products),
        "products": df_selected_products.drop(columns=["barcode_data"]).to_dict(
            orient="records"
        ),
    }

    # Insert the transaction
    insert_transaction_into_db(transaction_data)
    st.session_state.selected_products = []
    st.rerun()
