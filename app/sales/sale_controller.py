import base64
import os
import platform
import streamlit as st
from fpdf import FPDF
from datetime import datetime
from sales.sale_data import (
    fetch_products,
    get_product_by_barcode,
    insert_transaction_into_db,
)
from utils import LOGO_PATH


def get_products():
    """
    Request list of all products from data access.

    Returns:
        List[dict]: A list of product documents
    """
    products = fetch_products()
    return list(products)


def process_barcode(barcode_data):
    """
    Process a scanned barcode and request data acces to retrieve the corresponding product.

    Args:
        barcode_data (str): The scanned barcode data.

    Returns:
        dict: Fetched product with matching barcode
        str: If no product is found, return an error message
    """
    product = get_product_by_barcode(barcode_data)

    if product:
        return product

    return f"No product with scanned barcode: {barcode_data}."


def add_product_to_transaction(product_name, product_names, quantity, products):
    """
    Add a product to the transaction or update its quantity if already selected.

    Args:
        selected_product_name (str): The name of the selected product
        selected_product_names (list): List of names of already selected products
        quantity (int): The quantity of the product
        products (list): List of products

    Returns:
        None
    """
    if product_name in product_names:
        # Update the quantity for the existing product
        for product in st.session_state.selected_products:
            if product["product_name"] == product_name:
                product["quantity"] = quantity
    else:
        # Add a new entry to the list
        selected_product = [
            product for product in products if product["product_name"] == product_name
        ]
        if selected_product:
            selected_product[0]["quantity"] = quantity
            st.session_state.selected_products.append(selected_product[0])


def format_transaction_df(df_selected_products):
    """
    Format and clean the transaction DataFrame

    Args:
        df_selected_products (pd.DataFrame): DataFrame containing selected products.

    Returns:
        Styler: A formatted Styler object for displaying the DataFrame.
    """
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
    """
    Calculate the total price of the transaction.

    Args:
        df_selected_products (pd.DataFrame): DataFrame containing selected products.

    Returns:
        str: Total price of the transaction.
    """
    total = (df_selected_products["price"] * df_selected_products["quantity"]).sum()
    return round(total, 2)


def add_scanned_product_to_transaction(scanned_product):
    """
    Add a scanned product to the transaction.

    Args:
        scanned_product (str): The product information of the scanned product

    Returns:
        None
    """
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
    """
    Clear the transaction data stored in the session state

    Returns:
        None
    """
    st.session_state.selected_products = []
    st.rerun()


def add_transaction(df_selected_products):
    """
    Request data access to add a transaction to the database and generate a receipt.

    Args:
        df_selected_products (pd.DataFrame): DataFrame containing selected products.

    Returns:
       str: Base64-encoded string for displaying the PDF receipt using an iframe
       str: Error message
    """
    st.session_state.cam_on = False
    if df_selected_products.empty:
        return "Cannot finish an empty transaction"

    # Create a transaction document
    current_timestamp = datetime.utcnow()
    date_str = current_timestamp.strftime("%Y-%m-%d")
    time_str = current_timestamp.strftime("%H:%M:%S")
    transaction_data = {
        "date": date_str,
        "time": time_str,
        "total": get_total_transaction(df_selected_products),
        "products": df_selected_products.drop(columns=["barcode_data"]).to_dict(
            orient="records"
        ),
    }

    # Insert the transaction, and get the transaction _id
    transaction_id = str(insert_transaction_into_db(transaction_data))
    if not transaction_id:
        return "Error when inserting transaction"

    st.session_state.selected_products = []

    # generate receipt
    receipt = generate_receipt(df_selected_products, transaction_id)
    return receipt


# -- Receipt Generation --


def convert_pdf_to_base64(pdf_content):
    """
    Convert PDF content to a Base64-encoded string.

    Args:
        pdf_content (bytes): The content of the PDF file

    Returns:
        str: Base64-encoded string for displaying the PDF receipt using an iframe
    """
    base64_pdf = base64.b64encode(pdf_content).decode("utf-8")
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="900" type="application/pdf"></iframe>'
    return pdf_display


