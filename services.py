import json
from flask import abort
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from inf5190 import models

BASE_URL = "https://caissy.dev/shops"


class ProductServices:
    @classmethod
    def get_products(cls):
        db_products = models.Product.select()
        product_list = []
        for db_product in db_products:
            product = {"description": db_product.description, "id": db_product.id, "image": db_product.image,
                       "in_stock": db_product.in_stock, "name": db_product.name, "price": db_product.price,
                       "weight": db_product.weight}
            product_list.append(product)
        return {"products": product_list}


class OrderServices:
    @classmethod
    def formatted_order(cls, order_id):
        order = models.Order.get_or_none(models.Order.id == order_id)
        if not order:
            return abort(404)
        product = {"id": order.product.id, "quantity": order.quantity}
        credit_card = {}
        transaction = {}
        shipping_information = {}
        paid = False
        order_dict = {"id": order.id, "total_price": order.total_price, "email": order.email,
                      "credit_card": credit_card, "shipping_information": shipping_information,
                      "paid": paid, "transaction": transaction, "product": product,
                      "shipping_price": order.shipping_price}
        return {"order": order_dict}
    
    @classmethod
    def new_order(cls, post_data):
        product_id = post_data["product"]["id"]
        quantity = post_data["product"]["quantity"]
        product = models.Product.get_or_none(models.Product.id == product_id)
        price = product.price
        weight = product.weight
        total_price = price * quantity
        if weight < 500.0:
            shipping_price = 5
        elif weight < 2000.0:
            shipping_price = 10
        else:
            shipping_price = 25
        return models.Order.create(product_id=product_id, quantity=quantity, total_price=total_price, shipping_price=shipping_price)


class ApiError(Exception):
    pass


def perform_request(uri, method="GET", data=None):
    request = Request(f"{BASE_URL}/{uri}")
    request.method = method
    request.add_header("content-type", "application/json")
    
    if data:
        request.data = json.dumps(data).encode('utf-8')
    
    try:
        with urlopen(request) as response:
            data = response.read()
            headers = response.headers
            if headers["content-type"] == "application/json":
                return json.loads(data)
            else:
                return None
    
    except HTTPError as e:
        code = e.code
        headers = e.headers
        data = e.read()
        error = ApiError()
        error.code = code
        if headers["content-type"] == "application/json":
            error.content = json.loads(data)
        raise error
