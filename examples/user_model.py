from lightorm.model import Model
from lightorm.fields import IntegerField, StringField
from lightorm.db import connect

connect()

class User(Model):
    id = IntegerField(primary_key=True)
    name = StringField()
    age = IntegerField()

User.create_table()

u = User(name="Pra Ti Vaaa", age=22)
u.save()


print(User.all())