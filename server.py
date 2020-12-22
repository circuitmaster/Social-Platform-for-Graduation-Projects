from flask import Flask, request
import views

app = Flask(__name__)
app.config.from_object("settings")

app.add_url_rule("/", methods = ['GET', 'POST'], view_func=views.home_page)
app.add_url_rule("/about", methods = ['GET', 'POST'], view_func=views.about_page)


if __name__ == "__main__":
    port = app.config.get("PORT")
    app.run(host="localhost", port=port)