from flask import flash,session,g,Flask,redirect,render_template,url_for,request,flash
from flask_login import current_user,LoginManager,login_user,login_required,logout_user
from main import db
from form import Login,Register,Search,Comment1,Grade1,Buy,Add,Edit,Msearch
from model import U,Book,Comment,Like,Like_comment,Borrow,Collect,Grade,Record
from blueprints.t import t
from blueprints.book import book
from blueprints.user import user
from blueprints.comment import comment
from blueprints.personal import personal
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:123456@127.0.0.1:3306/book"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['SECRET_KEY']='asdafasdasdf'
db.init_app(app)
login = LoginManager(app)
login.init_app(app)
login.login_view = 'login'
app.register_blueprint(t)
app.register_blueprint(user)
app.register_blueprint(comment)
app.register_blueprint(personal)
@login.user_loader
def load_user(user_id):
    return U.query.get(int(user_id))
@app.route('/login/',methods=('POST','GET'))
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
            flash('密码错误')
        else:
            flash('账号不存在')
    return render_template('login.html',form=form)
@app.route('/',methods=('POST','GET'))
@login_required
def home():
    form=Search()
    a=current_user.id
    book=Book.query.filter(Book.s>0).all()
    books = Book.query.filter(Book.s > 0).all()
    book1 = Book.query.filter(Book.s == 0).all()
    if form.validate_on_submit():
        a = form.a.data
        n = form.n.data
        t = form.t.data
        s1 = form.s1.data
        if not s1:
            s1 = -1

        s2 = form.s2.data
        if not s2:
            s2 = 1000
        g1 = form.g1.data
        if not g1:
            g1 = -1
        g2 = form.g2.data
        like1 = form.like1.data
        like2 = form.like2.data
        if not g2:
            g2 = 6
        if not like1:
            like1 = -1
        if not like2:
            like2 = 1000
        if t:
            books = Book.query.filter(Book.s > s1, Book.s < s2, Book.like > like1, Book.like < like2, Book.g > g1,
                                      Book.g < g2,
                                      Book.a.contains(a), Book.n.contains(n), Book.t == t).all()
        if not t:
            books = Book.query.filter(Book.s > s1, Book.s < s2, Book.like > like1, Book.like < like2, Book.g > g1,
                                      Book.g < g2,
                                      Book.a.contains(a), Book.n.contains(n)).all()
    return render_template('home.html',book=books,form=form)
@app.route('/search',methods=('POST','GET'))
def search():
    form=Search()
    if request.method=='POST':
        a=form.a.data
        n=form.n.data
        t=form.t.data
        book=Book.query.filter(Book.a.contains(a),
                               Book.n.contains(n),
                               Book.t.contains(t),
                               Book.s>0).all()
    else:
        book=Book.query.filter().all()
    return render_template('search.html',form=form,book=book)
@app.route('/register',methods=('POST','GET'))
def register():
    form1=Search()
    form=Register()
    if request.method=='POST':
        n=form.n.data
        p=form.p.data
        pp=form.pp.data
        if p==pp:
            a=form.a.data
            A=U.query.filter(U.a==a).first()

            if A!=None:
                flash('账号已存在')
            else:
                s=form.s.data
                new=U(n=n,p=p,a=a,s=s,b=0)
                db.session.add(new)
                db.session.commit()
                flash('注册成功')
                return redirect('/login')
        else:
            flash('两次密码不一致')
    return render_template('register.html',form=form,form1=form1)
@app.route('/book',methods=('POST','GET'))
def book():
    form1=Comment1()
    form=Search()
    form2=Grade1()
    s=request.args.get('id')
    cid=request.args.get('cid')
    uid=current_user.id
    book=Book.query.filter(Book.id==s).first()
    record=Record(uid=uid,bid=s,bn=book.n,ba=book.a)
    db.session.add(record)
    db.session.commit()
    if form1.validate_on_submit():
        c=form1.c.data
        comment=Comment(c=c,bid=s,uid=current_user.id,like=0,un=current_user.n,bn=book.n)
        db.session.add(comment)
        db.session.commit()
        db.session.commit()
        return redirect('book?id=%d'%int(s))
    if form2.validate_on_submit():

        grades=Grade.query.filter(Grade.bid==s).all()

        k=True
        for i in grades:
            if i.uid==uid:
                k=False
                flash('您已评分此商品')
        if k:
            g = form2.g.data
            grade = Grade(g=g, uid=uid, bid=s)
            db.session.add(grade)
            db.session.commit()
            flash('评分成功')
            book.g_s += int(g)
            book.g_n+=1
            book.g = round(book.g_s / book.g_n, 2)
            db.session.commit()


    comment=Comment.query.filter(Comment.bid==s).all()
    like = Like.query.filter(Like.bid==s).all()
    like_comment=Like_comment.query.filter(Like_comment.uid==current_user.id).all()
    collect=Collect.query.filter(Collect.bid==s).all()
    comment_number=len(comment)
    k=True
    for a in like:
        if a.uid==uid:
            k=False
    l=True
    for a in collect:
        if a.uid==uid:
            l=False
    o=[]
    for a in like_comment:
        v=a.cid
        o.append(v)
    return render_template('book.html',o=o,k=k,l=l,collect=collect,
                           book=book,form=form,comment=comment,like=like,
                           likes=str(book.like),like_comment=like_comment,
                           form1=form1,form2=form2,comment_number=comment_number)


