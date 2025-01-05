from form import Login,Register,Search,Comment1,Grade1
from model import U,Book,Comment,Like,Like_comment,Borrow,Collect,Grade
from flask import flash,session,g,Flask,redirect,render_template,url_for,request,flash,Blueprint
from main import db
from flask_login import current_user,LoginManager,login_user,login_required,logout_user
book=Blueprint('book',__name__)
def get_user(user_name):
    users = U.query.filter(U.n==user_name).first()
    if users:
        return users
    return None
@book.route('/login/',methods=('POST','GET'))
def login():
    form=Login()
    if request.method=='POST':
        a=form.a.data
        p=form.p.data
        user1=U.query.filter(U.a==a).first()
        if user1:
            if p==user1.p:
                login_user(user1)
                flash('登陆成功')
                return redirect('/index')
            flash('登陆失败')
    return render_template('login.html',form=form)
@book.route('/')
def home():
    a=current_user.id
    book=Book.query.filter().all()

    return render_template('home.html',book=book)
@book.route('/search',methods=('POST','GET'))
def search():
    form=Search()
    if request.method=='POST':
        a=form.a.data
        n=form.n.data
        t=form.t.data
        book=Book.query.filter(Book.a.contains(a),
                               Book.n.contains(n),
                               Book.t.contains(t),).all()
    else:
        book=Book.query.filter().all()
    return render_template('search.html',form=form,book=book)
@book.route('/register',methods=('POST','GET'))
def register():
    form=Register()
    if request.method=='POST':
        n=form.n.data
        p=form.p.data
        pp=form.pp.data
        if p==pp:
            a=form.a.data
            s=form.s.data
            new=U(n=n,p=p,a=a,s=s)
            db.session.add(new)
            db.session.commit()
            flash('注册成功')
            return redirect('/login')
        else:
            flash('两次密码不一致')
    return render_template('register.html',form=form)



