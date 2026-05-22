from project.db import DATABASE



class Chat(DATABASE.Model):
    id = DATABASE.Column(DATABASE.Integer, primary_key= True)
    name_chat = DATABASE.Column(DATABASE.String, nullable= False)

