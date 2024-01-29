import streamlit as st
import plotly.express as px
from utils import FIG_BLUE_BACKGROUND_COLOUR
from analytics.analytic_controller import (
    get_cat_qty_price,
    get_sales_over_time, 
    get_transaction_totals,
    get_products_sales_qty
)


def products_and_qty_components(products_and_qty_df):
    with st.expander("Products and Quantity Sold"):
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


def daily_sales_components(sales_over_time_df):
    fig = px.line(sales_over_time_df, x="date", y="total sales", title="Total Daily Sales Over Time")
    fig.update_layout(plot_bgcolor=FIG_BLUE_BACKGROUND_COLOUR)
    st.plotly_chart(fig, use_container_width=True)
    

def cumulative_sales_components(cumulative_sales_df):
    fig = px.line(cumulative_sales_df, x="date", y="cumulative sales", title="Cumulative Daily Sales Over Time")
    fig.update_layout(plot_bgcolor=FIG_BLUE_BACKGROUND_COLOUR)
    st.plotly_chart(fig, use_container_width=True)


def category_bar_chart_components(category_qty_price_df):
    fig = px.bar(
        category_qty_price_df,
        x="category",
        y=["quantity", "total sales"],
        title="Product Sales by Category",
        labels={"value": "Total", "variable": "Metric"},
        barmode="group"
    )
    st.plotly_chart(fig, use_container_width=True)


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
        st.stop()

    if start_date > end_date:
        st.error("Select a valid time range.")
        st.stop()

    # get quantity avg first to pass to kpi
    transaction_total, transaction_total_avg = get_transaction_totals(start_date, end_date)
    
    if isinstance(transaction_total, str):
        st.error(transaction_total)
        st.stop()
    
    # get analytic data
    category_qty_price_total, quantity_avg = get_cat_qty_price(start_date, end_date)
    products_and_qty_df = get_products_sales_qty(start_date, end_date)
    sales_over_time_df, cumulative_sales_df = get_sales_over_time(start_date, end_date)

    # display data
    kpi_components(transaction_total, transaction_total_avg, quantity_avg)    
    products_and_qty_components(products_and_qty_df)
    category_bar_chart_components(category_qty_price_total)
    daily_sales_components(sales_over_time_df)
    cumulative_sales_components(cumulative_sales_df)    
