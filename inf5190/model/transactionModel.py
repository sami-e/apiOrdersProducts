from inf5190.model import models
from peewee import CharField, IntegerField, BooleanField


class Transaction(models.BaseModel):
    id = CharField(primary_key=True)
    success = BooleanField()
    amount_charged = IntegerField()
    error = CharField()
