from flask import render_template, request, redirect, url_for
#from flask_mysqldb import MySQL
import pymysql

registering = False
logging = False
errordict = {}

def home_page():
	global registering
	global logging
	logging = False
	registering = False
	if request.method == 'POST': 
		if 'register' in request.form:
			return validate_login_register(request.form,0)
		elif 'login' in request.form:
			return validate_login_register(request.form,1)

	
	return render_template("home.html", registering=False, logging=False, errordict={})
	

def about_page():
	global registering
	global logging
	logging = False
	registering = False
	if request.method == 'POST': 
		if 'register' in request.form:
			return validate_login_register(request.form,0)
		elif 'login' in request.form:
			return validate_login_register(request.form,1)

	return render_template("about.html",  registering=False, logging=False, errordict={})


def validate_login_register(form, loginFlag):
	errordict = {}
	global logging
	global registering
	if loginFlag == 1:
		#server.check_user()
		valid = True
		email = request.form.get("email")
		password = request.form.get("password")
		if email == "" or "@itu.edu.tr" not in email:
			valid = False
			errordict['loginmail'] = "e-mail is not valid"
		if password == "":
			valid = False 
			errordict['loginpassword'] = "password is not valid"
		if not valid:
			return render_template("home.html",  registering=registering, logging=True, errordict=errordict)
		else:
			con = pymysql.connect('localhost', 'root', 'graddbase123!', 'SPFGP')
			try:

				with con.cursor() as cur:
					cur.execute("SELECT PASSWORD FROM USER_TABLE WHERE EMAIL = " + "'" + email + "'")
					result = cur.fetchone()
					if not result:
						errordict['loginmail'] = "there is no registeration with that e-mail"
						return render_template("home.html",  registering=registering, logging=True, errordict=errordict)

					passwd = result[0]; 
					
					if passwd == password:
						print("login successfull")
					else:
						errordict['loginpassword'] = "wrong password"
						return render_template("home.html",  registering=registering, logging=True, errordict=errordict)

			finally:
			    con.close()

			logging = False
			return render_template("home.html",  registering=False, logging=False, errordict={})
	else:
		valid = True
		username = request.form.get("username")
		email = request.form.get("email")
		password = request.form.get("password")
		name = request.form.get("name")
		if name == "":
			valid = False
			errordict['regname'] = "name is not valid"
		if email == "" or email == "example@itu.edu.tr" or "@itu.edu.tr" not in email:
			valid = False
			errordict['regmail'] = "e-mail is not valid"
		if password == "":
			valid = False
			errordict['regpassword'] = "password is not valid"
		if username == "":
			valid = False
			errordict['regusername'] = "username is not valid"
		if not valid:
			return render_template("home.html",  registering=True, logging=logging, errordict=errordict)
		else:
			return render_template("home.html",  registering=False, logging=False, errordict={})











