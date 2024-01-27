import streamlit as st
import plotly.express as px
from utils import FIG_BLUE_BACKGROUND_COLOUR
from analytics.analytic_controller import (
    get_cat_qty_price,
    get_sales_over_time, 
    get_transaction_totals,
    get_products_and_qty
)


def products_and_qty_components(products_and_qty_df):
    st.subheader("Products and Quantity Sold")
    st.dataframe(products_and_qty_df, use_container_width=True)


def kpi_components(transaction_total, transaction_total_avg, quantity_avg):
    kpi1, kpi2, kpi3 = st.columns(3)

    with kpi1:
        st.metric("Total Sales", transaction_total)

    with kpi2:
        st.metric("Average Transaction Value", transaction_total_avg)

    with kpi3:
        st.metric("Average Quantity Per Product", quantity_avg)

    return True


def sales_over_time_components(sales_over_time_df):
    fig = px.line(sales_over_time_df, x="date", y="total_sales", title="Total Sales Per Day Over Time")
    fig.update_layout(
        plot_bgcolor=FIG_BLUE_BACKGROUND_COLOUR
    )
    st.plotly_chart(fig)


def category_bar_chart_components(category_qty_price_df):
    fig = px.bar(
        category_qty_price_df,
        x="category",
        y=["quantity", "price"],
        title="Product Sales by Category",
        labels={"value": "Total", "variable": "Metric"},
        barmode="group"
    )
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

    # get quantity avg first to pass to kpi
    transaction_total, transaction_total_avg = get_transaction_totals(start_date, end_date)
    
    if isinstance(transaction_total, str):
        st.error(transaction_total)
        return False
    
    # get analytic data
    category_qty_price_total, quantity_avg = get_cat_qty_price(start_date, end_date)
    products_and_qty_df = get_products_and_qty(start_date, end_date)
    sales_over_time_df = get_sales_over_time(start_date, end_date)

    # display data
    kpi_components(transaction_total, transaction_total_avg, quantity_avg)
    category_bar_chart_components(category_qty_price_total)
    products_and_qty_components(products_and_qty_df)
    sales_over_time_components(sales_over_time_df)
