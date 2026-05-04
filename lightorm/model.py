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


    @classmethod
    def create_table(cls):
        columns = []

        for name, field in cls.__fields__.items():
            col = f"{name} {field.sql_type}"
            if field.primary_key:
                col+=" PRIMARY KEY"
            columns.append(col)
        
        sql = f"CREATE TABLE IF NOT EXISTS {cls.__table__} ({', '.join(columns)});"
        execute(sql)
        return sql

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


    
    
    
    def update(self, **kwargs):
        sets = [f"{k} = {repr(v)}" for k, v in kwargs.items()]
        set_clause = ", ".join(sets)

        # find primary key
        pk_name = None
        for name, field in self.__fields__.items():
            if field.primary_key:
                pk_name = name
                break

        if pk_name is None:
            raise ValueError("No primary key defined for update()")
        
        pk_value = getattr(self, pk_name)

        sql = (
            f"UPDATE {self.__table__} "
            f"SET {set_clause} "
            f"WHERE {pk_name} = {repr(pk_value)}"
        )

        execute(sql)

        # update the object in memory
        for k, v in kwargs.items():
            setattr(self, k, v)

        return sql


    def delete(self):
        pk_name = None
        for name, field in self.__fields__.items():
            if field.primary_key:
                pk_name = name

        if pk_name is None:
            raise ValueError("No primary key defined for delete()")
        
        pk_value = getattr(self, pk_name)

        sql = (
            f"DELETE FROM {self.__table__} "
            f"WHERE {pk_name} = {repr(pk_value)};"
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
        
        rows = execute(sql)
        return [cls.from_row(row) for row in rows]
    
    @classmethod
    def all(cls):
        """
        Generate a SELECT * SQL statement.
        """

        sql = f"SELECT * FROM {cls.__table__};"
        rows = execute(sql)
        return [cls.from_row(row) for row in rows]
    
    @classmethod
    def update(cls, where: dict, **kwargs):
        sets = [f"{k} = {repr(v)}" for k, v in kwargs.items()]
        set_clause = ", ".join(sets)

        conditions = [f"{k} = {repr(v)}" for k, v in where.items()]
        where_clause = " AND ".join(conditions)

        sql = (
            f"UPDATE {cls.__table__} "
            f"SET {set_clause} "
            f"WHERE {where_clause} "
        )

        execute(sql)
        return sql
    
    @classmethod
    def update_all(cls, **kwargs):
        sets = [f"{k} = {repr(v)}" for k, v in kwargs.items()]
        set_clause = ", ".join(sets)

        sql = (
            f"UPDATE {cls.__table__} "
            f"SET {set_clause};"
        )

        execute(sql)
        return sql
    

    @classmethod
    def delete(cls, where: dict):
        conditions = [f"{k} = {repr(v)}" for k, v in where.items()]
        where_clause = " AND ".join(conditions)

        sql = f"DELETE FROM {cls.__table__} WHERE {where_clause}"
        execute(sql)
        return sql
    
    @classmethod
    def delete_all(cls):
        sql = f"DELETE FROM {cls.__table__};"
        execute(sql)
        return sql


    # a method to convert a db row to model instance i.e tuple to user instance
    @classmethod
    def from_row(cls, row):
        if row is None:
            return None
        
        obj = cls()
        for (col, _type), value in zip(cls.__fields__.items(),row):
            setattr(obj, col, value)
        return obj
        

    