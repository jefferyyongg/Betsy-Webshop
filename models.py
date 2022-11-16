# Models go here
from enum import unique
import os
from peewee import *

db = SqliteDatabase("webshop.db")


class BaseModel(Model):
    class Meta:
        database = db


# Tags should not duplicate
class Tag(BaseModel):
    name = CharField()


class Product(BaseModel):
    name = CharField()
    description = CharField()
    price_per_unit = DecimalField(decimal_places=2, auto_round=True)
    tag = ManyToManyField(Tag, backref="product")


# Only users should be able to purchase goods
class User(BaseModel):
    name = CharField()
    address_data = CharField()
    billing_information = CharField()
    product = ManyToManyField(Product, backref="user")


class User_to_product(BaseModel):
    user_id = ForeignKeyField(User)
    product_id = ForeignKeyField(Product)
    quantity = IntegerField()


class Product_to_tag(BaseModel):
    product_id = ForeignKeyField(Product)
    tag_id = ForeignKeyField(Tag)


class Transaction(BaseModel):
    buyer = ForeignKeyField(User, backref="transactions")
    purchased_product = ForeignKeyField(Product, backref="transactions")
    quantity = IntegerField()
