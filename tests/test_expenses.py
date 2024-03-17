import switch_path
import pytest
from expenses.expense_controller import (
    add_new_expense,
    filter_by_id,
)


def test_add_new_expense():
    # All required fields are provided
    expense = "Test 1"
    category = "Packaging"
    description = "blah blah"
    amount = "100"
    expense_date = "2022-01-01"
    uploaded_file = None

    ack, expense_id = add_new_expense(
        expense, category, description, amount, expense_date, uploaded_file
    )
    assert ack == True
    assert expense_id is not None

    # Missing required fields
    expense = ""
    category = "Packaging"
    description = "blah blah"
    amount = "100.00"
    expense_date = "2022-01-01"
    uploaded_file = None

    ack, expense_id = add_new_expense(
        expense, category, description, amount, expense_date, uploaded_file
    )
    assert ack == "Please fill in required fields"
    assert expense_id == None

    # Invalid amount
    expense = "Test 3"
    category = "Packaging"
    description = "blah blah"
    amount = "100abc"
    expense_date = "2022-01-01"
    uploaded_file = None

    ack, expense_id = add_new_expense(
        expense, category, description, amount, expense_date, uploaded_file
    )
    assert ack == "Price must be a valid number."
    assert expense_id == None

    # Expense date in the future
    expense = "Test 4"
    category = "Packaging"
    description = "blah blah"
    amount = "100"
    expense_date = "3000-01-01"
    uploaded_file = None

    ack, expense_id = add_new_expense(
        expense, category, description, amount, expense_date, uploaded_file
    )
    assert ack == "Expense date cannot be in the future."
    assert expense_id == None


def test_filter_by_id():
    # Empty transactions list
    transactions = []
    search_id = "abc"
    search_result = filter_by_id(transactions, search_id)
    assert search_result == []

    # No matching transactions
    transactions = [{"_id": "123"}, {"_id": "456"}, {"_id": "789"}]
    search_id = "abc"
    search_result = filter_by_id(transactions, search_id)
    assert search_result == []

    # Matching transactions
    transactions = [{"_id": "123"}, {"_id": "456"}, {"_id": "789"}]
    search_id = "456"
    search_result = filter_by_id(transactions, search_id)
    assert search_result == [{"_id": "456"}]

    # Case-insensitive search
    transactions = [{"_id": "abc"}, {"_id": "DEF"}, {"_id": "Ghi"}]
    search_id = "def"
    search_result = filter_by_id(transactions, search_id)
    assert search_result == [{"_id": "DEF"}]

    # Partial search and case-insensitive
    transactions = [{"_id": "abc"}, {"_id": "DEF"}, {"_id": "Ghief"}]
    search_id = "eF"
    search_result = filter_by_id(transactions, search_id)
    assert search_result == [{"_id": "DEF"}, {"_id": "Ghief"}]


if __name__ == "__main__":
    pytest.main(["-v", __file__])
