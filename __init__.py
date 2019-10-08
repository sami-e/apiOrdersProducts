from flask import Flask, redirect, url_for, request, Response
from inf5190 import models
from inf5190 import views
from inf5190 import services


def create_app(initial_config=None):
    app = Flask("inf5190")
    models.init_app(app)
    
    @app.route("/")
    def index():
        products = services.ProductServices.get_products()
        return products.response, products.status, products.headers
    
    @app.route("/order", methods=["POST"])
    def create_order():
        order = services.OrderServices.new_order(request.json)
        if order.status == "422 UNPROCESSABLE ENTITY":
            return order.response, order.status, order.headers
        return redirect(url_for("get_order", order_id=order.response)), order.status
    
    @app.route("/order/<int:order_id>", methods=["GET"])
    def get_order(order_id):
        order = services.OrderServices.formatted_order(order_id)
        return order.response, order.status, order.headers
    
    return app
