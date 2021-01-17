from flask import render_template, request, redirect, url_for, session, jsonify
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
			result = cur.fetchall()
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
			result = cur.fetchall()
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
			# opening session
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
					result2 = con.insert_id()
					print(result2)
					if role == "student":
						print(role)
						sql3 = "INSERT INTO STUDENT_TABLE(ID, USER_ID) VALUES (NULL, '%d')" % (result2)
						cur.execute(sql3)
					else:
						sql3 = "INSERT INTO PROFESSOR_TABLE(ID, USER_ID) VALUES (NULL, '%d')" % (result2)
						cur.execute(sql3)
					con.commit()
			except:
				print("exception occured registering")
				con.rollback()
			finally:
				con.close()
			print("registration successfull")
			# if registered succesfully redirect to home page
			return render_template("home.html",  registering=False, logging=False, errordict={}, departments=dep)
# function of the user page
def user_page():
	errordict = {}
	con = pymysql.connect('localhost', 'root', 'graddbase123!', 'SPFGP')
	try:
		with con.cursor() as cur:
			# to change department we need department names
			cur.execute("SELECT NAME FROM DEPARTMENT_TABLE") 
			deps = cur.fetchall()
			sql = "SELECT PHOTO FROM USER_TABLE WHERE USERNAME=" + "'" + session['user'] + "'"
			cur.execute(sql)
			result = cur.fetchone()
			displayable = None
			# retrieve image to html with base64 encoding
			if result[0] != None: 
				encoded = base64.b64encode(result[0])
				displayable = str(encoded)
			#print(result, type(result))
	finally:
		con.close()
	if request.method == 'POST':
		errordict = {}
		new_username = request.form.get('user')
		new_password = request.form.get('password')
		email = request.form.get("email")
		courses = request.form.getlist("course")
		grades = request.form.getlist("grade")
		department = request.form['department']
		file1 = request.files['img']

		# binary data of the photo
		data1 = file1.read()

		valid = True

		if session['user'] == new_username:
			errordict['user'] = "new username is same as current username"
			valid = False

		if "@itu.edu.tr" not in email:
			errordict['regmail'] = "email is not valid"
			valid = False

		if len(courses) != 0:
			for g in grades:
				if g.lower() not in ["aa", "ba", "bb", "cb", "cc", "dc", "dd", "ff"]:
					errordict['noc'] = "some of the grades are not valid"
					valid = False
					break

		if not valid:
			if displayable != None:
				return render_template("user.html", errordict=errordict, departments=deps, d=displayable[2:-1])
			else:
				return render_template("user.html", errordict=errordict, departments=deps, d=None)

		con = pymysql.connect('localhost', 'root', 'graddbase123!', 'SPFGP')

		try:
			with con.cursor() as cur:
				sql = "SELECT ID FROM USER_TABLE WHERE USERNAME=" + "'" + session['user'] + "'"
				cur.execute(sql)
				result = cur.fetchone()
				sqll = "SELECT ID FROM STUDENT_TABLE WHERE USER_ID=" + "'" + str(result[0]) + "'"
				cur.execute(sqll)
				resultt = cur.fetchone()
				if len(new_username) != 0:
					control_sql = "SELECT ID FROM USER_TABLE WHERE USERNAME=" + "'" + new_username + "'"
					cur.execute(control_sql)
					ress = cur.fetchone()
					if ress == None:	
						sql1 = "UPDATE USER_TABLE SET USERNAME=" + "'" + new_username + "'" + " WHERE ID=" + "'" + str(result[0]) + "'"
						cur.execute(sql1)
					else:
						errordict['user'] = "this username already exists"
						if displayable != None:
							return render_template("user.html", errordict=errordict, departments=deps, d=displayable[2:-1])
						else:
							return render_template("user.html", errordict=errordict, departments=deps, d=None)
				if len(new_password) != 0:
					sql1 = "UPDATE USER_TABLE SET PASSWORD=" + "'" + new_password + "'" + " WHERE ID=" + "'" + str(result[0]) + "'"
					cur.execute(sql1)
				if len(email) != 0:
					sql1 = "UPDATE USER_TABLE SET EMAIL=" + "'" + email + "'" + " WHERE ID=" + "'" + str(result[0]) + "'"
					cur.execute(sql1)
				# add or update the profile photo
				cur.execute("UPDATE USER_TABLE SET PHOTO= _binary %s WHERE ID= %s",(data1, result[0]))
				sql1 = "SELECT ID FROM DEPARTMENT_TABLE WHERE NAME=" + "'" + department + "'"
				cur.execute(sql1)
				result2 = cur.fetchone()
				print(result2)
				if result2 != None:
					sqldep = "UPDATE USER_TABLE SET DEPARTMENTID=" + "'" + str(result2[0]) + "'" + " WHERE ID=" + "'" + str(result[0]) + "'"
					cur.execute(sqldep)
				i = 0
				for c in courses:
					print(c)
					sql1 = "SELECT ID FROM COURSE_TABLE WHERE COURSENAME=" + "'" + c + "'"
					cur.execute(sql1)
					res = cur.fetchone()
					print(res)
					sql2 = "SELECT ID FROM COURSE_GRADE_TABLE WHERE STUDENTID=" + "'" + str(resultt[0]) + "'" + " AND COURSEID=" + "'" + str(res[0]) + "'"
					cur.execute(sql2)
					res2 = cur.fetchone()
					if res2 == None:
						sql3 = "INSERT INTO COURSE_GRADE_TABLE(ID, STUDENTID, COURSEID, GRADE) VALUES (NULL, '%d', '%d', '%s')" % (resultt[0], res[0], grades[i])
						cur.execute(sql3)
					else:
						sql3 = "UPDATE COURSE_GRADE_TABLE SET GRADE=" + "'" + grades[i] + "'" + " WHERE ID=" + "'" + str(res2[0]) + "'"
						cur.execute(sql3)
					i += 1
				
				con.commit()
				session['user'] = new_username
		except pymysql.Error as e:
			print("rolled back...", e)
			con.rollback()
		finally:
			con.close()
		print("Datas updated successfully")

		if displayable != None:
			return render_template("user.html", errordict={}, departments=deps, d=displayable[2:-1])
		else:
			return render_template("user.html", errordict={}, departments=deps, d=None)
	
	if displayable != None:
		return render_template("user.html", errordict={}, departments=deps, d=displayable[2:-1])
	else:
		return render_template("user.html", errordict={}, departments=deps, d=None)


