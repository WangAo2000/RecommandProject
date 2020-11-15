from flask import Flask, render_template, request, redirect
from users import Users

app = Flask(__name__)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    return '注册成功'


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/login',methods=['GET', 'POST'])
def login():
    pass


@app.route('/search', methods=['GEI', 'POST'])
def search():
    user1 = Users(1, '小明', '123456')
    username = request.form.get('username')
    print(username)
    password = request.form.get('password')
    if username == user1.username and password == user1.password:
        return render_template('search.html', user=user1)
    return render_template('index.html', msg='账号或密码不正确', username=username)


if __name__ == '__main__':
    app.run(debug=True)
