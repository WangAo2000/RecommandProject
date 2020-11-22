from flask import Flask, render_template, request, redirect, url_for, flash, session
from users import Users
import pymysql

app = Flask(__name__)
app.secret_key = 'this is a secret key'
# 链接数据库
conn = pymysql.connect(host='localhost', user='root', password='000000', database='recommend',charset='utf8')
cursor = conn.cursor()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        sql = "select * from users where username='%s'" % username
        cursor.execute(sql)
        is_exist = cursor.fetchone()
        # 判断数据是否存在
        if not is_exist:
            if password == repassword and username != '' and len(password) >= 6:
                # 插入数据
                sql = "insert into users values ('%s', '%s')" % (username, password)
                try:
                    cursor.execute(sql)
                    conn.commit()
                except:
                    conn.rollback()

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
        # 查询数据
        sql = "select * from users where username='%s'" % username
        cursor.execute(sql)
        user = cursor.fetchone()
        if user:
            user1 = Users(user[0], user[1])
            # 判断用户与密码是否一致
            if username == user1.username and password == user1.password:
                session[username] = password
                return render_template('search.html', user=user1)
        else:
            return render_template('index.html', msg='账号或密码不正确')
    if request.method == 'GET':
        username = request.args.get(username)
        if username:
            session.pop(username)
    return render_template('index.html')


@app.route('/register_succeed', methods=['GET', 'POST'])
def register_succeed():
    return render_template('register_succeed.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        username = request.form.get('username')
        user_id = request.form.get('user_id')
        return render_template('search.html', username=username)
    return render_template('search.html', user='')


if __name__ == '__main__':
    app.run(debug=True)
    cursor.close()
    conn.close()