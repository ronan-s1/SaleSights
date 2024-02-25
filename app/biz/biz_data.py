from pymongo import MongoClient
from streamlit import secrets


def connect_to_db():
    client = MongoClient(**secrets["mongo"])
    return client


def get_db():
    client = connect_to_db()
    db = client.salesights
    return db


def get_settings_collection():
    db = get_db()
    return db.settings


def fetch_openai_api_key():
    settings_collection = get_settings_collection()
    settings = settings_collection.find_one()
    return settings["openai_api_key"]


def fetch_model():
    settings_collection = get_settings_collection()
    settings = settings_collection.find_one()
    return settings["selected_model"]


# -- COLLECTIONS --


def get_expenses_collection():
    db = get_db()
    expenses_collection = db.expenses
    return expenses_collection


def get_expense_categories_collection():
    db = get_db()
    expense_categories_collection = db.expense_categories
    return expense_categories_collection


def get_product_categories_collection():
    db = get_db()
    product_categories_collection = db.product_categories
    return product_categories_collection


def get_products_collection():
    db = get_db()
    products_collection = db.products
    return products_collection


def get_sale_transactions_collection():
    db = get_db()
    sale_transactions_collection = db.sale_transactions
    return sale_transactions_collection


# -- FETCH DATA --


def fetch_products():
    products_collection = get_products_collection()
    result = products_collection.find({}, {"_id": 0})
    return result


def fetch_product_categories():
    products_collection = get_product_categories_collection()
    result = products_collection.find({}, {"_id": 0})
    return result


def fetch_expenses():
    expenses_collection = get_expenses_collection()
    result = expenses_collection.find({}, {"expense_image": 0, "_id": 0})
    return result


def fetch_sale_transactions():
    sale_transactions_collection = get_sale_transactions_collection()
    transactions = sale_transactions_collection.find()
    return transactions


def fetch_expense_categories():
    expenses_categories_collection = get_expense_categories_collection()
    result = expenses_categories_collection.find({}, {"_id": 0})
    return result
