from flask import Flask, redirect, url_for, request
from inf5190.controller.orderController import OrderController
from inf5190.controller.productController import ProductController
from inf5190.services import init_app


def create_app(initial_config=None):
    app = Flask("inf5190")
    init_app(app)
    
    @app.route("/")
    def index():
        products = ProductController.get_products()
        return products.response, products.status, products.headers
    
    @app.route("/order", methods=["POST"])
    def create_order():
        order = OrderController.new_order(request.json)
        if order.status == "422 UNPROCESSABLE ENTITY":
            return order.response, order.status, order.headers
        return redirect(url_for("get_order", order_id=order.response)), order.status
    
    @app.route("/order/<int:order_id>", methods=["GET"])
    def get_order(order_id):
        order = OrderController.formatted_order(order_id)
        return order.response, order.status, order.headers
    
    return app

