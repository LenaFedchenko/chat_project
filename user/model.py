from project.db import DATABASE
import flask_login

class User(DATABASE.Model, flask_login.UserMixin):
    id = DATABASE.Column(DATABASE.Integer, primary_key= True)
    email = DATABASE.Column(DATABASE.String, nullable= False, unique= True)
    password = DATABASE.Column(DATABASE.String, nullable= False)
    is_verified = DATABASE.Column(DATABASE.Boolean, nullable = False, default = False)

    first_name = DATABASE.Column(DATABASE.String, nullable= False, default= "Null")
    last_name = DATABASE.Column(DATABASE.String, nullable= False, default= "Null")
    username = DATABASE.Column(DATABASE.String, nullable= False, default= "Null" , unique= True)
    gender = DATABASE.Column(DATABASE.String, nullable= False, default= "Null")
    age = DATABASE.Column(DATABASE.String, nullable= False, default= "Null")
    
    
    chats = DATABASE.relationship(
        "Chat",
        secondary = "user_chat",
        back_populates = "users"
    )
    