@app.route('/like')
def like():
    bid = request.args.get('id')
    uid=current_user.id
    like1=Like.query.filter(Like.bid==bid).all()
    form=Comment1()
    k=True
    for a in like1:
        if a.uid==uid:
            k=False
            db.session.delete(a)
            db.session.commit()
            book=Book.query.filter(Book.id==bid).first()
            book.like=book.like-1
            db.session.commit()
    if k:
        book = Book.query.filter(Book.id == bid).first()
        like=Like(bid=bid,uid=uid,bn=book.n,ba=book.a)
        db.session.add(like)
        db.session.commit()
        book.like =book.like+1
        db.session.commit()
    return redirect('book?id=%d'%int(bid))
@app.route('/like_comment')
def like_comment():
    bid = request.args.get('id')
    uid=current_user.id
    cid=request.args.get('cid')

    like1=Like_comment.query.filter(Like_comment.cid==cid).all()

    k=True
    if str(like1) =='[]':
        like = Like_comment(cid=cid, uid=uid)
        db.session.add(like)
        db.session.commit()
        comment=Comment.query.filter(Comment.id==cid).first()
        comment.like+=1
        db.session.commit()
    else:
        for a in like1:
            if a.uid==uid:
                k=False
                db.session.delete(a)
                db.session.commit()
                db.session.commit()
                comment = Comment.query.filter(Comment.id == cid).first()
                comment.like=comment.like-1
                db.session.commit()
        if k:
            like=Like_comment(cid=cid,uid=uid)
            db.session.add(like)
            db.session.commit()
            comment = Comment.query.filter(Comment.id == cid).first()
            comment.like += 1
            db.session.commit()
    return redirect('book?id=%d'%int(bid))


@app.route('/borrow')
def borrow():
    bid = request.args.get('id')  # 获取书籍的 ID
    uid = current_user.id  # 获取当前登录用户的 ID
    book = Book.query.get(bid)  # 获取书籍信息
    s = book.s  # 书籍的库存
    price = book.p  # 书籍的价格
    k = True  # 购买状态标识

    # 获取当前用户的余额
    user = current_user
    balance = user.b  # 当前用户的余额

    if k:
        # 判断库存是否足够
        if s >= 1:
            # 判断余额是否足够
            if balance >= price:
                # 如果余额足够，扣除余额
                user.b -= price
                book.s = s - 1  # 库存减1
                db.session.commit()  # 提交更新

                # 创建借阅记录
                borrow = Borrow(bid=bid, uid=uid, bn=book.n, ba=book.a)
                db.session.add(borrow)  # 添加借阅记录到数据库
                db.session.commit()  # 提交数据库事务

                # 提示用户购买成功
                flash('购买成功')
            else:
                # 余额不足，提示用户
                flash('余额不足，无法购买此商品')
        else:
            # 库存不足，提示用户
            flash('库存不足')

    # 重定向回书籍详情页面
    return redirect('book?id=%d' % int(bid))


@app.route('/collect')
def collect():
    bid = request.args.get('id')
    uid=current_user.id
    collect=Collect.query.filter(Collect.bid==bid).all()
    form=Comment1()
    k=True
    for a in collect:
        if a.uid==uid:
            k=False
            db.session.delete(a)
            db.session.commit()
    if k:
        book=Book.query.filter(Book.id==bid).first()
        collect=Collect(bid=bid,uid=uid,bn=book.n,ba=book.a)
        db.session.add(collect)
        db.session.commit()
    return redirect('book?id=%d'%int(bid))
@app.route('/index')
def index():
    form=Search()
    uid=current_user.id
    user=U.query.filter(U.id==uid).first()
    like=Like.query.filter(Like.uid==uid).all()
    collect=Collect.query.filter(Collect.uid==uid).all()
    borrow=Borrow.query.filter(Borrow.uid==uid).all()
    record=Record.query.filter(Record.uid==uid).all()
    return render_template('index.html',user=user,like=like,collect=collect,borrow=borrow,record=record,form=form)

@app.route('/admin')
def admin():
    return redirect('/manage')
