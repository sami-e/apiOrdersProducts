import os
from peewee import Model, SqliteDatabase


def get_db_path():
    return os.environ.get('DATABASE', './inf5190/model/db.sqlite')


class BaseModel(Model):
    class Meta:
        database = SqliteDatabase(get_db_path())
