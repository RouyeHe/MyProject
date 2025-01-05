from flask import Blueprint,render_template
from model import Book
from form import Search
t=Blueprint('t',__name__)

@t.route('/t1')
def t1():
    form = Search()
    book = Book.query.filter(Book.t == '电子产品', Book.s > 0)
    return render_template('t1.html', book=book, form=form)

@t.route('/t2')
def t2():
    form = Search()
    book = Book.query.filter(Book.t == '家用电器', Book.s > 0)
    return render_template('t2.html', book=book, form=form)

@t.route('/t3')
def t3():
    form = Search()
    book = Book.query.filter(Book.t == '服装服饰', Book.s > 0)
    return render_template('t3.html', book=book, form=form)

@t.route('/t4')
def t4():
    form = Search()
    book = Book.query.filter(Book.t == '美妆护肤', Book.s > 0)
    return render_template('t4.html', book=book, form=form)

@t.route('/t5')
def t5():
    form = Search()
    book = Book.query.filter(Book.t == '食品饮料', Book.s > 0)
    return render_template('t5.html', book=book, form=form)

@t.route('/t6')
def t6():
    form = Search()
    book = Book.query.filter(Book.t == '家居用品', Book.s > 0)
    return render_template('t6.html', book=book, form=form)

@t.route('/t7')
def t7():
    form = Search()
    book = Book.query.filter(Book.t == '母婴用品', Book.s > 0)
    return render_template('t7.html', book=book, form=form)

@t.route('/t8')
def t8():
    form = Search()
    book = Book.query.filter(Book.t == '运动户外', Book.s > 0)
    return render_template('t8.html', book=book, form=form)

@t.route('/t9')
def t9():
    form = Search()
    book = Book.query.filter(Book.t == '图书音像', Book.s > 0)
    return render_template('t9.html', book=book, form=form)

@t.route('/t10')
def t10():
    form = Search()
    book = Book.query.filter(Book.t == '汽车用品', Book.s > 0)
    return render_template('t10.html', book=book, form=form)

@t.route('/t11')
def t11():
    form = Search()
    book = Book.query.filter(Book.t == '宠物用品', Book.s > 0)
    return render_template('t11.html', book=book, form=form)

@t.route('/t12')
def t12():
    form = Search()
    book = Book.query.filter(Book.t == '玩具乐器', Book.s > 0)
    return render_template('t12.html', book=book, form=form)

@t.route('/t13')
def t13():
    form = Search()
    book = Book.query.filter(Book.t == '办公用品', Book.s > 0)
    return render_template('t13.html', book=book, form=form)

@t.route('/t14')
def t14():
    form = Search()
    book = Book.query.filter(Book.t == '健康护理', Book.s > 0)
    return render_template('t14.html', book=book, form=form)
