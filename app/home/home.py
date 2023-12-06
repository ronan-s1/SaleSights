import streamlit as st
from home.home_controller import service_container, get_greeting


def home_main():
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

    with col2:
        product_container = service_container(
            "fa-solid fa-basket-shopping", "Products", "Manage your products with ease"
        )
        st.markdown(product_container, unsafe_allow_html=True)

    st.write("Need help? See our [docs](https://salesights.xyz).")
