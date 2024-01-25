import pandas as pd
from analytics.analytic_data import fetch_cat_and_qty, fetch_transaction_totals


def format_date(start_date, end_date):
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    return start_date_str, end_date_str


def get_cat_and_qty(start_date, end_date):
    start_date_str, end_date_str = format_date(start_date, end_date)
    transactions = fetch_cat_and_qty(start_date_str, end_date_str)

    # group by category and sum the quantities
    product_category_df = pd.DataFrame(transactions)
    category_totals = (
        product_category_df.groupby("category")["quantity"].sum().reset_index()
    )

    return category_totals


def get_transaction_totals(start_date, end_date):
    start_date_str, end_date_str = format_date(start_date, end_date)
    transaction_totals = fetch_transaction_totals(start_date_str, end_date_str)
    totals_df = pd.DataFrame(transaction_totals)

    # check if theres data
    if totals_df.empty:
        return f"No records between {start_date} and {end_date}"

    total_sum = round(totals_df["total"].sum(), 2)
    return total_sum
