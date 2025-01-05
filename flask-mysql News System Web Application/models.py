from exts import db
from flask_login import UserMixin
from datetime import datetime
class User_db(db.Model,UserMixin):
    __tablename__ = 'uu'
    Studentname=db.Column(db.Text)
    Studentage=db.Column(db.Integer)
    Studentsex=db.Column(db.Text)
    password=db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)
    number=db.Column(db.Integer)
class Admin(db.Model,UserMixin):
    __tablename__ = 'info'
    id = db.Column(db.Text, primary_key=True)
    username=db.Column(db.Text)
    number=db.Column(db.Integer)
class User(UserMixin):
    def __init__(self, user):
        self.Studentname = user.Studentname
        self.id = user.id
    def get(user_id):
        if not user_id:
            return None
        if User_db.query.filter(User_db.id==user_id).first():
            return User(User_db.query.filter(User_db.id==user_id).first())
        return None
class QuestionModel(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('uu.id'))
    class1=db.Column(db.Text)
    class2=db.Column(db.Text)
    like=db.Column(db.Text)
    author = db.relationship(User_db, backref="questions")
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('uu.id'))
    creat_time=db.Column(db.DateTime, default=datetime.now)
    like = db.Column(db.Text)
    question = db.relationship(QuestionModel, backref=db.backref('comments'))
    author = db.relationship(User_db, backref='answers')
class Like(db.Model):
    __tablename__ = "like"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id=db.Column(db.Integer)
    question_id=db.Column(db.Integer)
    q_title=db.Column(db.Text)
class Like_comment(db.Model):
    __tablename__ = "like_comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    comment_id = db.Column(db.Integer)
class Collect(db.Model):
    __tablename__ = "collect"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    q_id = db.Column(db.Integer)
    q_title = db.Column(db.Text)
    time=db.Column(db.DateTime, default=datetime.now)
class Browsing(db.Model):
    __tablename__ = "browsing"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    q_id = db.Column(db.Integer)
    q_title = db.Column(db.Text)
    time = db.Column(db.DateTime, default=datetime.now)
    q_contant=db.Column(db.Text)

