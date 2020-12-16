from flask import render_template, request

#registering = False
#logging = False

def home_page():
	#registering = False
	#logging = False
	#if request.method == "POST":
	#	if request.form.get("register"):
	#		registering = True
	#	elif request.form.get("login"):
	#		logging = True
	return render_template("home.html")

def about_page():
	return render_template("about.html")