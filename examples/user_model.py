from lightorm.model import Model
from lightorm.fields import IntegerField, StringField
from lightorm.db import connect

connect()

class User(Model):
    id = IntegerField(primary_key=True)
    name = StringField()
    age = IntegerField()

# User.create_table()

# u = User(name="umess", age=23)
# u.save()

# User.update(where={"name":"Umesh"}, age=30)
# print(User.all())

# users = User.all()
# for u in users:
#     print(u.name, u.age)


# User.delete(where={"age":30})

# User.update_all(age=22)
# print(User.all())

u = User(name="Umesh", age=25)
u.save()

u = User.get(id=5)
if u is None:
    print("user not found")
else:
    print(u.name)

