__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

from itertools import product
from models import *
from transaction import report
from peewee import *


def search(term):
    query = Product.select(Product.name).where(
        Product.name.contains(term)).dicts()
    for q in query:
        print(f"Products: {q}")


def list_user_products(user_id):
    query = User.select(Product.name).join(
        User_to_product).join(Product).where(User.id == user_id).dicts()
    for q in query:
        print(q)


def list_products_per_tag(tag_id):
    query = Product.select().join(Product_to_tag).join(
        Tag).where(Tag.get_id(Tag) == tag_id).dicts()
    for q in query:
        print(q)


def add_product_to_catalog(user_id, product):

    Product.insert(product).execute()

    query = Product.select(fn.COUNT(Product.id))
    count = query.scalar()

    User_to_product.insert(
        {User_to_product.user_id: user_id, User_to_product.product_id: count}).execute()


# go back and add remove product when quantity == 0
def update_stock(product_id, new_quantity):
    if new_quantity == 0:
        Product.delete().where(Product.id == product_id).execute()
        User_to_product.delete().where(User_to_product.product_id == product_id).execute()
    else:
        Product.update(quantity=new_quantity).where(
            Product.id == product_id).execute()


def purchase_product(product_id, buyer_id, quantity):

    buyer = Product.select().where(Product.id == product_id).dicts()
    for b in buyer:
        b.pop("id")
        add_product_to_catalog(buyer_id, b)
    update_stock(len(Product), quantity)

    seller = Product.select(Product.quantity).where(
        Product.id == product_id).dicts()
    for s in seller:
        update_stock(product_id, list(s.values())[0] - quantity)

    report(product_id, buyer_id, quantity)


def remove_product(product_id):
    Product.delete().where(Product.id == product_id).execute()
    User_to_product.delete().where(User_to_product.product_id == product_id).execute()
