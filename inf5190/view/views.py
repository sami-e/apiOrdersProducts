from flask import Response, jsonify


def display_products(db_products):
    products_list = []
    for db_product in db_products:
        product = {"description": db_product.description, "id": db_product.id, "image": db_product.image,
                   "in_stock": db_product.in_stock, "name": db_product.name, "price": db_product.price,
                   "weight": db_product.weight}
        products_list.append(product)
    return Response(response=jsonify({"products": products_list}), status=200,
                    headers={"Content-Type": "application/json; charset=utf-8"})


def display_order(order, product_order_list):
    if not order:
        error_not_found = {
            "errors": {
                "order": {
                    "code": "not-found",
                    "name": "La commande demandée n'existe pas"
                }
            }
        }
        return Response(response=jsonify(error_not_found), status=404,
                        headers={"Content-Type": "application/json; charset=utf-8"})
    
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
    
    if not order.credit_card:
        credit_card = {}
    else:
        credit_card = {
            "name": order.credit_card.name,
            "first_digits": order.credit_card.first_digits,
            "last_digits": order.credit_card.last_digits,
            "expiration_year": order.credit_card.expiration_year,
            "expiration_month": order.credit_card.expiration_month
        }

    if not order.transaction:
        transaction = {}
    elif not order.credit_card:
        error = {
            "code": order.transaction.error_code,
            "name": order.transaction.error_name
        }
        transaction = {
            "success": order.transaction.success,
            "amount_charged": order.transaction.amount_charged,
            "error": error
        }
    else:
        transaction = {
            "id": order.transaction.code,
            "success": order.transaction.success,
            "amount_charged": order.transaction.amount_charged,
            "error": {}
        }
    
    order_dict = {"id": order.id, "total_price": order.total_price, "email": order.email,
                  "credit_card": credit_card, "shipping_information": shipping_information,
                  "paid": order.paid, "transaction": transaction, "products": product_order_list,
                  "shipping_price": order.shipping_price}
    return Response(response=jsonify({"order": order_dict}), status=200,
                    headers={"Content-Type": "application/json; charset=utf-8"})


def display_error_out_of_inventory():
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


def display_error_missing_fields_product():
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


def display_error_missing_fields_order():
    error_missing = {
        "errors": {
            "order": {
                "code": "missing-fields",
                "name": "Il manque un ou plusieurs champs qui sont obligatoires"
            }
        }
    }
    return Response(response=jsonify(error_missing), status=422,
                    headers={"Content-Type": "application/json; charset=utf-8"})


def display_error_missing_shipping_info():
    error_no_shipping_info = {
        "errors": {
            "order": {
                "code": "missing-fields",
                "name": "Les informations du client sont nécessaires avant d'appliquer une carte de crédit"
            }
        }
    }
    return Response(response=jsonify(error_no_shipping_info), status=422,
                    headers={"Content-Type": "application/json; charset=utf-8"})


def display_error_already_paid():
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


def display_post_redirect(order_id):
    return Response(response=order_id, status=302)


def display_ok():
    return Response(status=200)


def display_order_standby():
    return Response(response=jsonify({}), status=202,
                    headers={"Content-Type": "application/json; charset=utf-8"})

def display_order_standby_conflict():
    return Response(response=jsonify({}), status=409,
                    headers={"Content-Type": "application/json; charset=utf-8"})
