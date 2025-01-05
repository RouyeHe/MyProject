from wtforms import StringField,SubmitField,PasswordField,SelectField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
class Login(FlaskForm):
    a=StringField(validators=[DataRequired()])
    p=PasswordField(validators=[DataRequired()])
    submit=SubmitField('登录')


class Register(FlaskForm):
    a=StringField(validators=[DataRequired()])
    p=PasswordField(validators=[DataRequired()])
    pp=PasswordField(validators=[DataRequired()])
    n=StringField(validators=[DataRequired()])
    s=SelectField(choices=['男','女'],validators=[DataRequired()])
    submit=SubmitField('注册')
class Search(FlaskForm):
    id=StringField()
    a=StringField()
    t=SelectField(choices=['','电子产品','运动户外','家用电器','图书音像','服饰服装','汽车用品','美妆护肤','宠物用品','食品饮料',
                           '玩具乐器','家具用品','办公用品','母婴用品','健康护理'])
    n=StringField()
    s1=StringField()
    s2=StringField()
    g1=StringField()
    g2=StringField()
    like1=StringField()
    like2=StringField()
    submit = SubmitField('搜索')

class Comment1(FlaskForm):
    c=StringField(validators=[DataRequired()])
    submit=SubmitField('评论')
class Grade1(FlaskForm):
    g=SelectField(choices=[1,2,3,4,5])
    submit=SubmitField('评分')
class Buy(FlaskForm):
    n=StringField(validators=[DataRequired()])
    a=StringField(validators=[DataRequired()])
    x=StringField(validators=[DataRequired()])
    t=SelectField(choices=['电子产品','运动户外','家用电器','图书音像','服饰服装','汽车用品','美妆护肤','宠物用品','食品饮料',
                           '玩具乐器','家具用品','办公用品','母婴用品','健康护理'])
    submit=SubmitField('购买')
class Add(FlaskForm):
    x=StringField(validators=[DataRequired()])
    submit=SubmitField('购买')
class Edit(FlaskForm):
    n = StringField()
    a = StringField()
    t = SelectField(label=None,choices=['','电子产品', '运动户外', '家用电器', '图书音像', '服饰服装', '汽车用品', '美妆护肤', '宠物用品', '食品饮料',
                             '玩具乐器', '家具用品', '办公用品', '母婴用品', '健康护理'])
    submit = SubmitField('更改')
class Msearch(FlaskForm):
    n = StringField()
    a = StringField()
    t = SelectField(label=None,choices=['','电子产品', '运动户外', '家用电器', '图书音像', '服饰服装', '汽车用品', '美妆护肤', '宠物用品', '食品饮料',
                             '玩具乐器', '家具用品', '办公用品', '母婴用品', '健康护理'])
    submit = SubmitField('搜索')
class Uedit(FlaskForm):
    a=StringField()
    p=StringField()
    n=StringField()
    s=SelectField(choices=['','男','女'])
    id=StringField()
    submit=SubmitField('更改')
class Uadd(FlaskForm):
    a=StringField(validators=[DataRequired()])
    p=StringField(validators=[DataRequired()])
    n=StringField(validators=[DataRequired()])
    s=SelectField(choices=['','男','女'])
    id=StringField(validators=[DataRequired()])
    submit=SubmitField('增添')
class Usearch(FlaskForm):
    a=StringField()
    p=StringField()
    n=StringField()
    s=SelectField(choices=['','男','女'])
    id=StringField()
    submit=SubmitField('查找')
class Cedit(FlaskForm):
    id=StringField()
    c=StringField()
    bid=StringField()
    uid=StringField()
    t=StringField()
    like=StringField()
    submit=SubmitField('更改')
class Cadd(FlaskForm):
    id=StringField(validators=[DataRequired()])
    c=StringField(validators=[DataRequired()])
    bid=StringField(validators=[DataRequired()])
    uid=StringField(validators=[DataRequired()])
    t=StringField(validators=[DataRequired()])
    like=StringField(validators=[DataRequired()])
    submit=SubmitField('增添')
class Csearch(FlaskForm):
    id=StringField()
    c=StringField()
    bid=StringField()
    uid=StringField()
    t=StringField()
    bn=StringField()
    like1=StringField()
    like2 = StringField()
    submit=SubmitField('查找')
class Information(FlaskForm):
    n = StringField()
    s = SelectField(choices=['', '男', '女'])
    submit = SubmitField('修改')
class Password(FlaskForm):
    p=StringField(validators=[DataRequired()])
    pp=StringField(validators=[DataRequired()])
    pp1=StringField(validators=[DataRequired()])
    submit = SubmitField('修改')