from flask import Flask, render_template, request, redirect, url_for, session, g
from users import Users
from connect_database import Database

app = Flask(__name__)
app.secret_key = 'this is a secret key'


@app.before_request
def before_request():
    if request.path == url_for('index'):
        session.clear()
    else:
        username = session.get('username', None)
        if username:
            with Database(database='recommend') as cursor:
                sql = "select * from users where username='%s'" % username
                cursor.execute(sql)
                user = cursor.fetchone()
                user1 = Users(user[0], user[1])
                g.user = user1
            return render_template('search.html', user=g.user)
        else:
            if request.path == url_for('search') or request.path == url_for('register_succeed'):
                return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        with Database(database='recommend') as cursor:
            sql = "select * from users where username='%s'" % username
            cursor.execute(sql)
            is_exist = cursor.fetchone()
            # 判断数据是否存在
            if not is_exist:
                if password == repassword and username != '' and len(password) >= 6:
                    # 插入数据
                    sql = "insert into users values ('%s', '%s')" % (username, password)
                    cursor.execute(sql)
                    return redirect('/register_succeed')
                else:
                    msg = '密码或账号不正确'
                    return render_template('register.html', msg=msg)
            else:
                msg = '用户已存在'
                return render_template('register.html', msg=msg)
    return render_template('register.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        with Database(database='recommend') as cursor:
            # 查询数据
            sql = "select * from users where username='%s'" % username
            cursor.execute(sql)
            user = cursor.fetchone()
            if user:
                user1 = Users(user[0], user[1])
                # 判断用户与密码是否一致
                if username == user1.username and password == user1.password:
                    session['username'] = username
                    session['password'] = password
                    # 查找影片
                    sql = 'select * from movies;'
                    cursor.execute(sql)
                    movies = cursor.fetchall()
                    return render_template('search.html', user=user1, movies=movies)
            else:
                return render_template('index.html', msg='账号或密码不正确')
    return render_template('index.html', user='')


@app.route('/register_succeed', methods=['GET', 'POST'])
def register_succeed():
    return render_template('register_succeed.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        username = request.form.get('username')
        user_id = request.form.get('user_id')
        return render_template('search.html', username=username)
    return render_template('search.html', user=g.user)


if __name__ == '__main__':
    app.run(debug=True)