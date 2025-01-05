from flask import render_template,Blueprint,request,redirect,Flask,flash,url_for
from flask_login import current_user,LoginManager,login_user,login_required,logout_user
from models import User_db,User,Admin,QuestionModel,Comment,Collect,Like,Browsing,Like_comment
from exts import db
from forms import LoginForm,LoginForm1,QuestionForm,Search,Addcomment,Change_password,Change_information,Register,C,Q,S,S1,Q1,C1
ddd=Blueprint('ddd',__name__)


def get_user(user_name):
    users = User_db.query.filter(User_db.Studentname==user_name).first()
    if users:
        return users
    return None

@ddd.route('/index')
@login_required
def index():
    return render_template('index.html',Studentname=current_user.Studentname,
                           sex=current_user.Studentsex,
                           id=current_user.id,
                           age=current_user.Studentage,
                           number=current_user.number)

@ddd.route('/index_hobby')
@login_required
def index_hobby():
    return render_template('index_hobby.html',Studentname=current_user.Studentname,
                           sex=current_user.Studentsex,
                           id=current_user.id,
                           age=current_user.Studentage,
                           number=current_user.number)
@ddd.route('/index_todo')
@login_required
def index_todo():
    return render_template('index_todo.html')

@ddd.route('/change_password',methods=('POST','GET'))
@login_required
def change_password():
    form=Change_password()
    if request.method=='POST':
        old_p=form.old_p.data
        new_p=form.new_p.data
        new_pp=form.new_pp.data
        old=current_user.password
        if int(old)==int(old_p):
            if int(new_p)==int(new_pp):
                id=current_user.id
                a = User_db.query.get(id)
                b=User_db(Studentname=a.Studentname, Studentage=a.Studentage, Studentsex=a.Studentsex, number=a.number, id=id,password=new_p)
                db.session.delete(a)
                db.session.commit()
                db.session.add(b)
                db.session.commit()
                flash('修改密码成功')
            else:
                flash('两次新密码不一致')
        else:
            flash('原密码错误')
    return render_template('change_password.html',form=form)
@ddd.route('/change_information',methods=('POST','GET'))
@login_required
def change_information():
    form=Change_information()
    if request.method=='POST':
        a=current_user.id
        b=User_db.query.filter(User_db.id==a).first()
        name = form.Studentname.data
        if not name:
            name=current_user.Studentname
        age = form.Studentage.data
        if not age:
            age=current_user.Studentage
        number = form.number.data
        if not number:
            number=current_user.number
        sex = form.Studentsex.data
        if not sex:
            sex=current_user.Studentsex
        db.session.delete(b)
        db.session.commit()
        new1 = User_db(Studentname=name, Studentage=age, Studentsex=sex, number=number,id=a,password=current_user.password)
        db.session.add(new1)
        db.session.commit()
        flash('修改成功')
        return redirect('/index')
    return render_template('change_information.html',form=form)
@ddd.route('/index_collect')
def index_collect():
    collects=Collect.query.filter(Collect.user_id==current_user.id).all()
    a=[]
    for i in collects:
        b=i.q_id
        a.append(b)
    m=[]
    for i in a:
        question=QuestionModel.query.filter(QuestionModel.id == i).first()
        m.append(question)
    collects = Collect.query.filter(Collect.user_id == current_user.id).all()
    c = []
    for i in collects:
        a = i.q_id
        c.append(a)
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    like = Like.query.filter(Like.user_id == current_user.id).all()
    d = []
    for i in like:
        a = i.question_id
        d.append(a)
    return render_template('index_collect.html',questions=m,c=c,d=d)
@ddd.route('/like-i')
def like_i():
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
    return redirect(url_for('ddd.index_collect'))
@ddd.route('/collect-i')
def collect_i():
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
    return redirect(url_for('ddd.index_collect'))
@ddd.route('/index_like')
def index_like():
    likes=Like.query.filter(Like.user_id==current_user.id).all()
    a=[]
    for i in likes:
        b=i.question_id
        a.append(b)
    m=[]
    for i in a:
        question=QuestionModel.query.filter(QuestionModel.id == i).first()
        m.append(question)
    collects = Collect.query.filter(Collect.user_id == current_user.id).all()
    c = []
    for i in collects:
        a = i.q_id
        c.append(a)
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    like = Like.query.filter(Like.user_id == current_user.id).all()
    d = []
    for i in like:
        a = i.question_id
        d.append(a)
    return render_template('index_like.html',questions=m,c=c,d=d)
@ddd.route('/like-il')
def like_il():
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
    return redirect(url_for('ddd.index_like'))
@ddd.route('/collect-il')
def collect_il():
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
    return redirect(url_for('ddd.index_like'))

@ddd.route('/browsing')
def browsing():
    browsing=Browsing.query.order_by(Browsing.time.desc(),Browsing.user_id==current_user.id).all()
    a=[]
    for i in browsing:
        b=i.q_id
        a.append(b)
    m=[]
    for i in a:
        question=QuestionModel.query.filter(QuestionModel.id == i).first()
        m.append(question)
    collects = Collect.query.filter(Collect.user_id == current_user.id).all()
    c = []
    for i in collects:
        a = i.q_id
        c.append(a)
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    like = Like.query.filter(Like.user_id == current_user.id).all()
    d = []
    for i in like:
        a = i.question_id
        d.append(a)
    return render_template('browsing.html',questions=m,c=c,d=d,browsing=browsing)
@ddd.route('/index_comment')
def index_comment():
    comment=Comment.query.order_by(Comment.creat_time.desc(),Comment.author_id==current_user.id).all()
    a=[]
    for i in comment:
        b=i.question_id
        a.append(b)
    m=[]
    for i in a:
        question=QuestionModel.query.filter(QuestionModel.id == i).first()
        m.append(question)
    collects = Collect.query.filter(Collect.user_id == current_user.id).all()
    c = []
    for i in collects:
        a = i.q_id
        c.append(a)
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    like_comment = Like_comment.query.filter(Like_comment.user_id == current_user.id).all()
    d = []
    for i in like_comment:
        a = i.comment_id
        d.append(a)
    return render_template('index_comment.html',questions=m,c=c,d=d,comment=comment)
@ddd.route('/like_comment-i')
def like_comment_i():
    comment_id = request.args.get('id')
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
            comment.like =comment.like+1
            db.session.commit()
    return redirect(url_for('ddd.index_comment'))


