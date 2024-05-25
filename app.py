import os
import matplotlib.image as mpimg
from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO, send, join_room
from flask import Flask, flash, redirect, render_template, request, session, abort,url_for
import os
from flask import send_file
from werkzeug.utils import secure_filename
import sqlite3
import cartonify_on_image as image_cartoon
import img2sketch as img2sk
#import imagesmooth as ims
#import edgedetection as ed
from pathlib import Path
import cartonify_on_video as cvideo
import realtime as rc
import eyecartoon as eyec

UPLOAD_FOLDER = './input'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
socketio = SocketIO(app)
@app.route('/')
def index():
	if not session.get('logged_in'):
		return render_template("index.html")
	else:
		return render_template('home.html')
@app.route('/registerpage')
def reg_page():
    return render_template("register.html")
	
@app.route('/loginpage')
def log_page():
    return render_template("login.html")
@app.route('/imagepage')
def imagepage():
	return render_template("imagepage.html")
@app.route('/Videopage')
def Videopage():
	return render_template("videopage.html")
@app.route('/Realpage')
def Realpage():
	return render_template("real.html")

    
    
   
@app.route('/register',methods=['POST'])
def reg():
	name=request.form['name']
	username=request.form['username']
	password=request.form['password']
	email=request.form['emailid']
	mobile=request.form['mobile']
	conn= sqlite3.connect("Database")
	cmd="SELECT * FROM login WHERE username='"+username+"'"
	print(cmd)
	cursor=conn.execute(cmd)
	isRecordExist=0
	for row in cursor:
		isRecordExist=1
	if(isRecordExist==1):
	        print("Username Already Exists")
	        return render_template("usernameexist.html")
	else:
		print("insert")
		cmd="INSERT INTO login Values('"+str(name)+"','"+str(username)+"','"+str(password)+"','"+str(email)+"','"+str(mobile)+"')"
		print(cmd)
		print("Inserted Successfully")
		conn.execute(cmd)
		conn.commit()
		conn.close() 
		return render_template("inserted.html")
@app.route('/videoupload',methods=['GET','POST'])
def videoupload():
	if request.method=='POST':
		img = request.files['my_image']
		fname=img.filename
		fname=Path(fname).stem
		img_path = "static/vinput/" + img.filename
		outimg_path="static/video/" + fname+".avi"
		
		img.save(img_path)
		cvideo.process(img_path,fname)
		print("outimg_path==",outimg_path)
		return render_template("vresult.html",in_path=img_path,vout_path=outimg_path)

@app.route('/strartcamera',methods=['GET', 'POST'])
def strartcamera():
	if request.method=='POST':
		rc.process()
		return redirect(url_for('index'))
@app.route('/strartcamera1',methods=['GET', 'POST'])
def strartcamera1():
	if request.method=='POST':
		eyec.process()
		return redirect(url_for('index'))


@app.route('/imageupload',methods=['GET', 'POST'])	
def imageupload():
	if request.method=='POST':
                
                img = request.files['my_image']
                img_path = "static/input/" + img.filename
                outimg_path="static/output/" + img.filename
                sketchout_path="static/output_sketch/" + img.filename
                #Bilateral_path="static/Bilateral/"+img.filename
                #Median_path="static/Median/"+img.filename
                #Gaussian_path="static/Gaussian/"+img.filename
                #sobel_path="static/sobel/"+img.filename
                #canny_path="static/canny/"+img.filename
                fname=img.filename
                fname=Path(fname).stem
                img.save(img_path)
                #ims.process(img_path,fname)
                #ed.process(img_path,fname)
                image_cartoon.process(img_path,fname)
                img2sk.process(img_path,fname)
				
                print("outputimage path==",outimg_path)
                
                return render_template("result.html",msg="Cartoon Generated", inpath=img_path, out_path=outimg_path,sk_out=sketchout_path)

@app.route('/login',methods=['POST'])
def log_in():
	#complete login if name is not an empty string or doesnt corss with any names currently used across sessions
	if request.form['username'] != None and request.form['username'] != "" and request.form['password'] != None and request.form['password'] != "":
		username=request.form['username']
		password=request.form['password']
		conn= sqlite3.connect("Database")
		cmd="SELECT username,password FROM login WHERE username='"+username+"' and password='"+password+"'"
		print(cmd)
		cursor=conn.execute(cmd)
		isRecordExist=0
		for row in cursor:
			isRecordExist=1
		if(isRecordExist==1):
			session['logged_in'] = True
			# cross check names and see if name exists in current session
			session['username'] = request.form['username']
			print("session==",session['logged_in'] )
			return redirect(url_for('index'))

	return redirect(url_for('index'))
	
@app.route("/logout")
def log_out():
    session.clear()
    return render_template("login.html")




if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
