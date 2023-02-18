from flask import Flask, request, render_template
from datetime import timedelta
import views

app = Flask(__name__)
# secret key for handling session
app.secret_key = ""
app.config.from_object("settings")
app.permanent_session_lifetime = timedelta(minutes=60)

# url rules
app.add_url_rule("/", methods = ['GET', 'POST'], view_func=views.home_page)
app.add_url_rule("/about", methods = ['GET', 'POST'], view_func=views.about_page)
app.add_url_rule("/user", methods = ['GET', 'POST'], view_func=views.user_page)
app.add_url_rule("/add_project", methods = ['GET', 'POST'], view_func=views.add_project)
app.add_url_rule("/logout", view_func=views.logout)
app.add_url_rule("/prj=<prj_id>", methods = ['GET', 'POST'], view_func=views.project)
app.add_url_rule("/livesearch=<search_pattern>", methods = ['GET', 'POST'], view_func=views.livesearch)
app.add_url_rule("/interest", methods = ['GET', 'POST'], view_func=views.interest)
app.add_url_rule("/my_projects", methods = ['GET', 'POST'], view_func=views.my_projects)
app.add_url_rule("/edit_prj=<prj_id>", methods = ['GET', 'POST'], view_func=views.edit_project)

# custom not found page function
@app.errorhandler(404)
def not_found(e):
	return render_template("not_found.html", errordict = {})

if __name__ == "__main__":
    port = app.config.get("PORT")
    app.run(host="0.0.0.0", port=port)
