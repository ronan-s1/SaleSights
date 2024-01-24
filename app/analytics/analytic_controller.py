import pandas as pd
from analytics.analytic_data import (
    fetch_cat_and_qty,
)


def get_cat_and_qty(start_date, end_date):
    transactions = list(fetch_cat_and_qty(start_date, end_date))
    product_category_df = pd.DataFrame(transactions)

    # group by category and sum the quantities
    category_totals = product_category_df.groupby("category")["quantity"].sum().reset_index()

    return category_totals

