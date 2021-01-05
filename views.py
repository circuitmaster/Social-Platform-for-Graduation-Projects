from flask import render_template, request, redirect, url_for, session
import pymysql

registering = False
logging = False
errordict = {}

def home_page():
	global registering
	global logging
	logging = False
	registering = False
	con = pymysql.connect('localhost', 'root', 'graddbase123!', 'SPFGP')
	try:
		with con.cursor() as cur:
			cur.execute("SELECT NAME FROM DEPARTMENT_TABLE")
			result = cur.fetchone()
			print(result, type(result))
	finally:
		con.close()
	if request.method == 'POST': 
		if 'register' in request.form:
			return validate_login_register(request.form,0)
		elif 'login' in request.form:
			return validate_login_register(request.form,1)

	
	return render_template("home.html", registering=False, logging=False, errordict={}, departments=result)
	

def about_page():
	global registering
	global logging
	logging = False
	registering = False
	con = pymysql.connect('localhost', 'root', 'graddbase123!', 'SPFGP')
	try:
		with con.cursor() as cur:
			cur.execute("SELECT NAME FROM DEPARTMENT_TABLE")
			result = cur.fetchone()
			print(result, type(result))
	finally:
		con.close()
	if request.method == 'POST': 
		if 'register' in request.form:
			return validate_login_register(request.form,0)
		elif 'login' in request.form:
			return validate_login_register(request.form,1)

	return render_template("about.html",  registering=False, logging=False, errordict={}, departments=result)


def validate_login_register(form, loginFlag):
	errordict = {}
	global logging
	global registering
	if loginFlag == 1:
		valid = True
		user = request.form.get("username")
		password = request.form.get("password")
		if user == "":
			valid = False
			errordict['loginuser'] = "username is not valid"
		if password == "":
			valid = False 
			errordict['loginpassword'] = "password is not valid"
		if not valid:
			return render_template("home.html",  registering=registering, logging=True, errordict=errordict)
		else:
			con = pymysql.connect('localhost', 'root', 'graddbase123!', 'SPFGP')
			try:

				with con.cursor() as cur:
					cur.execute("SELECT PASSWORD, ROLE FROM USER_TABLE WHERE USERNAME = " + "'" + user + "'")
					result = cur.fetchone()
					if not result:
						errordict['loginuser'] = "there is no registeration with that username"
						return render_template("home.html",  registering=registering, logging=True, errordict=errordict)

					passwd = result[0];
					role = result[1];
					
					if passwd == password:
						print("login successfull")
					else:
						errordict['loginpassword'] = "wrong password"
						return render_template("home.html",  registering=registering, logging=True, errordict=errordict)

			finally:
			    con.close()

			logging = False
			session["user"] = user
			session["role"] = role
			return render_template("home.html",  registering=False, logging=False, errordict={})
	else:
		valid = True
		role = request.form['question']
		department = request.form['department']
		username = request.form.get("username")
		email = request.form.get("email")
		password = request.form.get("password")
		name = request.form.get("name")
		surname = request.form.get("surname")
		if name == "":
			valid = False
			errordict['regname'] = "name is not valid"
		if surname == "":
			valid = False
			errordict['regsurname'] = "surname is not valid"
		if email == "" or "@itu.edu.tr" not in email:
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
			con = pymysql.connect('localhost', 'root', 'graddbase123!', 'SPFGP')

			try:
				with con.cursor() as cur:
					cur.execute("SELECT * FROM USER_TABLE WHERE USERNAME=" + "'" + username + "'")
					result = cur.fetchone()
					if result:
						errordict['regusername'] = "this username already exists, choose another"
						return render_template("home.html",  registering=True, logging=False, errordict=errordict)
					sql1 = "SELECT ID FROM DEPARTMENT_TABLE WHERE NAME=" + "'" + department + "'"
					cur.execute(sql1)
					result = cur.fetchone()
					sql = "INSERT INTO USER_TABLE(ID, USERNAME, PASSWORD, NAME, SURNAME, EMAIL, PHOTO, ROLE, DEPARTMENTID) VALUES (NULL, '%s', '%s', '%s', '%s', '%s', NULL, '%s', '%d')" % (username, password, name, surname, email, role, result[0])
					cur.execute(sql)
					con.commit()
			except:
				con.rollback()
			finally:
				con.close();
			print("registration successfull")
			return render_template("home.html",  registering=False, logging=False, errordict={})

def user_page():
	return render_template("user.html", errordict={})

def add_project():
	return render_template("add_project.html", errordict={})

def logout():
	session.pop("user", None)
	return redirect(url_for('home_page'))











