from inf5190.model import models
from peewee import CharField, IntegerField


class CreditCard(models.BaseModel):
    name = CharField()
    first_digits = CharField()
    last_digits = CharField()
    expiration_year = IntegerField()
    expiration_month = IntegerField()
