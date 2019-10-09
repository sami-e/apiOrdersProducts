from flask import abort, Response, jsonify
from inf5190.model.productModel import Product
from inf5190.model.orderModel import Order


class OrderController:
    @classmethod
    def formatted_order(cls, order_id):
        order = Order.get_or_none(Order.id == order_id)
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
        return Response(response=jsonify({"order": order_dict}), status=200,
                        headers={"Content-Type": "application/json; charset=utf-8"})
    
    @classmethod
    def new_order(cls, post_data):
        if "product" in post_data and "id" in post_data["product"] and "quantity" in post_data["product"] \
                and post_data["product"] and post_data["product"]["id"] and post_data["product"]["quantity"] \
                and post_data["product"]["quantity"] > 0:
            
            product_id = post_data["product"]["id"]
            quantity = post_data["product"]["quantity"]
            product = Product.get_or_none(Product.id == product_id)
            price = product.price
            weight = product.weight
            total_price = price * quantity
            if weight < 500.0:
                shipping_price = 5
            elif weight < 2000.0:
                shipping_price = 10
            else:
                shipping_price = 25
            
            if not product or not product.in_stock:
                error_stock = {
                    "errors": {
                        "product": {
                            "code": "out-of-inventory",
                            "name": "Le produit demandé n'est pas en inventaire"
                        }
                    }
                }
                return Response(response=jsonify(error_stock), status=422,
                                headers={"Content-Type": "application/json; charset=utf-8"})
            
            order = Order.create(product_id=product_id, quantity=quantity, total_price=total_price,
                                 shipping_price=shipping_price, paid=False)
            order_id = order.id
            return Response(response=order_id, status=302)
        
        else:
            error_missing = {
                "errors": {
                    "product": {
                        "code": "missing-fields",
                        "name": "La création d'une commande nécessite un produit"
                    }
                }
            }
            return Response(response=jsonify(error_missing), status=422,
                            headers={"Content-Type": "application/json; charset=utf-8"})
