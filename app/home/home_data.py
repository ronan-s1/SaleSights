from pymongo import MongoClient
from streamlit import secrets


def connect_to_db():
    client = MongoClient(**secrets["mongo"])
    return client


def get_db():
    client = connect_to_db()
    db = client.salesights
    return db
