from flask import Flask
from flask import escape, url_for
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

# 数据库配置


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path,'data.db')


db = SQLAlchemy(app)

# 创建数据库模型
class User(db.Model): # 表明将会是user(自动生成 小写处理)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))
    
# 自定义命令initdb
import click

@app.cli.command() # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop') # 设置选项
def initdb(drop):
    """initialize the database"""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('initialized database') # 输出提示信息
    
    
@app.cli.command()
def forge():
    """generate fake data"""
    db.create_all()
    
    name = "Fake"
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'],year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done')
    


    

# @app.route('/')
# @app.route('/home')
# @app.route('/index')
# def hello():
#     return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'

# @app.route('/user/<name>')
# def user_page(name):
#     return 'User:{}'.format(escape(name))

# @app.route('/test')
# def test_url_for():
#     print(url_for('hello'))
#     print(url_for('user_page',name='guanze'))
#     print(url_for('user_page',name='peter'))
#     print(url_for('test_url_for'))
#     print(url_for('test_url_for',num=2))
#     return 'TEST PAGE'

from flask import render_template


@app.route('/')
def index():
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('./index.html',user=user,movies=movies)