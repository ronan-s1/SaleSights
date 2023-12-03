import os
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
from home.home import home_main
from sale.sale_view import sale_main
from products.product_views import product_main

st.set_page_config(page_title="SaleSights")

LOGO_PATH = os.path.join("static", "img", "salesights-logo.png")
CSS_PATH = os.path.join("static", "css", "style.css")

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
        "Home": {"function": home_main, "icon": "house"},
        "Sale": {"function": sale_main, "icon": "cart-check"},
        "Products": {"function": product_main, "icon": "basket"},
    }

    pages_list = list(pages.keys())
    icons_list = [pages[page]["icon"] for page in pages_list]

    with st.sidebar:
        selected_page = option_menu(
            menu_title=None, options=pages_list, icons=icons_list, default_index=0
        )

    # Call the corresponding function based on the selected page
    if selected_page in pages:
        pages[selected_page]["function"]()


# Run the app
if __name__ == "__main__":
    main()
