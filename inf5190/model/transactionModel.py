from inf5190.model import models
from peewee import CharField, IntegerField, BooleanField


class Transaction(models.BaseModel):
    code = CharField(null=True)
    success = BooleanField()
    amount_charged = IntegerField()
    error_code = CharField(null=True)
    error_name = CharField(null=True)
