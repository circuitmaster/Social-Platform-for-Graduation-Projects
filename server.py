from flask import Flask, request
import views

app = Flask(__name__)
app.secret_key = "123base321"
app.config.from_object("settings")

app.add_url_rule("/", methods = ['GET', 'POST'], view_func=views.home_page)
app.add_url_rule("/about", methods = ['GET', 'POST'], view_func=views.about_page)
app.add_url_rule("/user", methods = ['GET', 'POST'], view_func=views.user_page)
app.add_url_rule("/add_project", methods = ['GET', 'POST'], view_func=views.add_project)
app.add_url_rule("/logout", view_func=views.logout)


if __name__ == "__main__":
    port = app.config.get("PORT")
    app.run(host="localhost", port=port)