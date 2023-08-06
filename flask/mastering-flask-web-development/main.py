from ast import Return
from email.policy import default
from xmlrpc.client import TRANSPORT_ERROR
from flask import Flask
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime


app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)
migrate = Migrate(app,db)


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255),nullable=False,unique=True,index=True)
    password = db.Column(db.String(255))
    posts = db.relationship(
    'Post',
    backref='user',
    lazy='dynamic'
)

    def __init__(self,username):
        self.username = username
    
    def __repr__(self):
        return f'User {self.username}'


tags = db.Table('post_tags',
    db.Column('post_id',db.Integer,db.ForeignKey('post.id')),
    db.Column('tag_id',db.Integer,db.ForeignKey('tag.id')))


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255),nullable=False)
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime(),default=datetime.datetime.now())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    comments = db.relationship(
        'Comment',
        backref='post',
        lazy='dynamic'
    )

    def __init__(self, title):
        self.title = title
    def __repr__(self):
        return "<Post '{}'>".format(self.title)


class Comment(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(255),nullable=False)
    text = db.Column(db.Text())
    date = db.Column(db.DateTime(),default=datetime.datetime.now())
    post_id = db.Column(db.Integer(),db.ForeignKey('post.id'))

    def __repr__(self):
        return f'Comment {self.name}'


class Tag(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    title = db.Column(db.String(255),nullable=False,unique=True)
    
    def __init__(self,title):
        self.title = title
    
    def __repr__(self) -> str:
        return f'Tag {self.title}'





@app.route('/')
def home():
    return '<h1>Hello World</h1>'

if __name__ == '__main__':
    app.run()