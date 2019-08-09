from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:lw880814@localhost:3306/flask'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

class Mytest(db.Model):
    __tablename__ = 'mytest'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),unique=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.Boolean)
    email = db.Column(db.String(120),unique=True)
    def __init__(self,name,age,gender,email):
        self.name = name
        self.age = age
        self.gender = gender
        self.email = email
    def __repr__(self):
        return "<Mytest%s>"%self.name
class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer,primary_key=True)
    tname = db.Column(db.String(30))
    tage = db.Column(db.Integer)
    course_id = db.Column(db.Integer,db.ForeignKey('course.id'))
    def __init__(self,tname,tage):
        self.tname = tname
        self.tage = tage
class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer,primary_key=True)
    cname = db.Column(db.String(30),nullable=True)
    teacher = db.relationship('Teacher',backref=('course'),lazy='dynamic')
    def __init__(self,cname):
        self.cname = cname
class Students(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer,primary_key=True)
    sname = db.Column(db.String(80))
    sage = db.Column(db.Integer)
    def __init__(self,sname,sage):
        self.sname = sname
        self.sage = sage
# db.drop_all()
db.create_all()
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/register',methods=['GET',"POST"])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        name=request.form['uname']
        age = request.form['uage']
        if request.form['ugender'] == '男':
            gender = True
        else:
            gender = False
        email = request.form['uemail']
        users = Mytest(name,age,gender,email)
        db.session.add(users)
        return redirect('/')
@app.route('/query')
def query():
    users = db.session.query(Mytest).all()
    return render_template('query.html',params=locals())

@app.route('/delete')
def delete():
    id = request.args.get('uid')
    user = Mytest.query.filter_by(id=id).first()
    db.session.delete(user)
    url = request.headers.get('referer','/query')
    return redirect(url)

@app.route('/alter/',methods=['POST','GET'])
def alter():

    if request.method == "GET":
        id = request.args.get('uid')
        user = Mytest.query.filter_by(id=id).first()
        return render_template('alter.html',params=locals())
    else:
        id = request.form.get('uid')
        user = Mytest.query.filter_by(id=id).first()
        user.name = request.form.get('uname')
        user.age = request.form.get('uage')
        if request.form['ugender'] == '男':
            user.gender = True
        else:
            user.gender = False
        user.email = request.form.get('uemail')
        db.session.add(user)
        return redirect('/query')

@app.route('/add_course')
def add_course():
    course1 = Course('python基础')
    course2 = Course('Python高级')
    course3 = Course('Pythonweb基础')
    course4 = Course('Pythonweb开发')
    db.session.add(course1)
    db.session.add(course2)
    db.session.add(course3)
    db.session.add(course4)
    return 'add ok!'
@app.route('/add_teacher')
def add_teacher():
    teacher1 = Teacher('laowei',35)
    course = Course.query.filter_by(id=1).first()
    print(course)
    print(teacher1.course)
    teacher1.course = course
    db.session.add(teacher1)
    return 'add teacher ok!'
if __name__=='__main__':
    app.run(debug=True)