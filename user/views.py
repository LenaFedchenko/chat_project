import flask
from .model import User
from project.db import DATABASE

def render_register():

    if flask.request.method == "POST":
        email = flask.request.form["email"]
        password = flask.request.form["password"]
    
        if email and password:

            user = User(
                email = email,
                password = password
            )
            DATABASE.session.add(user)
            DATABASE.session.commit()

    return flask.render_template("register.html")