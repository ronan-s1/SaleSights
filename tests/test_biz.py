import switch_path
import pytest
import pandas as pd
from biz.biz_controller import (
    process_query,
    selected_collections_processing,
    get_prefix_suffix,
    flatten_transactions,
)
from biz.utils.prompt_templates import (
    SINGLE_DF_PREFIX,
    SINGLE_DF_SUFFIX,
    MULTI_DF_PREFIX,
    MULTI_DF_SUFFIX,
)


def test_process_query():
    # Test when an empty dataframe is passed
    result, valid = process_query(pd.DataFrame())
    assert result == "Please select valid data to proceed. (single df is empty)"
    assert valid is False

    # Test when a list of empty dataframes is passed
    result, valid = process_query([pd.DataFrame(), pd.DataFrame()])
    assert (
        result
        == "Please select valid data to proceed. (multiple df selected but all empty)"
    )
    assert valid is False

    # Test when invalid data is passed
    result, valid = process_query("invalid data")
    assert result == "Please select valid data to proceed. (data not a df or list)"
    assert valid is False


def test_selected_collections_processing():
    # Test when no collection is selected
    selected_collections = []
    result, valid = selected_collections_processing(selected_collections)
    assert result is None
    assert valid == "Please select valid data to proceed."

    # Test when only one collection is selected
    selected_collections = ["collection1"]
    result, valid = selected_collections_processing(selected_collections)
    assert result == "collection1"
    assert valid is None

    # Test when multiple collections are selected
    selected_collections = ["collection1", "collection2", "collection3"]
    result, valid = selected_collections_processing(selected_collections)
    assert result == ["collection1", "collection2", "collection3"]


def test_get_prefix_suffix():
    # Test when a single dataframe is passed
    selected_collections_df = pd.DataFrame()
    prefix, suffix = get_prefix_suffix(selected_collections_df)
    assert prefix == SINGLE_DF_PREFIX
    assert suffix == SINGLE_DF_SUFFIX

    # Test when a list of multiple dataframes is passed
    selected_collections_df = [pd.DataFrame(), pd.DataFrame()]
    prefix, suffix = get_prefix_suffix(selected_collections_df)
    assert prefix == MULTI_DF_PREFIX
    assert suffix == MULTI_DF_SUFFIX

    # Test when invalid data is passed
    selected_collections_df = "invalid data"
    prefix, suffix = get_prefix_suffix(selected_collections_df)
    assert prefix == SINGLE_DF_PREFIX
    assert suffix == SINGLE_DF_SUFFIX


def test_flatten_transactions():
    # Test with empty transactions list
    transactions = []
    flattened_transactions = flatten_transactions(transactions)
    assert flattened_transactions == None

    # Test with a single transaction
    transactions = [
        {
            "_id": "123",
            "date": "2022-01-01",
            "time": "10:00:00",
            "total": 100.0,
            "products": [
                {
                    "product_name": "Product 1",
                    "category": "Category 1",
                    "barcode_data": "123456789",
                    "price": 10.0,
                    "quantity": 2,
                },
                {
                    "product_name": "Product 2",
                    "category": "Category 2",
                    "price": 20.0,
                    "quantity": 1,
                },
            ],
        }
    ]
    expected_flattened_transactions = [
        {
            "transaction_id": "123",
            "date": "2022-01-01",
            "time": "10:00:00",
            "total": 100.0,
            "product_name": "Product 1",
            "category": "Category 1",
            "barcode_data": "123456789",
            "price": 10.0,
            "quantity": 2,
        },
        {
            "transaction_id": "123",
            "date": "2022-01-01",
            "time": "10:00:00",
            "total": 100.0,
            "product_name": "Product 2",
            "category": "Category 2",
            "barcode_data": None,
            "price": 20.0,
            "quantity": 1,
        },
    ]
    flattened_transactions = flatten_transactions(transactions)
    assert flattened_transactions == expected_flattened_transactions

    # Test with multiple transactions
    transactions = [
        {
            "_id": "123",
            "date": "2022-01-01",
            "time": "10:00:00",
            "total": 100.0,
            "products": [
                {
                    "product_name": "Product 1",
                    "category": "Category 1",
                    "barcode_data": "123456789",
                    "price": 10.0,
                    "quantity": 2,
                }
            ],
        },
        {
            "_id": "456",
            "date": "2022-01-02",
            "time": "11:00:00",
            "total": 50.0,
            "products": [
                {
                    "product_name": "Product 2",
                    "category": "Category 2",
                    "price": 20.0,
                    "quantity": 1,
                },
                {
                    "product_name": "Product 3",
                    "category": "Category 3",
                    "price": 15.0,
                    "quantity": 3,
                },
            ],
        },
    ]
    expected_flattened_transactions = [
        {
            "transaction_id": "123",
            "date": "2022-01-01",
            "time": "10:00:00",
            "total": 100.0,
            "product_name": "Product 1",
            "category": "Category 1",
            "barcode_data": "123456789",
            "price": 10.0,
            "quantity": 2,
        },
        {
            "transaction_id": "456",
            "date": "2022-01-02",
            "time": "11:00:00",
            "total": 50.0,
            "product_name": "Product 2",
            "category": "Category 2",
            "barcode_data": None,
            "price": 20.0,
            "quantity": 1,
        },
        {
            "transaction_id": "456",
            "date": "2022-01-02",
            "time": "11:00:00",
            "total": 50.0,
            "product_name": "Product 3",
            "category": "Category 3",
            "barcode_data": None,
            "price": 15.0,
            "quantity": 3,
        },
    ]
    flattened_transactions = flatten_transactions(transactions)
    assert flattened_transactions == expected_flattened_transactions


if __name__ == "__main__":
    pytest.main(["-v", __file__])
