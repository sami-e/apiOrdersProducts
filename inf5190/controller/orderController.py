from inf5190.services import perform_request, ApiError
from inf5190.model.productModel import Product
from inf5190.model.orderModel import Order
from inf5190.model.shippingInfoModel import ShippingInformation
from inf5190.model.creditCardModel import CreditCard
from inf5190.model.transactionModel import Transaction
from inf5190.view import views


class OrderController:
    @classmethod
    def formatted_order(cls, order_id):
        order = Order.get_or_none(Order.id == order_id)
        return views.display_order(order)
    
    @classmethod
    def create_order(cls, post_data):
        if "product" in post_data and "id" in post_data["product"] and "quantity" in post_data["product"] \
                and isinstance(post_data["product"]["id"], int) and isinstance(post_data["product"]["quantity"], int) \
                and post_data["product"]["quantity"] > 0:
            
            product_id = post_data["product"]["id"]
            quantity = post_data["product"]["quantity"]
            product = Product.get_or_none(Product.id == product_id)
            
            if not product or not product.in_stock:
                return views.display_error_out_of_inventory()
            
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
            return views.display_post_redirect(order.id)
        
        else:
            return views.display_error_missing_fields_product()
    
    @classmethod
    def update_order(cls, post_data, order_id):
        if "credit_card" in post_data:
            return cls.update_credit_card(post_data, order_id)
        else:
            return cls.update_shipping_info(post_data, order_id)

    @staticmethod
    def update_shipping_info(post_data, order_id):
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
            return views.display_ok()
    
        else:
            return views.display_error_missing_fields_order()
    
    @staticmethod
    def update_credit_card(post_data, order_id):
        order = Order.get_or_none(Order.id == order_id)
        
        if not order.shipping_information:
            return views.display_error_missing_shipping_info()
        
        if "credit_card" in post_data and "name" in post_data["credit_card"] and "number" in post_data["credit_card"] \
                and "expiration_year" in post_data["credit_card"] and "cvv" in post_data["credit_card"] \
                and "expiration_month" in post_data["credit_card"]:
            
            if order.paid:
                return views.display_error_already_paid()
            
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
                "amount_charged": order.total_price + order.shipping_price}
            
            try:
                payment_response = perform_request(uri="pay", method="POST", data=payment_data)
            except ApiError as error:
                return views.display_error_payment_api(error)
            
            credit_card = CreditCard.create(name=payment_response["credit_card"]["name"],
                                            first_digits=payment_response["credit_card"]["first_digits"],
                                            last_digits=payment_response["credit_card"]["last_digits"],
                                            expiration_year=payment_response["credit_card"]["expiration_year"],
                                            expiration_month=payment_response["credit_card"]["expiration_month"])
            transaction = Transaction.create(id=payment_response["transaction"]["id"],
                                             success=payment_response["transaction"]["success"],
                                             amount_charged=payment_response["transaction"]["amount_charged"])
            Order.update(credit_card=credit_card.id,
                         transaction=transaction.id, paid=True).where(Order.id == order_id).execute()
            return views.display_ok()
        
        else:
            return views.display_error_missing_fields_order()