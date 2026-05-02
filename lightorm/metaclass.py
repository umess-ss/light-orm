from .fields import Field


class ModelMeta(type):
    """
    Metaclass that:
    - Collects all Field descriptors for the class
    - Removes them from the class namespace
    - Stores them in __fields__
    - Defines __table__ automatically
    """

    def __new__(cls, name, bases, attrs):
        #skip base model class
        if name == "Model":
            return super().__new__(cls, name, bases, attrs)
        
        fields = {}

        #collect field instances
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                fields[key] = value
                attrs.pop(key)


        #attach metadata
        attrs["__fields__"] = fields
        attrs["__table__"] = name.lower()

        return super().__new__(cls,name, bases, attrs)

