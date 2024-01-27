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


def fetch_cat_qty_price(start_date, end_date):
    # filter
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
        {
            "$project": {
                "_id": 0,
                "category": "$products.category",
                "quantity": "$products.quantity",
                "price": "$products.price"
            }
        },
    ]

    result = get_sale_transactions_collection().aggregate(pipeline)
    return result


def fetch_transaction_totals(start_date, end_date):
    # filter
    date_range = {
        "date": {
            "$gte": (start_date),
            "$lte": (end_date),
        }
    }

    # project only the total field
    pipeline = [{"$match": date_range}, {"$project": {"_id": 0, "total": "$total"}}]

    result = get_sale_transactions_collection().aggregate(pipeline)
    return result


def fetch_products_and_qty(start_date, end_date):
    # filter
    date_range = {
        "date": {
            "$gte": (start_date),
            "$lte": (end_date),
        }
    }

    # unwind products and group by product_name to sum the quantities
    pipeline = [
        {"$match": date_range},
        {"$unwind": "$products"},
        {
            "$group": {
                "_id": "$products.product_name",
                "total_quantity": {"$sum": "$products.quantity"},
            }
        },
        {"$project": {"_id": 0, "product_name": "$_id", "total_quantity": 1}},
    ]

    # Execute the aggregation pipeline
    result = get_sale_transactions_collection().aggregate(pipeline)
    return result


def fetch_sales_over_time(start_date, end_date):
    # filter
    date_range = {
        "date": {
            "$gte": start_date,
            "$lte": end_date,
        }
    }

    # group by date and sum the total values within each group
    pipeline = [
        {"$match": date_range},
        {"$group": {"_id": "$date", "total_sales": {"$sum": "$total"}}},
        {"$project": {"_id": 0, "date": "$_id", "total_sales": 1}},
        {"$sort": {"date": 1}}
    ]

    result = get_sale_transactions_collection().aggregate(pipeline)
    return result
