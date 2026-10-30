from flask import Flask
from markupsafe import escape
from flask import url_for

app = Flask(__name__)
@app.route('/')
@app.route('/index')
@app.route('/home')
def hello():
    return "<h1>Hello visitor</h1><img src = '127.0.0.1:5000/25年中秋.png'>"

@app.route('/user/<name>')
def user_page(name):
    return f'User {escape(name)} page'

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name = 'greyli'))
    print(url_for('user_page', name = 'peter'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', num = 2))
    return 'Test page'