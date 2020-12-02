from flask import Flask, render_template, request, redirect, url_for, session, g
from util import Users, Database

app = Flask(__name__)
app.secret_key = 'this is a secret key'
vaild_path = ['/register_succeed', '/search', '/brief']


@app.before_request
def before_request():
    # 登录页面清除session
    if request.path == url_for('index'):
        session.clear()
    else:
        # 获取session中的用户
        username = session.get('username', None)
        if username:
            with Database(database='recommend') as cursor:
                # 查询session中的用户保存到g对象中
                sql = "select * from users where username='%s'" % username
                cursor.execute(sql)
                user = cursor.fetchone()
                user1 = Users(user[0], user[1])
                g.user = user1
                # 查询session中的用户的推荐影片保存到g对象中
                sql = "select movies.moviename,brief,type,path,image from movies " \
                      "join user_movie on movies.moviename=user_movie.moviename " \
                      "where username='%s' " \
                      "and type=" \
                      "(select type from movies " \
                      "join user_movie on movies.moviename=user_movie.moviename " \
                      "where username='%s' ORDER BY record LIMIT 1)limit 3;"\
                      % (g.user.username, g.user.username)
                cursor.execute(sql)
                movies = cursor.fetchall()
                g.movies = movies
        else:
            # 未登录时不能访问的路径，并重定向到登录页面
            if request.path in vaild_path:
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
            # 判断用户是否存在
            if not is_exist:
                if password == repassword and username != '' and len(password) >= 6:
                    # 插入用户数据
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
    return render_template('index.html', user='')


@app.route('/login', methods=['GET', 'POST'])
def login():
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
                    # 一致保存用户进session并查询推荐影片
                    session['username'] = username
                    session['password'] = password
                    # 查询用户的推荐影片
                    sql = "select movies.moviename,brief,type,path,image from movies " \
                          "join user_movie on movies.moviename=user_movie.moviename " \
                          "where username='%s' " \
                          "and type=" \
                          "(select type from movies " \
                          "join user_movie on movies.moviename=user_movie.moviename " \
                          "where username='%s' ORDER BY record LIMIT 1)limit 3;" \
                          % (g.user.username, g.user.username)
                    cursor.execute(sql)
                    movies = cursor.fetchall()
                    return render_template('search.html', user=user1, movies=movies)
                else:
                    return render_template('index.html', msg='账号或密码不正确', user='')
            else:
                return render_template('index.html', msg='账号或密码不正确', user='')
    return render_template('index.html', user='')


@app.route('/register_succeed', methods=['GET', 'POST'])
def register_succeed():
    return render_template('register_succeed.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        moviename = request.form.get('moviename')
        # 查找影片名或影片类型
        with Database('recommend') as cursor:
            sql = "select * from movies where moviename='%s' or type='%s'" % (moviename, moviename)
            cursor.execute(sql)
            movies = cursor.fetchall()
        return render_template('search.html', user=g.user, movies=movies)
    return render_template('search.html', user=g.user, movies=g.movies)


@app.route('/brief')
def movie_brief():
    username = request.args.get('username')
    moviename = request.args.get('moviename')
    # 查询该用户是否观看影片
    with Database(database='recommend') as cursor:
        sql = "select * from user_movie where username='%s'and moviename='%s'" % (username, moviename)
        cursor.execute(sql)
        like = cursor.fetchone()
        # 如果有点击量加1
        if like:
            sql = "update user_movie set record=record+1 where username='%s' and moviename='%s';" % (username, moviename)
            cursor.execute(sql)
        # 没有就将影片加入用户中
        else:
            sql = "INSERT into user_movie values('%s', '%s', 1);" % (username, moviename)
            cursor.execute(sql)
    # 返回点击的影片
    with Database(database='recommend') as cursor:
        sql = "select * from movies where moviename='%s'" % moviename
        cursor.execute(sql)
        movie = cursor.fetchone()
    return render_template('brief.html', user=g.user, movie=movie)


if __name__ == '__main__':
    app.run(debug=True)
