import pandas as pd
from analytics.analytic_data import (
    fetch_cat_qty_price,
    fetch_daily_total_expenses,
    fetch_expenses,
    fetch_expenses_by_day_of_week,
    fetch_transaction_totals,
    fetch_products_sales_qty,
    fetch_sales_over_time,
    fetch_transactions_per_day,
    fetch_number_of_products_per_transaction,
    fetch_sale_transactions_by_day_of_week,
)


def format_date(start_date, end_date):
    """
    Format the start and end date to a string

    Args:
        start_date (datetime): start date in datetime format
        end_date (datetime): end date in datetime format

    Returns:
        start_date_str (str): start date as a string
        end_date_str (str): end date as a string
    """
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    return start_date_str, end_date_str


def get_cat_qty_price(start_date, end_date):
    """
    Get the category, quantity and price of products sold

    Args:
        start_date (datetime): start date
        end_date (datetime): end date

    Returns:
        category_qty_price_total (DataFrame): category, quantity and price of products sold
        quantity_avg (int): average quantity per transaction
    """
    start_date_str, end_date_str = format_date(start_date, end_date)
    transactions = fetch_cat_qty_price(start_date_str, end_date_str)

    product_category_df = pd.DataFrame(transactions)

    if product_category_df.empty:
        return product_category_df, None

    product_category_df = product_category_df.rename(columns={"price": "total sales"})

    # group by category and sum the quantities and prices
    category_qty_price_total = (
        product_category_df.groupby("category")[["quantity", "total sales"]]
        .sum()
        .reset_index()
    )

    # get avg quantity per transaction
    quantity_avg = round(product_category_df["quantity"].mean(), 2)

    return category_qty_price_total, quantity_avg


def get_transaction_totals(start_date, end_date):
    """
    Get the total sum and average of transaction totals.

    Args:
        start_date (datetime): start date
        end_date (datetime): end date

    Returns:
        total_sum (float): total sum of transaction totals
        total_avg (float): average of transaction totals
    """
    start_date_str, end_date_str = format_date(start_date, end_date)
    transaction_totals = fetch_transaction_totals(start_date_str, end_date_str)
    totals_df = pd.DataFrame(transaction_totals)

    # check if there's data
    if totals_df.empty:
        return None, None

    # get average and total for transaction totals
    total_sum = round(totals_df["total"].sum(), 2)
    total_avg = round(totals_df["total"].mean(), 2)

    return total_sum, total_avg


def get_products_sales_qty(start_date, end_date):
    """
    Get the products, total quantity and total sales. Sort by total sales.

    Args:
        start_date (datetime): start date
        end_date (datetime): end date

    Returns:
        products_and_qty_df (DataFrame): products, total quantity and total sales
    """
    start_date_str, end_date_str = format_date(start_date, end_date)
    products_and_qty = fetch_products_sales_qty(start_date_str, end_date_str)

    # rename columns in df
    products_and_qty_df = pd.DataFrame(products_and_qty)

    if products_and_qty_df.empty:
        return products_and_qty_df

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
    """
    Calculate the cumulative sales for each row in the dataframe.

    Args:
        df (DataFrame): dataframe with sales data.

    Returns:
        df (DataFrame): dataframe with cumulative sales column.
    """
    df["cumulative_sales"] = df["total_sales"].cumsum()

    return df


def get_sales_over_time(start_date, end_date):
    """
    Get the sales over time and the cumulative sales.

    Args:
        start_date (datetime): start date
        end_date (datetime): end date

    Returns:
        sales_over_time_df (DataFrame): sales over time
        cumulative_sales_df (DataFrame): cumulative sales
    """
    start_date_str, end_date_str = format_date(start_date, end_date)
    sales_over_time = fetch_sales_over_time(start_date_str, end_date_str)

    # create df and remove underscores
    sales_over_time_df = pd.DataFrame(sales_over_time)

    if sales_over_time_df.empty:
        return sales_over_time_df, sales_over_time_df

    cumulative_sales_df = calculate_cumulative_sales(sales_over_time_df)

    return sales_over_time_df, cumulative_sales_df


def get_transactions_per_day(start_date, end_date):
    """
    Get the transactions per day and the average transactions per day.

    Args:
        start_date (datetime): start date
        end_date (datetime): end date

    Returns:
        transactions_per_day_df (DataFrame): transactions per day
    """
    start_date_str, end_date_str = format_date(start_date, end_date)
    transactions_per_day = fetch_transactions_per_day(start_date_str, end_date_str)

    transactions_per_day_df = pd.DataFrame(transactions_per_day)

    if transactions_per_day_df.empty:
        return transactions_per_day_df, None

    average_transactions = round(transactions_per_day_df["transaction_count"].mean(), 2)

    return transactions_per_day_df, average_transactions


