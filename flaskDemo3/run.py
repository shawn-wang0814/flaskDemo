from flask import Flask, render_template, request, make_response, redirect
import time
app = Flask(__name__,template_folder='t',static_url_path='/s/',static_folder='s')

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/request')
def request_views():
    scheme = request.scheme
    method = request.method
    args = request.args
    form = request.form
    values = request.values
    cookies = request.cookies
    headers = request.headers
    ua = request.headers['User-Agent']
    referer = request.headers.get('referer','')
    path = request.path
    files = request.files
    full_path = request.full_path
    url = request.url
    return render_template('02_request.html',params=locals())
@app.route('/get')
def request_scheme():
    return render_template('02-get.html',params = locals())
@app.route('/form_do')
def form_do():
    if request.method == "GET":
        uname = request.args.get('uname')
        upwd = request.args.get('upwd')
        print('username:%s,upwd:%s'%(uname,upwd))
    return 'get data successfully!'
@app.route('/post',methods=['POST','GET'])
def post_views():
    if request.method == 'GET':
        return render_template('02-post.html')
    else:
        uname = request.form.get('uname')
        upwd = request.form.get('upwd')
        uemail = request.form.get('uemail')
        realname = request.form.get('trueName')
        print('uname:%s,upwd:%s,uemail:%s,realname:%s' % (uname, upwd, uemail, realname))
    return redirect('/')
# @app.route('/post_do',methods=['POST','GET'])
# def post_do():
#     if request.method == 'POST':
#         uname = request.form.get('uname')
#         upwd = request.form.get('upwd')
#         uemail = request.form.get('uemail')
#         realname = request.form.get('trueName')
#         print('uname:%s,upwd:%s,uemail:%s,realname:%s'%(uname,upwd,uemail,realname))
#     return 'post data successfully!'

@app.route('/response')
def response_views():
    resp = make_response(render_template('02-post.html'))
    return resp


@app.route('/file',methods=['GET','POST'])
def file_views():
    if request.method=='GET':
        return render_template('02-file.html')
    else:
        f = request.files['uimg']
        filenames = f.filename
        list1= filenames.split('.')
        times = str(time.time())
        filename = times + '.' + list1[1]
        f.save('s/img/'+filename)
        return 'upload sucess!'
if __name__==('__main__'):
    app.run(debug=True)