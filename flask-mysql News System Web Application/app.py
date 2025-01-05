from flask import session,g,Flask,redirect,render_template,url_for,request,flash,blueprints
from models import User_db,User,Admin,QuestionModel,Comment,Like,Like_comment,Collect,Browsing
from exts import db
from forms import LoginForm,LoginForm1,QuestionForm,Search,Addcomment,Change_password,Change_information,Register,C,Q,S,S1,Q1,C1
from flask_login import current_user,LoginManager,login_user,login_required,logout_user
from blueprints.classes import aaa
from blueprints.page import bbb
from blueprints.manage import ccc
from blueprints.myself import ddd
from blueprints.release_news import eee
from datetime import datetime
app=Flask(__name__)
app.config['SECRET_KEY']='GNAISHDNAC'
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:123456@127.0.0.1:3306/question"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db.init_app(app)
login = LoginManager(app)
login.init_app(app)
login.login_view = 'login'
app.register_blueprint(aaa)
app.register_blueprint(bbb)
app.register_blueprint(ccc)
app.register_blueprint(ddd)
app.register_blueprint(eee)
@login.user_loader
def load_user(user_id):
    return User_db.query.get(int(user_id))
def get_user(user_name):
    users = User_db.query.filter(User_db.Studentname==user_name).first()
    if users:
        return users
    return None
@app.route('/login/', methods=('POST', 'GET'))
def login():
    form = LoginForm()
    if request.method=='POST':
        id = form.id.data
        password = form.password.data
        user2= User_db.query.filter(User_db.id == id).first()
        if user2:
            if int(password) == user2.password:
                name=user2.Studentname
                user_info = get_user(name)
                user = User(user_info)
                login_user(user)
                flash("登录成功！")
                return redirect(url_for('ddd.index'))
        flash("登陆失败！")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("用户已登出！")
    return redirect(url_for('login'))
@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html',Studentname=current_user.Studentname)
@app.route('/info')
@login_required
def info():
    b=0
    result=User_db.query.filter().all()
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    comments=Comment.query.order_by(Comment.creat_time.desc()).all()
    for a in result:
        b+=1
    return render_template('info.html',result=result,b=b,questions=questions,comments=comments)


@app.route('/search1',methods=('GET','POST'))
def search1():
    form=Search()
    if request.method=='POST':
        title=form.title.data
        content=form.content.data
        result = QuestionModel.query.filter(
                                  QuestionModel.title.contains(title),
                                  QuestionModel.content.contains(content)).all()
        if result==[]:
            return redirect('/search1_fail')
    else:
        result=QuestionModel.query.all()
    return render_template('search1.html',form=form,questions=result)
@app.route('/search1_fail')
def search1_fail():
    form=Search()
    return render_template('search1_fail.html',form=form)
@app.route('/detail',methods=('GET','POST'))
def detail():
    form=Addcomment()
    id = request.args.get('id')
    comments = Comment.query.filter(Comment.question_id == id).all()
    question=QuestionModel.query.get(id)
    title=question.title
    browsing=Browsing(q_id=id,q_title=title,user_id=current_user.id,q_contant=question.content)
    db.session.add(browsing)
    db.session.commit()
    like_number=question.like
    b = 0
    for c in comments:
        b+=1
    if request.method=='POST':
        comment=form.comment.data
        new_comment = Comment(comment=comment,author_id=current_user.id,question_id=id,like=0)
        db.session.add(new_comment)
        db.session.commit()
        print(id)
        return redirect('detail?id=%d'%int(id))
    like=Like.query.filter(Like.user_id==current_user.id).all()
    k=True
    for i in like:
        if int(i.question_id)==int(id):
            k=False
    collect=Collect.query.filter(Collect.user_id==current_user.id).all()
    l=True
    for i in collect:
        if int(i.q_id)==int(id):
            l=False
    like_comments=Like_comment.query.filter(Like_comment.user_id==current_user.id).all()
    c=[]
    for i in like_comments:
        a=i.comment_id
        c.append(a)
    return render_template('detail.html',c=c,comments=comments,question=question,b=b,form=form,like_number=like_number,k=k,l=l,like_comments=like_comments,id=current_user.id)

@app.route('/register',methods=('POST','GET'))
def register():
    form=Register()
    if request.method=='POST':
        name=form.Studentname.data
        age=form.Studentage.data
        sex=form.Studentsex.data
        number=form.number.data
        password=form.password.data
        a=User_db.query.filter(User_db.number==number).first()
        print(a)
        if a == None:
            new= User_db(Studentname=name, Studentage=age, Studentsex=sex, number=number,id=number,password=password)
            db.session.add(new)
            db.session.commit()
            flash('注册成功')
            return redirect('/login')
        else:
            flash('该学号已存在')
    return render_template('register.html',form=form)
@app.route('/like')
def like():
    q_id=request.args.get('id')
    like1 = Like.query.filter(Like.question_id == q_id).all()
    k = True
    for a in like1:
        if a.user_id == current_user.id:
            k = False
            db.session.delete(a)
            db.session.commit()
            question = QuestionModel.query.filter(QuestionModel.id == q_id).first()
            question.like = question.like - 1
            db.session.commit()
    if k:
        question = QuestionModel.query.filter(QuestionModel.id == q_id).first()
        like = Like(question_id=q_id, user_id=current_user.id, q_title=question.title)
        db.session.add(like)
        db.session.commit()
        question.like = question.like + 1
        db.session.commit()
    return redirect('detail?id=%d' % int(q_id))
@app.route('/like_comment')
def like_comment():
    comment_id = request.args.get('id')
    question_id=request.args.get('id1')
    like_comments=Like_comment.query.filter(Like_comment.comment_id==comment_id).all()
    k=True
    if not like_comments:
        like_comment= Like_comment(user_id=current_user.id, comment_id=comment_id)
        db.session.add(like_comment)
        db.session.commit()
        comment=Comment.query.filter(Comment.id==comment_id).first()
        comment.like=comment.like+1
        db.session.commit()
    else:
        for a in like_comments:
            if a.user_id==current_user.id:
                k = False
                db.session.delete(a)
                db.session.commit()
                comment = Comment.query.filter(Comment.id == comment_id).first()
                comment.like=comment.like-1
                db.session.commit()
        if k:
            like_comment=Like_comment(comment_id=comment_id,user_id=current_user.id)
            db.session.add(like_comment)
            db.session.commit()
            comment = Comment.query.filter(Comment.id == comment_id).first()
            comment.like =comment.like+ 1
            db.session.commit()
    print(question_id)
    return redirect('detail?id=%d'%int(question_id))
@app.route('/collect')
def collect():
    q_id=request.args.get('id')
    collect = Collect.query.filter(Collect.q_id == q_id).all()
    k = True
    for a in collect:
        if a.user_id == current_user.id:
            k = False
            db.session.delete(a)
            db.session.commit()
    if k:
        q_id = request.args.get('id')
        question=QuestionModel.query.get(q_id)
        collect = Collect(q_id=q_id, user_id=current_user.id, q_title=question.title)
        db.session.add(collect)
        db.session.commit()
    return redirect('detail?id=%d' % int(q_id))

if __name__ == "__main__":
    app.run(debug=True)