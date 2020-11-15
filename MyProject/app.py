from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route('/register')
def register():
    if request.method == 'GET':
        return render_template('register.html')
    return render_template('register.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('index.html')


@app.route('/search', methods=['GEI', 'POST'])
def search():
    if request.method == 'POST':
        return render_template('/search.html')
    return render_template('search1.html')


if __name__ == '__main__':
    app.run(debug=True)
