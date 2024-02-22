#!/usr/bin/python3
"""Hello flask"""
from flask import Flask


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello():
    """Prints Hello HBNB!"""
    return "Hello HBNB!"


@app.route('/hbnb')
def hbnb():
    """Prints HBNB"""
    return "HBNB"


@app.route('/c/<text>')
def cisfun(text):
    """C is fun"""
    return 'C ' + text.replace("_", " ")


@app.route('/python/', defaults={'text': 'is cool'})
@app.route('/python/<text>')
def python_is_fun(text='is_cool'):
    """Python is cool"""
    return 'Python ' + text.replace("_", " ")


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
