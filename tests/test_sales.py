import switch_path
import pandas as pd
import pytest
from sales.sale_controller import (
    process_barcode,
    get_total_transaction,
)


def test_process_barcode():
    # Valid barcode
    barcode_data = "X002VTD301"
    expected_product = {
        "_id": "1",
        "product_name": "Vitamin D3 Supplement",
        "category": "Supplements",
        "barcode_data": "X002VTD301",
        "price": 5.99,
    }
    result = process_barcode(barcode_data)
    assert result == expected_product

    # Invalid barcode
    barcode_data = "blah"
    expected_error_message = f"No product with scanned barcode: {barcode_data}."
    result = process_barcode(barcode_data)
    assert result == expected_error_message


def test_get_total_transaction():
    # Test products
    selected_products = pd.DataFrame(
        {
            "product_name": ["A", "B", "C"],
            "price": [5.99, 3.49, 2.99],
            "quantity": [2, 1, 3],
        }
    )

    total_price = get_total_transaction(selected_products)
    assert total_price == 24.44


if __name__ == "__main__":
    pytest.main(["-v", __file__])
