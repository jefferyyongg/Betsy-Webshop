from models import *
from peewee import *


def delete_database():
    cwd = os.getcwd()
    database_path = os.path.join(cwd, "webshop.db")
    if os.path.exists(database_path):
        os.remove(database_path)


def insert_data():

    db.connect()

    db.create_tables(
        [
            User,
            Tag,
            Product,
            Transaction,
            User_to_product,
            Product_to_tag
        ]
    )

    users = [
        {"name": "Bob", "address_data": "street123",
            "billing_information": "juist'em"},
        {"name": "Alice", "address_data": "roadman123",
            "billing_information": "got'em"},
        {"name": "Caitlyn", "address_data": "atlantic123",
            "billing_information": "bought'em"}
    ]

    User.insert_many(users).execute()

    products = [
        {"name": "kitchen knife", "description": "Sharp kitchen knife",
            "price_per_unit": 25.99},
        {"name": "dog toy", "description": "very squeaky and loud",
            "price_per_unit": 14.99},
        {"name": "portable swimming pool", "description": "6x6x6 very durable",
            "price_per_unit": 59.99},
        {"name": "football", "description": "Pro football",
            "price_per_unit": 25.99},
        {"name": "dog food", "description": "delicious treat for pet",
            "price_per_unit": 14.99},
        {"name": "outside pet house", "description": "very durable",
            "price_per_unit": 59.99}
    ]

    Product.insert_many(products).execute()

    tags = [
        {"name": "Cookwear"},
        {"name": "Houseware"},
        {"name": "Pet-Toys"},
        {"name": "Sports"}
    ]

    Tag.insert_many(tags).execute()

    userproduct_data = [
        {"user_id": 1,  "product_id": 2, "quantity": 8},
        {"user_id": 1,  "product_id": 5, "quantity": 14},
        {"user_id": 1,  "product_id": 6, "quantity": 4},
        {"user_id": 2,  "product_id": 3, "quantity": 8},
        {"user_id": 2,  "product_id": 4, "quantity": 14},
        {"user_id": 3,  "product_id": 1, "quantity": 4},
    ]

    User_to_product.insert_many(userproduct_data).execute()

    producttag_data = [
        {"product_id": 1, "tag_id": 1},
        {"product_id": 1, "tag_id": 2},
        {"product_id": 2, "tag_id": 3},
        {"product_id": 3, "tag_id": 4},
        {"product_id": 4, "tag_id": 4},
        {"product_id": 5, "tag_id": 3},
        {"product_id": 6, "tag_id": 3},
    ]

    Product_to_tag.insert_many(producttag_data).execute()

    db.close()
