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


def get_expenses_collection():
    db = get_db()
    return db.expenses


def fetch_sale_transactions():
    sale_transactions_collection = get_sale_transactions_collection()
    transactions = sale_transactions_collection.find()
    return transactions


def fetch_expenses(start_date, end_date):
    # filter
    date_range = {
        "expense_date": {
            "$gte": (start_date),
            "$lte": (end_date),
        }
    }

    pipeline = [{"$match": date_range}, {"$project": {"_id": 0, "expense_image": 0}}]

    result = get_expenses_collection().aggregate(pipeline)
    return result


def fetch_daily_total_expenses(start_date, end_date):
    date_range = {
        "expense_date": {
            "$gte": (start_date),
            "$lte": (end_date),
        }
    }

    pipeline = [
        {"$match": date_range},
        {"$group": {"_id": "$expense_date", "total_amount": {"$sum": "$amount"}}},
        {"$project": {"_id": 0, "expense_date": "$_id", "total_amount": 1}},
        {"$sort": {"expense_date": 1}},
    ]

    result = get_expenses_collection().aggregate(pipeline)
    return result


def fetch_expenses_by_day_of_week(start_date, end_date):
    date_range = {
        "expense_date": {
            "$gte": start_date,
            "$lte": end_date,
        }
    }

    pipeline = [
        {"$match": date_range},
        {
            "$project": {
                "day_of_week": {"$dayOfWeek": {"$toDate": "$expense_date"}},
                "amount": 1,
            }
        },
        {"$group": {"_id": "$day_of_week", "total_amount": {"$sum": "$amount"}}},
        {"$project": {"_id": 0, "day_of_week": "$_id", "total_amount": 1}},
        {"$sort": {"day_of_week": 1}},
    ]

    result = get_expenses_collection().aggregate(pipeline)
    return result


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
                "price": "$products.price",
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


def fetch_products_sales_qty(start_date, end_date):
    # filter
    date_range = {
        "date": {
            "$gte": (start_date),
            "$lte": (end_date),
        }
    }

    # unwind products and group by product_name to sum the quantities and total sales
    pipeline = [
        {"$match": date_range},
        {"$unwind": "$products"},
        {
            "$group": {
                "_id": "$products.product_name",
                "total_quantity": {"$sum": "$products.quantity"},
                "total_sales": {
                    "$sum": {"$multiply": ["$products.price", "$products.quantity"]}
                },
            }
        },
        {
            "$project": {
                "_id": 0,
                "product_name": "$_id",
                "total_quantity": 1,
                "total_sales": 1,
            }
        },
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
        {"$sort": {"date": 1}},
    ]

    result = get_sale_transactions_collection().aggregate(pipeline)
    return result


def fetch_transactions_per_day(start_date, end_date):
    # filter
    date_range = {
        "date": {
            "$gte": start_date,
            "$lte": end_date,
        }
    }

    # group by date and count the number of transactions within each group
    pipeline = [
        {"$match": date_range},
        {"$group": {"_id": "$date", "transaction_count": {"$sum": 1}}},
        {"$project": {"_id": 0, "date": "$_id", "transaction_count": 1}},
        {"$sort": {"date": 1}},
    ]

    result = get_sale_transactions_collection().aggregate(pipeline)
    return result


def fetch_number_of_products_per_transaction(start_date, end_date):
    # filter
    date_range = {
        "date": {
            "$gte": (start_date),
            "$lte": (end_date),
        }
    }

    # include only the products field and calculate the size of the array
    pipeline = [
        {"$match": date_range},
        {"$project": {"_id": 0, "num_products": {"$size": "$products"}}},
    ]

    result = get_sale_transactions_collection().aggregate(pipeline)
    return result


def fetch_sale_transactions_by_day_of_week(start_date, end_date):
    date_range = {
        "date": {
            "$gte": start_date,
            "$lte": end_date,
        }
    }

    pipeline = [
        {"$match": date_range},
        {
            "$project": {
                "day_of_week": {"$dayOfWeek": {"$toDate": "$date"}},
                "total_amount": "$total",
            }
        },
        {"$group": {"_id": "$day_of_week", "total_amount": {"$sum": "$total_amount"}}},
        {"$project": {"_id": 0, "day_of_week": "$_id", "total_amount": 1}},
        {"$sort": {"day_of_week": 1}},
    ]

    result = get_sale_transactions_collection().aggregate(pipeline)
    return result
