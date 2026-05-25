from project.db import DATABASE
from user.model import *


class Chat(DATABASE.Model):
    id = DATABASE.Column(DATABASE.Integer, primary_key= True)
    name_chat = DATABASE.Column(DATABASE.String, nullable= False)
    img_chat = DATABASE.Column(DATABASE.String, nullable=False)
    last_msg = DATABASE.Column(DATABASE.String, nullable = False)
    creator_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("user.id"), nullable= False)
    users = DATABASE.relationship('User', secondary = 'user_chat', back_populates = 'chats')


class UserChat(DATABASE.Model):
    id = DATABASE.Column(DATABASE.Integer, primary_key = True)
    chat_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("chat.id"))
    user_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("user.id"))
