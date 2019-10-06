import json
from flask import Flask, abort, redirect, url_for, request
from inf5190 import models
from inf5190 import views
from inf5190 import services


def create_app(initial_config=None):
    app = Flask("inf5190")
    models.init_app(app)
    
    @app.route("/")
    def index():
        return services.ProductServices.get_products()

    @app.route("/order", methods=["POST"])
    def create_order():
        order = services.OrderServices.new_order(request.json)
        return redirect(url_for("get_order", order_id=order.id))
    
    @app.route("/order/<int:order_id>", methods=["GET"])
    def get_order(order_id):
        return services.OrderServices.formatted_order(order_id)
    
    return app
