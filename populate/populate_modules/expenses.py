import datetime
import random
import logging
from pymongo import MongoClient
from streamlit import secrets


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def connect_to_db():
    client = MongoClient(**secrets["mongo"])
    return client


def get_db():
    client = connect_to_db()
    db = client.salesights
    return db


def get_expenses_collection():
    db = get_db()
    return db.expenses


def get_expense_categories_collection():
    db = get_db()
    return db.expense_categories


def fetch_expense_categories():
    expense_categories_collection = get_expense_categories_collection()
    return [
        category["category"]
        for category in expense_categories_collection.find({}, {"category": 1})
    ]


def insert_expenses_to_collection(expenses):
    logger.info("Inserting expenses data into database")
    expenses_collection = get_expenses_collection()
    expenses_collection.insert_many(expenses)


def get_expenses_until_next_day():
    return random.randint(0, 3)


def generate_expenses_test_data(num_expenses):
    expenses_test_data = []
    expense_categories = fetch_expense_categories()

    day_counter = 0
    expense_counter = 0
    expenses_until_next_day = get_expenses_until_next_day()

    logger.info("Generating expenses test data")

    # loop through the number of expenses to generate
    for _ in range(num_expenses):
        # if the expenses counter has reached the random threshold to switch to the next day
        if expense_counter >= expenses_until_next_day:
            expense_counter = 0
            day_counter += 1
            expenses_until_next_day = get_expenses_until_next_day()

        # calculate the date for the expense date
        date = datetime.datetime(2024, 1, 1) + datetime.timedelta(days=day_counter)

        recorded_date_str = date.strftime("%Y-%m-%d")
        expense_date_str = (date - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

        # create expense
        expense = {
            "expense": f"Test Expense {expense_counter}",
            "category": random.choice(expense_categories),
            "description": "Test Description",
            "amount": round(random.uniform(10, 100), 2),
            "recorded_date": recorded_date_str,
            "expense_date": expense_date_str,
        }

        # add expense to list
        expenses_test_data.append(expense)
        expense_counter += 1

    # insert into db
    insert_expenses_to_collection(expenses_test_data)
