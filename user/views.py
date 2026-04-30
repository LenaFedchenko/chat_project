import flask
import werkzeug.security as security
from .model import User
from project.db import DATABASE


def render_register():

    if flask.request.method == "POST":
        email = flask.request.form["email"]
        password = flask.request.form["password"]
        if email and password:
            email_user = User.query.filter_by(email=email).first()
            if email_user == None:
                hashed_password = security.generate_password_hash(password)
                user = User(
                    email = email,
                    password = hashed_password
                )
                DATABASE.session.add(user)
                DATABASE.session.commit()

    return flask.render_template("register.html")