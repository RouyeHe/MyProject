from flask_login import UserMixin
from main import db
from datetime import datetime
class U(db.Model,UserMixin):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True)
    n = db.Column(db.Text)
    s = db.Column(db.Text)
    p = db.Column(db.Text)
    a = db.Column(db.Text)
    b = db.Column(db.Float)
class Book(db.Model):
    __tablename__='product'
    id=db.Column(db.Integer,primary_key=True)
    n = db.Column(db.Text)
    s = db.Column(db.Integer)
    t = db.Column(db.Text)
    a = db.Column(db.Text)
    like=db.Column(db.Integer)
    g=db.Column(db.Float)
    g_n = db.Column(db.Integer)
    p=db.Column(db.Float)
    g_s=db.Column(db.Integer)
class Comment(db.Model):
    __tablename__='comment'
    id=db.Column(db.Integer,primary_key=True)
    c=db.Column(db.Text)
    bn = db.Column(db.Text)
    bid=db.Column(db.Integer)
    uid=db.Column(db.Integer)
    like=db.Column(db.Integer)
    un=db.Column(db.Text)
    t=db.Column(db.DateTime,default=datetime.now)
class Like(db.Model):
    __tablename__='like'
    id=db.Column(db.Integer,primary_key=True)
    uid=db.Column(db.Integer)
    bid=db.Column(db.Integer)
    bn=db.Column(db.Text)
    ba=db.Column(db.Text)
    t = db.Column(db.DateTime, default=datetime.now)
class Like_comment(db.Model):
    __tablename__='like_comment'
    id=db.Column(db.Integer,primary_key=True)
    uid=db.Column(db.Integer)
    cid=db.Column(db.Integer)
class Borrow(db.Model):
    __tablename__='borrow'
    id=db.Column(db.Integer,primary_key=True)
    uid=db.Column(db.Integer)
    bid=db.Column(db.Integer)
    bn = db.Column(db.Text)
    ba = db.Column(db.Text)
    t = db.Column(db.DateTime, default=datetime.now)
class Collect(db.Model):
    __tablename__='collect'
    id=db.Column(db.Integer,primary_key=True)
    uid=db.Column(db.Integer)
    bid=db.Column(db.Integer)
    bn = db.Column(db.Text)
    ba = db.Column(db.Text)
    t = db.Column(db.DateTime, default=datetime.now)
class Grade(db.Model):
    __tablename__ = 'grade'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    bid = db.Column(db.Integer)
    g = db.Column(db.Integer)
class Record(db.Model):
    __tablename__='record'
    id=db.Column(db.Integer,primary_key=True)
    uid=db.Column(db.Integer)
    bid=db.Column(db.Integer)
    bn = db.Column(db.Text)
    ba = db.Column(db.Text)
    t = db.Column(db.DateTime, default=datetime.now)




