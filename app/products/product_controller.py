import pandas as pd
from products.product_data import (
    fetch_products,
    fetch_categories,
    insert_new_product_to_db,
    insert_new_category_to_db,
    delete_product_from_db,
    update_product_from_db,
    product_exists,
    category_exists,
    edit_category_in_db,
    delete_category_from_db,
)


def get_products():
    """
    Request list of all products from data access.

    Returns:
        List[dict]: A list of product documents
    """
    products = list(fetch_products())
    return list(products)


def get_products_df():
    """
    Puts all products in a dataframe

    Returns:
        List[dict]: A list containing all the products
        Dataframe: A pandas dataframe containing all the products
    """
    all_products = get_products()
    df_all_products = pd.DataFrame(
        all_products, columns=["product_name", "category", "barcode_data", "price"]
    )

    # rename columns
    df_all_products = df_all_products.rename(
        columns={
            "product_name": "Product",
            "category": "Category",
            "barcode_data": "Barcode",
            "price": "Price",
        }
    )

    return all_products, df_all_products


def get_categories():
    """
    Request list of all product categories from data access.

    Returns:
        List[dict]: A list of product category documentments
    """
    categories = fetch_categories()
    return list(categories)


def add_new_product(product_name, category, barcode_data, price):
    """
    Request data access layer to insert a new product.

    Args:
        product_name: str,
        category: str,
        barcode_data: str,
        price: str

    Returns:
        str: Error message
        None: No errors
    """
    # check if required data is missing
    if not all([product_name, category, price]):
        return "Please fill in required fields"

    # cast to float to check if the price is a valid number
    try:
        price = float(price)
    except ValueError:
        return "Price must be a valid number."

    new_product = {
        "product_name": product_name,
        "category": category,
        "barcode_data": barcode_data,
        "price": price,
    }

    if product_exists(new_product):
        return f"Product '{product_name}' already exists."

    insert_new_product_to_db(new_product)


def delete_product(product):
    """
    Request data access to delete a selected product.

    Args:
        product (pd.Dataframe): selected product to be deleted
    """
    product_obj_id = product["_id"].iloc[0]
    delete_product_from_db(product_obj_id)


def update_product(product_details, product_name, category, barcode, price):
    """
    Request data access to update product.

    Args:
        product_details (pd.Dataframe): _description_
        product_name (str): product name
        category (str): category of the product
        barcode (str): barcode data (optional)
        price (str): price of product

    Returns:
        str: Error message
        None: No errors
    """
    # Check if required data is missing
    if not all([product_name, category, price]):
        return "Please fill in required fields"

    # cast to flow to check if the price is a valid number
    try:
        price = float(price)
    except ValueError:
        return "Price must be a valid number."

    product_id = product_details["_id"].iloc[0]
    product_to_update = {
        "product_name": product_name,
        "category": category,
        "barcode_data": barcode,
        "price": price,
    }

    if product_exists(product_to_update):
        return f"Product '{product_name}' already exists."

    # Use the _id to identify the document for update
    update_product_from_db(product_id, product_to_update)


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
