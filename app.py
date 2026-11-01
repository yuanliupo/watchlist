from flask import Flask, render_template # 基础类和调用html的模板
from markupsafe import escape # html字符转义
from flask import url_for # 快捷生成url
from faker import Faker # 生成虚拟数据
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, select
from sqlalchemy.orm  import DeclarativeBase, Mapped, mapped_column
from pathlib import Path
import os
import sys # 获取当前程序的目录
import click # 自动创建数据库

SQLITE_PERFIX = 'sqlite:///' if sys.platform.startswith('win') else 'sqlite:////'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLITE_PERFIX + str(Path(app.root_path) / 'data.db').lstrip('/')

# 数据库类型
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(app, model_class = Base)

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key = True) # 主键
    name: Mapped[str] = mapped_column(String(20)) # 名字

class Movie(db.Model):
    __tablename__ = 'movie'
    id: Mapped[int] = mapped_column(primary_key = True)
    title: Mapped[str] = mapped_column(String(60))
    year: Mapped[str] = mapped_column(String(4))

# 自动创建命令
@app.cli.command('init-db') # 注册命令
@click.option('--drop', is_flag = True, help = 'Create after drop.')
def init_database(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
def forge():
    '''Generate fake data'''
    db.drop_all()
    db.create_all()
    fake = Faker()
    name = fake.name()
    movies = [{'title': ' '.join(fake.words(nb = 3, ext_word_list = None, unique = False)), 'year': fake.year()} for _ in range(20)]
    user = User(name = name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title = m['title'], year = m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done.')

@app.context_processor
def inject_user():
    user = db.session.execute(select(User)).scalar()
    return dict(user = user)

@app.route('/')
def index():
    movies = db.session.execute(select(Movie)).scalars().all()
    return render_template('index.html', movies = movies)

@app.route('/index')
@app.route('/home')
def hello():
    return "<h1>Hello visitor</h1>"

@app.route('/user/<name>')
def user_page(name):
    return f'User {escape(name)} page'

@app.route('/test')
def test_url_for():
    name = db.session.execute(select(User)).scalars().all()
    movies = db.session.execute(select(Movie)).scalars().all()
    print(url_for('hello'))
    print(url_for('user_page', name = 'greyli'))
    print(url_for('user_page', name = 'peter'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', num = 2)) 
    print(f"User name {name[0].name}")
    print(movies)
    print(type(movies))
    return 'Test page'

@app.errorhandler(404)
def page_not_found(error):
    
    return render_template('404.html'), 404