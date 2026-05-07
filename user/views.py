import flask
import werkzeug.security as security
from .model import User
from project.db import DATABASE
import flask_login


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
                return flask.redirect('/')

    return flask.render_template("register.html")


def render_login():
    email = flask.request.form.get('email')
    password = flask.request.form.get("password")
    
    if email and password:
        user = User.query.filter_by(email = email).scalar()
        print(user)
        is_hash_password = security.check_password_hash(user.password, password)

        if is_hash_password == True:
            flask_login.login_user(user)
            return flask.redirect('/')

    return flask.render_template("login.html")