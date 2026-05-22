import flask
import flask_login
from user.model import User
from project.db import DATABASE

def render_chat():
    if flask_login.current_user.is_authenticated:
        login = True
        return flask.render_template("chat.html",login=login)
    else:
        return flask.redirect("/register")



def get_data():
    if flask.request.method == "POST":
        first_name = flask.request.form.get("first_name")
        last_name = flask.request.form.get("last_name")
        username = flask.request.form.get("username")
        gender = flask.request.form.get("gender")
        birth_date = flask.request.form.get("birth_date")
        print(flask_login.current_user.id)
        user = User.query.filter_by(id = flask_login.current_user.id).scalar()
        if user is not None:
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.gender = gender
            user.age = birth_date

            DATABASE.session.commit()
            return flask.redirect("/")
