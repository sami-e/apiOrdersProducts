from flask import Response, jsonify
from inf5190.model.productModel import Product


class ProductController:
    @classmethod
    def get_products(cls):
        db_products = Product.select()
        products_list = []
        for db_product in db_products:
            product = {"description": db_product.description, "id": db_product.id, "image": db_product.image,
                       "in_stock": db_product.in_stock, "name": db_product.name, "price": db_product.price,
                       "weight": db_product.weight}
            products_list.append(product)
        return Response(response=jsonify({"products": products_list}), status=200,
                        headers={"Content-Type": "application/json; charset=utf-8"})
