import streamlit as st
from home.home_controller import service_container, get_greeting, start_connection


def home_main():
    """
    The home page view, display info about the services

    Return:
        None
    """
    greeting = get_greeting()
    st.markdown(f"### {greeting}")

    col1, col2 = st.columns(2)

    with col1:
        sale_container = service_container(
            "fa fa-shopping-cart",
            "Sale",
            "Efficiently log sale transactions and generate receipts",
        )
        st.markdown(sale_container, unsafe_allow_html=True)

        transaction_container = service_container(
            "fa fa-exchange", "Transactions", "View and find past transactions swiftly"
        )
        st.markdown(transaction_container, unsafe_allow_html=True)

        expenses_container = service_container(
            "fa fa-money-bill-transfer",
            "Expenses",
            "Track your expenses and upload receipts easily",
        )
        st.markdown(expenses_container, unsafe_allow_html=True)

    with col2:
        product_container = service_container(
            "fa-solid fa-basket-shopping", "Products", "Manage your products with ease"
        )
        st.markdown(product_container, unsafe_allow_html=True)

        analytics_container = service_container(
            "fa fa-line-chart",
            "Analytics",
            "See insights and metrics on your business data",
        )
        st.markdown(analytics_container, unsafe_allow_html=True)

        biz_container = service_container(
            "fa fa-robot",
            "Biz",
            "Ask questions on your data using state-of-the-art AI",
        )
        st.markdown(biz_container, unsafe_allow_html=True)

    st.write("Need help? See our [docs](https://salesights.xyz).")
    start_connection()
