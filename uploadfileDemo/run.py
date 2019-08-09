import datetime
import os

from flask import Flask, render_template, request

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/do_upload',methods=['GET','POST'])
def do_upload():
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        f = request.files['uimg']
        basedir = os.path.dirname(__file__)
        ext = f.filename.split('.')[1]
        strname = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        print(strname)
        fname = strname + '.' + ext
        filepath = os.path.join(basedir,'static/upload/',fname)
        f.save(filepath)
        return 'upload sucess!'
if __name__==('__main__'):
    app.run(debug=True,port=5000)