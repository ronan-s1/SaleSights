import switch_path
import pytest
import random
import string
from products.product_controller import (
    add_new_product,
    update_product,
)


def test_add_new_product():
    # Generate random barcode data so that tests can be run multiple times
    barcode_data = "".join(random.choices(string.ascii_letters + string.digits, k=10))

    # All required fields are provided
    product_name = "Test 1 and 4"
    category = "Food"
    price = "10"

    result = add_new_product(product_name, category, barcode_data, price)
    assert result is None

    # Product already exists
    product_name = "Test 1 and 4"
    category = "Food"
    price = "10"

    result = add_new_product(product_name, category, barcode_data, price)
    assert result == f"Product '{product_name}' already exists."

    # Missing required fields
    product_name = ""
    category = "Food"
    barcode_data = "1234567890"
    price = "10"

    result = add_new_product(product_name, category, barcode_data, price)
    assert result == "Please fill in required fields"

    # Invalid price
    product_name = "Test 3"
    category = "Food"
    barcode_data = "1234567890"
    price = "123abc"

    result = add_new_product(product_name, category, barcode_data, price)
    assert result == "Price must be a valid number."


if __name__ == "__main__":
    pytest.main(["-v", __file__])
