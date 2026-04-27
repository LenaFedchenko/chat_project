from project.db import DATABASE

class User(DATABASE.Model):
    
    id = DATABASE.Column(DATABASE.Integer, primary_key= True)
    email = DATABASE.Column(DATABASE.String, nullable= False)
    password = DATABASE.Column(DATABASE.String, nullable= False)

