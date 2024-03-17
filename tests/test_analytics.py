import switch_path
from datetime import datetime
import pandas as pd
import pytest
from analytics.analytic_controller import (
    format_date,
    get_transaction_totals,
    get_avg_number_of_products_per_transaction,
    get_daily_total_expenses,
    get_sale_transactions_by_day_of_week,
    get_expenses_by_day_of_week,
    get_expenses_data,
    get_transactions_per_day,
    get_products_sales_qty,
    get_cat_qty_price,
    get_sales_over_time,
)


def test_format_date():
    # Test formatting of start and end date
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 1, 31)
    start_date_str, end_date_str = format_date(start_date, end_date)
    assert start_date_str == "2022-01-01"
    assert end_date_str == "2022-01-31"


def test_get_transaction_totals():
    # Test total sum and average of transactions
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 1)
    total_sum, total_avg = get_transaction_totals(start_date, end_date)
    assert total_sum == 300
    assert total_avg == 50

    # Test date with no transactions
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 1, 1)
    total_sum, total_avg = get_transaction_totals(start_date, end_date)
    assert total_sum == None
    assert total_avg == None


def test_get_avg_number_of_products_per_transaction():
    # Test average number of products per transaction
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 1)
    avg_products = get_avg_number_of_products_per_transaction(start_date, end_date)
    assert avg_products == 4

    # Test date with no transactions
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 1, 1)
    avg_products = get_avg_number_of_products_per_transaction(start_date, end_date)
    assert avg_products == None


def test_get_sale_transactions_by_day_of_week():
    # Test sale transactions by day of week
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 1)

    expected_df = pd.DataFrame({"total_amount": [300], "day_of_week": ["Monday"]})

    sale_transactions_by_day_of_week_df = get_sale_transactions_by_day_of_week(
        start_date, end_date
    )
    assert sale_transactions_by_day_of_week_df.equals(expected_df)

    # Test when transactions_by_day_of_week_df is empty
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 1, 1)
    result = get_sale_transactions_by_day_of_week(start_date, end_date)
    assert result.empty


def test_get_daily_total_expenses():
    # Test daily total expenses
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 1)

    expected_df = pd.DataFrame({"total_amount": [200], "expense_date": ["2024-01-01"]})

    daily_expenses = get_daily_total_expenses(start_date, end_date)
    assert daily_expenses.equals(expected_df)

    # Test date with no transactions
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 1, 1)
    daily_expenses = get_daily_total_expenses(start_date, end_date)
    assert daily_expenses.empty


def test_get_expenses_by_day_of_week():
    # Test expenses by day of week
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 1)

    expected_df = pd.DataFrame({"total_amount": [200], "day_of_week": ["Monday"]})

    expenses_by_day_of_week_df = get_expenses_by_day_of_week(start_date, end_date)
    assert expenses_by_day_of_week_df.equals(expected_df)

    # Test when expenses_by_day_of_week_df is empty
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 1, 1)
    result = get_expenses_by_day_of_week(start_date, end_date)
    assert result.empty


def test_get_expenses_data():
    # Test expenses data
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 1)

    expected_df = pd.DataFrame(
        {"Category": ["Packaging"], "Count": [4], "Total Expense Amount": [200]}
    )

    expenses_data = get_expenses_data(start_date, end_date)
    assert expenses_data.equals(expected_df)

    # Test when expenses_data is empty
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 1, 1)
    expense_data_df = get_expenses_data(start_date, end_date)
    assert expense_data_df.empty


def test_get_transactions_per_day():
    # Test transactions per day
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 1)

    expected_df = pd.DataFrame({"transaction_count": [6], "date": ["2024-01-01"]})

    transactions_per_day_df, average_transactions = get_transactions_per_day(
        start_date, end_date
    )
    assert transactions_per_day_df.equals(expected_df)
    assert average_transactions == 6

    # Test date with no transactions
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 1, 1)
    transactions_per_day_df, average_transactions = get_transactions_per_day(
        start_date, end_date
    )
    assert transactions_per_day_df.empty
    assert average_transactions == None


def test_get_products_sales_qty():
    # Test products sales quantity
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 1)

    expected_df = pd.DataFrame(
        {
            "product": [
                "Gluten-Free Quinoa Pasta",
                "Natural Almond Butter",
                "Vitamin D3 Supplement",
                "Charcoal Infused Toothpaste",
            ],
            "total quantity": [6, 18, 12, 24],
            "total sales": [41.94, 66.42, 71.88, 119.76],
        }
    )

    products_and_qty_df = get_products_sales_qty(start_date, end_date)

    # Sort the dataframes to compare
    expected_df = expected_df.sort_values(by="product").reset_index(drop=True)
    products_and_qty_df = products_and_qty_df.sort_values(by="product").reset_index(
        drop=True
    )

    assert products_and_qty_df.equals(expected_df)

    # Test date with no transactions
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 1, 1)
    products_and_qty_df = get_products_sales_qty(start_date, end_date)
    assert products_and_qty_df.empty


def test_get_cat_qty_price():
    # Test category quantity and price
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 1)

    expected_df = pd.DataFrame(
        {
            "category": ["Food", "Personal Care", "Supplements"],
            "quantity": [24, 24, 12],
            "total sales": [64.08, 29.94, 35.94],
        }
    )

    category_qty_price_total_df, quantity_avg = get_cat_qty_price(start_date, end_date)
    assert category_qty_price_total_df.equals(expected_df)
    assert quantity_avg == 2.5

    # Test date with no transactions
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 1, 1)
    cat_qty_price_df, quantity_avg = get_cat_qty_price(start_date, end_date)
    assert cat_qty_price_df.empty
    assert quantity_avg == None


def test_get_sales_over_time():
    # Test sales over time
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 1)

    expected_sales_over_time_df = pd.DataFrame(
        {"total_sales": [300], "date": ["2024-01-01"], "cumulative_sales": [300]}
    )

    sales_over_time_df, cumulative_sales_df = get_sales_over_time(start_date, end_date)
    assert sales_over_time_df.equals(expected_sales_over_time_df)

    # Test date with no transactions
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 1, 1)
    sales_over_time_df, cumulative_sales_df = get_sales_over_time(start_date, end_date)
    assert sales_over_time_df.empty
    assert cumulative_sales_df.empty


if __name__ == "__main__":
    pytest.main()
