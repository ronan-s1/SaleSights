import streamlit as st
from datetime import datetime
import pandas as pd
from PIL import Image
import io
from expenses.expense_controller import (
    add_new_category,
    add_new_expense,
    delete_category,
    edit_existing_category,
    filter_by_id,
    get_categories,
    get_expenses,
    get_index,
    get_total_pages,
    next_page,
    prev_page,
    get_text_ocr,
)
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
                "Expense": [expense["expense"]],
                "Amount / Cost": [expense["amount"]],
                "Category": [expense["category"]],
                "Recorded Date": [expense["recorded_date"]],
                "Expense Date": [expense["expense_date"]],
                "Description": [expense["description"]],
            }
            df = pd.DataFrame(expense_data).T
            st.table(df)

            # display expense image if it exists
            if "expense_image" in expense:
                st.write("Expense Image:")
                image_data = expense["expense_image"]
                image = Image.open(io.BytesIO(image_data))
                st.image(image, caption="Expense Image", width=300)

    # display current page info
    st.write(f"Page {st.session_state.current_page_expense} of {total_pages}")


@st.cache_resource
def process_uploaded_file(uploaded_file):
    return get_text_ocr(uploaded_file)


def add_expense_components():
    uploaded_file = st.file_uploader(
        "Upload expense receipt (optional):",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=False,
    )

    if uploaded_file is not None:
        image, text_str = process_uploaded_file(uploaded_file)

        ocr_col1, ocr_col2 = st.columns(2)
        with ocr_col1:
            st.image(image)

        with ocr_col2:
            st.code(f"{text_str}", language="text")

    expense = st.text_input("Expense:")
    amount = st.text_input("Amount / Cost:")
    category_options = get_categories()
    category = st.selectbox("Select Category:", category_options)
    expense_date = st.date_input("Expense Date", format="YYYY/MM/DD", value=None)
    description = st.text_area("Description:")

    # Add product button
    if st.button("Add Expense"):
        ack, expense_id = add_new_expense(
            expense, category, description, amount, expense_date, uploaded_file
        )
        if isinstance(ack, str):
            st.warning(ack)
        elif ack:
            st.success(f"Expense added successfully. ID: {expense_id}")
        else:
            st.error("Error occursed adding the expense to the database.")


def add_category_components():
    new_category_name = st.text_input("Category Name:")

    if st.button("Add Category"):
        err = add_new_category(new_category_name)
        if err:
            st.warning(err)
        else:
            st.success(f"Category '{new_category_name}' added successfully.")


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
            st.success(
                f"Category '{selected_category_name}' edited to '{new_category_name}'."
            )


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
            st.success(f"Category '{selected_category_name}' deleted successfully.")


def expense_main():
    st.title("Business Expenses 💸")
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
        st.session_state.current_page_expense = 1
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
