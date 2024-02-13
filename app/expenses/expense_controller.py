from datetime import date
from datetime import datetime

import pandas as pd
import streamlit as st
from expenses.expense_data import category_exists
from expenses.expense_data import delete_category_from_db
from expenses.expense_data import edit_category_in_db
from expenses.expense_data import fetch_categories
from expenses.expense_data import fetch_expenses
from expenses.expense_data import insert_new_category_to_db
from expenses.expense_data import insert_new_expense_to_db


def get_categories():
    """
    Request list of all expense categories from data access.

    Returns:
        List[dict]: A list of expense category documentments
    """
    categories = fetch_categories()
    return list(categories)


def add_new_category(new_category):
    """
    Request data access to add new category

    Args:
        new_category (str): category to add

    Returns:
        str: Error message
        None: No errors
    """
    if not new_category:
        return "Please fill in required fields"

    new_category = new_category.capitalize()

    if category_exists(new_category):
        return f"category '{new_category}' already exists"

    new_category = {"category": new_category}

    insert_new_category_to_db(new_category)


def add_new_category(new_category):
    """
    Request data access to add new category

    Args:
        new_category (str): category to add

    Returns:
        str: Error message
        None: No errors
    """
    if not new_category:
        return "Please fill in required fields"

    new_category = new_category.capitalize()

    if category_exists(new_category):
        return f"category '{new_category}' already exists"

    new_category = {"category": new_category}

    insert_new_category_to_db(new_category)


def edit_existing_category(selected_category_name, new_category_name):
    """
    Request data access to edit an existing category.

    Args:
        selected_category_name (str): The current name of the category.
        new_category_name (str): The new name for the category.

    Returns:
        str: Error message
        None: no errors
    """
    if not all([selected_category_name, new_category_name]):
        return "Please fill in required fields"

    if category_exists(new_category_name):
        return f"category '{new_category_name}' already exists"

    edit_category_in_db(selected_category_name, new_category_name)


def delete_category(category_name):
    """
    Request data access to delete a category.

    Args:
        category_name (str): The name of the category to be deleted

    Returns:
        str: Error message
        None: no errors
    """
    if not category_name:
        return "Please fill in required fields"

    delete_category_from_db(category_name)


def add_new_expense(expense, category, description, amount, expense_date):
    # check if required data is missing
    if not all([expense, category, description, amount, expense_date]):
        return "Please fill in required fields"

    # cast to float to check if the amount is a valid number
    try:
        amount = float(amount)
    except ValueError:
        return "Price must be a valid number."

    current_timestamp = datetime.utcnow()
    recorded_date = current_timestamp.date()

    # convert expense_date to datetime.date object if it's not already
    if not isinstance(expense_date, date):
        try:
            expense_date = datetime.strptime(expense_date, "%Y-%m-%d").date()
        except ValueError:
            return "Expense date must be in the format YYYY-MM-DD."

    # check if expense date is in the future
    if expense_date > recorded_date:
        return "Expense date cannot be in the future."

    new_expense = {
        "expense": expense,
        "category": category,
        "description": description,
        "amount": amount,
        "recorded_date": recorded_date.strftime("%Y-%m-%d"),
        "expense_date": expense_date.strftime("%Y-%m-%d"),
    }

    insert_new_expense_to_db(new_expense)


def get_expenses():
    """
    Request all expenses from data access.

    Returns:
        List[dict]: A list of expense documents
    """
    return fetch_expenses()


def get_index(page_size):
    start_idx = (st.session_state.current_page_expense_expense - 1) * page_size
    end_idx = start_idx + page_size

    return start_idx, end_idx


def filter_by_id(transactions, search_id):
    search_id_lower = search_id.lower()
    search_result = [
        transaction
        for transaction in transactions
        if search_id_lower in str(transaction["_id"]).lower()
    ]

    st.session_state.current_page_expense = 1
    return search_result


def get_total_pages(page_size, transactions):
    total_pages = len(transactions) // page_size + (len(transactions) % page_size > 0)

    return total_pages


def get_index(page_size):
    start_idx = (st.session_state.current_page_expense - 1) * page_size
    end_idx = start_idx + page_size

    return start_idx, end_idx


def prev_page():
    if st.session_state.current_page_expense > 1:
        st.session_state.current_page_expense -= 1


def next_page():
    st.session_state.current_page_expense += 1
