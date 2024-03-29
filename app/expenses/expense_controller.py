from datetime import date
from datetime import datetime
import bson
import streamlit as st
import easyocr
from PIL import Image
import cv2
import numpy as np
from expenses.expense_data import (
    category_exists,
    delete_category_from_db,
    edit_category_in_db,
    fetch_categories,
    fetch_expenses,
    insert_new_category_to_db,
    insert_new_expense_to_db,
)


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


def add_new_expense(
    expense, category, description, amount, expense_date, uploaded_file=None
):
    """
    Request data access to add a new expense.

    Args:
        expense (str): The name of the expense
        category (str): The category of the expense
        description (str): A description of the expense
        amount (str): The amount of the expense
        expense_date (str): The date of the expense
        uploaded_file (file): The image of the expense receipt

    Returns:
        ack (bool): The acknowledgement of the expense addition
        expense_id (str): The id of the expense added
    """
    # check if required data is missing
    if not all([expense, category, description, amount, expense_date]):
        return "Please fill in required fields", None

    # cast to float to check if the amount is a valid number
    try:
        amount = float(amount)
    except ValueError:
        return "Price must be a valid number.", None

    current_timestamp = datetime.utcnow()
    recorded_date = current_timestamp.date()

    # convert expense_date to datetime.date object if it's not already
    if not isinstance(expense_date, date):
        try:
            expense_date = datetime.strptime(expense_date, "%Y-%m-%d").date()
        except ValueError:
            return "Expense date must be in the format YYYY-MM-DD.", None

    # check if expense date is in the future
    if expense_date > recorded_date:
        return "Expense date cannot be in the future.", None

    # create a new expense document
    new_expense = {
        "expense": expense,
        "category": category,
        "description": description,
        "amount": amount,
        "recorded_date": recorded_date.strftime("%Y-%m-%d"),
        "expense_date": expense_date.strftime("%Y-%m-%d"),
    }

    # add expense image if it exists
    if uploaded_file is not None:
        binary_image = bson.Binary(uploaded_file.read())
        new_expense["expense_image"] = binary_image

    ack, expense_id = insert_new_expense_to_db(new_expense)
    return ack, expense_id


def get_expenses():
    """
    Request all expenses from data access.

    Returns:
        List[dict]: A list of expense documents
    """
    return fetch_expenses()


def get_index(page_size):
    """
    Get the start and end index of the current page.

    Args:
        page_size (int): The number of items per page.

    Returns:
        start_idx (int): The start index of the current page.
        end_idx (int): The end index of the current page
    """
    start_idx = (st.session_state.current_page_expense - 1) * page_size
    end_idx = start_idx + page_size

    return start_idx, end_idx


def filter_by_id(transactions, search_id):
    """
    Filter transactions by the search id.

    Args:
        transactions (list): The list of transactions.
        search_id (str): The search id.

    Returns:
        search_result (list): The list of transactions that match the search id.
    """
    search_id_lower = search_id.lower()
    search_result = [
        transaction
        for transaction in transactions
        if search_id_lower in str(transaction["_id"]).lower()
    ]

    if len(search_result) == 0:
        st.session_state.current_page_expense = 0
    else:
        st.session_state.current_page_expense = 1

    return search_result


def get_total_pages(page_size, transactions):
    """
    Get the total number of pages for the current transactions.

    Args:
        page_size (int): The number of items per page.
        transactions (list): The list of transactions.

    Returns:
        total_pages (int): The total number of pages.
    """
    total_pages = len(transactions) // page_size + (len(transactions) % page_size > 0)

    return total_pages


def prev_page():
    """
    Decrement the current page by 1. If the current page is 1, it will not decrement.
    """
    if st.session_state.current_page_expense > 1:
        st.session_state.current_page_expense -= 1


def next_page():
    """
    Increment the current page by 1.
    """
    st.session_state.current_page_expense += 1


def get_text_ocr(uploaded_file):
    """
    Extract text from an image using easyocr.

    Args:
        uploaded_file (image): The image file to extract text from.

    Returns:
        image (np.array): The image as a numpy array
        text_str (str): The extracted text
    """
    reader = easyocr.Reader(["en"])
    image = Image.open(uploaded_file)

    # Use easyocr to read the text from the image
    result = reader.readtext(image)

    # extract text from the result
    text_str = "\n".join([text for (_, text, _) in result])

    return image, text_str
