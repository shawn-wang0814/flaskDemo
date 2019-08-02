from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:lw880814@localhost:3306/myflask'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),unique=True)
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    email = db.Column(db.String(120))
    def __init__(self,name,gender,age,email):
        self.name = name
        self.gender = gender
        self.age = age
        self.email = email

class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    gender = db.Column(db.String(30))
    age = db.Column(db.Integer)
    email = db.Column(db.String(120))
    course_id = db.Column(db.Integer,db.ForeignKey('course.id'))
    def __init__(self,name,gender,age,email):
        self.name = name
        self.gender = gender
        self.age = age
        self.email = email
class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),unique=True)
    times = db.Column(db.Integer)
    teacher = db.relationship('Teacher',backref='course',lazy='dynamic')
    def __init__(self,name,times):
        self.name = name
        self.times = times

class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    def __init__(self,name,age):
        self.name = name
        self.age = age

db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        name = request.form.get('uname')
        gender = request.form.get('ugender')
        age = request.form.get('uage')
        email = request.form.get('uemail')
        user = User(name,gender,age,email)
        db.session.add(user)
        return render_template('/')

@app.route('/query_user')
def query_user():
    users = User.query.all()
    return render_template('query_user.html',params=locals())

@app.route('/delete_user')
def delete_user():
    name = request.args.get('uname')
    user = User.query.filter_by(name=name).first()
    db.session.delete(user)
    return redirect('/query_user')

@app.route('/alter_user',methods=['POST','GET'])
def alter_user():
    name = request.args.get('uname')
    user = User.query.filter_by(name=name).first()
    if request.method == 'GET':
        return render_template('alter_user.html',params=locals())
    else:
        name = request.form.get('uname')
        gender = request.form.get('ugender')
        age = request.form.get('uage')
        email = request.form.get('uemail')
        user = User(name,gender,age,email)
        db.session.add(user)
        return redirect('/query_user')

@app.route('/add_teacher',methods=['POST','GET'])
def add_teacher():
    if request.method == 'GET':
        course = Course.query.all()
        return render_template('add_teacher.html',params=locals())
    else:
        name = request.form.get('tname')
        gender = request.form.get('tgender')
        age = request.form.get('tage')
        email = request.form.get('temail')
        course_name = request.form.get('course_name')
        course = Course.query.filter_by(name=course_name).first()
        teacher = Teacher(name,gender,age,email)
        teacher.course_id = course.id
        db.session.add(teacher)
        return redirect('/query_teacher')

@app.route('/query_teacher')
def query_teacher():
    teachers = Teacher.query.all()
    return render_template('query_teacher.html',params=locals())

@app.route('/alter_teacher',methods=['POST','GET'])
def alter_teacher():
    if request.method == 'GET':
        id = request.args.get('tid')
        teacher = Teacher.query.filter_by(id=id).first()
        course = Course.query.all()
        return render_template('alter_teacher.html',params=locals())
    else:
        id = request.form.get('tid')
        teacher = Teacher.query.filter_by(id=id).first()
        teacher.name = request.form.get('tname')
        teacher.gender = request.form.get('tgender')
        teacher.age = request.form.get('tage')
        teacher.email = request.form.get('temail')
        cname = request.form.get('course_name')
        course = Course.query.filter_by(name=cname).first()
        teacher.course = course
        db.session.add(teacher)
        return redirect('/query_teacher')

@app.route('/delete_teacher')
def delete_teacher():
    tname = request.args.get('tname')
    teacher = Teacher.query.filter_by(name=tname).first()
    db.session.delete(teacher)
    return redirect('/query_teacher')

@app.route('/add_course',methods=['POST','GET'])
def add_course():
    if request.method == 'GET':
        return render_template('add_course.html')
    else:
        cname = request.form.get('cname')
        ctime = request.form.get('ctime')
        course = Course(cname,ctime)
        db.session.add(course)
        return redirect('/')

@app.route('/query_course')
def query_course():
    courses = Course.query.all()
    print(courses)
    return render_template('query_course.html',params=locals())

@app.route('/delete_course')
def delete_course():
    id = request.args.get('cid')
    course = Course.query.filter_by(id=id).first()
    db.session.delete(course)
    return redirect('query_course')

@app.route('/alter_course',methods=['GET','POST'])
def alter_course():
    
    if request.method == 'GET':
        id = request.args.get('cid')
        course = Course.query.filter_by(id=id)
        print(locals())
        return render_template('alter_course.html',params=locals())
    else:
        id = request.form.get('cid')
        print(id)
        course = Course.query.filter_by(id=id).first()
        print(course)
        course.name = request.form.get('cname')
        course.times = request.form.get('ctime')
        db.session.add(course)
        return redirect('/query_course')


@app.route('/do_home')
def do_home():
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True)