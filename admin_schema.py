import sqlite3

connection = sqlite3.connect('main.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute(
    """CREATE TABLE admin(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(32) UNIQUE,
        password VARCHAR(64),
        reg_date VARCHAR(32)
    );"""
)

connection.commit()
cursor.close()
connection.close()