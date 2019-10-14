import json
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import click
from flask.cli import with_appcontext
from inf5190.model.creditCardModel import CreditCard
from inf5190.model.orderModel import Order
from inf5190.model.productModel import Product
from inf5190.model.shippingInfoModel import ShippingInformation
from inf5190.model.transactionModel import Transaction
from peewee import SqliteDatabase
from inf5190.model.models import get_db_path

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
            code = response.status
            headers = response.headers
            if headers["content-type"] == "application/json":
                return json.loads(data), code
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


@staticmethod
def performe_pos(url, post_fields):
    request = Request(url, urlencode(post_fields).encode())
    json = urlopen(request).read().decode()
    return (json)


@click.command("init-db")
@with_appcontext
def init_db_command():
    database = SqliteDatabase(get_db_path())
    database.create_tables([Product, CreditCard, ShippingInformation, Transaction, Order])
    click.echo("Initialized the database.")


def init_app(app):
    app.cli.add_command(init_db_command)
