from inf5190.model import models
from inf5190.model.orderModel import Order
from inf5190.model.productModel import Product
from peewee import ForeignKeyField, IntegerField


class ProductOrder(models.BaseModel):
    product = ForeignKeyField(Product)
    order = ForeignKeyField(Order, null=True)
    quantity = IntegerField()
