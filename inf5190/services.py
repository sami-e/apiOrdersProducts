import json
import os
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import click
from flask.cli import with_appcontext
from inf5190.model.creditCardModel import CreditCard
from inf5190.model.orderModel import Order
from inf5190.model.productModel import Product
from inf5190.model.shippingInfoModel import ShippingInformation
from inf5190.model.transactionModel import Transaction
from peewee import PostgresqlDatabase
from inf5190.model.models import get_db

DATABASE_NAME = os.environ.get('DB_NAME', 'inf5190')
BASE_URL = "https://caissy.dev/shops"


class ApiError(Exception):
    pass


def perform_request(uri, method="GET", data=None):
    request = Request(f"{BASE_URL}/{uri}")
    request.method = method
    request.add_header("content-type", "application/json")
    if data:
        request.data = json.dumps(data).encode('utf-8')
    try:
        with urlopen(request) as response:
            data = response.read()
            headers = response.headers
            if headers["content-type"] == "application/json":
                return json.loads(data)
            else:
                return None
    except HTTPError as e:
        code = e.code
        headers = e.headers
        data = e.read()
        error = ApiError()
        error.code = code
        if headers["content-type"] == "application/json":
            error.content = json.loads(data)
        raise error


@click.command("init-db")
@with_appcontext
def init_db_command():
    database = PostgresqlDatabase(DATABASE_NAME, **get_db())
    database.create_tables([Product, CreditCard, ShippingInformation, Transaction, Order])
    click.echo("Initialized the database.")


def init_app(app):
    app.cli.add_command(init_db_command)
