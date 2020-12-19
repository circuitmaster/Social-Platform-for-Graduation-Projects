from flask import Flask, request
#from flask_mysqldb import MySQL
import views


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")
    #mysql = MySQL(app)

    app.add_url_rule("/", methods = ['GET', 'POST'], view_func=views.home_page)
    app.add_url_rule("/about", methods = ['GET', 'POST'], view_func=views.about_page)
   

    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT")
    app.run(host="localhost", port=port)