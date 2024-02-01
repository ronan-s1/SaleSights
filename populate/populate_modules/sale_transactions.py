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
    logger.info("Inserting sale transactions data into database")
    sale_transactions_collection = get_sale_transactions_collection()
    sale_transactions_collection.insert_many(transactions)


def get_transactions_until_next_day():
    return random.randint(10, 30)


def generate_sale_transactions_test_data(num_transactions):
    products_collection = get_products_collection()
    sale_transactions_test_data = []

    # every 30 transactions, go to next day
    day_counter = 0
    transaction_counter = 0
    transactions_until_next_day = get_transactions_until_next_day()

    logger.info("Generating sale transactions test data")

    for _ in range(num_transactions):
        # if the transaction counter has reached the random threshold to switch to the next day
        if transaction_counter >= transactions_until_next_day:
            transaction_counter = 0
            day_counter += 1
            transactions_until_next_day = get_transactions_until_next_day()

        # Calculate the timestamp for the transaction date with a random time between 9 am and 8 pm
        transaction_date = datetime.datetime(2024, 1, 1) + datetime.timedelta(
            days=day_counter,
            hours=random.randint(9, 20),
            minutes=random.randint(0, 59),
        )

        # Random number of products from the products collection
        all_products = list(products_collection.find())
        number_of_products = random.randint(1, 5)

        products = []
        for _ in range(number_of_products):
            selected_product = random.choice(all_products)
            if selected_product not in products:
                products.append(selected_product)

        # random quantity for each product
        for product in products:
            product["quantity"] = random.randint(1, 4)

        # calculate total price
        total_price = round(
            sum(product["price"] * product["quantity"] for product in products), 2
        )

        # transaction document
        date_str = transaction_date.strftime("%Y-%m-%d")
        time_str = transaction_date.strftime("%H:%M:%S")

        transaction = {
            "date": date_str,
            "time": time_str,
            "total": total_price,
            "products": products,
        }

        # add transaction to list
        sale_transactions_test_data.append(transaction)
        transaction_counter += 1

    # insert into db
    insert_transactions_to_collection(sale_transactions_test_data)
