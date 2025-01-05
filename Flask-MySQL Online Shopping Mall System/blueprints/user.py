from flask import Blueprint,request,redirect,render_template
from model import U
from main import db
from form import Uedit,Uadd,Usearch,Add
user=Blueprint('user',__name__)
@user.route('/muser',methods=('POST','GET'))
def muser():
    form=Usearch()
    if form.validate_on_submit():
        id = form.id.data
        n = form.n.data
        p = form.p.data
        a = form.a.data
        s = form.s.data
        users=U.query.filter(U.n.contains(n),U.id.contains(id),
                            U.p.contains(p),U.a.contains(a),
                            U.s.contains(s)).all()
    else:
        users = U.query.filter().all()
    return render_template('muser.html',form=form,user=users)
@user.route('/udelete',methods=('POST','GET'))
def udelete():
    uid=request.args.get('id')
    user=U.query.filter(U.id==uid).first()
    db.session.delete(user)
    db.session.commit()
    return redirect('/muser')
@user.route('/uedit',methods=('POST','GET'))
def uedit():
    form=Uedit()
    if form.validate_on_submit():
        uid=request.args.get('id')
        user = U.query.filter(U.id == uid).first()
        id=form.id.data
        n=form.n.data
        p=form.p.data
        a=form.a.data
        s=form.s.data
        if id :
            user.id=id
            db.session.commit()
        if n:
            user.n=n
            db.session.commit()
        if p:
            user.p=p
            db.session.commit()
        if a:
            user.a=a
            db.session.commit()
        if s:
            user.s=s
            db.session.commit()
    uid = request.args.get('id')
    users=U.query.filter().all()
    user = U.query.filter(U.id == uid).first()
    return render_template('uedit.html',form=form,users=users,user=user)
@user.route('/uadd',methods=('POST','GET'))
def uadd():
    form = Uadd()
    if form.validate_on_submit():
        id = form.id.data
        n = form.n.data
        p = form.p.data
        a = form.a.data
        s = form.s.data
        new=U(id=id,n=n,p=p,a=a,s=s)
        db.session.add(new)
        db.session.commit()
        return redirect('/muser')
    uid = request.args.get('id')
    users = U.query.filter().all()
    user = U.query.filter(U.id == uid).first()
    return render_template('uadd.html',form=form,user=users)

@user.route('/usearch',methods=('POST','GET'))
def usearch():
    form = Usearch()
    if form.validate_on_submit():
        id = form.id.data
        n = form.n.data
        p = form.p.data
        a = form.a.data
        s = form.s.data
        users=U.query.filter(U.n.contains(n),U.id.contains(id),
                            U.p.contains(p),U.a.contains(a),
                            U.s.contains(s)).all()
    else:
        users = U.query.filter().all()
    return render_template(('usearch.html'),form=form,users=users)