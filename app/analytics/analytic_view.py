import streamlit as st
import plotly.express as px
from utils import FIG_BLUE_BACKGROUND_COLOUR, FIG_RED_BACKGROUND_COLOUR
from analytics.analytic_controller import (
    get_avg_number_of_products_per_transaction,
    get_cat_qty_price,
    get_daily_total_expenses,
    get_expenses_by_day_of_week,
    get_sale_transactions_by_day_of_week,
    get_sales_over_time,
    get_transaction_totals,
    get_products_sales_qty,
    get_transactions_per_day,
    get_expenses_data,
)


def transactions_per_day_components(transactions_per_day_df):
    fig = px.line(
        transactions_per_day_df,
        x="date",
        y="transaction_count",
        title="Number of Daily Transactions",
        labels={"date": "Date", "transaction_count": "Transactions"},
    )

    fig.update_layout(
        plot_bgcolor=FIG_BLUE_BACKGROUND_COLOUR,
        xaxis_title="Date",
        yaxis_title="Number of Transactions",
    )

    st.plotly_chart(fig, use_container_width=True, config=dict(displaylogo=False))


def products_and_qty_components_components(products_and_qty_df):
    fig = px.bar(
        products_and_qty_df,
        y="product",
        x=["total quantity", "total sales"],
        orientation="h",
        title="Sales and Quanitity by Product",
        labels={"value": "Total", "variable": "Metric", "product": "Product"},
    )

    fig.update_layout(yaxis_title="Product", xaxis_title="Total")
    st.plotly_chart(fig, use_container_width=True, config=dict(displaylogo=False))


def kpi_components(
    transaction_total,
    transaction_total_avg,
    quantity_avg,
    average_transactions,
    avg_number_of_products_per_transaction,
):
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi4, kpi5, _ = st.columns(3)

    if transaction_total is not None:
        with kpi1:
            st.metric("Total Sales", transaction_total)

    if transaction_total_avg is not None:
        with kpi2:
            st.metric("Avg Transaction Value", transaction_total_avg)

    if quantity_avg is not None:
        with kpi3:
            st.metric("Avg Quantity Per Product", quantity_avg)

    if average_transactions is not None:
        with kpi4:
            st.metric("Avg Daily Transactions", average_transactions)

    if avg_number_of_products_per_transaction is not None:
        with kpi5:
            st.metric(
                "Avg Units Per Transaction (UPT)",
                avg_number_of_products_per_transaction,
            )

    return True


def daily_sales_components(sales_over_time_df):
    fig = px.line(
        sales_over_time_df,
        x="date",
        y="total_sales",
        title="Total Daily Sales Over Time",
        labels={"date": "Date", "total_sales": "Total"},
    )

    fig.update_layout(
        plot_bgcolor=FIG_BLUE_BACKGROUND_COLOUR,
        yaxis_title="Total Sales",
        xaxis_title="Date",
    )

    st.plotly_chart(fig, use_container_width=True, config=dict(displaylogo=False))


def cumulative_sales_components(cumulative_sales_df):
    fig = px.line(
        cumulative_sales_df,
        x="date",
        y="cumulative_sales",
        title="Cumulative Daily Sales Over Time",
        labels={"date": "Date", "cumulative_sales": "Cummulative Sales"},
    )

    fig.update_layout(
        plot_bgcolor=FIG_BLUE_BACKGROUND_COLOUR,
        yaxis_title="cumulative sales",
        xaxis_title="Date",
    )

    st.plotly_chart(fig, use_container_width=True, config=dict(displaylogo=False))


def category_bar_chart_components(category_qty_price_df):
    fig = px.bar(
        category_qty_price_df,
        x="category",
        y=["quantity", "total sales"],
        title="Sales and Quanitity by Category",
        labels={"value": "Total", "variable": "Metric", "category": "Category"},
        barmode="group",
    )
    st.plotly_chart(fig, use_container_width=True, config=dict(displaylogo=False))


def date_range_components():
    with st.expander("Select Date Range"):
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", format="YYYY/MM/DD", value=None)

        with col2:
            end_date = st.date_input("End Date", format="YYYY/MM/DD", value=None)

        return start_date, end_date


def expense_category_pie_chart_components(expense_category_df):
    fig = px.pie(
        expense_category_df,
        values="Count",
        names="Category",
        title="Expenses by Category",
        hover_data=["Total Expense Amount"],
        color_discrete_sequence=px.colors.sequential.Reds_r,
    )
    st.plotly_chart(fig, use_container_width=True, config=dict(displaylogo=False))


