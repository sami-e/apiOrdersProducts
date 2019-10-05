from flask import Flask
from .models import init_app


def create_app(initial_config=None):
    app = Flask("inf5190")
    init_app(app)

    @app.route('/')
    def index():
        return "Hello World"

    return app


