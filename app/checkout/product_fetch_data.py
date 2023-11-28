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


def fetch_products():
    products_collection = get_products_collection()
    projection = {"_id": 1, "product_name": 1, "category": 1, "barcode_data": 1}
    return products_collection.find({}, projection)


def get_product_by_barcode(barcode):
    products_collection = get_products_collection()
    matching_product = products_collection.find_one({"barcode_data": barcode})
    return matching_product