from models import QuestionModel
from flask import render_template,Blueprint,Flask
aaa=Blueprint('aaa',__name__)

@aaa.route('/dangzheng')
def dangzheng():
    questions = QuestionModel.query.filter(QuestionModel.class1=='党政').all()
    return render_template('dangzheng.html',questions=questions)
@aaa.route('/yule')
def yule():
    questions = QuestionModel.query.filter(QuestionModel.class1=='娱乐').all()
    return render_template('yule.html',questions=questions)
@aaa.route('/taolun')
def taolun():
    questions = QuestionModel.query.filter(QuestionModel.class1=='讨论').all()
    return render_template('taolun.html',questions=questions)
@aaa.route('/fazhi')
def fazhi():
    questions = QuestionModel.query.filter(QuestionModel.class2=='法治').all()
    return render_template('fazhi.html',questions=questions)
@aaa.route('/junshi')
def junshi():
    questions = QuestionModel.query.filter(QuestionModel.class2=='军事').all()
    return render_template('junshi.html',questions=questions)
@aaa.route('/dangshi')
def dangshi():
    questions = QuestionModel.query.filter(QuestionModel.class2=='党史').all()
    return render_template('dangshi.html',questions=questions)
@aaa.route('/fanfu')
def fanfu():
    questions = QuestionModel.query.filter(QuestionModel.class2=='反腐').all()
    return render_template('fanfu.html',questions=questions)
@aaa.route('/dangjian')
def dangjian():
    questions = QuestionModel.query.filter(QuestionModel.class2=='党建').all()
    return render_template('dangjian.html',questions=questions)
@aaa.route('/meishi')
def meishi():
    questions = QuestionModel.query.filter(QuestionModel.class2=='美食').all()
    return render_template('meishi.html',questions=questions)
@aaa.route('/dianshiju')
def dianshiju():
    questions = QuestionModel.query.filter(QuestionModel.class2=='电视剧').all()
    return render_template('dianshiju.html',questions=questions)
@aaa.route('/yinyue')
def yinyue():
    questions = QuestionModel.query.filter(QuestionModel.class2=='音乐').all()
    return render_template('yinyue.html',questions=questions)
@aaa.route('/youxi')
def youxi():
    questions = QuestionModel.query.filter(QuestionModel.class2=='游戏').all()
    return render_template('youxi.html',questions=questions)
@aaa.route('/lundangzheng')
def lundangzheng():
    questions = QuestionModel.query.filter(QuestionModel.class2=='论党政').all()
    return render_template('lundangzheng.html',questions=questions)
@aaa.route('/lunyule')
def lunyule():
    questions = QuestionModel.query.filter(QuestionModel.class2=='论娱乐').all()
    return render_template('lunyule.html',questions=questions)
@aaa.route('/xianliao')
def xiaoliao():
    questions = QuestionModel.query.filter(QuestionModel.class2=='闲聊').all()
    return render_template('xianliao.html',questions=questions)
