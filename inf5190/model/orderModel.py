from inf5190.model.creditCardModel import CreditCard
from inf5190.model import models
from inf5190.model.shippingInfoModel import ShippingInformation
from inf5190.model.transactionModel import Transaction
from peewee import CharField, ForeignKeyField, IntegerField, BooleanField


class Order(models.BaseModel):
    total_price = IntegerField()
    email = CharField(null=True)
    credit_card = ForeignKeyField(CreditCard, backref="orders", null=True)
    shipping_information = ForeignKeyField(ShippingInformation, backref="orders", null=True)
    paid = BooleanField()
    transaction = ForeignKeyField(Transaction, backref="orders", null=True)
    shipping_price = IntegerField()
    in_progress = BooleanField()
