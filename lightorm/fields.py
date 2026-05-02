class Field:
    """
    Base field descriptor

    - Stores sql type and metadata
    - Uses __set_name__ to learn its attribute name
    - Stores values in instance.__dict__
    """

    def __init__(self, sql_type, primary_key=False):
        self.sql_type = sql_type
        self.primary_key = primary_key
        self.name = None


    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


class IntegerField(Field):
    def __init__(self, primary_key: bool = False):
        super().__init__(sql_type="INTEGER", primary_key= primary_key)

class StringField(Field):
    def __init__(self, primary_key: bool = False):
        super().__init__(sql_type="TEXT", primary_key=primary_key)





if __name__ == "__main__":
    class Dummy:
        id = IntegerField(primary_key=True)
        name = StringField()

    d = Dummy()
    d.id = 1
    d.name = "Umesh"

    print(d.id)
    print(d.name)

    print(Dummy.id.sql_type)
    print(Dummy.name.sql_type)