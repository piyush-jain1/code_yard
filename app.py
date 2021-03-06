from flask import Flask,request,render_template,session,redirect,url_for,escape
import requests
import json
import re
import os, os.path

from simulate import simulate_module

app = Flask(__name__)
app.register_blueprint(simulate_module)

@app.route('/', methods=['GET'])
def index():
	if request.method == 'GET':
		if 'username' in session:
			return redirect(url_for('dashboard'))
		else:
			return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
	if 'username' in session:
		return redirect(url_for('dashboard'))
	else:
		if request.method == 'GET':
			return render_template('login.html')
		elif request.method == 'POST':
			login_username = request.form['username']
			login_password = request.form['password']
			if re.match(r'^team\d\d$',login_username)!=None and re.match(r'^\d{4}$',login_password)!=None:
				team_number = int(login_username[4:6])
				team_password = (1234+7383*team_number)%10000
				if team_password==int(login_password):
					session['username'] = request.form['username']
					session['done'] = [0,0,0,0,0,0]
					session['unlock'] = 0
					directory = 'codes/'+session['username']
					if not os.path.exists(directory):
						print "not exists"
						os.makedirs(directory)
						for i in range(1,7):
							os.makedirs(directory+'/q'+str(i))
					return url_for("dashboard", _external=True)
			return url_for("login", _external=True)

@app.route('/dashboard', methods=['GET'])
def dashboard():
	if 'username' not in session:
		return redirect(url_for('login'))
	else:
		if request.method == 'GET':
			return render_template('dashboard.html')

@app.route('/submit', methods=['POST'])
def submit_code():
	code = request.form['code']
	which = request.form['which']
	session['done'][int(which)-1] = 1
	unlock = 1
	for i in range(3):
		if session['done'][i] == 0:
			unlock = 0
			break
	session['unlock'] = unlock
	dir_name = 'codes/'+session['username']+'/q'+which
	num_files = len([name for name in os.listdir(dir_name) if os.path.isfile(name)])
	filename = code+str(num_files)+'.pj'
	f = open(dir_name+'/'+filename,'w')
	f.write(code)
	f.close()
	return 'Submission Number: ' + str(num_files+1) + '\nCongratulation! Your code has been submitted\nIf possible you may try a more optimized approach for more marks'

@app.route('/bonus', methods=['GET'])
def  bonus():
	if(session['unlock'] == 1):
		return render_template('bonus.html')
	else:
		return "You are not yet there!"

@app.route('/logout', methods=['GET'])
def logout():
	session.pop('username', None)
	return redirect(url_for('login'))

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5000,debug=True)