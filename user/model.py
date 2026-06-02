from project.db import DATABASE
import flask_login


class User(DATABASE.Model, flask_login.UserMixin):
    id = DATABASE.Column(DATABASE.Integer, primary_key=True)

    email = DATABASE.Column(DATABASE.String, nullable=False, unique=True)
    password = DATABASE.Column(DATABASE.String, nullable=False)
    is_verified = DATABASE.Column(DATABASE.Boolean, nullable=False, default=False)

    first_name = DATABASE.Column(DATABASE.String, nullable=True)
    last_name = DATABASE.Column(DATABASE.String, nullable=True)
    username = DATABASE.Column(DATABASE.String, nullable=True, unique=True)
    gender = DATABASE.Column(DATABASE.String, nullable=True)
    age = DATABASE.Column(DATABASE.Integer, nullable=True)

    chats = DATABASE.relationship(
        "Chat",
        secondary="user_chat",
        back_populates="users"
    )

    messages = DATABASE.relationship(
        "Message",
        back_populates="user",
        cascade="all, delete-orphan"
    )