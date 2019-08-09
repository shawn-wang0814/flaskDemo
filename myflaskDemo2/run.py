from flask import Flask, render_template, json, request
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:lw880814@localhost:3306/myflask'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)


class City(db.Model):
    __tablename__ = "city"
    id = db.Column(db.Integer,primary_key=True)
    pro_id = db.Column(db.Integer,db.ForeignKey("province.id"))
    name = db.Column(db.String(120),unique=True)

    def __init__(self,pro_id,name):
        self.pro_id = pro_id
        self.name = name

    def to_c_dict(self):
        c_dict={
            "cid": self.id,
            "cpid": self.pro_id,
            "cname": self.name
        }
        return c_dict


class Province(db.Model):
    __tablename__ = "province"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120),unique=True)

    def __init__(self,name):
        self.name = name

    def to_p_dict(self):
        p_dict = {
            "pid": self.id,
            "pname": self.name
        }
        return p_dict


db.create_all()


@app.route('/province')
def province():
    return render_template('province.html')


@app.route('/load_pro')
def load_pro():
    provinces = Province.query.all()
    list_pro = []
    for p in provinces:
        list_pro.append(p.to_p_dict())
    print(list_pro)
    return json.dumps(list_pro)


@app.route('/load_city')
def load_city():
    id = request.args.get('id')
    print("id:",id)
    citys = City.query.filter_by(pro_id=id).all()
    list_city = []
    for c in citys:
        list_city.append(c.to_c_dict())
    print(list_city)
    return json.dumps(list_city)

if __name__ =="__main__":
    app.run(debug=True)