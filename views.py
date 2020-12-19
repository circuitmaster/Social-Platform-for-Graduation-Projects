from flask import render_template, request, redirect, url_for

registering = False
logging = False
errordict = {}

def home_page():
	print("home_page is rendered")
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
		email = request.form.get("email")
		password = request.form.get("password")
		if email!="" and password!="" and email!="example@itu.edu.tr" and password!="******":
			logging = False
			print("dolduruldu")
			return render_template("home.html",  registering=False, logging=False, errordict={})
		else:
			if email == "" or email == "example@itu.edu.tr" or "@itu.edu.tr" not in email:
				errordict['mail'] = "e-mail is not valid"
			if password == "":
				errordict['password'] = "password is not valid"
			logging = True	
			print("boş")
			#return redirect(home_page)
			return render_template("home.html",  registering=registering, logging=logging, errordict=errordict)
		print("logging in")
	else:
		valid = True
		username = request.form.get("username")
		email = request.form.get("email")
		password = request.form.get("password")
		name = request.form.get("name")
		if name == "":
			valid = False
			errordict['name'] = "name is not valid"
		if email == "" or email == "example@itu.edu.tr" or "@itu.edu.tr" not in email:
			valid = False
			errordict['mail'] = "e-mail is not valid"
		if password == "":
			valid = False
			errordict['password'] = "password is not valid"
		if username == "":
			valid = False
			errordict['username'] = "username is not valid"
		if not valid:
			registering = True
			return render_template("home.html",  registering=registering, logging=logging, errordict=errordict)
		else:
			return render_template("home.html",  registering=False, logging=False, errordict={})
		print("registering")











