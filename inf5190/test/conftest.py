import os
import pytest
from peewee import SqliteDatabase
from inf5190 import create_app
from inf5190.model.models import get_db_path
from inf5190.model.creditCardModel import CreditCard
from inf5190.model.orderModel import Order
from inf5190.model.productModel import Product
from inf5190.model.shippingInfoModel import ShippingInformation
from inf5190.model.transactionModel import Transaction

os.environ['DATABASE'] = ":memory:"


@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    database = SqliteDatabase(get_db_path())
    database.create_tables([Product, CreditCard, ShippingInformation, Transaction, Order])

    yield app

    database.drop_tables([Product, CreditCard, ShippingInformation, Transaction, Order])
    
    
@pytest.fixture
def client(app):
    return app.test_client()
