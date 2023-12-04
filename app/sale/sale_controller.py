import base64
from datetime import datetime as dt
import os
import streamlit as st
import pandas as pd
from fpdf import FPDF
from PIL import Image
import io
# from barcode import Code128
# from barcode.writer import ImageWriter
from datetime import datetime
from sale.sale_data import (
    fetch_products,
    get_product_by_barcode,
    insert_transaction_into_db,
    get_last_inserted_transaction,
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


def clear_transaction_data():
    st.session_state.selected_products = []
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
    insert_success = insert_transaction_into_db(transaction_data)
    if not insert_success:
        return "Error when inserting transaction"

    st.session_state.selected_products = []

    # generate receipt
    receipt = generate_receipt(df_selected_products)
    return receipt


def convert_pdf_to_base64(pdf_content):
    base64_pdf = base64.b64encode(pdf_content).decode("utf-8")
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    return pdf_display


def generate_receipt(df_selected_products):
    # preparing dataframe in correct format
    df_selected_products = df_selected_products.drop(columns=["category"])
    df_selected_products = df_selected_products.rename(
        columns={
            "product_name": "product",
            "price": "price",
            "quantity": "qty",
        }
    )
    pdf = FPDF()
    pdf.add_page()

    # Set font and styling
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, txt="Receipt", align='C')
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 11)

    # Current Date and Time
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M")

    pdf.cell(
        0,
        8,
        txt=f"Receipt Generation Date: {formatted_date}",
    )
    pdf.ln(8)

    # headers
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(15, 8, txt="qty", border=1, fill=True)
    pdf.cell(145, 8, txt="product", border=1, fill=True)
    pdf.cell(30, 8, txt="price", border=1, fill=True)

    # receipt Items
    for _, row in df_selected_products.iterrows():
        pdf.ln(8)
        pdf.cell(15, 8, txt=str(row["qty"]), border=1)
        pdf.cell(145, 8, txt=row["product"], border=1)
        pdf.cell(30, 8, txt="{:.2f}".format(row["price"]), border=1)

    # total
    pdf.ln(8)
    total = (df_selected_products["qty"] * df_selected_products["price"]).sum()
    formatted_total = "{:.2f}".format(total)
    pdf.cell(160, 8, txt="Total", border=1)
    pdf.set_fill_color(174, 247, 173)
    pdf.cell(30, 8, txt=f"{formatted_total}", border=1, fill=True)

    # id
    pdf.ln(10)
    pdf.cell(15, 8, txt=f"Transaction ID: {str(get_last_inserted_transaction())}")

    # add Salesights logo
    pdf.image(
        os.path.join("static", "img", "salesights-logo.png"), x=10, y=pdf.h - 20, w=40
    )

    # save the PDF to BytesIO
    pdf_byte_string = pdf.output()

    # display PDF using iframe
    iframe_base64_pdf = convert_pdf_to_base64(pdf_byte_string)

    return iframe_base64_pdf
