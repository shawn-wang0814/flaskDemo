from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request

import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:lw880814@localhost:3306/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),nullable=False,unique=True)
    age = db.Column(db.Integer)
    email = db.Column(db.String(120),unique=True)
    def __init__(self,username,age,email):
        self.username = username
        self.age = age
        self.email = email
    def __repr__(self):
        return "<User:%r>"%self.username

class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    sname = db.Column(db.String(80),nullable=False)
    sage = db.Column(db.Integer)
    def __init__(self,sname,sage):
        self.sname = sname
        self.sage = sage
    def __repr__(self):
        return "<Student%s>"%self.sname
class Teacher(db.Model):
    __tablename__ = "teacher"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    tname = db.Column(db.String(30),nullable=False)
    tage = db.Column(db.Integer)
    course_id = db.Column(db.Integer,db.ForeignKey('course.id'))
    def __init__(self,tname,tage):
        self.tname = tname
        self.tage = tage
    def __repr__(self):
        return "<Teacher%s>"%self.tname
class Course(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    cname = db.Column(db.String(30))
    teachers = db.relationship("Teacher",backref='course',lazy='dynamic')
    def __init__(self,cname):
        self.cname = cname
    def __repr__(self):
        return "<Course%s>"%self.cname
db.drop_all()
db.create_all()

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        uname = request.form.get('uname')
        uage = request.form.get('uage')
        uemail = request.form.get('uemail')
        user = Users(uname,uage,uemail)
        db.session.add(user)
        # db.session.commit()
    return 'regist success!'
if __name__ == "__main__":
    app.run(debug=True)