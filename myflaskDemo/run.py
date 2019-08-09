from flask import Flask, render_template, request, redirect, json
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
    pwd = db.Column(db.String(120))
    def __init__(self,name,gender,age,email,pwd):
        self.name = name
        self.gender = gender
        self.age = age
        self.email = email
        self.pwd = pwd


    def to_dict(self):
        dic = {
            'id': self.id,
            'uname': self.name,
            'ugender':self.gender,
            'uage': self.age,
            'uemail': self.email
        }
        return dic

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
    gender = db.Column(db.String(20))
    age = db.Column(db.Integer)
    course = db.relationship('Course',secondary='student_course',backref=db.backref('student',lazy='dynamic'),lazy='dynamic')
    courses = db.relationship(
        'Course',
        secondary='student_course',
        lazy='dynamic',
        backref=db.backref('students',lazy='dynamic')
    )
    def __init__(self,name,gender,age):
        self.name = name
        self.gender = gender
        self.age = age

<<<<<<< HEAD
# db.create_all()

=======
student_course = db.Table('student_course',
                          db.Column('id',db.Integer,primary_key=True),
                          db.Column('student_id',db.Integer,db.ForeignKey('student.id')),
                          db.Column('course_id',db.Integer,db.ForeignKey('course.id')))
db.drop_all()
db.create_all()
>>>>>>> fd5da3a3e2ce785f0cdfbbda704713d2b105b346

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
        pwd = request.form.get('upwd')
        user = User(name,gender,age,email,pwd)
        db.session.add(user)
        return redirect('/')
<<<<<<< HEAD

=======
>>>>>>> fd5da3a3e2ce785f0cdfbbda704713d2b105b346

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
@app.route('/add_student',methods=['GET','POST'])
def add_student():
    if request.method == 'GET':
        return render_template('add_student.html')
    else:
        name = request.form.get('sname')
        gender = request.form.get('sgender')
        age = request.form.get('sage')
        student = Student(name,gender,age)
        db.session.add(student)
        return redirect('/')
@app.route('/query_student')
def query_student():
    students = Student.query.all()
    return render_template('query_student.html',params=locals())

@app.route('/delete_student')
def delete_student():
    sname = request.args.get('sname')
    student = Student.query.filter_by(name=sname).first()
    db.session.delete(student)
    return redirect('/query_teacher')

@app.route('/alter_student',methods=['POST','GET'])
def alter_student():
    if request.method == 'GET':
        id = request.args.get('sid')
        student = Student.query.filter_by(id=id).first()
        return render_template('alter_student.html',params=locals())
    else:
        id = request.form.get('sid')
        student = Student.query.filter_by(id=id).first()
        student.name = request.form.get('sname')
        student.gender = request.form.get('sgender')
        student.age = request.form.get('sage')

        db.session.add(student)
        return redirect('/query_student')

@app.route('/add_student_course',methods=['GET','POST'])
def add_student_course():
    if request.method =='GET':
        student=Student.query.all()
        course = Course.query.all()
        return render_template('add_student_course.html',params=locals())
    else:
        sid = request.form.get('sid')
        cid = request.form.get('cid')
        stu = Student.query.filter_by(id=sid).first()
        cour = Course.query.filter_by(id=cid).first()
        stu.course.append(cour)
        db.session.add(stu)
        return redirect('/add_student_course')
@app.route('/query_student_course')

@app.route('/do_home')
def do_home():
    return redirect('/')


@app.route('/show_user')
def show_user():
    return render_template('show_user.html')


@app.route('/show_data')
def show_data():
    users = User.query.all()
    print(users)
    list_user = []
    for u in users:
        list_user.append(u.to_dict())
    print(list_user)
    return json.dumps(list_user)


@app.route('/01-user')
def user_view():
    return render_template('/01-user.html')


@app.route('/01-server')
def user_server():
    users = User.query.all()
    list_user = []
    for u in users:
        list_user.append(u.to_dict())
    return json.dumps(list_user)


if __name__=='__main__':
    app.run(debug=True)