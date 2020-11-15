from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/search', methods=['GEI', 'POST'])
def search():
    return render_template('search1.html')


if __name__ == '__main__':
    app.run(debug=True)
