from flask import render_template, request, redirect, url_for, session
import pymysql
import base64

# control variables --> unused currently but preferably can be used
registering = False
logging = False
# dictionary that holds error texts
errordict = {}

def home_page():
	global registering
	global logging
	logging = False
	registering = False
	con = pymysql.connect('localhost', 'root', 'graddbase123!', 'SPFGP')
	try:
		with con.cursor() as cur:
			# for sign up form get department names
			cur.execute("SELECT NAME FROM DEPARTMENT_TABLE") 
			result = cur.fetchone()
			print(result, type(result))
	finally:
		con.close()
	if request.method == 'POST': 
		if 'register' in request.form:
			return validate_login_register(request.form,0,result)
		elif 'login' in request.form:
			return validate_login_register(request.form,1,result)

	
	return render_template("home.html", registering=False, logging=False, errordict={}, departments=result)
	

def about_page():
	global registering
	global logging
	logging = False
	registering = False
	con = pymysql.connect('localhost', 'root', 'graddbase123!', 'SPFGP')
	try:
		with con.cursor() as cur:
			# for sign up form get department names
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

# function that handles validation of the login and register forms 
def validate_login_register(form, loginFlag, dep):
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
			# if user enters inavlid info redirected to same page with error msgs
			return render_template("home.html",  registering=registering, logging=True, errordict=errordict, departments=dep)
		else:
			con = pymysql.connect('localhost', 'root', 'graddbase123!', 'SPFGP')
			try:

				with con.cursor() as cur:
					cur.execute("SELECT PASSWORD, ROLE FROM USER_TABLE WHERE USERNAME = " + "'" + user + "'")
					result = cur.fetchone()
					if not result:
						errordict['loginuser'] = "there is no registeration with that username"
						return render_template("home.html",  registering=registering, logging=True, errordict=errordict, departments=dep)

					passwd = result[0];
					role = result[1];
					
					if passwd == password:
						print("login successfull")
					else:
						errordict['loginpassword'] = "wrong password"
						return render_template("home.html",  registering=registering, logging=True, errordict=errordict, departments=dep)

			finally:
			    con.close()

			logging = False
			session["user"] = user
			session["role"] = role
			# if logged in succesfully redirect to home page
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
			# if user enters inavlid info redirected to same page with error msgs
			return render_template("home.html",  registering=True, logging=logging, errordict=errordict, departments=dep)
		else:
			con = pymysql.connect('localhost', 'root', 'graddbase123!', 'SPFGP')

			try:
				with con.cursor() as cur:
					cur.execute("SELECT * FROM USER_TABLE WHERE USERNAME=" + "'" + username + "'")
					result = cur.fetchone()
					if result:
						errordict['regusername'] = "this username already exists, choose another"
						return render_template("home.html",  registering=True, logging=False, errordict=errordict, departments=dep)
					sql1 = "SELECT ID FROM DEPARTMENT_TABLE WHERE NAME=" + "'" + department + "'"
					cur.execute(sql1)
					result = cur.fetchone()
					sql = "INSERT INTO USER_TABLE(ID, USERNAME, PASSWORD, NAME, SURNAME, EMAIL, PHOTO, ROLE, DEPARTMENTID) VALUES (NULL, '%s', '%s', '%s', '%s', '%s', NULL, '%s', '%d')" % (username, password, name, surname, email, role, result[0])
					cur.execute(sql)
					con.commit()
			except:
				con.rollback()
			finally:
				con.close()
			print("registration successfull")
			# if registered succesfully redirect to home page
			return render_template("home.html",  registering=False, logging=False, errordict={})

def user_page():
	return render_template("user.html", errordict={})

def add_project():
	con = pymysql.connect('localhost', 'root', 'graddbase123!', 'SPFGP')
	try:
		with con.cursor() as cur:
			cur.execute("SELECT NAME FROM DEPARTMENT_TABLE")
			result = cur.fetchone()
			print(result, type(result))
	finally:
		con.close()
	if request.method == 'POST': 
		return validate_add_proj_form(request.form, result)
	return render_template("add_project.html", errordict={}, departments=result)

# logout function
def logout():
	session.pop("user", None)
	return redirect(url_for('home_page'))

# function that handles validation of the add project form
def validate_add_proj_form(form, dep):
	errordict = {}
	title = form.get("title")
	subject = form.get("subject")
	start_date = form.get("date1")
	end_date = form.get("date2")
	summary = form.get("summary")
	detailed = form.get("dtext")
	department = request.form['department']

	valid = True

	file1 = request.files['img']
	file2 = request.files['video']

	# binary data of the photo and video
	data1 = file1.read()
	data2 = file2.read()

	if title == "":
		valid = False
		errordict['title'] = "title can not be empty"
	if subject == "":
		valid = False
		errordict['subject'] = "subject can not be empty"
	if summary == "":
		valid = False
		errordict['summary'] = "summary can not be empty"
	if detailed == "":
		valid = False
		errordict['detailed'] = "detailed text can not be empty"
	if not valid:
		return render_template("add_project.html", errordict=errordict, departments=dep)

	con = pymysql.connect('localhost', 'root', 'graddbase123!', 'SPFGP')

	try:
		with con.cursor() as cur:
			sql1 = "SELECT ID FROM DEPARTMENT_TABLE WHERE NAME=" + "'" + department + "'"
			cur.execute(sql1)
			result = cur.fetchone()
			# photo is inserted as binary large object file to database
			cur.execute("INSERT INTO PROJECT_TABLE (ID, TITLE, SUBJECT, STARTDATE, ENDDATE, PHOTO, NUMOFLIKES, SUMMARY, DETAILEDTEXT, VIDEO, DEPARTMENTID) VALUES (NULL, %s, %s, %s, %s, _binary %s, 0, %s, %s, NULL, %s)", (title, subject, start_date, end_date, data1, summary, detailed, result[0]))
			con.commit()
	except pymysql.Error as e:
		print("rolled back...", e)
		con.rollback()
	finally:
		con.close()

	print(title,subject,start_date,end_date,sep=" ")
	print("Project added successfully")

	return redirect(url_for('add_project'))

# function of the profile pages of the projects
def project(prj_id):
	con = pymysql.connect('localhost', 'root', 'graddbase123!', 'SPFGP')
	try:
		with con.cursor() as cur:
			sql = "SELECT TITLE, SUBJECT, STARTDATE, ENDDATE, NUMOFLIKES, SUMMARY, DETAILEDTEXT, PHOTO FROM PROJECT_TABLE WHERE ID=" + "'" + prj_id + "'"
			cur.execute(sql)
			result = cur.fetchone()
			# retrieve image to html with base64 encoding
			encoded = base64.b64encode(result[7])
			displayable = str(encoded)

	finally:
		con.close()
	return render_template("project.html", title=result[0], subject=result[1], start_date=result[2], end_date=result[3], num_of_likes=result[4], summary=result[5], detailed=result[6], errordict={}, d=displayable[2:-1])




























