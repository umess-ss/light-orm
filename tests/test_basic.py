from lightorm.metaclass import ModelMeta
from lightorm.fields import IntegerField, StringField

class Model(metaclass=ModelMeta):
    pass

class User(Model):
    id = IntegerField(primary_key=True)
    name = StringField()

print(User.__fields__)
print(User.__table__)