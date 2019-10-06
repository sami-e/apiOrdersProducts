import os
import click, json
from urllib.request import urlopen
from flask.cli import with_appcontext
from peewee import Model, SqliteDatabase, CharField, ForeignKeyField, FloatField, IntegerField, BooleanField


def get_db_path():
    return os.environ.get('DATABASE', './inf5190/db.sqlite')


class BaseModel(Model):
    class Meta:
        database = SqliteDatabase(get_db_path())


class Product(BaseModel):
    name = CharField()
    in_stock = BooleanField()
    description = CharField()
    price = FloatField()
    image = CharField(null=True)
    quantity = IntegerField(null=True)
    weight = FloatField(null=True)


class CreditCard(BaseModel):
    name = CharField()
    first_digits = CharField()
    last_digits = CharField()
    expiration_year = IntegerField()
    expiration_month = IntegerField()


class ShippingInformation(BaseModel):
    country = CharField()
    address = CharField()
    postal_code = CharField()
    city = CharField()
    province = CharField(null=True)


class Transaction(BaseModel):
    id = CharField(primary_key=True)
    success = BooleanField()
    amount_charged = IntegerField()


class Order(BaseModel):
    total_price = FloatField()
    email = CharField()
    credit_card = ForeignKeyField(CreditCard, backref="orders")
    shipping_information = ForeignKeyField(ShippingInformation, backref="orders")
    paid = BooleanField()
    transaction = ForeignKeyField(Transaction, backref="orders")
    product = ForeignKeyField(Product, backref="orders")
    shipping_price = IntegerField()


@click.command("init-db")
@with_appcontext
def init_db_command():
    database = SqliteDatabase(get_db_path())
    database.create_tables([Product, CreditCard, ShippingInformation, Transaction, Order])
    with urlopen("https://caissy.dev/shops/products") as response:
        data = json.loads(response.read())
        for product in data["products"]:
            Product.create(name=product["name"], image=product["image"], description=product["description"],
                           price=product["price"], in_stock=product["in_stock"], weight=product["weight"])
    click.echo("Initialized the database.")


def init_app(app):
    app.cli.add_command(init_db_command)
