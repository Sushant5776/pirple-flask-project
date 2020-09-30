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

def get_Lists():
    connection = sqlite3.connect('main.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("""SELECT listname, created_by FROM lists ORDER BY id;""")
    db_lists = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return db_lists

def getList24():
    connection = sqlite3.connect('main.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("""SELECT listname, created_by FROM lists WHERE created_on > datetime('now', 'localtime', '-1 day') ORDER BY created_on DESC;""")
    db_lists = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return db_lists

def getUsers24():
    connection = sqlite3.connect('main.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("""SELECT username FROM users WHERE reg_date > datetime('now', 'localtime', '-1 day') ORDER BY reg_date DESC;""")
    db_users = cursor.fetchall()
    users = []
    for i in range(len(db_users)):
        user = db_users[i][0]
        users.append(user)
    connection.commit()
    cursor.close()
    connection.close()
    return users

def delete_user_admin(user_name):
    connection = sqlite3.connect('main.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM listitems WHERE created_by LIKE '{user_name}';""".format(user_name=user_name))
    cursor.execute("""DELETE FROM lists WHERE created_by LIKE '{user_name}';""".format(user_name=user_name))
    cursor.execute("""DELETE FROM users WHERE username LIKE '{user_name}';""".format(user_name=user_name))
    connection.commit()
    cursor.close()
    connection.close()
