import sqlite3

def check_passwd(username):
    connection = sqlite3.connect('main.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("""SELECT password FROM admin WHERE username LIKE '{username}';""".format(username=username))
    password = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    return password

def get_Users():
    connection = sqlite3.connect('main.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("""SELECT username FROM users ORDER BY id;""")
    db_users = cursor.fetchall()
    users = []
    for i in range(len(db_users)):
        user = db_users[i][0]
        users.append(user)
    connection.commit()
    cursor.close()
    connection.close()
    return users