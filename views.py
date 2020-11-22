from flask import render_template

def home_page():
    return render_template("home.html")

def about_page():
	return render_template("about.html")