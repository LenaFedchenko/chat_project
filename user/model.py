from project.db import DATABASE
import flask_login

class User(DATABASE.Model, flask_login.UserMixin):
    id = DATABASE.Column(DATABASE.Integer, primary_key= True)
    email = DATABASE.Column(DATABASE.String, nullable= False, unique= True)
    password = DATABASE.Column(DATABASE.String, nullable= False)

