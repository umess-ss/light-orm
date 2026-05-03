from lightorm.model import Model
from lightorm.fields import IntegerField, StringField
from lightorm.db import connect

connect()

class User(Model):
    id = IntegerField(primary_key=True)
    name = StringField()
    age = IntegerField()

User.create_table()

u = User(name="umess", age=23)
u.save()

User.update(where={"name":"Umesh"}, age=30)
print(User.all())



# User.delete(where={"age":30})

print(User.all())