def total_expenses_line_chart_components(daily_total_expenses_df):
    fig = px.line(
        daily_total_expenses_df,
        x="expense_date",
        y="total_amount",
        title="Total Daily Expenses Over Time",
        color_discrete_sequence=px.colors.sequential.Reds_r,
        labels={"expense_date": "Date", "total_amount": "Total"},
    )

    fig.update_layout(
        plot_bgcolor=FIG_RED_BACKGROUND_COLOUR,
        yaxis_title="Total Expenses",
        xaxis_title="Expense Date",
    )

    st.plotly_chart(fig, use_container_width=True, config=dict(displaylogo=False))


def expenses_by_day_of_week_chart_components(expenses_by_day_of_week_df):
    fig = px.bar(
        expenses_by_day_of_week_df,
        x="day_of_week",
        y="total_amount",
        title="Total Expenses by Day of Week",
        labels={"day_of_week": "Day", "total_amount": "Total Expenses"},
        color_discrete_sequence=px.colors.sequential.Reds_r,
    )

    fig.update_layout(
        yaxis_title="Total Expenses",
        xaxis_title="Day of Week",
    )

    st.plotly_chart(fig, use_container_width=True, config=dict(displaylogo=False))


def sales_by_day_of_week_chart_components(transactions_by_day_of_week_df):
    fig = px.bar(
        transactions_by_day_of_week_df,
        x="day_of_week",
        y="total_amount",
        title="Total Sales by Day of Week",
        labels={"day_of_week": "Day", "total_amount": "Total Sales"},
    )

    fig.update_layout(
        yaxis_title="Total Sales",
        xaxis_title="Day of Week",
    )

    st.plotly_chart(fig, use_container_width=True, config=dict(displaylogo=False))


def analytic_main():
    st.title("Analytics and Insights 📊")
    start_date, end_date = date_range_components()

    if (start_date is None) or (end_date is None):
        st.stop()

    if start_date > end_date:
        st.error("Select a valid time range.")
        st.stop()

    # get quantity avg first to pass to kpi
    transaction_total, transaction_total_avg = get_transaction_totals(
        start_date, end_date
    )

    # get analytic data
    category_qty_price_total, quantity_avg = get_cat_qty_price(start_date, end_date)
    products_and_qty_df = get_products_sales_qty(start_date, end_date)
    sales_over_time_df, cumulative_sales_df = get_sales_over_time(start_date, end_date)
    transactions_per_day_df, average_transactions = get_transactions_per_day(
        start_date, end_date
    )
    avg_number_of_products_per_transaction = get_avg_number_of_products_per_transaction(
        start_date, end_date
    )
    expense_category_df = get_expenses_data(start_date, end_date)
    daily_total_expenses_df = get_daily_total_expenses(start_date, end_date)
    expenses_by_day_of_week_df = get_expenses_by_day_of_week(start_date, end_date)
    transactions_by_day_of_week_df = get_sale_transactions_by_day_of_week(
        start_date, end_date
    )

    # st.write(transactions_by_day_of_week_df)
    # return
    # display data
    kpi_components(
        transaction_total,
        transaction_total_avg,
        quantity_avg,
        average_transactions,
        avg_number_of_products_per_transaction,
    )

    if not category_qty_price_total.empty:
        category_bar_chart_components(category_qty_price_total)
    else:
        st.warning("No sales found for the selected date range.")

    if not products_and_qty_df.empty:
        products_and_qty_components_components(products_and_qty_df)
    else:
        st.warning("No sales found for the selected date range.")

    if not cumulative_sales_df.empty:
        cumulative_sales_components(cumulative_sales_df)
    else:
        st.warning("No sales found for the selected date range.")

    if not sales_over_time_df.empty:
        daily_sales_components(sales_over_time_df)
    else:
        st.warning("No sales found for the selected date range.")

    if not transactions_by_day_of_week_df.empty:
        sales_by_day_of_week_chart_components(transactions_by_day_of_week_df)
    else:
        st.warning("No sales found for the selected date range.")

    if not transactions_per_day_df.empty:
        transactions_per_day_components(transactions_per_day_df)
    else:
        st.warning("No transactions found for the selected date range.")

    st.divider()

    if not expense_category_df.empty:
        expense_category_pie_chart_components(expense_category_df)
    else:
        st.warning("No expenses found for the selected date range.")

    if not daily_total_expenses_df.empty:
        total_expenses_line_chart_components(daily_total_expenses_df)
    else:
        st.warning("No expenses found for the selected date range.")

    if not expenses_by_day_of_week_df.empty:
        expenses_by_day_of_week_chart_components(expenses_by_day_of_week_df)
    else:
        st.warning("No expenses found for the selected date range.")