def add_project():
	if ('role' not in session.keys()) or session['role'] != 'professor' and session['role'] != 'admin':
		return redirect(url_for('home_page'))
	con = pymysql.connect('localhost', 'root', 'graddbase123!', 'SPFGP')
	try:
		with con.cursor() as cur:
			cur.execute("SELECT NAME FROM DEPARTMENT_TABLE")
			result = cur.fetchall()
			print(result, type(result))
	finally:
		con.close()
	if request.method == 'POST': 
		return validate_add_proj_form(request.form, result)
	return render_template("add_project.html", errordict={}, departments=result)

# logout function
def logout():
	session.pop("user", None)
	session.pop("role", None)
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
	students = form.getlist("contributer")
	reqs = form.getlist("prerequisite")
	department = request.form['department']

	print(students)
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
	if len(students) == 0:
		valid = False
		errordict['nos'] = "Project must include at least one student!"
	if not valid:
		return render_template("add_project.html", errordict=errordict, departments=dep)

	con = pymysql.connect('localhost', 'root', 'graddbase123!', 'SPFGP')

	try:
		with con.cursor() as cur:
			sql1 = "SELECT ID FROM DEPARTMENT_TABLE WHERE NAME=" + "'" + department + "'"
			cur.execute(sql1)
			result = cur.fetchone()
			# photo is inserted as binary large object file to database
			cur.execute("INSERT INTO PROJECT_TABLE(ID, TITLE, SUBJECT, STARTDATE, ENDDATE, PHOTO, NUMOFLIKES, SUMMARY, DETAILEDTEXT, VIDEO, DEPARTMENTID) VALUES (NULL, %s, %s, %s, %s, _binary %s, 0, %s, %s, NULL, %s)", (title, subject, start_date, end_date, data1, summary, detailed, result[0]))
			result2 = con.insert_id()
			sql2 = "SELECT p.ID FROM USER_TABLE u INNER JOIN PROFESSOR_TABLE p ON p.USER_ID = u.ID WHERE u.USERNAME=" + "'" + session["user"] + "'"
			cur.execute(sql2)
			result3 = cur.fetchone()
			print(result3)
			sql3 = "INSERT INTO PROJECT_MANAGER_TABLE(ID, PROFESSORID, PROJECTID) VALUES (NULL, '%d', '%d')" % (result3[0], result2)
			cur.execute(sql3)
			for s in students:
				sql4 = "INSERT INTO PROJECT_MEMBER_TABLE(ID, STUDENTID, PROJECTID) VALUES (NULL, '%d', '%d')" % (int(s), result2)
				cur.execute(sql4)
			for c in reqs:
				sql5 = "SELECT ID FROM COURSE_TABLE WHERE COURSENAME=" + "'" + c + "'"
				cur.execute(sql5)
				res = cur.fetchone()
				sql6 = "INSERT INTO COURSE_REQ_TABLE(ID, PROJECTID, COURSEID) VALUES (NULL, '%d', '%d')" % (result2, res[0])
				cur.execute(sql6)
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
	print(prj_id)
	con = pymysql.connect('localhost', 'root', 'graddbase123!', 'SPFGP')
	try:
		with con.cursor() as cur:
			sql = "SELECT TITLE, SUBJECT, STARTDATE, ENDDATE, NUMOFLIKES, SUMMARY, DETAILEDTEXT, PHOTO FROM PROJECT_TABLE WHERE ID=" + "'" + prj_id + "'"
			cur.execute(sql)
			result = cur.fetchone()
			# retrieve image to html with base64 encoding
			if result[7] != None: 
				encoded = base64.b64encode(result[7])
				displayable = str(encoded)

	finally:
		con.close()

	return render_template("project.html", title=result[0], subject=result[1], start_date=result[2], end_date=result[3], num_of_likes=result[4], summary=result[5], detailed=result[6], errordict={}, d=displayable[2:-1])