def prepare_dataframe(df_selected_products):
    """
    Structure dataframe of purchased products for the receipt.

    Args:
        df_selected_products (pd.DataFrame): DataFrame containing selected products.

    Returns:
        pd.Dataframe: Dataframe structured in the desired format for the receipt
    """
    df_selected_products = df_selected_products.drop(columns=["category"])
    df_selected_products = df_selected_products.rename(
        columns={
            "product_name": "product",
            "price": "price",
            "quantity": "qty",
        }
    )
    return df_selected_products


def generate_pdf_header(pdf):
    """
    Generate the header of the receipt.

    Args:
        pdf (FPDF): PDF object
    """
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, txt="Receipt", align='C')
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 11)


def add_date_time(pdf):
    """
    Add date and time of receipt generation.

    Args:
        pdf (FPDF): PDF object
    """
    now = datetime.now()
    formatted_date = now.strftime("%Y/%m/%d %H:%M:%S")
    pdf.cell(0, 8, txt=f"Receipt Generation Date: {formatted_date}")
    pdf.ln(8)


def add_headers(pdf):
    """
    Generate the header of the receipt.

    Args:
        pdf (FPDF): PDF object
    """
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(15, 8, txt="qty", border=1, fill=True)
    pdf.cell(145, 8, txt="product", border=1, fill=True)
    pdf.cell(30, 8, txt="price", border=1, fill=True)


def add_receipt_items(pdf, df_selected_products_formatted):
    """
    Add puchased products to the receipt from the dataframe.

    Args:
        pdf (FPDF): PDF object
        df_selected_products_formatted (pd.DataFrame): DataFrame containing selected products.
    """
    for _, row in df_selected_products_formatted.iterrows():
        pdf.ln(8)
        pdf.cell(15, 8, txt=str(row["qty"]), border=1)
        pdf.cell(145, 8, txt=row["product"], border=1)
        pdf.cell(30, 8, txt="{:.2f}".format(row["price"]), border=1)


def add_total(pdf, df_selected_products_formatted):
    """
    Calculate the total and add it to the receipt with some styling.

    Args:
        pdf (FPDF): PDF object
        df_selected_products_formatted (pd.DataFrame): DataFrame containing selected products.
    """
    pdf.ln(8)
    total = (
        df_selected_products_formatted["qty"] * df_selected_products_formatted["price"]
    ).sum()
    formatted_total = "{:.2f}".format(total)
    pdf.cell(160, 8, txt="Total", border=1)
    pdf.set_fill_color(174, 247, 173)
    pdf.cell(30, 8, txt=f"{formatted_total}", border=1, fill=True)


def add_transaction_id(pdf, transaction_id):
    """
    Add transaction ID of the purchase to the receipt.

    Args:
        pdf (FPDF): PDF object
        transaction_id (str): MongoDB Object ID of the transaction
    """
    pdf.ln(10)
    pdf.cell(15, 8, txt=f"Transaction ID: {transaction_id}")


def add_salesights_logo(pdf):
    """
    Add SaleSights Logo to bottom left corner of receipt.

    Args:
        pdf (FPDF): PDF object
    """
    pdf.image(
        os.path.join(LOGO_PATH),
        x=10,
        y=pdf.h - 20,
        w=40,
    )


def save_pdf(pdf):
    """
    Save pdf in RAM. This is OS dependent.

    Args:
        pdf (_type_): _description_

    Returns:
        bytes: A byte string containing the content of the generated PDF.
    """
    if platform.system() == "Windows":
        pdf_byte_string = pdf.output()
    else:
        pdf_byte_string = pdf.output(dest="S").encode("latin-1")

    return pdf_byte_string


def generate_receipt(df_selected_products, transaction_id):
    """
    Generate the pdf receipt.

    Args:
        df_selected_products (pd.DataFrame): DataFrame containing selected products.
        transaction_id (str): MongoDB Object ID of the transaction

    Returns:
        str: Base64-encoded string for displaying the PDF receipt using an iframe
    """
    df_selected_products_formatted = prepare_dataframe(df_selected_products)
    pdf = FPDF()
    pdf.add_page()

    generate_pdf_header(pdf)
    add_date_time(pdf)

    add_headers(pdf)
    add_receipt_items(pdf, df_selected_products_formatted)

    add_total(pdf, df_selected_products_formatted)

    add_transaction_id(pdf, transaction_id)
    add_salesights_logo(pdf)

    pdf_byte_string = save_pdf(pdf)

    iframe_base64_pdf = convert_pdf_to_base64(pdf_byte_string)

    return iframe_base64_pdf
