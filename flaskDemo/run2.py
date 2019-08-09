from flask import Flask,render_template
class Person(object):
    def __init__(self):
        self.name = None
    def say(self):
        return self.name+'is speaking!'

app = Flask(__name__)
@app.route('/')
def home():
    return '这是主页'

@app.route('/body')
def body():
    return render_template('02-body.html')
@app.route('/login')
def login():
    return '这是登录页面'

@app.route("/index")
def index():
    dic = {
        'name':'钢铁是怎样练成的',
        'author':'奥斯托洛夫斯基',
        "price":32.5,
        "pulisher":'北京大学出版社'
    }
    list1=['三国演义','红楼梦','西游记','水浒传']
    tup = ('郭富城','刘德华','张学友','黎明')
    person1 = Person()
    person1.name = '李四'
    dict = locals()
    print(dict)
    return render_template('index.html',params = dict)

if __name__=="__main__":
    app.run(debug=True)