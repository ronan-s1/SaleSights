from pymongo import MongoClient


def connect_to_db():
    client = MongoClient("localhost", 27017)
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
    projection = {"_id": 1, "product_name": 1, "category": 1, "barcode_data": 1}
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


def product_exists(product):
    products_collection = get_products_collection()
    matching_product = products_collection.find_one(product)
    return matching_product is not None