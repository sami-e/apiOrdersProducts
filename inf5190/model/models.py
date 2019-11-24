import os
from peewee import Model, PostgresqlDatabase


DATABASE_NAME = os.environ.get('DB_NAME', 'inf5190')


def get_db():
    return {
        "user": os.environ.get('DB_USER', 'root'),
        "password": os.environ.get('DB_PASSWORD', 'password'),
        "host": os.environ.get('DB_HOST', 'localhost'),
        "port": int(os.environ.get('DB_PORT', '5432')),
    }


class BaseModel(Model):
    class Meta:
        database = PostgresqlDatabase(DATABASE_NAME, **get_db())
