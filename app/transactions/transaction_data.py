from pymongo import MongoClient, DESCENDING
from streamlit import secrets


def connect_to_db():
    client = MongoClient(**secrets["mongo"])
    return client


def get_db():
    client = connect_to_db()
    db = client.salesights
    return db


def get_sale_transactions_collection():
    db = get_db()
    return db.sale_transactions


def fetch_sale_transactions():
    sale_transactions_collection = get_sale_transactions_collection()
    transactions = sale_transactions_collection.find().sort(
        [("date", DESCENDING), ("time", DESCENDING)]
    )
    return transactions
