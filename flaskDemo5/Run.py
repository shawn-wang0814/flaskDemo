from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import pymysql
from sqlalchemy import or_, text

pymysql.install_as_MySQLdb()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:lw880814@localhost:3306/flask"
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
db = SQLAlchemy(app)
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=True)
    age = db.Column(db.Integer)
    email = db.Column(db.String(120),unique=True)
    def __init__(self,username,age,email):
        self.username = username
        self.age = age
        self.email = email
    def __repr__(self):
        return "<Users:%s>"%self.username

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
    return redirect('/')

@app.route('/query')
def query():
    # datas = db.session.query(Users).all()
    # for u in datas:
    #     print(u.username,u.age,u.email)
    # theFirst = db.session.query(Users).filter(Users.username=='林志玲').first()
    # print(theFirst)
    # counts = db.session.query(Users).filter(Users.username=='林志玲').count()
    # print(counts)
    # # theLast = db.session.query(Users).last()
    # # print(theLast)
    # users1 = db.session.query(Users).filter(Users.age >18,Users.id>2).all()
    # print(users1)
    # theQuery = db.session.query(Users.username)
    # print(theQuery)
    users = db.session.query(Users).filter(or_(Users.age>18,Users.id<2)).all()
    print(users)

    users1 = db.session.query(Users).filter(Users.username.like('%e%')).all()
    print(users1)
    users2 = db.session.query(Users).filter_by(username='林志玲').first()
    print(users2)
    users3 = db.session.query(Users).limit(3).offset(1)
    print(users3)
    print(users3.all())
    # users4 = db.session.query(Users).order_by('id desc').all()
    users4 = db.session.query(Users).order_by(Users.id.desc(),Users.age.asc()).all()
    # users4 = db.session.query(Users).order_by(text('id desc,age asc')).all()
    print(users4)
    users5 = db.session.query(Users).group_by('age')
    print(users5)
    users6 = Users.query.filter(Users.id>3).all()
    print(users6)
    return 'query ok!'
@app.route('/query_all')
def query_all():
    users = db.session.query(Users).all()

    return render_template('query_all.html',params=locals())
# @app.route('/query_by_id/<int:id>',)
# def query_by_id(id):
#     user = db.session.query(Users).filter_by(id=id).first()
#     # uname = request.args.get('uname')
#     # print(uname)
#     params = locals()
#     print(params)
#     return render_template('select.html',params=locals())

@app.route('/query_by_id')
def query_by_id():
    id = request.args.get('id')
    user = db.session.query(Users).filter_by(id=id).first()
    return render_template('select.html',params = locals())

@app.route('/delete')
def delete():
    uname = request.args.get('uname')
    user = db.session.query(Users).filter(Users.username==uname).first()
    db.session.delete(user)
    url = request.headers.get('referer','/query_all')
    return redirect(url)

@app.route('/alter',methods=['GET','POST'])
def alter():
    if request.method == 'GET':
        uname = request.args.get('uname')
        print(uname)
        user = Users.query.filter_by(username=uname).first()
        return render_template('change.html',params=locals())
    else:
        id = request.form.get('uid')
        user = Users.query.filter_by(id=id).first()
        user.username = request.form.get('uname')
        user.age = request.form.get('uage')
        user.email = request.form.get('uemail')
        db.session.add(user)
        # url = request.headers.get('referer','/query_all')
        return redirect('/query_all')
if __name__ == '__main__':
    app.run(debug=True)