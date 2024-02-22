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


def insert_new_settings_to_db(settings):
    settings_collection = get_settings_collection()
    existing_settings = settings_collection.find_one()

    # only one settings document should exist
    if existing_settings:
        settings_collection.update_one({}, {"$set": settings})
    else:
        settings_collection.insert_one(settings)


def fetch_settings():
    settings_collection = get_settings_collection()
    settings = settings_collection.find_one()
    return settings
