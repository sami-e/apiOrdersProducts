import os
import click
from flask.cli import with_appcontext
from peewee import Model, SqliteDatabase, AutoField, CharField, DateTimeField, ForeignKeyField, FloatField, IntegerField


def get_db_path():
    return os.environ.get('DATABASE', './db.sqlite')


class BaseModel(Model):
    class Meta:
        database = SqliteDatabase(get_db_path())


class Product(BaseModel):
    description = CharField(null=False)
    id = AutoField(primary_key=True)
    image = CharField(null=False)
    quantity = IntegerField(unique=True)
    price = FloatField()
    in_stock = CharField(null=False)
    name = CharField(unique=True, null=False)


class Order(BaseModel):
    id = AutoField(primary_key=True)
    total_price = FloatField()
    email = CharField(null=False)
    credit_card = IntegerField()
    paid = CharField(null=False)
    transaction = CharField(null=False)
    products = ForeignKeyField(Products, backref="choices")
    quantity = ForeignKeyField(Products.quantity)
    shiping_price = FloatField()
    image = CharField(null=False)


class Shipping_Information(BaseModel):
    country = CharField(null=False)
    address = CharField(null=False)
    postal_code = CharField(null=False)
    city = CharField(null=False)
    province = CharField(null=False)


#class Poll(BaseModel):
#   id = AutoField(primary_key=True)
#   name = CharField(null=False)
#    date = DateTimeField()

#    def number_of_votes(self):
#        return self.vote_casts.count()

#    def __str__(self):
#        return self.name


#class Choice(BaseModel):
#    id = AutoField(primary_key=True)
#    choice = CharField(null=False)
#    poll = ForeignKeyField(Poll, backref="choices")

#    def number_of_votes(self):
#        return self.vote_casts.count()

#    def __str__(self):
#        return self.choice


class VoteCast(BaseModel):
    id = AutoField(primary_key=True)
    poll = ForeignKeyField(Poll, backref="vote_casts")
    choice = ForeignKeyField(Choice, backref="vote_casts")


@click.command("init-db")
@with_appcontext
def init_db_command():
    database = SqliteDatabase(get_db_path())
    database.create_tables([Products, Order, Shipping_Information])
    click.echo("Initialized the database.")


def init_app(app):
    app.cli.add_command(init_db_command)
