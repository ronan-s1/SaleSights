from pymongo import MongoClient
from streamlit import secrets


def connect_to_db():
    client = MongoClient(**secrets["mongo"])
    return client


def get_db():
    client = connect_to_db()
    db = client.salesights
    return db


def get_expense_categories_collection():
    db = get_db()
    return db.expense_categories


def get_expenses_collection():
    db = get_db()
    return db.expenses


def fetch_categories():
    product_categories = get_expense_categories_collection()
    return product_categories.distinct("category")


def insert_new_expense_to_db(new_expense):
    expenses = get_expenses_collection()
    result = expenses.insert_one(new_expense)
    return result.acknowledged, result.inserted_id


def fetch_expenses():
    expenses = get_expenses_collection()
    return expenses.find()


def category_exists(category):
    categories_collection = get_expense_categories_collection()
    matching_category = categories_collection.find_one(category)
    return matching_category is not None


def insert_new_category_to_db(category):
    categories_collection = get_expense_categories_collection()
    categories_collection.insert_one(category)


def edit_category_in_db(old_category_name, new_category_name):
    expense_collection = get_expenses_collection()
    pexpense_categories_collection = get_expense_categories_collection()

    # update all products with the old category to the new category
    expense_collection.update_many(
        {"category": old_category_name}, {"$set": {"category": new_category_name}}
    )

    # update the product categories collection if necessary
    pexpense_categories_collection.update_one(
        {"category": old_category_name},
        {"$set": {"category": new_category_name}},
        upsert=True,
    )


def delete_category_from_db(category_name):
    expense_collection = get_expenses_collection()
    pexpense_categories_collection = get_expense_categories_collection()

    # update all products with the deleted category to a new category called "Other"
    expense_collection.update_many(
        {"category": category_name}, {"$set": {"category": "Other"}}
    )

    # remove the deleted category from the product categories collection
    pexpense_categories_collection.delete_one({"category": category_name})
