import os
from datetime import datetime
from peewee import DoesNotExist
from flask import Flask, request, redirect, url_for, abort, jsonify
from models import init_app


def create_app(initial_config=None):
    app = Flask("inf5190")
    init_app(app)

    @app.route('/')
    def index():
        return "Hello World"

    return app
