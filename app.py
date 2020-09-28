from flask import Flask, render_template, request, redirect, url_for, session, g
import model, admin_model

app = Flask(__name__)
app.secret_key = 'keepitsecret'

admin_username = ''
username = ''
user = model.check_users()

@app.before_request
def before_request():
    g.username = None
    g.admin_username = None
    if 'username' in session:
        g.username = session['username']
    if 'admin_username' in session:
        g.admin_username = session['admin_username']

@app.route('/', methods=['GET'])
def index():
    if 'username' in session:
        g.user=session['username']
        return render_template('dashboard.html')
    return render_template('index.html')

@app.route('/termsOfUse', methods=['GET'])
def termsOfUse():
    return render_template('termsOfUse.html')

@app.route('/privacy', methods=['GET'])
def privacy():
    return render_template('privacy.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            password = password.replace("'", "''")
            if "'" in username or '"' in username:
                error_message = 'Username is not allowed! Try yourname123, something_me, etc.'
                return render_template('signup.html', message=error_message)
            else:
                message = model.signup(username, password)
                return render_template('signup.html', message=message)
        else:
            return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('username', None)
        username = request.form['username']
        password_form = request.form['password']
        username = username.replace("'", "''")
        password_form = password_form.replace("'", "''")
        password = model.check_passwd(username)
        if password_form == password:
            session['username'] = request.form['username']
            return redirect(url_for('dashboard'))
        else:
            error_message = 'Oops, Login Failed!'
            return render_template('login.html', message=error_message)
    else:
        return render_template('login.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'username' in session:
        username = session['username']
        lists = model.getList(username)
        return render_template('dashboard.html', username=username, lists=lists)
    else:
        return redirect(url_for('login'))

@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username', None)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('dashboard'))

@app.route('/logout/admin', methods=['GET'])
def admin_logout():
    if 'admin_username' in session:
        session.pop('admin_username', None)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('admin_login'))

@app.route('/createList', methods=['GET', 'POST'])
def createList():
    if 'username' in session:
        if request.method == 'POST':
            list_name = request.form['list_name']
            list_name = list_name.replace("'", "''")
            username = session['username']
            message = model.createList(list_name, username)
            return render_template('createList.html', message=message)
        else:
            return render_template('createList.html')
    else:
        return redirect(url_for('login'))

@app.route('/list/<string:list_name>', methods=['GET', 'POST'])
def list_(list_name):
    if 'username' in session:
        list_name_for_database = list_name.replace("'", "''")
        items = model.getItems(list_name_for_database)
        if request.method == 'POST':
            created_by = session['username']
            created_for = list_name_for_database
            itemname = request.form['itemname']
            itemname = itemname.replace("'", "''")
            model.addItem(created_for, itemname, created_by)
            return redirect('/list/{list_name}'.format(list_name=list_name))
        else:
            return render_template('list.html', list_name=list_name, items=items)
    else:
        return redirect(url_for('login'))

@app.route('/list/delete/<string:list_name>', methods=['GET'])
def deleteList(list_name):
    if 'username' in session:
        username = session['username']
        list_name_for_database = list_name.replace("'", "''")
        model.deleteList(list_name_for_database, username)
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route('/list/delete/<string:list_name>/<string:item_name>', methods=['GET'])
def deleteItem(list_name, item_name):
    username = session['username']
    list_name_for_database = list_name.replace("'", "''")
    item_name_for_database = item_name.replace("'", "''")
    model.deleteItem(list_name_for_database, item_name_for_database, username)
    return redirect('/list/{list_name}'.format(list_name=list_name))

@app.route('/list/edit/<string:list_name>', methods=['GET', 'POST'])
def editList(list_name):
    list_name_for_database = list_name.replace("'", "''")
    if request.method == 'POST':
        username = session['username']
        new_list_name = request.form['new_list_name']
        new_list_name_for_database = new_list_name.replace("'", "''")
        model.editList(list_name_for_database, new_list_name_for_database, username)
        return redirect(url_for('dashboard'))
    else:
        return render_template('editList.html', list_name=list_name)

@app.route('/list/edit/<string:list_name>/<string:item_name>', methods=['GET', 'POST'])
def editItem(list_name, item_name):
    if request.method == 'POST':
        username = session['username']
        new_item_name = request.form['new_item_name']
        list_name_for_database = list_name.replace("'", "''")
        new_item_name = new_item_name.replace("'", "''")
        item_name = item_name.replace("'", "''")
        model.editItem(item_name, new_item_name, list_name_for_database, username)
        return redirect('/list/{list_name}'.format(list_name=list_name))
    return render_template('editItem.html', list_name=list_name, item_name=item_name)

@app.route('/login/admin', methods=['GET', 'POST'])
def admin_login():
    if 'admin_username' in session:
        return redirect(url_for('admin_dashboard'))
    else:
        if request.method == 'POST':
            username = request.form['username']
            password_form = request.form['password']
            username = username.replace("'", "''")
            password_form = password_form.replace("'", "''")
            session.pop('admin_username', None)
            password = admin_model.check_passwd(username)
            if password_form == password:
                session['admin_username'] = request.form['username']
                return redirect(url_for('admin_dashboard'))
            else:
                return render_template('admin_login.html', message='Login Failed!')
        else:
            return render_template('admin_login.html')

@app.route('/dashboard/admin', methods=['GET'])
def admin_dashboard():
    if 'admin_username' in session:
        username = session['admin_username']
        return render_template('admin_dashboard.html', username=username)
    else:
        return redirect(url_for('admin_login'))

@app.route('/dashboard/admin/all_users', methods=['GET', 'POST'])
def all_users():
    if 'admin_username' in session:
        users = admin_model.get_Users()
        return render_template('admin_all_users.html', users=users)
    else:
        return redirect(url_for('admin_dashboard'))

@app.route('/dashboard/admin/all_lists', methods=['GET'])
def all_lists():
    if 'admin_username' in session:
        lists = admin_model.get_Lists()
        return render_template('admin_all_lists.html', lists=lists)
    else:
        return redirect(url_for('admin_login'))

@app.route('/dashboard/admin/lists_in_one_day', methods=['GET'])
def lists_in_one_day():
    if 'admin_username' in session:
        lists = admin_model.getList24()
        if not lists:
            message = 'No list created in last 1 day!'
            return render_template('admin_lists_one_day.html', message=lists)
        else:
            return render_template('admin_lists_one_day.html', lists=lists)
    else:
        return redirect(url_for('admin_login'))

@app.route('/dashboard/admin/users_in_one_day', methods=['GET'])
def users_in_one_day():
    if 'admin_username' in session:
        users = admin_model.getUsers24()
        if not users:
            message = 'No user registered in last 1 day!'
            return render_template('admin_users_one_day.html', message=message)
        else:
            return render_template('admin_users_one_day.html', users=users)

@app.route('/dashboard/admin/<string:from_type>/<string:user_name>', methods=['GET'])
def delete_user_admin(from_type, user_name):
    if 'admin_username' in session:
        admin_model.delete_user_admin(user_name)
        return redirect('/dashboard/admin/{from_type}'.format(from_type=from_type))
    else:
        return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)
