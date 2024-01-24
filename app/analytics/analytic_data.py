import pandas as pd
from datetime import datetime
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


def get_sale_transactions_collection():
    db = get_db()
    return db.sale_transactions


def fetch_sale_transactions():
    sale_transactions_collection = get_sale_transactions_collection()
    transactions = sale_transactions_collection.find()
    return transactions


def fetch_cat_and_qty(start_date, end_date):
    date_range = {
        "date": {
            "$gte": (start_date),
            "$lte": (end_date),
        }
    }
    
    # aggregation pipeline to project only the category and quantity
    pipeline = [
        {"$match": date_range},
        {"$unwind": "$products"},
        {"$project": {"_id": 0, "category": "$products.category", "quantity": "$products.quantity"}}
    ]

    result = get_sale_transactions_collection().aggregate(pipeline)
    
    return result
