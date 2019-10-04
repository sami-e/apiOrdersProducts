import os
from datetime import datetime
from peewee import DoesNotExist
from flask import Flask, request, redirect, url_for, abort, jsonify
from models import init_app, Product, CreditCard, ShippingInformation, Transaction, Order
import peewee as p


def create_app(initial_config=None):
    app = Flask(__name__)
    init_app(app)

    @app.route('/')
    def index():
        return "Hello World"

    return app


