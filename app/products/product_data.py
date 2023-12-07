from pymongo import MongoClient
from streamlit import secrets


def connect_to_db():
    client = MongoClient(**secrets["mongo"])
    return client


def get_db():
    client = connect_to_db()
    db = client.salesights
    return db


def get_products_collection():
    db = get_db()
    return db.products


def get_product_categories_collection():
    db = get_db()
    return db.product_categories


def fetch_products():
    products_collection = get_products_collection()
    projection = {
        "_id": 1,
        "product_name": 1,
        "category": 1,
        "barcode_data": 1,
        "price": 1,
    }
    return products_collection.find({}, projection)


def fetch_categories():
    product_categories = get_product_categories_collection()
    return product_categories.distinct("category")


def insert_new_product_to_db(new_product):
    products_collection = get_products_collection()
    products_collection.insert_one(new_product)


def delete_product_from_db(product_id):
    products_collection = get_products_collection()
    products_collection.delete_one({"_id": product_id})


def update_product_from_db(selected_product_id, product_to_update):
    products_collection = get_products_collection()
    products_collection.update_one(
        {"_id": selected_product_id}, {"$set": product_to_update}
    )


# if a product exists return True
def product_exists(product):
    products_collection = get_products_collection()
    matching_product = products_collection.find_one(product)
    return matching_product is not None


def insert_new_category_to_db(category):
    categories_collection = get_product_categories_collection()
    categories_collection.insert_one(category)


def category_exists(category):
    categories_collection = get_product_categories_collection()
    matching_category = categories_collection.find_one(category)
    return matching_category is not None


def edit_category_in_db(old_category_name, new_category_name):
    products_collection = get_products_collection()
    product_categories_collection = get_product_categories_collection()

    # update all products with the old category to the new category
    products_collection.update_many(
        {"category": old_category_name}, {"$set": {"category": new_category_name}}
    )

    # update the product categories collection if necessary
    product_categories_collection.update_one(
        {"category": old_category_name},
        {"$set": {"category": new_category_name}},
        upsert=True,
    )


def delete_category_from_db(category_name):
    products_collection = get_products_collection()
    product_categories_collection = get_product_categories_collection()

    # update all products with the deleted category to a new category called "Other"
    products_collection.update_many(
        {"category": category_name}, {"$set": {"category": "Other"}}
    )

    # remove the deleted category from the product categories collection
    product_categories_collection.delete_one({"category": category_name})
