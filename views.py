from flask import render_template, request


def home_page():
	if request.method == 'POST': 
		if 'register' in request.form:
			validate_login_register(request.form,0)
		elif 'login' in request.form:
			validate_login_register(request.form,1)
	
	return render_template("home.html")
	

def about_page():
	if request.method == 'POST': 
		if 'register' in request.form:
			validate_login_register(request.form,0)
		elif 'login' in request.form:
			validate_login_register(request.form,1)

	return render_template("about.html")


def validate_login_register(form, loginFlag):
	if loginFlag == 1:
		email = request.form.get("email")
		password = request.form.get("password")
		if email and password:
			print("dolduruldu")
		else:
			print("boş")
		print("logging in")
	else:
		print("registering")











