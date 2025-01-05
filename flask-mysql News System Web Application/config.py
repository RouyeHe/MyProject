a=[1,2,3,4,5]
t=0
for k in a:
    t+=1
    if t<=3:
        print(k)


        class Comment(db.Model):
            __tablename__ = "comment"
            id = db.Column(db.Integer, primary_key=True, autoincrement=True)
            comment = db.Column(db.Text, nullable=False)
            create_time = db.Column(db.DateTime, default=datetime.now)
            queston_id = db.Column(db.Integer, db.ForeignKey('question.id'))
            author_id = db.Column(db.Integer, db.ForeignKey('uu.id'))
            queston = db.relationship(QuestionModel, backref=db.backref('answers', order_by=create_time.desc()))
            author = db.relationship(QuestionModel, backref='answers')


<div class="a" style="margin-top: 40px">
    {% for message in get_flashed_messages() %}
        <div class="alert">{{ message }}<button class="close">×</button></div>
    {% endfor %}
    用户名{{Studentname}}<a href='{{ url_for('logout')}}'>登出</a>
</div>
