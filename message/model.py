from project.db import DATABASE
from datetime import datetime

class Message(DATABASE.Model):
    id = DATABASE.Column(DATABASE.Integer, primary_key= True)
    text_of_message = DATABASE.Column(DATABASE.String, nullable= False)
    time_of_msg = DATABASE.Column(DATABASE.DateTime, default = datetime.now)
    chat_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("chat.id"), nullable = False)
    user_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("user.id"), nullable = False)
    
    chat = DATABASE.relationship("Chat", back_populates = "messages")
    user = DATABASE.relationship("User", back_populates = "messages")
    
