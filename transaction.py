from models import *
from peewee import *


def report(product_id, buyer_id, quantity):
    Transaction.insert(
        {Transaction.buyer: buyer_id, Transaction.purchased_product: product_id, Transaction.quantity: quantity}).execute()
