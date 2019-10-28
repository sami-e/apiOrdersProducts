from inf5190.model.productModel import Product
from inf5190.view import views


class ProductController:
    @classmethod
    def get_products(cls):
        db_products = Product.select()
        return views.display_products(db_products)