@app.route('/buy',methods=('POST','GET'))
def buy():
    form=Buy()
    n=form.n.data
    a=form.a.data
    x=form.x.data
    t=form.t.data
    if form.validate_on_submit():
        book=Book(n=n,a=a,s=x,t=t,like=0,g=None,c=0)
        db.session.add(book)
        db.session.commit()
        return redirect('/admin')
    return render_template('buy.html',form=form)
@app.route('/manage',methods=('POST','GET'))
def manage():
    form1 = Add()
    bid = request.args.get('id')
    book = Book.query.filter(Book.id == bid).first()
    form=Search()
    books=Book.query.filter(Book.s>0).all()
    book1 = Book.query.filter(Book.s == 0).all()
    k=True
    if form.validate_on_submit():
        a=form.a.data
        n=form.a.data
        t=form.t.data
        s1=form.s1.data
        if not s1:
            s1=-1

        s2=form.s2.data
        if not s2:
            s2=1000
        g1=form.g1.data
        if not g1:
            g1=-1
        g2=form.g2.data
        like1=form.like1.data
        like2=form.like2.data
        if not g2:
            g2=6
        if not like1:
            like1=-1
        if not like2:
            like2=1000
        if t:
            books=Book.query.filter(Book.s>s1,Book.s<s2,Book.like>like1,Book.like<like2,Book.g>g1,Book.g<g2,
                                Book.a.contains(a),Book.n.contains(n),Book.t==t).all()
        if not t:
            books = Book.query.filter(Book.s > s1, Book.s < s2, Book.like > like1, Book.like < like2, Book.g > g1,
                                      Book.g < g2,
                                      Book.a.contains(a), Book.n.contains(n)).all()
        k=False
    return render_template('manage.html',books=books,book1=book1,form=form,k=k,form1=form1,book=book)
@app.route('/off')
def off():
    bid=request.args.get('id')
    book = Book.query.filter(Book.id==bid).first()
    a = book.s
    book.s = 0
    db.session.commit()
    return redirect('/manage')
@app.route('/off1')
def off1():
    bid=request.args.get('id')
    book = Book.query.filter(Book.id==bid and Book.s>0).first()
    a=book.s
    book.s=a-1
    db.session.commit()
    return redirect('/manage')
@app.route('/off2')
def off2():
    bid = request.args.get('id')
    book = Book.query.filter(Book.id == bid and Book.s > 0).first()
    db.session.add(book)
    db.session.commit()
    return redirect('/manage')
@app.route('/add',methods=('POST','GET'))
def add():
    form = Add()
    bid = request.args.get('id')
    book = Book.query.filter(Book.id == bid).first()
    books = Book.query.filter(Book.s > 0).all()
    book1 = Book.query.filter(Book.s == 0).all()
    k=True
    if form.validate_on_submit():
        x = form.x.data
        book = Book.query.filter(Book.id == bid).first()
        book.s += int(x)
        db.session.commit()
        return redirect('/manage')
    return render_template('add.html',form=form,book=book,books=books,book1=book1,k=k)
@app.route('/edit',methods=('POST','GET'))
def edit():
    form=Edit()
    bid=request.args.get('id')
    if form.validate_on_submit():
        n=form.n.data
        a=form.a.data
        t=form.t.data
        bid=request.args.get('id')
        book=Book.query.filter(Book.id==bid).first()
        if a:
            book.a=a
            db.session.commit()
        if n:
            book.n=n
            db.session.commit()
        if t:
            book.t=t
            db.session.commit()
        return redirect('/manage')
    book = Book.query.filter(Book.id == bid).first()
    books = Book.query.filter(Book.s > 0).all()
    book1 = Book.query.filter(Book.s == 0).all()
    k=True
    return render_template('edit.html',form=form,book=book,books=books,book1=book1,k=k)
@app.route('/msearch',methods=('POST','GET'))
def msearch():
    form=Msearch()
    books = Book.query.filter(Book.s > 0).all()
    book1 = Book.query.filter(Book.s == 0).all()
    if form.validate_on_submit():
        n=form.n.data
        a=form.a.data
        t=form.t.data
        books = Book.query.filter(Book.s > 0,Book.n.contains(n),Book.a.contains(a),Book.t.contains(t)).all()
        book1 = Book.query.filter(Book.s == 0,Book.n.contains(n),Book.a.contains(a),Book.t.contains(t)).all()
    return render_template('msearch.html',form=form,book=book,books=books,book1=book1)
@app.route('/loginout')
def loginout():
    logout_user()
    flash('已退出登录')
    return redirect('/login')
@app.route('/try1',methods=('POST','GET'))
def try1():
    return render_template('try1.html')
if __name__=='__main__':
    app.run(debug=True)