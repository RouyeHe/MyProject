from flask import render_template,Blueprint,request,redirect
from models import User_db,User,Admin,QuestionModel,Comment
from exts import db
from forms import LoginForm,LoginForm1,QuestionForm,Search,Addcomment,Change_password,Change_information,Register,C,Q,S,S1,Q1,C1
ccc=Blueprint('ccc',__name__)




@ccc.route('/add-s',methods=('POST','GET'))
def add_s():
    form=S()
    if form.validate_on_submit():
        id=form.id.data
        name = form.name.data
        age = form.age.data
        number = form.number.data
        sex = form.sex.data
        password=form.password.data
        new1=User_db(Studentname=name,Studentage=age,Studentsex=sex,number=number,id=id,password=password)
        db.session.add(new1)
        db.session.commit()
        return redirect('info')
    result=User_db.query.filter().all()
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    comments=Comment.query.order_by(Comment.creat_time.desc()).all()
    return render_template('add-s.html',result=result,questions=questions,comments=comments,form=form)
@ccc.route('/add-c',methods=('POST','GET'))
def add_c():
    form = C()
    if request.method=='POST':
        id = form.id.data
        comment = form.comment.data
        question_id = form.question_id.data
        author_id = form.author_id.data
        new1 = Comment(id=id,comment=comment,question_id=question_id,author_id=author_id)
        db.session.add(new1)
        db.session.commit()
        return redirect('info')
    result = User_db.query.filter().all()
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    comments = Comment.query.order_by(Comment.creat_time.desc()).all()
    return render_template('add-c.html', result=result, questions=questions, comments=comments, form=form)
@ccc.route('/add-q',methods=('POST','GET'))
def add_q():
    form = Q()
    if request.method == 'POST':
        id = form.id.data
        title = form.title.data
        content = form.content.data
        author_id = form.author_id.data
        class1=form.class1.data
        class2=form.class2.data
        new1 = QuestionModel(id=id,title=title, content=content,class1=class1,class2=class2, author_id=author_id)
        db.session.add(new1)
        db.session.commit()
        return redirect('info')
    result = User_db.query.filter().all()
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    comments = Comment.query.order_by(Comment.creat_time.desc()).all()
    return render_template('add-q.html', result=result, questions=questions, comments=comments, form=form)
@ccc.route('/edit_s',methods=('POST','GET'))
def edit_s():
    form=S()
    if form.validate_on_submit():
        oldid = request.args.get('id')
        old = User_db.query.get(oldid)
        id=form.id.data
        name = form.name.data
        age = form.age.data
        number = form.number.data
        sex = form.sex.data
        password=form.password.data
        new1=User_db(Studentname=name,Studentage=age,Studentsex=sex,number=number,id=id,password=password)
        db.session.delete(old)
        db.session.commit()
        db.session.add(new1)
        db.session.commit()
        return redirect('info')
    result=User_db.query.filter().all()
    oldid = request.args.get('id')
    old = User_db.query.get(oldid)
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    comments=Comment.query.order_by(Comment.creat_time.desc()).all()
    return render_template('edit_s.html',result=result,questions=questions,comments=comments,form=form,old=old)
@ccc.route('/delete-q')

def delete_q():
    c=request.args.get('id')
    a=QuestionModel.query.get(c)
    db.session.delete(a)
    db.session.commit()
    return redirect('/info')
@ccc.route('/delete')

def delete():
    c=request.args.get('id')
    a=User_db.query.get(c)
    db.session.delete(a)
    db.session.commit()
    return redirect('/info')
@ccc.route('/delete-c')

def delete_c():
    c=request.args.get('id')
    a=Comment.query.get(c)
    db.session.delete(a)
    db.session.commit()
    return redirect('/info')
@ccc.route('/search-s',methods=('POST','GET'))

def search_s():
    form = S1()
    if form.validate_on_submit():
        id = form.id.data
        name = form.name.data
        age = form.age.data
        number = form.number.data
        sex = form.sex.data
        password = form.password.data
        result = User_db.query.filter(User_db.id.contains(id),
                                      User_db.number.contains(number),
                                      User_db.Studentname.contains(name),
                                      User_db.Studentage.contains(age),
                                      User_db.Studentsex.contains(sex),
                                      User_db.password.contains(password)).all()
    else:
        result = User_db.query.all()
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    comments = Comment.query.order_by(Comment.creat_time.desc()).all()
    return render_template('search-s.html', result=result, questions=questions, comments=comments, form=form)
@ccc.route('/search-c',methods=('POST','GET'))

def search_c():
    form = C1()
    if form.validate_on_submit():
        id = form.id.data
        content = form.comment.data
        question_id= form.question_id.data
        author_id = form.author_id.data
        creat_time = form.creat_time.data
        print(id,content,question_id,author_id,creat_time)
        result = Comment.query.filter(Comment.question_id.contains(question_id),
                                      Comment.creat_time.contains(creat_time),
                                      Comment.id.contains(id),
                                      Comment.comment.contains(content),
                                      Comment.author_id.contains(author_id),
                                      ).all()
        print(result)
    else:
        result = Comment.query.all()
    return render_template('search-c.html', result=result,  form=form)
@ccc.route('/search-q',methods=('POST','GET'))
def search_q():
    form = Q1()
    if form.validate_on_submit():
        id = form.id.data
        title = form.title.data
        content = form.content.data
        create_time = form.create_time.data
        author_id = form.author_id.data
        class1 = form.class1.data
        class2=form.class2.data
        result = QuestionModel.query.filter(QuestionModel.id.contains(id),
                                      QuestionModel.title.contains(title),
                                      QuestionModel.content.contains(content),
                                      QuestionModel.create_time.contains(create_time),
                                      QuestionModel.author_id.contains(author_id),
                                      QuestionModel.class1.contains(class1),
                                QuestionModel.class2.contains(class2)).all()
    else:
        result = QuestionModel.query.all()
    return render_template('search-q.html', result=result, form=form)
@ccc.route('/edit-q',methods=('POST','GET'))
def edit_q():
    form=Q()
    if form.validate_on_submit():
        oldid = request.args.get('id')
        old = QuestionModel.query.get(oldid)
        id = form.id.data
        title = form.title.data
        content = form.content.data
        create_time = form.create_time.data
        author_id = form.author_id.data
        class1 = form.class1.data
        class2 = form.class2.data
        new1=QuestionModel(id=id,title=title,content=content,create_time=create_time,author_id=author_id,class2=class2,class1=class1)
        db.session.delete(old)
        db.session.commit()
        db.session.add(new1)
        db.session.commit()
        return redirect('info')
    oldid = request.args.get('id')
    old = QuestionModel.query.get(oldid)
    questions=QuestionModel.query.filter().all()
    return render_template('edit-q.html',old=old,questions=questions,form=form)
@ccc.route('/edit-c',methods=('POST','GET'))
def edit_c():
    form=C()
    if form.validate_on_submit():
        oldid = request.args.get('id')
        old = Comment.query.get(oldid)
        id = form.id.data
        content = form.comment.data
        question_id = form.question_id.data
        author_id = form.author_id.data
        creat_time = form.creat_time.data
        new1=Comment(id=id,comment=content,question_id=question_id,author_id=author_id,creat_time=creat_time)
        db.session.delete(old)
        db.session.commit()
        db.session.add(new1)
        db.session.commit()
        return redirect('info')
    comments=Comment.query.filter().all()
    oldid = request.args.get('id')
    old = Comment.query.get(oldid)
    return render_template('edit-c.html',comments=comments,form=form,old=old)