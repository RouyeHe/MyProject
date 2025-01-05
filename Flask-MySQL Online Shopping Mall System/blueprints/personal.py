from flask import Blueprint,request,redirect,render_template,flash
from flask_login import current_user

from model import Collect,Borrow,Like,U,Book,Comment,Record
from main import db
from form import Cedit,Cadd,Csearch,Information,Password,Search
personal=Blueprint('personal',__name__)
@personal.route('/dcollect')
def dcollect():
    id=request.args.get('id')
    collect=Collect.query.filter(Collect.id==id).first()
    db.session.delete(collect)
    db.session.commit()
    return redirect('/index')
@personal.route('/dborrow')
def dborrow():
    id=request.args.get('id')
    borrow=Borrow.query.filter(Borrow.id==id).first()
    bid=borrow.bid
    db.session.delete(borrow)
    db.session.commit()
    book=Book.query.filter(Book.id==bid).first()
    book.s+=1
    user=current_user
    user.b+=book.p
    db.session.commit()

    return redirect('/index')
@personal.route('/dlike')
def dlike():
    id=request.args.get('id')
    like=Like.query.filter(Like.id==id).first()
    db.session.delete(like)
    db.session.commit()
    return redirect('/index')
@personal.route('/information',methods=('POST','GET'))
def information():
    form1=Information()
    form=Search()
    if request.method=='POST':
        n=form1.n.data
        s=form1.s.data
        user=U.query.filter(U.id==current_user.id).first()
        if n:
            user.n=n
            db.session.commit()
        if s:
            user.s=s
            db.session.commit()
        flash('修改成功')
        return redirect('/index')
    user=U.query.filter(U.id==current_user.id).first()
    return render_template('information.html',form=form,form1=form1,user=user)
@personal.route('/password',methods=('POST','GET'))
def password():
    form=Password()
    id=request.args.get('id')
    if form.validate_on_submit():
        p=form.p.data
        pp=form.pp.data
        pp1=form.pp1.data
        user=U.query.filter(U.id==current_user.id).first()
        if user.p==p:
            if pp==pp1:
                user.p=pp
                db.session.commit()
                flash('修改成功')
            else:
                flash('新密码两次不一致')
        else:
            flash('原密码不正确')
        return redirect('/index')
    user = U.query.filter(U.id == current_user.id).first()
    return render_template('password.html',form=form,user=user)


@personal.route('/recharge', methods=('POST', 'GET'))
def recharge():
    if request.method == 'POST':
        # 获取表单提交的充值金额和充值方式
        amount = request.form.get('amount', type=float)  # 获取充值金额
        method = request.form.get('method')  # 获取充值方式

        # 确保金额大于0
        if amount and amount > 0:
            # 假设 'u' 是当前用户的对象
            u = current_user  # 获取当前登录用户对象（如果使用 flask-login）

            # 更新用户余额
            u.b += amount  # 假设 `balance` 是用户余额的属性

            # 提交到数据库
            db.session.commit()  # 如果您使用数据库，记得提交更改
            flash('充值成功')

            return redirect('/index')  # 充值成功后重新加载页面
        else:
            # 如果金额不合法，使用 flash 提示错误信息
            flash('充值金额必须大于0！', 'error')  # 使用 error 分类的提示
            return redirect('/index')  # 重新加载页面

    return render_template('recharge.html')
@personal.route('/my_like')
def my_like():
    form=Search()
    like=Like.query.filter(Like.uid==current_user.id).all()
    a=[]
    for i in like:
        s=i.bid
        a.append(s)
    b=[]
    for i in a:
        book=Book.query.filter(Book.id==i).first()
        b.append(book)
    return render_template('my_like.html',book=b,form=form)
@personal.route('/my_collect')
def my_collect():
    form=Search()
    collect = Collect.query.filter(Collect.uid == current_user.id).all()
    a = []
    for i in collect:
        s = i.bid
        a.append(s)
    b = []
    for i in a:
        book = Book.query.filter(Book.id == i).first()
        b.append(book)
    return render_template('collect.html', book=b, form=form)
@personal.route('/my_comment')
def my_collects():
    form=Search()
    comment = Comment.query.filter(Comment.uid == current_user.id).all()

    return render_template('my_comment.html', comment=comment, form=form)
@personal.route('/record')
def record():
    form=Search()
    record = Record.query.filter(Record.uid == current_user.id).all()
    a = []
    for i in record:
        s = i.bid
        a.append(s)
    b = []
    for i in a:
        book = Book.query.filter(Book.id == i).first()
        b.append(book)
    return render_template('record.html',record=record, book=b, form=form)
@personal.route('/rdelete')
def rdelete():
    form=Search()
    id=request.args.get('id')
    record = Record.query.filter(Record.id == id).first()
    db.session.delete(record)
    db.session.commit()
    return redirect('/record')
