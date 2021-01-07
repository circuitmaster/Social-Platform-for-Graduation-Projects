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

def logout():
	session.pop("user", None)
	return redirect(url_for('home_page'))

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

	#with open('photo.jpg', 'rb') as f:
	#	data = f.read()
	#data = pymysql.Binary(b"\x00\x01\x02")
	data1 = file1.read()
	data2 = file2.read()
	#print(data)

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
			#data = bytes(b'\x00\x01\x02')
			sql1 = "SELECT ID FROM DEPARTMENT_TABLE WHERE NAME=" + "'" + department + "'"
			cur.execute(sql1)
			result = cur.fetchone()
			#statement = "INSERT INTO PROJECT_TABLE(ID, TITLE, SUBJECT, STARTDATE, ENDDATE, PHOTO, NUMOFLIKES, SUMMARY, DETAILEDTEXT, VIDEO, DEPARTMENTID) VALUES (NULL, %s, %s, %s, %s, NULL, %d, %s, %s, NULL, %d)"
			#sql = "INSERT INTO PROJECT_TABLE(ID, TITLE, SUBJECT, STARTDATE, ENDDATE, PHOTO, NUMOFLIKES, SUMMARY, DETAILEDTEXT, VIDEO, DEPARTMENTID) VALUES (NULL, '%s', '%s', '%s', '%s',_binary '%s', '%d', '%s', '%s', NULL, '%d')" % (title, subject, start_date, end_date, (bytes(b'\x00\x01\x02'),), 0, summary, detailed, result[0])
			#tupp = (title, subject, start_date, end_date, 0, summary, detailed, result[0])
			#sql = """INSERT INTO PROJECT_TABLE(ID, TITLE, SUBJECT, STARTDATE, ENDDATE, PHOTO, NUMOFLIKES, SUMMARY, DETAILEDTEXT, VIDEO, DEPARTMENTID) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, NULL, ?)""",(title, subject, start_date, end_date, data, 0, summary, detailed, result[0])
			#cur.execute(sql)
			#cur.execute("insert into test_blob (PHOTO) values (_binary %s)", (data1,))
			cur.execute("INSERT INTO PROJECT_TABLE (ID, TITLE, SUBJECT, STARTDATE, ENDDATE, PHOTO, NUMOFLIKES, SUMMARY, DETAILEDTEXT, VIDEO, DEPARTMENTID) VALUES (NULL, %s, %s, %s, %s, _binary %s, 0, %s, %s, NULL, %s)", (title, subject, start_date, end_date, data1, summary, detailed, result[0]))
			#cur.execute("INSERT INTO DENEME (ID, NAME) VALUES (1, %s)", ("emre"))
			con.commit()
	except pymysql.Error as e:
		print("rolled back...", e)
		con.rollback()
	finally:
		con.close()

	print(title,subject,start_date,end_date,sep=" ")
	print("Project added successfully")

	return redirect(url_for('add_project'))










