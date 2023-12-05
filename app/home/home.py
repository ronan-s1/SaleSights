import streamlit as st
from datetime import datetime
from home.home_controller import service_container, get_greeting


def home_main():
    st.title("SaleSight Services")

    greeting = get_greeting()

    st.write(greeting)

    col1, col2 = st.columns(2)

    with col1:
        sale_container = service_container(
            "fa fa-shopping-cart",
            "Sale",
            "Log a sale transaction and generate a receipt efficiently",
        )
        st.markdown(sale_container, unsafe_allow_html=True)

    with col2:
        product_container = service_container(
            "fa-solid fa-basket-shopping", "Products", "Manage your products with ease"
        )
        st.markdown(product_container, unsafe_allow_html=True)
