import os
import click

from flask.cli import with_appcontext
from peewee import Model, SqliteDatabase, CharField, ForeignKeyField, FloatField, IntegerField, BooleanField
from .services import perform_request


def get_db_path():
    return os.environ.get('DATABASE', './inf5190/db.sqlite')


class BaseModel(Model):
    class Meta:
        database = SqliteDatabase(get_db_path())


class Product(BaseModel):
    id = IntegerField(null=False)
    name = CharField(unique=True, null=False)
    in_stock = CharField(null=False)
    description = CharField(null=False)
    price = FloatField(null=False)
    image = CharField()
    weight = FloatField()


class CreditCard(BaseModel):
    name = CharField(null=False)
    first_digits = CharField(unique=True, null=False)
    last_digits = CharField(unique=True, null=False)
    expiration_year = IntegerField(null=False)
    expiration_month = IntegerField(null=False)


class ShippingInformation(BaseModel):
    country = CharField(null=False)
    address = CharField(null=False)
    postal_code = CharField(null=False)
    city = CharField(null=False)
    province = CharField(null=False)


class Transaction(BaseModel):
    id = CharField(primary_key=True, null=False)
    success = BooleanField(null=False)
    amount_charged = IntegerField(null=False)


class Order(BaseModel):
    total_price = FloatField()
    email = CharField(null=False)
    credit_card = ForeignKeyField(CreditCard, backref="orders")
    shipping_information = ForeignKeyField(ShippingInformation, backref="orders")
    paid = BooleanField(null=False)
    transaction = ForeignKeyField(Transaction, backref="orders")
    product = ForeignKeyField(Product, backref="orders")
    shipping_price = IntegerField(null=False)


class Prods(object):
    @classmethod
    def get_product_by_id(cls, yt):
        db = SqliteDatabase(get_db_path())
        raw_product = db.execute("SELECT id, name FROM Product WHERE id = ?", [yt]).fetchone()

        if raw_product:
            return cls(
                id=raw_product[0],
                name=raw_product[1],
            )

        return None


def kkj():
    data = perform_request('products')
    database = SqliteDatabase(get_db_path(), timeout=15)
    for products in data['products']:
        database.execute(
            "INSERT INTO Product ('id' ,'name' , 'in_stock','description', 'price', 'image', 'weight' ) VALUES",
            [products['id'], products['name'], products['in_stock'], products['description'],
             products['price'], products['image'], products['weight']])

    database.commit()


@click.command("init-db")
@with_appcontext
def init_db_command():
    database = SqliteDatabase(get_db_path(), timeout=15)
    database.create_tables([Product, CreditCard, ShippingInformation, Transaction, Order])

    click.echo("Initialized the database.")


def init_app(app):
    app.cli.add_command(init_db_command)