def get_avg_number_of_products_per_transaction(start_date, end_date):
    """
    Get the average number of products per transaction.

    Args:
        start_date (datetime): start date
        end_date (datetime): end date

    Returns:
        avg_number_of_products_per_transaction (float): average number of products per transaction
    """
    start_date_str, end_date_str = format_date(start_date, end_date)
    products_per_transaction = fetch_number_of_products_per_transaction(
        start_date_str, end_date_str
    )

    products_per_transaction_df = pd.DataFrame(products_per_transaction)

    if products_per_transaction_df.empty:
        return None

    avg_number_of_products_per_transaction = round(
        products_per_transaction_df["num_products"].mean(), 2
    )

    return float(avg_number_of_products_per_transaction)


def get_sale_transactions_by_day_of_week(start_date, end_date):
    """
    Get the sale transactions by day of week.

    Args:
        start_date (datetime): start date
        end_date (datetime): end date

    Returns:
        transactions_by_day_of_week_df (DataFrame): sale transactions by day of week
    """
    start_date_str, end_date_str = format_date(start_date, end_date)
    transactions_by_day_of_week = fetch_sale_transactions_by_day_of_week(
        start_date_str, end_date_str
    )

    transactions_by_day_of_week_df = pd.DataFrame(transactions_by_day_of_week)

    if transactions_by_day_of_week_df.empty:
        return transactions_by_day_of_week_df

    # Map numerical day of week to day name
    day_of_week_map = {
        2: "Monday",
        3: "Tuesday",
        4: "Wednesday",
        5: "Thursday",
        6: "Friday",
        7: "Saturday",
        1: "Sunday",
    }
    transactions_by_day_of_week_df["day_of_week"] = transactions_by_day_of_week_df[
        "day_of_week"
    ].map(day_of_week_map)

    return transactions_by_day_of_week_df


def get_expenses_data(start_date, end_date):
    """
    Get the expenses data.

    Args:
        start_date (datetime): start date
        end_date (datetime): end date

    Returns:
        final_df (DataFrame): DataFrame with "Count", "Category", and "Total Expense Amount" columns
    """
    start_date_str, end_date_str = format_date(start_date, end_date)
    expenses = fetch_expenses(start_date_str, end_date_str)
    expenses_df = pd.DataFrame(expenses)

    if expenses_df.empty:
        return expenses_df

    # calc the count for each category
    category_distribution_df = expenses_df["category"].value_counts().reset_index()
    category_distribution_df.columns = ["Category", "Count"]

    # calc total for each category
    category_totals_df = (
        expenses_df.groupby("category")["amount"].sum().round(2).reset_index()
    )
    category_totals_df.columns = ["Category", "Total Expense Amount"]

    # Merge the 2 dfs on category
    final_df = pd.merge(category_distribution_df, category_totals_df, on="Category")

    return final_df


def get_daily_total_expenses(start_date, end_date):
    """
    Get the daily total expenses. Calls a function from data access that aggregates the total expenses by summing up the amount field for each day using the expense_date field.

    Args:
        start_date (datetime): start date
        end_date (datetime): end date

    Returns:
        daily_total_expenses_df (DataFrame): daily total expenses
    """
    start_date_str, end_date_str = format_date(start_date, end_date)
    daily_total_expenses = fetch_daily_total_expenses(start_date_str, end_date_str)

    daily_total_expenses_df = pd.DataFrame(daily_total_expenses)
    return daily_total_expenses_df


def get_expenses_by_day_of_week(start_date, end_date):
    """
    Get the total expenses by day of week.

    Args:
        start_date (datetime): start date
        end_date (datetime): end date

    Returns:
        expenses_by_day_of_week_df (DataFrame): total expenses by day of week
    """
    start_date_str, end_date_str = format_date(start_date, end_date)
    expenses_by_day_of_week = fetch_expenses_by_day_of_week(
        start_date_str, end_date_str
    )

    # Replace numerical day of week with day names
    expenses_by_day_of_week_df = pd.DataFrame(expenses_by_day_of_week)

    if expenses_by_day_of_week_df.empty:
        return expenses_by_day_of_week_df

    # Map numerical day of week to day name
    day_of_week_map = {
        2: "Monday",
        3: "Tuesday",
        4: "Wednesday",
        5: "Thursday",
        6: "Friday",
        7: "Saturday",
        1: "Sunday",
    }
    expenses_by_day_of_week_df["day_of_week"] = expenses_by_day_of_week_df[
        "day_of_week"
    ].map(day_of_week_map)

    return expenses_by_day_of_week_df
