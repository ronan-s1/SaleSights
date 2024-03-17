import switch_path
import pytest
import json
import os
from transactions.transaction_controller import get_transactions, filter_by_id


def read_transaction_json():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(
        script_dir, "test_set_up", "test_data", "sale_transactions.json"
    )
    with open(file_path, "r") as file:
        return list(json.load(file))


def test_get_transactions():
    # Test transactions
    expected_transactions = read_transaction_json()
    transactions = list(get_transactions())
    assert transactions == expected_transactions


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
