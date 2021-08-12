from peewee import *
from os import path
database_path = path.dirname(path.realpath(__file__))
db = SqliteDatabase(path.join(database_path, "MyDatabase.db"))

class Users(Model):
    name = CharField()
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db
Users.create_table(fail_silently=True)

class Products(Model):
    name = CharField()
    quantity = IntegerField()
    price = FloatField()

    class Meta:
        database = db
Products.create_table(fail_silently=True)
