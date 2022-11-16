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


def add_product_to_catalog(user_id, product, quantity):

    Product.insert(product).execute()

    query = Product.select(fn.COUNT(Product.id))
    count = query.scalar()

    User_to_product.insert(
        {User_to_product.user_id: user_id, User_to_product.product_id: count, User_to_product.quantity: quantity}).execute()


def update_stock(user_id, product_id, new_quantity):
    if new_quantity <= 0:
        User_to_product.delete().where(User_to_product.product_id == product_id).execute()
    else:
        User_to_product.update(quantity=new_quantity).where(
            User_to_product.user_id == user_id and User_to_product.product_id == product_id).execute()


# had to add seller_id otherwise it will subract all sellers quantities with the same product
# Changed the database structure so that multiple can have the same product with varying quantities
def purchase_product(product_id, seller_id, buyer_id, quantity):
    seller = User_to_product.select(User_to_product.quantity, User_to_product.user_id).where(
        User_to_product.user_id == seller_id, User_to_product.product_id == product_id)
    for s in seller:
        if s.quantity - quantity == 0:
            update_stock(s.user_id, product_id, s.quantity - quantity)
        elif s.quantity - quantity < 0:
            print("SELLER DOES NOT HAVE ENOUGH STOCK")
            return
        else:
            update_stock(s.user_id, product_id, s.quantity - quantity)

    buyer = User_to_product.select(User_to_product.user_id, User_to_product.product_id, User_to_product.quantity).where(
        User_to_product.user_id == buyer_id)
    buyer_list = [int(str(b.product_id)) for b in buyer]

    if product_id not in buyer_list:
        User_to_product.insert(
            {User_to_product.user_id: buyer_id, User_to_product.product_id: product_id, User_to_product.quantity: quantity}).execute()
    else:
        for b in User_to_product.select(User_to_product.quantity).where(User_to_product.user_id == buyer_id, User_to_product.product_id == product_id):
            update_stock(buyer_id, product_id, b.quantity + quantity)
    report(product_id, buyer_id, quantity)


def remove_product(product_id):
    Product.delete().where(Product.id == product_id).execute()
    User_to_product.delete().where(User_to_product.product_id == product_id).execute()


if __name__ == "__main__":
    ...
