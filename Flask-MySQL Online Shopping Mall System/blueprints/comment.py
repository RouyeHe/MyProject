from flask import Blueprint,request,redirect,render_template
from model import Comment,U,Book
from main import db
from form import Cedit,Cadd,Csearch
comment=Blueprint('comment',__name__)
@comment.route('/mcomment',methods=('POST','GET'))
def mcomment():
    form=Csearch()
    comments=Comment.query.filter().all()
    if form.validate_on_submit():
        id = form.id.data
        c = form.c.data
        bid = form.bid.data
        uid = form.uid.data
        bn=form.bn.data
        t = form.t.data
        like1=form.like1.data
        if not like1:
            like1=-1
        like2=form.like2.data
        if not  like2:
            like2=1000
        comments=Comment.query.filter(Comment.id.contains(id),Comment.c.contains(c),Comment.bid.contains(bid),
                                      Comment.uid.contains(uid),Comment.t.contains(t),Comment.like<like2,
                                      Comment.like>like1,Comment.bn.contains(bn)).all()
    return render_template('mcomment.html',comments=comments,form=form)
@comment.route('/cdelete',methods=('POST','GET'))
def cdelete():
    cid=request.args.get('id')
    user=Comment.query.filter(Comment.id==cid).first()
    db.session.delete(user)
    db.session.commit()
    return redirect('/my_comment')
@comment.route('/mdelete',methods=('POST','GET'))
def mdelete():
    cid=request.args.get('id')
    user=Comment.query.filter(Comment.id==cid).first()
    db.session.delete(user)
    db.session.commit()
    return redirect('/mcomment')
@comment.route('/cedit',methods=('POST','GET'))
def cedit():
    form=Cedit()
    if form.validate_on_submit():
        cid=request.args.get('id')
        comment = Comment.query.filter(Comment.id == cid).first()
        id=form.id.data
        c=form.c.data
        bid=form.bid.data
        uid=form.uid.data
        t=form.t.data
        like=form.like.data
        if id :
            comment.id=id
            db.session.commit()
        if c:
            comment.c=c
            db.session.commit()
        if bid:
            comment.bid=bid
            db.session.commit()
        if uid:
            comment.uid=uid
            db.session.commit()
        if t:
            comment.t=t
            db.session.commit()
        if like:
            comment.like=like
            db.session.commit()
    cid = request.args.get('id')
    comments=Comment.query.filter().all()
    comment = Comment.query.filter(Comment.id == cid).first()
    return render_template('cedit.html',form=form,comments=comments,comment=comment)
@comment.route('/cadd',methods=('POST','GET'))
def cadd():
    form = Cadd()
    if request.method=='POST':
        id = form.id.data
        c = form.c.data
        bid = form.bid.data
        uid = form.uid.data
        like = form.like.data
        user=U.query.get(uid)
        book=Book.query.get(bid)
        un=user.n
        bn=book.n
        new=Comment(id=id,c=c,bid=bid,uid=uid,like=like,un=un,bn=bn)
        db.session.add(new)
        db.session.commit()
        return redirect('/mcomment')
    cid = request.args.get('id')
    comments = Comment.query.filter().all()
    comment = Comment.query.filter(Comment.id == cid).first()
    return render_template('cadd.html',form=form,comments=comments,comment=comment)
@comment.route('/csearch',methods=('POST','GET'))
def csearch():
    form = Csearch()
    if form.validate_on_submit():
        id = form.id.data
        c = form.c.data
        bid = form.bid.data
        uid = form.uid.data
        t = form.t.data
        like = form.like.data
        comments=Comment.query.filter(Comment.id.contains(id),Comment.c.contains(c),
                            Comment.bid.contains(bid),Comment.uid.contains(uid),
                            Comment.t.contains(t),Comment.like.contains(like)).all()
    else:
        comments = Comment.query.filter().all()
    return render_template(('csearch.html'),form=form,comments=comments)