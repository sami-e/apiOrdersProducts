from flask import Flask, redirect, url_for, request
from inf5190.controller.orderController import OrderController
from inf5190.controller.productController import ProductController
from inf5190.model.productModel import Product
from inf5190.services import init_app, perform_request


def create_app(initial_config=None):
    app = Flask("__name__")
    init_app(app)

    @app.before_first_request
    def init_products_list():
        data = perform_request("products")
        for product in data["products"]:
            Product.create(id=product["id"], name=product["name"], image=product["image"],
                           description=product["description"],
                           price=product["price"], in_stock=product["in_stock"], weight=product["weight"])

    @app.route("/", methods=["GET"])
    def index():
        products = ProductController.get_products()
        return products.response, products.status, products.headers

    @app.route("/order", methods=["POST"])
    def post_order():
        order = OrderController.create_order(request.json)
        if order.status == "422 UNPROCESSABLE ENTITY":
            return order.response, order.status, order.headers
        return redirect(url_for("get_order", order_id=order.response)), order.status

    @app.route("/order/<int:order_id>", methods=["GET"])
    def get_order(order_id):
        order = OrderController.formatted_order(order_id)
        return order.response, order.status, order.headers

    @app.route("/order/<int:order_id>", methods=["PUT"])
    def put_order(order_id):
        order = OrderController.update_order(request.json, order_id)
        if order.status == "422 UNPROCESSABLE ENTITY":
            return order.response, order.status, order.headers
        new_order = OrderController.formatted_order(order_id)
        return new_order.response, new_order.status, new_order.headers

    return app