# function for livesearch
def livesearch(search_pattern):
	print(search_pattern)

	seach_val = request.form.get("text")
	con = pymysql.connect('localhost', 'root', 'graddbase123!', 'SPFGP')
	try:
		with con.cursor() as cur:
			if search_pattern == "all":
				query = "SELECT ID, TITLE FROM PROJECT_TABLE WHERE TITLE LIKE '%s'" % seach_val
				cur.execute(query)
				result = cur.fetchall()
			elif search_pattern == "name":
				query = "SELECT ID, TITLE FROM PROJECT_TABLE WHERE TITLE LIKE '%s'" % seach_val
				cur.execute(query)
				result = cur.fetchall()
			elif search_pattern == "cont":
				query = "SELECT ID, TITLE FROM PROJECT_TABLE WHERE TITLE LIKE '%s'" % seach_val
				cur.execute(query)
				result = cur.fetchall()
			elif search_pattern == "year":
				query = "SELECT ID, TITLE FROM PROJECT_TABLE WHERE STARTDATE LIKE '%s'" % seach_val
				cur.execute(query)
				result = cur.fetchall()
			elif search_pattern == "dep":
				query = "SELECT ID, TITLE FROM PROJECT_TABLE WHERE TITLE LIKE '%s'" % seach_val
				cur.execute(query)
				result = cur.fetchall()
			elif search_pattern == "fac":
				query = "SELECT ID, TITLE FROM PROJECT_TABLE WHERE TITLE LIKE '%s'" % seach_val
				cur.execute(query)
				result = cur.fetchall()
			elif search_pattern == "sub":
				query = "SELECT ID, TITLE FROM PROJECT_TABLE WHERE SUBJECT LIKE '%s'" % seach_val
				cur.execute(query)
				result = cur.fetchall()
			
	finally:
		con.close()
	return jsonify(result)

























