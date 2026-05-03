from .metaclass import ModelMeta
from .db import execute, fetch

class Model(metaclass=ModelMeta):
    """
    Base ORM model:
    - Handles instance initialization
    - Generates SQL for save(), filter(), all()
    """

    def __init__(self, **kwargs):
        #set values for each field
        for field_name in self.__fields__:
            setattr(self, field_name, kwargs.get(field_name))


    def save(self):
        """
        Generates an INSERT SQL statement.
        """
        fields = []
        values = []

        for name in self.__fields__:
            value = getattr(self, name)
            if value is not None:
                fields.append(name)
                values.append(repr(value))   #repr() adds quotes for string

        sql = (
            f"INSERT INTO {self.__table__}"
            f"({', '.join(fields)}) VALUES ({', '.join(values)});"
        )

        execute(sql)
        return sql

    @classmethod
    def filter(cls, **kwargs):
        """
        Generate a SELECT .... WHERE ... SQL statements.
        """
        conditions = [f"{k} = {repr(v)}" for k,v in kwargs.items()]
        where_clause = " AND ".join(conditions)

        sql = f"SELECT * FROM {cls.__table__} WHERE {where_clause};"
        
        rows = fetch(sql)
        return rows
    
    @classmethod
    def all(cls):
        """
        Generate a SELECT * SQL statement.
        """

        sql = f"SELECT * FROM {cls.__table__};"
        fetch(sql)
        return sql
    
    
    
    