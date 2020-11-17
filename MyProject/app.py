from flask import Flask, render_template, request, redirect, url_for, flash
from users import Users

app = Flask(__name__)
app.secret_key = 'this is a secret key'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('usename')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        msg = '密码或账号不正确'
        if password == repassword and username != '' and len(password) >= 6:
            return redirect('/register_succeed')
        else:
            return render_template('register.html', msg=msg)
    return render_template('register.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user1 = Users(1, '小明', '123456')
        username = request.form.get('username')
        password = request.form.get('password')
        if username == user1.username and password == user1.password:
            return render_template('search.html', username=user1.username)
        else:
            return render_template('index.html', msg='账号或密码不正确')
    return render_template('index.html')


@app.route('/register_succeed', methods=['GET', 'POST'])
def register_succeed():
    username = request.form.get('usename')
    password = request.form.get('password')
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
