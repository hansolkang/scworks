from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import Connection
from gridfs import GridFS
from werkzeug import secure_filename
from gridfs.errors import NoFile
import pymongo
import types
import os
#from pymongo.objectid import ObjectId

client = pymongo.MongoClient("localhost", 27017)
db = client.sharehouse
app = Flask(__name__)
app.config["SECRET_KEY"] = "5drfytguh23se5dr6ftugyw243e5d46rfted5r6yftugy5vd6rbft7gyn89"


class MongoGridFS:
  def __init__(self): pass
  def connect(self, host, port):
    if isinstance(port, types.StringType) == True:
      port = int(port)
    self.instanceConnection = Connection(host, port)
  def setDB(self, dbname):
    self.db = self.instanceConnection[dbname]
  def setGridFS(self, prefix = 'fs'):
    self.fs = GridFS(self.db, prefix)
  def put(self, data, **kwargs):
    self.fs.put(data, **kwargs)
  def get(self, filename):
    out = self.fs.get_last_version(filename)
    return out.read()
@app.route('/')
def hello_world():
    return 'hello world!'

@app.route('/user/<username>')
def show_user_profile(username):

    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' %post_id

@app.route('/logging')
def logging_test():
    test = 1;
    app.logger.debug('need debuging')
    app.logger.warning(str(test) + " line")
    app.logger.error('error ocur')
    return "finish logging"



@app.route('/sign')
def sign():
    return render_template('sign.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        if db.usr_info.find_one({"_id":request.form["ID"]}) is None:
            db.usr_info.insert({"_id":request.form["ID"], "password":request.form["password"],\
                                "Tel":request.form["Tel"], "name":request.form["name"],\
                                "gender":request.form["gender"]})
        else:
            return "id already exsist"
    else:
        return "worng access"
    return request.form["ID"] + "sign in"
   # return "asdf"
app.secret_key = 'asdqw12312easddser'

@app.route('/main/')
def main():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        temp = db.usr_info.find_one({"_id": request.form["ID"]})
        if temp is not None:
            print temp["password"] , type(temp["password"])
            print request.form["password"] , type(request.form["password"])
            if temp["password"] == request.form["password"]:
                session["ID"] = str(temp["_id"])
                session["login_status"] = True
                print session
                session['ID']
                return redirect(url_for('main'))
            else:
                return "wrong password"
        else:
            return "id doesn\'t exsist"
    else:
        return "worng access"
@app.route('/logout')
def logout():
    session["login_status"] = False
    return redirect(url_for('main'))

@app.route('/match')
def match():
    return render_template('match.html')

@app.route('/bulletinboard')
def bulletinboard():
    return render_template('bulletin_board.html')

@app.route('/bulletinboard/write')
def writebulletin():
    return render_template('write_bulletin_board.html')

@app.route('/bulletinboard/apply')
def bulletinapply():

    return None


@app.route('/view')
def view():
    return render_template('view.html')

@app.route('/list')
def list():
    return render_template('list.html')

@app.route('/writeboard')
def writeboard():
    return render_template('write_board.html')

@app.route('/writeboard/apply', methods=['POST'])
def apply():
    if request.method == "POST":
        #temp = db.houseboard.find_one({"_id": "index"})
        #index = int(temp["val"])
        #if temp is not None:
        db.houseboard.insert({"person_option" : request.form["person_option"],"contentTitle" : request.form["contentTitle"],"story": request.form["story"],"area_option1" : request.form["area_option1"],"gender": request.form["gender"],"age_option" : request.form["age_option"],"story" : request.form["story"],"match_info" : request.form["match_info"]})
        o = MongoGridFS()
        data = request.files['image']
        filename = data.filename
        o.connect('localhost', 27017)
        o.setDB('sharehouse')
        o.setGridFS()
        o.put(data, filename=filename)
        o.get(filename)
        return redirect(url_for('main'))
    else:
		return "worng access"

        #ret = o.get(image)
    #else:
     #   return "worng access"
    #return request.form["ID"] + "sign in"


        #return str(index)


if __name__ == '__main__':
    app.debug = True
    app.run()
