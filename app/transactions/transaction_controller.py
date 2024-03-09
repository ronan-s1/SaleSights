import streamlit as st
from transactions.transaction_data import (
    fetch_sale_transactions,
)


def get_transactions():
    """
    Get the transactions.

    Returns:
        transactions (list): list of transactions
    """
    return fetch_sale_transactions()


def structure_transaction_products(transaction):
    """
    Structure the transaction products.

    Args:
        transaction (dict): transaction data

    Returns:
        products_data (list): list of products in the transaction
    """
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
    """
    Filter transactions by id.

    Args:
        transactions (list): list of transactions
        search_id (str): search id

    Returns:
        search_result (list): list of transactions that match the search id
    """
    search_id_lower = search_id.lower()
    search_result = [
        transaction
        for transaction in transactions
        if search_id_lower in str(transaction["_id"]).lower()
    ]

    st.session_state.current_page = 1
    return search_result


def get_index(page_size):
    """
    Get the start and end index of the current page.

    Args:
        page_size (int): number of transactions per page

    Returns:
        start_idx (int): start index of the current page
        end_idx (int): end index of the current page
    """
    start_idx = (st.session_state.current_page - 1) * page_size
    end_idx = start_idx + page_size

    return start_idx, end_idx


def get_total_pages(page_size, transactions):
    """
    Get the total number of pages.

    Args:
        page_size (int): number of transactions per page
        transactions (list): list of transactions

    Returns:
        total_pages (int): total number of pages
    """
    total_pages = len(transactions) // page_size + (len(transactions) % page_size > 0)

    return total_pages


def prev_page():
    """
    Move to the previous page.
    """
    if st.session_state.current_page > 1:
        st.session_state.current_page -= 1


def next_page():
    """
    Move to the next page.
    """
    st.session_state.current_page += 1
