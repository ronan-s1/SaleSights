import os
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
from analytics.analytic_view import anlaytic_main
from home.home import home_main
from sales.sale_view import sale_main
from products.product_views import product_main
from transactions.transaction_view import transaction_main


LOGO_PATH = os.path.join("app", "static", "img", "salesights-logo.png")
LOGO_ICON_PATH = os.path.join("app", "static", "img", "salesights-title-icon.png")
CSS_PATH = os.path.join("app", "static", "css", "style.css")

st.set_page_config(page_title="SaleSights", page_icon=LOGO_ICON_PATH)


with open(CSS_PATH) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def get_logo_dimensions(dimensions, resize_multiplyer):
    width, height = dimensions
    width *= resize_multiplyer
    height *= resize_multiplyer

    return int(width), int(height)


def add_logo():
    logo = Image.open(LOGO_PATH)
    resize_multiplyer = 0.37
    width, height = get_logo_dimensions(logo.size, resize_multiplyer)
    modified_logo = logo.resize((width, height))
    return modified_logo


# service router
def main():
    salesights_logo = add_logo()
    st.sidebar.image(salesights_logo)

    pages = {
        "Home": {"page": home_main, "icon": "house"},
        "Sale": {"page": sale_main, "icon": "cart-check"},
        "Products": {"page": product_main, "icon": "basket"},
        "Transactions": {"page": transaction_main, "icon": "wallet2"},
        "Analytics": {"page": anlaytic_main, "icon": "graph-up"}
    }

    pages_list = list(pages.keys())
    icons_list = [pages[page]["icon"] for page in pages_list]

    with st.sidebar:
        selected_page = option_menu(
            menu_title=None, 
            options=pages_list, 
            icons=icons_list, 
            default_index=0
        )

    # Call the corresponding page based on the selected page
    if selected_page in pages:
        pages[selected_page]["page"]()


# Run the app
if __name__ == "__main__":
    main()
