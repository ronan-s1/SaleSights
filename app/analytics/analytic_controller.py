import pandas as pd

from analytics.analytic_data import (
    fetch_cat_and_qty,
)


# def get_transactions():
#     transactions = fetch_sale_transactions()
#     return list(transactions)


def get_cat_and_qty(start_date, end_date):
    transactions = list(fetch_cat_and_qty(start_date, end_date))
    product_category_df = pd.DataFrame(transactions)
    return product_category_df
