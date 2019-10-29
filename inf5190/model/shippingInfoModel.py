from inf5190.model import models
from peewee import CharField


class ShippingInformation(models.BaseModel):
    country = CharField()
    address = CharField()
    postal_code = CharField()
    city = CharField()
    province = CharField(null=True)
