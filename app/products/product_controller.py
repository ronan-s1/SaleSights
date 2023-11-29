from products.product_fetch_data import (
    fetch_products,
    fetch_categories,
    insert_new_product_to_db,
    delete_product_from_db,
    update_product_from_db,
    product_exists,
)


def get_products():
    products = fetch_products()
    return list(products)


def get_categories():
    categories = fetch_categories()
    return list(categories)


def add_new_product(product_name, category, barcode_data):
    new_product = {
        "product_name": product_name,
        "category": category,
        "barcode_data": barcode_data,
    }

    if product_exists(new_product):
        return f"Product '{product_name}' already exists."

    insert_new_product_to_db(new_product)


def delete_product(product):
    product_obj_id = product["_id"].iloc[0]
    delete_product_from_db(product_obj_id)


def update_product(product_details, product_name, category, barcode):
    product_id = product_details["_id"].iloc[0]
    # Update the existing product
    product_to_update = {
        "product_name": product_name,
        "category": category,
        "barcode_data": barcode,
    }

    if product_exists(product_to_update):
        return f"Product '{product_name}' already exists."

    # Use the _id to identify the document for update
    update_product_from_db(product_id, product_to_update)
