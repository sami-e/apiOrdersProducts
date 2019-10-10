from peewee import CharField, FloatField, BooleanField, IntegerField
from inf5190.model import models


class Product(models.BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    in_stock = BooleanField()
    description = CharField()
    price = FloatField()
    image = CharField(null=True)
    weight = FloatField(null=True)
