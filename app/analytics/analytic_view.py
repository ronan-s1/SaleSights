import streamlit as st
import plotly.express as px
from analytics.analytic_controller import get_cat_and_qty, get_transaction_totals


def kpi_components(start_date, end_date):
    transaction_total = get_transaction_totals(start_date, end_date)
    if isinstance(transaction_total, str):
        st.error(transaction_total)
        return False

    kpi1, kpi2, kpi3 = st.columns(3)

    with kpi1:
        st.metric("Total Sales", transaction_total)

    return True


def category_bar_chart_components(start_date, end_date):
    data = get_cat_and_qty(start_date, end_date)
    fig = px.bar(data, x="category", y="quantity", title="Product Sales by Category")
    st.plotly_chart(fig)


def date_range_components():
    with st.expander("Select Date Range"):
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", format="YYYY/MM/DD", value=None)

        with col2:
            end_date = st.date_input("End Date", format="YYYY/MM/DD", value=None)

        return start_date, end_date


def analytic_main():
    st.title("Analytics and Insights 📊")
    start_date, end_date = date_range_components()

    if (start_date is None) or (end_date is None):
        return

    if start_date > end_date:
        st.error("Select a valid time range.")
        return

    # if there's no records for entered date range
    data = kpi_components(start_date, end_date)
    if not data:
        return

    category_bar_chart_components(start_date, end_date)
