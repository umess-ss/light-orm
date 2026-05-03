from lightorm.model import Model
from lightorm.fields import IntegerField, StringField

class User(Model):
    id = IntegerField(primary_key=True)
    name = StringField()
    age = IntegerField()

u = User(name="Umesh", age=25)
u.save()


User.filter(age=25)
User.all()