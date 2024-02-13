import os

import streamlit as st


LOGO_PATH = os.path.join("app", "static", "img", "salesights-logo.png")
LOGO_ICON_PATH = os.path.join("app", "static", "img", "salesights-title-icon.png")
CSS_PATH = os.path.join("app", "static", "css", "style.css")
FIG_BLUE_BACKGROUND_COLOUR = "#f7f8ff"


def v_spacer(height):
    for _ in range(height):
        st.write("\n")
