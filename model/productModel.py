from peewee import CharField, FloatField, BooleanField
from inf5190.model import models


class Product(models.BaseModel):
    name = CharField()
    in_stock = BooleanField()
    description = CharField()
    price = FloatField()
    image = CharField(null=True)
    weight = FloatField(null=True)
