from flask import Flask
from .models import init_app, Product, kkj
from .services import perform_request


def create_app(initial_config=None):
    app = Flask("inf5190")
    init_app(app)

    @app.route('/')
    def index():
        kkj()
        return perform_request('products')

    @app.route('/<int:prod_id>', methods=['GET'])
    def product(prod_id):
        prt = Product.get_by_id(prod_id)
        return prt

    return app
