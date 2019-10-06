from flask import Flask, abort
# from inf5190 import views
# from inf5190 import services
from .models import init_app


def create_app(initial_config=None):
    app = Flask("inf5190")
    models.init_app(app)
    
    @app.route('/')
    def index():
        db_products = models.Product.select()
        product_list = []
        for db_product in db_products:
            product = {"description": db_product.description, "id": db_product.id, "image": db_product.image,
                       "in_stock": db_product.in_stock, "name": db_product.name, "price": db_product.price,
                       "weight": db_product.weight}
            product_list.append(product)
        return {"products": product_list}
    
    @app.route('/order/<int:order_id>', methods=['GET'])
    def get_order(order_id):
        order = models.Order.get_or_none(models.Order.id == order_id)
        if not order:
            return abort(404)
        return order.name
    
    return app
