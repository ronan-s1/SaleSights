from datetime import datetime
import streamlit as st
from transactions.transaction_controller import (
    filter_by_id,
    get_index,
    get_total_pages,
    get_transactions,
    structure_transaction_products,
    next_page,
    prev_page,
)


def display_transaction_components():
    page_size = 5
    transactions = list(get_transactions())

    if not transactions:
        st.error("No transactions.")
        return

    # filter transactions based on the entered ID
    search_id = st.text_input("Search by ID:")
    if search_id:
        transactions = filter_by_id(transactions, search_id)

    total_pages = get_total_pages(page_size, transactions)

    # columns for prev and next buttons
    col1, col2 = st.columns([10, 1])
    with col1:
        if st.session_state.current_page > 1:
            st.button("Previous", on_click=prev_page)

    with col2:
        if st.session_state.current_page < total_pages:
            st.button("Next", on_click=next_page)

    # start and end index for transactions list
    start_idx, end_idx = get_index(page_size)

    # display transactions for the current page
    for transaction in transactions[start_idx:end_idx]:
        formatted_date = f"{datetime.strptime(transaction['date'], '%Y-%m-%d').strftime('%B %d, %Y')} {transaction['time']}"
        with st.expander(formatted_date):
            st.write(f"ID: {transaction['_id']}")
            st.write(f"Total: {transaction['total']}")
            st.table(structure_transaction_products(transaction))

    # display current page info
    st.write(f"Page {st.session_state.current_page} of {total_pages}")


def transaction_main():
    st.title("View Sale Transactions🧾")

    if "current_page" not in st.session_state:
        st.session_state.current_page = 1

    display_transaction_components()
