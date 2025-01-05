from main import db
class U(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    n = db.Column(db.Text)
    s = db.Column(db.Text)
    p = db.Column(db.Integer)
    a = db.Column(db.Integer)