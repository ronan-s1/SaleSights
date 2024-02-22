import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image

from analytics.analytic_view import analytic_main
from biz.biz_view import biz_main
from home.home_view import home_main
from sales.sale_view import sale_main
from products.product_views import product_main
from transactions.transaction_view import transaction_main
from expenses.expense_view import expense_main
from settings.settings_view import settings_main

from utils import CSS_PATH, LOGO_ICON_PATH, LOGO_PATH

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
        "Transactions": {"page": transaction_main, "icon": "arrow-left-right"},
        "Analytics": {"page": analytic_main, "icon": "graph-up"},
        "Expenses": {"page": expense_main, "icon": "wallet"},
        "Biz": {"page": biz_main, "icon": "robot"},
        "Settings": {"page": settings_main, "icon": "gear"},
    }

    pages_list = list(pages.keys())
    icons_list = [pages[page]["icon"] for page in pages_list]

    with st.sidebar:
        selected_page = option_menu(
            menu_title=None, options=pages_list, icons=icons_list, default_index=0
        )

    # Call the corresponding page based on the selected page
    if selected_page in pages:
        pages[selected_page]["page"]()


# Run the app
if __name__ == "__main__":
    main()
