import time
from datetime import datetime

import pandas as pd
import streamlit as st
from expenses.expense_controller import add_new_category
from expenses.expense_controller import add_new_expense
from expenses.expense_controller import delete_category
from expenses.expense_controller import edit_existing_category
from expenses.expense_controller import filter_by_id
from expenses.expense_controller import get_categories
from expenses.expense_controller import get_expenses
from expenses.expense_controller import get_index
from expenses.expense_controller import get_total_pages
from expenses.expense_controller import next_page
from expenses.expense_controller import prev_page
from utils import v_spacer


def display_expenses_components():
    page_size = 5
    expenses = list(get_expenses())

    if not expenses:
        st.error("No expenses.")
        return

    # filter expenses based on the entered ID
    search_id = st.text_input("Search by ID:")
    if search_id:
        expenses = filter_by_id(expenses, search_id)

    total_pages = get_total_pages(page_size, expenses)

    # columns for prev and next buttons
    col1, col2 = st.columns([10, 1])
    with col1:
        if st.session_state.current_page_expense > 1 and total_pages > 1:
            st.button("Previous", on_click=prev_page)

    with col2:
        if st.session_state.current_page_expense < total_pages:
            st.button("Next", on_click=next_page)

    # start and end index for expenses list
    start_idx, end_idx = get_index(page_size)

    # display expenses for the current page
    for expense in expenses[start_idx:end_idx]:
        formatted_date = f"{datetime.strptime(expense['expense_date'], '%Y-%m-%d').strftime('%B %d, %Y')}"
        with st.expander(formatted_date):
            expense_data = {
                "Expense ID": [expense["_id"]],
                "Expense": [expense["name"]],
                "Amount / Cost": [expense["amount"]],
                "Category": [expense["category"]],
                "Description": [expense["description"]],
            }
            df = pd.DataFrame(expense_data).T
            st.table(df)

    # display current page info
    st.write(f"Page {st.session_state.current_page_expense} of {total_pages}")


def add_expense_components():
    expense = st.text_input("Expense:")
    amount = st.text_input("Amount / Cost:")

    category_options = get_categories()
    category = st.selectbox("Select Category:", category_options)
    expense_date = st.date_input("Expense Date", format="YYYY/MM/DD", value=None)
    description = st.text_area("Description:")

    # Add product button
    if st.button("Add Expense"):
        err = add_new_expense(expense, category, description, amount, expense_date)
        if err:
            st.warning(err)
        else:
            st.rerun()


def add_category_components():
    new_category_name = st.text_input("Category Name:")

    if st.button("Add Category"):
        err = add_new_category(new_category_name)
        if err:
            st.warning(err)
        else:
            st.rerun()


def edit_category_components():
    selected_category_name = st.selectbox(
        "Select a category:",
        get_categories(),
        key="select_category_edit_2",
    )

    new_category_name = st.text_input("Edit Category Name:", selected_category_name)

    # Add additional input fields for other category details if needed
    if st.button("Edit Category"):
        err = edit_existing_category(selected_category_name, new_category_name)
        if err:
            st.warning(err)
        else:
            st.rerun()


def delete_category_components():
    selected_category_name = st.selectbox(
        "Select a category to delete:",
        get_categories(),
        key="select_category_delete",
    )

    if st.button("Delete Category"):
        err = delete_category(selected_category_name)
        if err:
            st.warning(err)
        else:
            st.rerun()


def expense_main():
    st.header("Business Expenses 💸")
    categories = get_categories()

    if "current_page_expense" not in st.session_state:
        st.session_state.current_page_expense = 1

    if "current_tab" not in st.session_state:
        st.session_state.current_tab = "Log Expenses"

    # buttons to switch between tabs
    col1, col2 = st.columns([8.79, 2])
    if col1.button("Log Expenses"):
        st.session_state.current_tab = "Log Expenses"

    if col2.button("View Expenses"):
        st.session_state.current_tab = "View Expenses"

    # small gap between the tabs and the content
    v_spacer(2)

    # display the selected tab
    if st.session_state.current_tab == "Log Expenses":
        with st.expander("Add Expense"):
            add_expense_components()

        with st.expander("Add Category"):
            add_category_components()

        if categories:
            with st.expander("Edit Category"):
                edit_category_components()

            with st.expander("Delete Category"):
                delete_category_components()

    elif st.session_state.current_tab == "View Expenses":
        display_expenses_components()
