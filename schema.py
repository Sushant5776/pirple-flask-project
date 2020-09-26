import sqlite3

connection = sqlite3.connect('main.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute(
    """CREATE TABLE users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(32) UNIQUE,
        password VARCHAR(64),
        reg_date VARCHAR(32)
    );"""
)

cursor.execute(
    """CREATE TABLE lists(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        listname VARCHAR(32) UNIQUE,
        created_by VARCHAR(32),
        created_on VARCHAR(32)
    );"""
)

cursor.execute(
    """CREATE TABLE listitems(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        itemname VARCHAR(32),
        complete INTEGER,
        created_by VARCHAR(32),
        created_for VARCHAR(32),
        created_on VARCHAR(32)
    );"""
)
