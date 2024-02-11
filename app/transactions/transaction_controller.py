import streamlit as st
from transactions.transaction_data import (
    fetch_sale_transactions,
)


def get_transactions():
    return fetch_sale_transactions()


def structure_transaction_products(transaction):
    products_data = [
        {
            "Product Name": product["product_name"],
            "Category": product["category"],
            "Price": product["price"],
            "Quantity": product["quantity"],
        }
        for product in transaction["products"]
    ]

    return products_data


def filter_by_id(transactions, search_id):
    search_id_lower = search_id.lower()
    search_result = [
        transaction
        for transaction in transactions
        if search_id_lower in str(transaction["_id"]).lower()
    ]

    st.session_state.current_page = 1
    return search_result


def get_index(page_size):
    start_idx = (st.session_state.current_page - 1) * page_size
    end_idx = start_idx + page_size

    return start_idx, end_idx


def get_total_pages(page_size, transactions):
    total_pages = len(transactions) // page_size + (len(transactions) % page_size > 0)

    return total_pages


def prev_page():
    if st.session_state.current_page > 1:
        st.session_state.current_page -= 1


def next_page():
    st.session_state.current_page += 1
