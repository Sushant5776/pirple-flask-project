import sqlite3

def check_passwd(username):
    connection = sqlite3.connect('main.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("""SELECT password FROM users WHERE username LIKE '{username}';""".format(username=username))
    passwd = cursor.fetchone()
    if passwd is None:
        connection.commit()
        cursor.close()
        connection.close()
        return passwd
    else:
        passwd = passwd[0]
        connection.commit()
        cursor.close()
        connection.close()
        return passwd

def check_users():
    connection = sqlite3.connect('main.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("""SELECT username FROM users ORDER BY id DESC;""")
    db_users = cursor.fetchall()
    users = []
    for i in range(len(db_users)):
        person = db_users[i][0]
        users.append(person)
    connection.commit()
    cursor.close()
    connection.close()
    return users

def signup(username, password):
    connection = sqlite3.connect('main.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("""SELECT password FROM users WHERE username LIKE '{username}';""".format(username=username))
    exist = cursor.fetchone()
    if exist is None:
        cursor.execute("""INSERT INTO users(username, password, reg_date) VALUES ('{username}', '{password}', datetime('now', 'localtime'));""".format(username=username, password=password))
        connection.commit()
        cursor.close()
        connection.close()
        message = 'You have successfully signed up!'
        return message
    else:
        error_message = 'User already exists!'
        return error_message


def createList(listname, created_by):
    connection = sqlite3.connect('main.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("""SELECT listname FROM lists WHERE listname LIKE '{listname}';""".format(listname=listname))
    exist = cursor.fetchone()
    if exist is None:
        cursor.execute(
            """INSERT INTO lists(listname, created_by, created_on) VALUES('{listname}', '{created_by}', datetime('now', 'localtime'));""".format(listname=listname, created_by=created_by)
        )
        success_message = 'Successfully created a list!'
        connection.commit()
        cursor.close()
        connection.close()
        return success_message
    else:
        connection.commit()
        cursor.close()
        connection.close()
        error_message = 'List already taken!'
        return error_message

def getList(username):
    connection = sqlite3.connect('main.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("""SELECT listname FROM lists WHERE created_by LIKE '{username}' ORDER BY created_on DESC;""".format(username=username))
    db_lists = cursor.fetchall()
    lists  = []
    for i in range(len(db_lists)):
        list_name = db_lists[i][0]
        lists.append(list_name)
    connection.commit()
    cursor.close()
    connection.close()
    if db_lists is None:
        pass
    else:
        return lists

def addItem(listname, itemname, username):
    connection = sqlite3.connect('main.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("""SELECT itemname FROM listitems WHERE itemname LIKE '{itemname}' AND created_for LIKE '{listname}' AND created_by LIKE '{username}';""".format(itemname=itemname, listname=listname, username=username))
    exist = cursor.fetchone()
    if exist is None:
        cursor.execute("""INSERT INTO listitems(itemname, complete, created_by, created_for, created_on) VALUES('{itemname}', 0, '{username}', '{listname}', datetime('now', 'localtime'));""".format(itemname=itemname, username=username, listname=listname))
        connection.commit()
        cursor.close()
        connection.close()
    else:
        connection.commit()
        cursor.close()
        connection.close()

def getItems(list_name):
    connection = sqlite3.connect('main.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("""SELECT itemname FROM listitems WHERE created_for LIKE '{list_name}';""".format(list_name=list_name))
    db_items = cursor.fetchall()
    items = []
    for i in range(len(db_items)):
        item = db_items[i][0]
        items.append(item)
    connection.commit()
    cursor.close()
    connection.close()
    if db_items is None:
        pass
    else:
        return items

def deleteList(listname, username):
    connection = sqlite3.connect('main.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM lists WHERE listname LIKE '{listname}' AND created_by LIKE '{username}';""".format(listname=listname, username=username))
    cursor.execute("""DELETE FROM listitems WHERE created_for LIKE '{listname}' AND created_by LIKE '{username}';""".format(listname=listname, username=username))
    connection.commit()
    cursor.close()
    connection.close()

def deleteItem(listname, itemname, username):
    connection = sqlite3.connect('main.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM listitems WHERE itemname LIKE '{itemname}' AND created_for LIKE '{listname}' AND created_by LIKE '{username}';""".format(itemname=itemname, listname=listname, username=username))
    connection.commit()
    cursor.close()
    connection.close()

def editList(old_list_name, new_list_name, username):
    connection = sqlite3.connect('main.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("""UPDATE lists SET listname = '{new_list_name}', created_on = datetime('now', 'localtime') WHERE listname LIKE '{old_list_name}' AND created_by LIKE '{username}';""".format(new_list_name=new_list_name, old_list_name=old_list_name, username=username))
    cursor.execute("""update listitems SET created_for = '{new_list_name}' WHERE created_for LIKE '{old_list_name}' AND created_by LIKE '{username}';""".format(new_list_name=new_list_name, old_list_name=old_list_name, username=username))
    connection.commit()
    cursor.close()
    connection.close()

def editItem(old_item_name, new_item_name, list_name, username):
    connection = sqlite3.connect('main.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("""UPDATE listitems SET itemname = '{new_item_name}', created_on = datetime('now', 'localtime') WHERE itemname LIKE '{old_item_name}' AND created_for LIKE '{list_name}' AND created_by LIKE '{username}';""".format(new_item_name=new_item_name, old_item_name=old_item_name, list_name=list_name, username=username))
    connection.commit()
    cursor.close()
    connection.close()
