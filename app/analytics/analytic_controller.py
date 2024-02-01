import pandas as pd
from analytics.analytic_data import (
    fetch_cat_qty_price,
    fetch_transaction_totals,
    fetch_products_sales_qty,
    fetch_sales_over_time,
    fetch_transactions_per_day,
    fetch_number_of_products_per_transaction
)


def format_date(start_date, end_date):
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    return start_date_str, end_date_str


def get_cat_qty_price(start_date, end_date):
    start_date_str, end_date_str = format_date(start_date, end_date)
    transactions = fetch_cat_qty_price(start_date_str, end_date_str)

    product_category_df = pd.DataFrame(transactions)
    product_category_df = product_category_df.rename(columns={"price": "total sales"})

    # group by category and sum the quantities and prices
    category_qty_price_total = (
        product_category_df.groupby("category")[["quantity", "total sales"]]
        .sum()
        .reset_index()
    )

    # get avg quantity per transaction
    quantity_avg = round(product_category_df["quantity"].mean())

    return category_qty_price_total, quantity_avg


def get_transaction_totals(start_date, end_date):
    start_date_str, end_date_str = format_date(start_date, end_date)
    transaction_totals = fetch_transaction_totals(start_date_str, end_date_str)
    totals_df = pd.DataFrame(transaction_totals)

    # check if there's data
    if totals_df.empty:
        return f"No records between {start_date} and {end_date}", None

    # get average and total for transaction totals
    total_sum = round(totals_df["total"].sum(), 2)
    total_avg = round(totals_df["total"].mean(), 2)

    return total_sum, total_avg


def get_products_sales_qty(start_date, end_date):
    start_date_str, end_date_str = format_date(start_date, end_date)
    products_and_qty = fetch_products_sales_qty(start_date_str, end_date_str)

    # rename columns in df
    products_and_qty_df = pd.DataFrame(products_and_qty)
    products_and_qty_df = products_and_qty_df.rename(
        columns={
            "total_quantity": "total quantity",
            "product_name": "product",
            "total_sales": "total sales",
        }
    )

    # reorganise column order
    columns_order = ["product", "total quantity", "total sales"]
    products_and_qty_df = products_and_qty_df[columns_order]
    products_and_qty_df = products_and_qty_df.sort_values(
        by="total sales", ascending=True
    )

    return products_and_qty_df


def calculate_cumulative_sales(df):
    df["cumulative_sales"] = df["total_sales"].cumsum()
    return df


def get_sales_over_time(start_date, end_date):
    start_date_str, end_date_str = format_date(start_date, end_date)
    sales_over_time = fetch_sales_over_time(start_date_str, end_date_str)

    # create df and remove underscores
    sales_over_time_df = pd.DataFrame(sales_over_time)
    cumulative_sales_df = calculate_cumulative_sales(sales_over_time_df)

    return sales_over_time_df, cumulative_sales_df


def get_transactions_per_day(start_date, end_date):
    start_date_str, end_date_str = format_date(start_date, end_date)
    transactions_per_day = fetch_transactions_per_day(start_date_str, end_date_str)

    transactions_per_day_df = pd.DataFrame(transactions_per_day)
    average_transactions = round(transactions_per_day_df["transaction_count"].mean())

    return transactions_per_day_df, average_transactions


def get_avg_number_of_products_per_transaction(start_date, end_date):
    start_date_str, end_date_str = format_date(start_date, end_date)
    products_per_transaction = fetch_number_of_products_per_transaction(start_date_str, end_date_str)
    
    products_per_transaction_df = pd.DataFrame(products_per_transaction)
    avg_number_of_products_per_transaction = round(products_per_transaction_df["num_products"].mean())
    
    return avg_number_of_products_per_transaction