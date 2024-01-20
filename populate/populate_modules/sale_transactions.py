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


def get_sale_transactions_collection():
    db = get_db()
    return db.sale_transactions


def get_products_collection():
    db = get_db()
    return db.products


def insert_transactions_to_collection(transactions):
    logger.info("Insert sale transactions data into database")
    sale_transactions_collection = get_sale_transactions_collection()
    sale_transactions_collection.insert_many(transactions)


def generate_sale_transactions_test_data(num_transactions):
    products_collection = get_products_collection()
    sale_transactions_test_data = []

    # every 30 transactions, go to next day
    transactions_until_next_day = 30

    logger.info("Generating sale transactions test data")
    
    for i in range(num_transactions):
        # Calculate the number of days to add based on the current transaction index
        days_to_add = i // transactions_until_next_day

        # Calculate the timestamp for the transaction date with a random time between 9 am and 8 pm
        transaction_date = datetime.datetime.utcnow() + datetime.timedelta(
            days=days_to_add, hours=random.randint(9, 20)
        )

        # Random number of products from the products collection
        products = list(products_collection.find().limit(random.randint(1, 8)))

        # random quantity for each product
        for product in products:
            product["quantity"] = random.randint(1, 6)

        # calculate total price
        total_price = round(sum(product["price"] * product["quantity"] for product in products), 2)

        # transaction document
        transaction = {
            "timestamp": transaction_date,
            "total": total_price,
            "products": products
        }

        # add transaction to list
        sale_transactions_test_data.append(transaction)

    # insert into db
    insert_transactions_to_collection(sale_transactions_test_data)