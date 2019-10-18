from flask import abort, Response, jsonify

from inf5190.services import perform_request
from inf5190.model.productModel import Product
from inf5190.model.orderModel import Order
from inf5190.model.shippingInfoModel import ShippingInformation
from inf5190.model.creditCardModel import CreditCard
from inf5190.model.transactionModel import Transaction


class OrderController:
    @classmethod
    def formatted_order(cls, order_id):
        order = Order.get_or_none(Order.id == order_id)
        if not order:
            return abort(404)
        
        product = {"id": order.product.id, "quantity": order.quantity}
        
        if not order.credit_card:
            credit_card = {}
            transaction = {}
            paid = False
        else:
            credit_card = {
                "name": order.credit_card.name,
                "first_digits": order.credit_card.first_digits,
                "last_digits": order.credit_card.last_digits,
                "expiration_year": order.credit_card.expiration_year,
                "expiration_month": order.credit_card.expiration_month
            }
            transaction = {
                "id": order.transaction.id,
                "success": order.transaction.success,
                "amount_charged": order.transaction.amount_charged
            }
            paid = True
    
        if not order.shipping_information:
            shipping_information = {}
        else:
            shipping_information = {
                "country": order.shipping_information.country,
                "address": order.shipping_information.address,
                "postal_code": order.shipping_information.postal_code,
                "city": order.shipping_information.city,
                "province": order.shipping_information.province
            }

        order_dict = {"id": order.id, "total_price": order.total_price, "email": order.email,
                      "credit_card": credit_card, "shipping_information": shipping_information,
                      "paid": paid, "transaction": transaction, "product": product,
                      "shipping_price": order.shipping_price}
        return Response(response=jsonify({"order": order_dict}), status=200,
                        headers={"Content-Type": "application/json; charset=utf-8"})

    @classmethod
    def create_order(cls, post_data):
        if "product" in post_data and "id" in post_data["product"] and "quantity" in post_data["product"] \
                and isinstance(post_data["product"]["id"], int) and isinstance(post_data["product"]["quantity"], int) \
                and post_data["product"]["quantity"] > 0:

            product_id = post_data["product"]["id"]
            quantity = post_data["product"]["quantity"]
            product = Product.get_or_none(Product.id == product_id)

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

            price = product.price
            weight = product.weight
            total_price = price * quantity
            if weight < 500.0:
                shipping_price = 5
            elif weight < 2000.0:
                shipping_price = 10
            else:
                shipping_price = 25

            order = Order.create(product_id=product_id, quantity=quantity, total_price=total_price,
                                 shipping_price=shipping_price, paid=False)
            return Response(response=order.id, status=302)

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

    @classmethod
    def update_order(cls, post_data, order_id):
        order = Order.get_or_none(Order.id == order_id)
        if order.email:
            cls.update_credit_card(post_data, order_id)
        else:
            if "order" in post_data and "email" in post_data["order"] and "shipping_information" in post_data["order"] \
                    and "country" in post_data["order"]["shipping_information"] \
                    and "address" in post_data["order"]["shipping_information"] \
                    and "postal_code" in post_data["order"]["shipping_information"] \
                    and "city" in post_data["order"]["shipping_information"] \
                    and "province" in post_data["order"]["shipping_information"]:
                email = post_data["order"]["email"]
                country = post_data["order"]["shipping_information"]["country"]
                address = post_data["order"]["shipping_information"]["address"]
                postal_code = post_data["order"]["shipping_information"]["postal_code"]
                city = post_data["order"]["shipping_information"]["city"]
                province = post_data["order"]["shipping_information"]["province"]
                shipping_information = ShippingInformation.create(country=country, address=address,
                                                                  postal_code=postal_code,
                                                                  city=city, province=province)
                Order.update(email=email,
                             shipping_information=shipping_information.id).where(Order.id == order_id).execute()
                return Response(status=200)

            else:
                error_missing = {
                    "errors": {
                        "order": {
                            "code": "missing-fields",
                            "name": "Il manque un ou plusieurs champs qui sont obligatoire"
                        }
                    }
                }
                return Response(response=jsonify(error_missing), status=422,
                                headers={"Content-Type": "application/json; charset=utf-8"})

    @staticmethod
    def update_credit_card(post_data, order_id):
        order = Order.get_or_none(Order.id == order_id)
        if order.paid:
            error_already_paid = {
                "errors": {
                    "order": {
                        "code": "already-paid",
                        "name": "La commande a déjà été payée."
                    }
                }
            }
            return Response(response=jsonify(error_already_paid), status=422,
                            headers={"Content-Type": "application/json; charset=utf-8"})
        
        if "credit_card" in post_data and "name" in post_data["credit_card"] and "number" in post_data["credit_card"] \
                and "expiration_year" in post_data["credit_card"] and "cvv" in post_data["credit_card"] \
                and "expiration_month" in post_data["credit_card"]:
            name = post_data["credit_card"]["name"]
            number = post_data["credit_card"]["number"]
            expiration_month = post_data["credit_card"]["expiration_month"]
            expiration_year = post_data["credit_card"]["expiration_year"]
            cvv = post_data["credit_card"]["cvv"]
            
            payment_data = {"credit_card": {
                                "name": name,
                                "number": number,
                                "expiration_year": expiration_year,
                                "cvv": cvv,
                                "expiration_month": expiration_month
                                },
                            "amount_charged": order.total_price+order.shipping_price}
            payment_response = perform_request(uri="pay", method="POST", data=payment_data)[0]
            
            if payment_response:
                credit_card = CreditCard.create(name=payment_response["credit_card"]["name"],
                                                first_digits=payment_response["credit_card"]["first_digits"],
                                                last_digits=payment_response["credit_card"]["last_digits"],
                                                expiration_year=payment_response["credit_card"]["expiration_year"],
                                                expiration_month=payment_response["credit_card"]["expiration_month"])
                transaction = Transaction.create(id=payment_response["transaction"]["id"],
                                                 success=payment_response["transaction"]["success"],
                                                 amount_charged=payment_response["transaction"]["amount_charged"])
                Order.update(credit_card=credit_card.id,
                             transaction=transaction.id).where(Order.id == order_id).execute()
                return Response(status=200)
            else:
                error_declined = {
                    "errors": {
                        "credit_card": {
                            "code": "card-declined",
                            "name": "La carte de crédit a été déclinée"
                        }
                    }
                }
            return Response(response=jsonify(error_declined), status=422,
                            headers={"Content-Type": "application/json; charset=utf-8"})
        
        else:
            error_missing = {
                "errors": {
                    "order": {
                        "code": "missing-fields",
                        "name": "Les informations du client sont nécessaire avant d'appliquer une carte de crédit"
                    }
                }
            }
            return Response(response=jsonify(error_missing), status=422,
                            headers={"Content-Type": "application/json; charset=utf-8"})
