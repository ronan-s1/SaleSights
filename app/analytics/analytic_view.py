import pandas as pd
import datetime
import streamlit as st
from analytics.analytic_controller import get_cat_and_qty
import plotly.express as px


def analytic_main():
    st.title("Monthly Product Sales by Category")
    start_date = "2024-01-24"
    end_date = "2024-01-24"

    data = get_cat_and_qty(start_date, end_date)
    st.dataframe(data, use_container_width=True)

 

