import sqlite3

_connection = None


# a global sqlite connection
def connect(path="lightorm.db"):
    global _connection
    _connection = sqlite3.connect(path)
    return _connection


# a helper to execute sql
def execute(sql):
    cursor = _connection.cursor()
    cursor.execute(sql)
    _connection.commit()
    return cursor

# a helper to fetch rows

def fetch(sql):
    cursor = execute(sql)
    return cursor.fetchall()