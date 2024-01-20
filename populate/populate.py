import logging
import os
import json
from pymongo import MongoClient
from streamlit import secrets
from populate_modules.sale_transactions import generate_sale_transactions_test_data

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def read_json(data_file):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "sample_data", data_file)
    with open(file_path, "r") as file:
        return json.load(file)


def populate():
    logger.info("Connecting to database")
    client = MongoClient(**secrets["mongo"])

    # get the database and collections
    db = client.salesights
    product_categories_collection = db.product_categories
    products_collection = db.products
    sale_transactions_collection = db.sale_transactions

    # drop existing collections
    logger.info("Dropping existing collections")
    product_categories_collection.drop()
    products_collection.drop()
    sale_transactions_collection.drop()

    product_categories_data = read_json("product_categories.json")
    products_data = read_json("products.json")

    logger.info("Inserting data into product_categories collection")
    product_categories_collection.insert_many(product_categories_data)

    logger.info("Inserting data into products collection")
    products_collection.insert_many(products_data)
    
    generate_sale_transactions_test_data(5000)

    logger.info("Database populated successfully")


if __name__ == "__main__":
    populate()
