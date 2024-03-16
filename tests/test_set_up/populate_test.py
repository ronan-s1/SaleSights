import json
import os
from pymongo import MongoClient
from streamlit import secrets


def read_json(data_file):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "test_data", data_file)
    with open(file_path, "r") as file:
        return json.load(file)


def populate():
    client = MongoClient(**secrets["mongo"])
    db = client.salesights
    sale_transactions_collection = db.sale_transactions
    expenses_collection = db.expenses

    # drop the collection
    sale_transactions_collection.drop()
    expenses_collection.drop()

    # fetch and insert data
    sale_transactions_data = read_json("sale_transactions.json")
    expense_data = read_json("expenses.json")

    sale_transactions_collection.insert_many(sale_transactions_data)
    expenses_collection.insert_many(expense_data)
